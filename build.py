#!/usr/bin/env python3
"""產生課程網站：python3 build.py

讀取 data/syllabus.json 與 src/lessons/NNN.html（每課的內文片段），
輸出 index.html 與 lessons/NNN.html。只用 Python 標準函式庫。

課文片段開頭要有一段 meta 註解，例如：
<!--meta
{"no": 1, "title": "……", "questions": ["問一", "問二"]}
-->
questions 依提問順序排列，對應內文中的 <div class="qa q1">、q2、q3……
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "lessons"
OUT = ROOT / "lessons"
SITE_TITLE = "佛典思想史每日課程"
REPO_URL = "https://github.com/BluesLion/madhyamaka-course"

META_RE = re.compile(r"<!--meta\s*(\{.*?\})\s*-->", re.S)

HEAD = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600&family=Noto+Serif+TC:wght@400;700&display=swap">
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<header class="site-header"><div class="wrap">
  <a class="brand" href="{base}index.html">{site}</a>
  <a href="{base}index.html#units">課程目錄</a>
</div></header>
<main class="wrap">
"""

FOOT = """
</main>
<footer class="wrap site-footer">
  <p>經文引自 <a href="https://cbetaonline.dila.edu.tw/">CBETA 線上閱讀</a>（中華電子佛典協會）。
  原始碼：<a href="{repo}">{repo_short}</a></p>
</footer>
</body>
</html>
"""

QNAMES = "一二三四五六七八九十"


def esc(s):
    return html.escape(s, quote=True)


def load_syllabus():
    data = json.loads((ROOT / "data" / "syllabus.json").read_text(encoding="utf-8"))
    index = {}
    for unit in data["units"]:
        lessons = unit["lessons"]
        for pos, (no, title) in enumerate(lessons, 1):
            index[no] = {"title": title, "unit": unit, "pos": pos, "total": len(lessons)}
    return data, index


def load_lessons():
    lessons = {}
    for path in sorted(SRC.glob("*.html")):
        raw = path.read_text(encoding="utf-8")
        m = META_RE.search(raw)
        if not m:
            raise SystemExit(f"{path.name} 缺少 <!--meta {{...}} --> 區塊")
        meta = json.loads(m.group(1))
        meta["body"] = META_RE.sub("", raw, count=1).strip()
        lessons[int(meta["no"])] = meta
    return lessons


def lesson_href(no, base=""):
    return f"{base}lessons/{no:03d}.html"


def render_lesson(no, meta, syl, done):
    info = syl[no]
    unit = info["unit"]
    title = meta.get("title") or info["title"]
    parts = [HEAD.format(
        title=esc(f"第 {no} 課｜{title}｜{SITE_TITLE}"),
        desc=esc(f"中觀課程第 {no} 課：{title}"),
        base="../", site=esc(SITE_TITLE),
    )]
    parts.append(f'<p class="kicker">單元{esc(unit["no"])}・{esc(unit["name"])}　第 {info["pos"]}／{info["total"]} 課</p>')
    parts.append(f"<h1>第 {no} 課｜{esc(title)}</h1>")

    qs = meta.get("questions") or []
    if qs:
        chips = "".join(
            f'<span class="chip q{i}">問{QNAMES[i - 1]}：{esc(q)}</span>'
            for i, q in enumerate(qs, 1)
        )
        parts.append(f'<div class="legend"><span class="legend-title">課後問答已展開在課文中</span>{chips}</div>')

    parts.append(meta["body"])

    # 上一課／下一課
    prev_no, next_no = no - 1, no + 1
    if prev_no in done:
        prev = f'<a href="{prev_no:03d}.html">← 第 {prev_no} 課｜{esc(syl[prev_no]["title"])}</a>'
    else:
        prev = '<a href="../index.html#units">← 課程目錄</a>'
    if next_no in done:
        nxt = f'<a class="right" href="{next_no:03d}.html">第 {next_no} 課｜{esc(syl[next_no]["title"])} →</a>'
    elif next_no in syl:
        nxt = f'<span class="right disabled">第 {next_no} 課｜{esc(syl[next_no]["title"])}（尚未上課）</span>'
    else:
        nxt = '<span class="right disabled">全課程完</span>'
    parts.append(f'<nav class="pager">{prev}{nxt}</nav>')
    parts.append(FOOT.format(repo=REPO_URL, repo_short=REPO_URL.replace("https://", "")))
    return "\n".join(parts)


