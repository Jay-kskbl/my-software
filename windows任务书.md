# Windows 任务书（2026-11-19）

- 签发：Barry
- 执行：在 Barry 的 Windows 机器上工作的 GPT
- 撰写：Claude（macOS 会话）。Claude 不参与执行，也不在 macOS 上测试本任务书中的任何内容
- 基线：GitHub `main` 上包含本文件的那个提交（本文件随该提交一起推送）
- 增补：2026-11-21 14:26 添加 W4（T24s 前端界面优化的真实后端联调与界面核对，第 10 节），并在第 1、8、9 节补了对应的行
- 增补：2026-11-21 14:29 第 1 节补上 T24k–T24r（任务书写成之后、T24s 之前完成的 8 项；T24j 就是 W2，还没有做）
- 增补：2026-11-21 14:37 添加 W5（T24k、T24l、T24m、T24o、T24p 在真实环境上的补测，第 11 节），并在第 1、4、8、9 节补了对应的行
- 增补：2026-11-21 19:40 收到第一轮执行结果（GitHub `bb3883c`，执行者 Codex，基于 `8fb5830`）后添加：第 0 节（当前状态、基线同步、报告格式、测试计划、怎样才算完成）；W6（新基线复测、符号链接、其余真实环境补测、补交 W1–W3 原始数据，第 12 节）；W7（跨机器 CLIP 向量一致性、同时运行的内存、负载下的查询编码，第 13 节）；第 14 节（交回的原始数据与 Claude 的核对方法）；第 15 节（不交给 Windows 的项目）。并在第 2、8、9 节补了对应的行。W1–W5 已写的内容没有改
- 增补：2026-11-21 21:20 读了第一轮补充上传的日志（`0408d25`，核对记录见 `docs/changes/windows-2026-11-21-补充核对.md`）后，添加 W8（第 16 节：查 OCR 崩溃的事件日志、复现崩溃、OCR Worker 数与吞吐、smartcn 怎么切英文、B2 漏检分析、没有内存上限时的畸形文件防护），并在第 0.1、0.4、8、9、14 节补了对应的行；第 0.1 节的发现那一段补了一句。W1–W7 已写的步骤没有改

- 增补：2026-11-23 收到第二轮结果（`065e640`、`54d9760`，基线 `fd0b5eb`，执行者 Codex），核对后添加 W9（第 17 节：没完成的项目与改良后的补测方案，执行顺序见第 17.1 节），更新第 0.1 节的状态，更正第 16.8 节对照组的预期。W1–W8 已写的步骤没有改

- 增补：2026-11-25 核对第五轮结果（`415d343`）后，在第 17.1 节加更新说明，新增第 17.14 节（OCR Worker 数与崩溃，按正确的方法重做）

- 增补：2026-11-25 按 Barry 的要求重排第 17.1 节的执行顺序，各节步骤没有改

- 增补：2026-11-25 前端整体放入（T24ba–T24be，T24bg）：新增第 17.18 节（界面更新），第 17.1、17.2、17.12、17.13、14.2 节补上对应内容；第 10.2 节第 2、4、8、9 项和第 10.5 节只加注，原文保留（W4 是在改动前的界面上执行的）
- 增补：2026-11-26 W9 核对之后的修复（T24ah 数据库连接超时、T24ai 测试写法、T24aj `git_dirty`）：新增第 18 节 W10，安排这三项在 Windows 上的验证，以及 W9 没做完的第 17.6 节第 3a 步、第 17.9 节 backend 6 项；第 17.1 节的 2026-11-26 更新加了指向第 18 节的说明

本任务书有九项任务。**W1–W8 的执行顺序以第 0.4 节为准，W9 以第 17.1 节为准**（W4 于 2026-11-21 14:26 添加，W5 于 14:37 添加，W6、W7 于 19:40 添加，W8 于 21:20 添加，W9 于 2026-11-23 添加；W1–W8 已执行，状态见第 0.1 节）：

| 编号 | 任务 | 结果 |
|---|---|---|
| W1 | 补测：T24g 之后的代码、8 项符号链接测试、OCR 烟测脚本 | 全部测试的原始结果（JUnit XML） |
| W2 | T24j：写 DocVQA 数据集的下载与转换脚本 | 一个脚本 + 它的单元测试 + 转换好的实验数据 |
| W3 | 用 DocVQA 把实验流程从导入到 B0–B3 全部跑通 | 10 组实验的结果目录和汇总 |
| W4 | T24s 前端：真实后端联调、鼠标真实拖入、Windows 浏览器显示、重新截图（2026-11-21 14:26 添加） | 报告里的逐项核对结果 + 新界面截图 |
| W5 | T24k/T24l/T24m/T24o/T24p 的补测：换行符预检、一致性检查的结构比较与重建、空库启动 Worker、连接超时、生产构建（2026-11-21 14:37 添加） | 报告里的逐项结果（命令输出、退出码、耗时） |
| W6 | 新基线上的全套复测；8 项符号链接测试（Barry 本人的终端）；一致性修复、Worker 崩溃恢复与并发、解析超时、Ctrl-C、端口占用、真实文件解析与 OCR 的真实环境补测；补交 W1–W3 的原始数据（2026-11-21 19:40 添加） | JUnit XML、数据库与索引的导出文件、命令输出、真实样本与人工抄录文本 |
| W7 | 跨机器 CLIP 向量一致性；数据库、OpenSearch、后端、两个 Worker、CLIP 同时运行时的内存采样；OCR 负载下的查询编码耗时（2026-11-21 19:40 添加） | 向量 JSON、内存采样 CSV、检索耗时 CSV |
| W8 | 针对第一轮日志的补充测试：事件日志查 OCR 崩溃、复现崩溃、1/2/4 个 OCR Worker 的吞吐、smartcn 切英文、B2 漏检的导出与人工核对、没有内存上限时的畸形文件防护（2026-11-21 21:20 添加） | 事件日志导出、任务 CSV、1 秒间隔的内存与 CPU 采样、分词结果、OCR 文本导出、人工答案、畸形文件的任务 JSON |
| W9 | 第二轮没完成的项目与改良方案：连接超时改用本地监听、一致性修复后的检索结果按新标准重测、Ctrl+C 修复后重测、登录页与停机刷新、300 秒超时的文档，以及由 Barry 本人做的符号链接、真实文件、拖拽、人工核对（2026-11-23 添加） | 见第 17.12 节 |

做完后按第 8 节交付，按第 9 节自查，按第 14 节交回原始数据。

------------------------------------------------------------------------

## 0. 当前状态与测试计划（2026-11-21 19:40 添加）

### 0.1 各任务的状态

| 编号 | 状态（2026-11-21 19:40） | 依据 | 还差什么 |
|---|---|---|---|
| W1 | **部分完成**：除 8 项符号链接测试外全部通过（backend 932 passed、6 failed；shared 103 passed、2 failed；OCR Worker、CLIP 真实模型、前端、ruff、OCR 烟测都通过）。失败原因：执行账号 `codexsandboxoffline` 没有 `SeCreateSymbolicLinkPrivilege`，提权返回退出码 4 | `windows任务报告.txt` 第二、三节，`output/windows-w1/*.xml` | ① 8 项符号链接测试由 Barry 本人的终端跑（W6 第 12.3 节）；② W1 测的是 `8fb5830`，之后 Mac 上的提交（T24k–T24s）没测过，要在新基线上重跑（W6 第 12.2 节） |
| W2 | **执行方报告完成**：500 条查询、500 张 JPEG、重跑逐字节一致、`validate` 退出码 0、脚本测试 12 passed | 报告第四节，`bba3a1b` | Claude 核对（第 14.2 节） |
| W3 | **执行方报告完成**：10 个配置 × 3 次重复，退出码都是 0；`reocr` 前后 OCR 片段都是 1589；一致性检查退出码 0 | 报告第五至七节，`docvqa-runs.zip`（SHA-256 `287E939A…452504`） | ① 补交原始数据（W6 第 12.11 节）；② Claude 核对（第 14.2 节） |
| W4 | 未开始 | — | 按第 10 节做 |
| W5 | 未开始 | — | 按第 11 节做 |
| W6、W7 | 新增，未开始 | — | 按第 12、13 节做 |
| W8 | 新增（2026-11-21 21:20），未开始 | — | 按第 16 节做 |

**2026-11-23 更新（第二轮结果，核对见 `docs/changes/windows-2026-11-23-核对.md`）：**

| 编号 | 状态（2026-11-23） | 还差什么 |
|---|---|---|
| W1–W3 | 完成（W3 的处理过程数字已由 12.11 的原始数据证实） | 8 项符号链接（W9 第 17.9 节） |
| W4 | 部分完成：联调各项通过；停机刷新跳登录页（T24x 已修，要在新基线上重测）；全关时 `ch` 残留（Barry 定为保留现状，不算偏差） | 真实拖拽（17.7）、停机刷新与登录页（17.6） |
| W5 | 11.2–11.4、11.6 完成 | 11.5 改用本地监听重测（17.3） |
| W6 | 12.2、12.4 修复路径、12.5、12.6、12.8、12.11 完成；12.7 **未通过**（Windows 上 Ctrl+C 打断当前任务，代码问题） | 12.3（17.9）、12.4 第 10 步（17.4）、12.7（17.5，等修复）、12.9–12.10（17.10）、`mapping-eol.txt`（17.2） |
| W7 | 完成（13.2 的合计峰值由 Claude 按原始数据更正为 5732.8 MB） | — |
| W8 | 16.3–16.6、16.7 A、16.8 完成 | 16.7 B（17.11）、16.5 的一次超时（17.8） |
| W9 | 新增，未开始 | 按第 17 节做 |

第一轮里值得记下的发现（Claude 会写进 `docs/untested.md` 和 T27 的参考）：两张图片（`mjbw0217.jpg`、`mkvw0217.jpg`）的 OCR 子进程以 `0xC0000005`（访问违例）退出，自动重试 3 次都失败，改成只开一个 OCR Worker 后手动重试才成功；处理阶段同时开了 4 个 OCR Worker，OCR 每个任务平均 53.57 秒（macOS 单张测试图 0.44 秒，两者条件不同，不能直接比较）；DocVQA 上 B3 的指标低于 B2（CLIP 对英文查询起了负作用）。（2026-11-21 21:20 补充：补充上传的日志显示，崩溃一共 8 次、涉及 4 个文档，全部集中在 14:31:08–14:31:59，4 个 Worker 都碰到了；reocr 时没有再崩。详见第 16.1 节，W8 要查清原因。）

### 0.2 基线同步（Barry 做，Claude 不 push）

**状态（2026-11-21 21:30 更新）：** 第一轮结果已合并进 Mac 的 `main`（`1178e1c`），Barry 已把 `main` 推到 GitHub（推送时到 `c4e7561`，含 T24k–T24u、W4–W7 和本节）。Windows 的工作区还停在第一轮的 `bb3883c`，W4–W7 要用新代码，所以开始之前：

1. ~~Barry 在 Mac 上合并并推送~~（已完成，见上）。
2. Windows 上 `git pull`，确认是快进（fast-forward），而且拉到的提交不早于 `c4e7561`：`git merge-base --is-ancestor c4e7561 HEAD; echo $LASTEXITCODE` 输出 0，`git show HEAD:windows任务书.md` 能找到“0. 当前状态与测试计划”和第 0.2 节第 4 步。
3. 把这个提交号写进报告，并写进每个任务的 `output/windows-<任务>/git-head.txt`（第 14.1 节）。W6、W7 的结果只对这个提交有效。
4. **重新签出三个 mapping 文件（T24u，2026-11-21 21:10 添加）。** 这台机器的工作区是 T24u 之前签出的，三个 mapping 现在是 CRLF；拉到 T24u 后 git 不会重写它们，`git status` 也不显示修改，`git checkout --` 同样会跳过。要先删再签出（在仓库根目录）：

   ```powershell
   Remove-Item shared\text_index\mappings\*.json, backend\app\modules\vector_index\mappings\*.json
   git checkout -- shared/text_index/mappings backend/app/modules/vector_index/mappings
   git ls-files --eol -- shared/text_index/mappings backend/app/modules/vector_index/mappings
   Get-FileHash shared\text_index\mappings\*.json, backend\app\modules\vector_index\mappings\*.json -Algorithm SHA256
   ```

   预期：三行都是 `i/lf w/lf attr/text eol=lf`；SHA-256 开头分别为 `be91f8071d05`（doc_meta）、`0c7937251bab`（chunks）、`c984e85b889b`（image_vectors），与 Mac 一致。把输出存成 `output/windows-w6/mapping-eol.txt`。不做这一步，之后的实验记录仍会是 CRLF 的 hash。

### 0.3 报告格式

Barry 要求 Windows 上的执行者不新建、不修改 `.md` 文件。所以：

- 报告继续写在 `windows任务报告.txt`，在末尾按 W4、W5、W6、W7 各加一节，不改前面已有的内容。
- 任务书里要求写成 `.md` 的交付物（例如第 8 节的 `docs/changes/T24j.md`、`docs/downloads.md`），改为同名 `.txt`。Claude 核对后再转成 `.md` 并入文档。
- 文中的“GPT”指在 Windows 上执行本任务书的 AI（第一轮是 Codex），规则相同。

### 0.4 测试计划（执行顺序）

| 顺序 | 内容 | 谁做 | 依赖 | 预计耗时 |
|---|---|---|---|---|
| 1 | 基线同步（第 0.2 节） | Barry | — | 10 分钟 |
| 2 | W8 第 16.3 节：查事件日志里的 OCR 崩溃记录（应用程序日志满了会覆盖旧记录，越早做越好；2026-11-21 21:20 添加） | GPT | 1 | 10 分钟 |
| 3 | W5 第 11.2 节：换行符预检 | GPT | 1 | 10 分钟 |
| 4 | W6 第 12.2 节：新基线全套复测 | GPT | 3 | 1 小时 |
| 5 | W6 第 12.3 节：8 项符号链接测试 | **Barry 本人**（开发人员模式或管理员终端） | 1 | 20 分钟 |
| 6 | W6 第 12.11 节：补交 W1–W3 原始数据（`docmgr_docvqa` 还在时先导出，免得后面的步骤改了它）；同时做 W8 第 16.6 节和第 16.7 节 A（都只读 `docmgr_docvqa` 和 `docvqa_` 索引；2026-11-21 21:20 添加） | GPT | 1 | 45 分钟 |
| 7 | W5 第 11.3–11.6 节 | GPT | 4 | 1 小时 |
| 8 | W4（第 10 节） | GPT；第 10.3 节的鼠标拖入要有人操作 | 4 | 2 小时 |
| 9 | W6 第 12.4–12.10 节 | GPT；第 12.9 节的真实样本和人工抄录由 Barry 准备 | 4、6 | 半天 |
| 10 | W7（第 13 节） | GPT | 9（用 W6 建好的 `docmgr_w6`） | 1 小时 |
| 11 | W8 第 16.4、16.5、16.8 节（会把 CPU 占满，不要和 W7 或其他测量同时跑；2026-11-21 21:20 添加） | GPT | 10 | 3–4 小时 |
| 12 | W8 第 16.7 节 B：30 条漏检查询的人工核对（不依赖其他步骤，任何时候都可以做；2026-11-21 21:20 添加） | **Barry 本人** | — | 40 分钟 |
| 13 | 按第 14.1 节整理原始数据、算 SHA-256、提交；Barry 推送，大文件另交 | GPT、Barry | 全部 | 30 分钟 |

（2026-11-21 21:20：插入 W8 后重新编了号。原来的第 2–9 步依次变成第 3–10 步，原来的第 10 步变成第 13 步；原有步骤的内容没有变，只在第 6 步加上了 W8 的两项只读导出。）

某一步做不了时，按第 9 节最后一句处理：写明卡在哪里，继续做不依赖它的步骤。

### 0.5 怎样才算“测试已成功完成”

一项测试要同时满足下面三条，Claude 才会把它从 `docs/untested.md` 删除、在 DEVPLAN 里记成已验证：

1. **执行方自查通过**：该节“验收标准”里的每一条都打了勾，报告里写了命令、输出、退出码。
2. **原始数据齐全**：第 14.1 节列出的文件都交回了，`SHA256SUMS.txt` 与收到的文件一致，`git-head.txt` 是第 0.2 节确认的提交。
3. **Claude 核对通过**：按第 14.2 节的方法，用原始数据重算或比对，结果与报告一致。

只有报告里的一句“通过”、没有原始数据的，记为“执行方报告通过，未核对”，不算完成。Claude 核对的结果与报告不一致时，以原始数据为准，把这一项列给 Barry，不在 `untested.md` 里删除。

------------------------------------------------------------------------

## 1. 背景

本仓库是 Barry 的本科毕业设计：基于多模态信息检索的智能文档管理系统。开始前**必须先读**：

1. `GLOBAL.md`：全局约束，冲突时以它为准；附录 A 是已定决策，不得修改
2. `CLAUDE.md`：命令速查（启动后端、Worker、OCR Worker、CLIP 服务、测试、实验）
3. `experiments/README.md`：实验数据的三个文件怎么填、操作顺序、结果格式、退出码
4. `docs/changes/windows-2026-11-19-原始说明.txt`（原在仓库根目录，T24r 移到这里）：上一轮 Windows 测试（2026-11-19，基于 `50b244b`）的结果
5. `docs/untested.md`：当前的未测试清单，尤其是第 1、3、7 节

上一轮之后新增的代码：

| 任务 | 改动 | 要补的测试 |
|---|---|---|
| T24g | 实验运行前检查拦下混用的 OCR 模型 | `test_experiments_db.py::test_preflight_reports_mixed_ocr_models` |
| T24h | 烟测脚本 `scripts/smoke/ocr_e2e.py` 查 `ocr_results.params` | 运行烟测脚本 |
| T24i | 新命令 `python -m app.modules.experiments reocr [--yes]` | `test_experiments_db.py` 中 `test_reocr_requeues_finished_ocr_tasks_of_the_current_version`、`test_reocr_refuses_while_parse_or_ocr_tasks_are_unfinished` |
| T24k（2026-11-21 14:29 添加） | `891facb`：通用 Worker 与 OCR Worker 连接数据库带 `connect_timeout`，新配置 `WORKER_DB_CONNECT_TIMEOUT_SECONDS`、`OCR_WORKER_DB_CONNECT_TIMEOUT_SECONDS`（默认 10 秒，`.env.example` 已同步）。对执行的影响：`.env` 不用改（不写就用默认值）；数据库连不上时 Worker 约 10 秒内报错退出，不再卡一两分钟 | W1 第 1–3 项会一并跑到（shared `test_task_queue.py`，backend `test_worker_main.py` 等，OCR Worker `test_store_connect.py`）；连不通的地址上的实际超时见 W5 第 11.5 节（2026-11-21 14:37 添加） |
| T24l（2026-11-21 14:29 添加） | `f31590b`：通用 Worker 启动时比对 `alembic_version` 与代码里的最新迁移，OCR Worker 启动时检查它读写的表和列；不一致就以退出码 1 结束并提示 `alembic upgrade head`。迁移仍只到 `0002`。对执行的影响：W3 的 `docmgr_docvqa`、W4 的 `docmgr_ui` 必须先 `alembic upgrade head` 再启动 Worker（第 6.1、10.1 节已写），漏了 Worker 会直接退出 | W1 第 1、3 项会一并跑到（`test_worker_schema.py`、`test_store_schema.py` 是假连接的单元测试）；W3、W4 启动 Worker 时等于在真实 PostgreSQL 上走了一次“已迁移、检查通过”；空库和版本落后的情况见 W5 第 11.4 节（2026-11-21 14:37 添加） |
| T24m（2026-11-21 14:29 添加） | `49c67e4`：前端测试逐文件核对 `public/pdfjs/` 与已安装的 pdfjs-dist（比 sha256），新增 `npm run sync:pdfjs`；`package.json` 只加了这个脚本，依赖没变，不用重新 `npm install`。对执行的影响：如果这台机器的 git 开了 `core.autocrlf`，`public/pdfjs/` 里的 LICENSE、`.js` 等文本文件检出时会变成 CRLF，与 `node_modules` 里的 LF 版本 sha256 不同，`pdfjs-assets.test.mjs` 会失败。遇到时按第 4.2 节记成环境问题，写出 `git config core.autocrlf` 的值，**不要**运行 `sync:pdfjs` 去覆盖、也不要改测试。（2026-11-21 20:40 注：T24t 加了 `.gitattributes` 后，这个问题按第 11.2 节处理，见第 1 节 T24t 一行） | W1 第 5 项的 `npm test`（`tests/pdfjs-assets.test.mjs` 3 项）；**W1 之前先做 W5 第 11.2 节的换行符预检**（2026-11-21 14:37 添加） |
| T24n（2026-11-21 14:29 添加） | `0754962`：文件列表的标签不再被截断（文件名单行省略、标签换行）。T24s 又重排了这张表。对执行的影响：无 | W1 第 5 项；显示效果在 W4 第 10.2 节第 2 项一起看 |
| T24o（2026-11-21 14:29 添加） | `33a2384`：一致性检查的结构比较从 3 个键扩大到 12 个（含 `search_analyzer`），分析配置逐项比较，提示写出具体差异；mapping 和索引结构没有改，不需要重建索引。对执行的影响：W3 第 6.2 节第 5 步是这个检查第一次对真实 OpenSearch 运行。如果新建的索引就报“结构不一致”，多半是 OpenSearch 自己补上的键造成的误报：把提示原文写进报告，不要为此运行 `repair --fix rebuild-indices` | W1 第 1 项（`test_consistency.py`）；W3 第 6.2 节第 5 步；人为制造结构差异再重建见 W5 第 11.3 节（2026-11-21 14:37 添加） |
| T24p（2026-11-21 14:29 添加） | `aaa4bbc`：Element Plus 改为按需引入，首屏 JS 约 874 KB → 483 KB；没有新依赖，不用重新 `npm install`。对执行的影响：无；`npm run build` 在本机（T24s 之后）已不再提示分块超过 500 KB，Windows 上若仍提示，写进报告即可，不算失败 | W1 第 5 项（`tests/element.test.ts` 3 项和构建）；生产构建在浏览器里打开见 W5 第 11.6 节（2026-11-21 14:37 添加） |
| T24q（2026-11-21 14:29 添加） | `b18909e`：新增根目录 `README.md`（课题说明、快速开始、文档索引）。对执行的影响：无；命令仍以 `CLAUDE.md` 和本任务书为准 | 无 |
| T24r（2026-11-21 14:29 添加） | `f0ef765`：整理零散文件，上一轮的原始说明移到 `docs/changes/windows-2026-11-19-原始说明.txt`，截图移到 `docs/screenshots/windows-2026-11-19/`，空的 `output/` 目录删了。对执行的影响：第 1 节第 4 项的路径已改；W1 的 JUnit XML 仍写到 `output/windows-w1/`，`pytest --junitxml` 会自己建目录 | 无 |
| T24t（2026-11-21 20:40 添加） | `6521a1d`：新增根目录 `.gitattributes`，`frontend/public/pdfjs/**` 签出时不转换换行符（`-text`）。对执行的影响：W5 第 11.2 节的步骤已改，不再需要修改 git 设置；T24t 之前签出的工作区要按 11.2 第 5 步重新签出这个目录一次 | W5 第 11.2 节；W6 第 12.2 节的 `npm test` |
| T24u（2026-11-21 21:10 添加） | `.gitattributes` 新增两条：`shared/text_index/mappings/*.json`、`backend/app/modules/vector_index/mappings/*.json` 设 `text eol=lf`，签出和提交都用 LF。原因：第一轮 W3 的 `config.json` 里三个 mapping 的 hash 是 CRLF 版本，和仓库对不上（`docs/changes/windows-2026-11-21-核对.md` 第 5 节）。对执行的影响：**已有的工作区拉取后不会自己改正，`git status` 也看不出来**，必须按第 0.2 节第 4 步删掉这三个文件再签出 | 第 0.2 节第 4 步；W6 第 12.4 节第 10 步、W7 之后的 `config.json` 由 Claude 核对 mapping hash |
| T24s（2026-11-21 14:26 添加） | 前端界面优化（`281b226`，只改前端）：侧栏布局、拖拽上传与逐个文件的上传记录、检索通道面板、每条结果三个通道的名次与 RRF 融合分。只对着临时模拟后端检查过 | W1 第 5 项的前端测试（本机 93 项）；W4（第 10 节）的联调与界面核对 |

------------------------------------------------------------------------

## 2. 必须遵守的规则

1. **不改附录 A 的任何决策**，不改数据契约（`shared/` 里的 Pydantic 模型）、表结构、索引结构、API。需要改时停下来问 Barry。
2. **不装新依赖。** 本任务书只批准一项网络下载：W2 的 DocVQA 数据（见第 5.1 节）。其他任何下载或安装（pip 包、模型、工具、Docker）都先问 Barry。
3. **不调参。** 实验结果不理想时如实报告，不改检索参数、切分参数、OCR 参数、RRF k 来“改善”结果。
4. **不伪造。** 没有实际执行的测试写“未测试（Not Tested）”并说明原因，不写“通过”。
5. **不改 W2 以外的业务代码。** W1、W3 中发现的 bug：先记录（现象、复现步骤、日志），再问 Barry 要不要修；修复必须是最小改动，并单独提交。
6. **文档分工**：`DEVPLAN.md`、`docs/untested.md`、`docs/decisions.md` 由 Claude 收到结果后统一更新，**GPT 不要改这三个文件**。GPT 只写第 8 节列出的文件。
7. 依赖分环境：backend、shared 和 W2 脚本用 main 环境（`.venv-main`）；OCR Worker 用 `env_check/.venv-ocr`；CLIP 服务用 `env_check/.venv-clip`。不得混装。
8. 提交：每项任务（W1、W2、W3）各一个 commit，只包含该任务的改动，提交信息用中文，写明任务编号。**不要 push**，由 Barry 决定。
9. 不在日志、报告、提交里写密码、令牌和连接串。
10. **交回原始数据**（2026-11-21 19:40 添加）：W4–W8（W8 于 2026-11-21 21:20 加入本条）每一项都按第 14.1 节交回原始文件（JUnit XML、`--json` 输出、SQL 导出、命令输出原文），不能只在报告里写结论。导出前检查一遍，去掉密码、令牌、连接串。
11. **写明基线**（2026-11-21 19:40 添加）：每个任务开始前记下 `git rev-parse HEAD` 和 `git status --porcelain`；工作区有未提交改动时先停下来问 Barry，不要带着改动测试。

------------------------------------------------------------------------

## 3. 环境准备

沿用上一轮的 Windows 环境：Windows 11、Python 3.14.0、PostgreSQL 16.15、OpenSearch 2.19.1 + analysis-smartcn 2.19.1、三个虚拟环境、`models/ocr/` 与 `models/clip/clip_cn_vit-b-16.pt` 已就位。

1. 拉取 GitHub `main` 的最新提交，确认工作区干净（`git status`）。
2. **开启“开发人员模式”**（设置 → 系统 → 开发者选项），注销重登，在普通用户终端执行 `whoami /priv`，确认有 `SeCreateSymbolicLinkPrivilege`。拿不到这项权限时，W1 的 8 项符号链接测试改用有该权限的管理员终端运行，并在报告里写明用的是哪种。
3. 主库迁移到最新：在 `backend/` 下执行 `alembic upgrade head`，确认到 `0002`。
4. 测试库：确认空测试库 `docmgr_test` 存在，设置 `TEST_DATABASE_URL`、`TEST_OPENSEARCH_URL`（见 `.env.example`）。
5. 记录环境：Windows 版本、CPU、内存、Python 版本、PostgreSQL 版本、OpenSearch 版本，写进报告。

------------------------------------------------------------------------

## 4. W1：补测

