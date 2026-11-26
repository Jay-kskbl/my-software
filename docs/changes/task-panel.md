# 修改记录：任务状态与重试（2026-11-23）

- 来源：2026-11-23 前端评估。后端有任务查看、重试接口，前端没有界面；`decisions.md` D8 写“用户要在任务列表里查看”，但列表不存在
- 分支：`feat/search-motion`（克隆库）。Barry 于 2026-11-23 批准 P1–P4，决定在克隆库做，不进主仓库的 DEVPLAN，也不同步到主仓库
- 每个任务一个提交；提交编号补在本文件，单独提交
- 没有新依赖，没有改表结构、索引、配置

| 编号 | 内容 | 状态 | 提交 |
|---|---|---|---|
| P1 | 后端清理任务失败原因，原文只给管理员看 | 完成 | `5409181` |
| P2 | 前端任务逻辑（汇总、重试、轮询）与单元测试 | 完成 | `9519053` |
| P3 | 处理详情对话框，接入文件列表 | 完成 | `b2c5905` |
| P4 | 预览页提示条与自动刷新 | 完成 | `6af9c44` |
| P5（未批准） | 任务接口增加 `locator`，显示具体失败页码 | — | — |
| P6（未批准） | 管理员任务页 | — | — |

------------------------------------------------------------------------

## P1 后端清理任务失败原因

### 为什么

Worker 把异常原文存进 `processing_tasks.error`，任务接口原样返回，文档的 owner 和被共享者都能看到。没有预料到的异常会带出内部信息，按 Worker 的拼法实测：

- `FileNotFoundError: [Errno 2] No such file or directory: '/srv/docmgr/storage/…'`（服务器路径）
- `OperationalError: … connection to server at "127.0.0.1", port 1 failed`（数据库地址）

加界面之前接口已经是这样；加了界面会直接显示出来，所以先改后端。只在前端隐藏不算修好。

### 修改的文件

| 文件 | 改了什么 |
|---|---|
| `backend/app/modules/documents/task_errors.py`（新增） | `public_task_error()`：只放行认得出来的写法，其余只给类型名 |
| `backend/app/modules/documents/tasks.py` | `to_task_out(user, task)`：管理员看原文，其他人看清理过的 |
| `backend/app/api/tasks.py` | 三个任务接口都改用 `to_task_out` |
| `backend/tests/unit/test_task_errors.py`（新增） | 42 项 |
| `backend/tests/integration/test_documents.py` | 新增 1 项（owner、被共享者、管理员分别看到什么），**未运行** |
| `docs/api.md` §5.1 | 说明 `error` 的规则 |

### 关键设计

- 默认不放行：新增的异常没登记，后果是说明不够详细，而不是泄露。
- 检索服务的错误只保留到 HTTP 状态码。OpenSearch 的原因文字可能带节点名和内网地址（`[node-1][172.18.0.2:9300]`）。
- OCR 模型加载失败只保留前半句，后半句是内部异常，可能带模型目录。
- 数据库里的原文不变，排查问题不受影响。接口字段不变，只是 `error` 的文字变了。

### 验证

- 后端全量：763 通过、230 跳过（改之前 721 通过、229 跳过）。用主仓库的 `.venv-main` 运行克隆库的代码，没有写主仓库
- 变异检查：把 `to_task_out` 改成总是返回原文，`test_ordinary_user_gets_the_cleaned_reason` 失败
- `ruff check`、`ruff format --check` 通过
- **未测试（Not Tested）：** 新增的集成测试，本机没有 PostgreSQL

------------------------------------------------------------------------

## P2 前端任务逻辑与单元测试

### 修改的文件

| 文件 | 内容 |
|---|---|
| `frontend/src/api/types.ts` | 新增 `TaskType`、`Task` |
| `frontend/src/api/tasks.ts`（新增） | `listDocumentTasks`、`retryTask` |
| `frontend/src/features/tasks/summary.ts`（新增） | 按类型汇总成步骤：状态、计数、失败原因合并、等待重试、用时 |
| `frontend/src/features/tasks/retry.ts`（新增） | 批量重试：最多同时 4 个；409 `TASK_NOT_RETRYABLE` 算跳过；网络不通、401、403、5xx 时停下，不再一个个失败下去 |
| `frontend/src/features/tasks/watcher.ts`（新增） | 有没结束的任务就每 3 秒刷新；换文档、刷新、停止时取消旧请求，迟到的响应丢弃 |
| `frontend/tests/tasks/`（新增 3 个文件 + 公共数据） | 43 项 |
| `frontend/tests/client.test.ts` | 新增 3 项（两个接口的地址、方法、错误码） |

### 关键设计

- 逻辑都是纯 TypeScript，不依赖 Vue，项目里没有组件测试工具也能测。
- 一个文档只在上传时建一个 parse 任务（核对过 `documents/service.py`、`worker/handlers/parse.py`），重试用的是同一条记录，所以不需要处理“旧的失败、新的成功”。
- “失败但次数没用完”等于后端判定重试无用（`retryable=False`），用来给出提示；次数恰好用完时分不出来，按可以再试处理。
- 轮询出错时，只要上一次还有没结束的任务就继续试；第一次就失败则停下，由用户点刷新。

### 验证

类型检查通过；前端 25 个文件 301 项测试通过（原 22 个文件 255 项）。

