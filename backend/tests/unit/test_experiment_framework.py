"""T19：数据集校验、实验配置、运行器（检索函数是假的）、validate 命令。

这里用的都是合成的小数据，只验证框架本身；得到的数字不是实验结果。
"""

import json
from pathlib import Path

import pytest

from app.modules.experiments import (
    DatasetError,
    SearchFailed,
    SearchResult,
    load_config,
    load_dataset,
    run_queries,
)
from app.modules.experiments.__main__ import main
from app.modules.experiments.config import ExperimentConfig
from app.modules.experiments.dataset import (
    EXPERIMENTS_DIR,
    load_document_map,
    save_document_map,
)
from app.modules.experiments.runner import RankedDocument

MANIFEST = (
    "file_id,path,type,source,notes\n"
    "f1,a.pdf,pdf,自建,\n"
    "f2,b.png,image,自拍,无文字\n"
    "f3,c.docx,docx,课程资料,\n"
)
QUERIES = "query_id\ttype\ttext\nq1\ttext\t报销标准\nq2\tvisual\t蓝色的天空\nq3\tmixed\t会议照片\n"
QRELS = "query_id\tfile_id\tgrade\nq1\tf1\t3\nq1\tf3\t1\nq2\tf2\t2\n"


def make_root(tmp_path: Path, *, manifest=MANIFEST, queries=QUERIES, qrels=QRELS) -> Path:
    root = tmp_path / "experiments"
    (root / "datasets" / "files").mkdir(parents=True)
    (root / "qrels").mkdir()
    for name in ("a.pdf", "b.png", "c.docx"):
        (root / "datasets" / "files" / name).write_bytes(b"x")
    (root / "datasets" / "manifest.csv").write_text(manifest, encoding="utf-8")
    (root / "queries.tsv").write_text(queries, encoding="utf-8")
    (root / "qrels" / "week1.tsv").write_text(qrels, encoding="utf-8")
    return root


# ---- 数据集 ----


def test_valid_dataset_loads_with_summary(tmp_path):
    dataset = load_dataset(make_root(tmp_path))

    assert set(dataset.files) == {"f1", "f2", "f3"}
    assert dataset.qrels == {"q1": {"f1": 3, "f3": 1}, "q2": {"f2": 2}}
    summary = dataset.summary()
    assert summary["queries_by_type"] == {"mixed": 1, "text": 1, "visual": 1}
    assert summary["queries_without_relevant"] == ["q3"]
    assert summary["relevant_pairs"] == 3


def test_qrels_can_be_split_across_files(tmp_path):
    root = make_root(tmp_path)
    (root / "qrels" / "week2.tsv").write_text(
        "query_id\tfile_id\tgrade\nq3\tf2\t1\nq1\tf1\t3\n", encoding="utf-8"
    )

    dataset = load_dataset(root)

    assert dataset.qrels["q3"] == {"f2": 1}


def test_all_problems_are_reported_at_once(tmp_path):
    root = make_root(
        tmp_path,
        manifest=MANIFEST + "f1,dup.pdf,pdf,x,\nf4,../etc/passwd,pdf,x,\nf5,missing.pdf,word,,\n",
        queries=QUERIES + "q4\tother\t文本\n",
        qrels=QRELS + "q9\tf1\t1\nq1\tf9\t1\nq1\tf3\t5\n",
    )

    with pytest.raises(DatasetError) as excinfo:
        load_dataset(root)

    text = "\n".join(excinfo.value.problems)
    for expected in [
        "file_id f1 重复",
        "path 必须是相对",
        "type 只能是",
        "source 为空",
        "原文件不存在",
        "q9 不在 queries.tsv",
        "f9 不在 manifest.csv",
        "grade 必须是 0 到 3",
    ]:
        assert expected in text


@pytest.mark.parametrize("grade", ["²", "-1", "1.0", "", "4", "１"])
def test_grade_that_is_not_a_plain_integer_is_reported_not_a_crash(tmp_path, grade):
    root = make_root(tmp_path, qrels=QRELS + f"q1\tf3\t{grade}\n")

    with pytest.raises(DatasetError) as excinfo:
        load_dataset(root)

    assert "grade 必须是 0 到 3" in "\n".join(excinfo.value.problems)


