#!/usr/bin/env python3
"""Builds the website into docs/, which GitHub Pages serves.

Every file in src/pages/ is a page fragment that starts with a metadata comment:

    <!--
    title: Help
    description: One sentence for search results and link previews.
    path: help/
    nav: help
    -->

and is wrapped in src/layout.html. In both, these placeholders are replaced:

    {{root}}       relative path back to the site root ("" or "../"), so links work under any base path
    {{repo}}       the public GitHub repository
    {{issues}}     its "new issue" URL (append ?template=… for a form)
    {{store}}      the App Store label: "Coming soon" until APP_STORE_URL is set
    {{icon:name}}  an inline SVG icon from ICONS
    {{css_version}} a hash of site.css, so a changed stylesheet is never served from cache

Standard library only. Run:  python3 build.py
"""

import datetime
import hashlib
import re
import shutil
from pathlib import Path

BASE_URL = "https://brunobotelhobr.github.io/tcg-game-planner/"
REPO = "https://github.com/brunobotelhobr/tcg-game-planner"

# Release day: set both, rebuild. Until then every store link reads "Coming soon to the App Store".
APP_STORE_URL = ""  # e.g. "https://apps.apple.com/app/id1234567890"
APP_STORE_ID = ""   # e.g. "1234567890", for the Smart App Banner

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "docs"

NAV = [
    ("Features", "features", "#features"),
    ("Help", "help", "help/"),
    ("FAQ", "faq", "faq/"),
    ("Backlog", "backlog", "backlog/"),
    ("Support", "support", "support/"),
]


def svg(body: str) -> str:
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>')


ICONS = {
    "layers": svg('<path d="M12 3 3 8l9 5 9-5-9-5z"/><path d="m3 13 9 5 9-5"/>'),
    "grid": svg('<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>'),
    "trend": svg('<path d="m3 17 6-6 4 4 8-8"/><path d="M15 7h6v6"/>'),
    "box": svg('<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="m3 7.5 9 4.5 9-4.5M12 12v9"/>'),
    "trophy": svg('<path d="M8 21h8M12 17v4"/><path d="M7 4h10v5a5 5 0 0 1-10 0z"/>'
                  '<path d="M17 5h3v2a3 3 0 0 1-3 3M7 5H4v2a3 3 0 0 0 3 3"/>'),
    "chart": svg('<path d="M4 20V11M10 20V4M16 20v-7M2 20h20"/>'),
    "heart": svg('<path d="M12 20s-7-4.4-9-9a4.8 4.8 0 0 1 9-3 4.8 4.8 0 0 1 9 3c-2 4.6-9 9-9 9z"/>'),
    "shield": svg('<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>'),
    "refresh": svg('<path d="M20 12a8 8 0 1 1-2.3-5.7L20 8.6"/><path d="M20 3.5v5.1h-5.1"/>'),
    "search": svg('<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>'),
    "phone": svg('<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>'),
    "monitor": svg('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>'),
    "bug": svg('<rect x="7" y="8" width="10" height="12" rx="5"/><path d="M12 8V5M9.5 4 11 6M14.5 4 13 6'
               'M3 13h4M17 13h4M4 19l3-2M20 19l-3-2M4 7l3 2M20 7l-3 2"/>'),
    "bulb": svg('<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>'),
    "question": svg('<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6"/><path d="M12 17h.01"/>'),
    "database": svg('<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/>'
                    '<path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>'),
    "arrow": svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "cloud": svg('<path d="M7 18a5 5 0 0 1-.6-10A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9z"/>'),
    "sparkles": svg('<path d="m12 3 1.8 4.7 4.7 1.8-4.7 1.8L12 16l-1.8-4.7-4.7-1.8 4.7-1.8z"/>'
                    '<path d="m19 15 .8 2.2 2.2.8-2.2.8L19 21l-.8-2.2-2.2-.8 2.2-.8z"/>'),
    "file": svg('<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/>'
                '<path d="M12 18v-6M9 15l3 3 3-3"/>'),
    "lock": svg('<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'),
}


def store_label(root: str) -> str:
    if APP_STORE_URL:
        return (f'<a class="store" href="{APP_STORE_URL}">{ICONS["phone"]}'
                '<span><span class="top">Download on the</span><span class="bottom">App Store</span></span></a>')
    return (f'<span class="store" role="note">{ICONS["phone"]}'
            '<span><span class="top">Coming soon to the</span><span class="bottom">App Store</span></span></span>')


def parse(fragment: str):
    match = re.match(r"\s*<!--(.*?)-->", fragment, re.S)
    if not match:
        raise SystemExit("A page fragment must start with a metadata comment")
    meta = {}
    for line in match.group(1).strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, fragment[match.end():].strip()


def fill(text: str, values: dict) -> str:
    text = re.sub(r"\{\{icon:([a-z-]+)\}\}", lambda m: ICONS[m.group(1)], text)
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    leftover = re.search(r"\{\{[^}]+\}\}", text)
    if leftover:
        raise SystemExit(f"Unknown placeholder {leftover.group(0)}")
    return text


def main():
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "assets", OUT / "assets")

    # A new stylesheet gets a new URL, so browsers never pair fresh pages with a cached old one.
    css_version = hashlib.sha256((SRC / "assets" / "site.css").read_bytes()).hexdigest()[:10]
    urls = []
    for page in sorted((SRC / "pages").glob("*.html")):
        meta, body = parse(page.read_text(encoding="utf-8"))
        path = meta["path"]
        if path == "404":
            target, depth, canonical = OUT / "404.html", 0, BASE_URL
        else:
            target = OUT / path / "index.html"
            depth = path.count("/")
            canonical = BASE_URL + path
            urls.append(canonical)
        root = "../" * depth
        nav = "".join(
            f'<a href="{root}{href}"' + (' aria-current="page"' if meta.get("nav") == key else "") + f">{label}</a>"
            for label, key, href in NAV
        )
        title = meta["title"] if meta["title"].endswith("TCG Game Planner") else f'{meta["title"]} · TCG Game Planner'
        banner = (f'<meta name="apple-itunes-app" content="app-id={APP_STORE_ID}">\n' if APP_STORE_ID else "")
        values = {
            "root": root, "repo": REPO, "issues": f"{REPO}/issues/new", "store": store_label(root),
            "base_url": BASE_URL, "year": str(datetime.date.today().year), "css_version": css_version,
        }
        content = fill(body, values)
        html = fill(layout, {**values, "title": title, "description": meta["description"], "canonical": canonical,
                             "nav": nav, "content": content, "smart_banner": banner})
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n", encoding="utf-8")
    entries = "".join(f"  <url><loc>{url}</loc></url>\n" for url in sorted(urls))
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n', encoding="utf-8")
    print(f"Built {len(urls) + 1} pages into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
