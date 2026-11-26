"""T01 🧪：缺失必填配置时启动失败且错误信息明确。"""

import pytest

from app.config import PROJECT_ROOT, load_settings
from app.core.errors import ConfigError
from app.main import create_app

REQUIRED = {
    "DATABASE_URL": "postgresql://u:secret-pw@localhost:5432/db",
    "OPENSEARCH_URL": "http://localhost:9200",
    "CLIP_SERVICE_URL": "http://localhost:8001",
    "JWT_SECRET": "unit-test-secret-not-used-anywhere-else-0123456789",
}


@pytest.fixture
def clean_env(monkeypatch):
    for name in [
        *REQUIRED,
        "HEALTH_CHECK_TIMEOUT_SECONDS",
        "STORAGE_ROOT",
        "ACCESS_TOKEN_EXPIRE_SECONDS",
        "WORKER_LEASE_SECONDS",
        "WORKER_HEARTBEAT_SECONDS",
        "PDF_OCR_MIN_CHARS",
        "DATABASE_CONNECT_TIMEOUT_SECONDS",
    ]:
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


def test_loads_when_all_required_present(clean_env):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)

    settings = load_settings(env_file=None)

    assert settings.database_url == REQUIRED["DATABASE_URL"]
    assert settings.health_check_timeout_seconds == 2.0
    assert settings.database_connect_timeout_seconds == 5


@pytest.mark.parametrize("missing", list(REQUIRED))
def test_each_missing_required_var_is_named(clean_env, missing):
    for name, value in REQUIRED.items():
        if name != missing:
            clean_env.setenv(name, value)

    with pytest.raises(ConfigError) as excinfo:
        load_settings(env_file=None)

    message = str(excinfo.value)
    assert missing in message
    assert ".env.example" in message
    # 没缺的变量不应被误报
    for name in REQUIRED:
        if name != missing:
            assert name not in message


def test_all_missing_vars_listed_together(clean_env):
    with pytest.raises(ConfigError) as excinfo:
        load_settings(env_file=None)

    for name in REQUIRED:
        assert name in str(excinfo.value)


def test_empty_value_is_rejected(clean_env):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)
    clean_env.setenv("OPENSEARCH_URL", "")

    with pytest.raises(ConfigError, match="OPENSEARCH_URL"):
        load_settings(env_file=None)


def test_invalid_value_error_does_not_leak_secrets(clean_env):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)
    clean_env.setenv("HEALTH_CHECK_TIMEOUT_SECONDS", "-1")

    with pytest.raises(ConfigError) as excinfo:
        load_settings(env_file=None)

    assert "HEALTH_CHECK_TIMEOUT_SECONDS" in str(excinfo.value)
    assert "secret-pw" not in str(excinfo.value)


def test_reads_env_file(clean_env, tmp_path):
    env_file = tmp_path / ".env"
    lines = [f"{k}={v}" for k, v in REQUIRED.items()]
    lines.append("POSTGRES_USER=ignored-by-backend")
    env_file.write_text("\n".join(lines), encoding="utf-8")

    settings = load_settings(env_file=env_file)

    assert settings.clip_service_url == REQUIRED["CLIP_SERVICE_URL"]


def test_app_startup_fails_with_readable_message(clean_env, capsys, monkeypatch, tmp_path):
    # 指向一个不存在的 .env，保证测试不受开发机上真实 .env 的影响
    monkeypatch.setattr("app.config.DEFAULT_ENV_FILE", tmp_path / "no-such.env")
    monkeypatch.setattr(
        "app.main.load_settings", lambda: load_settings(env_file=tmp_path / "no-such.env")
    )

    with pytest.raises(SystemExit) as excinfo:
        create_app()

    assert excinfo.value.code == 1
    stderr = capsys.readouterr().err
    assert "缺少必填环境变量" in stderr
    assert "DATABASE_URL" in stderr


def test_storage_root_defaults_to_project_storage_dir(clean_env):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)
    clean_env.delenv("STORAGE_ROOT", raising=False)

    assert load_settings(env_file=None).storage_root == PROJECT_ROOT / "storage"


def test_relative_storage_root_resolved_against_project_root(clean_env):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)
    clean_env.setenv("STORAGE_ROOT", "data/files")

    assert load_settings(env_file=None).storage_root == PROJECT_ROOT / "data" / "files"


def test_absolute_storage_root_kept(clean_env, tmp_path):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)
    clean_env.setenv("STORAGE_ROOT", str(tmp_path))

    assert load_settings(env_file=None).storage_root == tmp_path


def test_cross_field_error_is_reported_readably(clean_env):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)
    clean_env.setenv("WORKER_LEASE_SECONDS", "10")
    clean_env.setenv("WORKER_HEARTBEAT_SECONDS", "9")

    with pytest.raises(ConfigError, match="WORKER_HEARTBEAT_SECONDS"):
        load_settings(env_file=None)


