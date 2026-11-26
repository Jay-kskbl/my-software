"""T24ba：任务失败原因的对外文字（documents/task_errors.py）。

数据库和接口的部分在 tests/integration/test_documents.py。
"""

import uuid
from datetime import UTC, datetime
from pathlib import Path

import httpx
import psycopg
import pytest
from shared.tasks import LEASE_EXPIRED_ERROR
from shared.text_index import OpenSearchClient, TextIndexError
from sqlalchemy import exc as sa_exc

from app.db.models import ProcessingTask, User
from app.modules.clip.client import ClipRejected, ClipUnavailable
from app.modules.documents.task_errors import INTERNAL, public_task_error
from app.modules.documents.tasks import to_task_out
from app.modules.parsing.errors import ParseError
from app.worker.handlers.errors import PipelineError

REPO = Path(__file__).resolve().parents[3]


def as_stored(exc: BaseException) -> str:
    """与 worker/runner.py、ocr_worker/loop.py 写进任务表的格式相同。"""
    return f"{type(exc).__name__}: {exc}"


def test_no_error_stays_none():
    assert public_task_error(None) is None


@pytest.mark.parametrize(
    "exc",
    [
        ParseError("PDF 已加密，需要口令才能读取，无法解析"),
        PipelineError("文档的原始文件不存在或无法读取，无法解析"),
        ClipUnavailable("CLIP 服务连接失败（ConnectError）"),
        ClipRejected("CLIP 服务拒绝了请求（HTTP 422，IMAGE_INVALID：图片损坏）"),
    ],
)
def test_project_errors_keep_their_message_without_the_type_name(exc):
    assert public_task_error(as_stored(exc)) == str(exc)


@pytest.mark.parametrize(
    "error",
    [
        "OcrTaskError: 文档的原始文件不存在，无法识别",
        "RenderError: PDF 第 3 页无法渲染（FzErrorSyntax）",
    ],
)
def test_ocr_worker_errors_keep_their_message(error):
    assert public_task_error(error) == error.split(": ", 1)[1]


@pytest.mark.parametrize(
    "error",
    [
        "处理超时（超过 60 秒），已终止",
        "处理超时（超过 0.5 秒），已终止",
        "识别超时（超过 120 秒），已终止",
        "子进程异常退出（退出码 -9）",
        "识别子进程异常退出（退出码 None）",
        "租约已丢失，停止处理",
        "未知错误",
        LEASE_EXPIRED_ERROR,
    ],
)
def test_framework_messages_are_kept(error):
    assert public_task_error(error) == error


# ---- 不能外露的内容 ----


def test_server_path_is_hidden():
    with pytest.raises(OSError) as info:
        open("/srv/docmgr/storage/2026/abc/secret.pdf")

    public = public_task_error(as_stored(info.value))

    assert public == f"{INTERNAL}（FileNotFoundError）"
    assert "/srv" not in public


def test_database_address_is_hidden():
    # 用真实的异常类型包一段写死的驱动错误文字（macOS 上连 127.0.0.1:1 实际得到的原文），
    # 不真正连接：Windows 上同样的连接得到的是不带地址的“connection timeout expired”，
    # 前置断言会失败（W9 17.2，T24ai）
    driver_error = psycopg.OperationalError(
        'connection failed: connection to server at "127.0.0.1", port 1 failed: '
        "could not receive data from server: Connection refused"
    )
    stored = as_stored(sa_exc.OperationalError(None, None, driver_error))
    assert "127.0.0.1" in stored  # 原文确实带着地址，否则这个测试没有意义

    public = public_task_error(stored)

    assert public == f"{INTERNAL}（OperationalError）"


def test_storage_key_is_hidden():
    public = public_task_error("StoredFileNotFoundError: 2026/11111111/ab12cd.pdf")

    assert public == f"{INTERNAL}（StoredFileNotFoundError）"


def test_multiline_error_is_hidden_completely():
    error = "DataError: (psycopg.DataError) bad\n[SQL: INSERT …]\n[parameters: {'text': '机密'}]"

    assert public_task_error(error) == f"{INTERNAL}（DataError）"


