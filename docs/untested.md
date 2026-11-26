# 未测试清单（Not Tested）

更新日期：2026-11-26（按 Windows W9 的核对结果删除已验证的 26 行、改写 4 行，第 1 节合计归 0，新增第 7.5 节，见 `docs/changes/windows-2026-11-26-核对.md`）。再上一次：2026-11-25（T24ag 登记 1 行，T24af 改 2 行、删 1 行；T24ae 登记 3 项、T24ad 登记 8 项未运行的集成测试和各自的实测；同日稍早按 Windows 第五轮的核对结果改写 Docker、Dockerfile、`RLIMIT_AS`、OCR 崩溃 6 行，第 7.4 节加 2 行，见 `docs/changes/windows-2026-11-25-核对.md`；这一轮没有测新代码）。再上一次：2026-11-23（按 Windows 第四轮（W4–W8，执行者 Codex，基线 `fd0b5eb`）的核对结果更新：第 4 节删除已验证的 14 行、改写 16 行，第 6.2 节删去 OS-6，第 7.2 节改写 2 行，第 7.3 节删 2 行、改写 3 行，新增第 7.4 节；核对见 `docs/changes/windows-2026-11-23-核对.md`。再上一次：2026-11-21（20:40 按 Windows 第一轮（W1–W3，执行者 Codex，基线 `8fb5830`）的核对结果更新：删除第 1、3 节的 T24g 1 项、T24i 2 项（Windows `output/windows-w1/backend.xml` 中通过），删除第 4 节已由 W3 原始数据证实的 4 行、改写 7 行，第 7 节新增 7.3；核对见 `docs/changes/windows-2026-11-21-核对.md`。同日 14:37 补登 T24p 漏登的一项，并注明 T24d、T24k、T24l、T24m、T24o 的条目已排进 `windows任务书.md` W5；同日稍早，T24s 完成后登记前端界面优化的 3 项未验证性质，见第 4 节“T24s 前端界面优化”；自动化测试的合计不变。同日稍早：按 T24k–T24n 的提交修正汇总数字和 Windows 未覆盖范围，没有运行任何测试。再上一次：2026-11-19 T24i 完成后，按 Barry 批准整理，并删除 Windows 第二轮已通过的 38 项）

这里列出**已经写好但从未实际执行过**的测试，以及其他没有经过验证的性质。
规则来自 GLOBAL.md“测试执行限制与代码验证要求”：跑不了的测试不强行执行、不安装工具，
在这里如实登记，并对相关代码做人工复核。

> **2026-11-19 整理（Barry 批准）：** 已在 2026-11-16 Windows 补测中实际通过的项目从本文件删除，包括：原第 3 节的 11 个连调文件（T03、T06、T07、T08、T13、T14、T15、T16、T17、T18、T19，共 190 项，含原第 2 节列出的全部 🧪）、第 6 节的 OS-1、OS-3、OS-4、OS-5、OS-8、OS-9、OS-10，以及第 4 节中因此得到验证的 7 行（两个 mapping 被 OpenSearch 接受、检索查询体被接受、高亮转义、`shared/tasks.py` 的 SQL、真实子进程里的处理函数、OCR Worker 完整链路、OpenSearch 启动与 smartcn 分词）。补测环境：Windows 11、Python 3.14.0、PostgreSQL 16.15、OpenSearch 2.19.1 + analysis-smartcn；证据在 `change-deepseek-v4/`（JUnit 原始结果 `test-results/integration-results.xml`），记录见 DEVPLAN §5“T00–T19 补测”“修复合入”。
>
> 两点限制，写论文和测试报告时要照实说明：（1）通过的是 Windows 上的验证副本，本仓库在 macOS 上没有 PostgreSQL 和 OpenSearch，没能复跑；副本与本仓库在合入 C01–C12 后逐行一致。（2）2026-11-16 之后，T21–T24 和 D34 的复核修正又改过部分代码路径（检索编排、实验框架、一致性检查、cleanup），这些改动之后上述 190 项没有再跑过；它们新增的测试仍登记在下面。
>
> 计数：本机 backend 跳过 212 项，其中 188 项属于上述 11 个文件（Windows 上同一批文件收集到 190 项，差异来自 `test_migrations.py`、`test_auth.py` 各多 1 项），剩下 24 项见第 1 节。

> **2026-11-19 Windows 第二轮补测（`27b51b2`，基于 `50b244b`，即 T24f 之后、T24g 之前的代码）：** 由 Barry 在 Windows 上完成，原始说明是 `docs/changes/windows-2026-11-19-原始说明.txt`，截图在 `docs/screenshots/windows-2026-11-19/`（T24r 从仓库根目录和 `output/playwright/` 移过来）；本会话没有重跑，只是据此登记。汇总：backend 923 passed、6 failed、0 skipped；shared 103 passed、2 failed；frontend 67 passed，类型检查和生产构建通过；OCR Worker 主环境 66 passed、4 skipped，ocr 环境真实识别 4 passed；CLIP 17 passed。8 项失败全部是符号链接测试的 WinError 1314（见第 7 节）。
>
> **同日删除（Barry 批准）：** backend 0 skipped 说明原第 3 节中 T24g 之前的 38 项（T22 `test_search_db.py` 1 项；`test_experiments_db.py` 中 D34 3 项、T24 4 项、T24c 4 项；`test_embed_db.py` 8 项；`test_vector_index_live.py` 8 项；`test_document_text.py` 的 T24e 10 项）以及 T24c、T24e 之后要重跑的 `test_migrations.py`、`test_ocr_worker_db.py`、`test_document_text.py` 原有 11 项都在这一轮执行并通过，已按 Barry 于 2026-11-19 的批准（“Delete them”）从本文件删除，连同第 2 节的 🧪 三行和第 4 节中只由这些测试覆盖的 12 行。限制：这一轮只有汇总数字，没有逐项的原始结果（JUnit XML）；通过的是 `50b244b` 的代码，之后 T24g、T24i 只改了实验框架（`experiments/__main__.py`），没有改这些测试覆盖的代码。T24g、T24h、T24i 登记的项目仍未测试。

**复核不等于测试通过。** 本文件中的任何一项，在实际运行通过之前，都不能在论文、测试报告或答辩中写成“已验证”。

维护方式：每完成一个任务，把新增的未测试项加进来；某一项实际运行通过后，从这里删除，并在 DEVPLAN §5 对应任务的备注里写明运行环境和结果。

## 1. 汇总

| 任务 | 测试文件 | 未测试项数 | 原因 | 代码复核 |
|---|---|---|---|---|
| **合计** | | **0** | | 本机 backend 跳过的 229 项 = 2026-11-16 通过的 188 项 + 2026-11-19 通过的 38 项 + 2026-11-21 通过的 3 项（T24g 1 项、T24i 2 项）。注意几轮基于不同的提交。2026-11-23 Windows 第四轮（W6 12.2）在 `fd0b5eb` 上又跑了一遍全部 950 项，除 6 项符号链接外都通过；之后只改了前端（T24v–T24z） |

