# 修改记录：搜索动效（search-motion，2026-11-21 ～ 2026-11-22）

- 来源：Barry 要求按根目录 `SEARCH_MOTION_DEV_GUIDE.md`（下称“指南”）在 `frontend/` 里实现三个搜索动效：动画 1 待机转动、动画 2 启动、动画 3 扫描加载
- 任务性质：不在 DEVPLAN 里，没有任务编号；只改前端；没有改后端、数据库、索引、附录 A；没有下载或安装任何东西
- 修改者：Claude（Opus 5.5）
- 分支与提交：克隆库 `feat/search-motion`，3 个提交，未 push（克隆库已删除 origin）
  - `9ab00b7` 公共层 + 扫描加载动画（动画 3），接入检索页
  - `4658130` 启动动画（动画 2），接入演示页
  - `d53fed7` 待机转动动画（动画 1），三个动效接入检索页
- 本文件与 `frontend/src/features/search-motion/README.md` 在上述 3 个提交之后单独提交（`fed3743`）
- 之后按 Barry 的决定做了三项小修改，单独一个提交（`1717a4d`），见第 7 节
- 再之后启动动画改为“没有输入时循环播放”，单独一个提交（`1cfe7fa`），见第 8 节
- 待机动画的光球改为星尘粒子效果，单独一个提交（`c52d036`），见第 9 节
- 待机动画放大到 120 px，单独一个提交（`3d1bd54`），见第 10 节
- 待机和启动改为同一个星尘光球动画，单独一个提交（`f12d6fe`），见第 11 节
- 登录页加待机动画，单独一个提交（`acc6855`），见第 12 节
- 登录页 logo 换成星尘光球 + 文档图标，并去掉第 12 节加的下方待机动画，单独一个提交（`226617f`），见第 13 节
- 登录页 logo 的光圈 10 秒一张一缩，单独一个提交（`f4e4c46`），见第 14 节
- 光圈缩放幅度加大，单独一个提交（`70c93c7`），见第 15 节
- 系统整体配色调节，单独一个提交（`91a82e1`），见第 16 节
- 光圈放大时向左右拉长，单独一个提交（`2a3f4a6`），见第 17 节
- 界面语言切换（中文 / English），单独一个提交（`4cadf08`），见第 18 节
- 光圈在两条对角线之间来回摆，单独一个提交（`0a4f4f1`），见第 19 节
- 缩放周期改为 15 秒、与摆动同步，单独一个提交，见第 20 节

------------------------------------------------------------------------

## 1. 范围与隔离方式

- 工作目录是本地克隆 `~/Desktop/BARRY zou-search-motion`，不是主仓库。克隆后删除了 origin，不会误推。
- `frontend/node_modules` 用 APFS 克隆（`cp -c`）从主仓库复制，没有执行 `npm install`，没有下载任何东西。Node 用主仓库的 `.tools/node`。
- 主仓库 `~/Desktop/BARRY zou` 没有任何改动。
- 与 GLOBAL.md 的关系：
  - §3.1 写明前端“不做复杂动画”；§2 规定非核心功能归 P4，须在 P0–P3 完成后、经 Barry 确认才实施。
  - 这三个动效属于增强功能，没有进入 DEVPLAN，也不算毕设的验收内容。放在克隆库里做，就是为了不进入主开发。
  - 如果以后要合回主仓库，需要先按 GLOBAL.md §2 P4、§11.4 走增强功能确认流程（见第 6 节第 7 条）。

## 2. 接入前检查清单结论（指南第 1 节）

| 检查项 | 结论 |
|---|---|
| 框架与渲染方式 | Vue 3.5（3.5.45）+ Vite 8（8.3.8）+ TypeScript 6.0.3 的单页应用，Element Plus 2.14.8；没有 SSR |
| 颜色来源 | Element Plus 的 `--el-*` 和 `src/styles.css` 的 `--app-*`（`--app-*` 大多引用 `--el-*`）。动效只通过 `shared/tokens.ts` 读这两组变量，不写死色值 |
| 暗色模式 | 项目原本没有暗色模式。`tokens.ts` 同时监听系统配色（`prefers-color-scheme`）和 `<html>` 的 class / style / data-theme，以后按 Element Plus 的方式（`html.dark`）加暗色时 Canvas 会自动重新取色。演示页引入 Element Plus 自带的 `dark/css-vars.css` 并切换 `html.dark` 来测暗色 |
| 动效库 | 没有。本次也没有引入，全部用 CSS 过渡、Web Animations API 和 Canvas 2D 手写 |
| 搜索请求在哪里发 | 原本在 `SearchView.vue` 视图层直接调用 `search()`，没有取消，也没有超时；靠 `loading` 守卫和 `rerun` 标记避免结果错位。现在改由 `scan-loader/searchSession.ts` 统一负责开始 / 成功 / 失败 / 取消四个时机 |
| 搜索框在哪里 | `SearchView.vue` 里的 `el-input`。首页 `/` 是文件列表（`DocumentsView`），不是搜索页，所以启动动画改为“会话内第一次进入 `/search` 时播放”；地址栏带着检索词（`?q=`）进来时不播 |
| 埋点 | 项目没有埋点。只留了回调：待机动画 `onIdle` / `onActive`（组件事件 `idle` / `active`），扫描动画 `onDone`（组件事件 `done`），启动动画 `onFinish` |
| 多语言 | 没有 i18n 库。动效文案集中在 `messages.ts`，以后接 i18n 只替换这一个文件。扫描动画原按指南写“网页”，Barry 决定改为“文件”（第 7 节） |

## 3. Barry 确认的默认决定

1. 在本地克隆库里做；用演示页 `/motion-lab` 加模拟请求自测（不需要登录和后端）。
2. 启动动画放在 `/search`（见上表“搜索框在哪里”）。
3. 检索框改为胶囊形（启动动画的终点就是这个形状），加放大镜前缀图标；“检索”按钮同样改为圆角。
4. 待机动画放在检索页引导区右侧的空白处；屏幕宽度 ≤600px 时隐藏。
5. 接口很快返回时也完整播一轮扫描（6 张卡约 3.6 s），之后再收拢 0.4 s 显示结果，不加速。

## 4. 逐文件修改记录

以下路径都相对 `frontend/`。新增文件在 `src/features/search-motion/` 下，共 23 个文件（约 2300 行，含演示页）。

### 4.1 公共层 `src/features/search-motion/shared/`（新增，`9ab00b7`；`tokens.ts` 在 `d53fed7` 又改一次）