def render_index(data, syl, done):
    total = len(syl)
    n_done = len(done)
    pct = round(n_done / total * 100, 1)
    latest = max(done) if done else None

    p = [HEAD.format(
        title=esc(f"{SITE_TITLE}：以中觀為主軸"),
        desc=esc("從阿含、般若經到龍樹《中論》，以中觀為主軸按歷史順序讀懂佛典，每天 15 分鐘。"),
        base="", site=esc(SITE_TITLE),
    )]
    p.append('<section class="hero">')
    p.append('<p class="kicker">MADHYAMAKA COURSE</p>')
    p.append(f"<h1>{esc(SITE_TITLE)}<br>以中觀為主軸</h1>")
    p.append('<p class="subtitle">每天一課、約 15 分鐘，共 174 課。先補足中觀要回應的阿含與部派背景，再讀般若經、龍樹與《大智度論》，然後順著歷史看中觀如何被漢傳三論、唯識、如來藏、密教、天台華嚴禪與藏傳各宗接續或回應。</p>')
    p.append(f'<div class="progress">已上 {n_done}／{total} 課')
    if latest:
        p.append(f'　·　最新：<a href="{lesson_href(latest)}">第 {latest} 課｜{esc(syl[latest]["title"])}</a>')
    p.append(f'<div class="progress-bar"><div style="width:{pct}%"></div></div></div>')
    p.append("</section>")

    p.append('<div class="howto"><strong>每課的固定格式</strong><ol>'
             "<li><strong>脈絡</strong>：時代、作者、這段文字在回應什麼問題。</li>"
             "<li><strong>原文</strong>：附經論名、卷次與 CBETA 連結（連到行首）。</li>"
             "<li><strong>逐句解說</strong>：白話翻譯，再講論證怎麼走。</li>"
             "<li><strong>名詞卡</strong>：新名詞的中文、梵文、定義，以及之後在哪一課再出現。</li>"
             "<li><strong>回扣與預告</strong>：連回學過的課，預告下一課。</li>"
             "</ol><p style=\"margin:.6rem 0 0\">課後的提問會直接展開在課文裡，每一問用一種顏色標示。</p></div>")

    p.append('<div id="units">')
    for unit in data["units"]:
        first, last = unit["lessons"][0][0], unit["lessons"][-1][0]
        p.append('<section class="unit">')
        p.append('<div class="unit-head">'
                 f'<span class="unit-no">單元{esc(unit["no"])}</span>'
                 f'<h2>{esc(unit["name"])}</h2>'
                 f'<span class="unit-meta">{esc(unit["era"])}　·　第 {first}–{last} 課</span></div>')
        p.append(f'<p class="unit-lead">{esc(unit["lead"])}</p>')
        p.append('<ol class="lesson-list">')
        for no, title in unit["lessons"]:
            if no in done:
                badge = '<span class="badge">新</span>' if no == latest else ""
                p.append(f'<li class="done"><span class="n">{no:03d}</span><a href="{lesson_href(no)}">{esc(title)}</a>{badge}</li>')
            else:
                p.append(f'<li class="pending"><span class="n">{no:03d}</span><span>{esc(title)}</span></li>')
        p.append("</ol></section>")
    p.append("</div>")
    p.append(FOOT.format(repo=REPO_URL, repo_short=REPO_URL.replace("https://", "")))
    return "\n".join(p)


def main():
    data, syl = load_syllabus()
    lessons = load_lessons()
    done = set(lessons)
    unknown = done - set(syl)
    if unknown:
        raise SystemExit(f"課綱裡沒有這些課號：{sorted(unknown)}")
    OUT.mkdir(exist_ok=True)
    for no, meta in sorted(lessons.items()):
        (OUT / f"{no:03d}.html").write_text(render_lesson(no, meta, syl, done), encoding="utf-8")
    (ROOT / "index.html").write_text(render_index(data, syl, done), encoding="utf-8")
    print(f"已產生 index.html 與 {len(done)} 課")


if __name__ == "__main__":
    main()