T05（存储）、T09（PDF 解析器）、T11（Word、Excel、图片解析器）和 T12（切分）不需要数据库，它们的测试全部在本机执行并通过，没有未测试项。

对照（数字取自各任务的 DEVPLAN §5 记录）：2026-11-21（T24l）本机实测 `backend/` 718 项通过、229 项跳过，`services/ocr_worker/`（main 环境）71 项通过、4 项跳过；T24k 时 `backend/` 711 项通过、229 项跳过，`shared/` 108 项通过；T24m、T24n 时 `frontend/` 70 项通过，T24p 时 73 项，T24s 时 93 项（10 个文件）。T24k–T24n、T24p、T24s 新增的测试都是单元测试，全部在本机运行过，跳过数没有变化，所以上面的合计仍为 3。2026-11-19（T24i）本机实测 `backend/` 709 项通过、229 项跳过；T24g 时为 705 项通过、227 项跳过；T24e 时为 703 项通过、226 项跳过；T24c 时为 692 项通过、216 项跳过，`shared/` 105 项通过；T24 时为 678 项通过、212 项跳过。

## 2. 影响最大的几项

原来列在这里的 🧪 测试（T06、T07、T08、T13、T14、T15 在 2026-11-16；T21 两项、T22 一项在 2026-11-19 第二轮）都已在 Windows 补测中通过。**目前没有仍未运行的 🧪 测试。**

## 3. 逐项清单

括号里的数字是该测试的参数化用例数，未标注的为 1。

（2026-11-26：T24ad 8 项、T24ae 3 项、T24ba 1 项在 Windows W9 全部通过，已删除。）目前没有写好但从未运行的自动化测试。（2026-11-21 20:40：原来这里的 T24g `test_preflight_reports_mixed_ocr_models`、T24i `test_reocr_requeues_finished_ocr_tasks_of_the_current_version`、`test_reocr_refuses_while_parse_or_ocr_tasks_are_unfinished` 在 Windows 第一轮通过，已删除。）

## 4. 不是测试、但同样没有验证过的性质

| 项目 | 说明 | 记录位置 |
|---|---|---|
| Worker 子进程的内存上限 | 用 `RLIMIT_AS` 实现，只在 Linux 上有效；开发机是 macOS，内核基本不执行这个限制 | `decisions.md` D16 |
| 后端连上真实数据库后的整体运行 | **部分验证（2026-11-19 Windows 第二轮）。** Windows 上用真实 PostgreSQL、OpenSearch、OCR Worker、CLIP 服务走通了注册、登录、上传、状态轮询、下载、OCR 检索、删除、共享与取消共享、CLIP 检索与降级。macOS 本机仍没有跑过 | DEVPLAN §5“Windows 第二轮补测” |
| 前端与真实后端的联调 | **大部分已验证（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W4 在真实后端、真实 CLIP 服务上核对了文件页（五列、来源、筛选空态）、拖拽区之外的上传与自动刷新、共享对话框、检索页（`ch` 参数、改开关自动重查、三格名次、RRF 融合分、耗时、CLIP 在线 / 降级 / 恢复）、预览页返回，W5 11.6 核对了生产构建。仍未验证：T24v–T24z 的登录页（见下面“T24v–T24z”一节；W4 测的是这些提交之前的代码）、真实鼠标拖入（`windows任务书.md` 第 17.6、17.7 节） | DEVPLAN §5 T10、T16、T24s |
| 前端页面组件的自动化测试 | 没有写，项目里也没有组件测试工具（加装需要 Barry 同意）。前端单元测试（T10 时 48 项，2026-11-21 T24n 时 70 项，T24s 时 93 项，2026-11-23 T24z 时 205 项）只覆盖接口封装、格式化、摘要清洗、位置格式和检索通道的纯函数（T24s 的 `utils/channels.ts`），以及 T24v–T24z 从登录页抽出的纯函数（跳转规则、会话恢复、表单规则、提交流程、错误文字、服务状态，`tests/login/`、`tests/auth.test.ts`）；登录页的组件本身（`LoginForm.vue` 等）、文件列表、共享对话框、检索页、预览页、PDF 查看器只做过人工浏览器检查 | DEVPLAN §5 T10、T16、T24v–T24z |
| PDF 预览在真实文件上的表现 | **部分验证。** 2026-11-19 Windows 第二轮发现中文 PDF 预览空白（pdf.js 没有配置 CMap 等资源），修复后用一份真实中文 PDF 在真实后端上看到正常显示（截图 `docs/screenshots/windows-2026-11-19/pdf-preview-e2e-fixed.png`）。修复后的预览在 macOS 浏览器里没有看过；扫描件、加密、接近 50 MB 的 PDF 仍没有试过 | `decisions.md` D29 |
| 真实后端经开发代理的访问 | **部分验证。** T05–T10 核查时启动了真实后端（数据库地址指向不存在的端口）和真实的前端开发代理，用 curl 验证了不需要数据库的路径：健康检查、数据库不可用返回 503、未登录 401、参数校验 422、未登录上传（multipart 经代理）401、超大上传 413。需要数据库的路径（登录成功之后的一切）仍未验证 | DEVPLAN §5 核查记录 |
| Windows 上的运行 | 2026-11-23 Windows 第四轮（W6 12.2，基线 `fd0b5eb`）：backend 950 项中 6 项、shared 108 项中 2 项因 WinError 1314 失败，其余通过，收集到的用例与 Mac 在同一提交上完全相同；OCR Worker、CLIP（含真实模型）、前端 93 项、ruff 都通过。之前三轮的情况见 DEVPLAN §5。`fd0b5eb` 之后只改了前端（T24v–T24z），在 Windows 上没有跑过（`windows任务书.md` 第 17.2 节） | DEVPLAN §5“T00–T19 补测”“Windows 第二轮补测” |
| PDF 解析器在真实文件上的表现 | T09 的测试用 PyMuPDF 现场生成的 PDF；没有用真实的扫描件、多栏排版、带表格或带水印的 PDF 验证过，阈值 20 也没有实验依据 | `decisions.md` D20 |
| Word、Excel、图片解析器在真实文件上的表现 | T11 的测试文件是用 python-docx、openpyxl、PyMuPDF 现场生成的；没有用 Microsoft Word / Excel / WPS 实际保存的文件、手机或相机拍的照片验证过。尤其是 Excel 公式的缓存值，测试里是手工改 XML 模拟的 | `decisions.md` D24 |
| mapping 文件随安装包发布 | T17 起 mapping 在 `shared/text_index/mappings/`，`shared/pyproject.toml` 声明了 package-data（`shared.text_index` 下的 `mappings/*.json`）。两个环境都是 editable 安装，没有做过普通安装来验证文件确实被打包。验证方法：在一个临时虚拟环境里 `pip install ./shared`（会联网下载依赖，按规则先征得同意），然后确认 `site-packages/shared/text_index/mappings/` 下有两个 JSON 文件 | `decisions.md` D26、D30 |
| B0–B2 实验 | **流程已验证（2026-11-21 Windows 第一轮 W3）：** 用 DocVQA 500 张英文扫描页在真实 PostgreSQL、OpenSearch 上跑通了导入、处理和运行，Claude 用 `results.jsonl` 独立重算的指标与 `metrics.json` 一致。DocVQA 只有英文文字型查询，数字不能当论文结论；**正式评测数据集和标注仍然没有**（T25） | `decisions.md` D32 |
| 一致性检查对真实 OpenSearch 的操作 | **已验证（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W5 11.3 在真实 OpenSearch 上做了新建索引后的检查（没有误报）、人为制造结构差异、`rebuild-indices` 与 `--force` 重建；W6 12.4 在 500 个文档上做了单个文档重建（片段与向量）、孤立文件删除，修复后计数不变。检索服务不可用时 `repair` 多打的一行误导提示，T24af 已修，待任务书第 17.17 节看实际输出 | `decisions.md` D31 |
| OCR 在真实文件上的表现 | 只用 PyMuPDF 现场生成的扫描版 PDF 页、图片和空白图验证过；没有真实扫描件、手机照片、多栏排版、竖排或手写文字 | `decisions.md` D30 |
| OCR 子进程的内存上限 | `OCR_WORKER_MEMORY_LIMIT_MB` 用 `RLIMIT_AS` 实现，只在 Linux 上有效；本机（macOS）启动时打印“无法设置识别子进程的内存上限”，只受超时保护。没有在 Linux 上验证过 | `decisions.md` D16、D30 |
| smartcn 的切分效果 | **英文部分有数据（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W8 16.6 实测 smartcn 对英文转小写、做 Porter 词干化、不去停用词、在标点处切开（详见核对记录第 3 节）。中文切分对 B0–B2 的影响仍要到阶段五（T25 之后） | `decisions.md` A13 |
| cleanup 硬删除与续租的配合 | 硬删除后任务记录被级联删除，父进程的下一次续租会把子进程按“租约丢失”终止。代码把硬删除放在最后一步来规避，但真实时序没有观察过 | `decisions.md` D27 |
| 切分参数对检索效果的影响 | 默认 500 字、重叠 50 字是经验值。“片段长度、重叠、是否给 Excel 片段补表头”对 B1、B2 的影响要到阶段五才有数据 | `decisions.md` D25 |
| zip 与像素上限的默认值 | 200 MB、5000 个条目、1 亿像素都是经验值。**拒绝路径已验证（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W8 16.8 在 Windows（没有内存上限）上用真实 Worker 处理了解压后 314 MB 的 docx、6001 个文件的 docx、12000×9000 的 PNG，三个都在解析前被拒绝、`attempts=1`，Worker 峰值 123.6 MB。接近上限但合法的真实大文件的内存和耗时仍没有测 | `decisions.md` D24 |
| smartcn 下的高亮效果 | 摘要是否落在命中词附近、长度是否接近 `SEARCH_SNIPPET_CHARS`，没有实际看过 | `decisions.md` D28 |
| IK 分词 | T00 环境实测中仍未完成的部分：IK（没有匹配 OpenSearch 2.19.1 的版本）。OS-6（并发内存）已由 W7 13.2 完成：六组进程同时运行 15 分钟，合计峰值 5732.8 MB、最低可用内存 886.6 MB（Claude 按原始数据重算） | 第 6 节 |