| 文件 | 内容 | 原因与影响 |
|---|---|---|
| `easing.ts` | `clamp01`、`lerp`、`progress`、`easeOutCubic`、`easeInOutCubic`，以及对应的 CSS 写法 `CSS_EASE_OUT`、`CSS_EASE_IN_OUT` | 指南 §3.4：聚拢、展开、淡入用缓出，样式切换和扫描线用缓入缓出；三个动效共用，不各写一份 |
| `reducedMotion.ts` | `prefersReducedMotion()`、`onReducedMotionChange()`（运行中系统设置变化也会通知）、`setReducedMotionOverride()`（演示页强制开 / 关） | 指南 §3.2：三个动效都从这里读，不各自写 `matchMedia`。强制开关只给演示页用，正式页面不调用 |
| `tokens.ts` | `readTokens()` 从 `--app-*` / `--el-*` 读 8 个颜色，读不到用 Element Plus 浅色默认值；`onThemeChange()` 监听系统配色和 `<html>` 属性变化。`d53fed7` 新增 `primaryStrong`（`--el-color-primary-dark-2`，后备 `#337ecc`） | 指南 §3.1。`primaryStrong` 的原因见第 5.3 节：浅色下主色对白底只有 2.78:1，常驻图形要求 3:1 |
| `canvas.ts` | `addFrame()`：全页面唯一的 `requestAnimationFrame` 循环，没有登记者时停帧，页面切到后台暂停，`dt` 封顶 100 ms；`activeFrameCount()` 供自测查残留；`createCanvasSurface()`：按 `devicePixelRatio` 设置画布像素、`ResizeObserver` 跟随容器尺寸、画布 `aria-hidden` | 指南 §3.3：同一时间最多一个 rAF；高清屏不模糊；侧栏展开等非窗口尺寸变化也能跟上 |
| `timers.ts` | `TimerGroup`：`after` / `cancel` / `clear` | 指南 §3.5、§6.4：取消、销毁时一次清空定时器，不留残留 |

### 4.2 文案 `src/features/search-motion/messages.ts`（新增，`9ab00b7`）

- `SCAN_TEXT`：正在打开文件… / 正在阅读第 i / n 个文件 / 正在整理答案… / 检索失败 / 重试（“文件”原为指南的“网页”，第 7 节改）。
- `SEARCH_TEXT.timeout(seconds)`：检索超时提示。

### 4.3 扫描加载动画 `src/features/search-motion/scan-loader/`（新增，`9ab00b7`）

| 文件 | 内容 | 原因与影响 |
|---|---|---|
| `machine.ts` | 纯函数状态机 `scanReducer`：`idle → scanning →（一轮结束且结果已到）summarizing → done`；`error`、`cancel`。结果到了只记 `resultReady`，等这一轮播完才进入整理 | 指南 §6.1。不碰 DOM，单元测试直接测 |
| `scanLoader.ts` | 框架无关的核心 `createScanLoader(host, options)`。卡片默认 6 张、上限 8 张；一轮 = 入场 600 ms + 每张卡 500 ms（6 张约 3.6 s），收拢 400 ms。卡片入场、对勾、收拢用 CSS 过渡 + 类名切换，扫描线用 Web Animations API。进度文字放在 `role="status"`、`aria-live="polite"` 的段落里，卡片区 `aria-hidden`。出错时卡片变淡，有 `onRetry` 时显示“重试”按钮。减少动效时去掉扫描线和收拢位移 | 指南 §6.2–§6.5 |
| `scanLoader.css` | 卡片、扫描线、对勾、收拢、出错、减少动效的样式，颜色全部引用项目变量。对勾底圆用 `--el-color-success-dark-2`，勾号用 `--app-surface` | 自测修复：暗色下底圆变成亮绿，原来的白勾对比度只有 1.91:1，改用页面底色（第 5.3 节） |
| `searchSession.ts` | `createSearchSession(loader, { timeoutMs, onError })`，返回 `run(task)`、`cancel()`、`pending`。新请求先中断旧请求（`AbortController`），旧请求晚到的返回按请求编号丢弃；默认 30 s 超时（`SearchTimeoutError`）；`onError` 把错误转成显示文字 | 指南 §6.3：四个时机放在请求这一层，一个不漏。自测修复：原来 `cancel()` 只在有进行中的请求时才停动画，请求已返回、动画还在播最后一轮时取消无效；改为 `cancel()` 总是调用 `loader.cancel()`，`run()` 内部只中断请求（`loader.start()` 自己会清旧动画，中间不出现一帧 idle） |
| `handle.ts` | `ScanLoaderHandle` 接口；`controlsFrom(() => ref)` 把组件 ref 包装成会话需要的控制对象，ref 未挂载时调用被忽略 | 页面和演示页共用 |
| `ScanLoader.vue` | Vue 适配层：挂载时创建核心、卸载时 `destroy`；props `pageCount`、`retryable`；事件 `done`、`retry`、`phase`；通过 `defineExpose` 暴露 `start` / `complete` / `error` / `cancel`。`idle` / `done` 时不占位 | 指南 §2：核心与框架分开 |

### 4.4 启动动画 `src/features/search-motion/launch/`（新增，`4658130`）

| 文件 | 内容 | 原因与影响 |
|---|---|---|
| `timeline.ts` | 纯函数时间轴 `launchFrame(t, chars)`、`launchDuration(chars)`：0–0.8 s 光标闪两次；0.8–1.7 s 60 个粒子聚拢成半径 24 px 的旋转光环；2.1–2.9 s 展开到胶囊轮廓；2.8–3.2 s 描边和图标淡入；3.1 s 起每秒打 10 字；打完停 250 ms。`pointOnOutline(box, s)` 按周长比例在胶囊轮廓上取点 | 指南 §5.1；单元测试直接测 |
| `playOnce.ts`（第 8 节已删除） | `hasPlayedLaunch` / `markLaunchPlayed` / `resetLaunchPlayed`，用 `sessionStorage` 记标记；读写异常（隐私模式）时一律 try/catch，按“没播过”处理 | 指南 §5.3：会话内只播一次，最坏情况是刷新后再播一次，不会报错 |
| `launchAnimation.ts` | 核心 `playLaunch(target, options)`，返回 `skip()`、`destroy()`。开始时读真实输入框的位置、宽高、圆角、背景、描边色、占位文字字体与颜色、前缀图标位置与 path，全部照它画；只打到输入框能显示的宽度为止。时间用累计 `dt`，切到后台暂停。任意按键 / 点击跳过（捕获阶段，不阻止默认行为，按下的字符进入输入框）；窗口尺寸或滚动变化直接跳到结束；减少动效打开时立即结束。结束时同一帧内显示真实输入框 → 移除 Canvas → `focus({ preventScroll: true })` | 指南 §5.2–§5.4：最容易出问题的是与真实搜索框对齐，所以不写死任何尺寸 |
| `launch.css` | `html[data-sm-launch] .sm-launch-target { visibility: hidden }`；Canvas 固定定位盖满视口、`pointer-events: none` | 随适配层同步加载：首帧就隐藏真实输入框，不闪；只是看不见、仍占位，布局不跳 |
| `useLaunchAnimation.ts` | Vue 适配层 `useLaunchAnimation(inputRef, { placeholder, hasValue, onFinish })`。在 setup 阶段（首帧前）决定播不播：减少动效、本会话播过、输入框已有内容时什么都不做；要播就给 `<html>` 打标记。挂载后才 `import('./launchAnimation')` 懒加载，找不到输入框或加载失败直接显示输入框 | 动画脚本不进首屏；el-input 上要加 `class="sm-launch-target"` |

### 4.5 待机转动动画 `src/features/search-motion/idle-spinner/`（新增，`d53fed7`）