------------------------------------------------------------------------

## P3 处理详情对话框，接入文件列表

### 修改的文件

| 文件 | 内容 |
|---|---|
| `frontend/src/features/tasks/TaskDialog.vue`（新增） | 处理详情：每个步骤的状态、说明、失败原因、重试按钮。只负责显示 |
| `frontend/src/features/tasks/useDocumentTasks.ts`（新增） | 加载、自动刷新、重试；离开页面即停。文件列表和预览页（P4）共用 |
| `frontend/src/features/tasks/text.ts`（新增） | 步骤名、说明、重试结果的文字 |
| `frontend/src/features/tasks/summary.ts` | 加 `parseStatus` |
| `frontend/src/views/DocumentsView.vue` | 状态标签改成按钮，点开处理详情；解析失败的多一行“查看原因”；重试后、解析状态变化后刷新列表 |
| `frontend/src/i18n/messages.ts` | 新增 `tasks.*`（中英文）；列名“处理状态”改“解析状态”，“处理成功 / 失败”改“已解析 / 解析失败”等 |
| `frontend/tests/tasks/text.test.ts`（新增）、`summary.test.ts`、`format.test.ts`、`i18n.test.ts` | 新增 25 项，改 3 处旧文字 |

### 关键设计

- 列名和状态文字改成“解析”：文档状态只跟随解析任务（D27），写“处理成功”会让人以为 OCR 也完成了。只改界面文字，接口取值不变。
- 被共享者能看不能重试，没有重试按钮；后端本来就返回 403。
- 失败原因来自后端，切到英文仍是中文，与其他后端文字相同。
- 没有新注册的 Element Plus 组件，没有新依赖。
- 同时只有一批重试（`singleFlight`）；重试途中离开页面，不再让列表去加载数据、排定时器。

### 验证

- 类型检查通过；前端 26 个文件 326 项测试通过；生产构建通过
- 浏览器（生产构建 + 临时模拟后端，没有提交）：部分失败、解析失败、向量失败、等待重试、没有记录、被共享者；重试成功后自动刷新到成功；连点两下只发一遍；40 项失败时并发峰值 4；403、503 只发 4 个就停；409 全部算跳过；加载失败后点刷新恢复；慢请求没返回就换文件，显示的是新文件；关闭后 7 秒内没有再请求；Enter 打开、Esc 关闭、焦点回到原按钮；375 px 宽没有横向溢出

------------------------------------------------------------------------

## P4 预览页提示条与自动刷新

### 修改的文件

| 文件 | 内容 |
|---|---|
| `frontend/src/views/PreviewView.vue` | 失败提示条（重试失败项、查看详情）；“处理详情”按钮；标题旁显示 OCR、向量的进度；解析完自动更新状态和抽取文本；OCR 有新结果时提示“点此刷新” |
| `frontend/src/features/tasks/changes.ts`（新增） | 什么时候要重新取文档、有没有新的 OCR 结果（纯函数） |
| `frontend/src/features/tasks/text.ts` | 加失败提示、进度的文字 |
| `frontend/src/components/ExtractedText.vue` | 对外提供 `reload()`：重新加载当前页，不滚动 |
| `frontend/src/i18n/messages.ts` | 新增 `tasks.*` 10 条、`preview.parseFailed`（中英文） |
| `frontend/src/features/tasks/TaskDialog.vue`、`frontend/src/views/DocumentsView.vue` | 提示文字改用正文颜色，原来的橙字、红字对比度不够 |
| `frontend/README.md`、`docs/untested.md` | 目录说明；登记未测试项 |
| `frontend/tests/tasks/changes.test.ts`（新增）、`text.test.ts` | 新增 18 项 |

### 关键设计

- 不能用“文档状态 ≠ 解析任务状态”判断要不要重新取文档：解析失败等待重试时，任务是 `pending`、文档是 `processing`（D27），两者本来就不同，那样每 3 秒都会多取一次。改为比较前后两次的解析任务状态，另外处理“取文档和取任务之间刚好解析完”。
- OCR 有新结果时只提示不自动刷新，不打断阅读；没打开过抽取文本的不提示。
- 任务没加载出来时只在标题旁说明，不影响看原文件。
- 解析失败时，抽取文本原来写“文件还没有处理完成”，改为“文件解析失败，没有抽取文本”。

### 验证

- 类型检查通过；前端 27 个文件 344 项测试通过；生产构建通过；新增代码没有写死色值
- 浏览器（同 P3）：OCR 部分失败 → 重试 → 进度 10/12 → 完成后出现“有新的识别结果”，点了才重新加载（自动 0 次、点击 1 次）；解析中的 Excel 解析完后自动显示抽取文本，轮询 7 秒期间没有多取文档；解析失败 → 重试 → 等待解析 → 已解析 → 文本自动出现；被共享者只有“查看详情”；任务接口 503 时原文件照常显示；离开页面后 7.5 秒没有再请求；375 px 没有横向溢出；英文界面正常
- 对比度：提示条文字浅色 12.1:1、深色 13.0:1；对话框提醒 13.0:1、15.3:1；说明文字 6.1:1、12.3:1

## 总体未测试（Not Tested）

见 `docs/untested.md`“任务状态与重试 P1–P4”：真实后端联调、P1 集成测试、上百页扫描件、管理员原文、其他浏览器与读屏软件、组件自动化测试。