### 4.1 要做的事

**（2026-11-21 14:37 添加）开始本节之前，先做第 11.2 节的 T24m 换行符预检**，把结果记进报告，否则第 5 项的前端测试失败时分不清是代码问题还是换行符问题。

| # | 内容 | 命令（目录） |
|---|---|---|
| 1 | backend 全部测试，设置 `TEST_DATABASE_URL` 和 `TEST_OPENSEARCH_URL` | `backend/`：`..\.venv-main\Scripts\python -m pytest --junitxml=..\output\windows-w1\backend.xml` |
| 2 | shared 全部测试 | `shared/`：`..\.venv-main\Scripts\python -m pytest --junitxml=..\output\windows-w1\shared.xml` |
| 3 | OCR Worker：main 环境测试 + ocr 环境真实识别 | 见 `CLAUDE.md`；main 环境加 `--junitxml=..\..\output\windows-w1\ocr_worker.xml` |
| 4 | CLIP 服务：main 环境测试 + clip 环境真实模型 | 见 `CLAUDE.md`；main 环境加 `--junitxml=..\..\output\windows-w1\clip_service.xml` |
| 5 | 前端：`npm run typecheck`、`npm test`、`npm run build` | `frontend/` |
| 6 | 代码检查：`ruff check . && ruff format --check .` | `backend/`、`shared/`、`services/ocr_worker/`、`services/clip_service/` |
| 7 | OCR 烟测（T24h），需要 PostgreSQL、OpenSearch、OCR 模型 | 仓库根目录，用法见 `scripts/smoke/ocr_e2e.py` 开头的说明；运行前测试库要先 `alembic upgrade head` 到 `0002` |
| 8 | `reocr` 命令手动走一遍（T24i）：在 W3 的数据处理完后执行 `reocr`（演练）和 `reocr --yes`，再跑一次 OCR Worker，确认任务重新完成、片段数不翻倍 | 放到 W3 的第 6.4 节一起做 |

pytest 输出的跳过（skipped）项要逐条列出原因。

### 4.2 验收标准

- [ ] backend：**0 failed、0 skipped**（包括 8 项中的 6 项符号链接测试、T24g 的 1 项、T24i 的 2 项）
- [ ] shared：0 failed（包括 2 项符号链接测试）
- [ ] OCR Worker、CLIP 服务：0 failed；skipped 的逐条说明原因
- [ ] 前端三项命令都成功；四个目录的 ruff 都通过
- [ ] 烟测脚本最后输出 PASS，且打印出 `ocr_results.params` 的三个键
- [ ] `output/windows-w1/` 下有 4 份 JUnit XML
- [ ] 有失败时：报告里写清测试名、完整错误、判断是环境问题还是代码问题；**不改测试来让它通过**（上一轮改异常类名断言那样的兼容修改，要先问 Barry）

------------------------------------------------------------------------

## 5. W2：T24j DocVQA 下载与转换脚本

### 5.1 数据集

| 项目 | 内容 |
|---|---|
| 名称 | `vidore/docvqa_test_subsampled`（Hugging Face） |
| 页面 | https://huggingface.co/datasets/vidore/docvqa_test_subsampled |
| 许可 | MIT（数据集卡片）；图片原始来源为 UCSF Industry Documents Library，原论文 DocVQA（arXiv 2007.00398） |
| 规模 | 500 行，1 个 split（`test`）；原始 Parquet 约 292 MB |
| 每行 | 一条英文查询 + 一张扫描文档页图片 |
| 用到的列 | `questionId`（字符串）、`query`（字符串）、`image`（图片）、`docId`（整数）、`image_filename`（字符串，8 个字符，如 `rnbx0223`）、`page`（字符串） |
| 不用的列 | `answer`、`question_types`（全为空）、`data_split`、`source` |

**下载方式（Barry 批准的方案 B）**：不下载 Parquet，不装 pyarrow。用 main 环境已有的 httpx 调 Hugging Face 的数据接口：

```
GET https://datasets-server.huggingface.co/rows?dataset=vidore/docvqa_test_subsampled&config=default&split=test&offset=<0,100,...,400>&length=100
```

应答的 `rows[i].row` 是一行数据，其中 `image` 是 `{"src": <临时签名地址>, "height": ..., "width": ...}`，再逐个下载 `src`。签名地址会过期，必须在同一次运行里取完列表后立刻下载；过期了就重新取列表。

**用途声明**：这批数据**只用于打通实验流程和记录性能**，不作为论文的正式检索效果结论。原因：只有英文文字型查询，没有视觉型和混合型（附录 A18）；系统的分词器 smartcn 和图文模型 Chinese-CLIP 都面向中文。

### 5.2 脚本规格

文件：`scripts/datasets/docvqa_import.py`（新建目录 `scripts/datasets/`）。用 main 环境运行：

```bash
.venv-main\Scripts\python scripts\datasets\docvqa_import.py --out experiments\docvqa
```

| 参数 | 含义 |
|---|---|
| `--out` | 输出的实验目录（即 `experiments` 命令的 `--root`），必填 |
| `--limit N` | 只处理前 N 行，用来试跑；默认全部 500 行 |
| `--timeout` | 单次请求超时秒数，默认 60 |

输出目录结构（与 `experiments/README.md` 第 1 节一致）：

```
experiments/docvqa/
  datasets/manifest.csv
  datasets/files/docvqa/<image_filename>.<png|jpg>
  datasets/source_rows.jsonl     # 原始行（不含图片），留作出处，见下文
  queries.tsv
  qrels/docvqa.tsv
```

要求：

1. **编号确定**，重跑结果完全相同：
   - `file_id` = `dv_` + `image_filename`（例如 `dv_rnbx0223`）
   - `query_id` = `dvq_` + `questionId`（例如 `dvq_57344`）
   - 两个文件按编号排序写出
2. **一张图片一个文件。** 多条查询指向同一个 `image_filename` 时，只下载一次、只写一行 manifest，qrels 里每条查询各一行。重复的图片数写进脚本输出。
3. **manifest.csv**：`type` 全部为 `image`；`source` 写 `DocVQA via vidore/docvqa_test_subsampled (MIT); images: UCSF Industry Documents Library`；`notes` 写 `docId=<docId>; page=<page>`。CSV 用标准库 `csv` 写，处理好逗号和引号。
4. **queries.tsv**：`type` 全部为 `text`；`text` 为 `query` 原文。查询里的制表符、换行替换成空格（替换了几条写进输出）。
5. **qrels/docvqa.tsv**：每条查询一行，`grade` 为 `3`（就是要找的那页，见 README 的等级定义）。只标这一页，不推测其他页是否相关。
6. **图片校验**：按文件头判断真实格式，只接受 PNG（`\x89PNG\r\n\x1a\n`）和 JPEG（`\xff\xd8\xff`），扩展名按真实格式写；其他格式不转换，脚本报错并列出这些行。单张超过 `UPLOAD_MAX_BYTES`（50 MB）也报错。记录每张图片的 sha256、字节数、宽、高。
7. **可续跑**：已存在且 sha256 与上次记录一致的图片跳过不下；中途失败（网络、超时）重试 3 次，仍失败就报错退出（退出码 1），已下载的保留。
8. **原始行留底**：`source_rows.jsonl` 每行写一条原始数据（全部列，`image` 只留宽、高，不留签名地址），外加 `sha256`、`bytes`、`saved_as`。
9. **不碰数据库和后端**：脚本只下载和写文件，不上传。上传交给 `experiments import`。
10. 结束时打印汇总：行数、查询数、不重复的图片数、重复数、下载数、跳过数、总字节数、耗时。
11. 代码风格与仓库一致：中文注释解释原因，ruff 通过；纯函数（行 → manifest/queries/qrels 的转换、文件头判断、文本清洗）与网络部分分开。

`.gitignore` 增加（与现有 `/experiments/datasets/files/` 等三行同样的写法）：

```
/experiments/docvqa/datasets/files/
/experiments/docvqa/datasets/document_map.csv
/experiments/docvqa/runs/
```

`manifest.csv`、`queries.tsv`、`qrels/docvqa.tsv`、`source_rows.jsonl` 进 Git；图片不进 Git。

### 5.3 测试

新建 `scripts/datasets/tests/test_docvqa_import.py`（pytest，main 环境），用假的行数据，不联网：

- 编号规则、排序、重跑输出相同
- 两条查询共用一张图片：manifest 一行，qrels 两行
- 文件头判断：PNG、JPEG 通过，其他（例如 GIF、WebP、空文件）报错
- 查询文本里的制表符、换行被替换
- CSV 中带逗号、引号的字段能被 `experiments validate` 读回（可以直接调用 `backend/app/modules/experiments/dataset.py` 的 `load_dataset` 验证）
- 已存在且 sha256 一致的图片不再下载（网络部分用假对象）

### 5.4 验收标准

- [ ] ruff 通过；`test_docvqa_import.py` 全部通过
- [ ] 真实运行一次：500 条查询全部写出，图片数 = 不重复的 `image_filename` 数，全部为 PNG 或 JPEG，没有超过 50 MB 的
- [ ] 再运行一次：下载数为 0，四个输出文件与第一次逐字节相同
- [ ] 在 `backend/` 下 `python -m app.modules.experiments --root ..\experiments\docvqa validate` 退出码 0，统计与脚本汇总一致
- [ ] 新增 `docs/downloads.md` 的一条登记：内容、版本（应答里 `cached-assets` 地址中的数据集修订号，如 `49bf8f13…`）、来源、安装位置、总大小、用途、批准（“Barry 于 2026-11-19 签发 Windows 任务书时批准方案 B”）
- [ ] 新增 `docs/changes/T24j.md`，格式参照 `docs/changes/T24h.md`（来源、任务性质、逐文件修改记录、验证、修改建议）

------------------------------------------------------------------------

## 6. W3：用 DocVQA 跑通实验流程

### 6.1 用独立的库、存储和索引

DocVQA 只是流程验证，**不能和以后的正式数据集混在同一套数据里**（运行前检查会把数据集外的文档算作问题，正式数据集导入时也会受干扰）。为 W3 单独准备：

| 项目 | 设置 |
|---|---|
| 数据库 | 新建空库 `docmgr_docvqa`，`DATABASE_URL` 指向它，`alembic upgrade head` |
| 文件存储 | `STORAGE_ROOT` 指向一个新的空目录 |
| 索引 | `OPENSEARCH_INDEX_PREFIX=docvqa_` |
| 配置 | 其他值与主 `.env` 相同；OCR Worker、CLIP 服务的参数保持默认，不调 |

**怎么切换：** 后端、通用 Worker、OCR Worker、CLIP 服务都固定读仓库根目录的 `.env`，不支持指定别的文件；但**进程的环境变量优先于 `.env`**（`backend/app/config.py` 用 pydantic-settings，OCR Worker 和 CLIP 服务的 `config.py` 先读 `.env` 再用 `os.environ` 覆盖）。所以不要改主 `.env`，而是在每个启动这些进程的 PowerShell 窗口里先设置：

```powershell
$env:DATABASE_URL = "postgresql://<用户>:<密码>@localhost:5432/docmgr_docvqa"
$env:STORAGE_ROOT = "<新的空目录>"
$env:OPENSEARCH_INDEX_PREFIX = "docvqa_"
```

`experiments`、`consistency`、`alembic` 命令也要在设置过这三个变量的窗口里执行（`alembic` 经 `backend/app/db/migrations/env.py` 调用同一个 `load_settings()`，同样读 `DATABASE_URL`）。每开一个新窗口都要重新设置。在报告里写明用了哪些变量（不写密码），并在启动后用 `/health` 或日志确认连的是 `docmgr_docvqa`。

### 6.2 导入与处理

在 `backend/` 下（main 环境，使用 6.1 的配置）：

1. `python -m app.modules.experiments --root ..\experiments\docvqa validate`
2. `python -m app.modules.experiments --root ..\experiments\docvqa import`
3. 启动 CLIP 服务、通用 Worker（长期运行写法见 `CLAUDE.md`）、OCR Worker，等全部任务完成
4. 记录：开始和结束时间；parse、ocr、embed 三类任务各多少个 succeeded / failed；failed 的逐条写出原因
5. 执行一致性检查 `python -m app.modules.consistency check`，记录输出和退出码

处理期间记录（够用即可，正式的性能实验是以后的 T27）：总耗时、OCR 每张图平均耗时（从 OCR Worker 日志或任务的开始/完成时间算）、四个进程的峰值内存（任务管理器或 `Get-Process` 观察即可，写明方法）。

### 6.3 运行实验

每个配置跑一次，各带 `--repeat 3`：

```bash
python -m app.modules.experiments --root ..\experiments\docvqa run --config ..\experiments\configs\B0.json --repeat 3
```

依次运行：`B0`、`B1`、`B2`、`B3`、`B3-no-ocr`、`B3-no-clip`、`clip-only`、`B3-k10`、`B3-k30`、`B3-k100`（共 10 个）。

- 运行前检查没通过时，**不要加 `--allow-incomplete`**，先按提示把原因处理掉（例如等任务完成、CLIP 服务没开）；处理不了的记录下来问 Barry。
- 每个配置记录：退出码、结果目录名、`metrics.json` 里总体的 P@10、R@10、nDCG@10（或配置里实际计算的 K）、查询延迟 P50/P95、重复 3 次的波动。

**预期现象（用来自查，不是目标）**：数据集全是图片，没有正文，所以 B1（只查正文）应该几乎检不到；B2（正文 + OCR）应明显好于 B1；B0 只匹配文件名（`rnbx0223.png` 这种编号），应该接近 0。如果实际结果与这些预期不符，**不要改参数**，在报告里写出来，并附几条查询的 `results.jsonl` 原始行。

### 6.4 `reocr` 手动检查（W1 第 8 项）

实验跑完后：

1. 记录 `chunks` 索引里 `source_type=ocr` 的片段数（或数据库 `document_chunks` 里 ocr 片段数）
2. `python -m app.modules.experiments --root ..\experiments\docvqa reocr`：记录演练输出
3. `... reocr --yes`，启动 OCR Worker 处理完
4. 再数一次 ocr 片段数：应与第 1 步相同（覆盖，不叠加）；再跑一次 `B2` 确认退出码 0

### 6.5 验收标准

- [ ] W3 全程使用独立的库、存储、索引前缀；主库没有被写入（报告里写明怎么确认的）
- [ ] 导入的文档数 = manifest 行数；parse、ocr、embed 任务全部 succeeded；有 failed 的逐条列出原因，并说明是否影响结论
- [ ] 一致性检查退出码 0（或列出每条差异及原因）
- [ ] 10 个配置都以**退出码 0** 结束，每个都有 3 次重复的结果目录，含 `config.json`、`results.jsonl`、`metrics.json`
- [ ] `reocr` 前后 ocr 片段数相同，之后 `B2` 退出码 0
- [ ] 结果目录（`experiments/docvqa/runs/`）**不提交 Git**（是否提交等 T25 时再定）；把整个目录另外打包成 `docvqa-runs.zip` 交给 Barry

------------------------------------------------------------------------

## 7. 不要做的事

- 不改 `DEVPLAN.md`、`docs/untested.md`、`docs/decisions.md`、`GLOBAL.md`、`CLAUDE.md`
- 不改检索、切分、OCR、CLIP、RRF 的参数和默认值；不改 `experiments/configs/` 下的配置
- 不往主库、主存储、主索引里导入 DocVQA
- 不安装 Docker、pyarrow 或任何新包；不下载 DocVQA 以外的数据
- 不为了让测试通过而放宽断言、跳过测试或改成 junction
- 不 push

------------------------------------------------------------------------

## 8. 交付物

| 文件 | 内容 | 进 Git |
|---|---|---|
| `windows任务报告.md`（仓库根目录） | 按第 9 节的表逐项写结果（通过 / 失败 / 未测试 + 原因），环境信息，W1 失败详情，W2 汇总，W3 每个配置的指标表和处理耗时，发现的问题与建议 | 是 |
| `output/windows-w1/*.xml` | W1 的 4 份 JUnit XML | 是 |
| `scripts/datasets/docvqa_import.py`、`scripts/datasets/tests/test_docvqa_import.py` | W2 脚本与测试 | 是 |
| `experiments/docvqa/` 下的 manifest、queries、qrels、`source_rows.jsonl` | W2 生成的数据 | 是 |
| `.gitignore` | 第 5.2 节的三行 | 是 |
| `docs/downloads.md` | 新增一条 DocVQA 登记 | 是 |
| `docs/changes/T24j.md` | W2 修改记录 | 是 |
| `docvqa-runs.zip` | W3 全部结果目录 | 否，直接交给 Barry |
| `windows任务报告.md` 的 W4 一节（2026-11-21 14:26 添加） | 第 10 节每个核对点的结果（通过 / 不符 / 未测试 + 原因）、浏览器名称和版本、发现的问题 | 是 |
| `docs/screenshots/windows-<执行日期>-t24s/*.png`（2026-11-21 14:26 添加） | 第 10.5 节的新界面截图 | 是 |
| `windows任务报告.md` 的 W5 一节（2026-11-21 14:37 添加） | 第 11 节每一步的命令、完整输出（去掉密码和连接串）、退出码、耗时；`core.autocrlf` 的值和 `git ls-files --eol` 的结果；结果与预期不符的逐条写出 | 是 |

| `windows任务报告.txt` 的 W6、W7 两节（2026-11-21 19:40 添加；报告用 `.txt`，见第 0.3 节） | 第 12、13 节每一步的命令、输出、退出码、耗时；结果与预期不符的逐条写出 | 是 |
| `output/windows-w4/` 至 `output/windows-w7/`（2026-11-21 19:40 添加） | 第 14.1 节列出的原始数据、`git-head.txt`、`SHA256SUMS.txt` | 是（单个文件超过 5 MB 的除外，见第 14.1 节） |
| 大文件压缩包（2026-11-21 19:40 添加） | 第 14.1 节中标“另交”的文件，按任务各打一个 zip | 否，交给 Barry；SHA-256 写进对应目录的 `SHA256SUMS.txt` |
| `windows任务报告.txt` 的 W8 一节、`output/windows-w8/`（2026-11-21 21:20 添加） | 第 16 节每一步的命令、输出、退出码、耗时，以及第 16.9 节列出的原始文件；`missed30-answers.tsv` 由 Barry 填好后一起提交 | 是（`ocr-chunks.csv`、日志若超过 5 MB，按第 14.1 节另交） |

提交顺序：W1（报告初稿 + XML）→ W2（脚本、测试、数据、`.gitignore`、`downloads.md`、`T24j.md`）→ W3（报告补全）→ W4（报告的 W4 一节 + 截图）→ W5（报告的 W5 一节；第 11.2 节的预检结果在 W1 的提交里先写进报告初稿）→ W6 → W7（各一个 commit，2026-11-21 19:40 添加）。

**注意（2026-11-21 19:40 添加）：** 第一轮把 `docvqa-runs.zip`（8 MB）提交进了 Git，与第 6.5 节“不提交 Git”不符。已经提交的不用撤回，是否从仓库里删除由 Barry 决定；以后的大文件按第 14.1 节另交。

------------------------------------------------------------------------

## 9. 完成标准汇总

| # | 标准 | 对应 |
|---|---|---|
| 1 | backend 0 failed、0 skipped；shared 0 failed；OCR Worker、CLIP 0 failed | 4.2 |
| 2 | 8 项符号链接测试通过，写明用的开发人员模式还是管理员终端 | 4.2 |
| 3 | T24g 1 项、T24i 2 项集成测试通过 | 4.2 |
| 4 | 烟测脚本 PASS，打印出 params | 4.2 |
| 5 | 前端三项、四个目录的 ruff 通过 | 4.2 |
| 6 | 4 份 JUnit XML | 4.2 |
| 7 | W2 脚本 ruff 通过、单元测试通过 | 5.4 |
| 8 | 500 条查询、图片全部为 PNG/JPEG、重跑输出逐字节相同 | 5.4 |
| 9 | `validate` 退出码 0 | 5.4 |
| 10 | `downloads.md`、`T24j.md` 已写 | 5.4 |
| 11 | 独立的库、存储、索引；主库未被写入 | 6.5 |
| 12 | 全部任务 succeeded（或失败逐条说明）；一致性检查通过 | 6.5 |
| 13 | 10 个配置 × 3 次重复，全部退出码 0 | 6.5 |
| 14 | `reocr` 前后片段数相同 | 6.5 |
| 15 | 报告如实：每项写通过 / 失败 / 未测试，未测试写原因；实验数字只作流程验证 | 8 |
| 16 | W4 用独立的库、存储、索引；第 10.2 节每个核对点都有结果（2026-11-21 14:26 添加） | 10.6 |
| 17 | 鼠标真实拖入：支持的类型上传成功，不支持的类型显示拒绝原因（2026-11-21 14:26 添加） | 10.6 |
| 18 | 写明看过的浏览器名称和版本（2026-11-21 14:26 添加） | 10.6 |
| 19 | 新界面截图齐全，画面里没有密码、令牌和个人文件（2026-11-21 14:26 添加） | 10.6 |
| 20 | W1 之前做了换行符预检，写明 `core.autocrlf` 和 `public/pdfjs/` 的换行符（2026-11-21 14:37 添加） | 11.7 |
| 21 | 只在 `w5_` 前缀下：结构差异被报出，重建（含 `--force`）后检查干净；其他前缀的索引没有变（2026-11-21 14:37 添加） | 11.7 |
| 22 | 空库、版本落后的库上两个 Worker 都以退出码 1 结束，提示与预期一致（2026-11-21 14:37 添加） | 11.7 |
| 23 | 连不通的地址上两个 Worker 都在设定秒数左右以退出码 1 结束（或如实写出不同的结果）（2026-11-21 14:37 添加） | 11.7 |
| 24 | 生产构建经 `npm run preview` 打开，各页面正常、没有未注册的组件（2026-11-21 14:37 添加） | 11.7 |
| 25 | 新基线上 backend、shared 0 failed（符号链接 8 项除外，单独看第 26 条）；收集到的测试与 Mac 上同一提交收集到的一致（2026-11-21 19:40 添加） | 12.12 |
| 26 | 8 项符号链接测试在 Barry 本人的终端通过，写明用的开发人员模式还是管理员终端（2026-11-21 19:40 添加） | 12.12 |
| 27 | 一致性检查的四类人为不一致都被检出并修好，之后 B2 结果与 W3 相同（2026-11-21 19:40 添加） | 12.12 |
| 28 | 强制结束 Worker 后任务被回收重做，最终没有重复数据（SQL 导出为证）（2026-11-21 19:40 添加） | 12.12 |
| 29 | 解析超时、Ctrl-C、端口占用三项的现象与预期一致，或如实写出不同（2026-11-21 19:40 添加） | 12.12 |
| 30 | 真实样本的原文件、抽取结果、人工抄录文本都交回（2026-11-21 19:40 添加） | 12.12 |
| 31 | W1–W3 的原始数据按第 12.11 节补交（2026-11-21 19:40 添加） | 12.12 |
| 32 | CLIP 向量 JSON、内存采样 CSV、负载下检索耗时 CSV 都交回，采样没有长于 15 秒的空档（2026-11-21 19:40 添加） | 13.5 |
| 33 | 每个任务目录都有 `git-head.txt`、`SHA256SUMS.txt`，与第 0.2 节的提交一致（2026-11-21 19:40 添加） | 14.1 |
| 34 | 事件日志已导出；8 个崩溃时刻对上了，或写明日志已被覆盖 / 当时没有生成（2026-11-21 21:20 添加） | 16.9 |
| 35 | 崩溃复现：单 Worker、4 Worker 各 10 轮的 CSV 齐全，1 秒间隔的内存采样覆盖全程（2026-11-21 21:20 添加） | 16.9 |
| 36 | Worker 数与吞吐：N = 1、2、4、1 四组 CSV 齐全，每组 40 个任务（2026-11-21 21:20 添加） | 16.9 |
| 37 | smartcn 分词 17 行、OCR 文本导出、30 条人工答案都交回（2026-11-21 21:20 添加） | 16.9 |
| 38 | 三个畸形文件都被拒绝解析、`attempts = 1`、错误原文与预期一致；对照组成功；通用 Worker 没有退出，峰值不超过 500 MB（2026-11-21 21:20 添加） | 16.9 |
| 39 | W9 第 17.12 节的每一条（2026-11-23 添加） | 17.12 |

任何一项做不到，不要硬凑：在报告里写明哪一项、卡在哪里、已经试过什么，然后继续做不依赖它的部分。

------------------------------------------------------------------------

## 10. W4：T24s 前端联调与界面核对（2026-11-21 14:26 添加）

T24s（`281b226`，2026-11-21）重做了前端界面，只改前端，后端和接口没有改。它只对着一个临时的模拟后端检查过（模拟后端返回虚构数据，不在仓库里），所以 `docs/untested.md` 第 4 节“T24s 前端界面优化”登记了 3 项未测试。本节把它们放到 Windows 上做。改了哪些地方见 `docs/changes/T24s.md`、`docs/decisions.md` D48。

规则：

- 只核对，**不改前端代码**。看到不符的地方按第 2 节第 5 条处理：记下现象、复现步骤、截图和浏览器控制台的报错，问 Barry 要不要修。
- 每个核对点在报告里写“通过 / 不符 / 未测试 + 原因”。`docs/untested.md` 里对应的条目由 Claude 收到报告后删除或改写（第 2 节第 6 条；CLAUDE.md 的规则是实际跑通后才删除），GPT 不改这个文件。
- 不为截图或浏览器核对安装任何新工具或浏览器扩展；截图用系统自带的截图工具（Win+Shift+S）或浏览器自带的功能。

### 10.1 环境（2026-11-21 14:26 添加）

和 W3 一样用独立的一套数据，不往主库、W3 的 `docmgr_docvqa`、测试库 `docmgr_test` 里写：

| 项目 | 设置 |
|---|---|
| 数据库 | 新建空库 `docmgr_ui`，`alembic upgrade head` |
| 文件存储 | `STORAGE_ROOT` 指向一个新的空目录 |
| 索引 | `OPENSEARCH_INDEX_PREFIX=ui_` |

切换方法同第 6.1 节：在每个启动进程的 PowerShell 窗口里先设置 `DATABASE_URL`、`STORAGE_ROOT`、`OPENSEARCH_INDEX_PREFIX` 三个环境变量。然后：

1. 启动后端、通用 Worker、OCR Worker、CLIP 服务（命令见 `CLAUDE.md`），用 `http://127.0.0.1:8000/health` 确认三项都是 `ok`。
2. 在 `frontend/` 下 `npm run dev`（与 W1 第 5 项用同一套 Node.js），浏览器打开 `http://127.0.0.1:5173`。开发服务器把 `/api`、`/health` 转发到 8000 端口。
3. 账号：用 `python -m app.modules.auth create-admin <用户名>` 建一个管理员；再在登录页注册一个普通用户。
4. 样例文件：上一轮用过的真实样本即可（中文 PDF、Word、Excel、相机 JPEG、PaddleOCR 示例图），再准备一个扫描版 PDF 或带文字的图片（看 OCR 命中）和一个不支持的文件（例如 `.txt` 或 `.gif`）。不要用个人文件。

### 10.2 用真实后端联调（2026-11-21 14:26 添加）

对应 `docs/untested.md` 第 4 节“T24s 前端界面优化”表的第 1 条“与真实后端联调”。和接口返回值比对时，打开浏览器开发者工具的“网络”面板看 `POST /api/search`、`GET /health` 的应答。