| 文件 | 内容 | 原因与影响 |
|---|---|---|
| `idleTracker.ts` | `createIdleTracker({ idleAfter, onIdle, onActive, throttleMs, target, visibility, now })`，返回 `idle`、`poke()`、`destroy()`。五种操作（pointermove、pointerdown、keydown、wheel、touchstart，passive 监听）；200 ms 内只重置一次计时；待机中任何操作立即退出；页面切到后台停止计时（待机中直接退出），回到前台从 0 重新计时 | 指南 §4.1。事件源和时钟可注入，便于单元测试 |
| `draw.ts` | `drawIdle(ctx, size, tokens, frame)`：8 根圆头射线匀速旋转、长度和粗细按相位波动；光球呼吸缩放（4 s 周期）+ 绕圈高光弧 + 每 2.4 s 一圈涟漪（第 9 节已改为星尘粒子）；`morph` 0→1 时射线向中心回收，`morph > 0.3` 起光球从 60% 放大淡入。颜色用 `primaryStrong` | 指南 §4.3、§4.4：两种样式读同一个旋转角，切换时不重置 |
| `idleSpinner.ts` | 核心 `createIdleSpinner(canvas, { idleAfter = 8000, switchEvery = 30000, style = 'auto' / 'rays' / 'orb', onIdle, onActive })`，返回 `visible`、`show()`、`hide()`、`destroy()`。淡入淡出 0.4 s、morph 0.8 s，都从当前值补间（切换中途有操作就从当前画面直接淡出）；完全淡出后停帧；后台时直接清掉；减少动效时不轮换、不转动，只显示静止射线 | 指南 §4.2、§4.5 |
| `IdleSpinner.vue` | Vue 适配层：props `idleAfter`、`switchEvery`、`spinnerStyle`、`size`（默认 72 px）；事件 `idle`、`active`；暴露 `show` / `hide`。参数变化时重建核心，卸载时 `destroy` | — |

### 4.6 演示页 `src/features/search-motion/lab/`（新增；`MotionLabView.vue` 在三个提交里都有修改，`IdleLabPanel.vue` 在 `d53fed7` 新增）

| 文件 | 内容 |
|---|---|
| `MotionLabView.vue` | `/motion-lab` 页面，不需要登录、不调后端。模拟请求四种模式：快速 0.3 s、慢速 5 s、报错 1.5 s、不返回（演示用 8 s 超时，正式为 30 s）；“连续搜索”（慢速后 0.4 s 再发快速）；“取消”；“重播启动动画”（清标记并刷新）；浅色 / 暗色切换（引入 Element Plus `dark/css-vars.css`）；减少动效跟随系统 / 强制开 / 强制关；显示 rAF 登记数和扫描状态；事件日志。胶囊检索框与检索页写法相同 |
| `IdleLabPanel.vue` | 待机面板：自动轮换 / 固定射线 / 固定光球；“快速走查”把参数改为 2 s 待机、5 s 切换；手动 `show()` / `hide()` |

这两个文件只用于自测和设计走查，不是正式功能。

### 4.7 已有文件的修改

| 文件 | 位置 | 修改前 → 修改后 | 原因与影响 |
|---|---|---|---|
| `src/api/client.ts` | `RequestOptions`（第 45–46 行）、`requestRaw` 的 `fetch` 调用与 `catch`（第 96–100 行） | 新增可选 `signal?: AbortSignal` 并传给 `fetch`；`catch {}` 改为 `catch (error)`，`signal` 已取消时原样抛出（AbortError），否则仍转成 `ApiError(0, 'NETWORK', …)` | 主动取消不是网络故障，不能显示“无法连接服务器”；由调用方判断是被覆盖还是超时。不传 `signal` 的调用行为不变 |
| `src/api/search.ts` | `search()`（第 9–10 行） | `search(body)` → `search(body, signal?)`，并把 `signal` 传给 `request` | 只多一个可选参数，其他调用方不受影响 |
| `src/router.ts` | `/documents/:id` 之后（第 27–32 行） | 新增公开路由 `/motion-lab`（懒加载 `MotionLabView.vue`，没有 `requiresAuth`） | 演示页不需要登录。克隆库专用，合回主仓库时建议不保留 |
| `src/views/SearchView.vue` | 脚本：导入、`useLaunchAnimation`（第 51 行）、`scanPhase` / `loading`（第 57–58 行）、`session` / `onSearch` / `onScanDone` / `watch(selection)` / `onBeforeUnmount`（第 127–200 行） | 去掉 `loading` 守卫和 `rerun`：`loading` 改为由扫描状态计算（scanning 或 summarizing）；`onSearch` 先清空旧结果，再经 `session.run((signal) => search(body, signal))` 发请求；结果在扫描收拢后由 `onScanDone` 写入；检索进行中改开关直接取消旧请求、按新开关重查；卸载时 `session.cancel()`；超时用 `SEARCH_TEXT.timeout` 提示；`SEARCH_UNAVAILABLE` 仍与“没有结果”区分开 | 指南 §6.3。原来连按回车会被守卫挡住，现在新的检索直接覆盖旧的，旧返回被丢弃，不会错位 |
| 同上 | 模板：检索框（第 211–224 行）、结果区（第 272–288 行） | `el-input` 加 `ref="searchInput"`、`class="sm-launch-target search-input"`、前缀放大镜 `AppIcon`，占位文字提成常量 `PLACEHOLDER`；“检索”按钮加 `round`；结果区去掉 `v-loading`，改放 `<ScanLoader retryable>`（重试即重新检索）；引导区拆成文字 + `<IdleSpinner class="guide-idle">` | 胶囊检索框、启动动画、扫描动画、待机动画四处接入 |
| 同上 | 样式（第 360 行起、第 445–468 行、第 485–505 行、第 692–699 行） | 输入框外框 `border-radius: 999px`；引导区改为 flex，右侧留出待机动画；摘要、结果列表、空结果加 0.3 s 淡入上移（`prefers-reduced-motion` 时去掉）；≤600px 隐藏 `.guide-idle` | — |

### 4.8 测试 `tests/search-motion/`（新增）

| 文件 | 用例数 | 覆盖内容 |
|---|---|---|
| `scan-machine.test.ts`（`9ab00b7`） | 7 | 结果到了等本轮播完、未到则下一轮、error / cancel、重新 start 清标记 |
| `search-session.test.ts`（`9ab00b7`） | 7 | 成功、失败、连续搜索丢弃旧返回、超时、cancel、请求已返回动画未播完时 cancel、成功后不再超时 |
| `launch.test.ts`（`4658130`） | 9 | 时间轴各阶段、打字速度与结束时刻、胶囊轮廓取点、会话内只播一次（含存储抛异常） |
| `idle-tracker.test.ts`（`d53fed7`） | 7 | 8 s 进入待机、五种操作、200 ms 节流、后台停止计时、destroy、poke |

## 5. 验证情况

### 5.1 命令

- `npm run typecheck`：通过。
- `npm test`：13 个文件、123 个用例全部通过（含新增 4 个文件、30 个用例）。
- `npm run build`：生产构建成功。

### 5.2 包体

- 三个动效合计约 10 KB（gzip）：共享 chunk 3.92 KB + CSS 0.88 KB + tokens 0.55 KB + 懒加载的启动动画 chunk 2.47 KB + SearchView 增量约 2.3 KB；低于指南要求的 15 KB。
- 不含演示页（单独的懒加载路由）。没有引入任何依赖。