### T20 CLIP 服务（2026-11-17 登记）

T20 的测试都在本机实际运行过（接口测试 39 项，真实模型测试 17 项，见 DEVPLAN §5 T20）。下面是没有验证过的性质：

| 项目 | 说明 | 记录位置 |
|---|---|---|
| CPU 以外的设备 | `CLIP_DEVICE=mps`、`cuda` 从未运行；只核对过“选了不支持的设备就报错退出”的代码 | `decisions.md` D33 |
| 其他操作系统 | macOS（arm64）、Windows（W1、W6 12.2 真实模型 17 项通过，W7 13.1 跨机器向量一致）都运行过；Linux 没有测 | `decisions.md` D33 |
| 真实图片 | 测试图片都是现场生成的纯色或色块图。真实照片、带 EXIF 的手机照片、渐进式 JPEG、接近 50 MB 的大图没有测 | — |
| 并发与长时间运行 | **部分数据（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W7 13.3 在 OCR 负载下连续 400 次检索，图像通道全部 ok；没有并发压测，没有长时间运行观察内存；吞吐和内存留给 T27 | DEVPLAN T27 |

### T15–T19 复核修正（2026-11-17 登记，见 `decisions.md` D34）

| 项目 | 原因 | 代码复核 |
|---|---|---|
| `consistency repair --fix index`、`rebuild-indices` 给解析失败的文档写回 `doc_meta` | 完整路径需要 PostgreSQL；`reindex_document` 本身有单元测试（已通过） | 已复核 |
| PDF 预览的绘制排队 | 只对着临时模拟接口、用一份 5 页的测试 PDF 检查过；没有自动化测试 | 已复核 |

### T21 图片向量与向量索引（2026-11-19 登记，见 `decisions.md` D35）

| 项目 | 说明 | 记录位置 |
|---|---|---|
| 一致性检查的向量部分 | **部分验证（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W6 12.4 在真实数据上检出“向量不在向量索引里”，`--fix index` 按数据库重建后检查干净。其余 4 种向量检测项和 `embeddings` 修复类别仍只有单元测试 | `decisions.md` D35 |

### T22 检索 v2：图像通道（2026-11-19 登记，见 `decisions.md` D36）

| 项目 | 说明 | 记录位置 |
|---|---|---|
| 并行线程在真实负载下的表现 | **部分数据（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W7 13.3 在 OCR 负载下连续 200 次检索（间隔 0.5 秒），图像通道全部 ok，总耗时 P50 200 ms、P95 279 ms。没有多个请求同时发出的并发测试 | `decisions.md` D36 |
| 3 秒查询超时是否合适 | **有数据（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** OCR 负载下图像通道耗时 P50 195.5 ms、P95 275.1 ms，空闲时 66.0 / 171.1 ms，400 次都没有超时。embed 批量运行时（CLIP 服务同时在编码图片）的排队没有量过，留给 T27 | `decisions.md` D36 |

### T23 前端 v2（2026-11-19 登记，见 `decisions.md` D37）

前端单元测试（缩略图加载、命中依据、降级提示）在本机执行并通过；浏览器检查只对着临时模拟后端做过。以下没有验证：

| 项目 | 说明 | 记录位置 |
|---|---|---|
| 与真实后端、真实 CLIP 服务联调 | **已验证（通道部分）（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W4 核对了通道标记、三格名次、CLIP 停服降级与恢复。图片缩略图、图片证据在真实后端上的显示只看了截图，没有逐项核对 | `decisions.md` D37 |
| 检索页组件的自动化测试 | `SearchView.vue` 没有组件测试；开关、地址栏、缩略图显示只靠浏览器手动检查 | `decisions.md` D37 |

