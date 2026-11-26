"""一致性检查的命令行入口（M13，DEVPLAN T18）。在 backend/ 目录、main 环境下运行：

    python -m app.modules.consistency check [--json] [--min-age 秒]
    python -m app.modules.consistency repair --fix 类别 [--fix 类别 ...] [--force] [--yes]

check 只读，不修改任何东西。repair 必须用 --fix 显式列出要修的类别；
不加 --yes 时只打印将要做什么（演练），加上才真正执行。

修复类别：
    index            按数据库重建单个文档在三个索引（doc_meta、chunks、image_vectors）里的数据，
                     或撤掉已删除文档的残留
    db-chunks        删掉数据库里不属于文档当前解析版本的片段
    ocr-results      删掉不属于当前版本任何 OCR 对象的识别结果
    cleanup-tasks    为已删除但没有清理任务的文档补建 cleanup 任务
    temp-files       删掉过期的上传临时文件
    orphan-files     删掉数据库里没有记录的已存储文件
    embeddings       删掉不再被任何图片使用的向量记录（image_embeddings）
    rebuild-indices  删掉三个索引，按版本库的 mapping 重建，并从数据库全量重新索引
                     （执行前先停掉通用 Worker 和 OCR Worker）。默认只在检查发现索引缺失
                     或结构不一致时执行；加 --force 无条件执行（T24d），例如改了检查比较不到的
                     设置（search_analyzer 等）之后。--force 同样要加 --yes 才真正执行

正在解析或识别（有 pending / processing 的 parse、ocr 任务）的文档，片段与索引类的检查和修复
都跳过它：处理过程中的中间状态不是不一致。

和其他后端命令一样读取完整的后端配置，所以 .env 里的必填项（含 JWT_SECRET）都要有。

退出码：0 没有发现问题（或修复完成）；2 发现了问题；1 配置、数据库出错，或检索服务不可用
（检索服务不可用时仍会报告数据库和磁盘的检查结果；repair 要修索引类别而检索服务不可用时，
其余类别照常修复，索引类别跳过，退出码同样是 1）。
"""

import argparse
import json
import sys
from collections import Counter

from shared.text_index import client_from_settings
from sqlalchemy.exc import OperationalError

from app.config import load_settings
from app.core.errors import ConfigError
from app.db.session import make_engine, make_session_factory
from app.modules.consistency.analyze import DEFAULT_MIN_AGE_SECONDS, analyze
from app.modules.consistency.collect import collect_db, collect_disk, collect_index
from app.modules.consistency.model import (
    REPAIR_INDEX,
    REPAIR_KINDS,
    REPAIR_REBUILD_INDICES,
    Issue,
    Snapshot,
)
from app.modules.consistency.repair import apply, plan
from app.modules.storage import LocalStorage

# 需要检索服务才能检查和修复的类别
INDEX_KINDS = (REPAIR_INDEX, REPAIR_REBUILD_INDICES)


