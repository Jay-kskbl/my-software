# 开发流程与任务清单（DEVPLAN.md）

> 本文件是 GLOBAL.md v2 的执行计划，也是项目进度的唯一记录。
> Claude Code 每次开始任务前读取本文件，完成任务后勾选并写一行完成记录。
> 周次为相对周（W1 = 开工第一周），实际日期由 Barry 确认后填在 §5。

------------------------------------------------------------------------

## 1. 在 Claude Code 中的工作循环

### 1.1 一次性准备（W1 第 1 天）

```bash
cd ~/Desktop/"BARRY zou"
git init
claude          # 在项目根目录启动 Claude Code
```

根目录下的 `CLAUDE.md` 会被 Claude Code 自动读取，其中已经引用了 `GLOBAL.md`。
`.claude/commands/` 下有两个自定义命令：`/next-task`、`/finish-task`。

### 1.2 每个任务的固定循环

```
① /clear                 每个任务开新上下文，避免上一个任务的内容干扰
② /next-task             Claude 读 DEVPLAN，找到下一个未完成任务，读相关代码，给出计划
③ 审计划                  涉及数据契约、数据库表、索引结构的任务，先切到 Plan 模式（Shift+Tab）只出计划
④ 批准 → 实现             Claude 小步修改、写测试、跑测试
⑤ 自己验证一次            按 Claude 给的命令亲手跑一遍（答辩时你要能讲清楚）
⑥ /finish-task           Claude 按 GLOBAL §11.3 汇报、勾选 DEVPLAN、自动 commit 并补填 commit 编号
⑦ 一个任务一个 commit      不 push；里程碑打 tag（mvp-0、mvp-1、mvp-2）由你确认
```

### 1.3 和 Claude Code 协作的规则

-   **一次只做一个任务编号。** 想加功能，先在 §4 "待议事项"里记一笔，不在当前任务里顺手做。
-   **先看计划再放权。** 带 🔒 的任务必须先出计划、你批准后才能写代码。
-   **测试是完成标准。** Claude 报告里写"未运行"的测试，不算完成。
-   **决策变更走附录 A。** 任何与 GLOBAL.md 附录 A 冲突的建议，Claude 必须先停下来问你。
-   **卡住超过两轮就换方式：** 让 Claude 先写一个最小复现测试，再修。
-   **你要能讲清楚每一块。** 每个里程碑后，让 Claude 用 5 句话解释该模块的设计，你复述一遍。这是答辩准备。

------------------------------------------------------------------------

## 2. 仓库结构（T01 建立）

```
BARRY zou/
├── CLAUDE.md  GLOBAL.md  DEVPLAN.md
├── .claude/commands/          next-task.md  finish-task.md
├── docs/                      architecture.md  data-model.md  api.md  env_report.md  decisions.md
│                              untested.md（未测试清单）  downloads.md（下载与安装记录）
├── env_check/                 阶段一环境实测脚本
├── shared/                    【所有环境共用】数据契约(§3.5)、ID 规则、任务领取库、切分(M7)、文本索引(M8)、存储路径检查 —— 依赖 pydantic + psycopg + httpx（T17 起）
├── backend/                   【main 环境】
│   ├── app/
│   │   ├── main.py  config.py
│   │   ├── api/               路由：auth / documents / search / tasks / health
│   │   ├── core/              安全、错误类型、日志
│   │   ├── db/                SQLAlchemy 模型、会话、Alembic 迁移
│   │   ├── modules/
│   │   │   ├── auth/          M1
│   │   │   ├── documents/     M2
│   │   │   ├── storage/       M3
│   │   │   ├── parsing/       M5
│   │   │   ├── vector_index/  M10
│   │   │   ├── search/        M11（编排 + rrf.py）
│   │   │   └── consistency/   M13
│   │   └── worker/            通用 Worker 入口与任务处理器（M4 运行时）
│   └── tests/                 unit/  integration/  fixtures/
├── services/
│   ├── ocr_worker/            【ocr 环境】M6，独立 requirements
│   └── clip_service/          【clip 环境】M9，独立 requirements，FastAPI
├── experiments/               M12：datasets/ qrels/ configs/ runs/ metrics.py runner.py
├── frontend/                  M14：Vue 3 + TS + Element Plus
└── deploy/                    docker-compose.yml（postgres + opensearch）、.env.example
```

------------------------------------------------------------------------

## 3. 任务清单

图例：🔒 必须先出计划并获批准　⭐ 关键路径　🧪 必须包含的测试

### 阶段一：需求与方案（W1–W3）

- [ ] **T00 环境实测**（Barry 自己运行，W1）
  -   按 `env_check/README.md` 跑完 00–05，得到 `env_check/env_report.md`
  -   根据报告填写附录 A13（分词器）、A14（是否需要降级预案）、OCR/CLIP 模型规格
  -   完成标准：报告 §6 的决策全部填写
- [x] **T01 仓库骨架** ⭐
  -   按 §2 建目录；`backend/pyproject.toml`（ruff + pytest）；`.gitignore`（含 `.venv-*`、`models/`、`storage/`、`.env`）
  -   `deploy/docker-compose.yml`：PostgreSQL + OpenSearch（分词插件按 T00 结论）
  -   `config.py`：从环境变量读取，启动时检查必填项并给出可读错误；`.env.example`
  -   `GET /health`：分别报告数据库、OpenSearch、CLIP 服务的状态（不可用时如实报告，而不是报错退出）
  -   🧪 缺失必填配置时启动失败且错误信息明确
- [x] **T02 数据契约** 🔒⭐
  -   `shared/contracts`：`ParsedDocument`、`TextBlock`、`SourceLocator`（四种类型）、`Chunk`、`OCRResult`、`SearchHit`、`ChannelResult`
  -   `shared/ids`：`chunk_id`、`image_id` 生成与解析函数
  -   🧪 每种 locator 的序列化往返；ID 生成确定性（同输入同输出）
- [x] **T03 数据库模型与迁移** 🔒⭐
  -   SQLAlchemy 模型：User、Document、DocumentShare、Tag、DocumentTag、ProcessingTask、DocumentChunk、ImageAsset、OCRResult、ImageEmbedding、SearchLog、ExperimentRun
  -   Alembic 初始迁移；`docs/data-model.md`（ER 图 + 字段说明）
  -   🧪 迁移能在空库上升级、降级
- [x] **T04 设计文档**
  -   `docs/architecture.md`（分层图、模块表、数据流，可直接取自 GLOBAL §3.2）
  -   `docs/api.md`（接口清单：路径、方法、权限、请求/响应结构、错误码）
  -   `docs/decisions.md`（把附录 A 和 T00 结论落成文字，论文可直接引用）
  -   **里程碑：方案评审** —— Barry 通读 docs/，确认后进入阶段二

**并行准备（W2 起）：** 开始收集评测文档。目标规模先定为 200–500 个文件，覆盖 PDF（含扫描件）、Word、Excel、图片四类，记录每个文件的来源。

### 阶段二：基础系统（W4–W6）

- [x] **T05 M3 存储抽象** ⭐
  -   `put(stream) -> StoredFile(storage_key, sha256, size)`；`open(key)`；`delete(key)`
  -   先写临时文件、校验后再移动到 `{yyyy}/{document_id}/{sha256}.{ext}`
  -   文件魔数校验（不信任扩展名和 MIME）
  -   🧪 路径穿越（`../`、绝对路径、符号链接）被拒绝；中途失败不残留临时文件
- [x] **T06 M1 认证与权限**
  -   注册/登录（JWT）、密码哈希、管理员角色
  -   `current_user` 依赖；`accessible_document_ids(user)`；`can_access(user, doc)`
  -   🧪 未登录 401；访问他人文档 403；管理员可见全部；共享后可见、取消共享后不可见
- [x] **T07 M4 任务框架** 🔒⭐（全项目风险最高的基础模块，越早完成越好）
  -   `shared/tasks`：用 `FOR UPDATE SKIP LOCKED` 领取、续租、回收过期租约、重试计数、失败原因
  -   `backend/app/worker`：主循环、按任务类型分发、子进程执行（超时、内存上限）、处理 N 个任务后自动退出
  -   🧪 **崩溃恢复：** 领取后杀掉 Worker → 租约过期 → 任务被重新领取
  -   🧪 **并发：** 两个 Worker 不会领到同一任务
  -   🧪 **幂等：** 同一任务执行两次，结果不重复
  -   🧪 超过最大重试次数后标记为 `failed` 并保存原因
- [x] **T08 M2 文档管理** ⭐
  -   上传（大小、格式、文件名长度限制）→ 存储 → 写 Document → 创建 parse 任务
  -   列表（分页、只列可访问文档）、下载、软删除（创建清理任务）、共享、标签
  -   🧪 上传中途失败不留半成品；删除后列表和下载都不可见；非法类型被拒绝
- [x] **T09 M5 PDF 解析器**（可与 T05–T08 并行，纯函数）
  -   PyMuPDF 按页抽文本 → `ParsedDocument`；按页判断是否需要 OCR（阈值来自配置）
  -   🧪 fixtures：文本型 PDF、扫描型 PDF、混合型 PDF、加密或损坏的 PDF
- [x] **T10 前端骨架**
  -   登录页、文件列表（含处理状态）、上传、下载、删除、共享
  -   **里程碑：基础系统** —— 能完整管理文件，数据库与文件存储一致，T07 的四项测试全部通过
  -   ⚠️ 里程碑状态（2026-11-14）：**未达成**。T05–T10 的代码已全部完成，但 T07 的四项测试和其余数据库集成测试共 91 项从未执行（本机没有 PostgreSQL），前端也没有与真实后端联调过。详见 `docs/untested.md`
  -   ⚠️ 更新（2026-11-16 补测，见 §5“T00–T19 补测”）：T07 四项 🧪 在内的全部数据库集成测试已在 Windows 验证副本上通过（`test_task_queue.py` 18/18，backend 728/728）。通过依赖的修复 C01–C12 已于 2026-11-17 合入本仓库（与通过测试的副本逐行一致）；本机没有 PostgreSQL，没能在本仓库上重跑这些数据库测试。前端与真实后端的浏览器联调仍未做

**并行标注（W4 起，每周 2–3 小时）：** 每周补 10–20 条查询；按文字型、视觉型、混合型分类；标注相关文件（qrels 格式见 T19）。

### 阶段三：解析、OCR 与 BM25（W7–W9）

- [x] **T11 M5 其余解析器**
  -   Word（段落级 locator）、Excel（工作表 + 单元格范围 locator）、图片（只做元数据，交给 OCR）
  -   zip 炸弹防护（解压总大小和文件数上限）、解析超时
  -   🧪 每种格式至少 2 个 fixture，外加 1 个畸形文件
- [x] **T12 M7 切分**
  -   切分长度、重叠长度由配置控制；每个 chunk 带 locator；Excel 按行组切分
  -   🧪 切分后拼接覆盖原文；locator 正确；参数变化时 `parse_version` 变化
- [x] **T13 M8 文本索引** 🔒
  -   `doc_meta`、`chunks` 两个索引的 mapping（分词器按 T00 结论），mapping 文件纳入版本管理
  -   `index_document(doc_id, chunks)`：先删除该文档的旧 `parse_version` 再写入；`delete_document(doc_id)`
  -   🧪 重复索引不产生重复数据；删除后查不到
- [x] **T14 解析流水线**
  -   parse 任务处理器：解析 → 切分 → 写 DocumentChunk → 索引 → 回写状态；需要 OCR 的页和图片创建 ocr 任务
  -   清理任务处理器：删索引 → 删文件 → 硬删除记录
  -   🧪 端到端：上传 PDF → 等任务完成 → chunks 索引中有该文档的数据
- [x] **T15 M11 检索 v1** ⭐
  -   B0 + BM25 双索引查询 → 聚合到 document_id（取最佳片段作为证据）→ **数据库二次校验** → 返回 `SearchHit`
  -   OpenSearch 故障时返回明确的错误，而不是空结果；每次检索写 SearchLog
  -   🧪 删除后立即查不到；取消共享后立即查不到；同一文件不重复出现；服务故障与"无结果"可以区分
- [x] **T16 前端检索页**
  -   搜索框、结果列表（文件名 + 命中片段高亮 + 来源位置）、PDF 用 pdf.js 打开并跳到对应页、Word/Excel 显示抽取文本
  -   **里程碑 MVP-0（打 tag `mvp-0`）：** 上传 PDF/Word → 检索 → 定位到页/段落 → 删除后搜不到（T16 完成时**未达成**，没有打 tag，原因见 §5 T16。2026-11-16 补测后：数据库与 OpenSearch 测试已通过、高亮转义已在真实 OpenSearch 上确认；剩余前后端浏览器联调，见 §4）
- [x] **T17 M6 OCR Worker** 🔒（ocr 环境）
  -   `services/ocr_worker`：只领取 ocr 任务；图片或 PDF 页 → OCRResult → 生成 `source_type=ocr` 的 chunks → 创建索引任务
  -   模型路径来自配置，缺失时启动报错；记录模型名称和版本
  -   🧪 识别生成的测试图；OCR 失败时任务标记 failed，原文件仍在
- [x] **T18 M13 一致性检查**
  -   `python -m app.modules.consistency check|repair`：对账数据库、磁盘、两个索引，输出差异；`repair` 需要显式参数才执行
  -   🧪 人为制造三类不一致，都能被检测出来
- [x] **T19 M12 实验框架 v1** 🔒
  -   `experiments/datasets/manifest.csv`（文件、类型、来源）、`qrels/*.tsv`（query_id、document_id、相关等级）、`queries.tsv`（query_id、文本、类型）
  -   `metrics.py`：P@K、R@K、nDCG@K（🧪 用手算的小例子验证）
  -   `runner.py`：读取配置（通道开关、参数）→ 调用 M11 → 保存每条查询的原始排名 → 输出指标，并按查询类型分层
  -   配置 B0、B1、B2
  -   **里程碑 MVP-1（打 tag `mvp-1`）：** 四类格式 + OCR 可检索；B0–B2 能在小标注集上跑出真实数字（T19 完成时**未达成**，没有打 tag，原因见 §5 T19。2026-11-16 补测后：OCR 全链路与 `test_experiments_db.py` 已通过，剩余阻塞只有评测数据和标注）

### 阶段四：图像检索与融合（W10–W12）

- [x] **T20 M9 CLIP 服务** 🔒（clip 环境）
  -   `services/clip_service`：启动时加载模型（路径缺失则报错）；`/health`、`/encode/text`、`/encode/image`
  -   接口返回模型名称、版本、向量维度
  -   🧪 健康检查；同一输入向量稳定；超大图片和损坏图片的处理
- [x] **T21 图片向量与 M10 向量索引**
  -   embed 任务：按 sha256 去重 → 调用 CLIP 服务 → 写 ImageEmbedding → 写入向量索引
  -   向量检索：`script_score` 精确计算 + 可访问 document_id 前置过滤
  -   🧪 过滤后只返回有权限的文档；重复图片只编码一次
- [x] **T22 M11 检索 v2 + RRF** 🔒⭐（`rrf.py` 已在 T15 提前完成，Barry 批准，见 decisions.md D28）
  -   图像通道：调用 CLIP 服务编码查询文本（设超时）→ 向量检索；超时或失败时降级，并在响应中标记该通道不可用
  -   `rrf.py`：输入各通道已聚合到文件级的排名列表，按 k 和截断深度融合；保留各通道原始排名和分数
  -   通道开关来自请求参数或实验配置
  -   🧪 RRF 用手算样例验证；关闭 CLIP 服务后检索仍然正常并带降级标记
- [x] **T23 前端 v2**
  -   结果中显示图片缩略图、命中通道标记；某通道不可用时给出提示
- [x] **T24 B3 与消融配置**
  -   B3、去掉 OCR、去掉 CLIP、只用 CLIP、RRF 不同 k 值
  -   **里程碑 MVP-2（打 tag `mvp-2`）：** 完整演示流程；关闭 CLIP 后基础检索不受影响——**未达成，没有打 tag**：数据库、OpenSearch、CLIP 的端到端联调都没做，评测数据集也还没有（与 MVP-0 相同，见 decisions.md D38）

### 插入任务（2026-11-19 Barry 批准，T25 之前做）

来源：DEVPLAN §4 的待议事项，Barry 于 2026-11-19 统一批准（见 decisions.md D39）。一次做一个，各自一个 commit。

