# 004 · 递进式圆角 + 连续曲率圆角（超椭圆）

原帖：https://x.com/Kubai087/status/2115469767650021796

## 原理

- 等距内缩：嵌套元素的内圆角 = 外圆角 − 间距（r = R − p），内外两段圆弧共用一个圆心，转角处的间距才和直边一样宽。直接对 AI 说「等距内缩」往往就够用。
- 连续圆角：普通 `border-radius` 是圆弧直接接直线，曲率在接缝处突变，有一道隐约的折痕。超椭圆过渡更顺，类似 iOS 的圆角。

## 规则

1. 由外向内推：对话框 / 卡片 → 面板、输入框、按钮 → chip、tag。容器圆角 R、内边距 p，内层取 R − p。例：对话框 32 + 内边距 16 → 面板和按钮 16；16 的面板里内缩 8 的 chip → 8。
2. 同一层级共用一个圆角值。
3. 最小 4px，再小就不再递减。
4. 胶囊和圆形保持全圆，不参与递减。
5. padding、gap、radius 都落在 4px 栅格上。
6. 项目有圆角 token 就改 token，不要硬编码。
7. 连续圆角做渐进增强：保留 `border-radius`，在 `@supports (corner-shape: superellipse(1.25))` 里加 `corner-shape: superellipse(1.25)`；胶囊和圆形显式设 `corner-shape: round`。目前 Chrome / Edge 139+ 支持，其他浏览器自动退回普通圆角。
8. 改完列出清单：`元素: 旧值 -> 新值`。

## 实现要点

```css
:root {
  --radius-dialog: 32px;
  --space-dialog: 16px;
  --radius-panel: max(4px, calc(var(--radius-dialog) - var(--space-dialog))); /* 16 */
  --space-panel: 8px;
  --radius-chip: max(4px, calc(var(--radius-panel) - var(--space-panel)));    /* 8 */
}
@supports (corner-shape: superellipse(1.25)) {
  :where(*) { corner-shape: superellipse(1.25); }
  .pill, .avatar { corner-shape: round; }
}
```

- Tailwind：在 `theme.extend.borderRadius` 定义 `dialog / panel / chip`，并保持 `rounded-dialog p-4 > rounded-panel p-2 > rounded-chip` 的配对。
- 超椭圆会改变视觉上的等效圆角大小，不支持的浏览器退回同一个 `border-radius` 时观感可能有偏差；要求高时分别在 Chrome 和 Safari 比对，必要时给退回值单独换算。
- 自查办法：在每个元素左上角按它的圆角画一个虚线圆和圆心点，正确时各层圆心重合。参考实现见 `assets/004-concentric-radius.html`（含「显示圆心」）。

## 常见错误

- 内外写成同一个值（都是 16）：内层转角显得鼓出来，角上间距变窄。
- 内层圆角比外层还大：像两张不相干的卡片叠在一起。
- 胶囊按钮也套 R − p：胶囊变成圆角矩形。
- 只改了圆角没改 padding，公式不再成立。

## 验收

- [ ] 每一层嵌套都满足 r = R − p，且不小于 4px。
- [ ] 同层级圆角一致；胶囊、头像保持全圆。
- [ ] 不支持 `corner-shape` 的浏览器里布局不变。
- [ ] 输出了 `元素: 旧值 -> 新值` 清单。