def test_pdf_ocr_threshold_default_and_bounds(clean_env):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)

    assert load_settings(env_file=None).pdf_ocr_min_chars == 20

    clean_env.setenv("PDF_OCR_MIN_CHARS", "0")
    with pytest.raises(ConfigError, match="PDF_OCR_MIN_CHARS"):
        load_settings(env_file=None)


def test_example_jwt_secret_is_rejected(clean_env):
    # .env.example 里的示例值足够长，但它是公开的：原样复制不能启动
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)
    clean_env.setenv("JWT_SECRET", "change-me-generate-a-random-secret-of-32-chars-or-more")

    with pytest.raises(ConfigError, match="JWT_SECRET") as excinfo:
        load_settings(env_file=None)

    assert "change-me-generate" not in str(excinfo.value)


def test_env_example_itself_does_not_pass_as_a_working_config(clean_env):
    # 防止示例文件和上面的检查脱节：把 .env.example 当作 .env 用，必须在 JWT_SECRET 上失败
    with pytest.raises(ConfigError, match="JWT_SECRET"):
        load_settings(env_file=PROJECT_ROOT / ".env.example")


def test_parse_limits_defaults_and_bounds(clean_env):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)

    settings = load_settings(env_file=None)
    assert settings.parse_zip_max_total_bytes == 200 * 1024 * 1024
    assert settings.parse_zip_max_entries == 5000
    assert settings.parse_image_max_pixels == 100_000_000

    for name in ("PARSE_ZIP_MAX_TOTAL_BYTES", "PARSE_ZIP_MAX_ENTRIES", "PARSE_IMAGE_MAX_PIXELS"):
        clean_env.setenv(name, "0")
        with pytest.raises(ConfigError, match=name):
            load_settings(env_file=None)
        clean_env.delenv(name)


def test_chunking_defaults_and_bounds(clean_env):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)

    settings = load_settings(env_file=None)
    assert (settings.chunk_max_chars, settings.chunk_overlap_chars) == (500, 50)

    clean_env.setenv("CHUNK_MAX_CHARS", "49")
    with pytest.raises(ConfigError, match="CHUNK_MAX_CHARS"):
        load_settings(env_file=None)

    clean_env.setenv("CHUNK_MAX_CHARS", "100")
    clean_env.setenv("CHUNK_OVERLAP_CHARS", "50")
    assert load_settings(env_file=None).chunk_overlap_chars == 50
    clean_env.setenv("CHUNK_OVERLAP_CHARS", "51")
    with pytest.raises(ConfigError, match="CHUNK_OVERLAP_CHARS"):
        load_settings(env_file=None)


def test_opensearch_options_defaults_and_bounds(clean_env):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)

    settings = load_settings(env_file=None)
    assert settings.opensearch_timeout_seconds == 10.0
    assert settings.opensearch_index_prefix == ""

    clean_env.setenv("OPENSEARCH_INDEX_PREFIX", "test_1-")
    assert load_settings(env_file=None).opensearch_index_prefix == "test_1-"

    for bad in ("Upper", "_leading", "has space"):
        clean_env.setenv("OPENSEARCH_INDEX_PREFIX", bad)
        with pytest.raises(ConfigError, match="OPENSEARCH_INDEX_PREFIX"):
            load_settings(env_file=None)
    clean_env.delenv("OPENSEARCH_INDEX_PREFIX")

    clean_env.setenv("OPENSEARCH_TIMEOUT_SECONDS", "0")
    with pytest.raises(ConfigError, match="OPENSEARCH_TIMEOUT_SECONDS"):
        load_settings(env_file=None)


def test_search_options_defaults_and_bounds(clean_env):
    for name, value in REQUIRED.items():
        clean_env.setenv(name, value)

    settings = load_settings(env_file=None)
    assert (settings.search_default_top_k, settings.search_max_top_k) == (20, 100)
    assert (settings.search_channel_depth, settings.search_rrf_k) == (100, 60)
    assert settings.search_channel_image_enabled is False

    clean_env.setenv("SEARCH_DEFAULT_TOP_K", "101")
    with pytest.raises(ConfigError, match="SEARCH_DEFAULT_TOP_K"):
        load_settings(env_file=None)
    clean_env.delenv("SEARCH_DEFAULT_TOP_K")

    clean_env.setenv("SEARCH_CHANNEL_DEPTH", "50")
    with pytest.raises(ConfigError, match="SEARCH_MAX_TOP_K"):
        load_settings(env_file=None)
    clean_env.delenv("SEARCH_CHANNEL_DEPTH")

    clean_env.setenv("SEARCH_CHANNEL_META_ENABLED", "false")
    clean_env.setenv("SEARCH_CHANNEL_TEXT_ENABLED", "false")
    with pytest.raises(ConfigError, match="SEARCH_CHANNEL"):
        load_settings(env_file=None)
    clean_env.delenv("SEARCH_CHANNEL_META_ENABLED")
    clean_env.delenv("SEARCH_CHANNEL_TEXT_ENABLED")

    clean_env.setenv("SEARCH_RRF_K", "0")
    with pytest.raises(ConfigError, match="SEARCH_RRF_K"):
        load_settings(env_file=None)
