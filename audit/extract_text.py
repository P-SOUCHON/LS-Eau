#!/usr/bin/env python3
"""Extract visible text and image/link inventories from the audited raw HTML pages."""
import html.parser
import pathlib
import re
import sys
import urllib.parse


class TextExtractor(html.parser.HTMLParser):
    SKIP = {"script", "style", "noscript", "template", "svg"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.parts = []
        self.images = []
        self.links = []
        self.bg_images = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.SKIP:
            self.skip_depth += 1
        if tag == "img":
            src = a.get("src") or a.get("data-src") or ""
            self.images.append({"src": src, "alt": a.get("alt", ""), "srcset": a.get("srcset", "")})
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        style = a.get("style", "")
        for m in re.finditer(r"url\((['\"]?)(.*?)\1\)", style):
            self.bg_images.append(m.group(2))
        if tag in ("p", "div", "h1", "h2", "h3", "h4", "li", "br", "section", "tr"):
            self.parts.append("\n")
        if tag in ("h1", "h2", "h3", "h4"):
            self.parts.append(f"[{tag.upper()}] ")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth > 0:
            self.skip_depth -= 1
        if tag in ("p", "h1", "h2", "h3", "h4", "li"):
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_depth == 0 and data.strip():
            self.parts.append(data)


raw_dir = pathlib.Path(__file__).parent / "raw"
out_dir = pathlib.Path(__file__).parent / "text"
out_dir.mkdir(exist_ok=True)

all_images = {}
for f in sorted(raw_dir.glob("*.html")):
    p = TextExtractor()
    p.feed(f.read_text(encoding="utf-8", errors="replace"))
    text = "".join(p.parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
    (out_dir / (f.stem + ".txt")).write_text(text, encoding="utf-8")

    # Also find image URLs anywhere in the raw source (editor stores them in JSON)
    src = f.read_text(encoding="utf-8", errors="replace")
    urls = set(re.findall(r'https?://[^"\'\\\s<>]+?\.(?:jpg|jpeg|png|webp|gif|svg)', src, re.I))
    urls.update(u for u in p.bg_images if u.startswith("http"))
    for im in p.images:
        if im["src"].startswith("http"):
            urls.add(im["src"])
    for u in sorted(urls):
        all_images.setdefault(u, []).append(f.stem)
    links = sorted(set(p.links))
    (out_dir / (f.stem + ".links.txt")).write_text("\n".join(links), encoding="utf-8")
    print(f"== {f.stem}: {len(text)} chars text, {len(urls)} image URLs, {len(links)} links")

inv = pathlib.Path(__file__).parent / "image_inventory.txt"
inv.write_text("\n".join(f"{u}\t{','.join(pages)}" for u, pages in sorted(all_images.items())), encoding="utf-8")
print(f"\nTotal unique image URLs: {len(all_images)} -> {inv}")