def test_contradicting_judgements_are_an_error(tmp_path):
    root = make_root(tmp_path)
    (root / "qrels" / "week2.tsv").write_text(
        "query_id\tfile_id\tgrade\nq1\tf1\t0\n", encoding="utf-8"
    )

    with pytest.raises(DatasetError, match="两处矛盾"):
        load_dataset(root)


def test_wrong_header_and_missing_qrels_are_reported(tmp_path):
    root = make_root(tmp_path, queries="id\ttext\nq1\t报销\n")
    (root / "qrels" / "week1.tsv").unlink()

    with pytest.raises(DatasetError) as excinfo:
        load_dataset(root)

    assert any("表头应为" in p for p in excinfo.value.problems)
    assert any("没有任何 .tsv" in p for p in excinfo.value.problems)


def test_comments_and_blank_lines_are_ignored(tmp_path):
    root = make_root(tmp_path, queries=QUERIES + "\n# 下周再补\n")

    assert len(load_dataset(root).queries) == 3


def test_document_map_round_trip(tmp_path):
    root = tmp_path / "experiments"
    assert load_document_map(root) == {}

    save_document_map({"f2": ("d2", "s2"), "f1": ("d1", "s1")}, root)

    assert load_document_map(root) == {"f1": ("d1", "s1"), "f2": ("d2", "s2")}


def test_templates_in_the_repository_have_the_right_headers():
    # 仓库里的空模板：表头正确，只是还没有数据（评测数据由 Barry 提供）
    dataset = load_dataset(EXPERIMENTS_DIR)

    assert dataset.summary()["files"] >= 0


# ---- 实验配置 ----


ALL_CONFIGS = [
    "B0",
    "B1",
    "B2",
    "B3",
    "B3-no-ocr",
    "B3-no-clip",
    "clip-only",
    "B3-k10",
    "B3-k30",
    "B3-k100",
]


def test_repository_has_exactly_the_planned_configs():
    names = sorted(p.stem for p in (EXPERIMENTS_DIR / "configs").glob("*.json"))
    assert names == sorted(ALL_CONFIGS)


@pytest.mark.parametrize("name", ALL_CONFIGS)
def test_repository_configs_load_and_differ_only_by_switches(name):
    config = load_config(EXPERIMENTS_DIR / "configs" / f"{name}.json")

    assert config.name == name
    config.check_against(100)


def test_b0_b1_b2_are_the_globally_defined_baselines():
    b0, b1, b2 = (load_config(EXPERIMENTS_DIR / "configs" / f"B{i}.json") for i in range(3))

    assert b0.channels == {"meta": True, "text": False, "image": False}
    assert (b1.channels, b1.source_types) == (
        {"meta": False, "text": True, "image": False},
        ["body"],
    )
    assert (b2.channels, sorted(b2.source_types)) == (b1.channels, ["body", "ocr"])


def load_named(name: str):
    return load_config(EXPERIMENTS_DIR / "configs" / f"{name}.json")


def test_b3_and_ablations_differ_from_b3_only_in_the_ablated_switch():
    b3 = load_named("B3")
    assert b3.channels == {"meta": True, "text": True, "image": True}
    assert sorted(b3.source_types) == ["body", "ocr"]
    # B3 的 k 来自后端配置（默认 60），k 值消融只覆盖 k
    assert b3.rrf_k is None

    def same_except(other, **changed):
        fields = {"channels", "source_types", "top_k", "ks", "rrf_k"}
        for field in fields - set(changed):
            got, want = getattr(other, field), getattr(b3, field)
            if field == "source_types":
                got, want = sorted(got), sorted(want)
            assert got == want, (other.name, field)
        for field, value in changed.items():
            assert getattr(other, field) == value, (other.name, field)

    same_except(load_named("B3-no-ocr"), source_types=["body"])
    same_except(load_named("B3-no-clip"), channels={"meta": True, "text": True, "image": False})
    same_except(load_named("clip-only"), channels={"meta": False, "text": False, "image": True})
    for k in (10, 30, 100):
        same_except(load_named(f"B3-k{k}"), rrf_k=k)


