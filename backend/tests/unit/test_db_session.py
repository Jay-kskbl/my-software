import pytest

from app.db.session import sqlalchemy_url


def test_plain_postgresql_url_gets_psycopg_driver():
    assert (
        sqlalchemy_url("postgresql://u:p%40ss@localhost:5432/db")
        == "postgresql+psycopg://u:p%40ss@localhost:5432/db"
    )


def test_already_qualified_url_is_normalised():
    assert sqlalchemy_url("postgresql+psycopg2://u@h/db") == "postgresql+psycopg://u@h/db"


def test_non_postgresql_url_rejected():
    with pytest.raises(ValueError, match="PostgreSQL"):
        sqlalchemy_url("sqlite:///x.db")


class _StopConnect(Exception):
    pass


def test_engine_passes_connect_timeout_to_psycopg():
    # T24ah：超时通过 connect_args 交给 psycopg。拦下 dialect.connect，不真正连接数据库
    from app.db.session import make_engine

    engine = make_engine("postgresql://u@127.0.0.1:1/db", connect_timeout_seconds=7)
    captured: dict = {}

    def fake_connect(*_args, **kwargs):
        captured.update(kwargs)
        raise _StopConnect

    engine.dialect.connect = fake_connect
    try:
        with pytest.raises(_StopConnect):
            engine.raw_connection()
    finally:
        engine.dispose()
    assert captured["connect_timeout"] == 7


def test_connect_timeout_is_required():
    from app.db.session import make_engine

    with pytest.raises(TypeError):
        make_engine("postgresql://u@127.0.0.1:1/db")  # type: ignore[call-arg]
