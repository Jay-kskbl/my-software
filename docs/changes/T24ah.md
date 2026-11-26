# 修改记录：T24ah 数据库连接超时，数据库停掉时接口返回 503（2026-11-26）

- 来源：`docs/changes/windows-2026-11-26-核对.md` 第 2 节 Bug 1，Barry 于 2026-11-26 批准（“修bug1”）。同一节的 Bug 2（`test_database_address_is_hidden`）和 `git_dirty` **没有做**，仍在 DEVPLAN §4 待决定
- 任务性质：小改动，不带 🔒；没有改表结构、索引、接口、数据契约、附录 A，没有新依赖。新增一个配置项
- 修改者：Claude（Opus 5.5）

## 逐文件修改记录

| 文件 | 位置 | 修改前 | 修改后 | 原因与影响 |
|---|---|---|---|---|
| `backend/app/db/session.py` | `make_engine()` | `create_engine(url, pool_pre_ping=True)`，没有连接超时（libpq 默认不限） | 新增必填关键字参数 `connect_timeout_seconds`，用 `shared.task_queue.connect_kwargs()` 经 `connect_args` 交给 psycopg | Windows 上连被拒绝的端口会一直等，`/api/auth/me` 超过 90 秒不返回（W9 17.6 第 3a 步）。做成必填，以后新加的调用方不会忘 |
| `backend/app/config.py` | 可选配置 | — | `database_connect_timeout_seconds: int = 5`（2–300） | libpq 只接受整数秒，小于 2 按 2 算，与 `WORKER_DB_CONNECT_TIMEOUT_SECONDS` 同样的范围 |
| `backend/app/main.py` | `create_app()` | `make_engine(url)` | 传 `DATABASE_CONNECT_TIMEOUT_SECONDS` | 超时后抛 `OperationalError`，`api/errors.py` 原有处理返回 503 `DATABASE_UNAVAILABLE`，没有改 |
| `backend/app/worker/context.py` | `task_context()` | `make_engine(url)` | 传 `WORKER_DB_CONNECT_TIMEOUT_SECONDS` | 与 T24k 的启动检查用同一个值；原来启动检查有超时、处理任务的引擎没有 |
| `backend/app/modules/{auth,consistency,documents,experiments}/__main__.py` | `main()` | `make_engine(url)` | 传 `DATABASE_CONNECT_TIMEOUT_SECONDS` | 命令行工具在 Windows 上数据库停掉时同样会一直等 |
| `backend/app/db/migrations/env.py` | `_database_url()` → `_database_url_and_timeout()` | 只返回地址 | 正常使用时读配置的超时；测试传入地址时用 5 秒 | `alembic upgrade head` 同理 |
| `.env.example` | 后端可选 | — | `DATABASE_CONNECT_TIMEOUT_SECONDS=5` 及说明 | GLOBAL §11.2 |
| `backend/tests/unit/test_auth_api.py` | 新增 1 项 | — | 开一个只 `listen()`、从不回应的端口：TCP 由内核接下，PostgreSQL 握手永远等不到回复，在 macOS 上复现 Windows 的“一直等”。设超时 2 秒，`/api/auth/me` 要在 15 秒内返回 503；请求放在线程里、最多等 30 秒，没有超时就失败而不是挂死 pytest | — |
| `backend/tests/unit/test_db_session.py` | 新增 1 项 | — | 拦下 `dialect.connect`，确认 `connect_timeout=7` 传到了驱动 | — |
| `backend/tests/unit/test_config.py` | 默认值 | — | 断言默认 5；`clean_env` 清掉这个变量 | — |
| `backend/tests/unit/test_consistency.py`、`test_requeue_failed.py` | 假的 settings、假的 `make_engine` | `SimpleNamespace` 没有超时字段；假函数只收一个参数 | 补上字段、假函数接受关键字参数 | 跟着接口改 |
| `backend/tests/integration/conftest.py` | `empty_engine` | `make_engine(url)` | 传 5 秒 | 跟着接口改 |
| `DEVPLAN.md`、`docs/untested.md` | — | — | 新任务、§4 标记、§5 完成记录；第 7.5 节 Bug 1 一行改写 | — |

健康检查（`api/health.py`）和 OCR Worker 原来就有超时，没有改。

## 验证

- 已运行（macOS，main 环境）：`backend/` pytest 814 passed、241 skipped；`ruff check`、`ruff format --check` 通过。shared、OCR Worker、CLIP 服务、前端没有改动，没有重跑
- 新增的“不回应端口”测试约 2 秒得到 503
- 反证：去掉 `connect_args` 后，“不回应端口”一项过了 30 秒请求仍挂着而失败，引擎一项因没有 `connect_timeout` 而失败；恢复后都通过
- **未测试（Not Tested）**：Windows 上重测 `windows任务书.md` 第 17.6 节第 3a 步（真实 PostgreSQL 停掉后刷新文件页）；`tests/integration/conftest.py` 和 `app/db/migrations/env.py` 的改动没有对真实 PostgreSQL 跑过。已登记 `docs/untested.md` 第 7.5 节；代码已复核，两处都只是多传一个整数参数

## 修改建议（后续）

1. 下次 Windows 测试时重跑第 17.6 节第 3a 步，预期刷新后约 5 秒出现“数据库不可用”，而不是一直转圈。
2. `pool_pre_ping` 探测旧连接和重新建连可能各等一次超时，最坏约 10 秒才返回 503；觉得太长可以把 `DATABASE_CONNECT_TIMEOUT_SECONDS` 调小（最小 2）。
3. Bug 2、`git_dirty` 仍待 Barry 决定（DEVPLAN §4）。