### 5.3 浏览器自测（演示页 `/motion-lab`，由子代理执行）

- 扫描加载动画：快速、慢速、报错、超时、连续搜索、减少动效、暗色、无残留（rAF 登记数回到 0）全部通过。自测发现并已修复 2 个问题：
  1. 请求已返回、动画还没播完时 `cancel()` 不生效（`searchSession.ts`，改为总是调用 `loader.cancel()`，`run()` 内只中断请求）；
  2. 暗色下对勾的白勾对比度只有 1.91:1（`scanLoader.css`，勾号改用 `--app-surface`）。
- 启动动画：10 项中 9 项通过，第 7 项部分实测。已确认：首帧不闪；结束画面与真实输入框逐像素对比基本重合（文字墨迹重心偏差约 x +0.45 px、y −0.25 px）；结束后输入框有焦点；按键跳过且字符进入输入框；同一会话刷新不重播；尺寸变化直接跳到结束；暗色跟随。
- 待机动画：12 项中 10 项通过；1 项发现问题已修复：浅色下主色对白底 2.78:1，不到 3:1，改用 `primaryStrong`（`--el-color-primary-dark-2`），浅色 4.20:1，暗色为 `#66b1ff`，已在浏览器取像素确认；1 项仅观察：图形原创性。射线像常见的加载图标，光球是呼吸圆，不像 Claude / OpenAI 的标志，但仍需设计评审确认。

### 5.4 未测试（Not Tested）

| 项目 | 原因 | 代替做法 |
|---|---|---|
| 检索页 `SearchView` 实机运行（含第 7 节“关掉全部通道即取消”） | 需要登录和后端，本机不跑 Docker | 只做了类型检查和代码复核；动效部分与演示页用的是同一套组件和会话 |
| 真实读屏软件 | 环境里没有读屏软件 | 只核对了 `role="status"`、`aria-live="polite"` 和 Canvas / 卡片的 `aria-hidden` |
| 系统级“减少动态效果”设置 | 浏览器面板无法模拟系统设置 | 用演示页的强制开关和代码复核代替（三个动效都从 `reducedMotion.ts` 读） |
| Chrome 性能面板 60 / 30 fps、4x CPU 降速 | 当前环境做不了 | 未测 |
| 低端安卓设备 | 没有设备 | 未测 |
| SSR | 项目没有 SSR | 不适用 |

## 6. 修改建议（后续）

1. ~~文案“网页”改“文件”~~：已改，见第 7 节。
2. ~~检索进行中关掉全部通道不取消旧请求~~：已改，见第 7 节。
3. ~~启动动画占位文字太长~~：已缩短，见第 7 节。
4. 接口很快返回时是否允许加速播完（指南 §10 待确认事项）。目前按 Barry 的决定完整播一轮，结果约 4 s 后（3.6 s 一轮 + 0.4 s 收拢）才显示。
5. 浏览器帧率低于 10 fps 时启动动画会比墙钟时间慢：`dt` 封顶 100 ms 是有意为之，避免切回前台时画面一下跳到结尾。
6. 检索出错时，页面上方的 `el-alert` 和扫描区的状态行都会显示错误文字（后者带“重试”），信息重复，可以考虑只保留一处。
7. 如果要合回主仓库：先按 GLOBAL.md §2 P4、§11.4 走增强功能确认流程（说明工作量、依赖、风险、对论文主线的价值），再决定是否保留 `/motion-lab` 演示页（建议不合入，同时去掉 `router.ts` 里的公开路由）。

## 7. 跟进修改（2026-11-22，Barry 决定“三项都改”）

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `src/features/search-motion/messages.ts` | “正在打开网页…”改为“正在打开文件…”，“正在阅读第 i / n 个网页”改为“…个文件”；文件头注释同步 | 本系统检索的是文件，不是网页。只改文案，不影响状态机和测试 |
| `src/views/SearchView.vue` | `PLACEHOLDER` 由约 46 字缩短为“输入关键词，或描述想找的图片”（14 字），并注明原因 | 启动动画按每秒 10 字逐字打出，原占位文字让动画拖到约 8 s；现在约 4.75 s（3.1 s 起打 + 1.4 s + 0.25 s 停留）。各通道的说明仍在下方引导区 |
| 同上 | `onSearch`：检索词为空或没有选通道时，如果正在检索（`loading`），先 `session.cancel()` 再返回 | 原来检索进行中把通道全部关掉，旧请求返回后仍会显示结果。现在请求被中断、扫描动画回到 idle、显示引导区；之后重新勾选通道需要再点“检索”（此时没有结果和错误，自动重查的条件不成立） |
| `src/features/search-motion/lab/MotionLabView.vue` | 演示页占位文字与检索页保持一致 | 演示页用来预览启动动画，时长要与检索页相同 |

验证：`npm run typecheck` 通过；`npm test` 14 个文件 123 项通过；`npm run build` 成功；演示页实测扫描状态行依次显示“正在打开文件…”“正在阅读第 1–6 / 6 个文件”“正在整理答案…”，输入框占位文字为新文案。检索页里“关掉全部通道即取消”需要后端，**未测试（Not Tested）**，只做了代码复核：`session.cancel()` 会中断请求、让 `id` 失效，旧返回在 `run()` 里被丢弃，扫描动画回到 idle。

## 8. 启动动画改为循环播放（2026-11-22）

Barry 在演示页看过后决定：启动动画“在未输入时循环播放，输入后停止”。这取代了指南 §5.3 的“会话内只播一次”和之前确认的“会话内第一次进 `/search` 时播放”。

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `launch/loop.ts`（新增） | `createLaunchLoop({ play, canPlay, gap?, target? })`，返回 `start` / `wake` / `running` / `destroy`。一轮结束后停 `LAUNCH_LOOP_GAP`（3000 ms）再播下一轮，等待期间有 `pointerdown` / `keydown` / `wheel` / `touchstart` 就重新计时；开播前问 `canPlay()`，不满足就停下，等 `wake()` 再排；因减少动效或卸载而结束的不再排下一轮 | 循环规则与“画一轮”分开，可以用假定时器单独测试 |
| `launch/launchAnimation.ts` | 开播时自己给 `<html>` 打 `data-sm-launch`（第一轮仍由适配层在首帧前打）；结束时只在 `skip`（用户按键 / 点击）时聚焦输入框，自然播完不再聚焦 | 后续几轮也要隐藏真实输入框；自然播完就聚焦的话，“输入框有焦点”会让循环立刻停下 |
| `launch/useLaunchAnimation.ts` | 去掉 sessionStorage 判断；第一轮条件改为“没开减少动效且输入框为空”；挂载后创建循环，`canPlay` = 没开减少动效 && 输入框为空 && 输入框没有焦点；输入框失焦、减少动效关闭时 `wake()`；卸载时停循环、移除监听、显示输入框 | 用户点进输入框准备输入时不再播，避免输入框被藏起来；输入后清空、离开输入框，3 秒后重新开始循环 |
| `launch/playOnce.ts`（删除） | 不再需要“会话内只播一次” | 不留无用模块 |
| `lab/MotionLabView.vue` | 去掉 `resetLaunchPlayed`，“重播启动动画（刷新）”只刷新页面 | 循环本来就会重播，刷新用来从第一轮看起 |
| `tests/search-motion/launch.test.ts` | 删掉“会话内只播一次”的 2 项，新增“没有输入时循环播放”6 项：播完停 3 秒再播、等待期间操作重新计时、有内容或有焦点时停止且 `wake` 后恢复、开始就有内容不播、减少动效结束不再排、`destroy` 清干净 | — |
| `src/features/search-motion/README.md` | 启动动画的说明改为循环规则 | — |

