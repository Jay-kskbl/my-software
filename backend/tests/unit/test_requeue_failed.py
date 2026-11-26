"""T24ae：把失败的 embed、ocr 任务成批放回队列。挑选规则和命令流程，不需要数据库。"""

import uuid
from types import SimpleNamespace

import pytest
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import OperationalError

from app.core.errors import ConfigError
from app.modules.documents import __main__ as cli
from app.modules.documents import requeue as module
from app.modules.documents.requeue import FailedTask, RequeuePlan, plan_requeue, requeue

V1 = "c1-m500-o50-aaaaaaaaaaaa"
V2 = "c1-m300-o50-bbbbbbbbbbbb"


def failed(task_type="embed", *, error="ClipUnavailable: 连接失败", **kwargs) -> FailedTask:
    values = {
        "id": uuid.uuid4(),
        "task_type": task_type,
        "document_id": uuid.uuid4(),
        "payload": {"image_id": "x"} if task_type == "embed" else {"parse_version": V1},
        "error": error,
        "document_deleted": False,
        "parse_version": V1,
    }
    return FailedTask(**{**values, **kwargs})


# ---- 挑选 ----


def test_failed_tasks_of_live_documents_are_selected():
    tasks = [failed(), failed("ocr")]

    assert plan_requeue(tasks) == RequeuePlan(tuple(tasks), 0, 0)


def test_deleted_documents_are_skipped():
    plan = plan_requeue([failed(document_deleted=True), failed("ocr", document_deleted=True)])

    assert plan.tasks == () and plan.skipped_deleted == 2


@pytest.mark.parametrize(
    "changes",
    [
        {"payload": {"parse_version": V2}},
        {"payload": None},
        {"payload": {}},
        {"parse_version": None},
    ],
)
def test_ocr_tasks_of_other_versions_are_skipped(changes):
    plan = plan_requeue([failed("ocr", **changes)])

    assert plan.tasks == () and plan.skipped_old_version == 1


def test_embed_does_not_depend_on_the_parse_version():
    # 向量只取决于图片内容和模型（D35），重新解析过的文档照样要补
    assert len(plan_requeue([failed(parse_version=None)]).tasks) == 1


def test_reasons_are_counted_and_shortened():
    long = "x" * 500
    plan = plan_requeue(
        [failed(error="A\n详细"), failed(error="A"), failed(error=None), failed(error=long)]
    )

    reasons = plan.reasons()
    assert reasons[0] == ("A", 2)
    assert ("（没有记录原因）", 1) in reasons
    assert all(len(reason) <= 101 for reason, _ in reasons)


def test_document_count_counts_each_document_once():
    same = uuid.uuid4()

    assert plan_requeue([failed(document_id=same), failed(document_id=same)]).document_count == 1


# ---- 放回队列的语句 ----


class FakeSession:
    def __init__(self, rowcount: int = 0) -> None:
        self.statements: list = []
        self.commits = 0
        self._rowcount = rowcount

    def execute(self, statement):
        self.statements.append(statement)
        return SimpleNamespace(rowcount=self._rowcount)

    def commit(self) -> None:
        self.commits += 1


def test_requeue_resets_the_same_columns_as_a_manual_retry():
    session = FakeSession(rowcount=1)
    task = failed()

    assert requeue(session, RequeuePlan((task,))) == 1

    compiled = session.statements[0].compile(dialect=postgresql.dialect())
    sql = str(compiled)
    assert "processing_tasks.status = " in sql  # 只动此刻仍为 failed 的
    assert "failed" in compiled.params.values()
    values = session.statements[0]._values
    assigned = {column.name: getattr(value, "value", value) for column, value in values.items()}
    assert assigned == {
        "status": "pending",
        "attempts": 0,
        "error": None,
        "started_at": None,
        "finished_at": None,
        "lease_expires_at": None,
        "claimed_by": None,
    }
    assert session.commits == 1


def test_requeue_with_nothing_to_do_does_not_touch_the_database():
    session = FakeSession()

    assert requeue(session, RequeuePlan()) == 0
    assert session.statements == [] and session.commits == 0


# ---- 命令 ----


@pytest.fixture
def calls(monkeypatch):
    """换掉读库和写库，记录有没有真的执行。"""
    state = SimpleNamespace(tasks=[], executed=[])
    monkeypatch.setattr(cli, "load_failed_tasks", lambda _session, kind: state.tasks)

    def fake_requeue(_session, plan):
        state.executed.append(plan)
        return len(plan.tasks)

    monkeypatch.setattr(cli, "requeue", fake_requeue)
    return state


def test_dry_run_lists_and_changes_nothing(calls, capsys):
    calls.tasks = [failed(), failed()]

    assert cli.cmd_requeue_failed(None, "embed", yes=False) == 0

    out = capsys.readouterr().out
    assert "2 个失败的 embed 任务" in out and "2 个：ClipUnavailable" in out and "演练" in out
    assert calls.executed == []


def test_yes_requeues_only_the_selected_tasks(calls, capsys):
    keep = failed("ocr")
    calls.tasks = [keep, failed("ocr", document_deleted=True), failed("ocr", parse_version=V2)]

    assert cli.cmd_requeue_failed(None, "ocr", yes=True) == 0

    assert calls.executed == [RequeuePlan((keep,), 1, 1)]
    out = capsys.readouterr().out
    assert "已放回队列 1 个 ocr 任务" in out and "OCR Worker" in out
    assert "文档已删除" in out and "旧的解析版本" in out


def test_nothing_to_do(calls, capsys):
    assert cli.cmd_requeue_failed(None, "embed", yes=True) == 0
    assert "没有需要放回队列的 embed 任务" in capsys.readouterr().out
    assert calls.executed == []


@pytest.mark.parametrize("argv", [["requeue-failed"], ["requeue-failed", "--type", "parse"], []])
def test_bad_arguments_exit_2_before_reading_the_config(monkeypatch, argv):
    monkeypatch.setattr(cli, "load_settings", lambda: pytest.fail("不应读配置"))

    with pytest.raises(SystemExit) as excinfo:
        cli.main(argv)
    assert excinfo.value.code == 2


def test_config_error_exits_1(monkeypatch, capsys):
    def broken():
        raise ConfigError("缺少必填环境变量：DATABASE_URL")

    monkeypatch.setattr(cli, "load_settings", broken)

    assert cli.main(["requeue-failed", "--type", "embed"]) == 1
    assert "DATABASE_URL" in capsys.readouterr().err


def test_database_error_exits_1_without_leaking_the_address(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "load_settings",
        lambda: SimpleNamespace(
            database_url="postgresql://u:secret@h:1/d", database_connect_timeout_seconds=5
        ),
    )

    def unreachable(_session, _kind):
        raise OperationalError("SELECT 1", {}, Exception("could not connect to h:1 user u"))

    monkeypatch.setattr(cli, "load_failed_tasks", unreachable)

    assert cli.main(["requeue-failed", "--type", "embed"]) == 1
    err = capsys.readouterr().err
    assert "无法连接数据库（OperationalError）" in err
    assert "secret" not in err and "h:1" not in err


def test_load_query_only_reads_failed_tasks_of_the_type():
    class Session:
        statement = None

        def execute(self, statement):
            Session.statement = statement
            return []

    assert module.load_failed_tasks(Session(), "embed") == []

    compiled = Session.statement.compile(dialect=postgresql.dialect())
    assert {"failed", "embed"} <= set(compiled.params.values())
    assert "JOIN documents" in str(compiled)