| # | 页面 | 核对点 | 预期 |
|---|---|---|---|
| 1 | 侧栏 | 管理员登录、普通用户登录各看一次 | 侧栏显示用户名；只有管理员有“管理员”标签；“文件 / 检索”导航和退出登录可用（顺带覆盖 untested.md 第 4 节“管理员视角的前端”，管理员看别人的文件时来源一栏显示管理员可见） |
| 2 | 文件页：加载 | 打开文件页；切换“全部 / 我上传的 / 共享给我的” | 列表 5 列（文件名、处理状态、大小、上传时间、操作）（T24bd 起第 2 列是“解析状态”：等待解析、解析中、已解析、解析失败，点它打开“处理详情”），类型、上传者、来源在文件名下面一行，文件名前有类型色块；空列表按范围显示不同说明 |
| 3 | 文件页：上传记录 | 点击上传区一次选 3–4 个文件 | 每个文件一条记录，依次经过“等待上传 → 上传中 → 已上传”；“清除已结束的记录”能清掉已结束的 |
| 4 | 文件页：5 秒自动刷新 | 上传后不刷新页面，看处理状态（T24bd 起叫“解析状态”） | 有等待处理或处理中的文件时，每 5 秒自动刷新一次，状态变成已完成后停止刷新 |
| 5 | 文件页：加载失败提示 | ① 停掉后端，刷新文件页；② 有文件在处理时停掉后端，等下一次自动刷新 | ① 页内红色提示“文件列表没有加载出来”；② 页内提示“自动刷新失败，列表里的状态可能不是最新的”；两种都不是弹出消息，也不是空列表。重新启动后端后恢复 |
| 6 | 文件页：共享对话框 | 打开共享对话框，再把浏览器窗口拉窄 | 对话框宽度不超出窗口（T24s 改为 `min(520px, 92vw)`，没有单独截图检查过） |
| 7 | 检索页：四个开关与 `ch` 参数 | 依次关掉“文件名”“正文”“OCR 文字”，再打开“图像（CLIP）”；四个全关一次；另用旧地址 `/search?q=<词>&img=1` 打开一次 | 默认地址里没有 `ch`；改开关后地址变成 `ch=…`，只列开着的开关；请求体的 `channels` 与开关一致，正文和 OCR 都关时请求里没有 `source_types`；四个全关时显示“至少选择一个检索通道”，不发请求；旧地址打开后图像开关是开的 |
| 8 | 检索页：改开关自动重查 | 检索过一次后改动开关；检索进行中再改一次 | 每次改动都自动重新检索（网络面板里多一次 `POST /api/search`）；进行中改动的，等这次返回后再查一次，最后显示的是按最新开关的结果（T24be 起改为：**立即取消**这次请求并按新开关重查，网络面板里旧请求是 canceled） |
| 9 | 检索页：三格名次与融合分 | 对 3–5 个结果，逐个比对卡片右侧和应答里的 `hits[].channels`、`hits[].score` | 三格（文件名 / 文字 / 图像）的“第 N 名”与应答的 `rank` 一致；应答里没有该通道、但通道执行了时显示“未命中”，没开的显示“未开启”，不可用的显示“不可用”；融合分等于 `score` 保留 4 位小数（T24be 起结果在后端返回后约 0.42 秒才显示，是收拢动画；`took_ms` 不含这段时间，核对方法不变） |
| 10 | 检索页：各通道耗时 | 比对结果汇总行和应答 | 总用时等于应答 `took_ms`；每个通道的耗时等于 `channels[].took_ms`，没开的写“未开启” |
| 11 | 检索页：CLIP 状态 | 进入检索页时看通道面板旁的 CLIP 状态，对照 `GET /health` | `clip_service.status` 为 `ok` 时显示“CLIP 服务在线” |
| 12 | 关掉 CLIP 服务后的降级显示（T32 答辩要演示） | 开着图像开关，停掉 CLIP 服务，再检索一次；然后重新启动 CLIP 服务再检索 | 停掉后：CLIP 状态变红（“CLIP 服务不可用，图像通道会被跳过”），出现黄色提示“图像检索暂时不可用，本次结果只来自文字检索（原因：…）”，图像格显示“不可用”，文字结果照常返回、没有报错页。重新启动后：图像通道检索成功，状态回到“CLIP 服务在线”。顺带覆盖 untested.md 第 4 节 T23 的“与真实后端、真实 CLIP 服务联调” |
| 13 | 预览页“返回” | ① 从检索结果点进预览页再点“← 返回”；② 把预览页地址复制到新标签页打开，再点“← 返回” | ① 回到检索页，检索词和开关还在；② 回到文件列表，不离开本系统 |

### 10.3 用鼠标从文件管理器真实拖入文件（2026-11-21 14:26 添加）

对应 `docs/untested.md` 第 4 节“T24s 前端界面优化”表的第 2 条。T24s 时是用脚本派发 drop 事件模拟的。

1. 从 Windows 文件资源管理器选中 2–3 个支持的文件（PDF、Word、Excel、PNG、JPEG），用鼠标拖到文件页的上传区松开。
2. 再拖入一个不支持的文件（例如 `.txt` 或 `.gif`）。点击选择文件时有类型过滤，拖入时没有，所以要用拖的方式才能送到后端。
3. 拖动经过上传区时看高亮：进入时高亮，在区内移动时不闪，移出时取消。

预期：支持的文件出现“已上传”记录，并开始处理；不支持的文件记录为“上传失败”，原因写明文件类型不支持（后端 415 `UNSUPPORTED_FILE_TYPE`）；浏览器没有直接打开被拖入的文件。

### 10.4 Windows 上的浏览器显示（2026-11-21 14:26 添加）

对应 `docs/untested.md` 第 4 节“T24s 前端界面优化”表的第 3 条“Chrome 以外的浏览器”。

1. 在 Edge 上把第 10.2 节的第 2、3、7、9、12 项和第 10.3 节看一遍；装了 Chrome 或 Firefox 的话也各看一遍。窗口拉到大约 1280 宽和 400 宽以下各看一次：窄的时候侧栏应收成页面顶部的一行，结果卡片的名次条换到卡片下面。
2. 报告里写明每个浏览器的名称和版本号。
3. 手边有装 Safari 的设备时，顺带看拖拽高亮会不会闪：拖动文件经过上传区里的文字时，高亮如果一闪一闪，记下来（untested.md 这一条的代码复核里记了：部分 Safari 版本拖动事件的 `relatedTarget` 可能为 null）。没有这样的设备就写“Safari 未测试”。

只看了 Edge、Chrome 时，这一条在 untested.md 里会缩小为“Safari、Firefox 未看过”，不会整条删除。

### 10.5 联调后重新截图（论文与 T31 用，2026-11-21 14:26 添加）

不对应 untested.md 的条目，对应 DEVPLAN §4 前端“待议（T24s 记录）”里的提醒：T24s 改了全部页面的布局和配色，旧截图（包括 `docs/screenshots/windows-2026-11-19/` 的 5 张）是改版之前的样子。T31 要逐条核对论文、README、截图和实际功能。

- （T24ba–T24be 之后要重截，放 `docs/screenshots/windows-<执行日期>-t24b/`，见第 17.18 节；旧截图不删。）放到 `docs/screenshots/windows-<执行日期>-t24s/`，PNG，浏览器窗口约 1280×800；文件名用英文和连字符，写明画面内容。
- 至少要有：登录页；文件页（含上传记录和处理状态）；检索页的说明状态（还没检索时）；全通道检索结果（能看清三格名次和融合分）；关掉一个通道后的对照结果；CLIP 停掉后的降级显示；预览页的 PDF 原文件和图片的抽取文本；窄窗口布局一张。
- 画面里不能有密码、令牌、连接串和个人文件。
- 旧截图不要删，用不用由 Barry 和 Claude 定。

### 10.6 验收标准（2026-11-21 14:26 添加）

- [ ] 全程使用独立的库、存储、索引前缀（`docmgr_ui`、`ui_`）；主库、`docmgr_docvqa`、`docmgr_test` 没有被写入（报告里写明怎么确认的）
- [ ] 第 10.2 节 13 个核对点都有结果；不符的附截图、复现步骤和控制台报错
- [ ] 第 10.3 节：鼠标拖入的支持类型上传成功，不支持的类型显示了拒绝原因
- [ ] 第 10.4 节：写明看过的浏览器名称和版本；Safari 有没有看写清楚
- [ ] 第 10.5 节的截图齐全，画面里没有敏感信息
- [ ] 没有改任何前端代码；发现的问题只记录、问 Barry


------------------------------------------------------------------------

## 11. W5：T24k、T24l、T24m、T24o、T24p 的补测（2026-11-21 14:37 添加）

这五项在 macOS 上只跑了单元测试（假连接、假应答），真实环境上的行为没有验证过（`docs/untested.md` 第 4 节、第 7.2 节）。改了什么见第 1 节对应的行和 `docs/changes/T24k.md`、`T24l.md`、`T24m.md`、`T24o.md`、`T24p.md`。

规则与 W4 相同：

- 只核对，**不改任何代码和配置文件**（包括 `.gitattributes`、`package.json`、mapping 文件）。结果不符时记下现象、复现步骤、完整输出，问 Barry（第 2 节第 5 条）。
- 每一步在报告里写命令、输出（去掉密码和连接串）、退出码；要计时的写耗时。`docs/untested.md` 里对应的条目由 Claude 收到报告后删除或改写，GPT 不改这个文件。
- 不装任何新工具；下面用到的 `git`、`psql`、`curl.exe`、PowerShell 的 `Invoke-RestMethod` 都是这台机器上已有的。
- 第 11.2 节在 W1 之前做；第 11.3–11.6 节按顺序做。

### 11.1 环境（2026-11-21 14:37 添加）

和 W3、W4 一样用独立的一套数据，不碰主库、`docmgr_test`、W3 的 `docmgr_docvqa` 和 W4 的 `docmgr_ui`：

| 项目 | 设置 | 用在 |
|---|---|---|
| 数据库 | 新建空库 `docmgr_w5`，`alembic upgrade head` | 11.3、11.6 |
| 数据库 | 新建空库 `docmgr_w5_empty`，**不要**执行 `alembic upgrade` | 11.4 |
| 文件存储 | `STORAGE_ROOT` 指向一个新的空目录 | 11.3、11.6 |
| 索引 | `OPENSEARCH_INDEX_PREFIX=w5_`（索引名为 `w5_doc_meta`、`w5_chunks`、`w5_image_vectors`） | 11.3、11.6 |

切换方法同第 6.1 节：每个 PowerShell 窗口先设置 `DATABASE_URL`、`STORAGE_ROOT`、`OPENSEARCH_INDEX_PREFIX`。建库可以用 `psql -h localhost -U <用户> -c "CREATE DATABASE docmgr_w5"`（`docmgr_w5_empty` 同样）。第 11.4、11.5 节会把 `DATABASE_URL` 改成别的值，**每一节开一个新窗口**，做完关掉，免得后面的命令带着错误的设置运行。

### 11.2 T24m 换行符预检（在 W1 之前做，2026-11-21 14:37 添加；按 T24t 修改于 2026-11-21 20:40）

T24t 在仓库根目录加了 `.gitattributes`，`frontend/public/pdfjs/**` 签出时不做换行符转换，Windows 上不需要再改 `core.autocrlf`。

背景：`tests/pdfjs-assets.test.mjs`（T24m）逐个比较 `frontend/public/pdfjs/` 与 `node_modules/pdfjs-dist` 里文件的 sha256。202 个文件里有 15 个是文本（LICENSE、`.js`），`core.autocrlf=true` 时它们原来会被签出成 CRLF，sha256 跟着变，测试就失败。对应 `docs/untested.md` 第 7.2 节“T24g 之后的代码”一行里的 T24m。

1. 确认已拉到 T24t：`git log --oneline -1 -- .gitattributes` 有输出（Barry 推送之后才拉得到，见第 0.2 节）。没有输出就先停下，不要往下做。
2. 记下 `git config --show-origin --get core.autocrlf` 的结果（只记录，不修改；没有输出就是没设置）。
3. `git ls-files --eol -- frontend/public/pdfjs`。预期每行的属性列都是 `attr/-text`，工作区列是 `w/lf` 或 `w/-text`，没有 `w/crlf`。**注意：** `git diff --stat` 在 `autocrlf=true` 时看不出换行符的差别，所以要用 `--eol`。
4. 在 `frontend/` 下 `npm test -- tests/pdfjs-assets.test.mjs`，预期 3 项通过。
5. 如果这份签出是 T24t 之前做的、第 3 步里还有 `w/crlf`，`git status --short -- frontend/public/pdfjs` 可能把这些文件显示为已修改（只是换行符不同，不是内容改动）。直接 `git checkout -- frontend/public/pdfjs` 重新签出这个目录，再重做第 3、4 步。**不要**改 `core.autocrlf`，**不要**运行 `npm run sync:pdfjs`（它会用 `node_modules` 里的文件覆盖，把问题掩盖掉）。

报告里写明第 2 步的值、第 3 步的结果（有没有 `w/crlf`）、是否做了第 5 步、第 4 步的结果。

### 11.3 T24o 一致性检查：人为制造结构差异，再只重建 `w5_` 的索引（2026-11-21 14:37 添加）

对应 `docs/untested.md` 第 4 节“一致性检查对真实 OpenSearch 的操作”（T24o 扩大了结构比较的范围，担心真实 OpenSearch 自己补上的键造成误报），以及“T24d rebuild-indices --force”一节的“对真实 OpenSearch 执行 `--fix rebuild-indices --force --yes`”。做法参照 `docs/changes/T24o.md` 修改建议第 1 条、`docs/decisions.md` D31、D43。

**每一步执行 `consistency` 命令之前，先确认前缀：** `echo $env:OPENSEARCH_INDEX_PREFIX` 必须输出 `w5_`，`echo $env:DATABASE_URL` 必须指向 `docmgr_w5`。前缀为空时，重建会删掉并重建主索引 `doc_meta`、`chunks`、`image_vectors`。这一节不要启动任何 Worker：重建会删索引，Worker 这时写索引会失败（D31）。

在 `backend/` 下（main 环境），先记一次全部索引：`curl.exe -s "http://127.0.0.1:9200/_cat/indices?v&h=index,docs.count,creation.date.string"`。

| # | 命令 | 预期 |
|---|---|---|
| 1 | `python -m app.modules.consistency check` | 退出码 2，报 2 个 `index_missing`：“索引 doc_meta 不存在”“索引 chunks 不存在”（提示里写的是不带前缀的名字；库里还没有图片向量，所以向量索引不存在不算问题） |
| 2 | `python -m app.modules.consistency repair --fix rebuild-indices` | 演练：打印要重建三个索引的计划和“先停掉 Worker”的提示，退出码 2，不做任何改动 |
| 3 | `python -m app.modules.consistency repair --fix rebuild-indices --yes` | 退出码 0；`_cat/indices` 里出现 `w5_doc_meta`、`w5_chunks`、`w5_image_vectors`（重建时三个一起建），其他索引的创建时间没有变 |
| 4 | `python -m app.modules.consistency check` | **退出码 0，没有任何结构问题。** 这是 T24o 的比较第一次对着真实 OpenSearch 新建的索引运行：如果这里就报“结构不一致”，就是误报，把提示原文全部写进报告，后面的步骤照做 |
| 5 | 改一处 mapping（见下面的命令） | OpenSearch 返回 `acknowledged: true` |
| 6 | `python -m app.modules.consistency check` | 退出码 2，报 `index_structure_mismatch`。用办法 A 时提示应为“索引 chunks 的结构与版本库里的 mapping 不一致：字段 text 的定义不同：search_analyzer 为 standard，应为 （未设置）”；用办法 B 时为“……多出字段 w5_extra” |
| 7 | `repair --fix rebuild-indices`（演练），再加 `--yes` | 演练退出码 2；执行退出码 0；只有 `w5_` 三个索引的创建时间变了 |
| 8 | `python -m app.modules.consistency check` | 退出码 0 |
| 9 | `repair --fix rebuild-indices --force`（演练），再加 `--yes`（D43） | 检查没有问题时也能强制重建：演练打印 `forced_rebuild` 计划，退出码 2；执行退出码 0；仍然只有 `w5_` 的索引被重建 |
| 10 | `python -m app.modules.consistency check`，最后再记一次 `_cat/indices` | 退出码 0；与开始时比较，只有 `w5_` 开头的索引是新的，其他前缀（包括主索引、`docvqa_`、`ui_`）的创建时间和文档数都没有变 |

第 5 步改 mapping 的办法：只动 `w5_chunks`，不删数据，改完由第 7 步重建恢复。

- **办法 A（优先，正好覆盖 T24o 新加的比较项）：** 给 `text` 字段加 `search_analyzer`。OpenSearch 允许对已有字段更新 `search_analyzer`，但要把原来的 `type` 和 `analyzer` 一起写上（与 `shared/text_index/mappings/chunks.json` 里一致）：

  ```powershell
  Invoke-RestMethod -Method Put -Uri "http://127.0.0.1:9200/w5_chunks/_mapping" -ContentType "application/json" -Body '{"properties":{"text":{"type":"text","analyzer":"docmgr_text","search_analyzer":"standard"}}}'
  ```

- **办法 B（A 被拒绝时用）：** 加一个版本库 mapping 里没有的字段。索引是 `dynamic: strict`，但 strict 只拒绝文档里的未知字段，用 mapping 接口显式加字段是允许的：

  ```powershell
  Invoke-RestMethod -Method Put -Uri "http://127.0.0.1:9200/w5_chunks/_mapping" -ContentType "application/json" -Body '{"properties":{"w5_extra":{"type":"keyword"}}}'
  ```

  办法 B 走的是 T24o 之前就有的“多出字段”比较，覆盖不到 T24o 新加的比较项。报告里写明用的是哪种，A 被拒绝时附上 OpenSearch 的错误原文。

不要改分析配置（`_settings` 里的 analysis）：那要先关闭索引，步骤多，容易误操作到别的索引。

### 11.4 T24l 空库上启动 Worker（2026-11-21 14:37 添加）

对应 `docs/untested.md` 第 4 节“T24l Worker 启动时检查数据库迁移”的两行（通用 Worker 的迁移版本检查、OCR Worker 的列检查，在真实 PostgreSQL 上）。提示文字取自 `backend/app/worker/schema.py`、`services/ocr_worker/ocr_worker/__main__.py`。

新开一个窗口，`DATABASE_URL` 指向 `docmgr_w5_empty`（其余两个变量照 11.1 设置），然后：

| # | 操作 | 预期 |
|---|---|---|
| 1 | 在 `backend/` 下 `..\.venv-main\Scripts\python -m app.worker`，然后 `echo $LASTEXITCODE` | 立刻结束，退出码 1，输出“Worker 无法启动：数据库还没有建表（没有 alembic_version），先在 backend/ 目录运行 alembic upgrade head” |
| 2 | 在 `services/ocr_worker/` 下 `..\..\env_check\.venv-ocr\Scripts\python -m ocr_worker`，然后 `echo $LASTEXITCODE` | 先加载 OCR 模型（日志“OCR 模型已加载”），然后结束，退出码 1，输出“OCR Worker 无法启动：数据库缺少 34 个需要的列（……等），先在 backend/ 目录运行 alembic upgrade head”，括号里列出前 5 个，都是 `document_chunks.` 开头 |
| 3 | 在 `backend/` 下 `..\.venv-main\Scripts\python -m alembic upgrade 0001`（只升到第一个迁移），再重复第 1、2 步 | 通用 Worker：退出码 1，“数据库结构版本为 ['0001']，代码要求 ['0002']：数据库落后时先在 backend/ 目录运行 alembic upgrade head；数据库比代码新时请更新代码”。OCR Worker：退出码 1，“数据库缺少 1 个需要的列（ocr_results.params）” |
| 4 | `..\.venv-main\Scripts\python -m alembic upgrade head`，再分别启动两个 Worker，启动后没有报错、进入等待时按 Ctrl+C | 两个都正常启动，不报结构问题（库里没有任务，所以只是空转） |

输出里不能有数据库密码；如果有，记下来（那是 bug）。做完关掉这个窗口，`docmgr_w5_empty` 留着或删掉都可以，报告里写明。

### 11.5 T24k 连不通的数据库地址（2026-11-21 14:37 添加）

对应 `docs/untested.md` 第 7.2 节“T24g 之后的代码”一行里的 T24k：连接超时只在 macOS 主环境实测过，OCR Worker 在 ocr 环境没有实际连过。

新开一个窗口，把 `DATABASE_URL` 设成一个**会超时**的地址，用户名、密码随便写，不要用真实的：

```powershell
$env:DATABASE_URL = "postgresql://w5:w5@10.255.255.1:5432/w5"
```

`10.255.255.1` 是一个通常不会回应的内网地址。不要用 `127.0.0.1` 上没有服务的端口：那会立刻被拒绝，测不到超时。

计时的写法（PowerShell）：

```powershell
$t0 = Get-Date; <启动命令>; $code = $LASTEXITCODE; "{0:N1} 秒，退出码 {1}" -f ((Get-Date) - $t0).TotalSeconds, $code
```

| # | 操作 | 预期 |
|---|---|---|
| 1 | 通用 Worker（`backend/` 下 `..\.venv-main\Scripts\python -m app.worker`），不设超时变量（默认 10 秒） | 约 10 秒后结束，退出码 1，输出“Worker 无法连接数据库（ConnectionTimeout），请确认数据库已启动、DATABASE_URL 正确” |
| 2 | 同上，先 `$env:WORKER_DB_CONNECT_TIMEOUT_SECONDS = "3"` | 约 3 秒后结束，退出码 1 |
| 3 | OCR Worker（`services/ocr_worker/` 下 `..\..\env_check\.venv-ocr\Scripts\python -m ocr_worker`），`$env:OCR_WORKER_DB_CONNECT_TIMEOUT_SECONDS = "5"` | 先加载模型，再约 5 秒后结束，退出码 1，输出“OCR Worker 无法连接数据库（ConnectionTimeout），请确认数据库已启动” |
| 4 | 同上，改成 `"20"` | 比第 3 步约多 15 秒 |

OCR Worker 是先加载模型、再连数据库的，总耗时里包括加载模型的时间。所以用第 3、4 步的差值（约 15 秒）判断超时设置生效，也可以对照日志里“OCR 模型已加载”那一行的时间。

如果这台机器所在的网络会立刻回绝这个地址（几秒内就报 `OperationalError`，而不是等到设定的秒数），这一节就测不到超时：如实记下现象和耗时，两种结果都有用。不要为此改网络设置。

### 11.6 T24p 生产构建在浏览器里打开（2026-11-21 14:37 添加）

对应 `docs/untested.md` 第 4 节“T24p Element Plus 按需引入”一行（生产构建产物没有在浏览器里打开过）。T24p 之前只在开发服务器上检查过：开发服务器和生产构建用的是同一份注册代码，但打包方式不同，按需引入漏掉的组件、样式只在生产构建里才可能暴露。这一步顺带看 T24s 的新界面在生产构建里的样子。

1. 用 11.1 的 `docmgr_w5`（第 11.3 节已经建好 `w5_` 索引）启动后端和通用 Worker。OCR Worker、CLIP 服务可开可不开：不开时检索页会显示 CLIP 不可用，也正好看提示条。用 `create-admin` 建一个管理员。
2. 在 `frontend/` 下 `npm run build`，再 `npm run preview`，浏览器打开它显示的地址（默认 `http://localhost:4173`）。
3. **先确认转发：** Vite 的 `preview` 沿用 `vite.config.ts` 里 `server.proxy` 的设置（本仓库用的 Vite 8.3.8 的源码里，`preview.proxy` 默认取 `server.proxy`），所以 `/api`、`/health` 应当照样转发到 8000 端口。打开开发者工具的“网络”面板登录一次，`POST /api/auth/login` 应为 200。如果是 404 或连不上，说明没有转发：这一步只能看登录页，记为限制，后面的页面不用看了。
4. 登录后各打开一次，每页都看开发者工具的“控制台”有没有报错：
   - 文件页：先上传一份中文 PDF、一张图片、一份 Word（不要用个人文件），等通用 Worker 处理完；看表格、标签、状态标签、“全部 / 我上传的 / 共享给我的”单选按钮组、分页（含每页条数下拉）、加载中的遮罩、上传区和上传记录、共享对话框、删除确认框（打开后取消，不要真删）
   - 检索页：输入框、检索通道的复选框、提示条、结果卡片、三格名次和融合分
   - 预览页：PDF 的“原文件 / 抽取文本”标签页和翻页、缩放（中文 PDF 应正常显示文字，CMap 等资源从 `pdfjs/` 加载）、图片的原图和抽取文本、Word 的抽取文本
   - 登录页：卡片、表单、注册链接
5. **怎么判断有没有漏注册的组件：** 生产构建里 Vue 不会在控制台提示“Failed to resolve component”，漏注册的组件只会原样留成一个不认识的标签、不显示内容。所以在开发者工具的“元素”面板里按 Ctrl+F 搜索 `<el-`：正常情况下一个都找不到，Element Plus 的组件会渲染成 `div`、`button` 等，class 以 `el-` 开头。找到了就记下标签名和所在页面。

### 11.7 验收标准（2026-11-21 14:37 添加）

- [ ] 第 11.2 节在 W1 之前做了：写明 `core.autocrlf` 的值、`git ls-files --eol` 的结果、单个测试的结果；确认了已拉到 T24t；做了第 5 步重新签出的写明；没有修改 `core.autocrlf`，没有运行 `sync:pdfjs`（按 T24t 修改于 2026-11-21 20:40）
- [ ] 第 11.3 节：每条 `consistency` 命令之前都确认了前缀是 `w5_`；第 4 步的结果如实写出（干净还是误报）；第 6 步报出了具体差异；第 7–10 步之后检查干净；其他前缀的索引没有变
- [ ] 第 11.4 节：空库、只升到 `0001` 的库上，两个 Worker 都以退出码 1 结束，提示与预期一致；升到最新后正常启动
- [ ] 第 11.5 节：两个 Worker 的耗时和退出码都记下了；超时设置生效（或如实写出这台机器的网络测不到超时）
- [ ] 第 11.6 节：写明 preview 有没有转发 `/api`；各页面的检查结果；“元素”面板里搜索 `<el-` 的结果
- [ ] 全程没有碰主库、`docmgr_test`、`docmgr_docvqa`、`docmgr_ui` 和它们的索引；没有改任何代码和配置文件

------------------------------------------------------------------------

## 12. W6：新基线复测与其余真实环境补测（2026-11-21 19:40 添加）

来源：第一轮结果（第 0.1 节），以及 `docs/untested.md` 第 4 节里还能在这台机器上、不装新东西就能补的项目。不能补的列在第 15 节。

规则与 W4、W5 相同：只核对，不改代码和配置文件；结果不符时记录现象、复现步骤、完整输出，问 Barry。每一步的原始数据按第 14.1 节放进 `output/windows-w6/`。

### 12.1 环境

| 用途 | 数据库 | 存储 | 索引前缀 | 用在 |
|---|---|---|---|---|
| 测试库 | `docmgr_test`（空库） | 测试自建 | 测试自建 | 12.2、12.3 |
| W3 的数据 | `docmgr_docvqa`（已有，500 个文档） | W3 的 `storage/w3-docvqa` | `docvqa_` | 12.4、12.11 |
| 本任务新建 | `docmgr_w6`（新建，`alembic upgrade head`） | 新的空目录 | `w6_` | 12.5–12.9 |

切换方法同第 6.1 节。每执行一条会写数据的命令之前，先 `echo $env:DATABASE_URL $env:OPENSEARCH_INDEX_PREFIX` 确认（输出里的密码不要抄进报告）。

### 12.2 新基线上的全套复测

**为什么：** W1 测的是 `8fb5830`。之后 Mac 上的提交里，T24k、T24l、T24o 改了后端和 shared，T24m、T24n、T24p、T24s 改了前端，都没有在 Windows 上跑过（`docs/untested.md` 第 7.2 节）。