检索页 `SearchView.vue` 不用改：`hasValue` 本来就是“检索词不为空”。所以从地址栏带着检索词进来不播；把检索词清空并离开输入框后，3 秒后开始循环。

验证：
- `npm run typecheck` 通过；`npm test` 14 个文件 127 项通过；`npm run build` 成功，懒加载的启动动画 chunk 为 2.46 KB（gzip）。
- 演示页实测：
  - 不操作时一轮约 4.6 s、间隔约 3.1 s，连续循环；
  - 点进输入框并输入“机房”、离开输入框后 9 s 内没有再播；
  - 清空后，只要还停在输入框里就不播，离开输入框 3.0 s 后恢复循环；
  - 控制台没有报错。
- 检索页实机**未测试（Not Tested）**，原因同第 5.4 节（需要登录和后端），已做代码复核。

注意：
- 页面空着的时候动画会一直循环。待机动画（8 秒无操作后出现）会和它同时在页面上动，是否需要让两者互斥，可以在设计走查时看。
- 循环期间点击页面上任何地方都会立即结束当前这一轮并聚焦输入框（沿用指南的“任意点击跳过”）。按键原来也一样，2026-11-25 改为别的控件有焦点时不抢（`new-feature-verification.md` V2）。

## 9. 待机动画的光球改为星尘粒子（2026-11-22）

Barry 要求光球“按 OpenAI《Introducing GPT-6.2 Astra and Sol》发布页头图的粒子特效来学习”。那张头图的内容是：深色背景上，一颗发光的星沿倾斜的轨道运动，拖着散开的星尘尾巴，尘粒闪烁，有四角星芒。这取代了指南 §4.3 原来规定的“实心圆呼吸 + 高光弧 + 涟漪”。

**做法**

- 只借鉴“发光核心、星尘拖尾、闪烁、四角星芒、倾斜椭圆轨道”这些通用视觉元素。
- 构图是自己的：两颗亮星在轨道上相隔半圈，对称地绕一个呼吸的核心转。
- 颜色沿用项目主色（浅色 `#337ecc`、暗色 `#66b1ff`），没有照搬原图的暖白配深色。
- 没有看、也没有复制对方页面的代码。
- 与 Claude / OpenAI 的 logo 造型无关（指南 §4.3 的原创要求不变）。

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `idle-spinner/draw.ts` | 光球部分重写为 `drawStardust`。<br>中心：径向渐变柔光，加呼吸的实心核（4 s 周期，±8%）。<br>2 颗亮星沿压扁（y × 0.6）、再倾斜 −0.42 rad 的椭圆轨道运动；各自带一个缓慢脉动的四角星芒。<br>每颗亮星拖一条约 1.15π 长的尾巴，各 90 粒星尘：越往尾巴越散、越暗、越往里收；每粒有自己的闪烁频率；每条尾巴有 2 粒带星芒。<br>远端粒子稍暗、稍小，有一点立体感。<br>粒子参数用固定种子（`mulberry32`）在模块加载时生成一次，画面不跳。<br>尺寸都按画布半径 R 计算。<br>新增 `withAlpha()`：把主题色转成 rgba，渐变才不会过渡到发灰的“透明黑”。<br>射线、morph（射线回收、光球 60%→100% 淡入）、共用旋转角都没变 | 待机动画状态机、计时、淡入淡出、减少动效（只显示静态射线）都不受影响；只换了光球的样子 |

**验证**

- `npm run typecheck` 通过；`npm test` 14 个文件 127 项通过；`npm run build` 成功。
- 演示页实测：
  - “固定光球”和“自动轮换”都正常显示；
  - 72 px 画布约 61 fps；
  - 控制台没有报错；
  - 放大到 230 px 预览，在浅色、暗色底上都检查过。
- 4× CPU 降速、低端设备仍然**未测试（Not Tested）**，原因同第 5.4 节。
- 每帧要画约 180 个小圆，外加几个星芒，比原来的实心圆多。原来那条“不像 Claude / OpenAI 标志”的观察结论，换成新图形后需要重新做设计评审。

## 10. 待机动画放大到 120 px（2026-11-22）

Barry 看过星尘光球后决定放大：72 px 时，闪烁、星芒、拖尾这些细节看不清。

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `idle-spinner/IdleSpinner.vue` | `size` 默认值 72 → 120 | 检索页和演示页都用默认值，两处一起变大。检索页引导区本来就有 5 行文字，高度够放 120 px；窄屏（≤ 600 px）照旧隐藏 |
| `idle-spinner/draw.ts` | 射线线宽封顶 4.5 px（`Math.min(R × 0.15, 4.5)`） | 射线按比例放大后，120 px 时线宽有 7.2 px，太粗；72 px 时线宽本来就是 4.3 px，不受影响。光球的所有尺寸都按半径计算，跟着变大 |

验证：
- `npm run typecheck` 通过；`npm test` 14 个文件 127 项通过；`npm run build` 成功。
- 演示页实测：射线和星尘光球在 120 px 下都正常显示，射线不再显得粗重。演示页的引导框因此从约 110 px 高变为 158 px。
- 检索页实机**未测试（Not Tested）**，原因同第 5.4 节。

## 11. 待机和启动用同一个星尘光球动画（2026-11-22）

Barry 决定：待机和启动做成同一个动画，都用第 9 节的星尘光球。

启动动画的做法也由 Barry 选定：星尘先在检索框中央聚成光球，再展开成检索框的边框。这样保留了启动动画“引出检索框”的作用。

这取代了：
- 指南 §4.3、§4.4：射线 / 光球两种样式、每 30 s 互相切换；
- 指南 §5.1：光标闪烁、60 个粒子聚成半径 24 px 的光环。

### 启动动画的新时间线

时间节点沿用原来的 `LAUNCH_TIMING`，没有改：
- 0 – 0.8 s：光球核心在检索框中央闪亮两下；
- 0.8 – 1.7 s：180 粒星尘和两颗亮星从四周飞来，聚成光球，两颗亮星拖着尾巴绕核心转；
- 2.1 – 2.9 s：转速放慢，星尘铺到胶囊轮廓上，核心淡出，闪烁和星芒收掉；
- 2.8 – 3.2 s：描边、图标淡入；
- 3.1 s 起：逐字打出占位文字。

总时长仍约 4.75 s。“没有输入时循环、输入后停止”的规则（第 8 节）不变。