- [x] **T24a 通用 Worker 启动时检查数据库**：启动时先连一次数据库，连不上以退出码 1 结束（与 OCR Worker 一致，GLOBAL §12）；领取循环中途断线仍然重试
- [x] **T24b `/health` 不暴露内部信息**：`detail` 只写异常类型，主机、端口、数据库用户名只写日志
- [x] **T24c OCR 参数进实验配置** 🔒：`OCR_MIN_CONFIDENCE`、`OCR_PDF_DPI` 随 OCR 结果写入数据库，实验运行时读出记进 `config.json`。涉及表结构，先给 Barry 看字段设计和迁移
- [x] **T24d `rebuild-indices --force`**：无条件强制重建，仍需 `--yes` 才执行
- [x] **T24e 文本预览按页码穿插 OCR 片段**：同一页里正文在前、OCR 在后
- [x] **T24f 预览页给 PDF、图片加“抽取文本”标签页**（Barry 于 2026-11-19 批准方案，按推荐做）：抽出公共组件 `ExtractedText.vue`；PDF、图片分“原文件 / 抽取文本”两个标签页，文本按需加载；从检索结果打开图片时默认显示抽取文本并跳到命中片段；标签页状态写进地址栏 `view=`
- [x] **T24g 运行前检查拦下混用的 OCR 模型**（Barry 于 2026-11-19 批准，来源 T24c 待议第 4 条）：数据集的 OCR 结果出现两个以上（模型名，模型版本）时报问题，默认拒绝运行，`--allow-incomplete` 放行；查询与 `config.json` 的 `ocr_models` 快照共用
- [x] **T24h 烟测脚本检查 `ocr_results.params`**（Barry 于 2026-11-19 批准，来源 T24c 待议第 2 条）：OCR 完成后直接查数据库，确认图片的识别结果记录了 `pdf_dpi`（图片为 null）、`min_confidence`、`max_pixels` 和模型标识
- [x] **T24i 重新 OCR 的命令**（Barry 于 2026-11-19 批准，来源 T24c 待议第 1 条）：`python -m app.modules.experiments reocr [--yes]` 把数据集文档当前版本的 OCR 任务放回队列，用 OCR Worker 现在的配置重新识别；不新建任务，不做“只重新切分”
- [x] **T24k Worker 连接数据库加超时**（Barry 于 2026-11-21 批准优化清单 A、B 组，第 1 项）：通用 Worker 与 OCR Worker 的数据库连接带 libpq `connect_timeout`，默认 10 秒，可配置
- [x] **T24l Worker 启动时检查数据库迁移**（优化清单第 2 项）：通用 Worker 比对 `alembic_version` 与代码里的最新迁移；OCR Worker 检查它读写的表和列是否存在；不一致时退出码 1 并提示 `alembic upgrade head`
- [x] **T24m pdf.js 资源同步检查**（优化清单第 3 项）：前端测试逐文件核对 `public/pdfjs/` 与已安装的 pdfjs-dist；新增 `npm run sync:pdfjs` 复制脚本
- [x] **T24n 文件列表的标签不再被截断**（优化清单第 4 项）：文件名单行省略、悬停看全名，标签放不下时换行
- [x] **T24o 一致性检查扩大索引结构的比较范围**（优化清单第 5 项）：字段定义比较 12 个键（含 `search_analyzer`），分析配置逐项比较；提示里写出差在哪里
- [x] **T24p Element Plus 按需引入**（优化清单第 6 项）：只注册用到的 23 个组件和对应样式；测试扫描全部 `.vue` 核对注册；首屏 JS 约 874 KB → 483 KB
- [x] **T24q 根目录 README.md**（优化清单第 7 项）：课题说明、组成、快速开始、测试、文档索引、当前状态；部署细节留给 T30
- [x] **T24r 整理零散文件**（优化清单第 8 项）：根目录的 Windows 第二轮原始说明移到 `docs/changes/`，`output/playwright/` 的截图移到 `docs/screenshots/windows-2026-11-19/`，引用同步
- [x] **T24s 前端界面优化**（Barry 2026-11-21 选定 B+A+C）：侧栏布局；文件页拖拽上传、逐个文件的上传记录、加载失败改为页内提示；检索页“检索通道”面板（四个开关、三个通道、CLIP 服务状态，改开关自动重新检索），结果卡片显示三个通道的名次和 RRF 融合分；颜色统一引用 Element Plus 变量；只改前端展示，不改后端和接口，没有新依赖
- [x] **T24t 新增 `.gitattributes`**（Barry 2026-11-21 批准，来自 W5 11.2 的待定项）：只对 `frontend/public/pdfjs/**` 设 `-text`，签出时不做换行符转换，Windows 上 `core.autocrlf=true` 时 T24m 的 sha256 比对不再因 CRLF 失败；不改全仓库的换行策略
- [x] **T24u mapping 文件固定用 LF**（Barry 2026-11-21 批准，来自 Windows 第一轮核对的发现）：`.gitattributes` 对 `shared/text_index/mappings/*.json`、`backend/app/modules/vector_index/mappings/*.json` 设 `text eol=lf`，实验记录里的 mapping hash 不再随 Windows 的 CRLF 签出而变

### 插入任务：登录页修复移植（2026-11-22 Barry 批准，T25 之前做）

来源：克隆库 `~/Desktop/BARRY zou-search-motion` 的 `feat/search-motion` 分支做过“登录页结构优化”L1–L8（计划书 `docs/登录页结构优化计划书.md`、修改记录 `docs/changes/login-page.md`，都只在那个分支上）。其中 A1–A4、B1、B2、C1、C4、C5 这几个问题在 main 上同样存在；但分支上的代码建在中英文切换和动效之上，不能直接合并。2026-11-22 Barry 批准“Approve, incl. T24z”：只把修 main 现有问题的部分移植过来，文字全部用中文，不带中英文切换、配色面板、星尘 logo（含 logo 插槽）、L7 布局和 `/motion-lab`。只改前端，不改后端、接口、表结构、附录 A，不新增依赖。一次做一个，各自一个 commit。

- [x] **T24v 跳转规则抽成纯函数，令牌过期后带原地址回登录页**（来自 L1 跳转部分、L3）：新增 `features/login/redirect.ts`（`safeRedirect` 拒绝反斜杠、控制字符、`//`、带协议和 `/login` 本身）；路由守卫、令牌失效回调、登录页都调用它；修 A2（过期后回不到原页面）、A4（已登录打开 `/login?redirect=` 一律去文件页）、B2
- [x] **T24w 拆出登录表单组件，提交流程单独成函数**（来自 L1 规则部分、L4、L5）：新增 `rules.ts`、`submit.ts`、`LoginForm.vue`、`LoginBrand.vue`，`LoginView.vue` 只留布局，卡片标题改为 `h2`；注册成功但登录失败时切回登录模式；校验结束前连按回车只发一次请求；修 A3、B1、C4
- [x] **T24x 后端连不上时保留令牌**（来自 L2）：`restoreSession` 只在 4xx 时删令牌，网络不通和 5xx 时保留、下次导航再确认；登录页显示“登录状态已保留”和“重试”；修 A1
- [x] **T24y 登录错误改在表单内显示**（来自 L6 中文部分）：新增 `errors.ts` 按错误码给出更具体的中文说明，按钮上方的错误区一直留到用户修改输入或重新提交；修 C1
- [x] **T24z 打开登录页时检查服务状态**（来自 L8）：调一次 `GET /health`，后端连不上或数据库不可用时提前提示，带“重新检查”，不轮询；修 C5

### 插入任务：Windows 第四轮核对的修复（2026-11-23 Barry 批准，T25 之前做）

- [x] **T24aa Ctrl-C 时两个 Worker 都把当前任务做完再退出**（来自 Windows 第四轮核对 §2 第 1、2 条，Barry 于 2026-11-23 批准“先修 Ctrl+C”）：两个 Worker 等子进程结果的 `poll()` 遇到 `InterruptedError` 接着等（Windows 上按 Ctrl-C 时会抛出）；通用 Worker 的子进程也忽略 SIGINT（D34 只改过 OCR 子进程）。见 D52
- [x] **T24ab Worker 被强制结束时，它的子进程跟着退出**（来自 `docs/changes/2026-11-23-代码复核建议.md` R1，Barry 于 2026-11-23 批准“先修 R1”）：两个 Worker 的子进程入口加父进程看门狗（`shared/parent_watch.py`），父进程一消失就退出。见 D53
- [x] **T24ac OCR Worker 收到停止信号时以 130 退出**（来自 `docs/changes/2026-11-23-代码复核建议.md` R5，Barry 于 2026-11-23 批准“修 R5”）：原来返回 0，外层循环会把它重新拉起。见 D54
- [x] **T24ad 失败的任务隔一段时间再重试**（来自 `docs/changes/2026-11-23-代码复核建议.md` R2 的 a，Barry 于 2026-11-25 选定不改表结构的做法“No migration”）：领取时按 `started_at` + `TASK_RETRY_DELAYS_SECONDS`（默认 30、120 秒）等待。见 D55
- [x] **T24ae 把失败的 embed、ocr 任务成批放回队列**（R2 的 b，Barry 于 2026-11-25 批准“做 T24ae”）：`python -m app.modules.documents requeue-failed --type embed|ocr [--yes]`，默认演练。见 D56
- [x] **T24af 检索服务不可用时，repair 不再说“没有需要修复的问题”**（R3，Barry 于 2026-11-25 批准“先做 R3”）：只对检查过的类别这样说
- [x] **T24ag 内存上限提示只打一次、网页图标**（R4 的前两处，Barry 于 2026-11-25 批准“先做 R4”）：不支持的系统上由 Worker 启动时说明一次；加 `favicon.svg`

### 插入任务：克隆库前端整体放入（2026-11-25 Barry 批准，T25 之前做）

来源：克隆库 `~/Desktop/BARRY zou-search-motion` 的 `feat/search-motion`（`2834695`）。Barry 于 2026-11-25 看过影响分析和计划后批准“批准，用建议选项”：① 检索结果一到就收拢，不再等扫描动画播完一轮；② 作为 GLOBAL §3.1“不做复杂动画”和 P4 规则的例外（D60）；③ `/motion-lab` 只在开发模式保留；④ 在单独的工作区和分支 `feat/frontend-port` 上做，Barry 看过之后才合进 `main`。没有新依赖，不改表结构、索引、配置、附录 A。编号从 T24ba 开始，避开同时在做的 T24a 系列。一次做一个，各自一个 commit，不 push。

- [x] **T24ba 任务失败原因清理后再返回**（来自克隆库 P1）：普通用户、被共享者看到清理过的文字，管理员看原文。必须在 T24bd 之前，否则任务面板会把服务器路径显示出来
- [x] **T24bb 登录竞态、文件列表、预览页的缺陷**（来自 V1 的一部分、V4）：这三处 main 上都已复现
- [x] **T24bc 中英文切换与配色**（来自克隆库的界面语言、系统配色、L6 英文部分、L7、V3）
- [x] **T24bd 任务面板：处理详情、重试、预览页自动刷新**（来自 P2–P4、V1）
- [x] **T24be 搜索动效，检索可取消、30 秒超时**（来自克隆库搜索动效、V2，按决定 ① ③ 修改）
- [x] **T24bf 文档收尾**
- [x] **T24bh 检索动效的文字只说真实发生的事**（Barry 于 2026-11-25 批准“改”）
- [x] **T24bg Windows 任务书按新界面修改**：新增第 17.18 节，第 10.2、10.5 节加注（原文保留），第 17.1、17.2、17.12、17.13、14.2 节补上对应内容

### 插入任务：Windows W9 核对的修复（2026-11-26 Barry 批准，T25 之前做）

- [x] **T24ah 数据库连接超时，数据库停掉时接口返回 503**（来自 `docs/changes/windows-2026-11-26-核对.md` Bug 1，Barry 于 2026-11-26 批准“修bug1”）：`make_engine()` 必须传连接超时；新增 `DATABASE_CONNECT_TIMEOUT_SECONDS`（默认 5）
- [x] **T24ai 测试不再依赖真实网络错误的文字**（同一核对记录 Bug 2，Barry 于 2026-11-26 批准“Fix both”）：`test_database_address_is_hidden` 改用写死的驱动错误文字
- [x] **T24aj 实验记录的 `git_dirty` 只看已跟踪文件**（同一核对记录“其他”第 1 条，Barry 于 2026-11-26 批准“Fix both”）：`git status --porcelain --untracked-files=no`

### 阶段五：实验（W13–W15）

- [ ] **T25 冻结数据集与标注**：查询总数、各类型数量、qrels 数量写进 `experiments/README.md`；冻结后不再修改
- [ ] **T26 质量实验**：B0–B3 和消融，每组重复运行，保存全部原始结果
- [ ] **T27 性能实验**：查询延迟 P50/P95（每个通道分别统计）、索引构建时间、OCR 每页耗时、CLIP 吞吐、各组件内存
- [ ] **T28 分析**：图表、按查询类型分层的结论、失败案例分析、负面结果和局限性

### 阶段六：论文与答辩（W16–W20）

- [ ] **T29 测试报告**：汇总所有 🧪 测试和覆盖率
- [ ] **T30 部署说明与使用说明**：Docker 方式和非 Docker 方式都写
- [ ] **T31 一致性核对**：逐条核对论文描述、README、截图和实际功能（参照 GLOBAL §13、§14）
- [ ] **T32 答辩演示脚本**：固定演示数据、固定操作步骤，包含关闭 CLIP 服务的降级演示

------------------------------------------------------------------------

## 4. 待议事项（P4 及新想法先记在这里，不做）

以下是 2026-11-14 核查 T05–T10 时发现、但不属于已完成任务范围的事项，留给后续任务或由 Barry 决定：

- **（T14 已解决）** 之前记给 T14 的提醒都已处理，做法见 `decisions.md` D27：存储新增 `local_path()`；文档状态只跟随 parse 任务的规则已定，并在任务失败、回收、重试时一并更新；parse 处理函数开头检查文档是否已删除；按 `mime_type` 选解析器，图片写 `image_assets`；`parser_options` 只传 PDF 的 `pdf_ocr_min_chars`；索引改为在每个任务开始时 `ensure_indices`（没有放在 API、Worker 启动时）；上传后由 parse 任务写 `doc_meta`，删除由 cleanup 任务调用 `delete_document`，改标签接口提交后尽力同步 `doc_meta`；`TextIndexUnavailable` / `TextIndexError` / `ParseError` / `PipelineError` 都由 Worker 按 `retryable` 处理。
- **（T21 已解决）给 T21 的补充（T18 记录）**
  - ~~一致性检查（D31）还没有覆盖 `image_embeddings`~~：T21 已补上无用向量（`embedding_orphan`，修复类别 `embeddings`）和向量索引与数据库不一致（`vector_*`，修复类别 `index`、`rebuild-indices`）的检测与修复，见 `decisions.md` D35。
- **（T24a 已解决，D40）待定（T18 记录）**
  - backend 通用 Worker 启动时不检查数据库，连不上时在领取循环里无限重试；OCR Worker 启动时连不上数据库就以退出码 1 结束（D30）。两者不一致，是否统一由 Barry 决定。
- **（T20、T21 已处理）给 T20、T21（CLIP）的参考（T17 记录）**
  - ~~CLIP 服务和 embed 任务可以复用~~（两者都没有采用：CLIP 服务不领任务（D33）；embed 任务由通用 Worker 领取，只发 HTTP 请求，见 D35） `shared.task_queue.PgTaskQueue`，以及 OCR Worker“常驻子进程加载模型、超时或崩溃时杀掉重开”的写法（`services/ocr_worker/ocr_worker/engine_process.py`）。
- **（T24e 已解决，D44；注意：当前前端看不到效果，见 D44）待改进（T17 记录）**
  - 文本预览接口按 `seq` 排序，扫描页的 OCR 片段排在全部正文片段之后。如果要按页码穿插，需要改预览接口的排序规则。
- **2026-11-16 补测的后续（来源：`change-deepseek-v4/`，见 §5“T00–T19 补测”）**
  - **修复已合入（2026-11-17）：** C01–C12 的 9 个文件已按 `change-deepseek-v4/modified-files/` 合入本仓库（只去掉了 Windows 换行符，逐行核对与报告一致，没有夹带其他改动）。N01 烟测脚本已于 2026-11-19 经 Barry 批准放进 `scripts/smoke/ocr_e2e.py`（去掉了 Windows 专用路径和写死的连接串，见 D39）。合入后本机（macOS）重跑结果见 §5“修复合入”。
  - **C12 的取舍：** OCR 引擎在 Windows 上关闭 oneDNN（`enable_mkldnn=os.name != "nt"`），macOS/Linux 不变。若阶段五在 Windows 上测 OCR 耗时，需要在论文里注明这一点。
  - ~~**`docs/untested.md` 待整理**~~（Barry 于 2026-11-19 批准，已整理：删除 Windows 补测已通过的项，剩 24 项测试，见该文件开头）。
  - **仍未验证：** 8 项符号链接测试在普通权限的 Windows 上失败（WinError 1314，环境权限问题），以管理员权限重跑后通过；前端与真实后端的浏览器联调（T10、T16）；OCR 与 CLIP 同时运行的内存（OS-6，CLIP 尚未实现）；IK 分词器（没有匹配 OpenSearch 2.19.1 的版本）；真实扫描件、手机照片、Office 实际保存的文件；Dockerfile 构建。
  - **测试项数变化：** untested.md 记的是 188 项，实际收集到 190 项（`test_migrations.py` 13→14，`test_auth.py` 19→20），更新 untested.md 时一并核对。
- **MVP-0 验收前必须做（T16 记录）**
  - ~~在有 PostgreSQL 和 OpenSearch（带 analysis-smartcn）的环境里补跑全部集成测试~~（2026-11-16 已在 Windows 验证副本上完成，190/190 通过，修复已于 2026-11-17 合入）。还需要把前端接到真实后端联调一遍：上传 PDF、Word → 等处理完成 → 检索 → 定位到页或段落 → 删除后搜不到。通过后再打 tag `mvp-0`。
  - ~~高亮摘要的 HTML 转义要在真实 OpenSearch 上确认（untested.md OS-10）~~（2026-11-16 已确认：`<script>` 被转义，只保留 `<em>`）。前端已对摘要做白名单清洗，只放行 `<em>`。
- **打包体积（T16 记录）**
  - ~~Vite 提示主包（约 874 KB）和 pdf.worker（约 1.27 MB）超过 500 KB。worker 本来就是单独加载的；主包可以在 T30 部署前考虑按需引入 Element Plus（D22）。~~（Barry 于 2026-11-21 批准，T24p 已完成：主包 349 KB）
- **给 T22（检索 v2）的衔接提醒（T15 补充）**
  - 直接复用 `backend/app/modules/search/rrf.py`，只需加~~图像通道、CLIP 调用超时降级~~和消融配置。~~现在两路是串行的，加第三路时可以考虑并行执行。~~（T22 已处理：图像通道与文本通道并行、超时降级，见 D36；消融配置属于 T24）
  - ~~图像通道目前在请求开启时报 `unavailable`（“图像检索尚未实现”），实现后改为真实状态。~~（T22 已处理，D36）
- **评测数据（T19 记录，由 Barry 负责，已滞后）**
  - 收集评测文档（原计划 W2 起，200–500 个文件）和每周标注（原计划 W4 起）都还没有开始。框架已就绪，格式和操作步骤见 `experiments/README.md`。没有数据就达不到 MVP-1，也无法开展阶段五的实验，建议尽快开始。
  - ~~`grade` 0–3 各等级的含义待 Barry 确认~~（Barry 于 2026-11-19 确认 README 中的写法）。