### T24f 预览页“抽取文本”标签页（2026-11-19 登记，见 `decisions.md` D45）

| 项目 | 说明 |
|---|---|
| 跳到命中片段后的自动滚动 | 这次检查时浏览器面板处于隐藏状态，`requestAnimationFrame` 不触发，滚动那一步没有执行。用改动前的代码在同一环境下对照，同样不滚动，所以不是 T24f 引入的；但 T24f 之后 Word/Excel 和抽取文本标签页的滚动都没有实际看到过 |
| 与真实后端联调 | 抽取文本标签页、`view=` 参数、默认标签页只对着临时模拟接口检查过 |
| 页面组件的自动化测试 | 没有（项目里没有组件测试工具）；只有 `initialPreviewTab` 的 5 项单元测试 |

### T24p Element Plus 按需引入（2026-11-21 补登，见 `docs/changes/T24p.md`）

T24p 完成时 DEVPLAN §5 写了这一项未测试，但当时没有登记到本文件，2026-11-21 14:37 补登。

没有剩余项。（2026-11-23：W5 11.6 用 `npm run preview` 打开了生产构建，上传、检索、PDF / 图片 / Word 预览都正常，没有未解析的 `<el-…>` 标签；已删除。）

### T24s 前端界面优化（2026-11-21 登记，见 `docs/changes/T24s.md`、`decisions.md` D48）

已执行并通过：类型检查；前端 10 个文件 93 项单元测试（新增 `channels.test.ts` 20 项）；生产构建（首屏 JS 约 483 KB，与 T24p 持平）；`src` 下没有写死的十六进制色值；浏览器对着临时模拟后端（scratchpad 里的 Node 脚本，不在仓库里，返回虚构数据）以 1280×800、375×812 截图核对文件页、脚本派发的 drop 事件（一个成功、一个被拒并显示原因）、检索页说明状态与全通道结果、关闭文件名通道后自动重检（`ch=body,ocr,image`）、CLIP 不可用时的降级显示、预览页标题区、窄屏布局，控制台只有被拒文件预期的 415。以下没有验证（已排进 `windows任务书.md` 第 10 节 W4，2026-11-21 14:26 添加；做完后按报告删除或改写对应行）：

| 项目 | 说明 | 代码复核 |
|---|---|---|
| 与真实后端联调 | **已验证（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W4 第 10.2 节逐项核对通过（`/health` 与 CLIP 状态、各通道 `status` 与 `took_ms`、三格名次、RRF 融合分、上传成功）。偏差两处：停后端后刷新跳登录页（T24x 已修，待第 17.6 节重测）；四个开关全关后地址栏保留上一次的 `ch`（Barry 定为保留现状，不算偏差） | 已复核 |
| 用鼠标从系统文件管理器真实拖入文件 | 本次是用脚本派发 drop 事件模拟的；真实拖放时浏览器给出的 `dataTransfer.files`、拖到子元素上时的 dragleave 没有实际看过 | 已复核：`onDrop` 取 `event.dataTransfer.files` 交给与点击选择相同的上传队列；dragenter、dragover 都 `preventDefault`（否则浏览器会直接打开文件）；dragleave 只在真正离开拖放区时取消高亮 |
| Chrome 以外的浏览器 | **Edge 已看（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W4 在 Chrome 157、Edge 158 上看过，400 px 窄窗正常。Firefox（那台机器没装）、Safari 没有看过 | 已复核：样式里用到的较新特性只有 `min()`、`:focus-visible`、flex 的 `gap` 和 CSS 变量；`onDragLeave` 依赖的 `relatedTarget` 在部分 Safari 版本可能为 null，只会让高亮闪一下 |

### T24v–T24z 登录页修复移植（2026-11-22 登记，见 `docs/changes/T24v.md` 起）

从克隆库 `feat/search-motion` 的登录页结构优化 L1–L8 移植，只改前端。每个任务都执行了类型检查、单元测试、生产构建，并对着临时模拟后端（scratchpad 里的 Node 脚本，按 `docs/api.md` 应答，不在仓库里）在内置浏览器里检查过。以下没有验证。已排进 `windows任务书.md` 第 17.6 节 W9（2026-11-23 添加，第 11 步“连按回车只发一次”同日补上）：停机刷新保留令牌与重试、数据库不可用、T24z 两种提示与耗时、表单内错误、令牌 60 秒过期后回原页面、已登录打开登录页、`/\evil.com`、连按回车。**没有安排**的三项，原因：“已注册但登录失败”在真实环境里很难让登录恰好在注册之后失败；“网络发出去没有应答时切换页面要等多久”和“数据库主机不应答时 `/health` 的耗时”需要专门搭不应答的地址，等 17.3 的本地监听做法验证过再议；读屏软件朗读需要 Barry 本人用讲述人或 VoiceOver 听，没有排期。做完后按报告删除或改写下表对应行：

| 项目 | 说明 | 代码复核 |
|---|---|---|
| T24x 与真实后端联调 | **大部分已验证（2026-11-26 W9 17.6，`docs/changes/windows-2026-11-26-核对.md`）：** 停后端刷新、恢复后重试都通过。数据库停掉、后端开着时 `/api/auth/me` 在 Windows 上一直挂着不返回（Bug 1，原因在 `make_engine()` 没有连接超时，不是 T24x 的问题），所以“数据库不可用时保留令牌”没有走通 | 待 Bug 1 修复后重测 |
| T24y 读屏软件 | 真实后端上的错误提示已由 W9 17.6 验证（2026-11-26）。`el-alert` 的 `role="alert"` 没有用 VoiceOver 等读屏软件实际听过 | — |

### T24ba–T24be 克隆库前端整体放入（2026-11-25 登记，见 `docs/changes/T24ba.md` 起）

已执行：每个任务的类型检查、单元测试、生产构建；浏览器（Chrome 内核）对着**真实的 FastAPI 应用 + SQLite 替身**检查（只替换引擎、列类型和 `/health` 的数据库探测，没有提交）。替身不等于 PostgreSQL。