### 修改的文件

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `shared/stardust.ts`（新增） | 从原 `idle-spinner/draw.ts` 抽出的星尘光球。导出：<br>• 粒子参数 `DUST`（固定种子，2 × 90 粒）、`ARMS`；<br>• 位置：`dustPose` / `headPose`；<br>• 亮度与大小：`twinkle`、`dustAlpha`、`dustRadius`；<br>• 画图：`drawCore`、`drawDust`、`drawHead`、`drawGlint`，以及整幅的 `drawStardust`。<br>粒子参数和画法与第 9 节相同 | 两个动画共用一套图形。启动动画需要拿到每粒星尘的位置，才能做聚拢和展开 |
| `idle-spinner/draw.ts`（删除） | 射线和 morph 不再需要 | 不留无用模块 |
| `idle-spinner/idleSpinner.ts` | 去掉样式选项、`switchEvery`、morph 补间、`TimerGroup`。<br>出现时淡入，并从 80% 放大到原大；消失时反过来。<br>减少动效时显示一帧静止的星尘光球（原来是静止射线） | 待机只剩一种样式；淡入淡出“从当前值出发”的规则不变 |
| `idle-spinner/IdleSpinner.vue` | props 只剩 `idleAfter`、`size` | 同上 |
| `launch/launchAnimation.ts` | 粒子改为星尘光球：<br>• 每粒星尘和亮星有随机飞来的起点；<br>• 按展开结束那一刻相对中心的方向，分到胶囊轮廓上的位置，展开时不交叉；<br>• 核心透明度 = max(闪亮, 聚拢) × (1 − 展开)；<br>• 展开时星尘透明度趋向 0.85、半径趋向 1.1 px，星芒收掉。<br>光球半径 48 px，与 120 px 的待机动画一样大；转速改为每秒 0.35 圈，与待机相同。颜色用 `primaryStrong` | 与待机视觉一致；对齐真实输入框、跳过、循环等逻辑都没动 |
| `launch/timeline.ts` | 删除 `PARTICLE_COUNT`、`RING_RADIUS`；注释改为新画面 | 时间轴纯函数不变，原有测试继续有效 |
| `lab/IdleLabPanel.vue` | 去掉样式单选；“快速走查”只改进入待机的时间（2 s） | 没有样式可选了 |
| `src/features/search-motion/README.md` | 结构和接口说明同步 | — |

### 验证

- `vue-tsc --noEmit` 通过；`vitest` 14 个文件 127 项通过；`npm run build` 成功，懒加载的启动动画 chunk 为 2.67 KB（gzip）。
- 演示页实测，启动动画逐段截图确认了：核心闪亮 → 星尘聚成光球 → 展开成胶囊虚线轮廓 → 描边出现、逐字打字 → 交给真实输入框。
- 待机 `show()` 显示星尘光球。
- 强制打开减少动效后，待机显示一帧静止画面，rAF 登记数为 0。
- 控制台没有报错。
- 检索页实机、低端设备、4× CPU 降速**未测试（Not Tested）**，原因同第 5.4 节。

### 注意

启动时每帧要画约 180 个粒子，比原来的 60 个多，在演示页上流畅，低端设备没测。新图形需要重新做设计评审（第 9 节已说明）。

## 12. 登录页加待机动画（2026-11-22）

Barry 要求登录页也加上这个待机动画，放在登录框下方。

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `src/views/LoginView.vue` | 在登录卡片下方加 `<IdleSpinner class="login-idle" />`，用默认参数：8 秒无操作出现，任意操作 0.4 秒内淡出，120 px | 与检索页同一个星尘光球。画布始终占 120 px 高的位置，出现、消失时页面不跳动；页面变长约 144 px（画布 120 px + 间距 24 px），窗口很矮时登录页会出现滚动条。登录逻辑没有改 |

验证：
- `vue-tsc --noEmit` 通过；`vitest` 127 项通过；`npm run build` 成功。
- 浏览器打开 `/login`（不需要后端），等 9 秒，登录框下方出现星尘光球。
- 实际登录流程需要后端，**未测试（Not Tested）**；登录逻辑没有改，只做了代码复核。

## 13. 登录页 logo 换成星尘光球 + 文档图标（2026-11-22）

Barry 要求把登录页顶部的 logo（原来是蓝色圆角方块里的文档图标）换成星尘光球，中间显示一个文档图标，图标从网上找。

Barry 选了：
- 图标用 Lucide 图标库的 `file-text`；
- 去掉第 12 节在登录框下方加的待机光球，页面上只留顶部一个。

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `src/components/AppIcon.vue` | 新增 `file-text` 图标：抄自 Lucide `file-text`（lucide-static v1.77.0，ISC 许可）的 5 条路径，注释里注明来源和许可 | 没有安装任何包，只是约 0.3 KB 的路径文字；已登记到 `docs/downloads.md` §2.8 #39。线宽沿用本组件的 1.8（Lucide 原图是 2） |
| `features/search-motion/shared/stardust.ts` | `drawCore` / `drawStardust` 新增可选参数 `{ coreRadius }`：放大实心核，柔光半径至少为实心核的 1.7 倍 | 实心核放大后，中间放得下图标；不传参数时画面和原来一样 |
| `features/search-motion/logo/StardustLogo.vue`（新增） | 120 px 画布画星尘光球，实心核为画布的 19%，HTML 的 `file-text` 图标（画布的 20%，颜色取页面底色）盖在正中。<br>一直转动（每秒 0.35 圈），用全页共用的 rAF 循环，页面切到后台时暂停。<br>减少动效时只画一帧静止画面。<br>主题变化时重新读色。<br>整体 `aria-hidden`：标题文字就在下面 | logo 不该等待机才出现，所以不用 `IdleSpinner`。白色图标对浅色下的实心核（`#337ecc`）约 4.2:1；暗色下图标为深色底色、实心核为 `#66b1ff` |
| `src/views/LoginView.vue` | 顶部 logo 换成 `<StardustLogo>`；删掉登录框下方的 `<IdleSpinner>`；页面上边距 72 → 40 px，标题上边距 12 → 4 px | logo 从 48 px 变成 120 px，收紧上方空白，登录框的位置大致不变 |
| `features/search-motion/README.md` | 目录说明加上 `logo/` | — |

验证：
- `vue-tsc --noEmit` 通过；`vitest` 127 项通过；`npm run build` 成功。
- 浏览器打开 `/login`（不需要后端）：星尘光球在标题上方转动，中间是白色的文档图标；控制台没有报错。
- 暗色主题下的登录页没有实际查看（项目目前没有暗色模式），颜色只做了代码复核。
- 实际登录需要后端，**未测试（Not Tested）**；登录逻辑没有改。

## 14. 登录页 logo 的光圈 10 秒一张一缩（2026-11-22）

Barry 要求登录页 logo 的光圈“先变大再变小，有规律地移动，10 秒一个循环”。

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `features/search-motion/shared/stardust.ts` | `StardustView` 新增可选的 `orbitScale`（默认 1），只缩放轨道半径，也就是星尘和亮星离核心的距离；粒子大小、核心大小不变 | 待机、启动动画不传这个参数，画面不变 |
| `features/search-motion/logo/StardustLogo.vue` | `orbitScale` 按余弦曲线变化：0 s 最小（72%），5 s 最大（原大），10 s 回到最小，如此循环。<br>旋转、闪烁照旧。<br>减少动效时停在原大 | 余弦曲线在最大、最小处都是平滑转向，没有顿挫。原大时最外侧的星芒离画布边缘约 5 px，不会被裁掉；不再继续放大，就是为了不出画布 |