- **（T24c 已解决，D42）给 T22、T26 的补充（T19 记录）**
  - OCR Worker 的参数（`OCR_MIN_CONFIDENCE`、`OCR_PDF_DPI`）还没有记录进实验配置，因为 backend 读不到 OCR Worker 的配置。正式实验前要补上，例如让 OCR Worker 把参数写进 `ocr_results`，或在实验配置里显式填写。
- **给 T21、T22 的衔接提醒（T20 记录）**
  - CLIP 服务的接口见 `api.md` §9：~~`POST /encode/text` 传 `{"texts": [...]}`（T22 用）~~（T22 已处理，D36）。~~`POST /encode/image` 写进 `image_embeddings`~~（T21 已实现，D35）。向量已归一化；T21 的精确检索用的是 `knn_score` + `cosinesimil`（与 T00 实测写法一致），对归一化向量排序与点积相同。
  - ~~调用方自己设超时（A5）。服务一次只算一个请求，embed 任务批量入库时，查询编码可能要排队，T22 定超时时要考虑。~~（T22 已处理：`SEARCH_IMAGE_TIMEOUT_SECONDS` 默认 3 秒，超时降级，D36）
  - ~~413、422 标为不可重试~~、~~向量维度 512 用于 mapping~~、~~embed 任务在哪个进程领取~~：T21 已处理（ClipRejected 不可重试；mapping 维度 512；通用 Worker 领取），见 D35。换模型仍要重建向量索引。
- **T15–T19 复核留下的事项（2026-11-17 记录，详见 decisions.md D34）**
  - 已定（Barry，2026-11-17）：库里有数据集以外的文档时保持只提示并记录 `documents_outside_dataset`，不拦截运行。~~待 Barry 决定：`rebuild-indices` 是否需要一个无条件强制重建的开关~~（Barry 于 2026-11-19 批准，T24d 已完成，D43）。
  - 待改进（Barry 于 2026-11-19 决定暂不做，写进论文局限）：重新解析与旧版本 OCR 的竞争窗口（旧版本 OCR 片段可能残留，一致性检查能清掉）。修它要改 T14 的 parse 流水线，需要在有 PostgreSQL 的机器上验证后再做。
  - 部署到 Linux 前要实测：OCR 识别子进程的内存上限用的是 `RLIMIT_AS`（默认 3072 MB），PaddlePaddle 可能因此加载失败。
- **待 Barry 决定（T20 记录）**
  - ~~`CLAUDE.md` 的“常用命令”还没有加 CLIP 服务的启动和测试命令~~（Barry 于 2026-11-17 同意，已补）。
  - ~~`env_check/models/clip_cn_vit-b-16.pt` 原文件是否删除~~（Barry 于 2026-11-19 批准，核对 sha256 一致后已删除，见 downloads.md）。
- **（T21 已解决）给 T21 的衔接提醒**
  - ~~parse 任务目前不创建 embed 任务~~：T21 在解析图片成功的同一事务里创建（与 OCR 任务同处），按 payload 去重；同内容只编码一次靠 sha256 咨询锁 + 查 `image_embeddings`，见 D35。
- **给 T22、T24 的衔接提醒（T21 记录）**
  - ~~向量检索：`app.modules.vector_index.search_vectors(client, query_vector, *, document_ids, model_name, model_version, depth) -> list[VectorHit]`（`VectorHit` 含 document_id、image_id、score）。`document_ids` 传 M1 的可访问集合，管理员传 `None`（不过滤），空集合直接返回空、不发请求；`model_name`、`model_version` 取 CLIP `/health` 的当前模型，只比较同一模型的向量；结果已按文档折叠、按分数排好，score 是 1+余弦相似度，只用于排名。索引不存在时先建索引、返回空；其他故障照常抛出，T22 要把它当作通道不可用，而不是空结果。返回前仍需 M11 的数据库二次校验。~~（T22 已处理：模型标识取自 `/encode/text` 的应答，故障记为通道不可用，见 D36）
  - ~~实验记录的 mapping hash（`backend/app/modules/experiments/environment.py` 的 `code_versions`）只遍历 `INDEX_NAMES`，不含 `image_vectors.json`，跑 B3 前要补~~（T24 已处理，D38）。
  - ~~CLIP 服务一次只算一个请求：embed 任务批量编码时，查询编码可能排在后面（单张图片最长等 `CLIP_ENCODE_TIMEOUT_SECONDS`），T22 定查询编码超时时要考虑。~~（T22 已处理：查询超时 3 秒、超时降级；排队导致降级仍是局限，见 D36）
- **待 Barry 决定（T24 记录）**
  - ~~`CLAUDE.md` 的“实验”命令一行是否补一句：B3 类配置（开了图像通道的）需先启动 CLIP 服务，并让通用 Worker 处理完 embed 任务~~（Barry 于 2026-11-19 同意，已补）。
- **待 Barry 决定（T21 记录）**
  - ~~`CLAUDE.md` 一致性检查命令的说明仍写“对账数据库、磁盘和两个索引”，类别列表里没有新增的 `embeddings`~~（Barry 于 2026-11-19 同意，已补）。
- **待实验决定（T12 记录）**
  - 是否给每个 Excel 片段补上该工作表的表头行：片段里只有数据、没有列名，按“列名 + 值”的方式搜索可能搜不到后面的行。补表头会让表头词在同一文件里重复计分。阶段五用实验比较。
  - Word 片段只定位到起始段落（Barry 于 2026-11-19 决定暂缓）。如果实验或演示发现跳转偏差影响使用，再考虑给 `DocxParaLocator` 增加结束段落字段（数据契约变更，需 Barry 批准）。
- **评测数据收集时顺带做**
  - 用几份真实的 Word、Excel（由 Office 或 WPS 保存）和手机照片过一遍 T11 的解析器，结果记到 `docs/untested.md` §4 对应的行。
- **待议（T24a 记录，见 `docs/changes/T24a.md` §4）**
  - ~~CLAUDE.md 的 Worker 命令说明没有写“启动时连不上数据库以退出码 1 结束”~~（Barry 于 2026-11-19 同意，已补）。
  - ~~启动检查没有连接超时（libpq 默认值），主机不可达时可能等一两分钟才报错。~~（Barry 于 2026-11-21 批准，T24k 已完成）
  - ~~启动检查不查表结构：空库（没迁移）时要到第一次领取才报错。~~（Barry 于 2026-11-21 批准，T24l 已完成）
- **优化清单（2026-11-21，Barry 批准 A、B 组 8 项）**：1 Worker 连接超时（T24k）、2 Worker 启动时检查迁移（T24l）、3 pdf.js 资源同步检查（T24m）、4 文件列表标签不截断（T24n）、5 一致性检查扩大结构比较（T24o）、6 Element Plus 按需引入（T24p）、7 根目录 README（T24q）、8 整理零散文件（T24r）。C 组（登录失败限制、缩略图接口、上传前查大小、存储配额）和 D 组（竞争窗口、Word 结束段落、只重新切分）没有批准，维持原决定
- ~~**待 Barry 决定（T24m 记录）**：`CLAUDE.md` 的前端命令一行是否补上 `npm run sync:pdfjs`~~（Barry 于 2026-11-21 同意，已补）。
- **待议（T24c 记录，见 `docs/changes/T24c.md` §4）**
  - ~~没有“对已解析的文档重新做 OCR”的入口~~（Barry 于 2026-11-19 批准，T24i 已完成：`experiments reocr`，见 D47）。“只改 `min_confidence` 时只重新切分”没有做，T24i 一律重新识别；如果阶段五要扫多个阈值、重新识别太慢，再议。
  - ~~待 Barry 决定（T24i 记录）：`CLAUDE.md` 的“实验”命令一行是否补上 `reocr`~~（Barry 于 2026-11-19 同意，已补）。
  - ~~运行前检查没有拦“数据集里用了两个不同的 OCR 模型”（快照里有 `ocr_models`），可以用同样的办法补上。~~（Barry 于 2026-11-19 批准，排为 T24g）
  - ~~`scripts/smoke/ocr_e2e.py` 可以加一项检查 `ocr_results.params` 有值。~~（Barry 于 2026-11-19 批准，T24h 已完成）
- **待议（T24d 记录，见 `docs/changes/T24d.md` §4）**
  - ~~CLAUDE.md 的一致性检查说明没有提 `--force`~~（Barry 于 2026-11-19 同意，已补）。
  - ~~结构检查只比较字段类型、分词器类型和 BM25 参数；要不要扩大比较范围（例如 `search_analyzer`），待议。~~（Barry 于 2026-11-21 批准，T24o 已完成）
  - ~~待 Barry 决定（T24o 记录）：`CLAUDE.md` 一致性检查说明里 `--force` 的举例已不准确~~（Barry 于 2026-11-21 同意，已改为“改了分析器插件内部参数等检查比较不到的设置”）。
- **待议（T24e 记录，见 `docs/changes/T24e.md` §4）**
  - （已批准，排为 T24f）前端预览页对 PDF、图片不显示抽取文本，T24e 的排序在界面上看不到。是否给 PDF、图片加一个“抽取文本”标签页（能看到 OCR 识别出了什么，答辩演示 OCR 时有用），属于新功能。Barry 于 2026-11-19 先决定不加（`e759bfc`），随后要求出方案，看过后于同日批准，排为 T24f。
- **安全方面，本科毕设范围内可以不做，但答辩可能被问到**（Barry 于 2026-11-19 决定：`/health` 一项排为 T24b；其余两项不做，写进论文“局限与改进”并准备答辩回答）
  - 登录接口没有限制尝试次数，可以被暴力猜密码。
  - 没有每个用户的存储配额。
  - ~~`/health` 是公开接口，依赖不可用时返回的 `detail` 里带有内部主机名和端口~~（T24b 已解决：只返回异常类型，详情写日志，见 D41）。
- **待议（Windows 第一轮日志，2026-11-21 记录，见 `docs/changes/windows-2026-11-21-补充核对.md` §2）**
  - 任务失败后立即回到 `pending`，领取按 `created_at` 排序，所以失败的任务马上又被领走：W3 里 3 次尝试大约 40 秒就用完了，一次短暂的故障就足以让任务永久失败。可以考虑加重试间隔（例如加一列“最早可领取时间”，或在领取 SQL 里按上次失败时间推迟），要动表结构或领取 SQL，属 🔒。等 `windows任务书.md` 第 16.4 节的数据回来，再由 Barry 决定做不做；不做就写进论文“局限”一节

- **待 Barry 决定（Windows 第四轮核对，2026-11-23 记录，见 `docs/changes/windows-2026-11-23-核对.md` §2）**
  - **（T24aa 已解决，D52）Ctrl+C 打断当前任务**：① OCR Worker 在 Windows 上，`engine_process.py` 的等待循环调用 `Connection.poll()` 时收到 Ctrl+C 会抛 `InterruptedError`，循环没有捕获（W6 12.7 实测：任务被记一次失败、Worker 退出码 1）；② 通用 Worker 的 `runner.py` 有同样的等待写法，而且子进程没有忽略 SIGINT（D34 只改了 OCR 子进程），任何系统上按 Ctrl+C 都会把正在解析的文件记一次失败（代码复核，未实测）。修法：两处等待循环捕获 `InterruptedError` 后继续等；通用 Worker 的子进程也 `signal(SIGINT, SIG_IGN)`；补单元测试。修完后按 `windows任务书.md` 第 17.5 节重测
  - （T24af 已解决）`consistency repair` 在检索服务不可用时，在“这次不会修复”之后还多打一行“所选类别下没有需要修复的问题”，与 D34 的意图相反。小改动
  - （已决定：保留现状）检索页四个开关全关时地址栏保留上一次的 `ch`（W4）。Barry 于 2026-11-25 决定保留现状（地址栏记的是最后一次真正执行的检索，刷新能恢复结果）

- **待 Barry 决定（代码复核建议，2026-11-23 记录，见 `docs/changes/2026-11-23-代码复核建议.md`）**
  - （T24ab 已解决，D53）R1 Worker 被强制结束后，子进程成为孤儿继续跑完任务
  - （2026-11-25 第五轮又有两份证据：OCR 内存不足时 3 次立刻重试都失败；embed 约 15 秒用完 3 次，建议优先做）（已解决：a 由 T24ad，D55；b 由 T24ae，D56；c 不做）R2 失败任务没有重试间隔；CLIP 短暂不可用会让 embed 永久失败且没有批量补救（a 加重试间隔要迁移，🔒；b 加重新排队命令；c 一致性检查新增一类）
  - （R3 已由 T24af 解决）R3 `repair` 的误导提示；（R4 前两处已由 T24ag 解决）R4 内存上限日志刷屏、favicon 404；（地址栏残留 `ch`：Barry 于 2026-11-25 决定保留现状（地址栏记的是最后一次真正执行的检索，刷新能恢复结果），不改）
  - （T24ac 已解决，D54）R5 OCR Worker 收到停止信号后返回 0，`CLAUDE.md` 的循环和 `run_ocr_worker_loop.ps1` 会把它重新拉起（通用 Worker 返回 130）；建议也返回 130，不带 🔒
  - 风险记录（不做）：`OCR_WORKER_MEMORY_LIMIT_MB=3072` 在 Linux 上可能太小

- **待 Barry 决定（Windows W9 核对，2026-11-26 记录，见 `docs/changes/windows-2026-11-26-核对.md` 第 2 节）**
  - **（T24ah 已解决）Bug 1**：Windows 上数据库停掉、后端开着时，`/api/auth/me` 等接口一直挂着不返回。`backend/app/db/session.py` 的 `make_engine()` 没有连接超时；Windows 上 psycopg 连被拒绝的端口会等到超时为止。建议新增 `DATABASE_CONNECT_TIMEOUT_SECONDS`（默认 5），通过 `connect_args` 传给 psycopg，超时后按现有逻辑返回 503
  - （T24ai 已解决）Bug 2：`test_task_errors.py::test_database_address_is_hidden` 依赖真实网络错误，Windows 上失败；改用写死的错误文字
  - （T24aj 已解决）实验记录的 `git_dirty` 把未跟踪文件也算进去，Windows 上每次都是 true；改为只看已跟踪文件

- **文档**
  - ~~项目根目录没有 `README.md`。GLOBAL §11.2 要求配置变化时同步更新 README，§14 的验收标准也要求 README；目前相关说明分散在 `CLAUDE.md` 和 `frontend/README.md` 里。T30 之前需要补。~~（Barry 于 2026-11-21 批准，T24q 已完成；部署细节留给 T30）
- **前端**
  - 新想法（T23 记录，Barry 于 2026-11-19 决定暂不做，归入 P4）：后端缩略图接口。现在检索页的缩略图取的是原图（D37），图片多、图片大时费流量。可以在后端加一个按需生成并缓存小图的接口，但需要 Pillow 之类的图像库（主环境新依赖），须 Barry 批准；不属于核心验收条件。
  - （Barry 于 2026-11-19 决定暂不做，写进局限）上传前没有在浏览器里检查文件大小（上限在后端配置里，前端不知道）。超限的文件要传完才被拒绝。
  - ~~文件名一栏较窄时，标签会被省略号截断。~~（Barry 于 2026-11-21 批准，T24n 已完成）
  - （T24be 已解决）（2026-11-22 记录，来自对克隆库 `feat/search-motion` 的审查）：检索请求可取消 + 超时。现在检索页靠 `loading` 守卫和 `rerun` 标记避免结果错位，上一次没返回时连按回车不会发新请求，也没有超时。分支上的做法：`api/client.ts` 的请求加可选 `signal`，新的检索中断旧请求、丢弃旧返回，30 秒没返回算失败。分支上它和扫描加载动画绑在一起，单独移植要拆开
  - 待议（T24s 记录，见 `docs/changes/T24s.md` §6）：① 上传百分比进度（要把上传请求从 fetch 改成 XHR）；② 图片预览缩放（现在只按容器宽度缩小显示）；③ 检索结果分页或“加载更多”（现在不传 `top_k`，最多 20 个文件）。三项都是新功能，由 Barry 决定。另外提醒：T24s 改了全部页面的布局和配色，T31 之前要按新界面重截文档和论文里的界面截图

------------------------------------------------------------------------

## 5. 日期与完成记录

开工日期（W1 周一）：______

