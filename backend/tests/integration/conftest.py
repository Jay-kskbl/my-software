"""集成测试需要一个真实的、专用的空 PostgreSQL 数据库。

通过环境变量 TEST_DATABASE_URL 指定，例如：
    TEST_DATABASE_URL=postgresql://docmgr:change-me@localhost:5432/docmgr_test
未设置时这些测试会被跳过（跳过 ≠ 通过，汇报时算"未运行"）。
"""

import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine, inspect, text

from app.config import Settings
from app.db.session import make_engine, make_session_factory
from app.main import create_app

BACKEND_DIR = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def test_database_url() -> str:
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("未设置 TEST_DATABASE_URL，跳过需要 PostgreSQL 的集成测试")
    return url


@pytest.fixture
def alembic_config(test_database_url: str) -> Config:
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.attributes["database_url"] = test_database_url
    return config


@pytest.fixture
def empty_engine(test_database_url: str):
    """一个确认为空的数据库；测试结束后清空，保证每个测试互不影响。"""
    engine = make_engine(test_database_url, connect_timeout_seconds=5)
    existing = inspect(engine).get_table_names()
    if existing:
        engine.dispose()
        # 宁可失败也不清库：TEST_DATABASE_URL 万一指到了开发库，不能把数据删掉
        pytest.fail(
            f"TEST_DATABASE_URL 指向的数据库不是空的（已有表：{existing}）。请使用专用的空测试库。"
        )
    yield engine
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    engine.dispose()


@pytest.fixture
def migrated_engine(empty_engine: Engine, alembic_config: Config) -> Engine:
    command.upgrade(alembic_config, "head")
    return empty_engine


@pytest.fixture
def session(migrated_engine: Engine):
    """已迁移的测试库上的一个数据库会话。"""
    with make_session_factory(migrated_engine)() as s:
        yield s


@pytest.fixture
def app(migrated_engine: Engine, test_database_url: str, tmp_path) -> FastAPI:
    settings = Settings(
        _env_file=None,
        database_url=test_database_url,
        opensearch_url="http://127.0.0.1:1",
        clip_service_url="http://127.0.0.1:1",
        jwt_secret="integration-test-secret-not-used-anywhere-else-0123456789",
        storage_root=tmp_path / "storage",
        # 上限调小，测试“超大文件”不必真的造一个 50 MB 的文件
        upload_max_bytes=64 * 1024,
    )
    return create_app(settings)


@pytest.fixture
def client(app: FastAPI):
    with TestClient(app) as c:
        yield c