验证：
- `vue-tsc --noEmit` 通过；`vitest` 127 项通过；`npm run build` 成功。
- 浏览器打开 `/login`，约每 2.5 s 截一次图：光圈从小（贴着中间的图标）到约 5 s 时最大，再缩回到约 10 s 时最小，循环正常；控制台没有报错。

## 15. 登录页 logo 的光圈缩放幅度加大（2026-11-22）

Barry 要求“放大缩小的程度变大”。

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `features/search-motion/logo/StardustLogo.vue` | 画布 120 → 160 px；光圈最小值 72% → 45%，最大仍为原大。实心核比例 19% → 14.5%、图标 20% → 15%，像素大小基本不变（约 23 px 半径、24 px 图标） | 最大和最小之比从 1.39 倍变成 2.2 倍。画布加大，最大时的光圈才不会出画布；最小时光圈贴住、部分盖在中间的圆上 |
| `src/views/LoginView.vue` | 页面上边距 40 → 24 px | logo 又高了 40 px，收一点上方空白 |

验证：浏览器打开 `/login`，约 4.6 s 时光圈最大、约 9.4 s 时最小，循环正常，最大时没有被裁掉。

## 16. 系统整体配色调节（2026-11-22）

Barry 要求加一个系统整体的配色调节，不只蓝白配色，可以调节，用于演示。

做法：全站颜色本来就都来自 Element Plus 的 CSS 变量，所以换配色只需要：
- 在 `<html>` 上改写主色那一组变量；
- 用 `html.dark` 切换 Element Plus 自带的暗色变量。

### 修改的文件

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `src/features/theme/theme.ts`（新增） | **预设主色** 6 个：海蓝（默认）、青碧、靛紫、琥珀橙、玫红、森绿。<br>**明暗模式**：浅色 / 深色 / 跟随系统。<br>**`paletteFor()`**：按 Element Plus 的算法算出 `--el-color-primary` 及 light-3/5/7/8/9、dark-2（暗色下与 `#141414` 混合，dark-2 与白色混合）。换了主色时，浅色下还给 `--app-bg` 掺 5% 主色；默认海蓝不掺。<br>**`contrastWarning()`**：自定义颜色太淡、白字看不清时给出提示。<br>**保存**：`loadTheme` / `saveTheme` 读写 `localStorage`，读写失败、内容损坏或不合法都回到默认值。<br>**`applyTheme()`**：写 `<html>` 的 style 和 `dark` 类，以及 `color-scheme` | 默认海蓝算出来的值与 Element Plus 自带的完全一致，所以不改配色时页面和原来一样 |
| `src/features/theme/store.ts`（新增） | 全局响应式状态。`initTheme()` 在挂载前应用保存过的配色；之后一改就应用并保存。“跟随系统”时监听系统深浅色变化 | 首屏就是保存过的配色，不会先闪一下蓝白 |
| `src/features/theme/ThemePicker.vue`（新增） | 页面右下角的圆形按钮（调色盘图标）。点开面板：6 个预设色点、一个彩虹色的“自定义”点（原生取色器）、浅色 / 深色 / 跟随系统、对比度提示、“恢复默认”。点面板外面或按 Esc 关闭 | 只用已注册的 `el-radio-group` / `el-radio-button` / `el-button`，没有新增组件注册 |
| `src/components/AppIcon.vue` | 新增 `palette` 图标（项目自己画的调色盘） | 面板按钮用 |
| `src/main.ts` | 全局引入 `element-plus/theme-chalk/dark/css-vars.css`（只在 `html.dark` 时生效）；挂载前调用 `initTheme()` | 暗色变量原来只在演示页引入 |
| `src/App.vue` | 根部加 `<ThemePicker />`，所有页面都有，包括登录页 | 演示时随时能切换 |
| `features/search-motion/lab/MotionLabView.vue` | 去掉自己引入的暗色样式；“切到暗色”按钮改为改全局配色的明暗模式 | 与配色面板共用一个状态，不会互相打架 |
| `tests/theme.test.ts`（新增，13 项） | 默认海蓝在浅色、暗色下与 Element Plus 自带值逐个相同；6 个预设色在浅色、暗色下对比度都达标、不比默认差；太淡的颜色有提示；保存读取（含损坏、非法值、存储抛异常）；明暗判断 | — |

### 联动

动效的颜色都会跟着变：
- 星尘光球、扫描动画通过 `tokens.ts` 监听 `<html>` 的 class / style，自动重新读色；
- 扫描卡片直接用 CSS 变量。

### 对比度

用 WCAG 公式计算，6 个预设色都满足：
- 白字在主色上：3.08–4.35:1，都不低于默认海蓝的 2.78:1；
- 浅色下 dark-2 对白底：4.60–6.21:1；
- 暗色下 dark-2 对 `#141414`：5.86–8.16:1。

### 验证

- `vue-tsc --noEmit` 通过；`vitest` 15 个文件 140 项通过；`npm run build` 成功。
- 浏览器实测（`/login`、`/motion-lab`）：
  - 面板能打开；
  - 选靛紫 + 深色后，整页变为深色，按钮、链接、星尘光球都变成紫色；
  - 选琥珀橙 + 浅色后，页面底色带一点暖色；
  - 刷新后配色保留；
  - 控制台没有报错；
  - 演示完已清掉浏览器面板里保存的配色。
- 登录后的页面（文件列表、检索页、预览页）在各配色下的样子：需要后端，**未测试（Not Tested）**。这些页面的颜色都来自同一组 CSS 变量，只做了代码复核。
- 自定义取色器只在代码里确认了绑定，没有在浏览器里实际拖动取色。

### 注意

- 默认配色下页面和原来完全一样。
- 选择只保存在当前浏览器。
- 这是演示用的增强功能。如果要合回主仓库，同样要走第 6 节第 7 条的确认流程。

## 17. 登录页 logo 的光圈放大时向左右拉长（2026-11-22）

Barry 要求：放大缩小的程度不变，左右比例的变化更大，左右不要太空，仍然 10 秒一个循环。

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `features/search-motion/shared/stardust.ts` | `StardustView` 新增可选的 `orbitStretch`（默认 1）：轨道在长轴方向（倾斜前的水平方向）再拉长 | 待机、启动动画不传这个参数，画面不变 |
| `features/search-motion/logo/StardustLogo.vue` | 画布 160 × 160 → 240 × 160（props 改为 `width` / `height`）。<br>同一个缩放进度 k（余弦曲线，10 s 一个循环）同时驱动两个量：<br>• 整体缩放：45% → 100%，与第 15 节相同；<br>• 左右拉长：1 → 1.9 倍。<br>减少动效时停在最大 | 最大时光圈的宽高比从约 1.7（原来的倾斜椭圆）变成约 2.9，两侧被星尘铺满；最外侧的星芒离左右边缘约 3 px、离上下边缘约 10 px，不会被裁掉 |