| 任务 | 完成日期 | commit | 备注 |
|---|---|---|---|
| T00 | 部分完成（2026-11-13） | e253c74 | 硬件、OCR、CLIP 已实测并写入 decisions.md §2；OpenSearch、分词（A13/A14）、并发内存未测试（Barry 决定不在本机使用 Docker），清单见 env_check/未测试/清单.md；OCR/CLIP 规格待 Barry 选定 |
| T01 | 2026-11-13 | 31e2c95 | 单元测试 13 项通过；docker-compose 只校验了语法，容器未实际启动；OpenSearch 中文分词插件待 T00 结论（A13） |
| T02 | 2026-11-13 | 43f7589 | shared 包测试 93 项通过 |
| T03 | 2026-11-13 | 62f3201 | 后端测试 30 项通过，其中 13 项集成测试在本地 PostgreSQL 16.15 上运行；未在 docker-compose 的 postgres:16.6 容器上运行 |
| T04 | 2026-11-13 | 403664d | 三份文档完成；Barry 于 2026-11-13 确认方案（含 api.md 的接口设计与 D12、D13），里程碑“方案评审”通过。遗留：decisions.md §2 中 OpenSearch、分词（A13）、降级预案（A14）、并发内存未测试，须在 T13 开始前确定；OCR/CLIP 规格分别在 T17、T20 开始前选定 |
| T05 | 2026-11-13 | b39f3dd | 后端测试 74 项通过（其中存储 54 项、配置新增 3 项），13 项集成测试因未设置 TEST_DATABASE_URL 未运行（与本任务无关）；接口为 stage/commit/discard 两步写入 + put 简便方法；支持 pdf/png/jpg/docx/xlsx 五种类型；进程被强杀时残留的临时文件尚无清理入口，留给 T18（已由 T18 的 `temp-files` 处理，见 decisions.md D31） |
| T06 | 2026-11-13 | 56e8336 | 已执行：不需要数据库的测试 113 项通过（T06 新增 37 项：密码哈希、令牌、未登录 401、参数校验 422、数据库不可用 503）。**未测试（Not Tested）**：`tests/integration/test_auth.py` 中 19 项需要 PostgreSQL 的测试（注册登录全流程、重名 409、访问他人文档 403、管理员可见全部、共享后可见与取消共享后不可见、软删除不可见、create-admin 命令），原因是本机没有 PostgreSQL，按 GLOBAL“测试执行限制”不安装；已对这部分代码和测试做人工复核，未发现问题。T03 的 13 项迁移测试同样未测试 |
| T07 | 2026-11-13 | 56e8336 | 计划经 Barry 批准后实现。已执行：后端测试 135 项通过（T07 新增 22 项：子进程执行的正常/异常/超时/崩溃/租约丢失，主循环的分发/回写/处理 N 个后退出/数据库出错不崩溃，配置校验）。**未测试（Not Tested）**：`tests/integration/test_task_queue.py` 的 18 项，包括 DEVPLAN 要求的全部四项 🧪（崩溃恢复、并发不重复领取、幂等、超过重试上限标记 failed），原因是本机没有 PostgreSQL，按 GLOBAL“测试执行限制”不安装；已逐条复核 SQL 与测试逻辑，未发现问题。内存上限在 macOS 上不生效（decisions.md D16）。里程碑“基础系统”要求 T07 四项测试全部通过，目前不满足 |
| T08 | 2026-11-13 | a749a23 | 已执行：后端测试 188 项通过（T08 新增 53 项：文件名与标签规范化、上传各步骤失败后不留文件（用假的数据库会话模拟）、全部路由未登录 401、Content-Length 超限 413、配置校验）。**未测试（Not Tested）**：`tests/integration/test_documents.py` 的 41 项，包括 DEVPLAN 要求的三项 🧪 在真实数据库上的版本（上传中途失败不留半成品、删除后列表和下载都不可见、非法类型被拒绝），以及列表、分页、共享、标签、任务重试；原因是本机没有 PostgreSQL，按 GLOBAL“测试执行限制”不安装；已逐条复核代码与测试。新增依赖 python-multipart 由 Barry 单独批准（decisions.md D19）。至此共 91 项数据库集成测试未测试。未测试项的逐项清单见 `docs/untested.md`，下载记录见 `docs/downloads.md` |
| T09 | 2026-11-13 | d317142 | 后端测试 209 项通过，其中 T09 新增 21 项（PDF 解析 20 项：文本型、扫描型、混合型、加密、损坏；配置 1 项），全部在本机实际执行，没有未测试项。按页判断规则细化为三种情况（decisions.md D20）。新增依赖 PyMuPDF 1.28.2 由 Barry 批准（D21，已登记到 docs/downloads.md）。测试用的 PDF 是现场生成的，未用真实扫描件验证 |
| T10 | 2026-11-14 | e5209a5 | 登录/注册页、文件列表（含处理状态与自动刷新）、上传、下载、删除、共享。已执行：类型检查通过、30 项前端单元测试通过、生产构建成功；在浏览器里对着临时的模拟接口把全部功能人工点了一遍。**未测试（Not Tested）**：与真实后端的联调（本机没有 PostgreSQL，真实后端的登录等接口无法运行）；页面组件没有自动化测试。新下载：Node.js 26.13.1（装在项目内 .tools/node/）和 131 个 npm 包，Barry 批准，已登记到 docs/downloads.md。里程碑“基础系统”未达成 |
| T05–T10 核查 | 2026-11-14 | a0872dc | Barry 要求的整体核查。方法：重跑全部测试与代码检查；从真实应用导出接口清单，与 api.md 和前端类型逐项对照（17 个接口、全部字段一致）；启动真实后端和前端开发代理，用 curl 走通不需要数据库的路径；通读各模块之间的衔接。发现并修复 5 处：① 超大上传经代理时用户看到 502 而不是 413；② 解析器标记的“不可重试”在子进程边界丢失；③ `.env.example` 里的示例 JWT 密钥长度合格，原样复制也能启动；④ 存储和 Worker 各有一处代码在 Windows 上会直接报错；⑤ `.gitignore` 的 `models/` 规则会误忽略任何同名目录。新增 7 项测试，后端现为 216 项通过。未修、留作后续的事项记在 §4。91 项数据库集成测试和前后端联调仍未测试，里程碑“基础系统”仍未达成 |
| T11 | 2026-11-14 | 3bd66e9 | Word、Excel、图片三个解析器，zip 炸弹防护（解压后总大小、条目数、加密条目），图片像素数上限与截断检查。已执行：后端测试 288 项通过（T11 新增 72 项：Word 18、Excel 19、图片 23、zip 检查 11、配置 1），全部在本机实际执行，没有未测试项；代码检查通过。每种格式的 fixture 都不少于 2 个，畸形文件包括 zip 炸弹、谎报大小的条目、截断、XML 损坏、缺主部件、互相冒充、伪造表格范围、像素炸弹。新增依赖 python-docx 1.2.0、openpyxl 3.1.5（带入 lxml、et-xmlfile）由 Barry 批准，已登记到 docs/downloads.md；规则与局限见 decisions.md D24。新增三个配置项（PARSE_ZIP_MAX_TOTAL_BYTES、PARSE_ZIP_MAX_ENTRIES、PARSE_IMAGE_MAX_PIXELS）。解析超时沿用 Worker 子进程边界的超时（T07），解析器内部没有另做；解析器尚未接入 Worker（T14）。测试文件都是现场生成的，未用 Office 实际保存的文件和真实照片验证，已记入 docs/untested.md §4 |
| T12 | 2026-11-14 | 8134a2e | 切分模块 `chunk_document` / `chunk_blocks`、`split_spans`、`make_parse_version`。规则见 decisions.md D25：PDF 页和图片不合并；Word 相邻段落、Excel 同一工作表相邻行按整块打包；Word 定位到起始段落，Excel 用外接矩形；打包时整块重叠，超长块按字符重叠并优先在换行、句末处断开；parse_version 由算法版本、切分参数、解析器名称和版本、解析参数确定性算出。新增配置 CHUNK_MAX_CHARS（500）、CHUNK_OVERLAP_CHARS（50）。已执行：后端测试 336 项通过（T12 新增 48 项：切分 47、配置 1），全部在本机实际执行，没有未测试项；代码检查通过。三项 🧪 都有对应测试，并用 T11 解析器生成的 docx、xlsx 做了衔接测试。没有新下载。切分尚未接入 Worker（T14）；正文与 OCR 片段的序号分配留给 T14/T17，记在 §4。实施过程中另一个会话（T11 实施 fork）曾在同一目录短暂做 T12，已由它撤回自己的改动；提交前逐个核对过文件内容，并重跑了全部测试 |
| T13 | 2026-11-14 | 0600f02 | 计划经 Barry 批准后实现，A13 选 smartcn 由 Barry 于 2026-11-14 在本会话亲自确认；代码由“T11 实施 (fork)”会话编写，复核、测试、文档和提交由本会话完成。`text_index` 模块：httpx 直连 REST（不引入 opensearch-py）、`doc_meta` 与 `chunks` 两个 strict mapping（分析器 `docmgr_text` 直接使用插件自带的 smartcn 分析器，显式 BM25 参数，无权限字段；`backend/pyproject.toml` 声明了 mapping 文件为 package-data）、`ensure_indices`、`index_document`（先删其他版本再批量写入，`_id`=chunk_id）、`index_doc_meta`、`delete_document`，错误分可重试 / 不可重试两类。新增配置 OPENSEARCH_TIMEOUT_SECONDS（10）、OPENSEARCH_INDEX_PREFIX（空）；`deploy/docker-compose.yml` 改为带 analysis-smartcn 的自定义镜像（`deploy/opensearch/Dockerfile`）。附录 A13 按 Barry 的选定改为 analysis-smartcn（未经实测，阶段五可换）；A14 未改，T13 按不启用实现。已执行：后端测试 378 项通过（T13 新增 42 项：模拟应答下的索引测试 41、配置 1），shared 93 项通过，代码检查通过。**未测试（Not Tested）**：`tests/opensearch/test_text_index_live.py` 的 13 项，包括 DEVPLAN 要求的两项 🧪（重复索引不产生重复数据、删除后查不到），原因是本机没有 OpenSearch（没有 Docker 和 Java）；两个 mapping 从未被 OpenSearch 接受过，`deploy/opensearch/Dockerfile` 从未构建，compose 只读过 YAML 结构，package-data 没有用普通安装验证过。复核时指出的两处已由编写会话修改：分析器改为直接用 smartcn 类型（少依赖两个名字）；补上 package-data 声明。已登记到 docs/untested.md，补测步骤见该文件第 5、6 节。没有新下载 |
| T14 | 2026-11-15 | eecd032 | 代码由“T11 实施 (fork)”会话编写（Barry 在该会话里让开始 T14），复核、测试、文档和提交由本会话完成。parse 任务：读文档（已删除则不做）→ processing → 确保索引并写 doc_meta → 按 mime_type 解析、切分 → 换掉正文片段并登记图片 → 写 chunks 索引 → 复查是否被删除 → succeeded + parse_version + 按页创建 OCR 任务。cleanup 任务：只清理已软删除的文档，顺序为索引 → 文件 → 硬删除（最后一步，级联删除连任务记录一起删掉）。文档状态只跟随 parse 任务，最终失败时由 `shared/tasks.py` 的 fail / reclaim_expired 在同一事务里改为 failed；重试 failed 的 parse 任务时文档回到 pending。改标签后尽力同步 doc_meta；compose 关闭 `action.auto_create_index`；存储新增 `local_path()`。规则与局限见 decisions.md D27。已执行：后端测试 415 项通过（T14 新增 37 项：流水线 30、local_path 7），shared 93 项通过，代码检查通过。**未测试（Not Tested）**：`tests/integration/test_pipeline_db.py` 的 23 项，包括 DEVPLAN 要求的 🧪 端到端（上传 PDF → 等任务完成 → chunks 索引中有该文档的数据）。原因是本机没有 PostgreSQL，其中 2 项还需要 OpenSearch。`shared/tasks.py` 新增的 SQL 从未执行，真实子进程里的处理函数从未运行，`action.auto_create_index` 未验证。已登记到 docs/untested.md。复核时指出的 1 个应修问题（改标签可能让 OpenSearch 自动建出错误的索引）和 1 处文字错误已由编写会话修改。没有修改附录 A，没有新下载 |
| T15 | 2026-11-15 | 68385a0 | 代码由“T11 实施 (fork)”会话编写（Barry 在该会话里让开始 T15），复核、测试、文档和提交由本会话完成。融合方式由 Barry 于 2026-11-15 在该会话选定“T15 就用 RRF (Recommended)”：`rrf.py` 从 T22 提前到 T15，k=60、每通道取前 100 个文件，都放配置；T22 只加图像通道、降级和消融配置。实现见 decisions.md D28：校验 → meta（doc_meta，文件名与标签）、text（chunks BM25，collapse 取每文档最佳片段作证据）两路 → RRF（只用名次，同分按 document_id 排序）→ 数据库二次校验（accessible_filter，不缓存）→ 先过滤后截取 top_k → 写 SearchLog；普通用户两路带可访问 ID 的 terms 前置过滤（只为召回），管理员不加；任何一路出错整体 503 SEARCH_UNAVAILABLE，故障也写日志；索引不存在时查询路径先建索引再查；图像通道未实现，默认关闭，开启时报 unavailable。新增 POST /api/search、SearchUnavailableError（503）、11 项 SEARCH_* 配置。已执行：后端测试 462 项通过（T15 新增 47 项，RRF、检索编排、配置），shared 93 项通过，代码检查通过。未测试（Not Tested）：`test_search_db.py` 20 项（19 项需要 PostgreSQL，1 项另需 OpenSearch），含 DEVPLAN 的四项 🧪；查询体从未被真实 OpenSearch 接受过；高亮转义待实测（untested.md OS-10）。复核发现 6 处局限，未改代码，写进 D28。没有修改附录 A，没有新下载 |
| T16 | 2026-11-15 | 066350f | 代码由“T11 实施 (fork)”会话编写（Barry 在该会话里让开始 T16），复核、测试、浏览器检查、文档和提交由本会话完成。新增后端接口 GET /api/documents/{id}/text（当前版本片段，按 seq 排序，来自数据库；chunk_id 直接跳到所在页）；前端检索页（检索词进地址栏，503 与无结果分开显示，失败通道逐个提示）、预览页（PDF 用 pdf.js 画在 canvas 并跳到命中页，图片原生显示，Word/Excel 显示抽取文本并滚到命中片段）、顶部导航、文件列表“查看”。规则见 decisions.md D29；D22 改为“只在两处用 v-html，都先转义再只插入 <em>”。新增依赖 pdfjs-dist 6.5.438，Barry 于 2026-11-15 批准（先在编写会话选“同意安装 6.5.438 (Recommended)”，又在本会话选“同意，现在安装 (Recommended)”），随之自动带入 @napi-rs/canvas 两个可选包（约 28 MB，浏览器不用；Barry 随后决定保留），已登记 downloads.md #21–#23。已执行：后端测试 462 项通过；前端类型检查、构建通过，单元测试 48 项通过（T16 新增 18 项）；浏览器检查是对着临时模拟接口做的（模拟接口不是项目代码，没有提交）：检索结果、摘要里的 <script> 和 <img onerror> 只显示成文字、空结果与 503 分开显示、图像通道提示、刷新保留检索词、PDF 跳到命中页及翻页/页码/缩放、Word 分页并滚到命中段（首轮发现直接打开不滚动，修复后复查通过）、图片预览。未测试（Not Tested）：test_document_text.py 11 项（需要 PostgreSQL）；前端与真实后端联调；页面组件无自动化测试；PDF 只用测试文件验证过。**MVP-0 里程碑未达成，没有打 tag**：全部数据库与 OpenSearch 测试都没有运行，前后端没有联调。没有修改附录 A |
| T17 | 2026-11-15 | 0151f34 | 计划由 Barry 在编写会话里批准（“批准，开始写”；选择“按原计划做 OCR Worker”“PP-OCRv5 mobile (Recommended)”“沿用 env_check/.venv-ocr (Recommended)”）；代码由“T11 实施 (fork)”会话编写，测试、复核、文档和提交由本会话完成。`services/ocr_worker`：只领取 ocr 任务，常驻识别子进程（模型只加载一次），PDF 页 200 dpi 渲染，识别结果按“文档 + 对象”替换，一页的行拼成一个文本块后切分，OCR 片段序号从 1e9 起每页预留 1000 个，保存时加锁复查版本、写索引只写不删、写完复查；启动时配置、模型、数据库任一有问题即退出码 1，不联网下载模型。chunking、text_index、PgTaskQueue、存储路径检查移到 shared（shared 新增 httpx 依赖）；parse 创建 ocr 任务时带上切分参数。规则见 decisions.md D30。新增下载：ocr 环境的 PyMuPDF 1.28.2、psycopg 3.3.9、psycopg-binary 3.3.9（Barry 批准，downloads.md #24–#26）；OCR 模型从本机缓存复制到 models/ocr（#27、#28，不进版本库）；shared 以 editable 方式离线装入两个环境。已执行：后端测试 463 项通过；shared 105 项通过；services/ocr_worker 63 项通过（main 环境）；🧪 真实识别 4 项在 ocr 环境通过（扫描版 PDF 页、独立图片、空白图、模型版本记录），用的是本地模型，~/.paddlex 没有新增模型、没有联网；启动检查三项通过（缺配置、模型目录不存在、数据库连不上都在约 1 秒内以退出码 1 结束）；代码检查通过。首轮复核发现并已修复：每行 OCR 文字各成一个片段；重新解析时 OCR 可能删掉新版本的索引片段；一个无效的测试用例；启动时连不上数据库不退出。未测试（Not Tested）：test_ocr_worker_db.py 10 项（需要 PostgreSQL）；OCR Worker 完整链路从未连真实数据库和 OpenSearch；真实扫描件；Linux 上的内存上限。CLAUDE.md 的命令说明待 Barry 同意后补（§4）。没有修改附录 A |
| T18 | 2026-11-15 | 12f4ebb | 代码由“T11 实施 (fork)”会话编写（Barry 在该会话里让开始 T18），测试、复核、文档和提交由本会话完成。`python -m app.modules.consistency check|repair`：以数据库为准，对账磁盘、`doc_meta`、`chunks`；19 种检测项，7 类修复（index、db-chunks、ocr-results、cleanup-tasks、temp-files、orphan-files、rebuild-indices）；repair 必须 `--fix` 指定类别，不加 `--yes` 只演练，每个动作执行前复查数据库；新文件、清理中的文档、正在处理的文档不报告；rebuild-indices 是 D26 要求的重建入口，需先停 Worker。规则见 decisions.md D31。首轮复核发现并已修复：对正在解析的文档，`repair --fix db-chunks` 会删掉解析中的新片段（另有 3 个小问题和 3 个新增检测项）。已执行：后端测试 499 项通过（T18 新增 36 项）；代码检查通过；命令行冒烟（三种 --help、repair 缺 --fix 时退出码 2、数据库连不上时立即以退出码 1 结束）。未测试（Not Tested）：test_consistency_db.py 12 项（需要 PostgreSQL，含 DEVPLAN 要求的三类不一致 🧪）；从未对真实 OpenSearch 扫描、检查结构和重建；从未在真实数据上跑过。CLAUDE.md 的命令说明待 Barry 同意后补（§4）。没有修改附录 A，没有新下载 |
| T19 | 2026-11-15 | 496d86b | 计划由 Barry 在编写会话里批准（“批准，开始写”，由编写会话转述）；代码由“T11 实施 (fork)”会话编写，测试、复核、文档和提交由本会话完成。框架已完成：`python -m app.modules.experiments validate|import|run`；数据格式 manifest.csv / queries.tsv / qrels/*.tsv（标注用 file_id，导入时生成 document_map.csv）；P@K、R@K、nDCG@K（手算样例验证），先按查询类型分层再给总体；B0、B1、B2 三个配置只切换通道、source_types、top_k、K；每次运行保存 config.json、results.jsonl、metrics.json 并写 experiment_runs；运行前检查不通过就拒绝运行；检索失败或通道不可用时标为不完整。规则见 decisions.md D32，使用说明见 experiments/README.md。首轮复核发现并已修复：结果目录可能重名导致整次运行丢失；P@K 与另两项的平均口径不一致。已执行：后端测试 540 项通过（T19 新增 41 项）；代码检查通过；命令行冒烟（validate 空模板退出码 0；run 空数据集退出码 1；用临时小数据集时 import、run 在数据库连不上时以退出码 1 结束；不进 Git 的三类路径确认被忽略）。没有新下载（没有装 psutil，用标准库代替）。未测试（Not Tested）：test_experiments_db.py 8 项（需要 PostgreSQL）；从未在真实数据和真实 OpenSearch 上运行。**里程碑 MVP-1 未达成，没有打 tag**：没有评测数据，B0–B2 还没有真实数字；全部数据库和 OpenSearch 测试也都没有运行。CLAUDE.md 的命令说明待 Barry 同意后补（§4）。没有修改附录 A |
| T00–T19 补测 | 2026-11-16 | bc671e0 | 由 Barry 在另一台机器上完成，报告和改动上传到仓库的 `change-deepseek-v4/`（00–04 五份说明、`modified-files/`、`test-results/`）；本行只是据此整理，本会话没有重跑。环境：Windows 11、Python 3.14.0、PostgreSQL 16.15、OpenSearch 2.19.1 + analysis-smartcn 2.19.1（插件安装器报 AccessDenied，改为手工解压）。**结果（报告所载）：** docs/untested.md §1 的 11 个连调文件 190 passed / 0 failed / 0 skipped（专用空库，JUnit 原始结果在 `test-results/integration-results.xml`），覆盖 T03、T06、T07（含四项 🧪）、T08、T13、T14、T15、T16、T17、T18、T19；backend 完整套件 728 passed（8 项符号链接测试需管理员权限，普通权限下失败）；shared 105 passed；services/ocr_worker 63 passed、4 skipped，另在 ocr 环境真实识别 4/4；前端 48 passed、类型检查与构建通过；ruff 三个目录通过。**T00 补测：** OpenSearch 启动、smartcn 分词（22 词，standard 34 个单字）、BM25 与带权限过滤的精确向量检索正常，BM25 P50 15.28 ms / P95 26.93 ms，JVM 堆 475.5/1024 MB；OS-10 高亮转义已确认。**OCR 全链路（N01 `ocr_e2e.py`）：** 上传图片 → parse → OCR Worker（PP-OCRv5 mobile）→ 写索引 → 检索命中（evidence.source_type=ocr）→ 删除后片段清理、搜不到，PASS。**为通过测试做的修改 C01–C12（9 个文件，没有动表结构、接口、mapping、依赖版本）：** alembic.ini 中文注释导致 GBK 解码失败；实验结果路径改用 `as_posix()`；测试读文件显式 UTF-8；两处排序断言写错；两处测试前置数据不对；env_check 在 Windows 上没有 `resource`；OCR 子进程崩溃时先 join 再读退出码；OCR 在 Windows 上关闭 oneDNN。这些修改补测时只在副本里，已于 2026-11-17 合入本仓库（见下一行）。T00 仍为部分完成（OS-6 并发内存、IK 未测）；里程碑“基础系统”、MVP-0、MVP-1 仍未宣布达成 |
| 修复合入 | 2026-11-17 | 2b4d0f7 | 按 Barry 指示把 C01–C12（9 个文件，+30/−9）合入本仓库，不含 N01。本机（macOS）重跑：ruff 三个目录通过；backend 540 passed、188 skipped、0 failed（跳过的是 11 个连调文件，本机没有 PostgreSQL 和 OpenSearch）；shared 105 passed；services/ocr_worker main 环境 63 passed、4 skipped，ocr 环境真实识别 4/4（覆盖改过的 engine.py、engine_process.py）；`env_check/_common.py` 在 macOS 上 `peak_rss_mb()` 正常返回。**未测试（Not Tested）**：改过的 4 个连调测试文件和 alembic.ini、实验结果路径的数据库路径，在本机都没跑，依据是 2026-11-16 Windows 补测（代码逐行一致） |
| T20 | 2026-11-17 | 90bb44f | 计划由 Barry 于 2026-11-17 在本会话批准（“批准，开始写”；选“装 FastAPI (Recommended)”“默认 CPU，可配置 (Recommended)”）。开始前按 Barry 要求重读了 DEVPLAN、decisions.md、`T15-T19 opus5.5 develop.md` 和 `change-deepseek-v4/` 的记录，确认 C01–C12 与 T15–T19 的改动不影响 T20。`services/clip_service`：启动时检查权重文件（缺失或 sha256 不符即退出码 1，不下载）→ 加载 Chinese-CLIP ViT-B-16 并自检 → 监听 127.0.0.1:8001；`GET /health`、`POST /encode/text`、`POST /encode/image`（请求体为图片字节），响应都带 model_name、model_version（`cn_clip-1.6.0-5997ef32c50d`）、dim（512）；向量 L2 归一化；图片只收 PNG、JPEG，字节数与像素数双重上限（413），损坏（422）；错误格式与后端一致。规则见 decisions.md D33，接口见 api.md §9。新下载：clip 环境 9 个包约 13 MB（downloads.md #29–#37，比征求同意时说的多 1 个 opentelemetry-api）；权重从 env_check/models 复制到 models/clip（#38，没有下载）。已执行（本机 macOS，CPU）：接口测试 39 项通过（main 环境，假编码器）；🧪 真实模型测试 17 项通过（clip 环境，经真实 HTTP 服务）：健康检查、同一文本和同一图片两次编码向量完全一致、超过像素上限与字节上限 413、九种损坏或不支持的图片 422、出错后服务仍可用、EXIF 方向、文本与图片向量在同一空间；命令行冒烟：权重缺失、sha256 不符、端口非法均以退出码 1 结束，正常启动后 curl 三个接口结果正确；代码检查通过。首轮测试发现并已修复：超过字节上限时服务提前断开，调用方看到连接中断而不是 413。未测试（Not Tested）：MPS、CUDA、Windows、Linux；跨机器的向量一致性；后端 /health 对着真实服务；真实照片；并发（已登记 untested.md）。CLAUDE.md 的命令说明待 Barry 同意后补（§4）。提交时工作区里另有 11 个不属于 T20 的文件被别的会话改动（backend 一致性检查与检索、前端、ocr_worker），没有纳入本次提交。没有修改附录 A，没有动表结构和索引 |
| T15–T19 复核修正 | 2026-11-17 | 591f482 | Barry 要求由 Fable 5.2 重新查看 Opus 5.5 写的 T15–T19 并修正不足。方法：通读五个任务的全部源码，逐条对照 `docs/T15-T19 opus5.5 develop.md` 的查验要点；重跑全部能在本机运行的测试。结论：主干（处理顺序、数据库二次校验、幂等、降级）正确，没有发现违反附录 A 的地方；修正 11 处，见 decisions.md D34：① 检索服务应答格式不对时由 500 改为 503；② 索引里 document_id 不合法的残留数据不再让检索失败；③ 预览页关键词高亮会拆坏 `&`、`<`、`'` 的转义，且区分大小写；④ PDF 预览连续翻页时误报“这一页无法显示”；⑤ 检索页重复提交；⑥ OCR 识别子进程被 Ctrl-C 打断；⑦ `PgStore.save` 返回类型标注；⑧ `consistency repair` 在检索服务不可用时报“没有问题”并返回 0；⑨ 重建索引丢掉解析失败文档的 doc_meta；⑩ 实验运行前检查不看 OCR 任务失败，`import` 替换文件后旧文档留在库里，库里有数据集以外的文档时没有提示；⑪ qrels 的 grade 校验遇到特殊字符会崩溃。没有动表结构、接口、mapping 和依赖，没有新下载，没有修改附录 A。已执行：backend 554 passed、191 skipped；shared 105 passed；services/ocr_worker 63 passed、4 skipped，ocr 环境真实识别 4 项通过；前端类型检查与构建通过、单元测试 51 项通过；三个目录代码检查通过；浏览器里对着临时模拟接口检查了 PDF 预览和文本高亮。未测试（Not Tested）：新增的 3 项数据库测试（需要 PostgreSQL）；`consistency repair` 的新提示与退出码；Ctrl-C 实际操作；已登记到 untested.md。看过但没有改的事项记在 §4 |
| T21 | 2026-11-19 | a2facca | 代码由本会话 Opus 5.5 编写（Barry 于 2026-11-19 切换了模型，并要求主会话只写代码、其余交给子代理）；测试、复核、文档和提交由子代理完成。T21 不带 🔒，没有单独的计划批准。新模块 `backend/app/modules/vector_index/`：索引 `image_vectors`（1 分片 0 副本，dynamic strict，`vector` 为 512 维 knn_vector，不开 `index.knn`、不建 HNSW，附录 A12），`_id` = image_id，重复写入即覆盖；`search_vectors` 用 script_score（`knn_score` + `cosinesimil`）精确检索，model_name、model_version 和可访问 document_id 作为前置过滤，按 document_id 折叠。CLIP 客户端 `backend/app/modules/clip/client.py`（连不上、超时、5xx、429 可重试；413、422 等 4xx 不可重试），新增配置 `CLIP_ENCODE_TIMEOUT_SECONDS`（60）。embed 任务由通用 Worker 领取，parse 解析图片成功时在同一事务里创建；按 sha256 加咨询锁后查 `image_embeddings`，同一内容只编码一次（并发时也一样）；文档状态不跟随 embed 任务。cleanup 连带删除向量索引里的数据（`image_embeddings` 不删，D10）。一致性检查覆盖向量：新增 5 种检测项和修复类别 `embeddings`，`index`、`rebuild-indices` 连向量一起重建。规则与局限见 decisions.md D35。复核发现并已修复两处：还没有任何向量记录时误报 `image_vectors` 缺失；删除无用向量时没加锁，与 embed 有竞争。已执行：backend 640 passed、207 skipped（比 T15–T19 复核修正时多 86 项通过、16 项跳过）；shared 105 passed；两个目录代码检查通过。**未测试（Not Tested）**：`test_embed_db.py` 8 项（需要 PostgreSQL，含 🧪“重复图片只编码一次”的数据库版本与并发版本）、`test_vector_index_live.py` 8 项（需要 OpenSearch，含 🧪“过滤后只返回有权限的文档”），两项 🧪 的假对象版本已在单元测试里通过；没有连真实 CLIP 服务与 Worker 端到端跑过；已登记 untested.md。向量检索尚未接入检索编排（T22）。没有新下载，没有改表结构（不需要迁移），没有修改附录 A；新增 mapping 不影响已有两个索引，不需要重建 |
| T22 | 2026-11-19 | 889a48b | 带 🔒：计划由 Barry 于 2026-11-19 在本会话批准（“批准，按推荐做”：图像通道与文本通道并行、`SEARCH_CHANNEL_IMAGE_ENABLED` 仍默认关闭、查询编码超时 3 秒）。代码由主会话编写；复测、复核、文档和提交由子代理完成。图像通道：CLIP `POST /encode/text` 编码查询（应答自带模型标识，每次查询只调用一次）→ 维度核对 → `search_vectors` 精确检索（同模型、权限前置过滤）→ 与 meta、text 一起 RRF → 数据库二次校验；图像通道在单独线程里与文本通道并行执行；CLIP 超时、连不上、拒绝、应答不对、维度不一致、向量索引出错都只把 image 标为 unavailable 并写明原因（200），文本通道出错仍是 503；text 与 image 都命中时证据用文本片段。新增配置 `SEARCH_IMAGE_TIMEOUT_SECONDS`；查询专用 CLIP 客户端放在 `app.state.query_clip`；检索日志记录 `image_model`；实验入口也传入查询客户端。规则见 decisions.md D36，api.md §7.1 已更新。已执行：backend 668 项通过、208 项跳过（T22 新增单元测试 28 项，检索编排与 CLIP 客户端，含三通道 RRF 手算样例和假网络层下“关闭 CLIP 服务后检索正常并带降级标记”），shared 105 项通过，ruff 两个目录通过。未测试（Not Tested）：`test_search_db.py` 新增的 `test_clip_service_down_degrades_to_text_search`（需要 PostgreSQL，是 🧪“关闭 CLIP 服务后检索仍然正常并带降级标记”的真实接口版本）；图像通道查询体从未发给真实 OpenSearch；从未连真实 CLIP 服务编码查询；并行线程在真实负载下的表现、3 秒超时是否合适都没有实测（见 untested.md）。没有修改附录 A，没有新下载 |
| T23 | 2026-11-19 | 38d2c06 | 代码由主会话编写（Barry 要求主会话只写代码），复测、浏览器检查、文档和提交由子代理完成。T23 不带 🔒，没有单独的计划批准。检索页：图片结果左侧显示缩略图（原图取成 Blob 显示，只取 PNG/JPEG，>5 MB 显示占位，并发 4，新检索或离开页面时释放地址）；命中通道标签按通道着色；图片证据写“图像语义匹配（CLIP）”，与 OCR 命中分开；新增“图像语义检索（CLIP）”开关（默认关，`img=1` 进地址栏，请求显式发送 `channels.image`）；不可用通道用黄色提示，图像通道写明“本次结果只来自文字检索”。规则见 decisions.md D37。已执行：前端类型检查、构建通过，单元测试 62 项通过（T23 前为 51 项，新增 11 项：缩略图加载 5、命中依据与降级提示 5、`isImageType` 1）；构建的“chunk 大于 500 kB”警告在 T23 之前就有（在 HEAD 的副本上构建同样出现，主包约 874 kB）。浏览器检查对着临时模拟后端做（模拟后端不是项目代码，没有提交）：不勾选时请求 `image=false`；勾选后请求 `image=true`、地址栏有 `img=1`，刷新和从预览页返回后保持；图片结果显示缩略图，点击进入预览；>5 MB 显示“图片较大”占位；下载失败显示“无法显示”；图片证据显示“图像语义匹配（CLIP）”；通道标签三种颜色；image 不可用时出现黄色提示。未测试（Not Tested）：与真实后端、真实 CLIP 服务的联调；页面组件没有自动化测试。没有修改附录 A，没有新下载 |
| T24 | 2026-11-19 | 34af94e | 代码由主会话（Opus 5.5）编写，测试复核、文档和提交由子代理完成；T24 不带 🔒。新增 7 个实验配置：B3、B3-no-ocr、B3-no-clip、clip-only、B3-k10、B3-k30、B3-k100（k=60 即 B3）；实验配置新增可选 `rrf_k`（只覆盖本次实验的 k，随 search_params 与检索日志记录）；开了图像通道的配置运行前检查 CLIP 服务是否可用、数据集图片是否都有当前模型的向量，模型信息记进 config.json 的 `clip_model`；`mapping_sha256` 补上 `image_vectors`。规则见 decisions.md D38。已执行：backend 678 项通过、212 项跳过，shared 105 项通过，ruff 通过（T24 新增单元测试 10 项，跳过数从 208 增至 212 即新增的 4 项集成测试）。未测试（Not Tested）：test_experiments_db.py 新增 4 项（需要 PostgreSQL）；B3 及消融从未在真实数据和真实 CLIP 上运行。**MVP-2 里程碑未达成，没有打 tag**（原因同 MVP-0）。没有修改附录 A，没有新下载 |
| 待议事项统一批准 | 2026-11-19 | 8609ef5 | Barry 于 2026-11-19 对 §4 中 14 项待批准事项“按推荐全部批准”（D39）。当场完成 5 项：qrels `grade` 含义确认；A14 定为不启用；删除重复的 CLIP 权重 `env_check/models/clip_cn_vit-b-16.pt`（删前核对 sha256 一致）；整理 `docs/untested.md`（删除 Windows 补测已通过的 190 项及 OS-1/3/4/5/8/9/10，剩 24 项测试）；N01 烟测脚本改写后放进 `scripts/smoke/ocr_e2e.py`，`.gitignore` 加 `storage-smoke/`。另 5 项排为 T24a–T24e；其余暂缓。已执行：烟测脚本 ruff 检查与格式检查通过、能编译，未设 `TEST_DATABASE_URL` 时退出码 2。**未测试（Not Tested）**：烟测脚本改写后没有实际跑过（本机没有 PostgreSQL 和 OpenSearch），已登记到 untested.md。没有改代码、表结构、索引和附录 A；没有新下载 |
| T24a | 2026-11-19 | e21a174 | D39 第 6 项，Barry 于 2026-11-19 批准；不带 🔒。`shared/task_queue.py` 的 `PgTaskQueue` 新增 `ping()`；`backend/app/worker/__main__.py` 启动时先 `ping`，任何 `psycopg.Error` 都打印“Worker 无法连接数据库（异常类型）”并以退出码 1 结束，不进入领取循环；信号处理改到检查之后登记；领取循环中途断线仍然重试（未改 `loop.py`）。新增 `tests/unit/test_worker_main.py` 4 项。已执行：backend 682 passed、212 skipped（新增 4 项通过）；shared 105 passed；services/ocr_worker（main 环境）63 passed、4 skipped；backend、shared 的 ruff 检查与格式检查通过；实际启动 `python -m app.worker`，`DATABASE_URL` 指向没有服务的端口：退出码 1，输出不含密码和端口。没有改表结构、接口、附录 A，没有新下载，没有未测试项。修改记录见 `docs/changes/T24a.md` |
| T24b | 2026-11-19 | 509502d | D39 第 7 项，Barry 于 2026-11-19 批准；不带 🔒。`backend/app/api/health.py`：依赖不可用时 `detail` 只给异常类型（HTTP 错误加状态码，如 `HTTPStatusError: HTTP 503`），完整的类型和消息写进 WARNING 日志；返回结构、状态码、`ok`/`degraded` 规则不变；`docs/api.md` §3 同步。`tests/unit/test_health.py` 新增 3 项（真实应用对着空闲端口：响应里没有主机、端口、用户名、密码，日志里有原因；HTTP 503 只留状态码；数据库认证失败不暴露用户名）。已执行：backend 685 passed、212 skipped（新增 3 项通过）；ruff 检查与格式检查通过。前端不读 `/health`，不受影响。没有改表结构、附录 A，没有新下载，没有未测试项。修改记录见 `docs/changes/T24b.md` |
| T24c | 2026-11-19 | 491b59b | 带 🔒：方案由 Barry 于 2026-11-19 批准（“批准，按推荐做”：参数作为 `save()` 的独立参数、不改数据契约；参数不一致或未记录时运行前拦截）。表结构：`ocr_results.params`（jsonb，默认 `{}`），迁移 `0002`，不需要重建索引。OCR Worker 写入 `pdf_dpi`（图片为 null）、`min_confidence`、`max_pixels`；实验 `config.json` 新增 `versions.ocr_params`，运行前检查新增 OCR 参数一项。已执行：backend 692 passed、216 skipped（新增单元测试 7 项通过，新增集成测试 4 项跳过）；shared 105 passed；services/ocr_worker（main 环境）66 passed、4 skipped（新增 3 项），ocr 环境真实识别 4/4；ruff 三个目录通过；`alembic heads` 为 `0002 (head)`；模型编译出的列定义为 `params JSONB DEFAULT '{}' NOT NULL`，与迁移一致。**未测试（Not Tested）**：迁移在真实 PostgreSQL 上升级、回退，`test_migration_matches_models`，`PgStore.save` 写入 params，快照与运行前检查的 SQL（GROUP BY jsonb），共 4 项新集成测试和 3 处改动过的已有集成测试，原因是本机没有 PostgreSQL，已登记到 untested.md 并做代码复核。修改记录见 `docs/changes/T24c.md` |
| T24d | 2026-11-19 | ad827bf | D39 第 9 项，Barry 于 2026-11-19 批准；不带 🔒。`consistency repair` 新增 `--force`：与 `--fix rebuild-indices` 一起用时，检查没发现索引缺失或结构不一致也重建三个索引；仍需 `--yes` 才执行，不加时照常只演练；`--force` 不配 `rebuild-indices` 时在读配置之前就报用法错误（退出码 2）；检索服务不可用时不强制。实现放在 `repair.plan(force_rebuild=…)`：补一条 `forced_rebuild` 计划项，检查已要求重建时不重复。`tests/unit/test_consistency.py` 新增 9 项（计划 4 项、命令行 5 项，命令行测试把数据库和检索服务的采集换成固定快照）。已执行：backend 701 passed、216 skipped；ruff 通过；实际运行 `--fix index --force` 报用法错误、退出码 2，`--fix rebuild-indices --force` 进入数据库步骤（本机没有数据库，退出码 1）。**未测试（Not Tested）**：对真实 OpenSearch 执行强制重建（`rebuild_indices` 本身原来就没在真实 OpenSearch 上跑过，本任务没有改它），已登记到 untested.md。修改记录见 `docs/changes/T24d.md` |
| T24e | 2026-11-19 | 110d5ac | D39 第 10 项，Barry 于 2026-11-19 批准；不带 🔒。`GET /api/documents/{id}/text` 改为按（页码，正文在前、OCR 在后，seq）排序，页码取 `locator->>'page'`，没有页码的定位按 0 算（Word、Excel、图片的顺序不变）；`chunk_id` 跳转用同一组排序键做行比较，计算所在页。`docs/api.md` §5.6 同步。**做完后核对发现：** 前端只对 Word、Excel 调用这个接口（PDF 用 pdf.js、图片直接显示），而 Word、Excel 没有 OCR 片段，所以当前界面上看不到变化；改动只对接口本身和以后的调用方有效，见 D44。测试：`tests/unit/test_document_text_order.py` 2 项（检查生成的 SQL）已通过；`test_document_text.py` 新增 10 项（含 7 个参数化跳转用例）需要 PostgreSQL，未运行。已执行：backend 703 passed、226 skipped；ruff 通过。**未测试（Not Tested）**：真实 PostgreSQL 上的排序和跳转，已登记到 untested.md。修改记录见 `docs/changes/T24e.md` |
| T24f | 2026-11-19 | ea9e56c | 新功能，方案由 Barry 于 2026-11-19 批准（“批准，按推荐做”；此前同日曾决定先不加，见 `e759bfc`）。只改前端，后端接口不动，没有新依赖。抽出 `ExtractedText.vue`（原 PreviewView 里 Word/Excel 的文本列表原样搬过去）；PDF、图片分“原文件 / 抽取文本”两个懒加载标签页；从检索结果打开图片时默认显示抽取文本并跳到命中片段，PDF 仍默认原文件并跳页；标签页写进地址栏 `view=`；抽取文本页顶部提示 OCR 可能有错字；PDF、图片没有片段时提示 OCR 可能还在处理中。新增 `utils/preview.ts`（`initialPreviewTab`）和 `tests/preview.test.ts` 5 项。已执行：前端类型检查通过、单元测试 67 项通过、生产构建成功；浏览器对着临时模拟接口检查：图片从检索结果打开默认“抽取文本”、命中片段标出并高亮，切到“原文件”图片加载、地址栏变 `view=file`；PDF 从检索结果打开停在原文件第 3 页且没有请求文本，切到“抽取文本”按页穿插（第 1 页正文、第 2 页 OCR、第 3 页正文）；`view=text` 刷新后停在抽取文本，再切回原文件 pdf.js 正常显示（宽 743px、第 3 页）；Word 页面无标签页，提示、分页、命中片段高亮和转义与原来一致。**未测试（Not Tested）**：跳到命中片段后的自动滚动（浏览器面板处于隐藏状态，`requestAnimationFrame` 不触发；改动前的代码在同一环境下同样不滚动，不是本次引入）；与真实后端联调；页面组件没有自动化测试。修改记录见 `docs/changes/T24f.md` |
| T24g | 2026-11-19 | d2169fe | T24c 待议第 4 条，Barry 于 2026-11-19 批准；不带 🔒。`backend/app/modules/experiments/__main__.py`：查询抽成 `_ocr_models()`，快照与运行前检查共用；新增纯函数 `ocr_model_problems()`，数据集 OCR 结果出现两个以上（模型名，模型版本）时报问题，默认拒绝运行，`--allow-incomplete` 放行；提示重新 import，或先用一致性检查 `ocr-results` 类别清理残留。`config.json` 格式不变。规则见 decisions.md D46。已执行：backend 705 passed、227 skipped（新增单元测试 2 项通过）；ruff 通过。**未测试（Not Tested）**：`test_experiments_db.py` 新增 1 项（需要 PostgreSQL），已登记到 untested.md 并复核。没有改表结构、索引、附录 A，没有新下载。修改记录见 `docs/changes/T24g.md` |
| T24h | 2026-11-19 | 4c7b6aa | T24c 待议第 2 条，Barry 于 2026-11-19 批准；不带 🔒。`scripts/smoke/ocr_e2e.py` 新增 `check_ocr_params()`：OCR 文字写入后用 psycopg（主环境已有，不是新依赖）查 `ocr_results`，要求该图片恰好 1 行、`params` 的键正好是 `pdf_dpi`、`min_confidence`、`max_pixels`，`pdf_dpi` 为 null（独立图片），数值类型正确，模型名和版本非空；不满足就 FAILED。已执行：ruff 检查与格式检查通过、能编译；未设 `TEST_DATABASE_URL` 时退出码 2；把数据库连接换成假对象，对 7 种情况（正常、没有行、两行、params 为空、pdf_dpi 非空、类型不对、模型名为空）逐一调用 `check_ocr_params`，结果都符合预期（临时脚本，没有入库）。**未测试（Not Tested）**：烟测脚本仍没有对真实 PostgreSQL、OpenSearch 和 OCR Worker 跑过，untested.md 中原有的一行已更新。没有改后端代码、表结构、附录 A，没有新下载。修改记录见 `docs/changes/T24h.md` |
| T24i | 2026-11-19 | d0be009 | T24c 待议第 1 条，Barry 于 2026-11-19 批准（“完成两项未完成事项”）；不带 🔒，没有改表结构、索引、接口、数据契约、附录 A，没有新下载。新增 `python -m app.modules.experiments reocr [--yes]`：数据集文档当前解析版本、状态为成功或失败的 OCR 任务原地放回 pending（尝试次数、错误、时间、租约、领取者清零，条件更新只动仍为成功或失败的行）；不新建任务，所以每个对象仍只有一个 OCR 任务，运行前检查、一致性检查、重新解析的去重都不受影响。数据集文档还有未完成的解析或 OCR 任务时拒绝执行（退出码 1）；不加 `--yes` 只演练。重做是覆盖：OCR Worker 原本就先删这一对象的旧识别结果和旧片段（数据库和索引）。没有做“只重新切分”。D42、D46 三条运行前检查提示里的处理办法改为“运行 reocr 重新识别”。规则见 decisions.md D47，用法写进 `experiments/README.md` §4（顺带补上 T24g 漏写的模型检查一句）。已执行：backend 709 passed、229 skipped（新增单元测试 4 项通过，新增集成测试 2 项跳过）；ruff 通过；`reocr --help` 正常。**未测试（Not Tested）**：`test_experiments_db.py` 新增 2 项（需要 PostgreSQL），以及放回队列后真实 OCR Worker 重新识别的全过程，已登记到 untested.md。`CLAUDE.md` 的命令说明没有改，记到 §4 待 Barry 决定。修改记录见 `docs/changes/T24i.md` |
| T24k | 2026-11-21 | 891facb | 优化清单第 1 项（来源 T24a 待议），Barry 于 2026-11-21 批准 A、B 组；不带 🔒。`shared/task_queue.py` 新增 `connect_kwargs()`，`PgTaskQueue` 新增可选参数 `connect_timeout_seconds`；OCR Worker 的 `PgStore` 同样；新配置 `WORKER_DB_CONNECT_TIMEOUT_SECONDS`、`OCR_WORKER_DB_CONNECT_TIMEOUT_SECONDS`（整数 2–300，默认 10），`.env.example` 同步。已执行：shared 108 passed（新增 `test_task_queue.py` 3 项）；backend 711 passed、229 skipped（新增 2 项）；services/ocr_worker（main 环境）67 passed、4 skipped（新增 `test_store_connect.py` 1 项、默认值断言 1 处）；三个目录 ruff 通过；ocr 环境能导入改过的模块。实测连一个不可达的地址（10.255.255.1）：不设超时 75.0 秒才报 OperationalError，设 2 秒时 2.0 秒报 ConnectionTimeout。没有改表结构、接口、附录 A，没有新下载，没有未测试项。修改记录见 `docs/changes/T24k.md` |
| T24l | 2026-11-21 | f31590b | 优化清单第 2 项（来源 T24a 待议），Barry 于 2026-11-21 批准；不带 🔒。新增 `backend/app/worker/schema.py`（`expected_heads`、`schema_problem`、`check_schema`），通用 Worker 在 ping 之后检查；OCR Worker 的 `store.py` 新增 `REQUIRED_COLUMNS`、`missing_columns`、`PgStore.schema_problems()`（查 `information_schema.columns`，ocr 环境没有 alembic），启动时检查。已执行：backend 718 passed、229 skipped（新增 7 项）；services/ocr_worker（main 环境）71 passed、4 skipped（新增 4 项）；ruff 通过；ocr 环境能导入；`python -m app.worker` 连不存在的端口仍以退出码 1 结束。**未测试（Not Tested）**：两个检查在真实 PostgreSQL 上的行为，已登记到 untested.md。没有改表结构、迁移、配置、附录 A，没有新下载。修改记录见 `docs/changes/T24l.md` |
| T24m | 2026-11-21 | 49c67e4 | 优化清单第 3 项（来源：审查 `27b51b2`），Barry 于 2026-11-21 批准；不带 🔒，没有新依赖。新增 `frontend/scripts/pdfjs-assets.mjs`（比较）、`scripts/sync-pdfjs.mjs`（先删后复制四个目录，再复核）、`tests/pdfjs-assets.test.mjs`（3 项）；`package.json` 加 `sync:pdfjs`；`frontend/README.md` 同步。写成 `.mjs` 是因为项目没有 `@types/node`。已执行：前端 70 项通过、类型检查通过；`sync:pdfjs` 运行后 `public/pdfjs/` 没有变化；故意改坏一个文件并加一个多余文件，测试失败且列出两者，同步后恢复。没有未测试项。修改记录见 `docs/changes/T24m.md` |
| T24n | 2026-11-21 | 0754962 | 优化清单第 4 项（来源：DEVPLAN §4 前端），Barry 于 2026-11-21 批准；不带 🔒。`DocumentsView.vue` 的“文件名”列去掉 `show-overflow-tooltip`（它把整格压成一行，连标签一起截掉），改为文件名单独省略并带 `title`、标签 flex 换行、特别长的标签自身省略。已执行：类型检查通过、前端 70 项通过；浏览器对着临时模拟接口检查（宽 800px）：长文件名省略且 `title` 为全名，6 个标签分两行全部显示，超长标签不撑破单元格。没有未测试项。修改记录见 `docs/changes/T24n.md` |
| T24o | 2026-11-21 | 33a2384 | 优化清单第 5 项（来源 T24d 待议），Barry 于 2026-11-21 批准；不带 🔒。`consistency/collect.py`：字段比较的键从 3 个增至 12 个（`search_analyzer`、`search_quote_analyzer`、`index`、`doc_values`、`norms`、`similarity`、`ignore_above`、`null_value`、`format` 等），值统一成字符串再比较；分析配置由只比较 `docmgr_text.type` 改为逐项比较 analyzer、tokenizer、filter、char_filter、normalizer；不一致的提示写出具体差异。向量索引的检查不变。已执行：backend 721 passed、229 skipped（新增 3 项，改写 1 项期望文字）；ruff 通过。**未测试（Not Tested）**：对真实 OpenSearch 运行（可能有误报，见 untested.md 第 4 节）。mapping 文件和索引结构没有改，不需要重建索引。修改记录见 `docs/changes/T24o.md` |
| T24p | 2026-11-21 | aaa4bbc | 优化清单第 6 项（来源 T16 记录、D22），Barry 于 2026-11-21 批准；不带 🔒，没有新依赖。新增 `frontend/src/element-components.ts`（23 个组件的清单）、`src/element.ts`（按组件引入样式；逐个 `app.component` 按名字注册，注册 `v-loading`、ElMessage、ElMessageBox，`provideGlobalConfig` 设中文）；`main.ts` 去掉整包引入；新增 `tests/element.test.ts`（扫描全部 `.vue` 的 `<el-xxx>` 核对已注册）。浏览器检查中发现第一版用 `app.use` 时 ElRadioGroup 没注册上（子组件的 install 是空的），改为按名字注册。构建结果：主 JS 873.8 → 348.9 KB（另有 82.6 KB 公共块、51.4 KB 消息框块），CSS 362.6 → 149.5 KB。已执行：类型检查通过、前端 73 项通过、构建成功；从清单删掉 ElTag 时测试失败；浏览器对着临时模拟接口逐页检查（文件列表、共享对话框、删除确认、检索、登录、预览），控制台无警告，中文语言包生效。**未测试（Not Tested）**：生产构建产物没有在浏览器里打开。修改记录见 `docs/changes/T24p.md` |
| T24q | 2026-11-21 | b18909e | 优化清单第 7 项（来源：DEVPLAN §4 文档；GLOBAL §11.2、§14），Barry 于 2026-11-21 批准；不带 🔒。新增根目录 `README.md`：四种检索方式与 B0–B3、五个进程与环境、顶层目录、五步快速开始（完整命令指向 CLAUDE.md）、测试命令、11 份文档的索引、当前状态（如实写明 MVP 未宣布、评测数据未建立）。已执行：16 个相对链接都存在；命令与 CLAUDE.md 一致，引用的可执行文件和子命令存在。没有按快速开始从头走一遍（本机没有 PostgreSQL、OpenSearch），与 untested.md 已有登记相同。修改记录见 `docs/changes/T24q.md` |
| T24r | 2026-11-21 | f0ef765 | 优化清单第 8 项（来源：审查 `27b51b2`），Barry 于 2026-11-21 批准；不带 🔒。`git mv`：`本轮测试失败与未完成.txt` → `docs/changes/windows-2026-11-19-原始说明.txt`；`output/playwright/*.png`（5 张）→ `docs/screenshots/windows-2026-11-19/`；空的 `output/` 删除。`windows任务书.md`、`docs/changes/windows-2026-11-19.md`、`docs/untested.md`（3 处）的引用改为新路径。内容没有改；不在批准范围内的根目录文件（zip、任务书、change-deepseek-v4/、claude-commands/）没有动。修改记录见 `docs/changes/T24r.md` |
| T24s | 2026-11-21 | 281b226 | 新功能（界面），Barry 于 2026-11-21 在三套样例方案中选定“B 侧栏布局，检索通道面板放到搜索栏下面，再和 A（精修）、C（通道名次条和融合分）一起做”；不带 🔒。只改前端展示，没有改后端、接口契约、数据契约、附录 A，没有新依赖（图标手画 SVG）。代码由主会话（Opus 5.5）编写，文档和提交由子代理完成。新增 `src/styles.css`（`--app-*` 公共取值全部引用 Element Plus 变量；公共类 `.app-logo`、`.page-head`、`.app-mark`，检索词高亮由红字改为浅黄底）、`components/AppIcon.vue`（5 个 SVG 图标）、`components/FileTypeBadge.vue`（类型色块）、`utils/download.ts`（`saveBlob`，合并两处下载代码）、`api/health.ts`（调用已有的 `GET /health`）、`utils/channels.ts`（四个开关对应三个通道、地址栏 `ch` 兼容旧的 `img=1`、文字通道关闭时不传 `source_types`、每条结果三个通道的四种状态、耗时与融合分格式）、`tests/channels.test.ts`（20 项）。`App.vue` 顶栏改为左侧导航栏（≤768px 收成顶部一行，内容区最宽 1200px）；`DocumentsView.vue` 拖拽上传区、队列逐个上传并保留每个文件的结果、表格 8 列减到 5 列、加载失败和自动刷新失败改为页内提示；`SearchView.vue` 检索通道面板（CLIP 服务状态、全关时不发请求、改开关自动重新检索）、结果卡片右侧三格名次和 RRF 融合分（`hit.score`）；`PreviewView.vue` 没有上一页时“返回”回到文件列表；三个组件的写死色值改为变量；ElContainer、ElHeader、ElMain 不再注册（23 → 20 个）。取舍：上传进度用逐个文件的状态代替百分比（fetch 拿不到上传进度）；融合分提示不写死 k=60（k 是后端配置，接口不返回）；主题色保持默认蓝。已执行：类型检查通过；前端 10 个文件 93 项通过（新增 20 项）；构建成功，首屏 JS 约 483 KB（index 349.07 + 公共块 82.70 + message 51.36），与 T24p 持平；`src` 下没有写死的十六进制色值；浏览器对着临时模拟后端（scratchpad 里的 Node 脚本，不在仓库里）以 1280×800 和 375×812 截图核对文件页、脚本派发 drop 模拟拖入（一个成功、一个被拒并显示原因）、检索页说明状态与全通道结果、关闭文件名通道后自动重检（`ch=body,ocr,image`）、CLIP 不可用时的降级显示、预览页标题区、窄屏布局，控制台只有被拒文件预期的 415。**未测试（Not Tested）**：① 与真实后端联调（本机没有 PostgreSQL / OpenSearch；`/health` 和检索响应的真实字段、各通道状态的显示没有核对）；② 用鼠标从系统文件管理器真实拖入文件；③ Chrome 以外的浏览器（Safari、Edge、Firefox）。已登记到 `docs/untested.md`。修改记录见 `docs/changes/T24s.md`，决策见 `decisions.md` D48 |
| T24t | 2026-11-21 | 6521a1d | Barry 于 2026-11-21 批准（来自 `windows任务书.md` W5 第 11.2 节的待定项“根治要靠 `.gitattributes`”）；不带 🔒。新增根目录 `.gitattributes`，只有一条规则 `frontend/public/pdfjs/** -text`（带中文注释），文件由主会话编写，验证、文档和提交由子代理完成。没有改代码、`public/pdfjs/` 的内容、附录 A，没有新下载。已执行（macOS，git 2.50.1，没有安装任何东西）：在 scratchpad 里用 `git clone --no-checkout -c core.autocrlf=true` + sparse-checkout 模拟 Windows 签出 `frontend/public/pdfjs`。对照组（没有 `.gitattributes`）：187 个 `i/-text w/-text`、15 个 `i/lf w/crlf`，与主仓库工作区比 sha256 只有 187/202 一致；实验组（复制 `.gitattributes` 后删掉目录重新签出）：187 个 `i/-text w/-text attr/-text`、15 个 `i/lf w/lf attr/-text`，sha256 202/202 一致；对照的 `frontend/README.md` 仍为 `w/crlf`（规则只作用于这个目录）。另发现：已经签出成 CRLF 的工作区，拉到这条规则后 15 个文件会显示为已修改（` M`），要 `git checkout -- frontend/public/pdfjs` 一次才变回 LF，模拟验证过。主仓库：`git ls-files --eol` 为 187 个 `attr/-text` 的二进制、15 个 `i/lf w/lf attr/-text`，`git status` 下 pdfjs 没有文件显示为已修改；`npm test -- tests/pdfjs-assets.test.mjs` 3 项通过。**未测试（Not Tested）**：真实 Windows 签出，仍按 W5 第 11.2 节执行。修改记录见 `docs/changes/T24t.md`，决策见 `decisions.md` D49 |
| T24u | 2026-11-21 | 61678e1 | Barry 于 2026-11-21 批准（“Yes, add them”，来自 `docs/changes/windows-2026-11-21-核对.md` 第 5 节第 1 条）；不带 🔒。`.gitattributes` 新增两条 `text eol=lf` 规则（三个 mapping 文件），带中文注释；没有改代码、mapping 内容、附录 A，没有新下载，不需要重建索引。选 `eol=lf` 而不是 T24t 的 `-text`：mapping 会被手工编辑，`eol=lf` 在提交时也把 CRLF 规范成 LF（D50）。已执行（macOS，git 2.50.1，scratchpad 里模拟 `core.autocrlf=true` 签出）：没有规则时三个文件签出为 CRLF，hash 正好是 W3 记下的 `3f9043ec…`、`1588dd18…`、`5d291270…`；规则进仓库后全新克隆为 `w/lf`，hash 与 Mac 一致；把文件改成 CRLF 再 `git add`，暂存区里是 LF；**规则之前签出的工作区拉取后仍是 CRLF，`git status` 不显示修改，`git checkout --` 也跳过，要先删文件再签出**（已写进任务书第 0.2 节第 4 步）。backend 相关单元测试 138 passed、shared 108 passed。**未测试（Not Tested）**：真实 Windows 签出。修改记录 `docs/changes/T24u.md`，决策 D50 |
| T24v | 2026-11-22 | c3c92b1 | Barry 于 2026-11-22 批准（“Approve, incl. T24z”，移植克隆库 `feat/search-motion` 的 L1 跳转部分与 L3）；不带 🔒。新增 `features/login/redirect.ts`（`safeRedirect`、`loginRoute`、`guardTarget`、`afterUnauthenticated`）；`router.ts` 守卫、`main.ts` 失效回调、`LoginView.vue` 都改为调用它。修 A2（令牌过期后回登录页不带原地址）、A4（已登录打开 `/login?redirect=` 一律去文件页）、B2（跳转地址只查 `/` 与 `//`，反斜杠、控制字符没处理）。没有改后端、接口、附录 A，没有新依赖。已执行：类型检查；前端 11 个文件 131 项通过（新增 `tests/login/redirect.test.ts` 38 项）；生产构建；浏览器对着临时模拟后端检查了未登录跳转带原地址、登录后回原页、令牌失效后带原地址回登录页、已登录打开登录页按 redirect 返回、`/\evil.com` 回首页。**未测试（Not Tested）**：与真实后端联调（已登记 `docs/untested.md`）。修改记录 `docs/changes/T24v.md` |
| T24w | 2026-11-22 | 82cc6c6 | Barry 于 2026-11-22 批准（移植 L1 表单规则部分、L4、L5）；不带 🔒。新增 `features/login/rules.ts`、`submit.ts`、`LoginForm.vue`、`LoginBrand.vue`，`LoginView.vue` 从 154 行减到 36 行，只留布局；卡片标题改为 `h2`；修 A3（注册成功但登录失败时停在注册模式、提前提示“已自动登录”）、B1、C4、校验结束前连按回车发两次请求；另修两处原有问题：切到注册模式时空表单立刻冒红字（加 `:validate-on-rule-change="false"`，浏览器里发现）、注册密码长度按 UTF-16 而不是按字符数算。提示文字用中文常量，与原来逐字相同；不加分支上的 logo 插槽。没有改后端、接口、附录 A，没有新依赖。已执行：类型检查；前端 13 个文件 165 项通过（新增 `rules.test.ts` 26 项、`submit.test.ts` 8 项）；生产构建；浏览器对着临时模拟后端检查了拆分前后 9 个元素位置相同、切换模式不冒红字、注册成功但登录失败、连按回车只发一次、密码错误提示。**未测试（Not Tested）**：与真实后端联调（已登记 `docs/untested.md`）。修改记录 `docs/changes/T24w.md` |
| T24x | 2026-11-22 | 46633e6 | Barry 于 2026-11-22 批准（移植 L2）；不带 🔒。`auth.ts` 的 `restoreSession` 只在 4xx 时删令牌，网络不通和 5xx 时保留令牌、`ready` 不置位、新增 `unreachable`；登录页在卡片上方显示“登录状态已保留”和“重试”（`LoginForm.vue` 加默认插槽）。修 A1（后端重启、502、503、断网时一刷新就被退出）。没有改后端、接口、附录 A，没有新依赖。已执行：类型检查；前端 14 个文件 177 项通过（新增 `auth.test.ts` 12 项）；生产构建；浏览器里真正停掉模拟后端（开发代理返回 502）后刷新：令牌保留并显示提示；重启模拟后端（令牌失效）点重试：令牌被删；模拟后端返回 502 再恢复后点重试：直接回到原页面。**未测试（Not Tested）**：与真实后端联调（已登记 `docs/untested.md`）。修改记录 `docs/changes/T24x.md`，决策 D51 |
| T24y | 2026-11-23 | 083bbbf | Barry 于 2026-11-22 批准（移植 L6 的中文部分）；不带 🔒。新增 `features/login/errors.ts`：5 个错误码（`INVALID_CREDENTIALS`、`USERNAME_TAKEN`、`VALIDATION_ERROR`、`DATABASE_UNAVAILABLE`、`INTERNAL_ERROR`）给出更具体的中文说明，其余显示后端原文；`LoginForm.vue` 的出错提示从顶部 3 秒就消失的 `ElMessage` 改为按钮上方的 `el-alert`（`role="alert"`），修改输入、切换模式、重新提交时收起；“注册成功”仍用顶部提示。修 C1。只改登录页。没有改后端、接口、附录 A，没有新依赖。已执行：类型检查；前端 15 个文件 189 项通过（新增 `errors.test.ts` 12 项）；生产构建；浏览器对着临时模拟后端检查了密码错误、用户名已存在、后端没启动（502）、注册成功但登录失败四种提示，以及修改输入、切换模式后收起。**未测试（Not Tested）**：与真实后端联调、读屏软件（已登记 `docs/untested.md`）。修改记录 `docs/changes/T24y.md` |
| T24z | 2026-11-23 | 6bab037 | Barry 于 2026-11-22 批准（“Approve, incl. T24z”，移植 L8）；不带 🔒。新增 `features/login/serviceStatus.ts`；登录页挂载后调一次 `GET /health`，后端连不上或数据库不可用时在卡片上方提前提示，带“重新检查”，不轮询；与 T24x 的提示同时成立时只显示 T24x 那一条。修 C5。只看后端和数据库，OpenSearch、CLIP 不影响登录。没有改后端、接口、附录 A，没有新依赖。已执行：类型检查；前端 16 个文件 205 项通过（新增 `service-status.test.ts` 16 项）；生产构建；浏览器对着临时模拟后端检查了正常时无提示、数据库不可用提示与重新检查、真正停掉模拟后端时有令牌只显示一条提示、无令牌时提示后端连不上、恢复后重新检查提示消失。**未测试（Not Tested）**：对着真实后端的 `/health`（已登记 `docs/untested.md`）。修改记录 `docs/changes/T24z.md` |
| Windows 第二轮补测 | 2026-11-19 | 27b51b2 | 由 Barry 在 Windows 上完成并推到 GitHub，本会话合入（合并提交 `73e5b58`），没有重跑全套。测试的是 `50b244b`（T24f 之后、T24g 之前）的代码。结果：backend 923 passed、6 failed、0 skipped；shared 103 passed、2 failed；frontend 67 passed，类型检查和生产构建通过；OCR Worker 主环境 66 passed、4 skipped，ocr 环境真实识别 4 passed；CLIP 17 passed。8 项失败全部是符号链接测试的 WinError 1314（普通权限，测试准备阶段失败）。修复 3 处：中文 PDF 预览空白（`PdfViewer.vue` 配置 CMap、标准字体、WASM、ICC，资源放 `frontend/public/pdfjs/`，与已装的 pdfjs-dist 6.5.438 逐文件一致，不是新下载）；两个测试不再写死 psycopg/httpx 的具体异常类名；向量检索测试不再写死余弦分数 2.0（2.19.1 实测 1.0）。真实产品测试走通了注册登录、上传处理、OCR 检索、删除、共享、CLIP 检索与降级、中文 PDF 预览。本机（macOS）复跑：`test_health.py`、`test_worker_main.py` 11 项通过，前端类型检查通过。**未测试（Not Tested）**：8 项符号链接测试待以开发人员模式重跑；Docker/compose；正式评测数据（候选数据集下载待批准）；Linux `RLIMIT_AS`；并发与长时间运行；极端真实文件；T24g、T24h、T24i 的代码；修复后的 PDF 预览在 macOS 上。逐项见 `docs/untested.md` 第 7 节；第 3 节的 38 项本轮已通过（只有汇总数字），Barry 于 2026-11-19 批准后已从 untested.md 删除，剩 T24g、T24i 的 3 项。修改记录 `docs/changes/windows-2026-11-19.md` |
| Windows 第三轮（W1–W3）核对 | 2026-11-21 | 1178e1c | 由 Codex 在 Barry 的 Windows 机器上按 `windows任务书.md` 执行（基线 `8fb5830`），推到 GitHub（`ef6d943`、`bba3a1b`、`df36ac1`、`bb3883c`）；Barry 指示“Merge and check them”后由本会话合并（`1178e1c`，无冲突，未 push）并在 macOS 上核对原始数据，没有重跑需要数据库的步骤。**W1：** backend 938 项中 6 项、shared 105 项中 2 项因 WinError 1314（符号链接权限）失败，其余通过，OCR Worker 70（4 skipped）、CLIP 56（17 skipped，均为 main 环境缺少 paddleocr/torch）；用例与 Mac 在 `8fb5830` 上收集到的完全相同；T24g 1 项、T24i 2 项通过，已从 `untested.md` 删除。**W2（T24j）：** DocVQA 500 张图、500 条查询、500 条 qrels，Mac 上脚本测试 12 passed、编号与引用全部正确（`validate` 只报图片不在 Mac 上）。**W3：** 10 个配置 × 3 次重复 + `reocr` 后 B2，独立重算的指标与 `metrics.json` 完全一致，重复间排名相同，`reocr` 前后 B2 排名逐条相同；B2 P@10 0.0424、R@10 0.4240、nDCG@10 0.3383，B3 低于 B2（仅流程验证，不作论文结论）。**发现：** mapping hash 因 Windows CRLF 签出与仓库不一致；`git_dirty: true`；两张图 OCR 子进程 `0xC0000005`；`docvqa-runs.zip` 进了 Git；处理过程的数字没有原始数据。详见 `docs/changes/windows-2026-11-21-核对.md`；剩余项排进任务书 W6、W7 |
| Windows 第四轮（W4–W8）核对 | 2026-11-23 | 75cffd5 | 由 Codex 在 Barry 的 Windows 机器上按 `windows任务书.md` 执行（基线 `fd0b5eb`；任务书里叫“第二轮”），推到 GitHub（`065e640`、`54d9760`）；Barry 指示“下载 GitHub 上的更新……确认测试是否已经完成”后由本会话合并（`75cffd5`，只新增文件）并在 macOS 上核对原始数据，没有重跑需要数据库的步骤。**完成：** W5 11.2–11.4、11.6；W6 12.2（backend 950 项 6 失败、shared 108 项 2 失败，都是 WinError 1314，用例与 Mac 在 `fd0b5eb` 上收集到的完全相同）、12.4 修复路径、12.5、12.6、12.8、12.11；W7 全部（13.1 由 Claude 在 Mac 上用同一权重重新编码，余弦相似度都是 1.0、排序相同；13.2 的合计峰值按原始数据更正为 5732.8 MB）；W8 16.3–16.6、16.7 A、16.8。**未通过：** W6 12.7（Windows 上 Ctrl+C 打断当前 OCR 任务，代码问题，§4）。**未完成：** W4 真实拖拽、W5 11.5（网络立刻回绝，测不到超时）、W6 12.3、12.9、12.10、W8 16.7 B；W6 12.4 第 10 步的判定标准定错了。改良方案写进 `windows任务书.md` 第 17 节 W9。**其他：** `output/SHA256SUMS.txt` 396 行中 291 行是对 CRLF 工作区文件算的、3 行对不上（小说明文件）；Claude 写的采样脚本把 OCR 识别子进程归错组。核对记录 `docs/changes/windows-2026-11-23-核对.md`；`docs/untested.md` 第 4 节删 14 行、改写 16 行，新增第 7.4 节 |
| Windows 第五轮核对 | 2026-11-25 | 217381f | 由 Codex 在 Barry 的 Windows 机器上执行，**测的代码是 `54d9760`**（不含 T24v–T24ac），任务书 W9 基本没有开始；Barry 告知后由本会话快进到 `217381f` 并核对原始数据。**完成：** W8 16.8 对照组、Docker Desktop 上的 compose 与 OpenSearch 镜像（OS-7 基本完成）、Linux 容器里的 `RLIMIT_AS`（部分）。**OCR 崩溃：** 复现了，但编排脚本取 `.ProcessId` 导致 Worker 没停掉、逐轮累积，“单 Worker 退化”不成立；按实际活着的数量重算：≤4 个 24 个任务 0 失败，≥5 个 10 轮每轮都有崩溃，日志有“页面文件太小”，判断为内存耗尽（`0xC0000005` 的因果是推断）。改良方案见任务书第 17.14 节。Docker Desktop、WSL、镜像装在 Windows 测试机上，Barry 说明不需要管（`docs/downloads.md` 第 5 节只作记录）。核对记录 `docs/changes/windows-2026-11-25-核对.md` |
| Windows W9 核对 | 2026-11-26 | 0629caa | 执行方在 Barry 的 Windows 机器上按 `windows任务书.md` 第 17 节执行，**测的代码是 `e1d61eb`**（含 T24aa–T24ag、T24ba–T24bh）；Barry 告知后由本会话快进到 `0629caa` 并核对原始数据。**完成：** 17.2（backend 1052 项中只有 6 项符号链接和 1 项测试写法问题失败；从没运行过的 12 项集成测试全部通过；mapping hash 与 Mac 一致）、17.1 Docker 补测（OS-7）、17.3、17.4、17.5、17.8、17.14、17.15、17.16、17.17；17.6 发现 Bug 1。**结论：** T24aa–T24ag 在 Windows 上全部验证；16 GB 机器上最多开 3 个 OCR Worker。**未完成：** 17.7、17.10、17.11（Barry 本人）；17.9 权限已有，shared 2 项通过，backend 6 项因临时目录不存在没跑起来。核对记录 `docs/changes/windows-2026-11-26-核对.md` |
| T24aa | 2026-11-23 | da6f29a | Barry 于 2026-11-23 批准（“先修 Ctrl+C”，来自 Windows 第四轮核对 §2 第 1、2 条）；不带 🔒。`backend/app/worker/runner.py`、`services/ocr_worker/ocr_worker/engine_process.py` 各加 `_poll`：`poll()` 遇到 `InterruptedError`（Windows 上按 Ctrl-C 时抛出，W6 12.7 实测）按剩余时间接着等；通用 Worker 子进程入口忽略 SIGINT（原来会把 `KeyboardInterrupt` 当作一次可重试的失败）。没有改表结构、接口、配置、附录 A，没有新依赖。已执行：`backend/` pytest 725 passed、229 skipped；`services/ocr_worker/` pytest 75 passed、4 skipped；ocr 环境真实识别 4 项通过；两处 ruff 通过；去掉修复后新增测试按预期失败。**未测试（Not Tested）**：Windows 上真实按 Ctrl+C（`windows任务书.md` 第 17.5 节）、macOS 上对着真实 Worker 按 Ctrl+C（本机没有 PostgreSQL），已登记 `docs/untested.md`。修改记录 `docs/changes/T24aa.md`，决策 D52 |
| T24ab | 2026-11-23 | 3d1eaf2 | Barry 于 2026-11-23 批准（“先修 R1”）；不带 🔒。新增 `shared/parent_watch.py`，`runner.py`、`engine_process.py` 的子进程入口调用：父进程被强制结束时子进程立即退出（W6 12.5 日志显示原来会继续跑完）。没有改表结构、接口、配置、附录 A，没有新依赖。已执行：`backend/` 726 passed、229 skipped；`shared/` 109 passed；`services/ocr_worker/` 76 passed、4 skipped；ocr 环境真实识别 4 项通过；三处 ruff 通过；去掉看门狗后两项强杀测试失败，恢复后各重复 6 次通过。**未测试（Not Tested）**：Windows 上的强制结束、真实 Worker 上的强制结束（`windows任务书.md` 第 17.5 节 C），已登记 `docs/untested.md`。顺带更正：代码复核建议里“退出码不同没有问题”的说法是错的，改列为 R5。修改记录 `docs/changes/T24ab.md`，决策 D53 |
| T24ac | 2026-11-23 | 664e54a | Barry 于 2026-11-23 批准（“修 R5”）；不带 🔒。`ocr_worker/__main__.py` 收到停止信号返回 130（与通用 Worker 一致），做满任务数仍返回 0；新增 `tests/test_main.py` 4 项。没有改表结构、接口、配置、附录 A，没有新依赖。已执行：`services/ocr_worker/` 80 passed、4 skipped；ocr 环境真实识别 4 项通过；ruff 通过；改之前新增测试 3 项失败；用真实信号驱动真实循环：bash 改之前被重新拉起、改之后停下，zsh 前后都能停。backend、shared 没有改动，没有重跑。**未测试（Not Tested）**：Windows 的 `run_ocr_worker_loop.ps1`（`windows任务书.md` 第 17.5 节 D），已登记 `docs/untested.md`。修改记录 `docs/changes/T24ac.md`，决策 D54 |
| T24ad | 2026-11-25 | 986474a | Barry 于 2026-11-25 选定（“No migration”）；不带 🔒（原计划加列带 🔒，改为用已有的 `started_at`）。`shared/tasks.py` 领取条件加重试间隔，两个 Worker 读 `TASK_RETRY_DELAYS_SECONDS`（默认 `30,120`）。没有改表结构、接口、附录 A，没有新依赖。已执行：`shared/` 124 passed；`backend/` 732 passed、237 skipped；`services/ocr_worker/` 82 passed、4 skipped；ocr 环境真实识别 4 项通过；三处 ruff 通过；去掉三处传参后新增测试各有失败。**未测试（Not Tested）**：领取 SQL 在真实 PostgreSQL 上（新增 8 项集成测试）、CLIP 短暂不可用后自己恢复（`windows任务书.md` 第 17.15 节），已登记 `docs/untested.md`。修改记录 `docs/changes/T24ad.md`，决策 D55 |
| T24ae | 2026-11-25 | dcbfb81 | Barry 于 2026-11-25 批准（“做 T24ae”）；不带 🔒。新增 `documents/requeue.py`、`documents/__main__.py`：`requeue-failed` 把失败的 embed、ocr 任务放回队列，默认演练，跳过已删除文档和旧版本 OCR 任务。没有改表结构、接口、配置、附录 A，没有新依赖。已执行：`backend/` 752 passed、240 skipped；ruff 通过；真实命令对着连不上的数据库退出码 1、不泄露口令；5 种改坏的写法都使新增测试失败。shared、OCR Worker 没有改动，没有重跑。**未测试（Not Tested）**：3 项集成测试（需要 PostgreSQL）、CLIP 恢复后补齐向量的全过程（`windows任务书.md` 第 17.16 节），已登记 `docs/untested.md`。修改记录 `docs/changes/T24ae.md`，决策 D56 |
| T24af | 2026-11-25 | c1f1df5 | Barry 于 2026-11-25 批准（“先做 R3”）；不带 🔒。`consistency/__main__.py`：检索服务不可用时只对检查过的类别说“没有需要修复的问题”，提示只写实际选了的索引类别，跳过重建时不打印重建的注意事项。退出码与修复行为没有变。没有改表结构、接口、配置、附录 A，没有新依赖。已执行：`backend/` 760 passed、240 skipped；ruff 通过；用修改前的代码跑，新增 8 项中 7 项失败。shared、OCR Worker 没有改动，没有重跑。**未测试（Not Tested）**：停掉真实 OpenSearch 后的输出（`windows任务书.md` 第 17.17 节），已登记 `docs/untested.md`。修改记录 `docs/changes/T24af.md` |
| T24ag | 2026-11-25 | 1bdcf07 | Barry 于 2026-11-25 批准（“先做 R4”）；不带 🔒。`runner.py` 只在 Linux 上设内存上限，其他系统不再每个任务打印，改由 Worker 启动时说明一次；新增 `frontend/public/favicon.svg` 并在 `index.html` 声明。R4 的 `ch` 残留不改（Barry 于 2026-11-25 决定保留现状（地址栏记的是最后一次真正执行的检索，刷新能恢复结果））。没有改表结构、接口、配置、附录 A，没有新依赖。已执行：`backend/` 769 passed、240 skipped；ruff 通过；前端类型检查、构建、17 个文件 207 项通过；浏览器里核对图标显示与请求；三处反证都使新增测试失败。shared、OCR Worker 没有改动，没有重跑。**未测试（Not Tested）**：Windows 上的 Worker 日志（`windows任务书.md` 第 17.2 节第 6 条）、Safari 与 Firefox 的图标，已登记 `docs/untested.md`。修改记录 `docs/changes/T24ag.md` |
| T24ba | 2026-11-25 | eee58fe | Barry 于 2026-11-25 批准（“批准，用建议选项”）；不带 🔒。新增 `documents/task_errors.py`，三个任务接口都经过 `to_task_out`：普通用户、被共享者看到清理过的失败原因，管理员看原文，数据库里不变。接口字段不变，没有改表结构、配置、附录 A，没有新依赖。已执行：`backend/` 802 passed、241 skipped（新增单元测试 42 项）；ruff 通过；把 `to_task_out` 改成总返回原文，新增测试失败；集成测试 3 个文件原样搬到 SQLite 替身上 82 通过、1 失败（`test_create_admin_command` 直连 PostgreSQL，替身覆盖不到）。shared、OCR、CLIP 没有改动，没有重跑。**未测试（Not Tested）**：新增的 1 项集成测试在 PostgreSQL 上，已登记 `docs/untested.md`。修改记录 `docs/changes/T24ba.md` |
| T24bb | 2026-11-25 | 26e8bd3 | Barry 于 2026-11-25 批准（“批准，用建议选项”）；不带 🔒。① 点“重试”没返回时又登录，不采用旧令牌的结果（`auth.ts`、`client.ts`）；② 文件列表只认最后一次加载，离开后停止（新增 `utils/latestRun.ts`）；③ 预览页之间跳转时重新创建（`App.vue` 的 key），没加载完就离开不再请求。只改前端，没有改后端、接口、附录 A，没有新依赖。已执行：类型检查；前端 17 个文件 210 项通过（新增 5 项）；撤掉 ① 后 3 项失败；生产构建；浏览器对着真实 FastAPI + SQLite 替身，修改前后各测一次。**未测试（Not Tested）**：PostgreSQL 上的真实后端、Windows、Chrome 以外的浏览器；三个 `.vue` 没有组件测试，已登记 `docs/untested.md`。修改记录 `docs/changes/T24bb.md` |
| T24bc | 2026-11-25 | 3bca177 | Barry 于 2026-11-25 批准（“批准，用建议选项”）；不带 🔒。新增 `src/i18n/`（中英文两套文字，类型约束结构一致）、`src/features/theme/`（主色、深浅色、语言按钮），所有页面的文字改为按当前语言取；登录页错误文字随语言切换；内容区底部留出浮动按钮的高度。检索页脚本和结构不变，只换文字。GLOBAL §3.1 注明例外（D60）。没有改后端、接口、附录 A，没有新依赖。已执行：类型检查；前端 19 个文件 226 项通过；生产构建；没有用不到的文字键；浏览器对着真实 FastAPI + SQLite 替身：英文界面四个页面没有残留中文（文件名、正文除外），确认框、分页随语言切换，配色与恢复默认，375×812 中英文五个页面浮动按钮零遮挡。**未测试（Not Tested）**：见 `docs/untested.md`“T24ba–T24be”。修改记录 `docs/changes/T24bc.md`，决策 D60 |
| T24bd | 2026-11-25 | 49a1702 | Barry 于 2026-11-25 批准（“批准，用建议选项”）；不带 🔒。新增 `src/features/tasks/`：处理详情对话框、批量重试（最多同时 4 个）、自动刷新、预览页失败提示与“有新的识别结果”；文件列表的列名和状态改为“解析状态、已解析、解析失败”等（文档状态只跟随解析任务，D27），接口取值不变。`api/client.ts` 的请求可以取消。没有改后端、接口、附录 A，没有新依赖。已执行：类型检查；前端 26 个文件 334 项通过；生产构建；变异 5 项都使测试失败（取消请求原来没有测试，撤掉实现不会失败，补了 2 项）；浏览器对着真实 FastAPI + SQLite 替身：重试后离开零请求，连点只发一批，部分失败 → 重试 → 进度 → 新文字提示 → 之后 7 秒零请求，被共享者只看到清理过的原因且没有重试按钮，取文档连续失败两次后自己恢复。**未测试（Not Tested）**：见 `docs/untested.md`“T24ba–T24be”。修改记录 `docs/changes/T24bd.md` |
| T24be | 2026-11-25 | e8c0853 | Barry 于 2026-11-25 批准（“批准，用建议选项”）；不带 🔒。新增 `src/features/search-motion/`：检索页的扫描加载、启动、待机动画，登录页星尘 logo；新的检索取消旧请求、丢弃旧返回，30 秒没返回算失败。与克隆库不同：**结果一到就收拢**（D60）；`/motion-lab` 只在开发模式有。没有改后端、接口、附录 A，没有新依赖；抄入 Lucide `file-text` 的 5 条路径（`docs/downloads.md` §2.8）。已执行：类型检查；前端 31 个文件 374 项通过，乱序两次也通过；生产构建里没有演示页；变异 2 项都使测试失败；浏览器对着真实 FastAPI + SQLite 替身：后端 10、50、300、1200、4500 毫秒返回，分别 436、474、724、1618、4925 毫秒显示结果（克隆库原来 4.02–4.03 秒），连点只发一次，检索中改词、改开关只显示新结果，收拢途中再搜、关掉全部通道、出错重试、离开页面均正常；生产构建打开 `/motion-lab` 回到登录页。**未测试（Not Tested）**：见 `docs/untested.md`“T24ba–T24be”。修改记录 `docs/changes/T24be.md`，决策 D60 |
| T24bf | 2026-11-25 | 7b64449 | Barry 于 2026-11-25 批准（“批准，用建议选项”）；不带 🔒。只改文档：`docs/test.md` 补 T24ba–T24be 的结果，更正 T24bd 的变异项数。Windows 任务书单列为 T24bg，等 Barry 看过草稿 |
| T24bg | 2026-11-25 | c82b33c | Barry 于 2026-11-25 批准（“按草稿改”）；不带 🔒。只改文档。与草稿不同：W4 第 10.2、10.5 节只加注不改原文（W4 已在旧界面上执行过）；造失败的三步换成做得到的办法（截断的 docx 上传时就被拒绝，改用加密 PDF；改存储目录得到的是项目自己的错误，改为在测试库里直接改 `error`；强杀 OCR Worker 太慢且不保证部分失败，改为缩短识别超时）。已执行：任务书里的样本脚本原样运行，`locked.pdf` 解析失败且不可重试、`scan6.pdf` 产生 6 个 OCR 目标；引用的界面文字逐条在代码里找到。**未测试（Not Tested）**：第 17.18 节本身要在 Windows 上执行。修改记录 `docs/changes/T24bg.md` |
| T24bh | 2026-11-25 | 74c950d | Barry 于 2026-11-25 批准（“改”）；不带 🔒。扫描区的“正在打开文件…”“正在阅读第 n / 6 个文件”合并为“正在检索…”，“正在整理答案…”改为“正在整理结果…”（英文同改）：6 是卡片数，系统也不打开文件、不生成答案（GLOBAL §8.1、§13）。只改前端文字，没有改后端、接口、附录 A，没有新依赖。已执行：测试先改，改之前 3 项失败；类型检查；前端 32 个文件 378 项通过（新增 2 项，检查中英文里没有计数和“阅读、打开、答案”）；生产构建里没有旧文字；浏览器对着真实 FastAPI + SQLite 替身：6 秒的检索跨两轮动画，中文依次是“正在检索…”“正在整理结果…”，英文对应，出错提示不变。后端没有改动，没有重跑。**未测试（Not Tested）**：同 T24be。修改记录 `docs/changes/T24bh.md` |
| T24ah | 2026-11-26 | 619dea8 | Windows W9 核对 Bug 1，Barry 于 2026-11-26 批准（“修bug1”）；不带 🔒。`backend/app/db/session.py` 的 `make_engine()` 新增必填参数 `connect_timeout_seconds`，经 `connect_args` 交给 psycopg（`connect_timeout`）；API 和四个命令行工具（auth、consistency、documents、experiments）、Alembic 迁移用新配置 `DATABASE_CONNECT_TIMEOUT_SECONDS`（默认 5，整数 2–300），通用 Worker 处理任务的引擎沿用 `WORKER_DB_CONNECT_TIMEOUT_SECONDS`。超时后 psycopg 抛 `OperationalError`，API 按原有处理返回 503 `DATABASE_UNAVAILABLE`。没有改表结构、索引、接口、附录 A，没有新依赖。已执行（macOS，main 环境）：`backend/` 814 passed、241 skipped；ruff 通过。新增单元测试 2 项：用一个只监听、从不回应的端口在 macOS 上复现“一直等”，`/api/auth/me` 约 2 秒返回 503；引擎把 `connect_timeout` 传给驱动。反证：去掉 `connect_args` 后两项都失败（请求过 30 秒仍挂着）。**未测试（Not Tested）**：Windows 上重测 `windows任务书.md` 第 17.6 节第 3a 步；改过的集成测试夹具和 Alembic 迁移入口没有对真实 PostgreSQL 跑过，已登记 `docs/untested.md` 第 7.5 节。Bug 2、`git_dirty` 没有做（Barry 只批准了 Bug 1）。修改记录 `docs/changes/T24ah.md` |
| T24ai | 2026-11-26 | cd1c31c | Windows W9 核对 Bug 2，Barry 于 2026-11-26 批准（“Fix both”）；不带 🔒。只改测试：`backend/tests/unit/test_task_errors.py::test_database_address_is_hidden` 原来真的去连 `127.0.0.1:1`，指望错误文字里带地址；Windows 上得到的是不带地址的 `connection timeout expired`，前置断言失败。改为用真实的异常类型（`sqlalchemy.exc.OperationalError` 包 `psycopg.OperationalError`）包一段写死的文字，文字是 macOS 上同样连接实际得到的原文，存进任务表后的格式与原来逐字相同。被测的 `public_task_error()` 没有改。没有改产品代码、配置、附录 A，没有新依赖。已执行（macOS，main 环境）：该文件 42 项通过；`backend/` 814 passed、241 skipped；ruff 通过。**未测试（Not Tested）**：Windows 上重跑，已登记 `docs/untested.md` 第 7.5 节。修改记录 `docs/changes/T24ai.md` |
| T24aj | 2026-11-26 | fc259ae | Windows W9 核对“其他”第 1 条，Barry 于 2026-11-26 批准（“Fix both”）；不带 🔒。`backend/app/modules/experiments/environment.py` 的 `machine_info()` 改用 `git status --porcelain --untracked-files=no`：未跟踪的文件（Windows 上的 `output/` 等）不再让 `git_dirty` 变成 true，已跟踪文件有未提交改动时仍为 true。`config.json` 的字段和格式不变；以前的实验记录里的 true 可能只是因为有未跟踪文件。没有改表结构、接口、附录 A，没有新依赖。已执行（macOS，main 环境）：新增单元测试 1 项（临时 git 仓库：只有未跟踪目录时为 false，改已跟踪文件后为 true），换回旧代码时失败；`backend/` 815 passed、241 skipped；ruff 通过。**未测试（Not Tested）**：Windows 上实际跑一次实验看 `config.json`，已登记 `docs/untested.md` 第 7.5 节。修改记录 `docs/changes/T24aj.md` |
