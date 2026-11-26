"""集中配置：全部从环境变量（或项目根目录的 .env）读取，启动时一次性校验。"""

from pathlib import Path

from pydantic import Field, SecretStr, ValidationError, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from shared.task_queue import parse_retry_delays

from app.core.errors import ConfigError
from app.modules.storage.filetype import SUPPORTED_TYPES

# backend/app/config.py → 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    # extra="ignore"：.env 里还有 docker-compose 用的变量（POSTGRES_* 等），后端不关心
    model_config = SettingsConfigDict(extra="ignore", env_file_encoding="utf-8")

    # ---- 必填 ----
    database_url: str = Field(min_length=1, description="PostgreSQL 连接串")
    opensearch_url: str = Field(min_length=1, description="OpenSearch 地址")
    clip_service_url: str = Field(min_length=1, description="CLIP 模型服务地址")
    # SecretStr：打印配置对象或写日志时显示为 **********，不会泄露
    # 至少 32 个字符：HS256 的密钥长度不应短于 256 位
    jwt_secret: SecretStr = Field(min_length=32, description="签发登录令牌（JWT）的密钥")

    @field_validator("jwt_secret")
    @classmethod
    def _jwt_secret_not_the_example(cls, value: SecretStr) -> SecretStr:
        # .env.example 里的示例值是公开的，长度也够：直接复制过来能启动，但任何人都能伪造令牌
        if value.get_secret_value().startswith("change-me"):
            raise ValueError("仍是 .env.example 中的示例值，必须换成自己生成的随机密钥")
        return value

    # ---- 可选 ----
    health_check_timeout_seconds: float = Field(default=2.0, gt=0)
    # API 与命令行工具连接数据库最多等多久（秒，libpq 的 connect_timeout 只接受整数，
    # 最小有效值 2）。
    # 不设时 Windows 上数据库停掉后接口会一直挂着；超时后接口返回 503（T24ah）
    database_connect_timeout_seconds: int = Field(default=5, ge=2, le=300)
    # 调用 OpenSearch 的超时（建索引、批量写入、删除、查询）
    opensearch_timeout_seconds: float = Field(default=10.0, gt=0)
    # embed 任务调用 CLIP 服务编码一张图片的超时（T21）。服务一次只算一个请求，
    # 排在后面的要等前面的算完，所以比单张图片的编码时间宽得多
    clip_encode_timeout_seconds: float = Field(default=60.0, gt=0)
    # 加在两个索引名前面。默认为空；测试用它得到独立的索引，不碰正式数据。
    # OpenSearch 的索引名只能是小写，且不能以 _ 或 - 开头
    opensearch_index_prefix: str = Field(default="", pattern=r"^([a-z0-9][a-z0-9_-]*)?$")
    access_token_expire_seconds: int = Field(default=3600, gt=0, description="登录令牌有效期")
    storage_root: Path = Field(
        default=PROJECT_ROOT / "storage", description="上传文件的存储根目录（M3）"
    )

    # ---- 上传限制（M2，GLOBAL §6.8）----
    upload_max_bytes: int = Field(default=50 * 1024 * 1024, gt=0, description="单个文件大小上限")
    upload_max_filename_chars: int = Field(default=255, gt=0, le=255)
    # 允许上传的类型，逗号分隔的扩展名；只能从存储模块支持的类型里选
    upload_allowed_types: str = Field(default="pdf,docx,xlsx,png,jpg")

    @field_validator("upload_allowed_types")
    @classmethod
    def _allowed_types_known(cls, value: str) -> str:
        known = {t.ext for t in SUPPORTED_TYPES}
        chosen = [part.strip().lower() for part in value.split(",") if part.strip()]
        unknown = sorted(set(chosen) - known)
        if not chosen or unknown:
            raise ValueError(f"只能是 {'、'.join(sorted(known))} 中的一个或多个，用逗号分隔")
        return ",".join(chosen)

    @property
    def upload_allowed_extensions(self) -> frozenset[str]:
        return frozenset(self.upload_allowed_types.split(","))

    # ---- 解析（M5）----
    # PDF 某页文本层的有效字符数低于它、且页面上有图片或图形时，该页走 OCR（GLOBAL §2 P1）。
    # 属于检索实验参数：每次实验随结果一起记录（GLOBAL §8.2）
    pdf_ocr_min_chars: int = Field(default=20, ge=1)
    # docx / xlsx 是 zip：解压后的总大小和文件数超过上限就拒绝解析（zip 炸弹，GLOBAL §7.2）
    parse_zip_max_total_bytes: int = Field(default=200 * 1024 * 1024, gt=0)
    parse_zip_max_entries: int = Field(default=5000, gt=0)
    # 图片的像素数（宽 × 高）上限，超过就拒绝处理：解码后每个像素要占 3–4 字节内存
    parse_image_max_pixels: int = Field(default=100_000_000, gt=0)

    # ---- 切分（M7）----
    # 一个片段最多多少个字符（中文一个字、英文一个字母都算一个），以及相邻片段重叠多少个字符。
    # 属于检索实验参数：每次实验随结果一起记录（GLOBAL §8.2）；改动后 parse_version 随之变化
    chunk_max_chars: int = Field(default=500, ge=50, le=10_000)
    chunk_overlap_chars: int = Field(default=50, ge=0)

    # ---- 检索（M11）----
    # 都是检索实验参数：每次检索随检索日志一起记录（GLOBAL §8.2）
    search_default_top_k: int = Field(default=20, ge=1)
    search_max_top_k: int = Field(default=100, ge=1)
    search_max_query_chars: int = Field(default=256, ge=1)
    # 每个通道最多取多少个文件参与 RRF 融合（截断深度）
    search_channel_depth: int = Field(default=100, ge=1, le=10_000)
    # RRF 常数 k：分数为 Σ 1/(k + 名次)。60 是原论文（Cormack 等，2009）的取值
    search_rrf_k: int = Field(default=60, ge=1)
    # meta 通道里文件名与标签的权重。默认相同：没有实验依据之前不偏向任何一个
    search_meta_filename_weight: float = Field(default=1.0, gt=0)
    search_meta_tags_weight: float = Field(default=1.0, gt=0)
    # 命中片段（高亮摘要）的长度，按字符计
    search_snippet_chars: int = Field(default=150, ge=20, le=2000)
    # 图像通道调用 CLIP 服务编码查询文本的超时（T22）。超时就降级为纯文本检索（附录 A5）。
    # CLIP 服务一次只算一个请求，embed 任务批量编码时查询要排队，所以不能太短也不能太长
    search_image_timeout_seconds: float = Field(default=3.0, gt=0, le=60)
    # 请求里没有指定时各通道是否开启。图像通道默认关闭（T22 Barry 决定：留到 T23/T24 再定）
    search_channel_meta_enabled: bool = True
    search_channel_text_enabled: bool = True
    search_channel_image_enabled: bool = False

    @model_validator(mode="after")
    def _search_limits_consistent(self) -> "Settings":
        if self.search_default_top_k > self.search_max_top_k:
            raise ValueError("SEARCH_DEFAULT_TOP_K 不能超过 SEARCH_MAX_TOP_K")
        # 每个通道至少要取够 top_k 个文件，否则只开一个通道时凑不满 top_k
        if self.search_max_top_k > self.search_channel_depth:
            raise ValueError("SEARCH_MAX_TOP_K 不能超过 SEARCH_CHANNEL_DEPTH")
        if not (
            self.search_channel_meta_enabled
            or self.search_channel_text_enabled
            or self.search_channel_image_enabled
        ):
            raise ValueError("SEARCH_CHANNEL_*_ENABLED 至少要开启一个")
        return self

    # ---- Worker（M4，附录 A3）----
    # 租约时长：太短会误回收仍在正常处理的任务，太长则 Worker 崩溃后恢复慢
    worker_lease_seconds: float = Field(default=60.0, gt=0)
    # 续租间隔，必须明显小于租约时长
    worker_heartbeat_seconds: float = Field(default=15.0, gt=0)
    # 队列为空时隔多久再查一次
    worker_poll_seconds: float = Field(default=2.0, gt=0)
    # 单个任务的处理时间上限，超过即终止子进程
    worker_task_timeout_seconds: float = Field(default=600.0, gt=0)
    # 单个任务子进程的内存上限（MB）。只在 Linux 上有效，见 docs/decisions.md D16
    worker_memory_limit_mb: int = Field(default=2048, gt=0)
    # 处理多少个任务后 Worker 主动退出，由外层重新拉起
    worker_max_tasks: int = Field(default=50, gt=0)
    # 连接数据库最多等多久（秒，libpq 的 connect_timeout 只接受整数，最小有效值 2）。
    # 不设上限时主机不可达要等操作系统的 TCP 超时，启动检查迟迟不报错（T24k）
    worker_db_connect_timeout_seconds: int = Field(default=10, ge=2, le=300)
    # 失败任务的重试间隔（秒，逗号分隔），与 OCR Worker 共用；写 0 表示马上重试（T24ad）
    task_retry_delays_seconds: str = Field(default="30,120")

    @field_validator("task_retry_delays_seconds")
    @classmethod
    def _retry_delays_valid(cls, value: str) -> str:
        parse_retry_delays(value)
        return value

    @property
    def retry_delays(self) -> tuple[float, ...]:
        return parse_retry_delays(self.task_retry_delays_seconds)

    @model_validator(mode="after")
    def _overlap_shorter_than_chunk(self) -> "Settings":
        # 重叠超过片段的一半时，相邻片段大部分内容相同，索引膨胀、同一段文字反复计分
        if self.chunk_overlap_chars * 2 > self.chunk_max_chars:
            raise ValueError("CHUNK_OVERLAP_CHARS 不能超过 CHUNK_MAX_CHARS 的一半")
        return self

    @model_validator(mode="after")
    def _heartbeat_shorter_than_lease(self) -> "Settings":
        # 至少留出两次续租的机会：一次续租因数据库抖动失败，不至于立刻丢掉租约
        if self.worker_heartbeat_seconds * 2 > self.worker_lease_seconds:
            raise ValueError("WORKER_HEARTBEAT_SECONDS 不能超过 WORKER_LEASE_SECONDS 的一半")
        return self

    @field_validator("storage_root")
    @classmethod
    def _storage_root_absolute(cls, value: Path) -> Path:
        # 相对路径一律相对项目根目录，不随启动时的工作目录变化
        return value if value.is_absolute() else PROJECT_ROOT / value


def load_settings(env_file: Path | None = DEFAULT_ENV_FILE) -> Settings:
    """读取并校验配置。有问题时抛出 ConfigError，信息里列出每个出错的环境变量。

    env_file=None 表示只读环境变量（测试用）。
    """
    try:
        return Settings(_env_file=env_file)
    except ValidationError as exc:
        missing: list[str] = []
        invalid: list[str] = []
        for err in exc.errors():
            # 跨字段的检查（model_validator）没有对应的单个变量，loc 为空
            name = str(err["loc"][0]).upper() if err["loc"] else "配置项之间的约束"
            if err["type"] == "missing":
                missing.append(name)
            else:
                # 不输出变量的值：DATABASE_URL 里可能带密码
                invalid.append(f"{name}（{err['msg']}）")

        lines = ["配置检查失败，后端无法启动："]
        if missing:
            lines.append(f"  缺少必填环境变量：{', '.join(missing)}")
        if invalid:
            lines.append(f"  取值不合法：{'; '.join(invalid)}")
        lines.append("  请参照项目根目录的 .env.example 创建 .env，或直接设置上述环境变量。")
        raise ConfigError("\n".join(lines)) from exc
