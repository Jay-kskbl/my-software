"""实验框架的命令行入口（M12，DEVPLAN T19）。在 backend/ 目录、main 环境下运行：

    python -m app.modules.experiments validate
    python -m app.modules.experiments import
    python -m app.modules.experiments run --config ../experiments/configs/B1.json [--repeat 3]
    python -m app.modules.experiments reocr [--yes]

validate  只检查 experiments/ 下的清单、查询集和标注的格式，不连数据库。
import    以实验专用的管理员账号上传清单里的文件（已导入的按内容哈希跳过），
          生成 datasets/document_map.csv。之后要启动 Worker 完成解析和 OCR。
run       运行一组实验，结果写到 experiments/runs/<时间>_<名称>/，并写一条 experiment_runs 记录。
          运行前检查数据集里的文档是否都已处理成功、有没有待清理的文档；
          不满足时中止，加 --allow-incomplete 可以强行运行（结果里会记录这一点）。
reocr     把数据集文档当前解析版本的 OCR 任务放回队列，用 OCR Worker 现在的配置重新识别
          （例如改了 OCR_PDF_DPI、OCR_MIN_CONFIDENCE 之后）。不加 --yes 只列出要重做的任务。
          之后要启动 OCR Worker 处理完，run 的运行前检查会等它们完成。

退出码：0 成功；1 出错（配置、数据库、数据集不合法、运行前检查不通过）；
2 运行完成但不完整（有检索失败或本应执行的通道不可用），这样的结果不能当正式数据。
reocr：0 已放回队列，或演练成功、没有需要重做的任务；1 出错，或还有未完成的解析、OCR 任务。
"""

import argparse
import dataclasses
import hashlib
import json
import secrets
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from shared.tasks import (
    STATUS_FAILED,
    STATUS_PENDING,
    STATUS_PROCESSING,
    STATUS_SUCCEEDED,
    TASK_OCR,
    TASK_PARSE,
)
from shared.text_index import client_from_settings
from sqlalchemy import func, select, update
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.config import load_settings
from app.core.errors import ConfigError, SearchUnavailableError
from app.db.models import (
    Document,
    ExperimentRun,
    ImageAsset,
    ImageEmbedding,
    OCRResult,
    ProcessingTask,
    User,
)
from app.db.session import make_engine, make_session_factory
from app.modules.auth import create_user
from app.modules.auth.permissions import ADMIN_ROLE
from app.modules.clip import ClipClient, ClipError, query_clip_client_from_settings
from app.modules.experiments.config import load_config
from app.modules.experiments.dataset import (
    EXPERIMENTS_DIR,
    DatasetError,
    load_dataset,
    load_document_map,
    save_document_map,
)
from app.modules.experiments.environment import code_versions, machine_info, opensearch_info
from app.modules.experiments.runner import (
    RankedDocument,
    SearchFailed,
    SearchResult,
    run_queries,
)
from app.modules.search import SearchRequestData, params_from_settings, search
from app.modules.storage import LocalStorage

# 实验专用账号：检索日志里靠它与日常使用区分开
EXPERIMENT_USERNAME = "experiment"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _experiment_user(session: Session, *, create: bool) -> User | None:
    user = session.scalar(select(User).where(User.username == EXPERIMENT_USERNAME))
    if user is None and create:
        # 密码随机生成、不保存：这个账号只给命令行用，不需要登录
        user = create_user(session, EXPERIMENT_USERNAME, secrets.token_urlsafe(32), role="admin")
    if user is not None and user.role != ADMIN_ROLE:
        raise SystemExit(f"账号 {EXPERIMENT_USERNAME} 已存在但不是管理员，请换一个名字或手动处理")
    return user


# ---- validate ----


def cmd_validate(root: Path) -> int:
    try:
        dataset = load_dataset(root)
    except DatasetError as exc:
        print(f"数据集有 {len(exc.problems)} 处问题：", file=sys.stderr)
        for problem in exc.problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(json.dumps(dataset.summary(), ensure_ascii=False, indent=2))
    return 0


