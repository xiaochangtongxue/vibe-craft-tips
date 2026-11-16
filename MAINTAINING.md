# 维护：新增一期

用户给出新一期原帖链接、要求加进本 skill 时按这里做。使用 skill 时不需要读这个文件。

## 1. 取原帖内容

- **每期的依据是作者随附的 Prompt 原文**（通常在作者自己的回复里），数值、时长、曲线都以它为准。没有 Prompt 就不动手写，不用视频截图或自己的推导去补。
- 正文：`https://api.fxtwitter.com/<user>/status/<id>`。x.com 未登录返回 402，也看不到作者回复。
- 拿 Prompt：先用已登录 X 的浏览器（Claude in Chrome，或在内置浏览器里让用户登录）打开原帖读作者回复；都不行就**立刻停下告诉用户**，请用户把 Prompt 贴过来，不要做完再在结尾提一句。
- 演示视频（mp4 可在内置浏览器里用 `video.currentTime` 逐段看）只用来对照效果，不作为数值来源。

## 2. 参考文件 `reference/NNN-slug.md`

格式跟已有各期一致：`# NNN · 标题` → `原帖：链接` → 原理 → 范围 → 数值/配方 → 实现要点（结尾写「参考实现见 `assets/NNN-slug.html`」）→ 常见错误 → 验收。改写整理，不照抄原文。

## 3. demo：每期一个独立页面 `assets/NNN-slug.html`

- **一期一页**，文件名和参考文件同名（`reference/014-delete-effects.md` ↔ `assets/014-delete-effects.html`）。不要把新一期塞进别的页面，也不要恢复成一个大文件。
- 页面结构照抄任意一期（如 `assets/013-shockwave-halo.html`）：`<!doctype html>` + `<meta charset="utf-8">` + 字体 + `<link rel="stylesheet" href="base.css">` + 本期 `<style>`；`<main class="page">` 里依次是空的 `<nav class="crumbs">`（脚本会填）、`<section class="tip" id="tNNN">`、`<p class="credit">`；最后 `<script src="base.js"></script>` + 本期 `<script>`。
- 公共部分只放在 `assets/base.css`（token、深浅色、标题、`.stage`、`.ctrls`、`.seg`、`.specs`、`.o-btn`）和 `assets/base.js`（`$`、`$$`、`clamp`、`seg()`、`reduceMotion`、`isDarkTheme()`、`onThemeChange()`）。本期需要的其他东西都写在本页里；不要为了一期去改公共文件，真正多期共用、改了不影响旧页面的才往里加。
- **命名空间**：本期的 class、id、`@keyframes`、自定义属性仍用 `tNNN-` 前缀（`.t014-card`、`#t014-app`、`--t015-pl`），因为它们和 `base.css` 在同一页里：001 用 `@property` 注册了 `--top`，撞名会让样式静默失效。001–011 保留历史前缀，不回头改。
- 本期的 CSS 和 JS 各用一行 `/* ---------- NNN 主题 ---------- */` 开头。
- 写完运行 `python3 scripts/build_index.py`：重写所有页面的翻页条（全部 / 上一期 / 下一期），重新生成 `assets/index.html`。

## 4. SKILL.md

description 里的条数、`001–NNN` 和新主题的触发词；正文标题和条数；索引表加一行（demo 页和参考文件同名，不用另列）。

## 5. 验证

- 本地预览用返回 `charset=utf-8` 的服务器。可以在项目 `.claude/launch.json` 里加：`python3 -c "import http.server as h, functools; H = h.SimpleHTTPRequestHandler; H.extensions_map['.html'] = 'text/html; charset=utf-8'; h.test(functools.partial(H, directory='<skill>/assets'), h.ThreadingHTTPServer, port=5186)"`，打开 `/NNN-slug.html`。
- 按常见笔记本窗口（如 1346 × 640）看一遍：舞台连同控件一屏放得下，底部的条、按钮点得到；舞台里的滚动区不要用 `overscroll-behavior: contain` 锁住页面滚动，否则鼠标在舞台上时滚不到下面。
- 检查控制台无报错，新一期每个状态都操作一遍，看终态截图。动效类的按 `reference/015-continuity.md` 第 7 节做两遍逐帧验收（暂停看几何、不暂停看时序）。预览窗格隐藏或计时不稳时中途截图不可信：用 JS 读状态确认，或对 `document.getAnimations()` 统一 `pause()` 并设 `currentTime`、按帧截图（WAAPI 动画）；自己的 rAF 动画给一个慢放开关。
- 检查新前缀没有残留旧名：`grep -n 'tNNN-' assets/NNN-slug.html`，并确认没有引入新的短前缀。
- 打开 `index.html` 和相邻两期，确认翻页链接正确。
