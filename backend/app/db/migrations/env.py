"""Alembic 运行环境。只支持在线模式（直接连接数据库执行）。"""

from logging.config import fileConfig

from alembic import context

from app.config import load_settings
from app.db import models  # noqa: F401 —— 导入后各表才会注册到 Base.metadata
from app.db.base import Base
from app.db.session import make_engine

config = context.config
if config.config_file_name is not None:
    # 不关闭已有 logger：测试里调用迁移时，不能把其他模块的日志关掉
    fileConfig(config.config_file_name, disable_existing_loggers=False)

target_metadata = Base.metadata


# 测试传入地址时不读项目配置，用这个值；与 DATABASE_CONNECT_TIMEOUT_SECONDS 的默认值相同
_TEST_CONNECT_TIMEOUT_SECONDS = 5


def _database_url_and_timeout() -> tuple[str, int]:
    # 测试通过 config.attributes 传入测试库地址；正常使用时读取项目配置
    url = config.attributes.get("database_url")
    if url:
        return url, _TEST_CONNECT_TIMEOUT_SECONDS
    settings = load_settings()
    return settings.database_url, settings.database_connect_timeout_seconds


def run_migrations() -> None:
    url, timeout = _database_url_and_timeout()
    engine = make_engine(url, connect_timeout_seconds=timeout)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


if context.is_offline_mode():
    raise SystemExit("本项目不支持 Alembic 离线模式（--sql），请直接连接数据库执行迁移。")

run_migrations()