def _print_issues(issues: list[Issue]) -> None:
    if not issues:
        print("没有发现不一致。")
        return
    counts = Counter(issue.kind for issue in issues)
    print(f"发现 {len(issues)} 处不一致：")
    for kind, count in sorted(counts.items()):
        print(f"  {kind}：{count}")
    print()
    for issue in issues:
        where = f"[{issue.document_id}] " if issue.document_id else ""
        how = f"（可修复：--fix {issue.repair}）" if issue.repair else "（需人工处理）"
        print(f"- {issue.kind} {where}{issue.detail}{how}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m app.modules.consistency")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="对账数据库、磁盘和三个索引，只读")
    check.add_argument("--json", action="store_true", help="以 JSON 输出，便于脚本处理")
    repair = sub.add_parser("repair", help="修复指定类别的不一致")
    repair.add_argument("--fix", action="append", choices=REPAIR_KINDS, required=True)
    repair.add_argument("--yes", action="store_true", help="真正执行；不加时只演练")
    repair.add_argument(
        "--force",
        action="store_true",
        help="与 --fix rebuild-indices 一起用：检查没发现问题也重建三个索引；仍需 --yes 才执行",
    )
    for p in (check, repair):
        p.add_argument(
            "--min-age",
            type=float,
            default=DEFAULT_MIN_AGE_SECONDS,
            help="文件至少存在多少秒才算残留（避开正在进行的上传），默认 3600",
        )
    args = parser.parse_args(argv)
    if args.command == "repair" and args.force and "rebuild-indices" not in args.fix:
        # 退出码 2（argparse 的惯例），在读配置、连数据库之前就拦下
        parser.error("--force 只能和 --fix rebuild-indices 一起使用")

    try:
        settings = load_settings()
    except ConfigError as exc:
        print(exc, file=sys.stderr)
        return 1

    engine = make_engine(
        settings.database_url, connect_timeout_seconds=settings.database_connect_timeout_seconds
    )
    client = client_from_settings(settings)
    try:
        with make_session_factory(engine)() as session:
            try:
                db = collect_db(session)
            except OperationalError as exc:
                print(f"无法连接数据库（{type(exc).__name__}），检查中止", file=sys.stderr)
                return 1
            index = collect_index(client)
            snapshot = Snapshot(db=db, disk=collect_disk(settings.storage_root), index=index)
            issues = analyze(snapshot, min_age_seconds=args.min_age)

            if args.command == "check":
                if args.json:
                    print(
                        json.dumps(
                            {
                                "index_available": index.available,
                                "index_error": index.error,
                                "issues": [i.to_json() for i in issues],
                            },
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                else:
                    _print_issues(issues)
                if not index.available:
                    print(
                        f"\n检索服务不可用（{index.error}），没有检查索引；以上只是数据库和磁盘的结果",
                        file=sys.stderr,
                    )
                    return 1
                return 2 if issues else 0

            # 检索服务不可用时索引没有被检查，索引类的问题一条也不会出现在 issues 里。
            # 这时不能说“没有需要修复的问题”并返回 0：其余类别照常处理，最后以退出码 1 结束
            skipped_kinds = (
                [] if index.available else [k for k in INDEX_KINDS if k in set(args.fix)]
            )
            index_skipped = bool(skipped_kinds)
            if index_skipped:
                print(
                    f"检索服务不可用（{index.error}），没有检查索引，"
                    f"{'、'.join(skipped_kinds)} 这次不会修复；检索服务恢复后请重新运行。",
                    file=sys.stderr,
                )
            # 检索服务不可用时不强制：重建需要检索服务，上面已经说明这次不修索引
            selected = plan(issues, args.fix, force_rebuild=args.force and index.available)
            if not selected:
                if not index_skipped:
                    print("所选类别下没有需要修复的问题。")
                    return 0
                # 索引没检查过，不能笼统地说“没有需要修复的问题”；只对检查过的类别这样说（T24af）
                checked = [k for k in REPAIR_KINDS if k in set(args.fix) - set(skipped_kinds)]
                if checked:
                    print(f"其余所选类别（{'、'.join(checked)}）下没有需要修复的问题。")
                return 1
            print(f"将要修复 {len(selected)} 处：")
            for issue in selected:
                where = f"[{issue.document_id}] " if issue.document_id else ""
                print(f"- {issue.repair}：{issue.kind} {where}{issue.detail}")
            if "rebuild-indices" in args.fix and not index_skipped:
                print(
                    "\n注意：重建索引前请先停掉通用 Worker 和 OCR Worker，重建期间检索结果不完整。"
                )
            if not args.yes:
                print("\n这是演练，没有改动任何东西。确认无误后加上 --yes 执行。")
                return 2
            report = apply(
                selected,
                session=session,
                client=client if index.available else None,
                storage=LocalStorage(settings.storage_root),
                storage_root=settings.storage_root,
            )
            print()
            for line in report.done:
                print(f"已完成：{line}")
            for line in report.skipped:
                print(f"已跳过：{line}")
            return 1 if index_skipped else 0
    finally:
        client.close()
        engine.dispose()


if __name__ == "__main__":
    sys.exit(main())
