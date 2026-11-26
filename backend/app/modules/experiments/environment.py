"""M12：随每次实验保存的环境信息（GLOBAL §9.2 第 2、5 条：固定并说明实验环境）。

取不到的项记为 None 并写明原因，不中止实验：环境信息是记录，不是前提。
"""

import hashlib
import os
import platform
import subprocess
from pathlib import Path
from typing import Any

from shared.chunking import CHUNKER_VERSION
from shared.text_index import IMAGE_VECTORS, INDEX_NAMES, OpenSearchClient, TextIndexError

from app.modules.experiments.dataset import PROJECT_ROOT

_MAPPINGS_DIR = PROJECT_ROOT / "shared" / "text_index" / "mappings"
# 图片向量索引的 mapping 在 M10 里（D35），不在 INDEX_NAMES 中
_VECTOR_MAPPING = (
    PROJECT_ROOT
    / "backend"
    / "app"
    / "modules"
    / "vector_index"
    / "mappings"
    / f"{IMAGE_VECTORS}.json"
)


def _git(*args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args], cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10, check=True
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip()


def _memory_bytes() -> int | None:
    """物理内存总量。不用 psutil（main 环境没有装）：先试 sysconf，macOS 上再试 sysctl。"""
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    except (ValueError, OSError, AttributeError):
        pass
    try:
        out = subprocess.run(
            ["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=5, check=True
        )
        return int(out.stdout.strip())
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def _sha256(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def machine_info() -> dict[str, Any]:
    # 只看已跟踪的文件：未跟踪的输出目录（如 Windows 上的 output/）不改变运行的代码，
    # 算进去的话这个标志总是 true、失去意义（W9 核对，T24aj）
    status = _git("status", "--porcelain", "--untracked-files=no")
    return {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor() or None,
        "cpu_count": os.cpu_count(),
        "memory_bytes": _memory_bytes(),
        "python": platform.python_version(),
        "git_commit": _git("rev-parse", "HEAD"),
        # 已跟踪的文件有未提交的改动时，提交号不能完整说明运行的是哪份代码
        "git_dirty": None if status is None else bool(status),
    }


def code_versions() -> dict[str, Any]:
    return {
        "chunker_version": CHUNKER_VERSION,
        "mapping_sha256": {
            **{name: _sha256(_MAPPINGS_DIR / f"{name}.json") for name in INDEX_NAMES},
            IMAGE_VECTORS: _sha256(_VECTOR_MAPPING),
        },
    }


def opensearch_info(client: OpenSearchClient) -> dict[str, Any]:
    try:
        version = client.request("GET", "/").json().get("version", {}).get("number")
        plugins = client.request("GET", "/_cat/plugins", params={"format": "json"}).json()
    except TextIndexError as exc:
        return {"error": exc.message}
    return {
        "version": version,
        "plugins": sorted({f"{p.get('component')} {p.get('version')}" for p in plugins}),
    }
