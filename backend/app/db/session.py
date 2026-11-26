from shared.task_queue import connect_kwargs
from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker


def sqlalchemy_url(database_url: str) -> str:
    """把配置里的 postgresql://… 转成 SQLAlchemy 使用 psycopg 3 驱动的写法。

    配置只保留一种写法（标准的 postgresql://，psycopg 可直接使用），
    避免同一个数据库地址在 .env 里出现两个变量。
    """
    url = make_url(database_url)
    if url.get_backend_name() != "postgresql":
        raise ValueError("DATABASE_URL 必须是 PostgreSQL 连接串（postgresql://…）")
    return url.set(drivername="postgresql+psycopg").render_as_string(hide_password=False)


def make_engine(database_url: str, *, connect_timeout_seconds: int) -> Engine:
    """建立 SQLAlchemy 引擎。

    connect_timeout_seconds 必须由调用方给出（libpq 的 connect_timeout，整数秒，小于 2 按 2 算）：
    不设时 Windows 上连一个被拒绝的端口会一直等，接口挂着不返回，用户看不到“数据库不可用”
    （W9 17.6 实测，T24ah）。超时后 psycopg 抛 OperationalError，API 按现有处理返回 503。
    """
    # pool_pre_ping：数据库重启后，连接池里的旧连接会先被探测并丢弃，而不是让请求失败
    return create_engine(
        sqlalchemy_url(database_url),
        pool_pre_ping=True,
        connect_args=connect_kwargs(connect_timeout_seconds),
    )


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)