| 项目 | 说明 | 代码复核 |
|---|---|---|
| 真实的 PostgreSQL、Worker、OpenSearch、CLIP、OCR | 任务状态由脚本改动，检索结果是注入的（OpenSearch 没启动时的 503 是真实的）。任务领取、真实处理过程没有参与 | 已复核：用到的接口和错误码没有变 |
| Windows、Safari、Firefox、Edge、真机触屏、读屏软件 | 都没有看过。Windows 第四轮的界面结果（W4 10.2、截图 `windows-2026-11-23-t24s`）基于改动前的界面，要重测 | — |
| T24bc 中英文、配色 | 只在内置浏览器里看过；翻译没有请人校对 | 已复核：`i18n.test.ts` 保证两套文字结构一致、英文里没有中文；存储读写失败时用默认值 |
| T24bd 任务面板 | 真实 Worker 上的完整流程没有走过：停掉 CLIP → 上传图片 → embed 失败 → 打开 CLIP → 点重试 → 图像检索能搜到；停掉 OCR Worker → 扫描件部分页失败 → 重试 → OCR 文字能搜到。T24ad 的重试间隔期间只看过造出来的 `pending`。任务接口不分页，几百个任务时的大小和 3 秒一次的开销没有量过。`TaskDialog.vue` 没有组件测试；管理员登录后的界面没有看过 | 已复核：字段与 `TaskOut` 一致；重试只调现有的 `POST /api/tasks/{id}/retry`，它清空 `started_at`，不受重试间隔限制 |
| T24be 搜索动效 | 30 秒超时、低配机器上的帧率、系统真正打开“减少动态效果”（只有演示页的强制开关和代码复核）没有测。`scanLoader.ts`、`launchAnimation.ts` 操作 DOM 和 Canvas，没有单元测试，靠浏览器检查；中文输入法组字时按回车没有测 | 已复核：状态机、时间轴、请求会话、待机计时、焦点判断都是有单元测试的纯逻辑；组字中的回车不会触发表单提交 |
| T24bb 登录竞态、文件列表、预览页 | 三个 `.vue` 没有组件测试（没有组件测试工具），在浏览器里修改前后各测一次 | 已复核：判断在 `auth.ts`、`client.ts`、`LatestRun` 里，有单元测试 |

### T24e 文本预览排序（2026-11-19 登记，见 `decisions.md` D44）

| 项目 | 说明 | 代码复核 |
|---|---|---|
| 前端效果 | T24f 起 PDF、图片的“抽取文本”标签页会调用这个接口，按页穿插的顺序在浏览器里对着模拟接口看到过；真实后端上没有看过 | — |

### T24d rebuild-indices --force（2026-11-19 登记，见 `decisions.md` D43）

没有剩余项。（2026-11-23：W5 11.3 第 9 步在真实 OpenSearch 上执行了 `--fix rebuild-indices --force` 的演练与 `--yes`，之后检查干净；已删除。）

### T24l Worker 启动时检查数据库迁移（2026-11-21 登记，见 `docs/changes/T24l.md`）

没有剩余项。（2026-11-23：两行都已由 W5 11.4 验证：空库、只升到 `0001` 的库上两个 Worker 都以退出码 1 结束并给出正确提示，升到 `0002` 后正常启动；已删除。）

### T24i 重新 OCR（2026-11-19 登记，见 `decisions.md` D47）

没有剩余项。（2026-11-23：W6 12.11 交回了 W3 的 SQL 与索引计数，reocr 前后 OCR 片段都是 1589、没有重复；W6 12.7 又在 60 个文档上 reocr 一次，全部重新识别成功；已删除。）

### T24g OCR 模型检查（2026-11-19 登记，见 `decisions.md` D46）

没有剩余项。（2026-11-21 20:40：`test_preflight_reports_mixed_ocr_models` 在 Windows 第一轮通过，已删除。）

### T24c OCR 参数（2026-11-19 登记，见 `decisions.md` D42）

没有剩余项。（2026-11-21 20:40：“OCR Worker 真实链路写入 params”已由 W3 证实，已删除：500 条真实 OCR 结果都带 `pdf_dpi`、`min_confidence`、`max_pixels`，见 W3 各结果目录 `config.json` 的 `versions.ocr_params`；W1 的烟测执行方也报告 PASS。）

### T24 B3 与消融配置（2026-11-19 登记，见 `decisions.md` D38）

| 项目 | 说明 | 记录位置 |
|---|---|---|
| B3 及消融在真实数据上运行 | **流程已验证（2026-11-21 W3）：** 7 个配置在 DocVQA 上用真实 PostgreSQL、OpenSearch、CLIP 服务运行，退出码 0、结果完整，Claude 核对了指标、重复间排名和配置记录。正式评测数据集上仍没有运行（T25、T26） | `decisions.md` D38 |
| MVP-2 里程碑 | 未达成，没有打 tag `mvp-2` | `decisions.md` D38 |

## 5. 补测方法

需要一个 PostgreSQL 16 实例和一个**空的**专用测试库（库里已有表时测试会直接失败，不会清库）。

1. 建库 `docmgr_test`，把连接串写进 `.env` 的 `TEST_DATABASE_URL`（格式见 `.env.example`）。
2. 在 `backend/` 目录执行：

   ```bash
   export $(grep '^TEST_DATABASE_URL=' ../.env) && ../.venv-main/bin/pytest
   ```

3. 预期结果：除 `tests/opensearch/` 的 13 项、`test_pipeline_db.py` 的 2 项端到端测试和 `test_search_db.py` 的 1 项真实索引测试外全部运行。两类都补测时的预期见下面的“OpenSearch 测试”。
4. 有失败的话先修；全部通过后更新本文件和 DEVPLAN §5。

在另一台机器上补测时，把那台机器的系统和 PostgreSQL 版本一起记下来。

**OpenSearch 测试（T13 的 13 项、T14 的 2 项端到端、T15 的 1 项）**

需要一个装了 analysis-smartcn 插件的 OpenSearch 2.19.1。最简单的办法是用项目自己的 `deploy/docker-compose.yml` 启动（第 6 节第 6 步），它会构建带插件的镜像。

1. 确认插件已装：`curl -s "http://127.0.0.1:9200/_cat/plugins?v"` 的输出里有 `analysis-smartcn`。
2. 在 `backend/` 目录执行：

   ```bash
   TEST_OPENSEARCH_URL=http://localhost:9200 ../.venv-main/bin/pytest tests/opensearch -v
   ```

3. 测试只使用形如 `test_xxxxxxxxxx_doc_meta` 的独立索引，结束时只删除自己建的索引，不碰 `doc_meta`、`chunks` 正式索引。即使这样，也不要对着有真实数据的 OpenSearch 运行。
4. 预期结果：13 项全部通过。最先可能失败的是创建索引（mapping 写法不被接受），报错会写明是哪个字段或设置。
5. T14 的 2 项端到端测试同时需要数据库和 OpenSearch，并且会启动真实的 Worker 子进程。在 `backend/` 目录执行：

   ```bash
   export $(grep '^TEST_DATABASE_URL=' ../.env) && TEST_OPENSEARCH_URL=http://localhost:9200 ../.venv-main/bin/pytest tests/integration/test_pipeline_db.py -v
   ```

   测试会把配置写进环境变量，交给子进程读取（环境变量优先于 `.env`）；索引同样使用带随机前缀的独立索引。
6. T15 的 1 项真实索引测试同样需要两者，在 `backend/` 目录执行：

   ```bash
   export $(grep '^TEST_DATABASE_URL=' ../.env) && TEST_OPENSEARCH_URL=http://localhost:9200 ../.venv-main/bin/pytest tests/integration/test_search_db.py -v
   ```

   预期 20 项全部通过。