验证：
- `vue-tsc --noEmit` 通过。
- 浏览器打开 `/login`，在约 2.3 s、4.7 s、9.5 s 截图：分别是中间状态、最大（宽椭圆，左右铺开）、最小（贴住中间的圆）；循环正常。

## 18. 界面语言切换：中文 / English（2026-11-22）

Barry 要求增加一个切换语言的模块，一个英语、一个中文，放在配色按钮旁边。

做法：项目里没有 i18n 库，按“不安装新依赖”的规定，自己写了一个最小实现。
- `locale` 是一个 ref，`m()` 返回当前语言的文字表。模板和 computed 里调用 `m()`，语言一变就自动刷新。
- 原来写成常量表的标签（如 `STATUS_LABEL`）用 `translated()` 包一层，取值时才按当前语言生成，调用方的写法不用改。

### 新增

| 文件 | 内容 |
|---|---|
| `src/i18n/messages.ts` | 中文 `zh` 与英文 `en` 两套文字，共约 200 条，按页面分组：app、login、documents、preview、share、pdf、format、locator、channels、search、scan、api、theme、locale。`en` 的类型就是 `zh` 的结构，少一条或参数对不上，类型检查都会报错 |
| `src/i18n/index.ts` | `locale`、`m()`、`translated()`、`loadLocale` / `saveLocale`（localStorage，读写失败一律用中文），以及 `initLocale()`：同步 `<html lang>` 和页面标题，切换时保存 |
| `src/features/theme/LocaleSwitch.vue` | 右下角“中 \| EN”胶囊按钮，点一下立即切换，当前语言高亮（主色） |
| `tests/i18n.test.ts`（5 项） | 两套文字的键、类型、数组长度完全一致；英文里没有漏下的中文；`m()` / `translated()` 随语言切换；状态、位置、名次、扫描文案跟着切换；保存读取（含非法值、存储抛异常） |

### 修改

| 文件 | 修改 |
|---|---|
| `App.vue` | 侧栏标题、导航、管理员标签、退出登录改用 `m()`；右下角新增 `.floating-tools` 容器，放语言切换和配色按钮 |
| `views/LoginView.vue` | 全部文字；校验规则改成 computed；表单加 `:validate-on-rule-change="false"`，否则切换语言时会把空表单当场校验一遍，冒出一排红字（浏览器实测发现后修复） |
| `views/DocumentsView.vue`、`views/PreviewView.vue`、`views/SearchView.vue`、`components/ShareDialog.vue`、`components/PdfViewer.vue` | 全部界面文字 |
| `utils/format.ts`、`utils/locator.ts`、`utils/channels.ts` | 状态、来源、类型、位置、通道、名次等文字改为按当前语言生成 |
| `api/client.ts` | 前端自己生成的错误提示（连不上服务器、HTTP 错误等） |
| `features/search-motion/messages.ts` | 扫描动画、超时文案改为从 i18n 取 |
| `features/search-motion/scan-loader/scanLoader.ts` | “重试”按钮文字在每次出错时重新取 |
| `features/search-motion/launch/useLaunchAnimation.ts` | `placeholder` 可以传函数，每一轮开播前取一次，切换语言后下一轮就打新语言的占位文字 |
| `features/theme/theme.ts`、`ThemePicker.vue` | 配色面板文字、预设色名、对比度提示；面板改为相对按钮定位（位置由 App.vue 的容器决定） |
| `element.ts` | Element Plus 的全局语言改为 computed（`zh-cn` / `en`），分页、确认框按钮、空表格等自带文字跟着切换（用的是已安装的 element-plus 自带的语言包，没有新增依赖） |
| `main.ts` | 挂载前调用 `initLocale()` |

### 没有翻译的部分

- **后端返回的错误信息**（如登录失败的原因）：来自后端，仍是中文。
- **演示页 `/motion-lab` 自己的按钮和说明**：自测用，仍是中文；页面里的扫描动画、启动动画文字会跟着切换。
- **代码注释**：不翻译。

### 验证

- `vue-tsc --noEmit` 通过；`vitest` 16 个文件 145 项通过；`npm run build` 成功。
- 浏览器实测：
  - `/login` 在中文和英文之间来回切换，标题、说明、表单、按钮、页面标题（浏览器标签）都正确，没有多余的校验红字；
  - 配色面板英文显示正常；
  - `/motion-lab` 在英文下，扫描状态依次显示 “Opening files…”“Reading file 1 of 6”……；`<html lang>` 为 `en`；
  - 刷新后语言保留；
  - 演示完已清掉浏览器面板里保存的语言。
- 登录后的页面（文件列表、检索、预览、共享对话框、PDF 查看器）的英文显示需要后端，**未测试（Not Tested）**。只做了代码复核和类型检查：英文文字表的结构由类型检查保证完整，模板中的中文已全部替换（只剩注释）。
- 英文长度比中文长，表格列宽、按钮等可能出现换行或截断，同样需要登录后实际查看。

## 19. 登录页 logo 的光圈在两条对角线之间来回摆（2026-11-22）

Barry 要求：光圈按“左上—右下”“右上—左下”的节奏循环，一个循环 15 秒。

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `features/search-motion/shared/stardust.ts` | `StardustView` 新增可选的 `tilt`（轨道倾斜角），默认仍为固定的 `TILT`（−0.42 rad），并导出 `TILT` | 待机、启动动画不传这个参数，画面不变 |
| `features/search-motion/logo/StardustLogo.vue` | 倾斜角 = 0.42 × cos(2π t / 15 s)：<br>• 0 s：+0.42 rad，长轴“左上—右下”；<br>• 7.5 s：−0.42 rad，“右上—左下”；<br>• 15 s：回到“左上—右下”。<br>中间平滑经过水平，在两条对角线附近停留得久一些。<br>减少动效时停在原来的固定倾斜 | 摆动幅度与原来的固定倾斜相同（约 24°），最大、最宽时也不会出画布 |

说明：缩放和左右拉长仍是 10 秒一个循环，与 15 秒的摆动各走各的节奏，每 30 秒对齐一次。如果希望两者同步（例如都改成 15 秒），只需改 `PULSE_MS`。

验证：
- `vue-tsc --noEmit` 通过；`vitest` 145 项通过；`npm run build` 成功。
- 浏览器打开 `/login`，在约 4.6 s、7.8 s、12.8 s、15.3 s 截图：分别为略向“右上—左下”、明显“右上—左下”、“左上—右下”、“左上—右下”，与公式一致。

## 20. 缩放周期改为 15 秒，与摆动同步（2026-11-22）

Barry 选择让缩放（含左右拉长）也改成 15 秒，与第 19 节的摆动同步。

| 文件 | 修改 | 原因与影响 |
|---|---|---|
| `features/search-motion/logo/StardustLogo.vue` | `PULSE_MS` 10 000 → 15 000，注释同步 | 缩放和摆动同时起步：<br>• 0 s：最小，“左上—右下”；<br>• 7.5 s：最大、最宽，“右上—左下”；<br>• 15 s：回到最小，“左上—右下”。<br>每个循环完全一样 |

验证：
- `vue-tsc --noEmit` 通过；`vitest` 145 项通过。
- 浏览器在约 0.5 s、7.4 s、14.8 s 截图：最小 → 最大并呈“右上—左下” → 最小，与预期一致。
