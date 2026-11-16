const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
const isDarkTheme = () => getComputedStyle(document.documentElement).getPropertyValue('--is-dark').trim() === '1';
function onThemeChange(fn) {
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', fn);
  new MutationObserver(fn).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
}
function seg(el, fn) {
  el.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b || b.disabled) return;
    $$('button', el).forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    fn(b.dataset.v, b);
  });
}
