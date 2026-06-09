#!/usr/bin/env python3
"""Build the Conflict Portfolio static site from chapter draft files."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMM = ROOT.parent
OUT = ROOT / "docs"

CHAPTERS = [
    {
        "slug": "birth-order",
        "title": "Birth Order",
        "subtitle": "Chapter 1",
        "source": COMM / "Attachment Style" / "birthOrder.txt",
    },
    {
        "slug": "attachment-style",
        "title": "Attachment Style",
        "subtitle": "Chapter 2",
        "source": COMM / "Attachment Style" / "attachmentStyle.txt",
    },
    {
        "slug": "personality-type",
        "title": "Personality Type",
        "subtitle": "Chapter 3",
        "source": COMM / "Personality type" / "draft.txt",
    },
    {
        "slug": "family-culture",
        "title": "Family & Culture",
        "subtitle": "Chapter 4",
        "source": COMM / "Family and Culture" / "draft.txt",
    },
    {
        "slug": "communication-style",
        "title": "Communication Style",
        "subtitle": "Chapter 5",
        "source": COMM / "Communication Style" / "draft.txt",
    },
    {
        "slug": "conflict-style",
        "title": "Conflict Style",
        "subtitle": "Chapter 6",
        "source": COMM / "Conflict Style" / "draft.txt",
    },
    {
        "slug": "coping-skills",
        "title": "Coping Skills",
        "subtitle": "Chapter 7",
        "source": COMM / "Coping Skills" / "draft.txt",
    },
    {
        "slug": "resolving-conflicts",
        "title": "Resolving Conflicts",
        "subtitle": "Chapter 8",
        "source": COMM / "Resolving Conflicts" / "draft.txt",
    },
]

SECTION_MARKERS = {
    "introduction",
    "reflection",
    "references",
    "a conflict i experienced",
    "my communication style",
    "my conflict style",
    "family background and culture",
    "how i cope with stress, anxiety, and negative emotions",
    "my myers-briggs score",
    "introduction page: birth order theory and conflict",
    "introduction page: attachment theory and conflict",
    "research page: middle-child birth order",
    "research page: anxious attachment style",
    "reflection page: middle-child birth order and conflict",
    "reflection page: anxious attachment style and conflict",
    "introduction: conflict styles and their role in team work",
    "strengths and growth areas",
    "key evidence and integration",
    "practical strategies (concise)",
    "anticipated challenges and mitigations",
    "measuring success",
    "practical example",
    "implementation plan",
    "conclusion and commitment",
    "brief summary: people tend toward five conflict styles, avoid, accommodate, compete, compromise, and collaborate, and each style has tradeoffs depending on context. avoidance can reduce short‑term tension but leaves problems unresolved, accommodation preserves relationships at the cost of unmet needs, competition can produce quick results while risking resentment, compromise yields partial wins for both sides, and collaboration seeks integrative solutions that attend to underlying concerns. collaboration is my default because it aims to maximize both solution quality and relationship protection, but collaboration requires process discipline and emotional awareness to work well.",
}


def is_heading(line: str) -> bool:
    text = line.strip()
    if not text:
        return False
    if text.startswith("\t"):
        return False
    lower = text.lower().rstrip(":")
    if lower.endswith(" questions"):
        return True
    if text.endswith(":") and len(text) < 80:
        return True
    if lower in SECTION_MARKERS:
        return True
    if text.lower().startswith("introduction page:"):
        return True
    if text.lower().startswith("research page:"):
        return True
    if text.lower().startswith("reflection page:"):
        return True
    if text in {
        "Resolving Conflicts",
        "Coping Skills and Conflict",
        "Communication Style and Conflict",
        "Family, Culture, and Conflict",
        "Myers-Briggs Personality Type and Conflict",
    }:
        return True
    return False


def heading_level(text: str) -> int:
    lower = text.lower()
    if lower.startswith("introduction page:") or lower.startswith("research page:") or lower.startswith("reflection page:"):
        return 2
    if " questions" in lower:
        return 3
    if lower == "references":
        return 2
    if lower in {"introduction", "reflection"}:
        return 2
    return 2


def convert_text_to_html(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    parts: list[str] = []
    refs_mode = False
    ref_items: list[str] = []

    def flush_refs():
        nonlocal refs_mode, ref_items
        if not ref_items:
            return
        parts.append('<div class="references">')
        parts.append("<h2>References</h2><ul>")
        for item in ref_items:
            item = item.strip()
            if not item:
                continue
            if "http://" in item or "https://" in item:
                url = item[item.find("http") :].strip()
                label = item[: item.find("http")].strip() or url
                parts.append(
                    f'<li>{escape(label)} <a href="{escape(url)}" target="_blank" rel="noopener noreferrer">{escape(url)}</a></li>'
                )
            else:
                parts.append(f"<li>{escape(item)}</li>")
        parts.append("</ul></div>")
        ref_items = []
        refs_mode = False

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue

        stripped = line.strip()
        lower = stripped.lower()

        if lower == "references":
            flush_refs()
            refs_mode = True
            continue

        if refs_mode:
            if line.startswith("\t"):
                ref_items.append(stripped)
            else:
                ref_items.append(stripped)
            continue

        if is_heading(line):
            level = heading_level(stripped)
            parts.append(f"<h{level}>{escape(stripped.rstrip(':'))}</h{level}>")
            continue

        if line.startswith("\t"):
            parts.append(f"<p>{escape(stripped)}</p>")
        else:
            parts.append(f"<p>{escape(stripped)}</p>")

    flush_refs()
    return "\n".join(parts)


def nav_html(active: str | None = None) -> str:
    links = ['<a href="index.html">Home</a>']
    for chapter in CHAPTERS:
        slug = chapter["slug"]
        cls = ' class="active"' if active == slug else ""
        links.append(f'<a href="{slug}.html"{cls}>{escape(chapter["title"])}</a>')
    return "\n".join(links)


def page_shell(title: str, body: str, active: str | None = None) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)} | Conflict Portfolio</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="site-header-inner">
      <h1><a href="index.html">Conflict Portfolio</a></h1>
      <p>Communication Course Portfolio</p>
      <nav class="top-nav" aria-label="Portfolio chapters">
        {nav_html(active)}
      </nav>
    </div>
  </header>
  <main class="page-wrap">
    {body}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <p>Conflict Portfolio &middot; Spring 2026</p>
    </div>
  </footer>
</body>
</html>
"""


