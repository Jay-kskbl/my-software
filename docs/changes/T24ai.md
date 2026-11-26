# 修改记录：T24ai 测试不再依赖真实网络错误的文字（2026-11-26）

- 来源：`docs/changes/windows-2026-11-26-核对.md` 第 2 节 Bug 2，Barry 于 2026-11-26 批准（“Fix both”）
- 任务性质：只改测试，不带 🔒；没有改产品代码、配置、表结构、接口、附录 A，没有新依赖
- 修改者：Claude（Opus 5.5）

## 逐文件修改记录

| 文件 | 位置 | 修改前 | 修改后 | 原因与影响 |
|---|---|---|---|---|
| `backend/tests/unit/test_task_errors.py` | `test_database_address_is_hidden` | 真的用 SQLAlchemy 连 `127.0.0.1:1`，先断言错误文字里有 `127.0.0.1`，再检查脱敏结果 | 用 `sqlalchemy.exc.OperationalError(None, None, psycopg.OperationalError(…))` 构造同样类型的异常，驱动错误文字写死为 macOS 上同样连接实际得到的原文；其余断言不变 | Windows 上同样的连接得到 `connection timeout expired`，不带地址，前置断言失败（W9 17.2）。被测的 `public_task_error()` 没有问题。存进任务表后的文字格式与真实连接逐字相同（已在 macOS 上对比） |
| 同上 | import | `from sqlalchemy import create_engine` | `import psycopg`、`from sqlalchemy import exc as sa_exc` | `create_engine` 只有这一项用到；psycopg 主环境里已有 |
| `DEVPLAN.md`、`docs/untested.md` | — | — | 新任务、§4 标记、§5 完成记录；第 7.5 节 Bug 2 一行改写 | — |

## 验证

- 已运行（macOS，main 环境）：`test_task_errors.py` 42 项通过；`backend/` pytest 814 passed、241 skipped；ruff 通过
- **未测试（Not Tested）**：Windows 上重跑（不再连网络，预期与 macOS 相同）

## 修改建议（后续）

无。
