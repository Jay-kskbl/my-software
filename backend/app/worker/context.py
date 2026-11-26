"""任务处理函数运行时需要的资源：配置、数据库会话、文件存储、检索服务客户端。

处理函数运行在 spawn 出来的子进程里（见 runner.py），只收到一个 Task，
父进程的数据库连接和配置对象都带不过来，所以每个任务开始时在子进程里重新建立，
任务结束时全部关闭。子进程处理完一个任务就退出，不存在连接复用的问题。
"""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from shared.text_index import OpenSearchClient, client_from_settings
from sqlalchemy.orm import Session

from app.config import Settings, load_settings
from app.db.session import make_engine, make_session_factory
from app.modules.storage import LocalStorage


@dataclass(frozen=True)
class TaskContext:
    settings: Settings
    session: Session
    storage: LocalStorage
    index: OpenSearchClient


@contextmanager
def task_context() -> Iterator[TaskContext]:
    """按当前环境的配置建立一套资源，退出时关闭。"""
    settings = load_settings()
    # 与 Worker 启动检查用同一个超时（T24k、T24ah）
    engine = make_engine(
        settings.database_url,
        connect_timeout_seconds=settings.worker_db_connect_timeout_seconds,
    )
    try:
        with (
            make_session_factory(engine)() as session,
            client_from_settings(settings) as index,
        ):
            yield TaskContext(
                settings=settings,
                session=session,
                storage=LocalStorage(settings.storage_root),
                index=index,
            )
    finally:
        engine.dispose()
