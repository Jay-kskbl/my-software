# 修改记录：T24aj 实验记录的 `git_dirty` 只看已跟踪文件（2026-11-26）

- 来源：`docs/changes/windows-2026-11-26-核对.md` 第 2 节“其他”第 1 条，Barry 于 2026-11-26 批准（“Fix both”）
- 任务性质：小改动，不带 🔒；没有改表结构、索引、接口、配置、附录 A，没有新依赖；`config.json` 的字段和格式不变
- 修改者：Claude（Opus 5.5）

## 逐文件修改记录

| 文件 | 位置 | 修改前 | 修改后 | 原因与影响 |
|---|---|---|---|---|
| `backend/app/modules/experiments/environment.py` | `machine_info()` | `git status --porcelain`，未跟踪的文件也算 | `git status --porcelain --untracked-files=no` | Windows 上一直有未跟踪的 `output/`，`git_dirty` 每次都是 true，失去意义（W9 17.4）。已跟踪文件有未提交改动时仍为 true |
| `backend/tests/unit/test_experiment_framework.py` | 新增 1 项 | — | 在临时目录建 git 仓库：只有未跟踪的 `output/` 时为 false；改了已跟踪文件后为 true | 把 `environment.PROJECT_ROOT` 指到临时仓库，不碰本仓库 |
| `DEVPLAN.md`、`docs/untested.md` | — | — | 新任务、§4 标记、§5 完成记录；第 7.5 节一行改写 | — |

## 局限

- 新建了一个源码文件却没有 `git add` 时，`git_dirty` 不会因此变 true。只有已跟踪的代码 import 它才会被运行，而那样已跟踪文件本身就有改动，所以影响很小；实验配置文件本身会完整写进 `config.json`。
- 以前的实验记录里 `git_dirty: true` 可能只是因为有未跟踪文件，不能据此判断当时代码被改过。
- D50 里说的“mapping 改成 CRLF 而没提交时 `git_dirty` 不会变 true”不受影响，仍以 hash 为准。

## 验证

- 已运行（macOS，main 环境）：新增测试通过；用修改前的代码，新增测试失败；`backend/` pytest 815 passed、241 skipped；ruff 通过
- **未测试（Not Tested）**：Windows 上实际跑一次实验，看 `config.json` 的 `git_dirty`

## 修改建议（后续）

无。