**做法：** 在第 0.2 节确认的提交上，把第 4.1 节第 1–6 项完整重做一遍，JUnit 输出改到 `output/windows-w6/`（`backend.xml`、`shared.xml`、`ocr_worker.xml`、`clip_service.xml`）。前端三项命令的完整输出存成 `frontend-typecheck.txt`、`frontend-test.txt`、`frontend-build.txt`；ruff 的输出存成 `ruff.txt`。第 4.1 节第 7 项 OCR 烟测也重做一次，输出存成 `ocr-smoke.txt`。

另外导出收集到的测试清单，供 Claude 与 Mac 对照（先在仓库根目录 `New-Item -ItemType Directory -Force output\windows-w6`，重定向不会自己建目录）：

```powershell
# backend/ 下；shared/ 下同样做一次，文件名换成 shared-collect.txt
..\.venv-main\Scripts\python -m pytest --collect-only -q > ..\output\windows-w6\backend-collect.txt
```

**预期：** 除第 12.3 节的 8 项外，backend、shared 0 failed、0 skipped；OCR Worker、CLIP 0 failed（main 环境里因为没装 paddleocr、torch 而跳过的项，和第一轮一样逐条说明）；前端三项命令成功（T24s 之后前端单元测试在 Mac 上是 93 项）；ruff 通过；烟测 PASS。第 11.2 节的换行符预检要先做。

### 12.3 8 项符号链接测试（Barry 本人的终端）

**为什么：** 执行方的沙箱账号拿不到建符号链接的权限（第 0.1 节），这 8 项两轮都没跑成。它们测的是“存储拒绝经符号链接指向外部的路径”（GLOBAL §7.2 防路径穿越），不能跳过。

**谁做：** Barry 在自己登录的 Windows 账号下操作，不经过执行方的沙箱。

1. 设置 → 系统 → 开发者选项 → 打开“开发人员模式”，注销后重新登录。做不到时改用“以管理员身份运行”的 PowerShell。
2. `whoami /priv | Select-String SeCreateSymbolicLink`，确认有这一行。把整行输出存成 `output/windows-w6/symlink-priv.txt`。
3. 只跑这 8 项：

   ```powershell
   # backend/ 下
   ..\.venv-main\Scripts\python -m pytest --junitxml=..\output\windows-w6\symlink-backend.xml "tests/unit/test_consistency.py::test_symlinks_are_never_treated_as_stored_files" "tests/unit/test_storage.py::test_file_symlink_pointing_outside_rejected" "tests/unit/test_storage.py::test_directory_symlink_pointing_outside_rejected" "tests/unit/test_storage.py::test_put_refuses_to_write_through_directory_symlink" "tests/unit/test_storage.py::test_symlinked_temp_directory_refused_at_startup"
   # shared/ 下
   ..\.venv-main\Scripts\python -m pytest --junitxml=..\output\windows-w6\symlink-shared.xml "tests/test_storage_keys.py::test_symlinked_directory_is_rejected" "tests/test_storage_keys.py::test_symlinked_file_is_rejected"
   ```

**预期：** backend 6 passed（`test_directory_symlink_pointing_outside_rejected` 有 `[year]`、`[document]` 两个参数），shared 2 passed。报告里写明用的是开发人员模式还是管理员终端。

### 12.4 一致性检查的修复路径（在 W3 的数据上）

**为什么：** `docs/untested.md` 第 4 节：`repair --fix index`、带向量的修复、检索服务不可用时的提示，都只在假数据上测过（D31、D34、D35）。W3 的一致性检查只证明了“干净的数据检查结果干净”，没有证明“不干净的数据能被查出来、能修好”。

**前提：** 第 12.11 节的导出已经做完；所有 Worker 都停着；窗口里的变量指向 `docmgr_docvqa`、`docvqa_`。在 `backend/` 下执行。每条 `consistency` 命令都加 `--json`（`check` 支持；`repair` 不支持的就存原文），输出存成 `output/windows-w6/consistency/<步骤号>-<名称>.json|txt`，并记下退出码。

先从 `experiments/docvqa/datasets/document_map.csv` 取第一行的 `document_id`，下面记作 `<D1>`；再取第二行，记作 `<D2>`。

| # | 操作 | 预期 |
|---|---|---|
| 1 | `python -m app.modules.consistency check --json` | 退出码 0，没有问题（与 W3 相同） |
| 2 | 停掉 OpenSearch，再 `check --json` | 退出码 1；仍然输出数据库和磁盘的检查结果，并写明检索服务不可用、索引没有检查（D31、D34） |
| 3 | OpenSearch 仍停着，`repair --fix index --yes` | 退出码 1；明确提示索引类别这次没有修复，**不是**“没有需要修复的问题”（D34 修正过的行为） |
| 4 | 重新启动 OpenSearch，等 `_cluster/health` 不是 red；删掉 `<D1>` 在 `docvqa_chunks` 里的全部片段（命令见下），再 `check --json` | 退出码 2；报出 `<D1>` 的索引与数据库不一致，修复类别为 `index` |
| 5 | 删掉 `<D2>` 在 `docvqa_image_vectors` 里的向量，再 `check --json` | 退出码 2；除第 4 步的问题外，报出 `<D2>` 的向量缺失（`vector_*` 一类，D35） |
| 6 | 在 `STORAGE_ROOT` 下造一个孤立文件（做法见下），再 `check --json` | 退出码 2；多报一条 `orphan_file` |
| 7 | `repair --fix index --fix orphan-files`（演练） | 退出码 2；列出要修的三类问题，不做改动（再 `check` 一次应与第 6 步相同） |
| 8 | `repair --fix index --fix orphan-files --yes` | 退出码 0 |
| 9 | `check --json`；再数一次 `docvqa_chunks` 中 `source_type=ocr` 的片段数和 `docvqa_image_vectors` 的文档数 | 退出码 0；ocr 片段 1589、向量 500，与修复前相同 |
| 10 | 启动 CLIP 服务（B3 要用，Worker 仍然不开），`python -m app.modules.experiments --root ..\experiments\docvqa run --config ..\experiments\configs\B2.json`，再用 `B3.json` 跑一次 | 都是退出码 0；指标与 W3 的 B2、B3 相同（Claude 会逐条比对排名，见第 14.2 节） |

第 4、5 步的删除命令（只针对一个文档，`refresh=true` 让删除立刻可见）：

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:9200/docvqa_chunks/_delete_by_query?refresh=true" -ContentType "application/json" -Body '{"query":{"term":{"document_id":"<D1>"}}}'
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:9200/docvqa_image_vectors/_delete_by_query?refresh=true" -ContentType "application/json" -Body '{"query":{"term":{"document_id":"<D2>"}}}'
```

应答里的 `deleted` 分别应大于 0、等于 1，写进报告。前缀一定是 `docvqa_`，不要写成别的索引。

第 6 步造孤立文件：在 `STORAGE_ROOT\2026\` 下新建一个目录，名字是一个新生成的 UUID（`[guid]::NewGuid().ToString()`）；从 `experiments\docvqa\datasets\files\docvqa\` 复制任意一张图片进去，改名为它自己的 SHA-256（`(Get-FileHash <文件> -Algorithm SHA256).Hash.ToLower()`）加 `.jpg`。这样它的路径形状合法、数据库里没有记录。把目录名和文件名写进报告。

计数命令（第 9 步）：

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:9200/docvqa_chunks/_count" -ContentType "application/json" -Body '{"query":{"term":{"source_type":"ocr"}}}'
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:9200/docvqa_image_vectors/_count"
```

### 12.5 Worker 崩溃恢复与并发（在真实数据上）

**为什么：** T07 的崩溃恢复、并发不重复领取已经用集成测试验证过（假任务）；第一轮 W3 同时开了 4 个 OCR Worker，但没有导出能证明“没有重复数据”的原始记录。这一节在真实解析、OCR、编码上强制结束 Worker，用 SQL 导出证明任务被回收、结果没有重复（GLOBAL §9.1“Worker 中途崩溃后任务能被回收重新执行，且重复执行不产生重复记录或重复索引”）。

**准备 60 个文件的小数据集**（放在仓库外的新目录，不进 Git；不联网，从 W2 已下载的文件里复制）。在仓库根目录：

```powershell
$dst = "<仓库外的新目录>\docvqa60"
.\.venv-main\Scripts\python -I -c @'
import csv, shutil, sys
from pathlib import Path
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
with open(src / "datasets/manifest.csv", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))[:60]
ids = {r["file_id"] for r in rows}
(dst / "datasets/files/docvqa").mkdir(parents=True)
(dst / "qrels").mkdir()
with open(dst / "datasets/manifest.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
for r in rows:
    shutil.copy2(src / "datasets/files" / r["path"], dst / "datasets/files" / r["path"])
qrels = (src / "qrels/docvqa.tsv").read_text(encoding="utf-8").splitlines()
keep = [qrels[0]] + [line for line in qrels[1:] if line.split("\t")[1] in ids]
qids = {line.split("\t")[0] for line in keep[1:]}
(dst / "qrels/docvqa.tsv").write_text("\n".join(keep) + "\n", encoding="utf-8", newline="\n")
queries = (src / "queries.tsv").read_text(encoding="utf-8").splitlines()
picked = [queries[0]] + [line for line in queries[1:] if line.split("\t")[0] in qids]
(dst / "queries.tsv").write_text("\n".join(picked) + "\n", encoding="utf-8", newline="\n")
print(len(rows), "files,", len(qids), "queries")
'@ experiments\docvqa $dst
```

预期打印 `60 files, 60 queries`。然后在 `docmgr_w6`、`w6_` 下 `validate`、`import`（`--root $dst`）。

**步骤：**

1. 启动 CLIP 服务；开**两个**通用 Worker、**两个** OCR Worker（各自一个窗口）。把四个进程的 PID 写进报告（`Get-Process python | Select-Object Id, StartTime, Path`，或各窗口的启动日志）。
2. 等到至少 10 个 parse 任务完成、还有 parse 任务在处理时，查出正在处理的任务和领取者：

   ```sql
   SELECT id, task_type, document_id, claimed_by, attempts, lease_expires_at FROM processing_tasks WHERE status = 'processing';
   ```

   用 `Stop-Process -Id <PID> -Force` 强制结束其中一个通用 Worker（不是 Ctrl+C）。记下被结束的 Worker 当时持有的任务 id。
3. 用同样的办法，在 OCR 任务处理中强制结束一个 OCR Worker，记下任务 id。
4. **不要**重启被结束的两个进程。等剩下的一个通用 Worker、一个 OCR Worker 把所有任务做完（租约 60 秒到期后，被结束的进程持有的任务会回到 pending 再被领取）。
5. 全部完成后，导出下面的查询结果（第 14.1 节的 `sql/` 目录），并执行 `consistency check --json`。

```sql
-- 1 各类任务的状态与尝试次数
SELECT task_type, status, attempts, count(*) FROM processing_tasks GROUP BY 1, 2, 3 ORDER BY 1, 2, 3;
-- 2 尝试过不止一次的任务（应包含第 2、3 步记下的任务）
SELECT id, task_type, document_id, status, attempts, claimed_by, error, started_at, finished_at FROM processing_tasks WHERE attempts > 1 ORDER BY started_at;
-- 3 每个领取者处理了多少任务（应能看到四个不同的领取者）
SELECT claimed_by, task_type, count(*) FROM processing_tasks GROUP BY 1, 2 ORDER BY 1, 2;
-- 4 同一文档同时存在多个解析版本的片段（应为 0 行）
SELECT document_id, count(DISTINCT parse_version) FROM document_chunks GROUP BY 1 HAVING count(DISTINCT parse_version) > 1;
-- 5 每个文档每种来源的片段数（Claude 用来与索引计数对照）
SELECT document_id, source_type, count(*) FROM document_chunks GROUP BY 1, 2 ORDER BY 1, 2;
-- 6 同一对象的 OCR 结果重复（应为 0 行）
SELECT document_id, locator::text, count(*) FROM ocr_results GROUP BY 1, 2 HAVING count(*) > 1;
-- 7 同一内容、同一模型的向量重复（应为 0 行）
SELECT sha256, model_name, model_version, count(*) FROM image_embeddings GROUP BY 1, 2, 3 HAVING count(*) > 1;
-- 8 总数
SELECT (SELECT count(*) FROM documents) AS documents, (SELECT count(*) FROM document_chunks) AS chunks, (SELECT count(*) FROM ocr_results) AS ocr_results, (SELECT count(*) FROM image_embeddings) AS embeddings;
```

导出写法（每条一个 CSV；`psql` 的 `\copy` 在客户端写文件，不需要数据库服务器的文件权限）：

```powershell
psql -h localhost -U <用户> -d docmgr_w6 -c "\copy (<上面的查询，去掉末尾分号>) TO 'output/windows-w6/sql/w6-<编号>.csv' CSV HEADER"
```

同时导出索引计数：`curl.exe -s "http://127.0.0.1:9200/_cat/indices/w6_*?v&h=index,docs.count"` 存成 `w6-indices.txt`；再对 `w6_chunks` 按 `source_type` 做两次 `_count`（同第 12.4 节）存成 `w6-chunks-count.txt`。

**预期：** 所有任务最终 `succeeded`；第 2 条查询里有第 2、3 步记下的任务，`attempts` 为 2；第 4、6、7 条为 0 行；一致性检查退出码 0；数据库片段数与索引计数一致。

### 12.6 解析超时的端到端

**为什么：** `docs/untested.md` 第 4 节“解析超时对真实解析器的作用”：超时机制有单元测试，但“一个真的跑太久的解析被杀掉”没有端到端跑过。

1. 用 main 环境的 PyMuPDF（已有，不是新依赖）在仓库外生成一个大 PDF：

   ```powershell
   .\.venv-main\Scripts\python -I -c "import fitz,sys; d=fitz.open(); [d.new_page().insert_text((72,72), f'第 {i} 页 timeout test ' * 20, fontname='china-s') for i in range(3000)]; d.save(sys.argv[1])" "<仓库外的目录>\big3000.pdf"
   ```

2. 停掉第 12.5 节剩下的通用 Worker，在一个新窗口里设 `$env:WORKER_TASK_TIMEOUT_SECONDS = "2"`（只在这个窗口），启动一个通用 Worker。
3. 登录拿令牌、上传这个 PDF：

   ```powershell
   $tok = (Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/auth/login" -ContentType "application/json" -Body '{"username":"<用户>","password":"<密码>"}').access_token
   curl.exe -s -H "Authorization: Bearer $tok" -F "file=@<仓库外的目录>\big3000.pdf" http://127.0.0.1:8000/api/documents
   ```

   令牌和密码不要写进报告。
4. 等这个文档的 parse 任务结束，导出 `GET /api/documents/<id>` 和 `GET /api/documents/<id>/tasks` 的 JSON。
5. 关掉这个窗口的 Worker，在没有设超时变量的窗口里重新启动通用 Worker，用 `POST /api/tasks/<任务 id>/retry` 重试，等它完成后再导出一次第 4 步的两个 JSON。

**预期：** 第 4 步：parse 任务 `failed`，`attempts` 等于最大重试次数，`error` 写明超时；文档 `status` 为 `failed`；文件仍在（下载接口 200）；同时间段其他文档不受影响。第 5 步：任务 `succeeded`，文档 `succeeded`，片段数大于 0。如果 2 秒内就解析完了（第 4 步成功），把页数加到 10000 再试一次，仍然成功就如实记下耗时。

### 12.7 OCR Worker 在识别中途按 Ctrl+C

**为什么：** D34：识别子进程忽略 SIGINT，按 Ctrl+C 时父进程“处理完当前任务后退出”，正在识别的这一页不应记成失败。只有代码复核，没有实际按过。

1. 先停掉前面各节还开着的所有 Worker。在 `docmgr_w6` 下 `python -m app.modules.experiments --root <docvqa60 目录> reocr --yes`（第 12.6 节的大 PDF 不在数据集里，不受影响），只启动**一个** OCR Worker。
2. 看到日志开始识别某个任务后（记下任务 id），在这个窗口按一次 Ctrl+C。
3. 记下 Worker 打印的内容和退出码，然后查这个任务：`SELECT id, status, attempts, error FROM processing_tasks WHERE id = '<任务 id>';`

**预期：** 日志出现“收到信号 SIGINT，完成当前任务后退出”；这个任务 `succeeded`、`attempts` 为 1、`error` 为空；Worker 在这个任务之后退出，没有再领新任务。之后重新启动 OCR Worker 把剩下的任务做完（W7 要用完整的数据）。

### 12.8 端口被占用

`docs/untested.md` 第 4 节“端口被占用”。在后端已经在 8000 端口运行时，再开一个窗口在 `backend/` 下启动第二个后端（同样的命令）；CLIP 服务已经在 8001 端口时，再启动第二个 CLIP 服务。

**预期：** 第二个进程报端口被占用并退出（记下退出码和输出原文），第一个进程不受影响：`/health` 仍然 200，CLIP 的 `/health` 仍然 200。第二个 CLIP 服务会先加载模型再报错，写明从启动到退出的耗时。

### 12.9 真实文件的解析与 OCR

**为什么：** `docs/untested.md` 第 4 节：解析器和 OCR 只用程序现场生成的文件测过，没有用 Office/WPS 真正保存的文件、真实扫描件、手机照片测过。论文里的“支持格式”要有真实文件的依据。

**样本（由 Barry 准备，不要用个人文件；每个文件写清来源，填进 `output/windows-w6/real-files/sources.csv`，列为 `name,kind,made_by,source,notes`）：**

| 类型 | 至少几个 | 要求 |
|---|---|---|
| Word（Microsoft Word 保存） | 2 | 有标题、正文段落、一张表格；其中一个含中英文混排 |
| Word（WPS 保存） | 1 | 这台机器装了 WPS 才做，没有就写“未测试” |
| Excel | 2 | 至少一个有多个工作表、合并单元格、公式（公式的计算结果要已保存） |
| 有文本层的 PDF | 2 | 一份中文、一份双栏排版（例如公开的论文） |
| 扫描 PDF | 1 | 打印一页公开文字再扫描或拍照转 PDF，没有文本层 |
| 手机照片 | 2 | 拍公开海报、书的版权页之类；至少一张是竖着拍的（带 EXIF 方向） |
| 截图 | 1 | 一张带中文文字的系统截图（不要有个人信息） |

**步骤：** 在 `docmgr_w6` 下用前端或接口上传全部样本，等处理完。对每个文件导出 `GET /api/documents/<id>`、`GET /api/documents/<id>/text`、`GET /api/documents/<id>/tasks` 三个 JSON，存到 `output/windows-w6/real-files/<name>/`。**原文件也交回**（打进 W6 的另交压缩包，第 14.1 节），Claude 要在 Mac 上用同一个解析器重新解析对照。

**人工抄录（用来算 OCR 字符错误率 CER）：** 从扫描 PDF、两张手机照片、截图里各选一段（每段 50–200 字），Barry 照着原图逐字抄录，存成 `output/windows-w6/real-files/<name>/ground-truth.txt`（UTF-8，第一行写这段文字在原图里的位置，例如“第 1 页第 2 段”，第二行起是正文）。不要照着 OCR 结果改，抄错了宁可留着。

**预期（Claude 核对，见第 14.2 节）：** Word 的定位都是 `docx_para`，没有页码；Excel 是 `xlsx_range`，工作表名正确，公式单元格给出的是计算结果；PDF 的 `pdf_page` 页码在 1 到总页数之间；扫描页有 `source_type=ocr` 的片段；竖拍的照片 OCR 结果是正向的文字。

### 12.10 预览页在真实后端上：按页穿插 OCR、抽取文本标签页、高亮

对应 `docs/untested.md` 第 4 节 T24e、T24f 的“真实后端上没有看过”和“smartcn 下的高亮效果”。用第 12.9 节上传的扫描 PDF（或一份既有文本页又有扫描页的 PDF）和手机照片，在 `npm run dev` 的前端上：

1. 打开 PDF 的预览页，切到“抽取文本”标签页：同一页里正文在前、OCR 片段在后，页码从小到大。截图存成 `output/windows-w6/preview/pdf-extracted.png`，同时导出 `/text` 的 JSON 对照。
2. 用照片里 OCR 出来的一个词检索，从结果点进预览页：默认显示“抽取文本”标签页并滚到命中片段，地址栏有 `view=`。截图。
3. 检索三个中文词（各取样本里出现过的），看结果卡片里的摘要：命中词有高亮，摘要落在命中词附近。截图，并导出这三次 `POST /api/search` 的应答 JSON。

### 12.11 补交 W1–W3 的原始数据

第一轮只交了 JUnit XML 和实验结果目录，下面这些数字只在报告里有、没有原始数据，Claude 无法核对。**在第 12.4 节改动 `docmgr_docvqa` 之前先导出**，放到 `output/windows-w3-supplement/`：

| 文件 | 怎么得到 | 用来核对 |
|---|---|---|
| `sql/w3-1.csv` … `sql/w3-8.csv` | 第 12.5 节的 8 条查询，改在 `docmgr_docvqa` 上执行 | parse/ocr/embed 各 500 succeeded；第 4、6、7 条 0 行；片段数 |
| `w3-indices.txt`、`w3-chunks-count.txt` | 同第 12.5 节，前缀换成 `docvqa_` | 索引计数 = 数据库计数（报告写的 ocr 1589） |
| `w3-consistency.json` | `consistency check --json` | 报告写的“没有发现不一致” |
| `w3-ocr-params.csv` | `SELECT model_name, model_version, params::text, count(*) FROM ocr_results GROUP BY 1, 2, 3;` | 只有一种模型和一种参数（T24c、T24g） |
| `w3-ocr-failures.txt` | `mjbw0217.jpg`、`mkvw0217.jpg` 两个 OCR 任务的 id、三次失败的 `error` 原文、OCR Worker 日志里对应的几十行、手动重试的时间和方法 | 第 0.1 节记下的 `0xC0000005` |
| `w3-logs.zip`（另交） | W3 期间四个 OCR Worker、通用 Worker、CLIP 服务的日志（第一轮放在 `storage-smoke/w3-logs/`），去掉连接串 | 报告里 OCR 平均 53.57 秒、P95 131 秒的来源 |
| `w3-memory.csv`（如果第一轮的采样原始数据还在） | 原始采样 | 报告里的峰值内存；不在了就写“没有保留” |
| `document_map.csv` | `experiments/docvqa/datasets/document_map.csv`（它被 `.gitignore` 忽略，复制一份进来） | 结果里的 `document_id` 与 `file_id` 对应 |

### 12.12 验收标准

- [ ] 12.2：在第 0.2 节的提交上重跑；除 8 项符号链接外 0 failed；4 份 JUnit XML、2 份 collect 清单、前端与 ruff 输出、烟测输出都在
- [ ] 12.3：Barry 本人的终端；`symlink-priv.txt` 有那一行；backend 6 passed、shared 2 passed
- [ ] 12.4：10 步都有输出和退出码；第 4–6 步的问题都被报出；第 9 步计数与修复前相同；第 10 步 B2、B3 退出码 0
- [ ] 12.5：四个进程的 PID 和被结束的任务 id 都记了；8 个 CSV 与索引计数都导出；第 4、6、7 条为 0 行；一致性检查退出码 0
- [ ] 12.6–12.8：现象与预期一致，或如实写出不同；JSON 和输出原文都交回
- [ ] 12.9：样本数量达到表里的要求（做不到的写明）；三个 JSON、原文件、`sources.csv`、4 段人工抄录都交回
- [ ] 12.10：三组截图和对应的 JSON
- [ ] 12.11：表里的文件都交回；不在了的写明
- [ ] 全程没有改代码和配置文件；没有碰主库和 `docmgr_test` 之外的测试数据

------------------------------------------------------------------------

## 13. W7：跨机器 CLIP 向量一致性、同时运行的内存、负载下的查询编码（2026-11-21 19:40 添加）

### 13.1 跨机器的 CLIP 向量一致性

**为什么：** `docs/untested.md` 第 4 节 T20“跨机器的向量一致性”：同一输入的向量只在同一进程里比较过。实验如果在一台机器上建向量、在另一台机器上编码查询，或者两台机器的结果要放在一起比较，就需要知道两边算出来的向量是否一致。

**输入（两台机器上都有，都在 Git 里）：**

- 文本 10 条：`会议室里的白板照片`、`一只猫`、`红色的汽车`、`手写的数学公式`、`表格截图`、`扫描的合同第一页`、`夜晚的城市街道`、`a cat`、`a scanned document`、`中文文字的截图`
- 图片 6 张：`docs/screenshots/windows-2026-11-19/` 下的 5 张 PNG，`change-deepseek-v4/test-results/ocr-e2e/20261116-143732/ocr-smoke.png`

**做法：** 启动 CLIP 服务（默认设置，CPU），在仓库根目录：

```powershell
$texts = @('会议室里的白板照片','一只猫','红色的汽车','手写的数学公式','表格截图','扫描的合同第一页','夜晚的城市街道','a cat','a scanned document','中文文字的截图')
$body = @{ texts = $texts } | ConvertTo-Json -Compress
$t = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8001/encode/text" -ContentType "application/json; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($body))
$imgs = @(Get-ChildItem docs\screenshots\windows-2026-11-19\*.png) + @(Get-Item change-deepseek-v4\test-results\ocr-e2e\20261116-143732\ocr-smoke.png)
$iv = foreach ($f in $imgs) { $r = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8001/encode/image" -ContentType "application/octet-stream" -InFile $f.FullName; [pscustomobject]@{ path = (Resolve-Path -Relative $f.FullName); sha256 = (Get-FileHash $f.FullName -Algorithm SHA256).Hash.ToLower(); vector = $r.vector } }
$h = Invoke-RestMethod -Uri "http://127.0.0.1:8001/health"
[pscustomobject]@{ health = $h; model_version = $t.model_version; texts = $texts; text_vectors = $t.vectors; images = $iv } | ConvertTo-Json -Depth 6 -Compress | Out-File -Encoding utf8 output\windows-w7\clip-vectors.json
```

再记下 clip 环境的版本：`env_check\.venv-clip\Scripts\python -c "import torch, cn_clip, platform; print(torch.__version__, cn_clip.__version__, platform.platform())"`，存成 `clip-env.txt`。

**判定（Claude 在 Mac 上用同样的输入、同样的权重编码后比对，第 14.2 节）：** 每条文本、每张图片两边向量的余弦相似度都 ≥ 0.999；10 条文本对 6 张图片的相似度排序两边完全相同。不要求逐位相同（x86 与 arm64 的浮点运算顺序不同）。达不到时不算执行失败，是一条要写进论文“局限”的发现。

### 13.2 同时运行时的内存（OS-6）

**为什么：** `docs/untested.md` 第 6 节 OS-6、第 7.2 节：PostgreSQL、OpenSearch、后端、通用 Worker、OCR Worker、CLIP 服务同时运行时的总内存一直没有原始数据；第一轮只给了四个 Python 进程的峰值，没有数据库和 OpenSearch，也没有采样原始数据。论文“实验环境”一节要用。

**负载：** 在 `docmgr_w6` 上 `reocr --yes`（`--root` 为第 12.5 节的 docvqa60 目录），启动后端、一个通用 Worker、**一个** OCR Worker（默认设置）、CLIP 服务；同时跑第 13.3 节的检索循环。

**采样（每 5 秒一次，至少 15 分钟，或到 OCR 任务全部完成）：** 新开一个 PowerShell 窗口：