def build_index() -> None:
    cards = []
    for chapter in CHAPTERS:
        cards.append(
            f"""<a class="chapter-card" href="{chapter['slug']}.html">
  <h3>{escape(chapter['subtitle'])}: {escape(chapter['title'])}</h3>
  <p>Introduction, personal results, reflection, and references.</p>
</a>"""
        )
    body = f"""
<section class="hero">
  <h2>Conflict Portfolio</h2>
  <p>Conflict is inevitable, but it does not have to damage relationships. This portfolio brings together what I learned about birth order, attachment style, personality type, family and culture, communication style, conflict style, coping skills, and resolving conflict in different contexts.</p>
  <p>Each chapter includes the full weekly writing: an introduction to the topic, my personal connection to it, reflection questions, and references.</p>
</section>
<section class="toc-grid">
  {''.join(cards)}
</section>
"""
    (OUT / "index.html").write_text(page_shell("Home", body), encoding="utf-8")


def build_chapters() -> None:
    for chapter in CHAPTERS:
        source = chapter["source"]
        content = source.read_text(encoding="utf-8")
        html = convert_text_to_html(content)
        body = f"""
<article class="chapter-content">
  <h2>{escape(chapter['subtitle'])}: {escape(chapter['title'])}</h2>
  {html}
</article>
"""
        (OUT / f"{chapter['slug']}.html").write_text(
            page_shell(chapter["title"], body, chapter["slug"]),
            encoding="utf-8",
        )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "css").mkdir(exist_ok=True)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    build_index()
    build_chapters()
    appendix = OUT / "appendix.html"
    if appendix.exists():
        appendix.unlink()
    print(f"Built portfolio site in {OUT}")


if __name__ == "__main__":
    main()