# ---- import ----


def cmd_import(root: Path, settings: Any, session: Session) -> int:
    from app.modules.documents.service import soft_delete_document, upload_document

    try:
        dataset = load_dataset(root)
    except DatasetError as exc:
        print("数据集不合法，先运行 validate：", *exc.problems, sep="\n  - ", file=sys.stderr)
        return 1
    user = _experiment_user(session, create=True)
    storage = LocalStorage(settings.storage_root)
    mapping = load_document_map(root)
    imported = skipped = replaced = 0
    for file in dataset.files.values():
        path = root / "datasets" / "files" / file.path
        sha = _sha256(path)
        existing = mapping.get(file.file_id)
        previous = session.get(Document, uuid.UUID(existing[0])) if existing else None
        if previous is not None and previous.deleted_at is not None:
            previous = None
        if existing and existing[1] == sha and previous is not None:
            skipped += 1
            continue
        with path.open("rb") as stream:
            # 不加标签：标签会参与 B0 的文件名/标签检索，人为加上会影响实验结果
            document = upload_document(
                session,
                storage,
                user,
                stream=stream,
                filename=path.name,
                tags=[],
                limits=_upload_limits(settings),
            )
        mapping[file.file_id] = (str(document.id), sha)
        save_document_map(mapping, root)  # 每导入一个就保存，中途失败也不丢记录
        imported += 1
        if previous is not None:
            # 文件内容换过：旧文档不再属于数据集。不删掉的话它仍会被检索到，
            # 占掉名次、改变 BM25 的统计量，而标注里并没有它（附录 A15：替换即新建，旧的按删除处理）
            soft_delete_document(session, previous)
            replaced += 1
    print(
        f"导入 {imported} 个文件（其中 {replaced} 个替换了内容已变的旧文档，旧文档已删除），"
        f"跳过 {skipped} 个已导入的。请启动 Worker 和 OCR Worker 完成处理。"
    )
    return 0


def _upload_limits(settings: Any):
    from app.modules.documents.service import UploadLimits

    # 与上传接口（api/documents.py）使用同样的限制：数据集文件和用户上传的文件走同一套校验
    return UploadLimits(
        max_bytes=settings.upload_max_bytes,
        max_filename_chars=settings.upload_max_filename_chars,
        allowed_extensions=settings.upload_allowed_extensions,
    )


# ---- run ----


def _preflight(session: Session, document_ids: list[uuid.UUID]) -> list[str]:
    """运行前检查。返回问题列表（空表示可以运行）。"""
    problems: list[str] = []
    documents = list(session.scalars(select(Document).where(Document.id.in_(document_ids))))
    found = {d.id for d in documents}
    missing = [d for d in document_ids if d not in found]
    if missing:
        problems.append(f"{len(missing)} 个数据集文件在数据库里找不到（重新运行 import）")
    deleted = [d for d in documents if d.deleted_at is not None]
    if deleted:
        problems.append(f"{len(deleted)} 个数据集文件已被删除")
    unfinished = [d for d in documents if d.deleted_at is None and d.status != "succeeded"]
    if unfinished:
        problems.append(
            f"{len(unfinished)} 个数据集文件还没有处理成功（等 Worker 处理完，或查看失败原因）"
        )
    busy = session.scalar(
        select(func.count())
        .select_from(ProcessingTask)
        .where(ProcessingTask.status.in_(("pending", "processing")))
    )
    if busy:
        problems.append(f"还有 {busy} 个未完成的任务（解析、OCR 或清理），结果可能随时变化")
    pending_cleanup = session.scalar(
        select(func.count()).select_from(Document).where(Document.deleted_at.is_not(None))
    )
    if pending_cleanup:
        # D28：管理员检索不做前置过滤，已删除未清理的文档会占通道名次，结果可能少于 top_k
        problems.append(f"有 {pending_cleanup} 个已删除但还没清理的文档，会影响管理员检索的名次")
    versions = {d.parse_version for d in documents if d.deleted_at is None}
    if len(versions) > 1:
        problems.append(f"数据集文件的解析版本不一致：{sorted(map(str, versions))}")
    # 文档状态只反映 parse 任务（D27）：某一页的 OCR 最终失败时文档仍是 succeeded，
    # 但这一页的文字不在索引里。不检查的话，B2 会在缺了 OCR 文字的数据上得出数字
    current = {d.id: d.parse_version for d in documents if d.deleted_at is None}
    failed_ocr = sum(
        1
        for document_id, payload in session.execute(
            select(ProcessingTask.document_id, ProcessingTask.payload).where(
                ProcessingTask.document_id.in_(document_ids),
                ProcessingTask.task_type == TASK_OCR,
                ProcessingTask.status == STATUS_FAILED,
            )
        )
        if document_id in current and (payload or {}).get("parse_version") == current[document_id]
    )
    if failed_ocr:
        problems.append(
            f"数据集文件有 {failed_ocr} 个 OCR 任务失败，这些页或图片的文字没有进入索引"
            "（在任务列表里查看原因并重试）"
        )
    problems += ocr_param_problems(_ocr_param_rows(session, document_ids))
    problems += ocr_model_problems(_ocr_models(session, document_ids))
    return problems