```powershell
$out = "output\windows-w7\memory.csv"
"time,group,pid,working_set_mb,private_mb" | Out-File -Encoding utf8 $out
$end = (Get-Date).AddMinutes(15)
while ((Get-Date) -lt $end) {
  $now = (Get-Date).ToString("o")
  Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('postgres.exe','java.exe','python.exe','node.exe') } | ForEach-Object {
    $c = "$($_.CommandLine)"
    $g = if ($_.Name -eq 'postgres.exe') {'postgresql'} elseif ($_.Name -eq 'java.exe') {'opensearch'} elseif ($_.Name -eq 'node.exe') {'node'} elseif ($c -match 'uvicorn') {'api'} elseif ($c -match 'ocr_worker') {'ocr_worker'} elseif ($c -match 'clip_service') {'clip_service'} elseif ($c -match 'app.worker') {'worker'} else {'python_other'}
    $p = Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue
    if ($p) { "$now,$g,$($_.ProcessId),{0:F1},{1:F1}" -f ($p.WorkingSet64/1MB), ($p.PrivateMemorySize64/1MB) | Out-File -Append -Encoding utf8 $out }
  }
  $avail = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1KB
  "$now,system_available,0,{0:F1},0" -f $avail | Out-File -Append -Encoding utf8 $out
  Start-Sleep -Seconds 5
}
```

（用 `F1` 而不是 `N1`：`N1` 会输出 `1,234.5` 这样带千位逗号的数字，破坏 CSV。可用内存用 CIM 取，不用 `Get-Counter`：中文版 Windows 的性能计数器名称是中文的，英文路径会报错。）OCR 识别子进程是 `python.exe`，命令行里也有 `ocr_worker`，会被归到 `ocr_worker` 组，这是想要的。报告里写明机器总内存、采样开始和结束时间、负载期间 OCR 完成了多少个任务。

### 13.3 OCR 负载下的查询编码耗时

**为什么：** D36 的局限：CLIP 服务一次只算一个请求，embed 和查询编码会排队，3 秒超时会不会经常触发没有量过（`docs/untested.md` 第 4 节 T22“3 秒查询超时是否合适”）。`reocr` 不产生 embed 任务，所以这里量的是“OCR 占满 CPU 时”的查询编码。

与第 13.2 节同时进行，在另一个窗口（先按第 12.6 节第 3 步的写法拿 `$tok`）：

