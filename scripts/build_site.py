#!/usr/bin/env python3
from __future__ import annotations

import json
from html import escape
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "issues"
REPORT_DIR = ROOT / "reports"
SCHEMA_PATH = ROOT / "pipeline" / "report.schema.json"

LEVEL_LABELS = {
    "primary": "一手来源",
    "media": "高可信媒体",
    "context": "政策基线 / 背景",
    "research": "机构研究",
}


def e(value: object) -> str:
    return escape(str(value), quote=True)


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_issues() -> list[dict]:
    issues = []
    schema = load_schema()
    validator = Draft202012Validator(schema)
    for path in sorted(DATA_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
        if errors:
            messages = []
            for err in errors:
                location = ".".join(map(str, err.path)) or "<root>"
                messages.append(f"{path}: {location}: {err.message}")
            raise SystemExit("\n".join(messages))
        if path.stem != data["issue"]["date"]:
            raise SystemExit(f"{path}: filename must equal issue.date")
        issues.append(data)
    if not issues:
        raise SystemExit("No issue JSON files found under data/issues/")
    return sorted(issues, key=lambda x: x["issue"]["date"], reverse=True)


def source_card(item: dict) -> str:
    level = item["source_level"]
    parts = [
        '<div class="source-card">',
        '<div class="source-head">',
        f'<span class="badge {e(level)}">{e(LEVEL_LABELS[level])}</span>',
        f'<span class="badge">{e(item["source_name"])}</span>',
        f'<span class="source-meta">{e(item["published"])}</span>',
        '</div>',
        f'<div class="source-title">{e(item["title"])}</div>',
        f'<p><strong>中文摘要：</strong>{e(item["summary"])}</p>',
    ]
    if item.get("why_it_matters"):
        parts.append(f'<p class="tiny"><strong>为什么值得关注：</strong>{e(item["why_it_matters"])}</p>')
    if item.get("caveat"):
        parts.append(f'<p class="tiny"><strong>核查提示：</strong>{e(item["caveat"])}</p>')
    parts.append(f'<div class="fact-type">信息性质：{e(item["information_type"])}</div>')
    parts.append(f'<a class="source-link" href="{e(item["url"])}" target="_blank" rel="noopener">查看原文 ↗</a>')
    if item.get("related_url"):
        parts.append(f' <a class="source-link related" href="{e(item["related_url"])}" target="_blank" rel="noopener">相关一手资料 ↗</a>')
    parts.append('</div>')
    return "".join(parts)


def render_issue(data: dict) -> str:
    issue = data["issue"]
    window = data["window"]
    nav = [
        '<a href="../index.html">← 返回首页</a>',
        '<a href="#overview">信息速览</a>',
        '<a href="#sources">原始资料索引</a>',
        '<a href="#calendar">下周日历</a>',
    ]
    body = [
        '<!doctype html><html lang="zh-CN"><head>',
        '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
        f'<meta name="description" content="{e(issue["title"])}">',
        f'<title>{e(issue["title"])}｜{e(issue["date"])}</title>',
        '<link rel="stylesheet" href="../assets/style.css">',
        '''<style>
.source-card{border:1px solid rgba(127,127,127,.22);border-radius:14px;padding:18px 20px;margin:16px 0;background:rgba(255,255,255,.02)}
.source-head{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:8px}.badge{display:inline-block;padding:3px 8px;border-radius:999px;font-size:.78rem;border:1px solid rgba(127,127,127,.35)}
.badge.primary{font-weight:700}.badge.context{opacity:.76}.source-title{font-size:1.02rem;font-weight:700;margin:.35rem 0}.source-meta{font-size:.86rem;opacity:.72}.source-card p{margin:.6rem 0}.source-link{display:inline-block;margin:6px 10px 0 0;font-weight:650;text-decoration:none}.related{opacity:.82}.fact-type,.tiny{font-size:.84rem;opacity:.74}.brief-list li,.index-list li{margin:.55rem 0}.section-note{border-left:3px solid currentColor;padding-left:14px;opacity:.8}.calendar-row{display:grid;grid-template-columns:110px 1fr;gap:14px;padding:12px 0;border-bottom:1px solid rgba(127,127,127,.18)}
@media(max-width:640px){.calendar-row{grid-template-columns:1fr;gap:3px}.source-card{padding:15px}}
</style>''',
        '</head><body>',
        '<header class="hero"><div class="wrap">',
        f'<div class="eyebrow">Gold Weekly · Issue {issue["number"]:03d} · Source-first</div>',
        f'<h1>{e(issue["title"])}</h1>',
        f'<p>观察窗口：{e(window["start"])}—{e(window["end"])}｜国际一手信息与可核查来源优先</p>',
        f'<nav class="nav">{"".join(nav)}</nav></div></header><main>',
        '<section class="section" id="overview"><div class="wrap article"><span class="tag">本周信息速览</span><h2>这一周最值得知道的事实</h2><ul class="brief-list">',
        ''.join(f'<li>{e(x)}</li>' for x in data["overview"]),
        '</ul><div class="callout"><strong>阅读方式：</strong>正文优先回答“发生了什么、原文在哪里、中文读者如何快速读懂”。参考分析集中在文末。</div></div></section>',
    ]

    for idx, section in enumerate(data["sections"], start=1):
        body.append(f'<section class="section" id="{e(section["id"])}"><div class="wrap article"><h2>{idx}. {e(section["title"])}</h2>')
        if section.get("note"):
            body.append(f'<p class="section-note">{e(section["note"])}</p>')
        for group in section["groups"]:
            if group["name"]:
                body.append(f'<h3>{e(group["name"])}</h3>')
            body.extend(source_card(item) for item in group["items"])
        body.append('</div></section>')

    section_no = len(data["sections"]) + 1
    body.append(f'<section class="section" id="sources"><div class="wrap article sources"><h2>{section_no}. 本周重要原始资料索引</h2><ol class="index-list">')
    body.extend(f'<li><a href="{e(x["url"])}" target="_blank" rel="noopener">{e(x["label"])}</a></li>' for x in data["source_index"])
    body.append('</ol></div></section>')

    section_no += 1
    body.append(f'<section class="section" id="calendar"><div class="wrap article"><h2>{section_no}. 下周信息日历</h2><p>只列已经公开确定的发布时间和会议安排，不预测结果。</p>')
    for row in data["calendar"]:
        body.append(f'<div class="calendar-row"><strong>{e(row["date"])}</strong><div><strong>{e(row["title"])}</strong>：{e(row["summary"])}<br><a href="{e(row["url"])}" target="_blank" rel="noopener">官方/原始页面 ↗</a></div></div>')
    body.append('</div></section>')

    section_no += 1
    body.append(f'<section class="section"><div class="wrap article"><h2>{section_no}. 简短参考分析</h2><div class="callout"><strong>以下属于参考分析，不构成事实陈述或投资建议。</strong></div><ul class="brief-list">')
    body.extend(f'<li>{e(x)}</li>' for x in data["analysis"])
    body.append('</ul></div></section>')

    section_no += 1
    body.append(f'<section class="section"><div class="wrap article"><h2>{section_no}. 给非专业中文读者的简明摘要</h2><div class="callout">')
    body.extend(f'<p>{e(x)}</p>' for x in data["plain_summary"])
    body.append('</div><p class="muted">本周报用于国际公开信息收集、中文整理与研究参考，不构成投资建议。</p></div></section>')
    body.append(f'</main><footer class="footer"><div class="wrap">Gold Weekly · Issue {issue["number"]:03d} · {e(issue["date"])}</div></footer></body></html>')
    return ''.join(body)


def render_index(issues: list[dict]) -> str:
    latest = issues[0]
    latest_issue = latest["issue"]
    archive = []
    for data in issues:
        issue = data["issue"]
        archive.append(
            f'<div class="report-item"><div><strong>{e(issue["date"])}</strong><div class="muted">第 {issue["number"]} 期 · Source-first 信息汇编</div></div>'
            f'<a href="reports/{e(issue["date"])}.html">打开 →</a></div>'
        )
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="全球黄金信息周报"><title>Gold Weekly｜全球黄金信息周报</title><link rel="stylesheet" href="assets/style.css"></head><body>
<header class="hero"><div class="wrap"><div class="eyebrow">Gold Weekly · Source-first International Digest</div><h1>全球黄金信息周报</h1><p>为中文读者整理国际黄金相关一手信息：保留原文入口，提供中文摘要，区分事实、官方说法、媒体报道与参考分析。</p><nav class="nav"><a href="#latest">最新一期</a><a href="#archive">历史周报</a><a href="#method">方法说明</a></nav></div></header>
<main><section class="section" id="latest"><div class="wrap"><span class="tag">Latest</span><h2>最新一期</h2><div class="grid"><article class="card"><div class="muted">{e(latest["window"]["start"])}—{e(latest["window"]["end"])}</div><h3>{e(latest_issue["title"])}</h3><p>{e(latest["overview"][0])}</p><a class="btn" style="color:#3e351f;border-color:#b9a36b" href="reports/{e(latest_issue["date"])}.html">阅读完整周报 →</a></article><article class="card"><div class="muted">核心方式</div><div class="metric">Source-first</div><p>重要信息保留来源、发布日期、原文标题、中文摘要、信息性质和可点击原文链接。</p></article><article class="card"><div class="muted">分析占比</div><div class="metric">≤ 15%</div><p>分析仅用于解释可能的影响机制，不作为周报主体，也不提供确定性交易建议。</p></article></div></div></section>
<section class="section" id="archive"><div class="wrap"><h2>历史周报</h2><div class="report-list">{''.join(archive)}</div></div></section>
<section class="section" id="method"><div class="wrap article"><h2>方法说明</h2><p class="lead">站点标准由仓库中的 <code>pipeline/REPORT_SPEC.md</code> 和 JSON Schema 固定，不由单次生成提示词临时决定。</p><div class="grid"><div class="card"><h3>来源优先</h3><p>央行、财政部、统计机构、国际组织、交易所与行业一手数据优先；Reuters、Bloomberg、AP、FT、WSJ、BBC 等用于补充与交叉核验。</p></div><div class="card"><h3>可人工编辑</h3><p>每期内容储存在 <code>data/issues/YYYY-MM-DD.json</code>。人工修改 JSON 后，构建程序会重新生成网页。</p></div><div class="card"><h3>可验证构建</h3><p>GitHub Actions 部署前验证结构化数据是否符合固定 Schema，再生成所有报告与首页。</p></div></div></div></section></main><footer class="footer"><div class="wrap">Gold Weekly · 信息整理与研究使用</div></footer></body></html>'''


def main() -> None:
    issues = load_issues()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    for data in issues:
        path = REPORT_DIR / f'{data["issue"]["date"]}.html'
        path.write_text(render_issue(data), encoding="utf-8")
        print(f"built {path.relative_to(ROOT)}")
    (ROOT / "index.html").write_text(render_index(issues), encoding="utf-8")
    print("built index.html")


if __name__ == "__main__":
    main()