7. 高亮摘要的转义（没有自动化测试，手工做一次）：用一个带随机前缀的测试索引，写入一条 `text` 为 `<script>alert(1)</script> 报销标准` 的片段，分别查“报销”（有命中词）和只靠词干匹配、没有可高亮词的查询，确认返回的 `evidence.snippet` 里 `<script>` 显示为 `&lt;script&gt;`，只有 `<em>` 是标签。结果记到本文件第 4 节对应的行。
8. 同时设置 `TEST_DATABASE_URL` 和 `TEST_OPENSEARCH_URL` 运行整个 `pytest`，预期 728 项全部运行，0 项跳过（backend 目录）。

## 6. OpenSearch 相关的未测试项与补测步骤

更新日期：2026-11-14（T13 开始前）

### 6.1 为什么没测

本机（Apple M4，24 GB 内存，macOS 26.6.2）上没有能运行 OpenSearch 的环境：

- Barry 决定不在本机安装和运行 Docker；
- 本机没有 Java 运行时（`/usr/bin/java` 只是系统占位程序，执行时提示找不到 Java）；
- OpenSearch 官方没有发布 macOS 的正式安装包（2026-11-14 查询，只找到面向开发者的快照构建）。

按 GLOBAL.md“测试执行限制”，这些测试不在本机强行执行，也不为它们安装任何东西，统一登记在这里。

### 6.2 未测试项

| 编号 | 项目 | 用什么测 | 要回答的问题 | 影响 |
|---|---|---|---|---|
| OS-2 | 中文分词对比：IK（standard 与 smartcn 已于 2026-11-16 在 Windows 上对比：smartcn 22 词，standard 34 个单字） | 同上 | 附录 A13 选哪个分词器 | T13 的 mapping，`deploy/docker-compose.yml` 的镜像 |

OS-1 至 OS-6 与 `env_check/未测试/清单.md` 的 1–6 项一一对应。OS-1、OS-3、OS-4、OS-5、OS-8、OS-9、OS-10 已在 2026-11-16 Windows 补测中完成并从上表删除（2026-11-19 整理）；A14 已由 Barry 于 2026-11-19 确定不启用。下面第 6.4 节的步骤原样保留，供在别的机器上复跑。

### 6.3 测试机器要求

- 能运行 Docker 的电脑：Docker Desktop（macOS / Windows）或 Docker Engine（Linux）都可以。不必是本机——Barry 决定本机不装 Docker。
- 内存至少 8 GB，Docker 可用内存设为 4 GB 以上（Docker Desktop：Settings → Resources → Memory）。
- 能访问 Docker Hub（拉取 `opensearchproject/opensearch:2.19.1`）。构建实测镜像时，容器内要能从 OpenSearch 官方地址下载 analysis-smartcn 插件。
- Python 3.11。
- **下载提醒：** 下面的步骤会下载 Docker 镜像（OpenSearch 官方镜像 1 GB 左右）、smartcn 插件和 Python 包 psutil。按 CLAUDE.md，下载前先确认，下载后登记到 `docs/downloads.md`，并写明是在哪台机器上装的。

### 6.4 详细步骤

以下命令都在**测试机器**上执行。`<项目目录>` 指测试机器上本仓库的根目录（用 `git clone` 或直接拷贝整个目录都可以）。

**第 0 步：记录测试机器**

```bash
cd <项目目录>/env_check
python3.11 -m venv .venv-main
.venv-main/bin/pip install -r requirements-main.txt
.venv-main/bin/python 00_sysinfo.py
```

```bash
mv results/00_sysinfo.json results/00_sysinfo.testbox.json
git checkout -- results/00_sysinfo.json   # 恢复仓库里开发机的那份；不是 git 克隆的，就从开发机拷一份回来
```

`00_sysinfo.py` 记下测试机器的 CPU、内存和系统版本，但它固定写到 `results/00_sysinfo.json`，会盖掉仓库里开发机的那份，所以运行后立刻改名，再把开发机的恢复回来。在另一台机器上测得的延迟和内存不代表开发机，写进论文时要注明是哪台机器。

**第 1 步（可选）：决定是否同时测 IK**

1. 到 IK 插件的发布页查找与 OpenSearch **2.19.1 完全一致**的发行包（zip 文件名或说明里写明 2.19.1）。
2. 找到了：打开 `env_check/opensearch/Dockerfile`，取消最后两行的注释，把 `IK_URL=` 填成那个 zip 的地址。
3. 找不到：不装 IK，在结果里写明“IK 没有与 2.19.1 匹配的版本”。这本身就是一条结论：选 IK 就要更换 OpenSearch 版本。

**第 2 步：构建并启动实测用的 OpenSearch（OS-1）**

```bash
cd <项目目录>/env_check/opensearch
docker compose up -d --build
```

等它启动。正常情况下一分钟以内，下面的命令会返回带 `"status"` 的 JSON：

```bash
curl -s http://127.0.0.1:9200/_cluster/health
```

- 返回的 `status` 为 `green` 或 `yellow`：启动成功。单节点时 `yellow` 是正常的。
- 两分钟后仍然连不上：执行 `docker compose logs --tail 100`，把输出保存下来，记为 OS-1 失败，不要往下做。

确认插件已安装（输出里应有 `analysis-smartcn`，装了 IK 的话还有 IK）：

```bash
curl -s "http://127.0.0.1:9200/_cat/plugins?v"
```

**第 3 步：运行实测脚本（OS-1 至 OS-5）**

```bash
cd <项目目录>/env_check
.venv-main/bin/python 01_check_opensearch.py
```

结果写入 `results/01_opensearch.json`。脚本依次做这些事：读版本和插件；用每个候选分词器切分同一句中文；用最好的可用分词器建测试索引，跑 6 个查询；测 BM25 和向量检索的延迟；读 JVM 堆。

**第 4 步：换 2g 堆再测一次（OS-5，只在需要时做）**

满足任意一条才需要做：第 3 步出现内存不足错误、查询明显卡顿、JVM 堆用量接近上限。

```bash
cd <项目目录>/env_check
cp results/01_opensearch.json results/01_opensearch_1g.json
OS_HEAP=2g docker compose -f opensearch/docker-compose.yml up -d --force-recreate
# 等第 2 步的 curl 恢复返回后：
.venv-main/bin/python 01_check_opensearch.py
cp results/01_opensearch.json results/01_opensearch_2g.json
```

**第 5 步：并发内存（OS-6）**

这一步要求测试机器上已经按 `env_check/README.md` 第 1 步建好 ocr 和 clip 两个环境，并下载了模型。做不到就跳过，记为“OS-6 未测试”。

保持 OpenSearch 运行，开三个终端，都先 `cd <项目目录>/env_check`：

```bash
# 终端 B
.venv-ocr/bin/python 02_check_ocr.py --mobile --hold
```

```bash
# 终端 C
.venv-clip/bin/python 03_check_clip.py --hold
```

```bash
# 终端 D（等 B、C 都显示模型已加载后再运行）
.venv-main/bin/python 04_mem_snapshot.py
```