```powershell
$qs = (Get-Content <docvqa60 目录>\queries.tsv -Encoding utf8 | Select-Object -Skip 1) | ForEach-Object { ($_ -split "`t")[2] }
$out = "output\windows-w7\search-under-load.csv"
"time,i,took_ms,image_status,image_took_ms,hits" | Out-File -Encoding utf8 $out
for ($i = 0; $i -lt 200; $i++) {
  $q = $qs[$i % $qs.Count]
  $b = @{ query = $q; channels = @{ meta = $true; text = $true; image = $true } } | ConvertTo-Json -Compress
  $r = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/search" -Headers @{ Authorization = "Bearer $tok" } -ContentType "application/json; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($b))
  $img = $r.channels | Where-Object { $_.channel -eq 'image' }
  "$((Get-Date).ToString('o')),$i,$($r.took_ms),$($img.status),$($img.took_ms),$($r.hits.Count)" | Out-File -Append -Encoding utf8 $out
  Start-Sleep -Milliseconds 500
}
```

（如果应答里 `channels` 的字段名与上面不同，按 `docs/api.md` §7.1 的实际结构改，并在报告里写明改了什么；同时把第一条应答原样存成 `search-sample.json`。）OCR 任务做完后，不开 OCR Worker 再跑一遍同样的循环，存成 `search-idle.csv`，作为对照。

### 13.4 不做的

不改 `SEARCH_IMAGE_TIMEOUT_SECONDS`、不调 CLIP 设备、不开 MPS/CUDA；这一节只量现状。正式的性能实验是 T27。

### 13.5 验收标准

- [ ] 13.1：`clip-vectors.json` 有 10 条文本、6 张图片的向量和 `health` 信息；`clip-env.txt` 有版本
- [ ] 13.2：`memory.csv` 覆盖至少 15 分钟，相邻两次采样的间隔不超过 15 秒；六组进程（postgresql、opensearch、api、worker、ocr_worker、clip_service）都出现过；报告写了总内存和负载情况
- [ ] 13.3：`search-under-load.csv`、`search-idle.csv` 各 200 行，`search-sample.json` 在
- [ ] 没有改任何代码和配置文件

------------------------------------------------------------------------

## 14. 交回的原始数据与 Claude 的核对方法（2026-11-21 19:40 添加）

### 14.1 交回什么、怎么交

每个任务一个目录：`output/windows-w4/`、`output/windows-w5/`、`output/windows-w6/`、`output/windows-w7/`、`output/windows-w8/`（2026-11-21 21:20 添加；里面的 `missed/missed270.tsv`、`missed/missed30.tsv` 是 Claude 预先放好的输入，不要改）、`output/windows-w9/`（2026-11-23 添加）、`output/windows-w3-supplement/`。每个目录里都要有：

- `git-head.txt`：`git rev-parse HEAD` 和 `git status --porcelain` 的输出（第 2 节第 11 条）
- `commands.txt`：按执行顺序列出实际运行的命令（去掉密码、令牌、连接串）和每条的退出码
- `SHA256SUMS.txt`：目录里每个文件以及对应的另交压缩包的 SHA-256（`Get-FileHash -Algorithm SHA256`，一行一个：`<小写 hash>  <相对路径>`）
- 各节要求的原始文件

单个文件超过 5 MB 的（日志、原文件、截图过多时）不进 Git，打进 `<任务>-extra.zip` 另交给 Barry，hash 写进 `SHA256SUMS.txt`。Barry 推送 GitHub、把压缩包放到 Mac 的 `~/Desktop/windows-results/` 后告诉 Claude。

### 14.2 Claude 收到后怎么核对

Claude 在 Mac 上做，不装新东西；Mac 上没有 PostgreSQL 和 OpenSearch，所以只核对原始数据，不重做需要数据库的步骤。核对结果写进 `docs/changes/windows-<收到日期>-核对.md`，按结论更新 `docs/untested.md` 和 DEVPLAN。

| 对象 | Claude 的核对方法 | 判为通过的条件 |
|---|---|---|
| 所有目录 | 重算 `SHA256SUMS.txt`；读 `git-head.txt` | hash 全部一致；提交号是第 0.2 节的那个，`git status` 为空 |
| JUnit XML（W1、12.2、12.3） | 解析 XML，统计 tests/failures/errors/skipped，列出失败和跳过的用例名；与 Mac 上同一提交的 `pytest --collect-only -q` 清单逐条对比（W1 对比 `8fb5830`，12.2 对比第 0.2 节的提交） | 失败只有已知原因的项；Windows 收集到的用例 = Mac 收集到的用例（差异逐条解释）；跳过的都有原因 |
| W2 数据 | 在 Mac 上运行 `experiments validate`（只读文件，不需要数据库）；在 Mac 上跑 `scripts/datasets/tests/`；检查编号规则、500 条、`file_id` 与图片名对应 | 退出码 0；测试通过；统计与报告一致 |
| W3 结果目录（`docvqa-runs.zip`） | 用 `backend/app/modules/experiments/metrics.py` 从 `results.jsonl` 和 qrels 重算每条查询的 P@10、R@10、nDCG@10，与 `metrics.json` 比对；比较 3 次重复的排名是否完全相同；检查 `config.json` 里的 `git_commit`、`git_dirty`、`clip_model`（权重 hash 前 12 位 `5997ef32c50d`）、三个 mapping 的 sha256（与 Mac 上同一提交的文件比对）、`ocr_params`、`complete`；比较 `reocr` 前后两次 B2 的逐条排名 | 重算的指标与 `metrics.json` 相同（浮点误差 1e-9 以内）；重复间排名相同；配置字段齐全、hash 一致；两次 B2 排名逐条相同 |
| W3 补交数据（12.11） | 读 SQL CSV 与索引计数，交叉比对：任务全部 succeeded；片段数（数据库）= 索引计数；重复检查为 0 行；OCR 模型与参数只有一种；从日志里重算 OCR 每任务平均耗时和 P95 | 与报告里的数字一致；不一致的逐条列给 Barry |
| 12.4 一致性修复 | 读每一步的 `--json` 输出和退出码；比对第 10 步的 `results.jsonl` 与 W3 同配置的排名 | 每一步的退出码与问题类别符合预期；修复后计数不变；B2、B3 排名与 W3 逐条相同 |
| 12.5 崩溃与并发 | 读 8 个 CSV：被强制结束时持有的任务 `attempts=2` 且最终 succeeded；四个领取者都出现；第 4、6、7 条 0 行；每个文档的片段数加总 = 索引计数 | 全部满足 |
| 12.6–12.8 | 读 JSON 和输出原文，与预期逐条对照 | 符合预期；不符合的列给 Barry |
| 12.9 真实文件 | 在 Mac 上用同一提交的解析器（`backend/app/modules/parsing/`，纯函数，不需要数据库）重新解析交回的原文件，与 Windows 的 `/text` JSON 比较正文片段和定位；用人工抄录算 OCR 的 CER（编辑距离 / 抄录字数，去掉空白后计算） | 非 OCR 片段的文本和定位两边相同；定位类型符合第 12.9 节的预期；CER 如实记录（不设通过线，作为论文数据） |
| 13.1 CLIP 向量 | 在 Mac 上用同样的权重、同样的输入编码，计算两边每个向量的余弦相似度和 10×6 的排序 | 余弦相似度都 ≥ 0.999 且排序相同；否则记为发现 |
| 13.2 内存 | 按组、按采样时刻加总内存，算每组峰值、总峰值和最低可用内存；检查采样间隔 | 间隔不超过 15 秒、六组都在；数字作为论文“实验环境”的数据 |
| 13.3 负载下检索 | 从两份 CSV 算总耗时与图像通道耗时的 P50/P95、图像通道 `unavailable` 的比例 | 数据完整（各 200 行）；结论作为 T27 与 D36 局限的依据 |
| W4、W5 | 对照报告逐项看截图、命令输出、退出码 | 每个核对点都有结果和证据 |
| W8 第 16.3 节（2026-11-21 21:20 添加） | 把事件的时刻和 OCR Worker 日志里的 8 次失败逐一对应，提取出错模块和异常代码 | 时刻能对上（或者写明日志已被覆盖）；按第 16.3 节的规则归类 |
| W8 第 16.4、16.5 节 | 从 CSV 统计每轮、每组的崩溃次数、耗时 P50/P95、吞吐量；把崩溃时刻对到 `memory.csv`，看崩溃前 10 秒的可用内存和 CPU；重算 `SHA256SUMS.txt` | 行数齐全、时刻对得上；结论按第 16.4 节的三种情况归类，第 16.5 节的数字进 T27 |
| W8 第 16.6 节 | 逐行看分词结果，判断有没有转小写、词干化、去停用词 | 17 行齐全；结论写进论文“局限”一节 |
| W8 第 16.7 节 | 对 270 条漏检按第 16.7 节分三类；30 条人工答案与 OCR 文本比对，算字符级的编辑距离比例 | 文件齐全；`ocr-chunks.csv` 的行数与 1589 一致，或者已说明差异 |
| W8 第 16.8 节 | 逐个对照任务 JSON 里的 `status`、`attempts`、`error`；从 `memory.csv` 取 `worker` 组的峰值 | 与第 16.8 节的预期逐条一致，才判为通过 |
| W9（2026-11-23 添加） | 各小节末尾的“Claude 怎么判断”；17.3 读 `timeouts.json` 和输出原文；17.4 逐条比较 8 个结果目录的排名，换位处算分数相对差，核对 `config.json` 的 mapping hash 与 `git_dirty`；17.5 读日志、退出码、任务 CSV；17.6、17.7、17.18 对照截图与网络记录；17.9 解析 JUnit | 第 17.12 节的条件 |

核对中发现的代码问题，Claude 不自己修，先报给 Barry（与第 2 节第 5 条相同）。

------------------------------------------------------------------------

## 15. 不交给 Windows 的项目（2026-11-21 19:40 添加）

下面这些还没完成，但不放进本任务书，原因各不相同。Barry 改变决定时再加新任务。

| 项目 | 为什么不交给 Windows | 由谁、什么时候 |
|---|---|---|
| T25 评测数据集与标注（文字型、视觉型、混合型查询，200–500 个文件） | 附录 A18 要求分层查询集，视觉型查询要专门收集图片；相关性标注是论文的评测依据，应由 Barry 本人完成，不能由 AI 代标。DocVQA 只是流程验证 | Barry；越早越好，T26–T28 都依赖它 |
| T26–T28 正式实验与分析 | 依赖 T25；正式实验的机器（Mac 还是 Windows）要先定下来并固定，写进论文“实验环境” | T25 之后由 Barry 决定在哪台机器上跑 |
| `deploy/docker-compose.yml`、`deploy/opensearch/Dockerfile`（OS-7） | 要装 Docker，第 2 节第 2 条禁止；Barry 决定 Mac 上不用 Docker | Barry 批准在 Windows 装 Docker 后再加任务（T30 部署说明需要） |
| Linux 上 `RLIMIT_AS` 内存上限 | 这台机器没有 Linux，装 WSL 是新安装 | 需要 Barry 批准；不做就写进论文局限 |
| IK 分词（OS-2） | 没有与 OpenSearch 2.19.1 匹配的 IK 版本 | 不做，写进论文 |
| 前端页面组件的自动化测试 | 要装组件测试工具 | 需要 Barry 批准 |
| `CLIP_DEVICE=mps`、`cuda` | Windows 没有 MPS；这台机器的 GPU 与 CUDA 环境没有确认，装 CUDA 版 torch 是新安装 | MPS 可以在 Mac 上由 Claude 做（Barry 同意后） |
| Safari | W4 第 10.4 节已写成“有设备就看” | 同 W4 |
| T29–T32 测试报告、部署说明、一致性核对、答辩脚本 | 是文档工作，依赖 W4–W7 的核对结果 | Claude 与 Barry |

------------------------------------------------------------------------

## 16. W8：针对第一轮日志的补充测试（2026-11-21 21:20 添加）

来源：Claude 读了第一轮补充上传的文件（`output/windows-w3/`、`windows-w3-test-evidence.zip` 里的日志、`docvqa-runs.zip` 的逐条结果），发现几处 W4–W7 都没覆盖的问题，核对记录在 `docs/changes/windows-2026-11-21-补充核对.md`。W8 就是为这些问题补的测试。

规则与 W6 相同：只测量和核对，**不改代码和配置文件**，环境变量只在窗口里临时设，而且只设本节写明的；**不调参**，第 16.5 节比较 Worker 数只是测量，结果不拿来改默认配置，要改先问 Barry；结果与预期不符时，记下现象、复现步骤、完整输出，问 Barry。原始数据按第 14.1 节放进 `output/windows-w8/`，报告写进 `windows任务报告.txt` 末尾新加的 W8 一节。

### 16.1 第一轮发现了什么

| # | 发现 | 依据 | 对应小节 |
|---|---|---|---|
| 1 | 8 次 `0xC0000005` 全部发生在 14:31:08–14:31:59 这 51 秒内，4 个 OCR Worker 都碰到了。涉及 4 个文档，不是报告里写的 2 个：manifest 里相邻的 `dv_mjbw0217`、`dv_mjxn0226`、`dv_mkhg0227`、`dv_mkvw0217`（数据行第 238–241 行）。其中 `mjbw0217`、`mkvw0217` 3 次都失败，另外两个第二次就成功了。之后 reocr 同样开 4 个 Worker、同样这 500 张图，一次都没崩 | `ocr*.err.log`、`reocr-ocr*.err.log` | 16.3、16.4 |
| 2 | 任务失败后立即回到 `pending`。领取按 `created_at` 排序，失败的任务马上又被领走，3 次尝试大约 40 秒就用完了，一次短暂的故障就足以让任务永久失败 | 日志时间；`shared/tasks.py` | 16.4 只记录现象，不改代码（改要动表结构，属 🔒） |
| 3 | 内存只记了 4 个 Python 进程组的峰值，没有时间线，也没有系统可用内存，判断不了 14:31 是不是内存不足 | `memory-peaks.json`、`monitor_w3_memory.ps1` | 16.4、16.5 |
| 4 | Windows 上 Worker 的子进程没有内存上限：通用 Worker 日志里“当前系统不支持设置内存上限”出现了 1000 次（D16）。防 zip 炸弹、防超大图片只能靠解析前的检查 | `worker.err.log` | 16.8 |
| 5 | B2 只有 230/500 条查询的相关文档进了前 20 名。漏掉的 270 条里，很多是“What is the title of the document?”这类没有内容词的问题 | `docvqa-runs.zip` | 16.7 |
| 6 | smartcn 怎么切英文、数字、标点，从来没有实测过，而 DocVQA 的查询和 OCR 文本都是英文 | — | 16.6 |

### 16.2 环境

| 用途 | 数据库 | 存储 | 索引前缀 | 用在 |
|---|---|---|---|---|
| W3 的数据（只读） | `docmgr_docvqa`（已有） | W3 的 `storage/w3-docvqa` | `docvqa_` | 16.6、16.7 |
| 崩溃复现 | `docmgr_w8a`（新建，`alembic upgrade head`） | 新的空目录 | `w8a_` | 16.4 |
| Worker 数与吞吐、畸形文件 | `docmgr_w8b`（新建，`alembic upgrade head`） | 新的空目录 | `w8b_` | 16.5、16.8 |

切换方法同第 6.1 节。每执行一条会写数据的命令之前，先 `echo $env:DATABASE_URL $env:OPENSEARCH_INDEX_PREFIX $env:STORAGE_ROOT` 确认（输出里的密码不要抄进报告）。数据库密码用 `$env:PGPASSWORD` 在窗口里设，不写进任何文件。

**公用的准备**（仓库根目录，每个新开的 PowerShell 窗口执行一次；`<用户>` 换成数据库用户名）：

```powershell
$repo = (Get-Location).Path
$out  = "$repo\output\windows-w8"
New-Item -ItemType Directory -Force "$out\logs", "$out\crash4", "$out\scale", "$out\analyze", "$out\missed", "$out\bad-files" | Out-Null
function Q($db, $sql) { psql -h localhost -U <用户> -d $db -tAc $sql }
function Export($db, $sql, $file) { psql -h localhost -U <用户> -d $db -c "\copy ($sql) TO '$file' CSV HEADER" }
function Wait-Tasks($db, $types) {
  do { Start-Sleep -Seconds 5; $n = [int](Q $db "SELECT count(*) FROM processing_tasks WHERE task_type IN ($types) AND status IN ('pending', 'processing')") } while ($n -gt 0)
}
function Start-Ocr($name) {
  Start-Process -FilePath "$repo\env_check\.venv-ocr\Scripts\python.exe" -ArgumentList '-m', 'ocr_worker' -WorkingDirectory "$repo\services\ocr_worker" -RedirectStandardOutput "$out\logs\$name.out.log" -RedirectStandardError "$out\logs\$name.err.log" -NoNewWindow -PassThru
}
```

`Start-Ocr` 返回的进程对象要记下来（`$w1 = Start-Ocr 'crash4-single'`），停止时用 `Stop-Process -Id $w1.Id`。**只在队列已经清空、Worker 空闲时停止**（`Wait-Tasks` 返回之后），这样不会打断正在识别的任务。`Export` 的文件路径用相对仓库根目录的正斜杠路径，例如 `'output/windows-w8/crash4/single-r01.csv'`。

**内存与 CPU 采样脚本**（第 13.2 节脚本的变体：每 1 秒一次，多记一行 CPU 总占用，有停止文件时结束）。先把它存到仓库外：

```powershell
Set-Content -Encoding utf8 "<仓库外的目录>\sample_w8.ps1" -Value @'
param([string]$Out, [string]$Stop)
"time,group,pid,working_set_mb,private_mb" | Out-File -Encoding utf8 $Out
while (-not (Test-Path -LiteralPath $Stop)) {
  $now = (Get-Date).ToString("o")
  Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('postgres.exe','java.exe','python.exe','node.exe') } | ForEach-Object {
    $c = "$($_.CommandLine)"
    $g = if ($_.Name -eq 'postgres.exe') {'postgresql'} elseif ($_.Name -eq 'java.exe') {'opensearch'} elseif ($_.Name -eq 'node.exe') {'node'} elseif ($c -match 'uvicorn') {'api'} elseif ($c -match 'ocr_worker') {'ocr_worker'} elseif ($c -match 'clip_service') {'clip_service'} elseif ($c -match 'app.worker') {'worker'} else {'python_other'}
    $p = Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue
    if ($p) { "$now,$g,$($_.ProcessId),{0:F1},{1:F1}" -f ($p.WorkingSet64/1MB), ($p.PrivateMemorySize64/1MB) | Out-File -Append -Encoding utf8 $Out }
  }
  $avail = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1KB
  "$now,system_available,0,{0:F1},0" -f $avail | Out-File -Append -Encoding utf8 $Out
  $cpu = (Get-CimInstance Win32_PerfFormattedData_PerfOS_Processor -Filter "Name='_Total'").PercentProcessorTime
  "$now,cpu_total_percent,0,$cpu,0" | Out-File -Append -Encoding utf8 $Out
  Start-Sleep -Seconds 1
}
'@
```

在一个单独的窗口里运行：`powershell -NoProfile -ExecutionPolicy Bypass -File "<仓库外的目录>\sample_w8.ps1" -Out "$out\<小节目录>\memory.csv" -Stop "$out\<小节目录>\stop.flag"`。结束时 `New-Item "$out\<小节目录>\stop.flag"`，再把 `stop.flag` 删掉。用 CIM 类名而不用 `Get-Counter`，原因见第 13.2 节（中文版 Windows 的计数器名称是中文的）。报告里写明机器的逻辑处理器数和总内存：`(Get-CimInstance Win32_Processor).NumberOfLogicalProcessors`、`(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory`，存成 `$out\machine.txt`。

**小数据集的生成脚本**（第 12.5 节脚本的变体，多两个参数：从第几行开始、取几行，行号从 0 算）。脚本里只用单引号：Windows PowerShell 5.1 把参数传给 `python -c` 时会吞掉里面的双引号，所以写成文件再运行（第 12.5 节如果遇到 `SyntaxError`，也改用这个脚本，参数写 `0 60`）：

```powershell
Set-Content -Encoding utf8 "<仓库外的目录>\make_subset.py" -Value @'
import csv, shutil, sys
from pathlib import Path
src, dst, start, count = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
with open(src / 'datasets/manifest.csv', encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))[start:start + count]
ids = {r['file_id'] for r in rows}
(dst / 'datasets/files/docvqa').mkdir(parents=True)
(dst / 'qrels').mkdir()
with open(dst / 'datasets/manifest.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
for r in rows:
    shutil.copy2(src / 'datasets/files' / r['path'], dst / 'datasets/files' / r['path'])
qrels = (src / 'qrels/docvqa.tsv').read_text(encoding='utf-8').splitlines()
keep = [qrels[0]] + [line for line in qrels[1:] if line.split('\t')[1] in ids]
qids = {line.split('\t')[0] for line in keep[1:]}
(dst / 'qrels/docvqa.tsv').write_text('\n'.join(keep) + '\n', encoding='utf-8', newline='\n')
queries = (src / 'queries.tsv').read_text(encoding='utf-8').splitlines()
picked = [queries[0]] + [line for line in queries[1:] if line.split('\t')[0] in qids]
(dst / 'queries.tsv').write_text('\n'.join(picked) + '\n', encoding='utf-8', newline='\n')
print(len(rows), 'files,', len(qids), 'queries:', ' '.join(sorted(ids)))
'@
```

### 16.3 查 Windows 事件日志里的崩溃记录（最先做）

**为什么：** 发现 1。Windows 给每次程序崩溃都会记一条“应用程序错误”（事件 ID 1000），里面写着出错的是哪个模块（dll）。这是最快的定位办法，但应用程序日志满了会覆盖旧记录，所以**基线同步之后马上做**。

**步骤**（普通权限的 PowerShell 就能读应用程序日志）：

```powershell
Get-WinEvent -FilterHashtable @{LogName='Application'; Id=1000,1001; StartTime='2026-11-21 13:15'; EndTime='2026-11-21 15:30'} -ErrorAction SilentlyContinue | Where-Object { $_.Message -match 'python' } | Format-List TimeCreated, Id, ProviderName, Message | Out-File -Encoding utf8 "$out\crash-events.txt"
Get-WinEvent -ListLog Application | Format-List LogName, FileSize, MaximumSizeInBytes, RecordCount, LogMode | Out-File -Encoding utf8 "$out\application-log-info.txt"
(Get-WinEvent -LogName Application -MaxEvents 1 -Oldest).TimeCreated.ToString('o') | Out-File -Append -Encoding utf8 "$out\application-log-info.txt"
Get-ChildItem "C:\ProgramData\Microsoft\Windows\WER\ReportArchive", "$env:LOCALAPPDATA\Microsoft\Windows\WER\ReportArchive" -Directory -Filter 'AppCrash_python*' -ErrorAction SilentlyContinue | Select-Object FullName, LastWriteTime | Format-Table -AutoSize | Out-File -Encoding utf8 "$out\wer-reports.txt"
```

时间范围 13:15–15:30 覆盖了 W3 处理的全过程（13:20–15:27），可以顺便看有没有日志里没记到的崩溃。`wer-reports.txt` 里列出的、时间在 11-21 14:31 前后的目录，把其中的 `Report.wer`（文本文件）复制到 `$out\wer\<目录名>.wer`。交回之前检查一遍内容：可以有用户名和路径，但不能有密码和令牌。

**预期：**
- `crash-events.txt` 里有 ID 1000 的事件，时间与下面 8 个时刻逐一对应（相差 2 秒以内）：14:31:08、14:31:09、14:31:32、14:31:33、14:31:48、14:31:49、14:31:51、14:31:59。每条都有“错误模块名称”和“异常代码 0xc0000005”。
- 如果一条都没有：看 `application-log-info.txt` 里最早一条事件的时间，晚于 11-21 14:31 就是被覆盖了，在报告里写“已被覆盖”。早于这个时间却仍然没有，就写“当时没有生成错误报告”。这两种情况都不算失败，接着做第 16.4 节。

**Claude 怎么判断**（核对时用，见第 14.2 节）：出错模块是 Paddle 自己的 dll（例如 `paddle_inference.dll`、`mkldnn.dll`、`libiomp5md.dll`），记为“多个识别进程同时运行时 Paddle 出错”，论文里写成局限，部署建议少开 Worker。是 `ntdll.dll`、`ucrtbase.dll` 一类，记为“堆内存被写坏或内存不足”，要看第 16.4 节当时的可用内存。

### 16.4 复现 OCR 崩溃（`docmgr_w8a`）

**为什么：** 发现 1–3。要分清两件事：崩溃是这 4 张图片本身引起的，还是“4 个识别进程同时运行”引起的。还要第一次拿到崩溃前后的内存时间线。

**准备：**
1. 生成 4 个文件的小数据集，预期打印 `4 files, 4 queries: dv_mjbw0217 dv_mjxn0226 dv_mkhg0227 dv_mkvw0217`：

   ```powershell
   $crash4 = "<仓库外的新目录>\docvqa-crash4"
   .\.venv-main\Scripts\python -I "<仓库外的目录>\make_subset.py" experiments\docvqa $crash4 237 4
   ```

2. 窗口变量指向 `docmgr_w8a`、`w8a_`、新的存储目录；在 `backend/` 下 `alembic upgrade head`，然后 `validate`、`import`（`--root $crash4`，同第 12.5 节）。
3. 启动 CLIP 服务和一个通用 Worker，等 parse 和 embed 全部完成：`Wait-Tasks 'docmgr_w8a' "'parse', 'embed'"`。然后在各自的窗口里按 Ctrl+C 停掉 CLIP 服务和通用 Worker，让后面的测量只有 OCR 在跑。此时 4 个 OCR 任务处于 `pending`，**还没有任何 OCR Worker 在运行**。
4. 在另一个窗口启动采样脚本，输出到 `$out\crash4\memory.csv`。

**A. 单个 OCR Worker，10 轮：**

```powershell
$w = Start-Ocr 'crash4-single'
for ($r = 1; $r -le 10; $r++) {
  if ($r -gt 1) { Push-Location backend; ..\.venv-main\Scripts\python -m app.modules.experiments --root $crash4 reocr --yes; Pop-Location }
  Wait-Tasks 'docmgr_w8a' "'ocr'"
  Export 'docmgr_w8a' "SELECT id, document_id, status, attempts, claimed_by, error, started_at, finished_at FROM processing_tasks WHERE task_type = 'ocr' ORDER BY document_id" ("output/windows-w8/crash4/single-r{0:D2}.csv" -f $r)
}
Stop-Process -Id $w.Id
```

**B. 4 个 OCR Worker 同时运行，10 轮：** 每轮 4 个任务分给 4 个 Worker 同时识别，也就是 14:31 时的情形。

```powershell
$ws = 1..4 | ForEach-Object { Start-Ocr "crash4-multi$_" }
Start-Sleep -Seconds 60   # 等 4 个 Worker 都加载完模型（看各自的 .err.log 里出现“OCR 模型已加载”）
for ($r = 1; $r -le 10; $r++) {
  Push-Location backend; ..\.venv-main\Scripts\python -m app.modules.experiments --root $crash4 reocr --yes; Pop-Location
  Wait-Tasks 'docmgr_w8a' "'ocr'"
  Export 'docmgr_w8a' "SELECT id, document_id, status, attempts, claimed_by, error, started_at, finished_at FROM processing_tasks WHERE task_type = 'ocr' ORDER BY document_id" ("output/windows-w8/crash4/multi4-r{0:D2}.csv" -f $r)
}
$ws | ForEach-Object { Stop-Process -Id $_.Id }
```

如果某一轮有任务最终 `failed`，`reocr` 照样会把它放回队列，下一轮继续，不用手动重试。全部结束后停掉采样（`New-Item "$out\crash4\stop.flag"`），再把 `$out\logs\crash4-*.err.log` 留着交回。

**预期：**
- 20 个 CSV，每个 4 行。A 的 10 轮都应为 `succeeded`、`attempts = 1`。如果 A 也崩了，说明和图片有关，在报告里写明是哪一张、第几轮。
- B 可能崩，也可能不崩，两种都如实记录。崩溃时 `error` 写着“识别子进程异常退出（退出码 3221225477）”，`attempts` 大于 1。
- 有崩溃的话，按第 16.3 节的命令把这次测试时段的事件日志也导出来，存成 `$out\crash4\crash-events.txt`。
- `memory.csv` 覆盖 A、B 的全过程，相邻两次采样间隔不超过 3 秒，`ocr_worker`、`system_available`、`cpu_total_percent` 三组都有。

**Claude 怎么判断：** 统计 A、B 各自的崩溃次数和崩溃的任务；把每次崩溃的时刻（日志里的“失败”行，以及 CSV 里 `attempts > 1` 的任务）对到 `memory.csv`，看崩溃前 10 秒内 `system_available` 的最低值和 `ocr_worker` 的合计。三种结论：
- A 不崩、B 崩，崩时可用内存接近 0：内存不足；
- A 不崩、B 崩，崩时可用内存充足：多个识别进程同时运行时 Paddle 出错（结合第 16.3 节的模块名）；
- A、B 都不崩：第一轮的崩溃复现不了，记为“与当时的机器状态有关，原因不明”。
同时记下 B 里每个崩溃任务前后几次尝试的间隔秒数，作为发现 2 的实测数据（不改代码）。

### 16.5 开几个 OCR Worker 合适（`docmgr_w8b`）

**为什么：** 发现 3。第一轮开 4 个 Worker 时，每张图平均 53.57 秒（第 0.1 节）。每个识别进程都会尽量占满 CPU，几个进程可能在互相抢。T27 的性能实验和论文的部署建议，都需要知道 1、2、4 个 Worker 的吞吐量、每张耗时和内存。

**准备：**
1. 生成 40 个文件的小数据集：manifest 数据行第 221–260 行（从 `dv_lxkp0227` 到 `dv_mzbx0227`），包含第 16.4 节的 4 个文件。预期打印 `40 files, 40 queries: ...`：

   ```powershell
   $scale = "<仓库外的新目录>\docvqa-scale40"
   .\.venv-main\Scripts\python -I "<仓库外的目录>\make_subset.py" experiments\docvqa $scale 220 40
   ```

2. 窗口变量指向 `docmgr_w8b`、`w8b_`、新的存储目录；`alembic upgrade head`、`validate`、`import`（`--root $scale`）。和第 16.4 节一样，用 CLIP 服务和一个通用 Worker 做完 parse、embed，然后停掉它们。
3. 启动采样脚本，输出到 `$out\scale\memory.csv`。

**步骤：** 按 N = 1、2、4、1 的顺序做 4 组。最后再做一次 N = 1，是为了看机器状态有没有随时间变化。第一组直接处理 import 产生的 OCR 任务，后面每组先 `reocr --yes`：

```powershell
$plan = 1, 2, 4, 1
for ($i = 0; $i -lt $plan.Count; $i++) {
  $n = $plan[$i]
  $ws = 1..$n | ForEach-Object { Start-Ocr ("scale-g{0}-w{1}" -f ($i + 1), $_) }
  Start-Sleep -Seconds 60   # 等模型加载完，再放任务
  if ($i -gt 0) { Push-Location backend; ..\.venv-main\Scripts\python -m app.modules.experiments --root $scale reocr --yes; Pop-Location }
  Wait-Tasks 'docmgr_w8b' "'ocr'"
  Export 'docmgr_w8b' "SELECT id, document_id, status, attempts, claimed_by, error, started_at, finished_at FROM processing_tasks WHERE task_type = 'ocr' ORDER BY started_at" ("output/windows-w8/scale/g{0}-n{1}.csv" -f ($i + 1), $n)
  $ws | ForEach-Object { Stop-Process -Id $_.Id }
}
```

注意：第一组的 OCR 任务在 import 时就已经是 `pending`，Worker 一启动就会领，所以第一组的耗时里含模型加载。报告里写明，Claude 会用 `started_at` 扣掉这一段。全部做完后停止采样，并在报告里写明每组开始和结束的时刻。

**预期：** 4 个 CSV，每个 40 行，最终全部 `succeeded`。有失败或 `attempts > 1` 的，如实列出来，不要重试到成功再交。

**Claude 怎么判断：** 每组算：总耗时（最晚 `finished_at` 减最早 `started_at`）、吞吐量（张/分钟）、每张耗时（`finished_at − started_at`）的 P50 和 P95、崩溃次数；再从 `memory.csv` 按时段算 OCR 组内存峰值、最低可用内存、CPU 平均占用。结果作为 T27 的输入和论文“部署建议”的依据。**不设通过线**，数据完整就算完成。如果吞吐量在 N = 2 或 4 时没有比 N = 1 明显提高，就说明多开 Worker 主要是在抢 CPU，报告里照实写。

### 16.6 smartcn 怎么切英文（`docvqa_` 索引，只读）

**为什么：** 发现 6。论文要说明 BM25 在英文查询上的局限，需要知道 smartcn 对英文有没有转小写、有没有词干化、去不去停用词、怎么处理数字和标点。

**步骤：** OpenSearch 在运行即可，不需要 Worker。

```powershell
$texts = @(Get-Content experiments\docvqa\queries.tsv -Encoding utf8 | Select-Object -Skip 1 -First 10 | ForEach-Object { ($_ -split "`t")[2] })
$texts += 'Names NAMED naming', 'U.S.A. e-mail 2026-11-21 $1,234.50 No.5', 'What is the title of the document?', '智能文档管理系统 Document Management'
$s = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:9200/docvqa_chunks/_search' -ContentType 'application/json' -Body '{"size":3,"query":{"term":{"source_type":"ocr"}},"sort":[{"chunk_id":"asc"}],"_source":["chunk_id","text"]}'
$texts += @($s.hits.hits | ForEach-Object { $_._source.text })
$texts | ForEach-Object {
  $b = @{ analyzer = 'docmgr_text'; text = $_ } | ConvertTo-Json -Compress
  $r = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:9200/docvqa_chunks/_analyze' -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($b))
  @{ text = $_; tokens = @($r.tokens | ForEach-Object { $_.token }) } | ConvertTo-Json -Compress
} | Out-File -Encoding utf8 "$out\analyze\analyze.jsonl"
```

**预期：** `analyze.jsonl` 有 17 行（10 条查询 + 4 句测试文字 + 3 段 OCR 文本），每行都有 `tokens`。

**Claude 怎么判断：** 逐行看：`Names`、`NAMED` 是否变成小写；`names`、`named`、`naming` 有没有归到同一个词干；`what`、`is`、`the` 有没有被去掉；`U.S.A.`、`e-mail`、日期、金额被切成什么。结论写进论文“局限”一节和 T27 的分析，**不设通过线**，数据完整就算完成。

### 16.7 B2 为什么漏检（导出在 `docmgr_docvqa` 上只读；人工核对由 Barry 做）

**为什么：** 发现 5。270 条漏检，要分清三种原因：查询本身没有内容词（例如“What is the title of the document?”）、OCR 没认出答案所在的那些字、文字认出来了但排名不够靠前。前两种在论文里的写法完全不同。

**A. 导出 OCR 文本（GPT 做，与第 12.11 节同时进行）：**

```powershell
Export 'docmgr_docvqa' "SELECT document_id, seq, text FROM document_chunks WHERE source_type = 'ocr' ORDER BY document_id, seq" 'output/windows-w8/missed/ocr-chunks.csv'
Copy-Item experiments\docvqa\datasets\document_map.csv "$out\missed\document_map.csv"
```

预期：`ocr-chunks.csv` 有 1589 行数据（不算表头），与第一轮报告的数一致；不一致就照实写。

**B. 人工核对 30 条（Barry 做，约 40 分钟）：** Claude 已从 B2 的结果里挑出漏检的 270 条，放在 `output/windows-w8/missed/missed270.tsv`；按 `query_id` 顺序取前 30 条，放在 `output/windows-w8/missed/missed30.tsv`。对每一行：
1. 打开 `image` 列给出的图片（图片在 W2 下载的目录里，不进 Git）；
2. 找到能回答 `query` 的地方，把图上的原文照抄到 `answer_in_image` 列里，大小写、标点都照抄，最多 50 个字符；图上有多处，就选最明显的那一处；找不到或者有歧义，写 `无法确定`；
3. **做完 30 条之前不要看 OCR 结果**，免得被它带偏。

另存为 `output/windows-w8/missed/missed30-answers.tsv`（UTF-8、制表符分隔，不要用 Excel 另存，Excel 会改编码）。

**Claude 怎么判断：**
- 270 条全部自动分类：①去掉“what / is / the / document / title / name”这类模板词后，查询里没有剩下的内容词，记为“查询太泛”；②有内容词，而且相关文档的 OCR 文本里都出现了，记为“排名问题”；③有内容词，但 OCR 文本里缺了，记为“OCR 缺字”。
- 30 条人工答案：每条看 `answer_in_image` 有没有出现在相关文档的 OCR 文本里（统一大小写、去掉空白后比较），再算字符级的编辑距离比例。
- 结果作为论文分析 B2 局限的数据，**不设通过线**。A、B 两份文件都交回才算完成。

### 16.8 没有内存上限时，畸形文件的防护还管不管用（`docmgr_w8b`）

**为什么：** 发现 4。Linux 上子进程有内存上限兜底，Windows 上没有，只能靠解析之前的三道检查：zip 解压后的总大小（`PARSE_ZIP_MAX_TOTAL_BYTES`，200 MB）、zip 里的文件数（`PARSE_ZIP_MAX_ENTRIES`，5000）、图片像素数（`PARSE_IMAGE_MAX_PIXELS`，1 亿）。这三道检查只有单元测试，没有用真实 Worker 在 Windows 上跑过（GLOBAL §7.2、§9.1“畸形压缩包处理”）。

**步骤：**
1. 用 main 环境的标准库（不需要新依赖）在仓库外生成三个文件：

   ```powershell
   Set-Content -Encoding utf8 "<仓库外的目录>\make_bad_files.py" -Value @'
   import struct, sys, zlib, zipfile
   from pathlib import Path
   out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
   CT = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
         '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
   with zipfile.ZipFile(out / 'bomb.docx', 'w', zipfile.ZIP_DEFLATED) as z:
       z.writestr('[Content_Types].xml', CT)
       with z.open('word/document.xml', 'w') as f:
           block = b' ' * (1 << 20)
           for _ in range(300):
               f.write(block)
   with zipfile.ZipFile(out / 'many.docx', 'w', zipfile.ZIP_DEFLATED) as z:
       z.writestr('[Content_Types].xml', CT)
       for i in range(6000):
           z.writestr(f'word/media/x{i}.txt', 'x')
   def chunk(t, d):
       return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)
   w, h = 12000, 9000
   c = zlib.compressobj(9)
   row = b'\x00' * (w + 1)
   idat = bytearray()
   for _ in range(h):
       idat += c.compress(row)
   idat += c.flush()
   png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 0, 0, 0, 0))
          + chunk(b'IDAT', bytes(idat)) + chunk(b'IEND', b''))
   (out / 'huge.png').write_bytes(png)
   for p in sorted(out.iterdir()):
       print(p.name, p.stat().st_size)
   '@
   .\.venv-main\Scripts\python -I "<仓库外的目录>\make_bad_files.py" "<仓库外的新目录>\bad-files"
   ```

   （`CT` 那两行里的双引号是 XML 属性的引号，在 Python 字符串里，不经过命令行传参，不受 PowerShell 5.1 吞引号的影响。）Mac 上同一脚本生成的大小是：`bomb.docx` 306197 字节（解压后 314573058 字节）、`huge.png` 105052 字节（12000×9000 像素）、`many.docx` 712105 字节（6001 个文件）。Windows 上应该相同或只差几个字节。
2. 窗口变量指向 `docmgr_w8b`、`w8b_`。启动后端和**一个**通用 Worker，不开 OCR Worker 和 CLIP 服务。启动采样脚本，输出到 `$out\bad-files\memory.csv`。
3. 在 `backend/` 下 `python -m app.modules.auth create-admin w8admin` 建一个用户（密码在终端里输入，不写进报告）；用第 12.6 节第 3 步的写法登录，拿到 `$tok`。
4. 逐个上传，记下 HTTP 状态码和应答。最后一个 `ffhv0228.jpg` 是对照组：它是正常图片，而且不在第 16.5 节的 40 个文件里，用来证明 Worker 处理完三个畸形文件之后仍然正常：

   ```powershell
   foreach ($f in 'bomb.docx', 'many.docx', 'huge.png') {
     curl.exe -s -o "$out\bad-files\upload-$f.json" -w "%{http_code}`n" -H "Authorization: Bearer $tok" -F "file=@<仓库外的新目录>\bad-files\$f" http://127.0.0.1:8000/api/documents
   }
   curl.exe -s -o "$out\bad-files\upload-control.json" -w "%{http_code}`n" -H "Authorization: Bearer $tok" -F "file=@experiments\docvqa\datasets\files\docvqa\ffhv0228.jpg" http://127.0.0.1:8000/api/documents
   ```

5. 等 parse 任务全部结束（`Wait-Tasks 'docmgr_w8b' "'parse'"`），对 4 个文档各导出 `GET /api/documents/<id>` 和 `GET /api/documents/<id>/tasks`，存成 `$out\bad-files\<文件名>-document.json`、`<文件名>-tasks.json`；再导出一次 `GET /health`，存成 `health.json`。然后停止采样。

**预期：**
- 4 次上传都返回 `201`。上传时只看文件头和 `[Content_Types].xml`，三道上限检查发生在解析阶段，这是设计如此。
- `bomb.docx`：parse 任务 `failed`、`attempts = 1`（这类错误不可重试，不浪费重试次数），`error` 是“解压后共 314573058 字节，超过上限 209715200 字节，拒绝解析（可能是 zip 炸弹）”；文档 `status` 为 `failed`。
- `many.docx`：同上，`error` 是“压缩包内有 6001 个文件，超过上限 5000 个，拒绝解析”。
- `huge.png`：同上，`error` 是“图片尺寸为 12000×9000，像素数超过上限 100000000，拒绝处理”；没有产生 ocr 和 embed 任务。
- 对照组 `ffhv0228.jpg`：parse `succeeded`，产生了 ocr 和 embed 任务。OCR Worker 没开，ocr 任务停在 `pending`；embed 任务由通用 Worker 领取，CLIP 服务没开，会重试几次后标为 `failed`，这是设计行为（`CLAUDE.md`“启动 Worker”一条）。（2026-11-23 更正：原来写的是两个任务都停在 `pending`，第二轮实测 embed 为 `failed`，是这里写错了。）
- `memory.csv` 里 `worker` 组的峰值不超过 500 MB（第一轮 W3 处理 500 张图时的峰值是 261.7 MB）；整个过程中通用 Worker 没有退出。
- 如果错误原文、`attempts` 或状态与上面不同，照原样记下来，不要重试到符合预期为止。

**Claude 怎么判断：** 逐个对照 JSON 里的 `status`、`attempts`、`error` 和上面的预期；从 `memory.csv` 取 `worker` 组在上传前后的峰值；确认对照组成功。全部符合就判为通过，并从 `docs/untested.md` 删去对应的“Windows 上没有内存上限时的畸形文件处理”。

### 16.9 验收标准

- [ ] 16.3：`crash-events.txt`、`application-log-info.txt`、`wer-reports.txt` 都在；有事件时 8 个时刻都对上了，没有事件时写明是被覆盖还是当时没生成
- [ ] 16.4：20 个 CSV，每个 4 行；A、B 的崩溃次数写进报告；`memory.csv` 覆盖全程、间隔不超过 3 秒；有崩溃时附上这次的事件日志
- [ ] 16.5：4 个 CSV，每个 40 行；每组的开始、结束时刻写进报告；`memory.csv` 覆盖全程；`machine.txt` 在
- [ ] 16.6：`analyze.jsonl` 有 17 行
- [ ] 16.7：`ocr-chunks.csv`（1589 行，或者写明实际行数）、`document_map.csv`、Barry 填好的 `missed30-answers.tsv`
- [ ] 16.8：4 份上传应答、8 份文档和任务 JSON、`health.json`、`memory.csv`；每个文件的结果都与预期逐条对照过
- [ ] 全程没有改代码和配置文件；没有碰 `docmgr`、`docmgr_test`、`docmgr_w6`；对 `docmgr_docvqa` 只读
- [ ] `output/windows-w8/` 里有 `git-head.txt`、`commands.txt`、`SHA256SUMS.txt`（第 14.1 节）

### 16.10 怎样算测试成功

按第 0.5 节的三条判定：执行方自查通过（第 16.9 节每条都打勾，报告里有命令、输出、退出码），原始数据齐全，Claude 核对通过（第 14.2 节的 W8 几行）。W8 里只有第 16.8 节有通过或失败之分；其余各节是测量，**数据完整、来源可查就算完成**，结论由 Claude 核对后写进核对记录和 `docs/untested.md`，作为 T27 和论文的依据。任何一项做不到，按第 9 节最后一句处理：写明卡在哪里，继续做不依赖它的部分。

------------------------------------------------------------------------

## 17. W9：第二轮没完成的项目与改良后的补测方案（2026-11-23 添加）

来源：第二轮结果（`065e640`、`54d9760`，基线 `fd0b5eb`）的核对，记录在 `docs/changes/windows-2026-11-23-核对.md`。已经完成的不再重做；本节只安排**没完成的**、**判定标准要改的**、**发现了新问题的**几项。规则同 W6：只测量和核对，不改代码和配置文件；环境变量只在窗口里临时设；结果与预期不符时，记下现象和完整输出，问 Barry。原始数据放进 `output/windows-w9/`，报告写进 `windows任务报告.txt` 末尾新加的 W9 一节，或单独写 `output/windows-w9/summary.txt`。

### 17.1 第二轮的结果与本节的安排

| 原小节 | 第二轮结果 | 本节怎么处理 |
|---|---|---|
| W4 10.2 第 5 项场景①（停后端后刷新） | 跳到了登录页。这正是 T24x 修的问题，但 T24x 在 `fd0b5eb` 之后才提交，Windows 测的是修复前的代码 | 第 17.6 节在新基线上按 T24x 的新行为重测 |
| W4 10.2 第 7 项（四个开关全关后 `ch` 残留） | 地址栏留着上一次的 `ch=image` | Barry 于 2026-11-25 决定保留现状（地址栏记的是最后一次真正执行的检索，刷新能恢复结果），不算偏差，**不测** |
| W4 10.3 真实鼠标拖入 | 自动化工具不能跨窗口拖 | 第 17.7 节由 Barry 手动做 |
| W5 11.5 连接超时 | 网络立刻回绝，测不到超时 | 第 17.3 节改用本地监听 |
| W6 12.3 符号链接 | 执行方没有权限 | 第 17.9 节，Barry 本人 |
| W6 12.4 第 10 步 | 排名与 W3 不完全相同；原判定标准（逐条相同）定错了 | 第 17.4 节按新标准重测，并补交结果目录 |
| W6 12.7 OCR Ctrl+C | **未通过**：Windows 上正在识别的任务被打断 | 已由 T24aa 修复（2026-11-23，D52），按第 17.5 节重测，并加测通用 Worker |
| W6 12.5 强制结束 Worker | 数据正确；但日志显示被强杀的 Worker 的子进程还在继续跑 | 已由 T24ab 修复（2026-11-23，D53），按第 17.5 节 C 验证 |
| W6 12.9、12.10 真实文件 | 没有样本 | 第 17.10 节放宽样本的来源说明，由 Barry 自己制作 |
| 第 0.2 节第 4 步的 `mapping-eol.txt` | 没交 | 第 17.2 节补交 |
| W7 13.2 内存 | 合计峰值少算了 OCR 识别子进程（采样脚本的问题，Claude 已按原始数据重算为 5732.8 MB） | 不重测；以后的采样改用第 17.2 节的新脚本 |
| W8 16.5 第一组的一次 300 秒超时 | 同一文档第二次 88 秒成功 | 第 17.8 节对这个文档单独重复测 |
| W8 16.7 B 人工核对 | 没做 | 第 17.11 节，Barry 本人 |
| W8 16.8 对照组 embed | 实际是重试后 `failed` | 这是设计行为，第 16.8 节的预期已更正，**不重测** |
| T24v–T24z 登录页 | 在 `fd0b5eb` 之后提交，没有测过 | 第 17.6 节与真实后端联调 |

**2026-11-26 更新（W9 结果，核对见 `docs/changes/windows-2026-11-26-核对.md`）：** 上表第 2–9 步都已完成。还剩：① Barry 本人的 17.7、17.10、17.11；② 17.9 的 backend 6 项——权限已经有了，只是指定的 `--basetemp` 目录不存在，换一个存在的目录重跑（`New-Item -ItemType Directory -Force <目录>` 之后再跑第 12.3 节的命令）；③ 17.6 第 3a 步要等 Bug 1 修复后重测。**（2026-11-26 再更新：Bug 1 已由 T24ah 修复；②、③ 改到第 18 节 W10 做，见第 18.4、18.5 节。）**

**执行顺序（2026-11-25 重排：刚改过、影响最大的代码先验证；各节内容没有变）：**

| 顺序 | 内容 | 谁做 | 依赖 | 预计耗时 |
|---|---|---|---|---|
| 1 | Barry 推送；Windows `git pull`，确认 T24aa–T24ag、T24ba–T24be、T24bh 都在（见下面的更新说明） | Barry、GPT | — | 15 分钟 |
| 2 | 第 17.2 节：换行符核对、前端三项命令、backend / shared / OCR Worker 全套测试（含从没运行过的 12 项集成测试）。**集成测试有失败就先停下报给 Barry**，不做第 3、4 步 | GPT | 1 | 1.5 小时 |
| 3 | 第 17.15 节：重试间隔；接着第 17.16 节：批量放回队列。这里要用的 `docmgr_w9`、前缀 `w9_`、新的存储目录在这一步新建（`alembic upgrade head`） | GPT | 2 | 50 分钟 |
| 4 | 第 17.5 节：Ctrl+C、强制结束后的子进程、循环脚本 | GPT | 2 | 50 分钟 |
| 5 | 第 17.4 节：12.4 第 10 步重测；接着第 17.17 节：检索服务停掉时 `repair` 的提示 | GPT | 2 | 70 分钟 |
| 6 | 第 17.6 节：登录页与停机刷新 | GPT | 2 | 1 小时 |
| 7 | 第 17.18 节：界面更新（T24ba–T24be，接着第 17.6 节用同一套 `docmgr_ui`） | GPT | 2、6 | 2 小时 |
| 8 | 第 17.14 节：OCR Worker 数与崩溃（会吃满内存，不和别的测量同时跑） | GPT | 2 | 2 小时 |
| 9 | 第 17.3 节：连接超时 | GPT | 1 | 20 分钟 |
| 10 | 第 17.8 节：300 秒超时的文档（`docmgr_w9` 已被第 3 步用过，改用新建的 `docmgr_w9c`、前缀 `w9c_`） | GPT | 2 | 40 分钟 |
| 11 | 按第 14.1 节整理 `output/windows-w9/`、提交；Barry 推送，大文件另交 | GPT、Barry | 全部 | 30 分钟 |

**Barry 本人的四项**不依赖上表，随时可以做，建议顺序：第 17.9 节符号链接（20 分钟，最先做）→ 第 17.10 节真实文件（可以和 T25 收集数据一起）→ 第 17.7 节鼠标拖入（10 分钟左右）→ 第 17.11 节 30 条核对（40 分钟）。

**2026-11-25 更新（第五轮，核对见 `docs/changes/windows-2026-11-25-核对.md`）：** 第五轮测的是旧代码 `54d9760`，**上表各项除了“第 16.8 节对照组”都还没有做**，仍按上面的顺序执行；先 `git pull`，`git log --oneline | Select-String "T24aa|T24ab|T24ac|T24ad|T24ae|T24af|T24ag|T24ba|T24bb|T24bc|T24bd|T24be|T24bh"` 要能各找到一条。第五轮的 OCR 崩溃复现见第 17.14 节，要重做。已经完成的：`docker-compose.yml`、OpenSearch 的 Dockerfile（还差后端 `/health` 的输出，以及 `down` 之后数据卷保留，可以顺手补上，存到 `output/windows-w9/docker/`）。

### 17.2 基线、公用脚本、新的内存采样脚本

1. `git pull`，确认是快进，记下提交号写进 `output/windows-w9/git-head.txt`（第 14.1 节的格式）。这个提交要包含 T24v–T24z（`git log --oneline | Select-String T24z` 能找到）。
2. 补做第 0.2 节第 4 步的核对，输出存成 `output/windows-w9/mapping-eol.txt`：

   ```powershell
   git ls-files --eol -- shared/text_index/mappings backend/app/modules/vector_index/mappings
   Get-FileHash shared\text_index\mappings\*.json, backend\app\modules\vector_index\mappings\*.json -Algorithm SHA256
   ```

   预期：三行都是 `i/lf w/lf attr/text eol=lf`；SHA-256 开头为 `be91f8071d05`（doc_meta）、`0c7937251bab`（chunks）、`c984e85b889b`（image_vectors）。不一致就按第 0.2 节第 4 步先删再签出，然后再导出一次。
3. 新基线上有前端改动（T24v–T24z、T24bb–T24be）、任务接口改动（T24ba）和 Worker 改动（T24aa、T24ab、T24ac、T24ad）以及一个新命令（T24ae）、一处命令行提示（T24af，**2026-11-25 更正：原来写“只有前端代码变了”已过时**）。在 `frontend/` 下运行三项命令，输出存成 `frontend-typecheck.txt`、`frontend-test.txt`、`frontend-build.txt`。预期：类型检查、构建成功，单元测试 32 个文件 378 项全部通过（Mac 上 T24bh 的结果；**2026-11-25 更正：原来写 17 个文件 207 项，是 T24ba 之前的数**）。如果这次拉到的提交里已经有 Ctrl+C 的修复（第 17.5 节），再按第 12.2 节重跑 backend、shared、OCR Worker 的测试，JUnit 存到 `output/windows-w9/`。
4. 第 16.2 节的公用函数（`Q`、`Export`、`Wait-Tasks`、`Start-Ocr`）照用，只把 `$out` 改成 `"$repo\output\windows-w9"`。
5. **新的内存采样脚本。** 第 13.2、16.2 节的脚本把 OCR 识别子进程归进了 `python_other`：子进程是 multiprocessing 启动的，命令行里没有 `ocr_worker`。新脚本沿着父进程往上找，并且每次只调用一次 CIM，所以采样更快：

   ```powershell
   Set-Content -Encoding utf8 "<仓库外的目录>\sample_w9.ps1" -Value @'
   param([string]$Out, [string]$Stop, [double]$Interval = 1)
   "time,group,pid,working_set_mb,private_mb" | Out-File -Encoding utf8 $Out
   function Group-Of($p, $byId) {
     $cur = $p
     for ($i = 0; $i -lt 6 -and $cur; $i++) {
       $c = "$($cur.CommandLine)"
       if ($cur.Name -eq 'postgres.exe') { return 'postgresql' }
       if ($cur.Name -eq 'java.exe') { return 'opensearch' }
       if ($cur.Name -eq 'node.exe') { return 'node' }
       if ($c -match 'uvicorn') { return 'api' }
       if ($c -match '-m\s+ocr_worker') { if ($i -eq 0) { return 'ocr_worker' } else { return 'ocr_engine' } }
       if ($c -match '-m\s+clip_service') { return 'clip_service' }
       if ($c -match '-m\s+app\.worker') { if ($i -eq 0) { return 'worker' } else { return 'worker_child' } }
       $cur = $byId[[int]$cur.ParentProcessId]
     }
     return 'python_other'
   }
   while (-not (Test-Path -LiteralPath $Stop)) {
     $t0 = Get-Date; $now = $t0.ToString('o')
     $procs = @(Get-CimInstance Win32_Process -Property ProcessId, ParentProcessId, Name, CommandLine, WorkingSetSize, PrivatePageCount)
     $byId = @{}; foreach ($p in $procs) { $byId[[int]$p.ProcessId] = $p }
     $lines = @(foreach ($p in $procs) {
       if ($p.Name -in @('postgres.exe', 'java.exe', 'python.exe', 'node.exe')) {
         "$now,$(Group-Of $p $byId),$($p.ProcessId),{0:F1},{1:F1}" -f ($p.WorkingSetSize / 1MB), ($p.PrivatePageCount / 1MB)
       }
     })
     $avail = (Get-CimInstance Win32_OperatingSystem -Property FreePhysicalMemory).FreePhysicalMemory / 1KB
     $cpu = (Get-CimInstance Win32_PerfFormattedData_PerfOS_Processor -Filter "Name='_Total'").PercentProcessorTime
     $lines += "$now,system_available,0,{0:F1},0" -f $avail
     $lines += "$now,cpu_total_percent,0,$cpu,0"
     $lines | Out-File -Append -Encoding utf8 $Out
     $wait = $Interval - ((Get-Date) - $t0).TotalSeconds
     if ($wait -gt 0) { Start-Sleep -Milliseconds ([int]($wait * 1000)) }
   }
   '@
   ```

   用法同第 16.2 节：`powershell -NoProfile -ExecutionPolicy Bypass -File "<仓库外的目录>\sample_w9.ps1" -Out <文件> -Stop <停止文件>`。识别子进程归在 `ocr_engine` 组，解析子进程归在 `worker_child` 组。用之前先空跑 30 秒，确认相邻两次采样的间隔不超过 3 秒，并把这 30 秒的输出存成 `sampler-selftest.csv`。

6. **内存上限提示与网页图标（T24ag，2026-11-25 添加）。** W9 里任何一次用通用 Worker 处理 5 个以上任务时，把它的启动日志存成 `worker-startup.log`：`Select-String "内存上限|限制子进程的内存"` 应当只在启动时命中 1 行（“当前系统不支持限制子进程的内存”），任务处理期间没有。第 17.6 节打开前端时，网络记录里不应有 `favicon.ico`，`favicon.svg` 返回 200，浏览器标签上有图标。

### 17.3 连接超时（改良 W5 第 11.5 节）

**为什么改：** 第二轮 `10.255.255.1` 被网络立刻回绝（约 1.9 秒报 `OperationalError`），根本没走到超时。改成在本机起一个**只接受连接、从不回应**的监听：客户端连得上，但等不到数据库的应答，只能靠 `connect_timeout` 结束。Claude 在 Mac 上用 psycopg 试过：设 3 秒、5 秒，分别在 3.0、5.0 秒报 `ConnectionTimeout`。

1. 在仓库外写监听脚本，在一个单独的窗口里运行（main 环境的标准库就够，不需要新依赖）：

   ```powershell
   Set-Content -Encoding utf8 "<仓库外的目录>\blackhole.py" -Value @'
   import socket, sys
   port = int(sys.argv[1])
   s = socket.socket()
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind(('127.0.0.1', port))
   s.listen(50)
   print('blackhole listening on', port, flush=True)
   held = []
   while True:
       c, _ = s.accept()
       held.append(c)  # 只接受，不回应，也不关闭
   '@
   .\.venv-main\Scripts\python -I "<仓库外的目录>\blackhole.py" 55999
   ```

2. 另开一个窗口：`$env:DATABASE_URL = "postgresql://w9:w9@127.0.0.1:55999/w9"`（用户名、密码随便写，不要用真实的），然后按第 11.5 节的计时写法做原表的 4 步（通用 Worker 默认、设 3 秒，OCR Worker 设 5 秒、20 秒）。每步的完整输出存成 `timeout-<步骤>.txt`，耗时和退出码汇总到 `timeouts.json`。
3. 做完后在监听窗口按 Ctrl+C 结束它。

**预期：** 第 1 步约 10 秒、第 2 步约 3 秒结束，退出码 1，输出“Worker 无法连接数据库（ConnectionTimeout）……”；第 3、4 步先加载模型，再分别等约 5 秒、20 秒，退出码 1，两步的耗时差约 15 秒，输出“OCR Worker 无法连接数据库（ConnectionTimeout）……”。四步的耗时与设定值相差都在 2 秒以内，才判为通过。

### 17.4 一致性修复之后的检索结果（改良 W6 第 12.4 节第 10 步）

**为什么改：** 第二轮 B2 有 110 / 500 条排名与 W3 不同，但指标几乎不变（nDCG@10 差 −0.0002）。删除文档或重写片段时，OpenSearch 不会马上清掉旧的文档，只是标记为“已删除”，等段合并时才真正清掉；而 BM25 的统计值（文档总数、平均长度、词频）把这些已删除的文档也算进去。W3 的 B2 是在 reocr（每个 OCR 任务都先删后写）之后跑的，12.4 又删了一个文档的片段再重建，两次的“已删除文档数”不同，分数有微小差别，分数接近的文档就会换位置。所以“与 W3 逐条相同”这条标准定错了。新标准分三条：**同一索引状态下连续两次结果完全相同**；**指标与 W3 只差很小的量**；**能用合并前后的对比说明原因**。

在 `docmgr_docvqa`、`docvqa_` 上做（第 12.4 节修复后的状态，不要再造不一致），所有 Worker 停着，CLIP 服务开着（B3 要用）。在 `backend/` 下：

1. 记下索引状态，存成 `index-before.txt`：

   ```powershell
   curl.exe -s "http://127.0.0.1:9200/_cat/indices/docvqa_*?v&h=index,docs.count,docs.deleted,segments.count"
   ```

2. 先 `git status --porcelain > ..\output\windows-w9\git-status-before-runs.txt`，然后各跑两次，依次记为 R1、R2：

   ```powershell
   ..\.venv-main\Scripts\python -m app.modules.experiments --root ..\experiments\docvqa run --config ..\experiments\configs\B2.json
   ..\.venv-main\Scripts\python -m app.modules.experiments --root ..\experiments\docvqa run --config ..\experiments\configs\B2.json
   ..\.venv-main\Scripts\python -m app.modules.experiments --root ..\experiments\docvqa run --config ..\experiments\configs\B3.json
   ..\.venv-main\Scripts\python -m app.modules.experiments --root ..\experiments\docvqa run --config ..\experiments\configs\B3.json
   ```

3. 只对 `docvqa_` 的三个索引清掉已删除的文档（这是 OpenSearch 的段合并，不改数据、不删索引）：

   ```powershell
   foreach ($i in 'docvqa_chunks', 'docvqa_doc_meta', 'docvqa_image_vectors') { curl.exe -s -X POST "http://127.0.0.1:9200/$i/_forcemerge?only_expunge_deletes=true" }
   ```

   等几秒，再执行第 1 步的命令，存成 `index-after.txt`。
4. 再跑一次 B2、一次 B3，记为 R3。
5. 把这 6 个结果目录，加上第二轮 12.4 的两个目录（`20261122T105621.715980Z_B2_bca3b6`、`20261122T105723.742460Z_B3_e0a936`），一起打成 `w9-runs.zip`（大于 5 MB 就另交），SHA-256 写进 `SHA256SUMS.txt`。

**预期：**
- `index-before.txt` 里 `docvqa_chunks` 的 `docs.deleted` 大于 0，`index-after.txt` 里是 0（或明显变小）；
- B2 的 R1 与 R2、B3 的 R1 与 R2，500 条查询的排名逐条完全相同；
- R3 允许与 R1 不同；
- R1、R2、R3 的 P@10、R@10、nDCG@10 与 W3 同配置相差都不超过 0.01；
- 退出码都是 0，`complete` 都是 true。

**Claude 怎么判断：** 逐条比较排名；对排名变了的查询，从 `results.jsonl` 取换位的两个文档在通道内的分数，算相对差。如果换位都发生在分数相对差很小（例如小于 1%）的地方，就确认“已删除文档影响统计值”这个解释成立。同时核对 8 个目录 `config.json` 里三个 mapping 的 SHA-256（应为第 17.2 节第 2 步的 LF 版本）和 `git_dirty`（对照 `git-status-before-runs.txt` 解释）。

### 17.5 Ctrl+C 重测（T24aa 修复之后）

**为什么：** 第二轮 12.7 发现，Windows 上 OCR Worker 识别途中按 Ctrl+C，主进程等待识别子进程时抛 `InterruptedError`，当前任务被记成一次失败、放回队列，Worker 以退出码 1 结束，不符合 D34“处理完当前任务后退出”。Claude 复核代码时又发现，通用 Worker 有同样的等待写法，而且它的子进程没有忽略 Ctrl+C，在任何系统上都会把正在解析的文件记成一次失败。这两处已由 **T24aa**（2026-11-23，D52）修复：等待被打断时接着等，通用 Worker 的子进程也忽略 Ctrl+C。先确认拉到的提交包含 T24aa（`git log --oneline | Select-String T24aa`），并按第 17.2 节第 3 步重跑 backend、shared、OCR Worker 的测试（backend 应多出 `test_worker_runner.py` 的 4 项，其中 1 项在 Windows 上跳过；OCR Worker 应多出 `test_engine_process.py` 的 4 项，其中 1 项跳过），再做这一节。

**为了留下原始输出，Worker 改在 `cmd` 窗口里运行**，把日志重定向到文件（PowerShell 的管道会干扰 Ctrl+C）：

A. **OCR Worker**（`docmgr_w6`，同第 12.7 节）：先 `reocr --yes`（`--root` 为 docvqa60 目录），再新开一个 **cmd** 窗口，设好与第 6.1 节相同的环境变量（`set DATABASE_URL=...` 等），然后在 `services\ocr_worker` 下：

```bat
..\..\env_check\.venv-ocr\Scripts\python -m ocr_worker 2> ..\..\output\windows-w9\ctrlc-ocr.log
echo exit=%ERRORLEVEL%
```

在另一个窗口看 `ctrlc-ocr.log`，出现“开始 OCR 任务”后记下任务 id，回到 cmd 窗口按一次 Ctrl+C。等它退出，把 `exit=` 那一行存进 `ctrlc-ocr-exit.txt`，再导出这个任务：`Export 'docmgr_w6' "SELECT id, status, attempts, error, started_at, finished_at FROM processing_tasks WHERE id = '<任务 id>'" 'output/windows-w9/ctrlc-ocr-task.csv'`。之后照常启动 OCR Worker 把剩下的做完。

B. **通用 Worker**（`docmgr_w6`）：用第 12.6 节的 `big3000.pdf` 再上传一次（不设超时变量，它要解析几十秒）。在 cmd 窗口的 `backend` 下：

```bat
..\.venv-main\Scripts\python -m app.worker 2> ..\output\windows-w9\ctrlc-worker.log
echo exit=%ERRORLEVEL%
```

日志出现这个文档的“开始任务”后按一次 Ctrl+C，同样记下退出码、导出任务。

**预期：** 日志出现停止提示（OCR Worker 是“收到信号 2，处理完当前任务后退出”，通用 Worker 是“收到信号 SIGINT，完成当前任务后退出”）；当前任务**照常做完**：`succeeded`、`attempts = 1`、`error` 为空；Worker 在这之后退出，不再领新任务；日志里没有 `InterruptedError`、`KeyboardInterrupt`。退出码：两个 Worker 都是 130（OCR Worker 原来是 0，T24ac 改为 130，D54）。第二轮 12.7 记录的退出码 1 不能由代码解释，这次如果又看到 130 以外的值，照实记录，并写明是怎么启动的。

**C. 强制结束 Worker，子进程应当跟着退出**（T24ab，`docmgr_w6`，2026-11-23 添加）。先确认拉到的提交包含 T24ab；`test_worker_runner.py`、`test_engine_process.py` 里的 `test_child_exits_when_the_parent_is_killed` 各 1 项应当在 Windows 上通过（不跳过）。然后分别对通用 Worker（再上传一次 `big3000.pdf`）和 OCR Worker（`reocr --yes` 之后）做：

1. 启动 Worker，看到“开始任务”（或“开始 OCR 任务”）后，记下主进程 PID、任务 id，并列出它的子进程：

   ```powershell
   Get-CimInstance Win32_Process -Filter "ParentProcessId = <主进程 PID>" | Select-Object ProcessId, ParentProcessId, CommandLine | Format-List | Out-File -Encoding utf8 "$out\kill-<worker>-children.txt"
   ```

   虚拟环境里的 `python.exe` 可能是启动器，真正的 Worker 是它的子进程；以日志里领取者标识中的 PID 为准。
2. `Stop-Process -Id <主进程 PID> -Force`，等 3 秒，再用 `Get-Process -Id <子进程 PID> -ErrorAction SilentlyContinue` 逐个查第 1 步列出的 `spawn_main` 子进程，输出存成 `kill-<worker>-after.txt`（没有输出就写“无”）。
3. 重新启动一个 Worker，等任务被回收重做，导出这个任务（同 A 的 `Export`，文件名 `kill-<worker>-task.csv`）。

**预期：** 第 2 步 3 秒后子进程都已不在；被杀 Worker 的日志里没有 `BrokenPipeError`；第 3 步任务最终 `succeeded`、`attempts = 2`，同一文档没有重复的 OCR 任务（`SELECT document_id, payload::text, count(*) FROM processing_tasks WHERE task_type = 'ocr' GROUP BY 1, 2 HAVING count(*) > 1` 为 0 行）。

**D. 在循环脚本里按 Ctrl+C**（T24ac，2026-11-23 添加）。A、B 两步直接运行 Worker，不套循环；这一步专门验证循环。在 `services\ocr_worker` 下用 `run_ocr_worker_loop.ps1` 启动（`-StopFile` 指向一个不存在的文件），看到“OCR 模型已加载”后按一次 Ctrl+C，等 60 秒。**预期：** Worker 打印“收到信号 2……”后退出，循环随之结束，60 秒内没有再出现“OCR 模型已加载”，也没有残留的 `-m ocr_worker` 进程（`Get-CimInstance Win32_Process | Where-Object CommandLine -match '-m ocr_worker'`）。窗口输出存成 `ctrlc-loop.txt`。

### 17.6 登录页与停机刷新（T24v–T24z、W4 第 10.2 节第 5 项场景①）

**为什么：** T24v–T24z 只对着临时模拟后端检查过（`docs/untested.md` 第 4 节“T24v–T24z”）；W4 场景①在第二轮测的是 T24x 之前的代码。在 W4 的 `docmgr_ui` 上，用 `npm run dev` 的前端做。每一步截图存到 `output/windows-w9/login/`，同时用浏览器开发者工具把这一步的网络请求导出成 HAR（或者至少记下请求地址和状态码）。

| # | 操作 | 预期 |
|---|---|---|
| 1 | 登录后停掉后端，在文件页按 F5 刷新；再在检索页（`/search?q=合同`）刷新一次 | 都跳到登录页：文件页是首页，地址是 `/login`；检索页带 `redirect=/search?q=合同`（编码后）。本地令牌**还在**（开发者工具 → Application → Local Storage），卡片上方显示“暂时连不上服务器，登录状态已保留……”和“重试”；**不**同时显示 T24z 的提示 |
| 2 | 重新启动后端，点“重试” | 不用输密码，直接回到第 1 步之前的页面 |
| 3 | 停掉 PostgreSQL（后端开着），刷新文件页 | `/api/auth/me` 返回 503，同样保留令牌并显示第 1 步的提示；再清掉令牌打开 `/login`：显示 T24z 的“后端已启动，但数据库不可用……”和“重新检查”；记下打开页面到提示出现大约几秒 |
| 4 | 启动 PostgreSQL，点“重新检查” | 提示消失 |
| 5 | 停掉后端，清掉令牌，打开 `/login` | 显示“连不上后端服务，现在无法登录……”；启动后端后点“重新检查”，提示消失 |
| 6 | 用错误的密码登录 | 按钮上方红色提示“用户名或密码错误”，几秒后仍在；改一下密码框，提示收起 |
| 7 | 注册模式下用已存在的用户名注册 | 提示“这个用户名已被注册……”；切回登录模式，提示收起 |
| 8 | 新开一个窗口设 `$env:ACCESS_TOKEN_EXPIRE_SECONDS = "60"`，在这个窗口重启后端；登录，打开 `/search?q=合同` 并检索一次，等 70 秒后再点“检索” | 回到登录页，地址带 `redirect=/search?q=合同`（编码后），本地令牌已清除；重新登录后回到检索页，检索框里是“合同”。做完关掉这个窗口，用原来的设置重启后端 |
| 9 | 已登录时直接打开 `/login?redirect=/search` | 直接进入 `/search`，不停在登录页 |
| 10 | 未登录时打开 `/login?redirect=/\evil.com`，登录 | 登录后回到首页 `/`，地址栏不出现 `evil.com` |
| 11 | 退出登录。开发者工具 → Network 勾选 Preserve log，限速选 Slow 3G（或 Slow 4G）；在登录页填好正确的用户名和密码，光标留在密码框，**快速连按两次回车**；登录完成后把限速改回 No throttling（2026-11-23 添加，T24w） | Network 里 `POST /api/auth/login` **只有一条**；进入文件页。如果两次回车之间页面已经跳走，加大限速再试一次 |

**Claude 怎么判断：** 对照截图和网络记录逐条看；第 3 步的耗时作为 T24z“数据库连不上时提示晚一点出现”的实测数据。全部符合，才从 `docs/untested.md` 删掉“T24v–T24z”一节的对应行，以及第 4 节“前端与真实后端的联调”里登录页的部分。

### 17.7 鼠标从资源管理器真实拖入（W4 第 10.3 节，Barry 手动）

自动化工具不能把文件从一个窗口拖到另一个窗口，所以由 Barry 手动做。准备：`npm run dev` 的前端、W4 的 `docmgr_ui`，资源管理器打开第 10.3 节的样本目录（一个 PDF、一张图片、一个不支持的文件，例如 `.txt`）。

1. 浏览器打开文件页，按 F12 打开开发者工具，切到“网络”标签页，勾选“保留日志”。
2. 用鼠标把 PDF 拖进上传区：拖到区内时区域高亮；在区内的文字上来回拖几下，高亮不应该闪烁消失；松开后开始上传。
3. 同时拖入图片和 `.txt`：图片上传成功，`.txt` 显示拒绝原因。
4. 截三张图：拖动时高亮、上传记录、拒绝原因，存到 `output/windows-w9/drag/`；网络标签页里右键 → “以 HAR 格式保存”，存成 `drag.har`（保存前看一眼，不要包含其他网站的请求）。

**预期：** 两个支持的文件 `POST /api/documents` 返回 201，`.txt` 在前端就被拒绝或后端返回 415，页面显示的原因与第 10.3 节一致。

### 17.8 第一组那次 300 秒超时（W8 第 16.5 节）

**为什么：** 第 16.5 节第一组里，文档 `f35fbcc2`（249 行文字）第一次识别超过 300 秒被终止，第二次 88 秒就成功了。只开一个 Worker、CPU 约 40%，不像是资源不够。要看它是偶发，还是这张图本身有时会卡住。

1. 在 `docmgr_w8b` 上：`SELECT id, filename FROM documents WHERE id = 'f35fbcc2-53bb-41e2-a74f-36ecabd0a75b';` 得到图片名；在第 16.5 节的 `docvqa-scale40\datasets\manifest.csv` 里找到它的行号，用 `make_subset.py` 单独生成一个 1 个文件的数据集 `docvqa-slow1`。
2. 新建 `docmgr_w9c`、前缀 `w9c_`、新的存储目录，`alembic upgrade head`、`validate`、`import`，用 CLIP 服务和一个通用 Worker 做完 parse、embed 后停掉它们。
3. 启动第 17.2 节的新采样脚本（输出 `slow1/memory.csv`）；启动**一个** OCR Worker，按第 16.4 节 A 的循环跑 **15 轮**，每轮导出 `slow1/r<NN>.csv`。

**预期：** 15 个 CSV，每个 1 行。如果有一轮超过 300 秒，记下是第几轮，并看 `memory.csv` 里那段时间 `ocr_engine` 组的内存和 CPU 有没有异常（例如内存持续上涨、CPU 降到接近 0）。**Claude 怎么判断：** 统计 15 轮的耗时分布；没有一轮超过 200 秒，就记为偶发，写进论文局限；超时能复现，就作为 OCR 的问题报给 Barry。

### 17.9 8 项符号链接测试（W6 第 12.3 节，Barry 本人）

做法与第 12.3 节完全相同，那里的命令可以直接复制。两点提醒：
- “开发人员模式”打开后要**注销再登录**，`whoami /priv` 里出现 `SeCreateSymbolicLinkPrivilege` 才算生效；不想改系统设置，就用“以管理员身份运行”的 PowerShell。
- 只跑这 8 项，JUnit 存成 `output/windows-w9/symlink-backend.xml`、`symlink-shared.xml`，`whoami /priv` 那一行存成 `symlink-priv.txt`。

预期：backend 6 passed、shared 2 passed。

### 17.10 真实文件的解析与 OCR（W6 第 12.9、12.10 节，Barry 准备样本）

步骤和核对方法都按第 12.9、12.10 节。第二轮没做的原因是没有样本，这里说清楚“真实样本”指什么，让准备工作变简单：

- “真实”指**由真实的软件或设备产生**，不是指内容必须是别人的文档。Barry 自己在 Microsoft Word 里新建一份文档，打几段字、插一个表格、存盘，就是合格的“Word 保存的文件”；Excel 同理（多个工作表、合并单元格、一个公式，存盘前让公式算出结果）。不能用 AI 或脚本生成文件来代替。
- 有文本层的 PDF：在 Word 里“另存为 PDF”就是一份中文 PDF；双栏的可以用任意公开论文的 PDF。
- 扫描 PDF：打印一页公开的文字，用手机扫描 App 或打印机的扫描功能存成 PDF。
- 手机照片：拍公开的海报、书的版权页，其中一张竖着拍；直接从手机传到电脑，不要截图、不要压缩。
- 截图：一张带中文文字的系统设置页面截图，不要有个人信息。
- 人工抄录：第 12.9 节要求的 4 段，每段 50–200 字，照着原图抄。

`sources.csv` 的 `made_by` 写 Barry，`source` 写“自制（Word 2021 保存）”“手机拍摄（型号）”之类。按第 12.9 节，原文件也要交回。

### 17.11 30 条漏检查询的人工核对（W8 第 16.7 节 B，Barry 本人）

做法不变，见第 16.7 节 B。Claude 已经按自动规则把 270 条分好类（核对记录第 3 节）：14 条查询太泛、33 条内容词都在 OCR 文本里、223 条有内容词不在 OCR 文本里。这 30 条人工答案用来区分最后一类里，哪些是 OCR 漏认了、哪些是图上本来就没有这些词。

### 17.14 OCR Worker 数与崩溃：按正确的方法重做（2026-11-25 添加）

**为什么：** 2026-11-25 的第五轮复现了 `0xC0000005`，但编排脚本用 `$workers.ProcessId` 停 Worker，而 `Start-Process -PassThru` 返回的对象只有 `.Id`，**每一轮的 Worker 都没停掉**，标称“单 Worker”的第 9 轮实际有 9 个在跑（核对见 `docs/changes/windows-2026-11-25-核对.md` 第 2 节）。重新统计后看到：活着的 Worker 不超过 4 个时没有失败，5 个以上每轮都崩。这一节用干净的步骤确认，并补上当时没有采集的**提交内存**（页面文件用量），判断内存耗尽是不是原因。

**方法上的三条硬要求：** 停进程用 `.Id`；每一轮开始前先**数清活着的 OCR Worker**，不为 0 就先全部停掉、等 10 秒再数；每一轮只测一种 Worker 数。测试期间其他程序（浏览器、Docker 之外的服务）保持不变，并记下可用内存的起始值。

**准备：** 数据集用第 16.4 节的 `docvqa-crash4`，数据库与前缀用新的 `docmgr_w9b`、`w9b_`。在新基线（包含 T24aa–T24ac）上做。**先停掉平时常开的 OCR Worker**，只保留 PostgreSQL、OpenSearch、CLIP。采样用第 17.2 节的新脚本，把每次采样最后的 `cpu_total_percent` 一行之前加一行（提交内存，单位 MB，`commit_used` 与 `commit_limit`）：

```powershell
$os = Get-CimInstance Win32_OperatingSystem -Property TotalVirtualMemorySize, FreeVirtualMemory, FreePhysicalMemory
$lines += "$now,commit_limit,0,{0:F1},0" -f ($os.TotalVirtualMemorySize / 1KB)
$lines += "$now,commit_free,0,{0:F1},0" -f ($os.FreeVirtualMemory / 1KB)
```

**步骤：** Worker 数 N = 1、2、3、4、5、6，每种 5 轮（共 30 轮）。每一轮：

```powershell
function Count-Ocr { @(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match '-m ocr_worker' -and $_.Name -eq 'python.exe' }).Count }
function Stop-AllOcr { Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match '-m ocr_worker' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }; Start-Sleep -Seconds 10 }
# 每轮开头
if ((Count-Ocr) -ne 0) { Stop-AllOcr }
"round=<N>-<r> before=$(Count-Ocr) time=$(Get-Date -Format o)" | Out-File -Append -Encoding utf8 "$out\worker-count.txt"
# 启动 N 个：Start-Ocr（第 16.2 节），用返回对象的 .Id 停止
# 等 4 个 OCR 任务全部结束 → 导出 CSV → Stop-AllOcr → 再写一行 after=$(Count-Ocr)
```

注意 `python.exe -m ocr_worker` 在虚拟环境里有启动器和真正的进程两个，`Count-Ocr` 的数要除以 2 理解；日志里“OCR 模型已加载”的份数才是真正的 Worker 数，两者对照写进报告。**可用内存低于 300 MB 或出现“页面文件太小”就停止这一组**，照实记录停在哪一轮，不要继续加压。

**预期：** 30 个 CSV（停止的组除外），每个 4 行；`worker-count.txt` 每轮 before、after 都是 0；`memory.csv` 覆盖全程、间隔不超过 3 秒，有 `commit_free`、`commit_limit`、`system_available`。不设通过线。

**Claude 怎么判断：** 按实际 Worker 数统计失败数；看每次失败前 10 秒的 `commit_free`，如果失败都集中在提交内存将尽的时刻、充足时没有失败，就确认“内存耗尽”；得出建议的 Worker 上限，写进 T30。

### 17.15 失败任务的重试间隔（T24ad，2026-11-25 添加）

**为什么：** 失败的任务原来马上又被领走，CLIP 停十几秒就会让图片永久没有向量。T24ad 让失败过的任务按“上一次尝试的开始时间 + 30 秒 / 120 秒”再领（D55）。SQL 在 Mac 上没有跑过。

1. **集成测试**（随第 17.2 节第 3 步的 backend 测试一起跑）：`tests/integration/test_task_queue.py` 里 T24ad 的 8 项应全部通过，不跳过。
2. **CLIP 短暂不可用后自己恢复**（`docmgr_w9`，CLIP 服务先不开）：启动后端和一个通用 Worker，上传一张图片，记下时间。等 embed 任务第 1 次失败后（`attempts = 1`、`error` 为 ClipUnavailable），启动 CLIP 服务。每 5 秒导出一次这个任务，直到它结束：

   ```powershell
   Q 'docmgr_w9' "SELECT now(), status, attempts, started_at, error FROM processing_tasks WHERE task_type = 'embed' ORDER BY created_at DESC LIMIT 1" | Out-File -Append -Encoding utf8 "$out\retry\embed.txt"
   ```

3. **CLIP 一直不开**：另传一张图片，同样导出，直到 `failed`。

**预期：** 第 2 步：第 1 次失败后，距它的 `started_at` 不到 30 秒时不会出现第 2 次尝试；CLIP 起来后的下一次尝试成功，任务 `succeeded`。第 3 步：相邻两次尝试的 `started_at` 相差不少于 30 秒、120 秒，第 3 次失败后 `failed`，从第 1 次开始到 `failed` 约 150 秒（加上每次尝试的几秒）。轮询间隔 2 秒，所以允许多出几秒。

**Claude 怎么判断：** 逐行看 `embed.txt` 的时间和 `attempts`，两次间隔都不短于设定值才判为通过；同时确认等待期间别的任务照常被处理。

### 17.16 把失败的任务成批放回队列（T24ae，2026-11-25 添加）

**为什么：** CLIP 关得久了，期间的 embed 任务试完 3 次就是 `failed`，恢复后也不会自己再试。T24ae 新增了一个命令来补救（D56）。数据库部分在 Mac 上没有跑过。

1. **集成测试**（随 backend 测试一起跑）：`tests/integration/test_requeue_failed_db.py` 3 项应全部通过，不跳过。
2. **全过程**（接着第 17.15 节第 3 步，那里已经有一个 `failed` 的 embed 任务；再多传 2 张不同的图片，等它们也 `failed`）。在 `backend\` 下，先不启动 CLIP：

   ```powershell
   ..\.venv-main\Scripts\python -m app.modules.documents requeue-failed --type embed
   ```

   然后启动 CLIP 服务，再加 `--yes` 执行一次；等任务处理完，再不加 `--yes` 执行一次。三次的输出和退出码存成 `retry\requeue-1.txt` 到 `requeue-3.txt`。前后各导出一次 embed 任务的 `id, status, attempts, error`，以及 `image_embeddings` 的条数；最后 `consistency check --json`。

**预期：** 第 1 次列出 3 个任务，原因是 ClipUnavailable，没有改动（导出与之前相同）；第 2 次“已放回队列 3 个”，之后 3 个都 `succeeded`、`attempts = 1`，向量条数加 3；第 3 次“没有需要放回队列的 embed 任务”；三次退出码都是 0；一致性检查没有问题。

**Claude 怎么判断：** 对照三次输出与前后两次导出，全部符合才判为通过。

### 17.17 检索服务停掉时 repair 的提示（T24af，2026-11-25 添加）

接着第 17.4 节做，`docmgr_docvqa`、`docvqa_`，只演练和看提示，不改数据。先 `check` 一次，确认没有不一致（有的话先停下问 Barry），再停掉 OpenSearch，在 `backend\` 下依次执行，输出（标准输出和标准错误都要）与退出码存成 `repair-down-1.txt` 到 `repair-down-3.txt`：

```powershell
..\.venv-main\Scripts\python -m app.modules.consistency repair --fix index
..\.venv-main\Scripts\python -m app.modules.consistency repair --fix index --fix temp-files
..\.venv-main\Scripts\python -m app.modules.consistency repair --fix temp-files
```

**预期：** 第 1 条只说“没有检查索引，index 这次不会修复”，**没有**“没有需要修复的问题”，退出码 1；第 2 条另有一行“其余所选类别（temp-files）下没有需要修复的问题”，退出码 1；第 3 条只有“所选类别下没有需要修复的问题”，退出码 0。做完重新启动 OpenSearch。逐条一致才判为通过。

### 17.18 界面更新：失败原因、任务面板、中英文与配色、检索动效（T24ba–T24be，2026-11-25 添加）

**为什么：** T24ba–T24be 在 Mac 上只对着“真实 FastAPI 应用 + SQLite 替身”检查过：任务状态是脚本改的，检索结果是注入的，没有真实的 PostgreSQL、Worker、OpenSearch、CLIP、OCR（`docs/untested.md` 第 4 节“T24ba–T24be”）。W4 的界面结果基于改动前的界面，本节一并重测。

**准备：** 接着第 17.6 节，用 W4 的 `docmgr_ui`（前缀 `ui_`）、`npm run dev` 的前端，界面语言先用中文、默认配色。账号要三个：普通用户 A、普通用户 B、管理员。截图存到 `output/windows-w9/ui/`（`01.png` 起编号，一步多张时 `01a.png`、`01b.png`），网络记录存成 HAR。

生成两个样本（放在仓库外的目录，不提交；口令是测试用的）：

```powershell
Set-Content -Encoding utf8 "<仓库外的目录>\make_ui_samples.py" -Value @'
import pathlib, sys
import pymupdf
d = pathlib.Path(sys.argv[1])
doc = pymupdf.open(); doc.new_page().insert_text((72, 100), "x")
doc.save(d / "locked.pdf", encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="test-pw", owner_pw="test-owner")
s = pymupdf.open()
for i in range(6):
    t = pymupdf.open(); p = t.new_page(width=600, height=800)
    p.insert_text((60, 120), f"W9 sample page {i + 1}", fontsize=40)
    q = s.new_page(width=600, height=800); q.insert_image(q.rect, pixmap=p.get_pixmap(dpi=150))
