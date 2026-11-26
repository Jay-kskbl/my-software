"""T06：不需要数据库就能验证的接口行为——未登录 401、参数校验 422、数据库不可用 503。

需要真实数据库的部分（注册、登录、权限）在 tests/integration/test_auth.py。
"""

import socket
import uuid

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.core.security import create_access_token
from app.main import create_app

SECRET = "unit-test-secret-not-used-anywhere-else-0123456789"


def _closed_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def client(tmp_path):
    # 数据库地址指向一个没有服务的端口：这些测试要么根本不该碰数据库，要么就是在测数据库不可用
    port = _closed_port()
    settings = Settings(
        _env_file=None,
        database_url=f"postgresql://u:secret-pw@127.0.0.1:{port}/db",
        opensearch_url=f"http://127.0.0.1:{port}",
        clip_service_url=f"http://127.0.0.1:{port}",
        jwt_secret=SECRET,
        storage_root=tmp_path / "storage",
    )
    with TestClient(create_app(settings)) as c:
        yield c


def assert_error(resp, status: int, code: str) -> dict:
    assert resp.status_code == status
    body = resp.json()
    assert set(body) == {"error"}
    assert set(body["error"]) == {"code", "message"}
    assert body["error"]["code"] == code
    return body["error"]


# ---- 🧪 未登录 401 ----


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Authorization": ""},
        {"Authorization": "Bearer"},
        {"Authorization": "Bearer not-a-jwt"},
        {"Authorization": "Basic dXNlcjpwYXNz"},
        {"Authorization": "Token abc"},
    ],
    ids=["no-header", "empty", "bearer-only", "garbage-token", "basic", "wrong-scheme"],
)
def test_me_without_valid_token_is_401(client, headers):
    resp = client.get("/api/auth/me", headers=headers)

    assert_error(resp, 401, "UNAUTHENTICATED")
    assert resp.headers["WWW-Authenticate"] == "Bearer"


def test_token_signed_with_other_secret_is_401(client):
    token = create_access_token(
        uuid.uuid4(),
        secret="another-unit-test-secret-0123456789-abcdefghijklmn",
        expires_in_seconds=60,
    )

    resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert_error(resp, 401, "UNAUTHENTICATED")


# ---- 参数校验 422 ----


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"username": "barry"},
        {"username": "ab", "password": "long-enough-password"},
        {"username": "a" * 33, "password": "long-enough-password"},
        {"username": "has space", "password": "long-enough-password"},
        {"username": "巴里巴里", "password": "long-enough-password"},
        {"username": "barry", "password": "short"},
        {"username": "barry", "password": "x" * 129},
        {"username": "barry", "password": "long-enough-password", "role": "admin"},
    ],
    ids=[
        "empty",
        "no-password",
        "username-too-short",
        "username-too-long",
        "username-space",
        "username-non-ascii",
        "password-too-short",
        "password-too-long",
        "extra-role-field",
    ],
)
def test_register_with_invalid_body_is_422(client, body):
    resp = client.post("/api/auth/register", json=body)

    assert_error(resp, 422, "VALIDATION_ERROR")


def test_validation_error_does_not_echo_the_password(client):
    resp = client.post("/api/auth/register", json={"username": "barry", "password": "s3cr3t"})

    assert_error(resp, 422, "VALIDATION_ERROR")
    assert "s3cr3t" not in resp.text


# ---- 数据库不可用 503 ----


def test_login_when_database_is_down_is_503_not_401(client):
    # 数据库故障不能被当成“密码错误”
    resp = client.post("/api/auth/login", json={"username": "barry", "password": "whatever-pw"})

    error = assert_error(resp, 503, "DATABASE_UNAVAILABLE")
    assert "127.0.0.1" not in error["message"]
    assert "secret-pw" not in resp.text


def test_valid_token_when_database_is_down_is_503(client):
    token = create_access_token(uuid.uuid4(), secret=SECRET, expires_in_seconds=60)

    resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert_error(resp, 503, "DATABASE_UNAVAILABLE")


def test_database_that_never_answers_gives_503_within_timeout(tmp_path):
    # T24ah：Windows 上连被拒绝的端口不会立刻失败，而是一直等（W9 17.6）。
    # 这里用一个只监听、从不回应的端口在任何系统上复现“一直等”：TCP 连接由内核接下，
    # 但 PostgreSQL 的握手永远等不到回复。没有连接超时时，这个请求会一直挂着。
    import threading
    import time

    with socket.socket() as silent:
        silent.bind(("127.0.0.1", 0))
        silent.listen(8)
        port = silent.getsockname()[1]
        settings = Settings(
            _env_file=None,
            database_url=f"postgresql://u:secret-pw@127.0.0.1:{port}/db",
            opensearch_url=f"http://127.0.0.1:{port}",
            clip_service_url=f"http://127.0.0.1:{port}",
            jwt_secret=SECRET,
            storage_root=tmp_path / "storage",
            database_connect_timeout_seconds=2,
        )
        token = create_access_token(uuid.uuid4(), secret=SECRET, expires_in_seconds=60)
        result: dict = {}

        def call() -> None:
            with TestClient(create_app(settings)) as c:
                started = time.monotonic()
                result["resp"] = c.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
                result["elapsed"] = time.monotonic() - started

        worker = threading.Thread(target=call, daemon=True)
        worker.start()
        # 放宽到 30 秒，只为了没有超时时测试失败而不是挂死整个 pytest
        worker.join(timeout=30)

    assert not worker.is_alive(), "数据库不回应时请求一直挂着：连接超时没有生效"
    assert_error(result["resp"], 503, "DATABASE_UNAVAILABLE")
    # pool_pre_ping 和真正的连接各可能等一次超时，留出余量
    assert result["elapsed"] < 15