完成后在终端 B、C 按 Ctrl+C。结果写入 `results/04_mem_snapshot.json`。

**第 6 步：项目自己的 compose 与健康检查（OS-7）**

先关掉实测用的 OpenSearch，它和项目的 OpenSearch 都占用 9200 端口：

```bash
cd <项目目录>/env_check/opensearch && docker compose down
```

```bash
cd <项目目录>
cp .env.example .env
```

编辑 `.env`：

- 把 `POSTGRES_PASSWORD` 改成自己的密码，`DATABASE_URL` 里的密码要与它一致；
- `JWT_SECRET` 换成一个随机值，可以用 `python3 -c "import secrets; print(secrets.token_urlsafe(48))"` 生成。

```bash
docker compose --env-file .env -f deploy/docker-compose.yml up -d
```

```bash
python3.11 -m venv .venv-main
.venv-main/bin/pip install -e "shared[dev]" -e "backend[dev]"
```

```bash
cd backend && ../.venv-main/bin/alembic upgrade head
```

```bash
cd backend && ../.venv-main/bin/uvicorn app.main:create_app --factory
```

在另一个终端执行：

```bash
curl -s http://127.0.0.1:8000/health
```

预期：`database` 和 `opensearch` 都是 `"ok"`；`clip_service` 是 `"unavailable"`（CLIP 服务还没写，属于正常）；整体 `status` 为 `"degraded"`。

这一步顺带让第 5 节的 91 项数据库集成测试有了 PostgreSQL，可以接着按第 5 节补测。

**第 7 步：T13 集成测试（OS-8）**

在第 6 步启动的 OpenSearch 上运行（项目的镜像已装 analysis-smartcn）：

```bash
cd <项目目录>/backend && TEST_OPENSEARCH_URL=http://localhost:9200 ../.venv-main/bin/pytest tests/opensearch -v
```

预期 13 项全部通过。测试只操作带随机前缀的索引，结束时自行删除。

**第 8 步：收尾**

```bash
cd <项目目录> && docker compose --env-file .env -f deploy/docker-compose.yml down
```

`down` 不加 `-v`，数据卷保留。

### 6.5 结果怎么读、怎么用来定 A13 和 A14

**A13（选哪个分词器），看 `results/01_opensearch.json` 的 `analyzers`：**

| 现象 | 结论 |
|---|---|
| `standard` 把中文逐字切开 | 正常现象，证明必须装中文分词插件 |
| `smartcn` 把“文档管理”“信息检索”“跨模态”这类词切成完整的词或合理的两字词 | smartcn 可用 |
| 装了 IK，`ik_max_word` 切得明显更合理（专业词完整、没有错切） | 可以考虑 IK，但要接受“版本必须严格匹配”的维护代价 |
| 两者差别不大 | 选 smartcn：官方插件，与 OpenSearch 同版本发布，以后升级不会卡在插件上 |

另外看 `bm25_hits`：脚本用选出的分词器建了一个 6 条记录的测试索引，跑 6 个查询。按测试数据，排第一的应当分别是：财务报告 → d1，发票 → d2，路由协议 → d3，检索模块 → d4，图文模型 → d5，预算 → d1。排第一的不对，或者没有命中，要记下来。注意：脚本只用选出的那一个分词器建索引（装了 IK 时优先用 `ik_max_word`，否则用 `smartcn`），要比较两者的检索结果，需要改脚本第 112 行的选择顺序后再跑一次。

**A14（是否启用降级预案）：同时满足下面三条就不启用，继续用 OpenSearch。**

1. 第 2 步启动成功，集群状态为 `green` 或 `yellow`；
2. 1g 堆（或第 4 步的 2g 堆）下没有内存不足错误，查询延迟在几十毫秒以内；
3. 第 5 步的 `system_available_gb` 不低于 1.5 GB，`swap_used_gb` 没有持续增长。

任何一条不满足，就把数据交给 Barry，由 Barry 决定是否启用降级预案（GLOBAL §11.4，必须 Barry 同意）。

### 6.6 测完之后要做的事

1. 把测试机器上 `env_check/results/` 里的这些文件拷回开发机的同一目录：`00_sysinfo.testbox.json`、`01_opensearch.json`（做了第 4 步的，还有 `01_opensearch_1g.json`、`01_opensearch_2g.json`）、`04_mem_snapshot.json`，以及 `history/` 下新增的带时间戳的文件。不要拷 `00_sysinfo.json`。
2. 在开发机上运行 `cd env_check && .venv-main/bin/python 05_make_report.py`，重新生成 `env_check/env_report.md`。报告的第 1 节仍是开发机，第 2 节（OpenSearch）和第 5 节（并发内存）来自测试机器，要在这两节开头手工注明“测于另一台机器”，并引用 `00_sysinfo.testbox.json` 里的配置。
3. 在 `docs/decisions.md` §2 填写 A13、A14、JVM 堆大小的结论，并写明测试机器。
4. A13 选定后修改 `deploy/docker-compose.yml`：改用装了所选插件的镜像。插件版本必须与 OpenSearch 版本完全一致。
5. 把通过的项从本节删除；失败的项留在这里，写明失败现象，并附上日志。
6. 在 `docs/downloads.md` 登记测试机器上下载的内容。

## 7. Windows 第二轮补测（2026-11-19）登记的未通过与未测试项

来源：`docs/changes/windows-2026-11-19-原始说明.txt`（`27b51b2`）。本会话没有重跑；在 macOS 上只重跑了这一轮改过的两个单元测试文件（`test_health.py`、`test_worker_main.py`，11 项通过）和前端类型检查（通过）。

### 7.1 未通过：符号链接测试（WinError 1314）

在 Windows 普通权限下，测试准备阶段调用 `os.symlink` / `Path.symlink_to` 失败，尚未进入项目代码。2026-11-16 第一轮以管理员权限重跑时这 8 项通过过，这一轮没有重跑。

| 位置 | 测试 |
|---|---|
| backend | `tests/unit/test_consistency.py::test_symlinks_are_never_treated_as_stored_files` |
| backend | `tests/unit/test_storage.py::test_file_symlink_pointing_outside_rejected` |
| backend | `tests/unit/test_storage.py::test_directory_symlink_pointing_outside_rejected[year]`、`[document]` |
| backend | `tests/unit/test_storage.py::test_put_refuses_to_write_through_directory_symlink` |
| backend | `tests/unit/test_storage.py::test_symlinked_temp_directory_refused_at_startup` |
| shared | `tests/test_storage_keys.py::test_symlinked_directory_is_rejected`、`test_symlinked_file_is_rejected` |

补测方法：打开 Windows“开发人员模式”，注销重登，`whoami /priv` 确认有 `SeCreateSymbolicLinkPrivilege`，再重跑 backend 和 shared；或用有该权限的管理员终端。不能改成 junction：这些测试验证的就是符号链接逃逸。这 8 项在 macOS 本机一直通过。