s.save(d / "scan6.pdf", deflate=True)
'@
.venv-main\Scripts\python "<仓库外的目录>\make_ui_samples.py" "<仓库外的目录>"
```

| # | 操作 | 预期 |
|---|---|---|
| 1 | 停掉 CLIP 服务，A 上传一张图片，打开它的“处理详情”等着，直到图像向量失败（T24ad 的间隔，约 2 分半） | 等待期间显示“第 n/3 次失败，等待再次处理”和原因；最后是“失败”“已尝试 3/3 次”“原因：CLIP 服务连接失败（…）”。图片能正常预览，预览页有黄色提示“图像向量生成失败，图像语义检索暂时搜不到这张图片。” |
| 2 | 启动 CLIP 服务，点“重试失败项” | 提示“已放回队列 1 项，等待处理”；Worker 日志里**几秒内**就领走（不等 30 秒）；成功后提示自己消失。开图像通道能搜到这张图片 |
| 3 | A 上传 `scan6.pdf`，启动一个 OCR Worker，有 2 页成功后按 Ctrl+C 停掉；新窗口设 `$env:OCR_WORKER_TASK_TIMEOUT_SECONDS = "0.2"` 再启动，等其余页都失败（约 3 分钟；如果还能成功就改成 0.05），停掉并关掉这个窗口。用原来的设置启动 OCR Worker，打开预览页的“抽取文本”停在那里，点“重试失败项” | 失败时提示“6 项 OCR 识别中有 n 项失败……”，详情里是“共 6 项：成功 a，失败 n”“原因：识别超时（超过 0.2 秒），已终止（n 项）”。重试后标题旁显示“OCR 识别进行中：x/6”；有页完成后出现“OCR 有新的识别结果 点此刷新”，**点了才更新**，不自己跳动；全部完成后提示消失。检索 `sample` 能搜到 |
| 4 | A 上传 `locked.pdf` | 列表显示“解析失败”和“查看原因”；详情是“已尝试 1/3 次”“原因：PDF 已加密，需要口令才能读取，无法解析”和“系统判定重试无用……”。预览页的“抽取文本”写“文件解析失败，没有抽取文本” |
| 5 | A 把 `locked.pdf` 共享给 B。模拟一个没有预料到的错误：`Q 'docmgr_ui' "UPDATE processing_tasks SET error = 'FileNotFoundError: [Errno 2] No such file or directory: ''C:\srv\docmgr\a.pdf''' WHERE task_type = 'parse' AND document_id = '<它的 id>'"`（只改这个测试库）。A、B、管理员各打开一次处理详情，并把 `GET /api/documents/<id>/tasks` 的应答存成 `tasks-a.json`、`tasks-b.json`、`tasks-admin.json` | A、B 看到“原因：系统内部错误（FileNotFoundError）”，两个应答里**都没有** `srv`；B **没有**重试按钮，提示“只有文件的上传者和管理员可以重试”；管理员看到原文（T24ba） |
| 6 | A 在 `locked.pdf` 的处理详情里点“重试”，立刻点侧栏“检索”，在检索页停 30 秒看网络面板 | 离开之后没有 `/api/documents` 和 `/tasks` 的请求；回到文件页状态正确（T24bb、T24bd） |
| 7 | 网络限速 Slow 3G，文件页快速依次点“共享给我的”“我上传的” | 最后显示的是“我上传的”文件，与选中的按钮一致（T24bb） |
| 8 | 文件列表 → 打开文件甲 → 返回列表 → 打开文件乙；在浏览器的后退按钮上长按（或右键），直接选甲那一条 | 地址和页面内容都是甲（T24bb） |
| 9 | 同第 17.6 节第 8 步，把令牌有效期设为 60 秒重启后端；A 登录并打开检索页，停掉后端，刷新检索页（显示“登录状态已保留”）；等到登录满 70 秒，启动后端。先在表单里填好 B 的用户名和密码，限速 Slow 3G，点“重试”后马上按回车登录 | 进入的是 B，没有被退回登录页，本地令牌还在；再点几个页面都正常（T24bb）。做完用原来的设置重启后端 |
| 10 | 检索页：① 快速改词并连按回车；② 连点“检索”按钮三下；③ 检索中改一次开关（都在 Slow 3G 下做） | 检索中扫描区写“正在检索…”，结果到了写“正在整理结果…”，没有文件计数（T24bh）。① 只显示最后一个词的结果，前面的请求是 canceled；② 只有 1 条 `POST /api/search`；③ 同第 10.2 节第 8 项的新预期 |
| 11 | 停掉 OpenSearch 后检索；启动后点扫描区的“重试” | 红色“检索服务暂时不可用”，**不是**“没有找到匹配的文件”；重试后正常显示结果 |
| 12 | 打开检索页，按 Tab 把焦点移到右下角“EN”，停 5 秒等启动动画重新播放，按回车 | 语言切换为英文，焦点仍在“EN”上，没有跳到检索框；再点“中”切回 |
| 13 | 切到 English，把登录页、文件页、共享对话框、删除确认框、处理详情、预览页、检索结果看一遍；切回中文 | 除了后端返回的文字（失败原因等）、文件名、正文和按钮“中”，没有中文；分页、确认框也跟着切换；没有文字溢出或被截断 |
| 14 | 配色：选靛紫 + 深色，看文件页、处理详情、检索结果、预览页；按 F5；再点“恢复默认” | 文字都看得清；刷新后保持；恢复默认后与原来的海蓝浅色一致 |
| 15 | 窗口宽约 1280、768、375 各一次，文件页（20 条以上）、预览页、检索结果都滚到底 | 右下角的语言、配色按钮不压住分页和其他按钮，没有横向滚动条 |
| 16 | Windows 设置 → 辅助功能 → 视觉效果 → 关闭“动画效果”，刷新登录页和检索页；做完改回 | 没有启动动画，logo 和待机只有静止画面；检索可用，结果正常 |
| 17 | `npm run build` 后 `npm run preview`，打开 `/motion-lab` | 回到首页或登录页；`dist\assets` 里没有 `MotionLabView`（开发模式下能打开，是正常的） |
| 18 | 第 10–15 步在 Chrome、Edge 各看一遍，装了 Firefox 的话也看；按第 10.5 节的清单重截论文用的图，另加：处理详情、预览页失败提示、英文界面、深色界面各一张 | 报告里写明浏览器版本；新图放 `docs/screenshots/windows-<执行日期>-t24b/` |

**Claude 怎么判断：** 对照截图和网络记录逐条看；第 2 步的领取时间读 Worker 日志；第 5 步在三个应答里搜 `srv`；全部符合，才从 `docs/untested.md` 删掉“T24ba–T24be”的对应行。30 秒检索超时、低配机器的帧率、读屏软件、中文输入法组字时按回车不在本节，仍是未测试。

### 17.12 验收标准

- [ ] 17.2：`git-head.txt` 的提交包含 T24z；`mapping-eol.txt` 三行 LF、hash 与 Mac 一致；前端三项命令的输出都在；`sampler-selftest.csv` 相邻采样间隔不超过 3 秒
- [ ] 17.3：四步耗时与设定值相差不超过 2 秒，都报 `ConnectionTimeout`、退出码 1
- [ ] 17.4：`index-before.txt`、`index-after.txt`、`git-status-before-runs.txt`、`w9-runs.zip`（8 个目录）都在；R1 与 R2 逐条相同；指标与 W3 相差不超过 0.01
- [ ] 17.5（修复之后）：A、B 两个任务都是 `succeeded`、`attempts = 1`，退出码都是 130，日志里没有 `InterruptedError`、`KeyboardInterrupt`；C 的两个 Worker 强制结束 3 秒后子进程都不在，任务 `succeeded`、`attempts = 2`，没有重复的 OCR 任务；D 的循环在按 Ctrl+C 后结束、没有重新拉起
- [ ] 17.6：11 步都有截图和网络记录（第 11 步的网络记录里能数出登录请求的条数），结果逐条对照了预期
- [ ] 17.18：18 步都有截图，第 2、3、5、6、7、9、10 步有网络记录，第 5 步有接口应答原文；结果逐条对照了预期；新截图在 `docs/screenshots/windows-<日期>-t24b/`
- [ ] 17.7：三张截图和 `drag.har`
- [ ] 17.8：15 个 CSV 和 `memory.csv`
- [ ] 17.9：backend 6 passed、shared 2 passed，`symlink-priv.txt` 在
- [ ] 17.10：样本、`sources.csv`、三个 JSON、原文件、4 段人工抄录都交回
- [ ] 17.11：`missed30-answers.tsv` 填完 30 行
- [ ] 全程没有改代码和配置文件；`output/windows-w9/` 有 `git-head.txt`、`commands.txt`、`SHA256SUMS.txt`

### 17.13 怎样算测试成功

仍按第 0.5 节的三条判定。本节里有通过或失败之分的是 17.3、17.4、17.5、17.6、17.7、17.9、17.18；其余是测量或样本，**数据完整、来源可查就算完成**，结论由 Claude 核对后写进核对记录和 `docs/untested.md`。哪一项做不到，写明卡在哪里，继续做不依赖它的部分。**SHA-256 请对仓库里提交的文件算**（提交之后再算，或者统一换成 LF 后再算）：第二轮有 291 个文本文件的 hash 是对 CRLF 签出的工作区文件算的，Claude 要先换成 CRLF 才能对上。

------------------------------------------------------------------------

## 18. W10：W9 之后的修复（T24ah–T24aj）与剩下的补测（2026-11-26 添加）

来源：W9 核对（`docs/changes/windows-2026-11-26-核对.md`）发现的 Bug 1、Bug 2、`git_dirty`，Mac 上已由 T24ah、T24ai、T24aj 修好（修改记录 `docs/changes/T24ah.md`、`T24ai.md`、`T24aj.md`），都还没在 Windows 上跑过；另有 W9 没做完的第 17.6 节第 3a 步和第 17.9 节 backend 6 项。规则同 W9：只测量和核对，不改代码和配置文件；环境变量只在窗口里临时设；结果与预期不符时，记下现象和完整输出，问 Barry。原始数据放进 `output/windows-w10/`，报告写进 `output/windows-w10/summary.txt`。第 17.7、17.10、17.11 节（Barry 本人）不变，不在本节重复。

### 18.1 执行顺序

| 顺序 | 内容 | 谁做 | 依赖 | 预计耗时 |
|---|---|---|---|---|
| 1 | 第 18.2 节：拉取、确认基线 | GPT | — | 10 分钟 |
| 2 | 第 18.3 节：backend 全套测试（含集成测试） | GPT | 1 | 40 分钟 |
| 3 | 第 18.4 节：backend 6 项符号链接测试 | GPT 或 Barry | 1 | 10 分钟 |
| 4 | 第 18.5 节：数据库停掉时的接口与命令行（Bug 1 重测，含第 17.6 节第 3a 步） | GPT | 1 | 40 分钟 |
| 5 | 第 18.6 节：`git_dirty` | GPT | 1 | 10 分钟 |
| 6 | 按第 14.1 节整理 `output/windows-w10/`、提交；Barry 推送 | GPT、Barry | 全部 | 20 分钟 |

### 18.2 基线

1. `git pull`，确认是快进。`git log --oneline | Select-String "T24ah|T24ai|T24aj"` 要能各找到一条。提交号按第 14.1 节的格式写进 `output/windows-w10/git-head.txt`。
2. 先 `New-Item -ItemType Directory -Force output\windows-w10`（重定向不会自己建目录）。

### 18.3 backend 全套测试

**为什么：** T24ah 改了 `make_engine()` 的参数，集成测试的夹具 `tests/integration/conftest.py` 和 Alembic 迁移入口 `app/db/migrations/env.py` 都跟着改了，Mac 上没有 PostgreSQL，没跑过；T24ai 改写了 W9 里在 Windows 上失败的 `test_database_address_is_hidden`。

1. 按第 12.2 节的做法，在 `backend/` 下设好 `TEST_DATABASE_URL`（指向空的 `docmgr_test`），跑全套 pytest，JUnit 存成 `output/windows-w10/backend.xml`，并导出 `backend-collect.txt`。**`--basetemp` 指定的目录要先建好**（W9 的 6 项符号链接就是因为它不存在才没跑起来）：

   ```powershell
   New-Item -ItemType Directory -Force w10-data\pytest-tmp-backend
   ..\.venv-main\Scripts\python -m pytest --basetemp=..\w10-data\pytest-tmp-backend --junitxml=..\output\windows-w10\backend.xml
   ```

   `w10-data\` 放在仓库根目录下、不提交（和 W9 的 `w9-data\` 一样）；路径按自己的实际位置改，关键是目录事先存在。
2. 同样在 `backend/` 下跑 ruff：`ruff check . ; ruff format --check .`，输出存成 `ruff.txt`。

**预期：** 0 failed、0 skipped（这次符号链接的 6 项也应通过；如果仍因权限失败，记下来，不影响其余判断）。共 1056 项（Mac 上收集的数），比 W9 的 1052 项多 4 项（T24ah 3 项：`test_auth_api.py::test_database_that_never_answers_gives_503_within_timeout`、`test_db_session.py::test_engine_passes_connect_timeout_to_psycopg`、`test_db_session.py::test_connect_timeout_is_required`；T24aj 1 项：`test_experiment_framework.py::test_git_dirty_ignores_untracked_files`），以 `backend-collect.txt` 为准。`test_task_errors.py::test_database_address_is_hidden` **必须通过**（它不再连网络）。ruff 通过。

### 18.4 backend 6 项符号链接测试（改良第 17.9 节）

W9 里 `whoami /priv` 已经能看到 `SeCreateSymbolicLinkPrivilege`，shared 的 2 项通过；backend 的 6 项是因为 `--basetemp` 目录不存在（`WinError 3`）没跑起来。第 18.3 节的全套测试已经包含这 6 项；如果那里因为别的原因没跑成，就单独跑：

```powershell
# 仓库根目录
New-Item -ItemType Directory -Force w10-data\pytest-tmp-symlink
whoami /priv | Select-String SeCreateSymbolicLink | Out-File -Encoding utf8 output\windows-w10\symlink-priv.txt
# backend/ 下（命令即第 12.3 节的那条，只多了 --basetemp）
..\.venv-main\Scripts\python -m pytest --basetemp=..\w10-data\pytest-tmp-symlink --junitxml=..\output\windows-w10\symlink-backend.xml "tests/unit/test_consistency.py::test_symlinks_are_never_treated_as_stored_files" "tests/unit/test_storage.py::test_file_symlink_pointing_outside_rejected" "tests/unit/test_storage.py::test_directory_symlink_pointing_outside_rejected" "tests/unit/test_storage.py::test_put_refuses_to_write_through_directory_symlink" "tests/unit/test_storage.py::test_symlinked_temp_directory_refused_at_startup"
```

**预期：** 6 passed（`test_directory_symlink_pointing_outside_rejected` 有两个参数）。执行方的沙箱账号仍然建不了符号链接时，交给 Barry 在自己的终端里跑同一条命令。

### 18.5 数据库停掉时的接口与命令行（T24ah，Bug 1 重测）

**为什么：** W9 第 17.6 节第 3a 步：后端开着、PostgreSQL 停掉，`/api/auth/me` 超过 90 秒不返回。T24ah 给后端的数据库连接加了超时（新配置 `DATABASE_CONNECT_TIMEOUT_SECONDS`，默认 5 秒，见 `.env.example`），超时后返回 503 `DATABASE_UNAVAILABLE`；四个命令行工具和 `alembic` 也用这个超时。通用 Worker 处理任务时用 `WORKER_DB_CONNECT_TIMEOUT_SECONDS`（默认 10）。Mac 上连被拒绝的端口会立刻失败，测不出原来的问题，只用“只接受连接、从不回应”的端口在单元测试里复现过。

用 W9 第 17.6 节的那一套（`docmgr_ui`、`npm run dev` 的前端、管理员账号）。截图存到 `output/windows-w10/dbdown/`，每一步的完整输出存成 `dbdown-<步骤>.txt`，耗时和退出码汇总到 `dbdown.json`。

| # | 操作 | 预期 |
|---|---|---|
| A | 后端、PostgreSQL 都开着，用第 12.6 节第 3 步的写法登录拿到 `$tok`；然后停掉 PostgreSQL 服务，计时请求一次：`Measure-Command { try { Invoke-WebRequest -Uri http://127.0.0.1:8000/api/auth/me -Headers @{Authorization="Bearer $tok"} -TimeoutSec 120 } catch { $_.Exception.Response.StatusCode.value__; $_.ErrorDetails.Message } }` | 返回 503，正文 `code` 为 `DATABASE_UNAVAILABLE`；耗时约 5 秒，**不超过 15 秒**（连接池先检查旧连接、再新建连接，最坏可能各等一次超时） |
| B | 同样停着 PostgreSQL，重复 A 的请求 3 次 | 每次都是 503，耗时都在 15 秒以内；记下 3 次的耗时 |
| C | 第 17.6 节第 3 步（即 W9 的 3a）：浏览器里刷新文件页 | 保留令牌，显示“暂时连不上服务器，登录状态已保留……”；再清掉令牌打开 `/login`：显示 T24z 的“后端已启动，但数据库不可用……”。记下打开页面到提示出现大约几秒（预期 15 秒以内） |
| D | 第 17.6 节第 4 步：启动 PostgreSQL，点“重新检查” | 提示消失；再请求一次 A，返回 200 |
| E | 新开一个窗口，设 `$env:DATABASE_CONNECT_TIMEOUT_SECONDS = "2"`，在这个窗口重启后端；停掉 PostgreSQL，重复 A | 503，耗时约 2 秒，不超过 6 秒。做完关掉这个窗口，用原来的设置重启后端 |
| F | PostgreSQL 停着，在 `backend/` 下计时运行 `python -m app.modules.consistency check` 和 `alembic current`（窗口里的变量指向 `docmgr_ui`、`ui_`） | 两条都在 15 秒内结束，退出码非 0，提示数据库连不上，不挂着 |
| G | 做完启动 PostgreSQL，`python -m app.modules.consistency check` | 退出码 0，和停机前一样 |

**Claude 怎么判断：** A、B、E 的状态码与耗时，C 的截图与耗时，F 的退出码与耗时。都符合，才从 `docs/untested.md` 第 7.5 节删掉 Bug 1 一行的“未测试”部分，并在 DEVPLAN 的 T24ah 记录里写上 Windows 结果。

### 18.6 `git_dirty`（T24aj）

**为什么：** W9 里 `output/` 下的未跟踪目录让实验记录的 `git_dirty` 每次都是 true。T24aj 改为只看已跟踪文件。

1. 在仓库根目录：`git status --porcelain` 和 `git status --porcelain --untracked-files=no` 的输出分别存成 `git-status-all.txt`、`git-status-tracked.txt`。预期：前者有 `??` 开头的行（至少有 `output/windows-w10/`），后者为空。如果后者不为空，说明有已跟踪的文件被改过，先记下来、问 Barry，不要自己还原。
2. 在 `backend/` 下：`..\.venv-main\Scripts\python -c "from app.modules.experiments.environment import machine_info; print(machine_info()['git_dirty'])"`，输出存成 `git-dirty.txt`。预期：后者为空时打印 `False`。
3. 如果这次顺便跑了任何实验（不要求专门跑），打开结果目录里的 `config.json`，`machine.git_dirty` 应为 `false`。

### 18.7 验收标准

- [ ] 18.2：`git-head.txt` 的提交包含 T24ah、T24ai、T24aj
- [ ] 18.3：`backend.xml` 0 failed、0 skipped，`test_database_address_is_hidden` 通过，新增的 4 项都在且通过；`backend-collect.txt`、`ruff.txt` 在
- [ ] 18.4：backend 6 项符号链接 passed（在 18.3 里或单独跑），`symlink-priv.txt` 在
- [ ] 18.5：A–G 都有输出或截图，`dbdown.json` 有每一步的耗时和状态码（或退出码）
- [ ] 18.6：`git-status-all.txt`、`git-status-tracked.txt`、`git-dirty.txt` 都在
- [ ] 全程没有改代码和配置文件；`output/windows-w10/` 有 `git-head.txt`、`commands.txt`、`SHA256SUMS.txt`（SHA-256 的算法同第 17.13 节）

### 18.8 怎样算测试成功

仍按第 0.5 节的三条判定。有通过或失败之分的是 18.3、18.4、18.5、18.6。哪一项做不到，写明卡在哪里，继续做不依赖它的部分。
