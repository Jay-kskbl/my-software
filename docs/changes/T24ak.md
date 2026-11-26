# 修改记录：T24ak Windows 任务书新增 W10（2026-11-26）

- 来源：Barry 于 2026-11-26 指示“如果还有什么测试需要完成，依旧是写入 windows 任务书”
- 任务性质：只改文档，不带 🔒；没有改代码、配置、表结构、接口、附录 A，没有新依赖
- 修改者：Claude（Opus 5.5）

## 逐文件修改记录

| 文件 | 位置 | 修改前 | 修改后 | 原因与影响 |
|---|---|---|---|---|
| `windows任务书.md` | 文件头 | — | 增补一行 | 说明第 18 节的来由 |
| 同上 | 第 17.1 节“2026-11-26 更新” | 17.9 backend 6 项、17.6 第 3a 步写在这里 | 加一句：改到第 18 节做 | 避免两处安排同一件事 |
| 同上 | 新增第 18 节 W10 | — | 18.1 顺序；18.2 基线（要有 T24ah–T24aj）；18.3 backend 全套测试，`--basetemp` 目录先建好，预期 1056 项、0 failed、0 skipped；18.4 backend 6 项符号链接；18.5 数据库停掉时 A–G 七步（接口 503 与耗时、重复 3 次、浏览器第 3a 步、恢复、2 秒超时、`consistency check` 与 `alembic current`、恢复后检查）；18.6 `git_dirty`；18.7 验收；18.8 判定 | Mac 上测不了的部分：连被拒绝端口的 Windows 行为、真实 PostgreSQL 上的集成测试和迁移入口、符号链接权限 |
| `docs/untested.md` | 第 7.5 节三行 | “未测试”没有写在哪里补 | 指向第 18.3、18.5、18.6 节 | — |
| `DEVPLAN.md` | §3 任务、§5 记录 | T24ah 记录写“新增单元测试 2 项” | 更正为 3 项（漏数了 `test_connect_timeout_is_required`）；新增 T24ak | 用 `e1d61eb` 的工作树收集到 1052 项、现在 1056 项对出来的 |
| `docs/changes/T24ah.md` | `test_db_session.py` 一行 | 新增 1 项 | 新增 2 项 | 同上 |

## 验证

- 只改文档，没有运行测试。第 18 节里引用的预期已逐项对过代码：`consistency check` 连不上数据库时打印“无法连接数据库……”并返回 1；`alembic` 经 `env.py` 用 `DATABASE_CONNECT_TIMEOUT_SECONDS`；前端 503 的提示与第 17.6 节第 3 步相同；测试名与 Mac 上的收集结果一致
- **未测试（Not Tested）**：第 18 节的全部内容（要在 Windows 上执行）

## 修改建议（后续）

Windows 结果回来后按第 18.7 节核对，通过的项从 `docs/untested.md` 第 7.5 节删除。
