#!/usr/bin/env python3
"""Build the Conflict Portfolio static site from chapter draft files."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMM = ROOT.parent
OUT = ROOT / "docs"
STUDENT_NAME = "Tristan Johnson"

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


def primary_action(active: str | None = None) -> tuple[str, str]:
    if active is None:
        return f"{CHAPTERS[0]['slug']}.html", "Start Reading"
    for index, chapter in enumerate(CHAPTERS):
        if chapter["slug"] == active:
            if index + 1 < len(CHAPTERS):
                next_chapter = CHAPTERS[index + 1]
                return f"{next_chapter['slug']}.html", "Next Chapter"
            return "index.html", "Back to Home"
    return f"{CHAPTERS[0]['slug']}.html", "Start Reading"


def toc_menu_html(active: str | None = None) -> str:
    home_cls = "toc-item is-current" if active is None else "toc-item"
    items = [f'<a href="index.html" class="{home_cls}" role="menuitem">Home</a>']
    for index, chapter in enumerate(CHAPTERS, start=1):
        cls = "toc-item is-current" if active == chapter["slug"] else "toc-item"
        label = f"Chapter {index}: {chapter['title']}"
        items.append(
            f'<a href="{chapter["slug"]}.html" class="{cls}" role="menuitem">{escape(label)}</a>'
        )
    return "\n            ".join(items)


def bottom_nav_html(active: str | None = None) -> str:
    href, label = primary_action(active)
    return (
        f'<nav class="chapter-bottom-nav" aria-label="Continue reading">'
        f'<a href="{href}" class="btn btn-primary">{escape(label)}</a>'
        f"</nav>"
    )


def header_actions_html(active: str | None = None, suffix: str = "main") -> str:
    menu_id = f"toc-menu-{suffix}"
    toggle_id = f"toc-toggle-{suffix}"
    href, label = primary_action(active)
    return f"""<div class="header-actions">
          <div class="toc-dropdown">
            <button type="button" class="btn btn-ghost" id="{toggle_id}" aria-expanded="false" aria-controls="{menu_id}" aria-haspopup="true">
              Table of Contents
            </button>
            <div class="toc-menu" id="{menu_id}" role="menu" hidden>
              {toc_menu_html(active)}
            </div>
          </div>
          <a href="{href}" class="btn btn-primary">{escape(label)}</a>
        </div>"""


def header_html(active: str | None = None, variant: str = "main") -> str:
    suffix = "dock" if variant == "dock" else "main"
    if variant == "dock":
        header_class = "site-header site-header--dock"
        header_id = ' id="header-dock"'
        subtitle = ""
        title_markup = '<p class="dock-title"><a href="index.html">Conflict Portfolio</a></p>'
    else:
        header_class = "site-header site-header--main"
        header_id = ""
        subtitle = "<p>Communication Course Portfolio</p>"
        title_markup = "<h1><a href=\"index.html\">Conflict Portfolio</a></h1>"

    return f"""<header class="{header_class}"{header_id} aria-hidden="{"true" if variant == "dock" else "false"}">
    <div class="site-header-inner">
      <div class="header-row">
        <div class="header-brand">
          {title_markup}
          {subtitle}
        </div>
        {header_actions_html(active, suffix)}
      </div>
    </div>
  </header>"""


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
  {header_html(active, "main")}
  {header_html(active, "dock")}
  <main class="page-wrap">
    {body}
    {bottom_nav_html(active)}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <p>{escape(STUDENT_NAME)} &middot; Conflict Portfolio &middot; Spring 2026</p>
    </div>
  </footer>
  <button type="button" class="back-to-top" id="back-to-top" aria-label="Return to top">
    <span aria-hidden="true">&uarr;</span>
  </button>
  <script>
  (function () {{
    var mainHeader = document.querySelector(".site-header--main");
    var dock = document.getElementById("header-dock");
    var backToTop = document.getElementById("back-to-top");
    var lastY = window.scrollY || 0;
    var dockOpen = false;
    var suppressDockUntilTop = false;
    var atTopThreshold = 16;
    var atBottomThreshold = 32;
    var scrollDelta = 4;
    var backToTopThreshold = 400;

    function atPageBottom() {{
      var y = window.scrollY || 0;
      var maxScroll = Math.max(
        0,
        document.documentElement.scrollHeight - window.innerHeight
      );
      return maxScroll - y <= atBottomThreshold;
    }}

    function wireToc(headerRoot) {{
      if (!headerRoot) return;
      var toggle = headerRoot.querySelector(".toc-dropdown button");
      var menu = headerRoot.querySelector(".toc-menu");
      if (!toggle || !menu) return;

      function closeMenu() {{
        menu.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
      }}

      headerRoot.querySelector(".toc-dropdown").addEventListener("click", function (event) {{
        event.stopPropagation();
      }});

      toggle.addEventListener("click", function () {{
        var open = menu.hidden;
        document.querySelectorAll(".toc-menu").forEach(function (other) {{
          if (other !== menu) {{
            other.hidden = true;
            var otherToggle = other.parentElement.querySelector("button");
            if (otherToggle) otherToggle.setAttribute("aria-expanded", "false");
          }}
        }});
        menu.hidden = !open;
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      }});

      menu.querySelectorAll(".toc-item").forEach(function (link) {{
        link.addEventListener("click", closeMenu);
      }});

      return closeMenu;
    }}

    var closeDockToc = wireToc(dock);
    wireToc(mainHeader);

    document.addEventListener("click", function () {{
      document.querySelectorAll(".toc-menu").forEach(function (menu) {{
        menu.hidden = true;
      }});
      document.querySelectorAll(".toc-dropdown button").forEach(function (btn) {{
        btn.setAttribute("aria-expanded", "false");
      }});
    }});

    function setDockOpen(open) {{
      if (!dock || dockOpen === open) return;
      dockOpen = open;
      dock.classList.toggle("is-revealed", open);
      dock.setAttribute("aria-hidden", open ? "false" : "true");
      if (!open && closeDockToc) closeDockToc();
    }}

    function onScroll() {{
      var y = window.scrollY || 0;
      var delta = y - lastY;

      if (y <= atTopThreshold || atPageBottom()) {{
        setDockOpen(false);
        if (y <= atTopThreshold) suppressDockUntilTop = false;
      }} else if (suppressDockUntilTop) {{
        setDockOpen(false);
        if (delta > scrollDelta) {{
          suppressDockUntilTop = false;
        }}
      }} else if (delta < -scrollDelta) {{
        setDockOpen(true);
      }} else if (delta > scrollDelta) {{
        setDockOpen(false);
      }}

      if (backToTop) {{
        backToTop.classList.toggle("is-visible", y > backToTopThreshold);
      }}

      lastY = y;
    }}

    if (backToTop) {{
      backToTop.addEventListener("click", function () {{
        suppressDockUntilTop = true;
        setDockOpen(false);
        window.scrollTo({{ top: 0, behavior: "smooth" }});
      }});
    }}

    window.addEventListener("scroll", onScroll, {{ passive: true }});
    setDockOpen(false);
    onScroll();
  }})();
  </script>
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