# T24c（D42）：OCR Worker 把每条识别结果实际用的参数写在 ocr_results.params 里
OCR_PARAM_KEYS = ("pdf_dpi", "min_confidence", "max_pixels")


def _ocr_param_rows(
    session: Session, document_ids: list[uuid.UUID]
) -> list[tuple[dict[str, Any], int]]:
    """数据集文档的 OCR 结果按参数分组：[(params, 条数)]。"""
    return [
        (dict(params or {}), int(count))
        for params, count in session.execute(
            select(OCRResult.params, func.count())
            .where(OCRResult.document_id.in_(document_ids))
            .group_by(OCRResult.params)
        )
    ]


def ocr_params_summary(rows: list[tuple[dict[str, Any], int]]) -> list[dict[str, Any]]:
    """记进 config.json 的形式：每种参数组合一项，按条数从多到少。"""
    summary = [{"params": params, "results": count} for params, count in rows]
    return sorted(summary, key=lambda item: (-item["results"], json.dumps(item["params"])))


def ocr_param_problems(rows: list[tuple[dict[str, Any], int]]) -> list[str]:
    """OCR 参数没有记录或前后不一致时报告问题（结果无法复现）。

    逐个参数比较，而不是比较整个组合：独立图片不渲染，pdf_dpi 为 None，
    和 PDF 页的 dpi 不同是正常的，所以 pdf_dpi 只比较非 None 的值。
    """
    problems: list[str] = []
    unrecorded = sum(count for params, count in rows if not params)
    if unrecorded:
        problems.append(
            f"有 {unrecorded} 条 OCR 结果没有记录识别参数（T24c 之前写入），"
            "无法确认用的是什么配置（运行 reocr 重新识别，或在空的实验库上重新 import 并处理）"
        )
    recorded = [params for params, _ in rows if params]
    for key in OCR_PARAM_KEYS:
        values = {params.get(key) for params in recorded}
        if key == "pdf_dpi":
            values.discard(None)
        if len(values) > 1:
            problems.append(
                f"数据集的 OCR 结果用了不同的 {key}：{sorted(values, key=str)}"
                "（处理期间改过 OCR Worker 的配置；统一配置后运行 reocr 重新识别）"
            )
    return problems


def _ocr_models(session: Session, document_ids: list[uuid.UUID]) -> list[str]:
    """数据集文档的 OCR 结果用到的模型，每项为“模型名 模型版本”，已排序。

    model_version 带两个权重文件哈希的前 8 位，换了权重也能区分（T17）。
    """
    return sorted(
        {
            f"{name} {version}"
            for name, version in session.execute(
                select(OCRResult.model_name, OCRResult.model_version)
                .where(OCRResult.document_id.in_(document_ids))
                .distinct()
            )
        }
    )


