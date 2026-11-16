# 007 · 让文字排版更顺眼（中英文）

原帖：https://x.com/Kubai087/status/2116555064227811412

## 原理

中文和英文都要处理对齐、行长不均、避头尾。几条全局 CSS 就能解决大部分问题。更重要的是做 i18n 时，让 Agent 结合实际布局挑选合适的译文：避免一个词被拆到两行，也避免出现过多空隙。

## 范围

只改文字如何换行、间距、对齐和截断；不改文案、字体、颜色和布局。规则放进全局文本样式（base CSS、排版 token 或 Tailwind 的 base 层），让每个页面自动继承。

## 规则

| 问题 | 做法 |
|---|---|
| 标题断行难看、最后一行只剩一两个字 | 标题、短文案用 `text-wrap: balance` |
| 段落末尾孤字、孤词 | 正文用 `text-wrap: pretty` |
| 中文标点跑到行首（避头尾） | `line-break: strict`；不要用 `line-break: anywhere` |
| 英文单词被从中间拆开 | 不要用 `word-break: break-all`；用 `word-break: normal` + `overflow-wrap: break-word`（只在单词长到放不下时才断） |
| 英文两端对齐出现大空隙 | 英文正文左对齐；需要断字时加 `lang="en"` 与 `hyphens: auto` |
| 中文段落边缘参差 | 中文正文可以 `text-align: justify`，汉字之间分配空隙不会难看 |
| 中西文之间没有间距 | `text-autospace: normal`（Chrome 140+，渐进增强）；不支持的浏览器不要靠手打空格硬补 |
| 全角标点挤压 | `text-spacing-trim: normal` |
| 行尾标点悬挂 | `hanging-punctuation: allow-end`（目前主要是 Safari，渐进增强） |
| 必须连在一起的短语 | 包一层 `white-space: nowrap` 的 span，长度控制在一屏宽以内 |

所有多语言文本都标正确的 `lang` 属性，浏览器才会按对应语言的规则断行和断字。

## i18n 选词

- 按钮、标签、导航、表头这类宽度固定的地方，先看译文放不放得下；放不下就换更短的说法（德语「Einstellungen speichern」→「Speichern」），而不是缩小字号或让它折成两行。
- 截断只用在用户可以从别处看到全文的地方（列表里的长文件名配 Tooltip），不要截断按钮文字。
- 给 Agent 的要求：改每一条文案前，对照它所在组件的最大宽度和字号估算长度。

## 参考实现

`assets/007-typography.html`：左右两栏对比，带容器宽度滑杆，可以直接观察 break-all、两端对齐、避头尾和 autospace 的差别。

## 验收

- [ ] 拖动容器宽度时，标题不出现单字成行，段落末尾不留孤字。
- [ ] 中文标点不出现在行首，英文单词不被拆开。
- [ ] 中西文之间有间距（支持的浏览器），不支持时也不乱。
- [ ] 固定宽度的按钮和标签在所有语言下都是一行。
