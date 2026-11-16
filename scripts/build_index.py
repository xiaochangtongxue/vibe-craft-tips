# 重写 assets/ 下每期页面的翻页条，并重新生成 assets/index.html。新增一期后运行：python3 scripts/build_index.py
import sys, re, pathlib, html
A = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "assets"
pages = sorted(p for p in A.glob('[0-9][0-9][0-9]-*.html'))
titles = [re.search(r'<title>\d{3} · (.*?)</title>', p.read_text()).group(1) for p in pages]
for i, p in enumerate(pages):
    prev = f'<a href="{pages[i-1].name}">← {pages[i-1].name[:3]}</a>' if i else ''
    nxt = f'<a href="{pages[i+1].name}">{pages[i+1].name[:3]} →</a>' if i + 1 < len(pages) else ''
    nav = f'<nav class="crumbs" aria-label="翻页"><a href="index.html">全部 {len(pages)} 期</a><span style="display:flex;gap:16px">{prev}{nxt}</span></nav>'
    t = re.sub(r'<nav class="crumbs".*?</nav>', nav, p.read_text(), count=1, flags=re.S)
    p.write_text(t)
first = pages[0].read_text()
head = first[:first.index('<link rel="stylesheet" href="base.css">')]
head = re.sub(r'<title>.*?</title>', '<title>Vibe 质感小技巧</title>', head)
credit = re.search(r'<p class="credit">.*?</p>', first).group(0)
items = '\n'.join(f'  <li><a href="{p.name}"><span>{p.name[:3]}</span>{html.escape(t)}</a></li>' for p, t in zip(pages, titles))
(A / 'index.html').write_text(f'''{head}<link rel="stylesheet" href="base.css">
<style>
.idx h1 {{ font: 650 clamp(28px, 4vw, 40px)/1.15 var(--font); letter-spacing: -.025em; margin: 8px 0 8px; }}
.idx > p {{ margin: 0 0 28px; color: var(--muted); }}
.idx ol {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 10px; }}
.idx ol a {{ display: flex; gap: 14px; align-items: baseline; padding: 14px 16px; border-radius: 12px; background: var(--surface); box-shadow: 0 0 0 1px var(--line); text-decoration: none; color: var(--fg); }}
.idx ol a:hover {{ box-shadow: 0 0 0 1px var(--line-strong); }}
.idx ol a span {{ font: 500 12.5px var(--mono); color: var(--accent); }}
</style>
</head>
<body>
<main class="page idx">
<h1>让你 Vibe 的产品更有质感</h1>
<p>{len(pages)} 期，每期一页，舞台都可以直接上手操作。</p>
<ol>
{items}
</ol>
{credit}
</main>
</body>
</html>
''')
print(len(pages), 'pages')