def ocr_model_problems(models: list[str]) -> list[str]:
    """数据集的 OCR 结果用了不止一个模型时报告问题（T24g）。

    OCR Worker 写入前会删掉同一文档同一对象的旧结果，每个对象只留一条，
    所以出现两个模型说明确实有一部分页或图片是用另一个模型识别的，
    B2、B3 的数字会混进两个模型的识别效果。
    """
    if len(models) <= 1:
        return []
    return [
        f"数据集的 OCR 结果用了不同的模型：{models}"
        "（处理期间换过 OCR 模型；统一后运行 reocr 重新识别。"
        "也可能是重新解析后残留的旧结果，可先用一致性检查的 ocr-results 类别清理）"
    ]


def _image_preflight(
    session: Session, document_ids: list[uuid.UUID], clip: ClipClient
) -> tuple[list[str], dict[str, Any]]:
    """开了图像通道的实验（B3 等）的运行前检查。返回（问题列表，CLIP 模型信息）。

    - CLIP 服务要能连上：否则每条查询的图像通道都会降级，结果只是文本检索；
    - 数据集里的每张图片都要有当前模型的向量：embed 任务失败或还没跑完的图片
      不在向量索引里，图像通道永远检索不到它们（文档状态不跟随 embed 任务，D27、D35）。
    模型信息（model_version 含权重文件 sha256 的前 12 位）记进 config.json（GLOBAL §3.4）。
    """
    try:
        model = clip.model()
    except ClipError as exc:
        return [f"CLIP 服务不可用（{exc.message}），图像通道无法参与检索"], {"error": exc.message}
    info = {
        "model_name": model.model_name,
        "model_version": model.model_version,
        "dim": model.dim,
    }
    missing = session.scalar(
        select(func.count())
        .select_from(ImageAsset)
        .outerjoin(
            ImageEmbedding,
            (ImageEmbedding.sha256 == ImageAsset.sha256)
            & (ImageEmbedding.model_name == model.model_name)
            & (ImageEmbedding.model_version == model.model_version),
        )
        .where(ImageAsset.document_id.in_(document_ids), ImageEmbedding.id.is_(None))
    )
    problems = []
    if missing:
        problems.append(
            f"数据集里有 {missing} 张图片还没有当前 CLIP 模型的向量"
            "（embed 任务失败或未完成；在任务列表里查看原因并重试）"
        )
    return problems, info


def _outside_dataset(session: Session, document_ids: list[uuid.UUID]) -> int:
    """库里不属于数据集的未删除文档数。

    实验账号是管理员，检索范围是全库：这些文档会被检索到、占掉名次（指标里一律算不相关），
    也会改变 BM25 的词频统计。不拦截运行，但要记进 config.json 并提示——正式实验应当在
    只装了数据集的库上做。
    """
    return int(
        session.scalar(
            select(func.count())
            .select_from(Document)
            .where(Document.deleted_at.is_(None), Document.id.not_in(document_ids))
        )
        or 0
    )


def _snapshot_versions(session: Session, document_ids: list[uuid.UUID]) -> dict[str, Any]:
    parse_versions = sorted(
        {
            v
            for v in session.scalars(
                select(Document.parse_version).where(Document.id.in_(document_ids))
            )
            if v
        }
    )
    return {
        "parse_versions": parse_versions,
        "ocr_models": _ocr_models(session, document_ids),
        "ocr_params": ocr_params_summary(_ocr_param_rows(session, document_ids)),
    }