### 7.2 仍未测试

| 项目 | 说明 | 记录位置 |
|---|---|---|
| Docker 与 compose | Windows 上已装 Docker Desktop 4.99.0，两个服务容器启动成功（同第 4 节两行）。后端、Worker 没有容器化，仍在主机上运行 | 第 4 节、第 6 节 |
| 正式检索评测 | `experiments/` 仍是 0 个文件、0 条查询、0 条 qrels，B0–B3 没有正式指标。2026-11-21 W2、W3 用 `vidore/docvqa_test_subsampled`（500 张英文扫描页，在 `experiments/docvqa/`）只做了流程验证 | 第 4 节“B0–B2 实验”“T24 B3” |
| `RLIMIT_AS` 内存上限 | **部分验证（2026-11-25 Windows 第五轮的 Linux 容器）：** 两个 `_limit_memory` 能设上限（256 MB），超限申请得到 `MemoryError`。跑的是为 Python 3.9 改过的副本和桩依赖；真实解析、真实 OCR 下默认值（通用 2048 MB、OCR 3072 MB）够不够没有测 | `decisions.md` D16、D30；`docs/changes/windows-2026-11-25-核对.md` |
| 并发、长时间运行、吞吐、峰值内存 | **部分数据（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W7 13.2 六组进程同时运行的内存（合计峰值 5732.8 MB）；W8 16.5 用 40 张图比较了 1、2、4 个 OCR Worker（4.327 张/分钟最高，但每张耗时和 CPU 争抢也最高）。没有长时间运行观察 | DEVPLAN T27 |
| 极端真实文件 | 已用 6 个真实样本（中文 PDF、Word、Excel、相机 JPEG、PaddleOCR 示例图、一个 PDF 模糊测试样本）；接近 50 MB 的 PDF、加密 PDF、多栏/表格/水印/竖排/手写扫描件、Office/WPS 实际保存的复杂文件、超大图片、渐进式 JPEG、超限压缩包都没有测 | 第 4 节解析器、OCR 各行 |
| T24g 之后的代码 | **已覆盖到 `fd0b5eb`（2026-11-23 Windows 第四轮，W4–W8，基线 `fd0b5eb`，核对见 `docs/changes/windows-2026-11-23-核对.md`）：** W5 11.2–11.4、11.6 与 W6 12.2 在 `fd0b5eb` 上覆盖了 T24k–T24u；T24k 的连接超时因网络立刻回绝没有测到，改用本地监听重测（`windows任务书.md` 第 17.3 节）。`fd0b5eb` 之后的 T24v–T24z 没有在 Windows 上跑过 | 第 3 节、第 4 节 |
| 修复后的 PDF 预览在 macOS 上 | `PdfViewer.vue` 新增 `cMapUrl`、`standardFontDataUrl`、`wasmUrl`、`iccUrl`，资源在 `frontend/public/pdfjs/`；只在 Windows 上看过，macOS 浏览器里没有看过；生产构建后资源路径（`BASE_URL`）在 macOS 上也没有检查 | DEVPLAN §5“Windows 第二轮补测” |
| 余弦分数的绝对值 | `test_vector_index_live.py` 原来断言完全相同方向得 2.0，OpenSearch 2.19.1 实际为 1.0；测试改为只断言排序和严格递减。分数只用于通道内排名，不影响 RRF，但 `search_vectors` 文档里原来写的“1 + 余弦相似度”与实测不符，已改为“范围由版本决定” | `decisions.md` D35 |

### 7.3 Windows 第一轮（2026-11-21，W1–W3）的发现

执行者 Codex，基线 `8fb5830`（实验运行时为 `bba3a1b`）。核对见 `docs/changes/windows-2026-11-21-核对.md`。

| 项目 | 说明 | 后续 |
|---|---|---|
| 8 项符号链接测试 | 仍因 WinError 1314 失败（同第 7.1 节）：执行方的沙箱账号没有 `SeCreateSymbolicLinkPrivilege`，提权返回退出码 4 | `windows任务书.md` W6 第 12.3 节，由 Barry 本人的终端运行 |
| `git_dirty: true` | 第二轮的实验结果目录没有交回，仍无法确认 | `windows任务书.md` 第 17.4 节要求交回并记下运行前的 `git status` |
| OCR 子进程访问违例 | 第五轮按实际 Worker 数重算：≤4 个不崩、≥5 个必崩；W9 17.14 用正确的方法重做：N=1–3 共 60 个任务 0 失败，N=4 第 3 轮内存跌到 20 MB 被中止，没有出现 `0xC0000005`。结论：内存耗尽时会崩，16 GB 机器上最多开 3 个 OCR Worker；`0xC0000005` 与内存的因果仍是推断 | 写进 T30、论文局限 |

### 7.4 Windows 第四轮（2026-11-23，W4–W8）的发现

执行者 Codex，基线 `fd0b5eb`。核对见 `docs/changes/windows-2026-11-23-核对.md`。

| 项目 | 说明 | 后续 |
|---|---|---|
| 8 项符号链接测试 | **2026-11-26：** 权限已经有了，shared 2 项通过；backend 6 项因为指定的 `--basetemp` 目录不存在（WinError 3）没跑起来 | 换一个存在的临时目录重跑 backend 6 项 |
| 采样脚本把 OCR 识别子进程归错组 | 任务书第 13.2、16.2 节的脚本按命令行归组，multiprocessing 启动的识别子进程被归进 `python_other`。W7 的合计峰值因此少算约 3 GB，已按原始数据更正；W8 16.5 汇总里的内存数字同样受影响 | 任务书第 17.2 节换成按父进程归组的新脚本 |
| 真实文件、人工核对、真实拖拽 | W6 12.9、12.10，W8 16.7 B，W4 10.3 都需要 Barry 本人准备或操作，这一轮没做 | 任务书第 17.7、17.10、17.11 节 |

### 7.5 Windows W9（2026-11-26，基线 `e1d61eb`）的发现

核对见 `docs/changes/windows-2026-11-26-核对.md`。

| 项目 | 说明 | 后续 |
|---|---|---|
| 数据库停掉时后端接口一直挂着（Bug 1） | `make_engine()` 没有连接超时；Windows 上 psycopg 连被拒绝的端口会一直等到超时，不设就一直等。`/api/auth/me` 超过 90 秒不返回 | 待修（DEVPLAN §4） |
| `test_database_address_is_hidden` 在 Windows 上失败（Bug 2） | 测试依赖真实网络错误的文字里带地址，Windows 上得到的是超时，不带地址；被测函数没有问题 | 待修（DEVPLAN §4） |
| 实验记录的 `git_dirty` 总是 true | `git status --porcelain` 把未跟踪的输出目录也算进去 | 待修（DEVPLAN §4） |
| `_forcemerge` 清除已删除文档的效果 | 已删除文档只占 0.38%，低于清理门槛，没有清；“已删除文档影响 BM25 统计值”的解释没有被直接证实 | 不再安排；排名稳定性已验证 |