def test_rrf_k_override_must_be_positive(tmp_path):
    path = tmp_path / "c.json"
    path.write_text(
        json.dumps(
            {"name": "X", "channels": {"meta": True, "text": True, "image": False}, "rrf_k": 0}
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="rrf_k"):
        load_config(path)


@pytest.mark.parametrize(
    "data, message",
    [
        ({"name": "B9", "channels": {"meta": True}}, "三个通道"),
        ({"name": "B9", "channels": {"meta": False, "text": False, "image": False}}, "至少"),
        ({"name": "../x", "channels": {"meta": True, "text": False, "image": False}}, "只能包含"),
        (
            {"name": "B9", "channels": {"meta": True, "text": False, "image": False}, "x": 1},
            "Extra",
        ),
    ],
)
def test_invalid_configs_are_rejected(tmp_path, data, message):
    path = tmp_path / "c.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        load_config(path)


def test_top_k_must_cover_the_largest_k_and_respect_the_backend_limit():
    config = ExperimentConfig(
        name="X", channels={"meta": True, "text": False, "image": False}, top_k=10, ks=[5, 20]
    )

    with pytest.raises(ValueError, match="不能小于最大的 K"):
        config.check_against(100)
    with pytest.raises(ValueError, match="SEARCH_MAX_TOP_K"):
        config.model_copy(update={"top_k": 200, "ks": [5]}).check_against(100)


# ---- 运行器 ----

CONFIG = ExperimentConfig(
    name="T", channels={"meta": False, "text": True, "image": False}, top_k=5, ks=[1, 3]
)
DOC_TO_FILE = {"d1": "f1", "d2": "f2", "d3": "f3"}


def fake_search(answers: dict[str, list[str]], *, fail: set[str] = frozenset(), status=None):
    calls: list[str] = []

    def search(text: str) -> SearchResult:
        calls.append(text)
        if text in fail:
            raise SearchFailed("检索服务暂时不可用")
        return SearchResult(
            ranking=[
                RankedDocument(document_id=d, score=1.0 / (i + 1), channels=[{"channel": "text"}])
                for i, d in enumerate(answers.get(text, []))
            ],
            took_ms=10 + len(calls),
            channel_status=status or {"meta": "disabled", "text": "ok", "image": "disabled"},
        )

    search.calls = calls  # type: ignore[attr-defined]
    return search


def test_run_records_rankings_and_stratified_metrics(tmp_path):
    dataset = load_dataset(make_root(tmp_path))
    search = fake_search({"报销标准": ["d1", "dX", "d3"], "蓝色的天空": ["d3", "d2"]})

    result = run_queries(CONFIG, dataset, DOC_TO_FILE, search)

    assert result.complete
    q1 = next(r for r in result.records if r["query_id"] == "q1")
    # 原始排名保存下来：数据集之外的文档 file_id 为 None
    assert [x["file_id"] for x in q1["ranking"]] == ["f1", None, "f3"]
    assert q1["outside_dataset"] == 1
    assert q1["metrics"]["P@1"] == 1.0 and q1["metrics"]["R@3"] == 1.0
    metrics = result.metrics
    # 按查询类型分层：文字型 P@1=1，视觉型 P@1=0
    assert metrics["by_type"]["text"]["P@1"]["mean"] == 1.0
    assert metrics["by_type"]["visual"]["P@1"]["mean"] == 0.0
    # 总体：q3 没有相关文件，三个指标都不计入它——P@1 = (1 + 0) / 2，条数都是 2
    assert metrics["overall"]["P@1"]["mean"] == pytest.approx(1 / 2)
    assert metrics["overall"]["P@1"]["queries"] == 2
    assert metrics["overall"]["R@3"]["queries"] == 2
    assert metrics["queries_without_relevant"] == ["q3"]
    assert metrics["latency_ms"]["searches"] == 3


def test_failed_search_is_recorded_and_never_scored_as_empty(tmp_path):
    dataset = load_dataset(make_root(tmp_path))
    search = fake_search({"报销标准": ["d1"]}, fail={"蓝色的天空"})

    result = run_queries(CONFIG, dataset, DOC_TO_FILE, search)

    assert not result.complete
    failed = next(r for r in result.records if r["query_id"] == "q2")
    assert failed["ok"] is False and "不可用" in failed["error"]
    assert "metrics" not in failed
    assert result.metrics["failed_searches"] == 1
    # 视觉型那一层只有这条失败的查询：不出现在结果里，而不是算成 0
    assert "visual" not in result.metrics["by_type"]


def test_unavailable_channel_marks_the_run_incomplete(tmp_path):
    dataset = load_dataset(make_root(tmp_path))
    status = {"meta": "disabled", "text": "ok", "image": "unavailable"}

    result = run_queries(CONFIG, dataset, DOC_TO_FILE, fake_search({}, status=status))

    assert not result.complete
    assert result.records[0]["unavailable_channels"] == ["image"]


def test_repeats_run_every_query_again_and_report_spread(tmp_path):
    dataset = load_dataset(make_root(tmp_path))
    search = fake_search({"报销标准": ["d1"]})

    result = run_queries(CONFIG, dataset, DOC_TO_FILE, search, repeats=3)

    assert len(search.calls) == 9
    assert sorted({r["repetition"] for r in result.records}) == [1, 2, 3]
    spread = result.metrics["overall"]["P@1"]["across_repeats"]
    assert spread["runs"] == 3 and spread["stdev"] == 0.0


def test_repeats_must_be_positive(tmp_path):
    with pytest.raises(ValueError):
        run_queries(CONFIG, load_dataset(make_root(tmp_path)), {}, fake_search({}), repeats=0)


# ---- validate 命令 ----


def test_validate_command_prints_the_summary(tmp_path, capsys):
    assert main(["--root", str(make_root(tmp_path)), "validate"]) == 0

    summary = json.loads(capsys.readouterr().out)
    assert summary["files"] == 3 and summary["queries"] == 3


def test_validate_command_lists_problems_and_fails(tmp_path, capsys):
    root = make_root(tmp_path, qrels="query_id\tfile_id\tgrade\nq1\tf9\t1\n")

    assert main(["--root", str(root), "validate"]) == 1
    assert "f9 不在 manifest.csv" in capsys.readouterr().err


def test_machine_info_is_collected_without_extra_packages():
    from app.modules.experiments.environment import code_versions, machine_info

    info = machine_info()
    assert info["python"] and info["cpu_count"]
    assert info["memory_bytes"] is None or info["memory_bytes"] > 0
    versions = code_versions()
    assert versions["chunker_version"] >= 1
    assert all(len(h) == 64 for h in versions["mapping_sha256"].values())
    # 三个索引的结构都记录（T24 补上图片向量索引）
    assert set(versions["mapping_sha256"]) == {"doc_meta", "chunks", "image_vectors"}


def test_git_dirty_ignores_untracked_files(tmp_path, monkeypatch):
    # T24aj：未跟踪的输出目录不算“工作区不干净”；已跟踪文件改了才算
    import subprocess

    from app.modules.experiments import environment

    def git(*args: str) -> None:
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

    git("init", "-q")
    (tmp_path / "code.py").write_text("x = 1\n", encoding="utf-8")
    git("add", "code.py")
    git("commit", "-q", "-m", "init")
    monkeypatch.setattr(environment, "PROJECT_ROOT", tmp_path)

    (tmp_path / "output").mkdir()
    (tmp_path / "output" / "result.txt").write_text("raw", encoding="utf-8")
    assert environment.machine_info()["git_dirty"] is False

    (tmp_path / "code.py").write_text("x = 2\n", encoding="utf-8")
    assert environment.machine_info()["git_dirty"] is True