def cmd_run(args: argparse.Namespace, root: Path, settings: Any, session: Session) -> int:
    try:
        config = load_config(Path(args.config))
        params = params_from_settings(settings)
        if config.rrf_k is not None:
            # k 值消融：只改这次实验的 k，其余参数仍来自后端配置；生效的值随结果记录
            params = dataclasses.replace(params, rrf_k=config.rrf_k)
        config.check_against(params.max_top_k)
        dataset = load_dataset(root, check_files=False)
    except (ValueError, DatasetError) as exc:
        print(exc, file=sys.stderr)
        return 1

    if not dataset.queries or not dataset.files:
        print("数据集里还没有查询或文件（见 experiments/ 下的模板），无法运行", file=sys.stderr)
        return 1
    user = _experiment_user(session, create=False)
    if user is None:
        print(f"没有实验账号 {EXPERIMENT_USERNAME}，先运行 import", file=sys.stderr)
        return 1
    mapping = load_document_map(root)
    missing = sorted(set(dataset.files) - set(mapping))
    if missing:
        print(f"{len(missing)} 个文件还没有导入（如 {missing[0]}），先运行 import", file=sys.stderr)
        return 1
    document_ids = [uuid.UUID(mapping[f][0]) for f in dataset.files]
    problems = _preflight(session, document_ids)
    clip_model: dict[str, Any] | None = None
    if config.channels["image"]:
        with query_clip_client_from_settings(settings) as clip:
            image_problems, clip_model = _image_preflight(session, document_ids, clip)
        problems += image_problems
    if problems:
        print("运行前检查没有通过：", *problems, sep="\n  - ", file=sys.stderr)
        if not args.allow_incomplete:
            return 1
        print("已指定 --allow-incomplete，继续运行；结果里会记录这些问题。", file=sys.stderr)
    outside = _outside_dataset(session, document_ids)
    if outside:
        print(
            f"提示：库里另有 {outside} 个不属于数据集的文档，它们会参与检索并占用名次；"
            "这个数目会记进 config.json。正式实验请在只有数据集的库上运行。",
            file=sys.stderr,
        )

    started = datetime.now(UTC)
    # 先建好结果目录再跑查询：名字带微秒和随机后缀，连续运行也不会重名；
    # 跑到一半出错时，至少目录和配置已经在，便于追查
    run_dir = (
        root
        / "runs"
        / f"{started.strftime('%Y%m%dT%H%M%S.%fZ')}_{config.name}_{secrets.token_hex(3)}"
    )
    run_dir.mkdir(parents=True, exist_ok=False)
    client = client_from_settings(settings)
    # 与 API 用同一种查询编码客户端和超时：实验测到的就是系统实际的行为
    query_clip = query_clip_client_from_settings(settings)
    run_row = ExperimentRun(name=config.name, config={})
    try:

        def do_search(text: str) -> SearchResult:
            try:
                outcome = search(
                    session,
                    user,
                    SearchRequestData(
                        query=text,
                        top_k=config.top_k,
                        channels=dict(config.channels),
                        source_types=list(config.source_types),
                    ),
                    client=client,
                    params=params,
                    clip=query_clip,
                )
            except SearchUnavailableError as exc:
                raise SearchFailed(exc.message) from exc
            return SearchResult(
                ranking=[
                    RankedDocument(
                        document_id=str(hit.document_id),
                        score=hit.score,
                        channels=[c.model_dump(mode="json") for c in hit.channels],
                    )
                    for hit in outcome.hits
                ],
                took_ms=outcome.took_ms,
                channel_status={r.channel: r.status for r in outcome.channels},
            )

        full_config = {
            "experiment": config.model_dump(mode="json"),
            "search_params": params.to_log(),
            "processing_params": {
                "chunk_max_chars": settings.chunk_max_chars,
                "chunk_overlap_chars": settings.chunk_overlap_chars,
                "pdf_ocr_min_chars": settings.pdf_ocr_min_chars,
            },
            "dataset": dataset.summary(),
            "documents_outside_dataset": outside,
            "versions": {**code_versions(), **_snapshot_versions(session, document_ids)},
            "opensearch": opensearch_info(client),
            # 开了图像通道时为查询编码所用的 CLIP 模型，没开时为 None
            "clip_model": clip_model,
            "machine": machine_info(),
            "preflight_problems": problems,
            "repeats": args.repeat,
            "started_at": started.isoformat(),
        }
        document_to_file = {mapping[f][0]: f for f in dataset.files}
        result = run_queries(config, dataset, document_to_file, do_search, repeats=args.repeat)
    finally:
        client.close()
        query_clip.close()

    full_config["complete"] = result.complete and not problems
    (run_dir / "config.json").write_text(
        json.dumps(full_config, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (run_dir / "results.jsonl").open("w", encoding="utf-8") as f:
        for record in result.records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    (run_dir / "metrics.json").write_text(
        json.dumps(result.metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    run_row.config = full_config
    run_row.metrics = result.metrics
    run_row.raw_results_path = run_dir.relative_to(root.parent).as_posix()
    run_row.finished_at = datetime.now(UTC)
    session.add(run_row)
    session.commit()

    print(f"结果已保存到 {run_dir}")
    overall = result.metrics.get("overall", {})
    for name in sorted(overall):
        mean = overall[name]["mean"]
        shown = "—" if mean is None else f"{mean:.4f}"
        print(f"  {name}: {shown}（{overall[name]['queries']} 条查询）")
    if not full_config["complete"]:
        print("注意：这次运行不完整（有检索失败、通道不可用或运行前检查未通过），不能当正式数据。")
        return 2
    return 0


# ---- reocr ----


def reocr_task_ids(
    tasks: list[tuple[uuid.UUID, uuid.UUID, dict[str, Any] | None, str]],
    current_versions: dict[uuid.UUID, str],
) -> list[uuid.UUID]:
    """要放回队列的 OCR 任务（T24i）。

    tasks 为（任务 id，文档 id，payload，状态）；current_versions 为未删除文档的当前解析版本。
    只要当前版本的任务：旧版本的任务即使放回队列，OCR Worker 也会按 stale-version 跳过。
    只要已结束（成功或失败）的任务：还在排队或处理中的不用动。
    """
    return [
        task_id
        for task_id, document_id, payload, status in tasks
        if status in (STATUS_SUCCEEDED, STATUS_FAILED)
        and document_id in current_versions
        and (payload or {}).get("parse_version") == current_versions[document_id]
    ]


def cmd_reocr(args: argparse.Namespace, root: Path, session: Session) -> int:
    """把数据集文档当前版本的 OCR 任务放回队列，用 OCR Worker 现在的配置重新识别（T24i）。

    复用原来的任务，而不是新建：每个页或图片仍然只有一个 OCR 任务，
    运行前检查（失败的 OCR 任务）、一致性检查（ocr_targets）、重新解析时的去重都不受影响。
    OCR Worker 重做一个对象时先删掉它的旧识别结果和旧片段（数据库和索引都是），再写新的，
    所以重做是覆盖，不会叠加（GLOBAL §3.3 幂等）。
    """
    try:
        dataset = load_dataset(root, check_files=False)
        mapping = load_document_map(root)
    except DatasetError as exc:
        print(exc, file=sys.stderr)
        return 1
    missing = sorted(set(dataset.files) - set(mapping))
    if missing:
        print(f"{len(missing)} 个文件还没有导入（如 {missing[0]}），先运行 import", file=sys.stderr)
        return 1
    document_ids = [uuid.UUID(mapping[f][0]) for f in dataset.files]
    if not document_ids:
        print("数据集里还没有文件", file=sys.stderr)
        return 1

    busy = session.scalar(
        select(func.count())
        .select_from(ProcessingTask)
        .where(
            ProcessingTask.document_id.in_(document_ids),
            ProcessingTask.task_type.in_((TASK_PARSE, TASK_OCR)),
            ProcessingTask.status.in_((STATUS_PENDING, STATUS_PROCESSING)),
        )
    )
    if busy:
        # 正在解析的文档，解析完会建新版本的 OCR 任务；正在 OCR 的任务放回队列会和它抢
        print(
            f"数据集文档还有 {busy} 个未完成的解析或 OCR 任务，等它们处理完再重新 OCR",
            file=sys.stderr,
        )
        return 1

    current = {
        document_id: version
        for document_id, version in session.execute(
            select(Document.id, Document.parse_version).where(
                Document.id.in_(document_ids), Document.deleted_at.is_(None)
            )
        )
        if version
    }
    tasks = [
        (task_id, document_id, payload, status)
        for task_id, document_id, payload, status in session.execute(
            select(
                ProcessingTask.id,
                ProcessingTask.document_id,
                ProcessingTask.payload,
                ProcessingTask.status,
            ).where(
                ProcessingTask.document_id.in_(document_ids),
                ProcessingTask.task_type == TASK_OCR,
            )
        )
    ]
    task_ids = reocr_task_ids(tasks, current)
    selected = set(task_ids)
    documents = len({document_id for task_id, document_id, _, _ in tasks if task_id in selected})
    if not task_ids:
        print("数据集文档没有需要重新 OCR 的任务（没有扫描页或图片，或还没解析完）")
        return 0
    print(f"将把 {documents} 个文档的 {len(task_ids)} 个 OCR 任务放回队列，重新识别。")
    if not args.yes:
        print("这是演练，没有改动任何数据。确认 OCR Worker 的配置后，加 --yes 执行。")
        return 0

    # 条件更新：执行前状态刚好变了的任务（例如有人同时在界面上点了重试）不动
    result = session.execute(
        update(ProcessingTask)
        .where(
            ProcessingTask.id.in_(task_ids),
            ProcessingTask.status.in_((STATUS_SUCCEEDED, STATUS_FAILED)),
        )
        .values(
            status=STATUS_PENDING,
            attempts=0,
            error=None,
            started_at=None,
            finished_at=None,
            lease_expires_at=None,
            claimed_by=None,
        )
        .execution_options(synchronize_session=False)
    )
    session.commit()
    print(
        f"已放回队列 {result.rowcount} 个 OCR 任务。启动 OCR Worker 处理完之后再运行实验；"
        "处理期间 run 的运行前检查会提示有未完成的任务。"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m app.modules.experiments")
    parser.add_argument(
        "--root",
        type=Path,
        default=EXPERIMENTS_DIR,
        help="实验目录，默认为仓库根目录的 experiments/",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="检查清单、查询集和标注的格式")
    sub.add_parser("import", help="上传数据集文件，生成 document_map.csv")
    run = sub.add_parser("run", help="运行一组实验")
    run.add_argument(
        "--config", required=True, help="实验配置文件，如 ../experiments/configs/B1.json"
    )
    run.add_argument("--repeat", type=int, default=1, help="重复运行几次，默认 1")
    run.add_argument("--allow-incomplete", action="store_true", help="运行前检查不通过时也继续")
    reocr = sub.add_parser("reocr", help="把数据集文档的 OCR 任务放回队列，重新识别")
    reocr.add_argument("--yes", action="store_true", help="真正执行；不加时只列出要重做的任务")
    args = parser.parse_args(argv)
    root: Path = args.root.resolve()

    if args.command == "validate":
        return cmd_validate(root)
    if args.command == "run" and args.repeat < 1:
        parser.error("--repeat 至少为 1")

    try:
        settings = load_settings()
    except ConfigError as exc:
        print(exc, file=sys.stderr)
        return 1
    engine = make_engine(
        settings.database_url, connect_timeout_seconds=settings.database_connect_timeout_seconds
    )
    try:
        with make_session_factory(engine)() as session:
            try:
                if args.command == "import":
                    return cmd_import(root, settings, session)
                if args.command == "reocr":
                    return cmd_reocr(args, root, session)
                return cmd_run(args, root, settings, session)
            except OperationalError as exc:
                print(f"无法连接数据库（{type(exc).__name__}）", file=sys.stderr)
                return 1
    finally:
        engine.dispose()


if __name__ == "__main__":
    sys.exit(main())