def test_search_service_reason_is_cut_after_the_status():
    # 用真实的客户端产生错误，避免测试里的写法与代码不一致
    def respond(_request: httpx.Request) -> httpx.Response:
        reason = "[node-1][172.18.0.2:9300][indices:data/write/bulk]"
        body = {"error": {"type": "remote_transport_exception", "reason": reason}}
        return httpx.Response(503, json=body)

    client = OpenSearchClient(
        "http://search.internal:9200", timeout_seconds=1, transport=httpx.MockTransport(respond)
    )
    with client, pytest.raises(TextIndexError) as info:
        client.request("GET", "/chunks")
    stored = as_stored(info.value)
    assert "172.18.0.2" in stored

    assert public_task_error(stored) == "检索服务暂时不可用（HTTP 503）"


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        (
            "TextIndexUnavailable: 检索服务连接失败（ConnectError）",
            "检索服务连接失败（ConnectError）",
        ),
        (
            "TextIndexError: 检索服务拒绝了请求（HTTP 400，mapper_parsing_exception：原文 '机密'）",
            "检索服务拒绝了请求（HTTP 400）",
        ),
        ("TextIndexError: 10 个片段写入失败：http://10.0.0.5:9200", "检索服务出错"),
    ],
)
def test_search_errors(error, expected):
    assert public_task_error(error) == expected


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        (
            "EngineStartError: OCR 模型加载失败：FileNotFoundError: /opt/models/ocr/det",
            "OCR 模型加载失败",
        ),
        (
            "EngineStartError: 加载 OCR 模型超时（超过 60 秒）",
            "加载 OCR 模型超时（超过 60 秒）",
        ),
        (
            "EngineStartError: OCR 子进程启动时异常退出（退出码 -11）",
            "OCR 子进程启动时异常退出（退出码 -11）",
        ),
        ("EngineStartError: 其他原因 /opt/models", "OCR 模型加载失败"),
    ],
)
def test_ocr_engine_start_errors_hide_the_model_path(error, expected):
    assert public_task_error(error) == expected


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        ("MemoryError: ", "处理时内存不足，已终止"),
        ("ParseError: ", f"{INTERNAL}（ParseError）"),  # 没有说明时至少给出类型
        ("一句没登记过的话 /srv/docmgr", INTERNAL),
        # 认得的开头后面夹带了别的内容：整句不放行
        ("子进程异常退出（退出码 -9） /srv/docmgr", INTERNAL),
        ("", INTERNAL),
    ],
)
def test_unrecognised_text_is_not_passed_through(error, expected):
    assert public_task_error(error) == expected


# ---- 名单与代码一致 ----


@pytest.mark.parametrize(
    ("path", "names"),
    [
        ("backend/app/modules/parsing/errors.py", ["ParseError"]),
        ("backend/app/worker/handlers/errors.py", ["PipelineError"]),
        ("backend/app/modules/clip/client.py", ["ClipUnavailable", "ClipRejected"]),
        ("shared/text_index/errors.py", ["TextIndexError", "TextIndexUnavailable"]),
        ("services/ocr_worker/ocr_worker/pipeline.py", ["OcrTaskError"]),
        ("services/ocr_worker/ocr_worker/rendering.py", ["RenderError"]),
        ("services/ocr_worker/ocr_worker/engine_process.py", ["EngineStartError"]),
    ],
)
def test_listed_types_still_exist(path, names):
    # ocr_worker 装在另一个环境里，导入不了，所以统一查源码。改了类名这里会失败，提醒同步名单
    source = (REPO / path).read_text(encoding="utf-8")
    for name in names:
        assert f"class {name}(" in source


# ---- 谁能看到原文 ----


def make_task(error: str | None) -> ProcessingTask:
    return ProcessingTask(
        id=uuid.uuid4(),
        document_id=uuid.uuid4(),
        task_type="parse",
        status="failed",
        attempts=3,
        max_attempts=3,
        error=error,
        created_at=datetime.now(UTC),
        started_at=None,
        finished_at=None,
    )


RAW = "FileNotFoundError: [Errno 2] No such file or directory: '/srv/docmgr/a.pdf'"


def test_ordinary_user_gets_the_cleaned_reason():
    task = make_task(RAW)

    out = to_task_out(User(username="alice", role="user"), task)

    assert out.error == f"{INTERNAL}（FileNotFoundError）"
    assert out.id == task.id
    assert task.error == RAW  # 数据库对象没有被改


def test_admin_gets_the_original_reason():
    assert to_task_out(User(username="root", role="admin"), make_task(RAW)).error == RAW


def test_task_without_error():
    assert to_task_out(User(username="alice", role="user"), make_task(None)).error is None
