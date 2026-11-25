#!/usr/bin/env python3
"""QA: verify every internal link, image, stylesheet and script resolves,
check heading order, unique titles, and scan for leftover editor references."""
import html.parser
import pathlib
import re
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8901"
ROOT = pathlib.Path(__file__).parent.parent / "website"

pages = sorted(ROOT.rglob("*.html"))
errors = []
checked_urls = {}


def fetch(url):
    if url in checked_urls:
        return checked_urls[url]
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            checked_urls[url] = r.status
    except Exception as e:
        checked_urls[url] = str(e)
    return checked_urls[url]


class PageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.headings = []
        self.title = ""
        self.in_title = False
        self.imgs_without_alt = 0
        self.ids = set()
        self.dup_ids = []
        self.use_refs = []
        self.inline_event_handlers = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                self.dup_ids.append(a["id"])
            self.ids.add(a["id"])
        for k, v in attrs:
            if k.startswith("on"):
                self.inline_event_handlers.append(k)
        if tag == "a" and a.get("href"):
            self.refs.append(("href", a["href"]))
        if tag == "img":
            if "alt" not in a:
                self.imgs_without_alt += 1
            for k in ("src",):
                if a.get(k):
                    self.refs.append(("img", a[k]))
            if a.get("srcset"):
                for part in a["srcset"].split(","):
                    u = part.strip().split(" ")[0]
                    if u:
                        self.refs.append(("srcset", u))
        if tag == "link" and a.get("href"):
            self.refs.append(("link", a["href"]))
        if tag == "script" and a.get("src"):
            self.refs.append(("script", a["src"]))
        if tag == "use" and a.get("href"):
            self.use_refs.append(a["href"])
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))
        if tag == "title":
            self.in_title = True

    def handle_data(self, data):
        if self.in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False


titles = {}
for f in pages:
    rel = f.relative_to(ROOT).as_posix()
    url_path = "/" + rel
    p = PageParser()
    src = f.read_text(encoding="utf-8")
    p.feed(src)

    # leftover editor / third-party references
    for pat in ("website-editor.net", "multiscreensite", "ionos", "duda",
                "googleapis", "gstatic", "fontawesome", "cdn."):
        for m in re.finditer(pat, src, re.I):
            line = src[:m.start()].count("\n") + 1
            errors.append(f"{rel}:{line}: leftover reference '{pat}'")

    if p.title in titles:
        errors.append(f"{rel}: duplicate title with {titles[p.title]}")
    titles[p.title] = rel
    if not p.title:
        errors.append(f"{rel}: missing title")
    if p.imgs_without_alt:
        errors.append(f"{rel}: {p.imgs_without_alt} img without alt")
    if p.dup_ids:
        errors.append(f"{rel}: duplicate ids {p.dup_ids}")
    if p.inline_event_handlers:
        errors.append(f"{rel}: inline handlers {p.inline_event_handlers}")
    if p.headings and p.headings[0] != 1:
        errors.append(f"{rel}: first heading is h{p.headings[0]}")
    if p.headings.count(1) != 1:
        errors.append(f"{rel}: {p.headings.count(1)} h1 elements")
    prev = 0
    for h in p.headings:
        if prev and h > prev + 1:
            errors.append(f"{rel}: heading jump h{prev} -> h{h}")
        prev = h

    # symbol use references
    for u in p.use_refs:
        if u.startswith("#") and u[1:] not in p.ids:
            errors.append(f"{rel}: <use> references missing symbol {u}")

    # resolve refs
    for kind, ref in p.refs:
        if ref.startswith(("mailto:", "tel:", "#", "data:")):
            if ref.startswith("#") and ref[1:] and ref[1:] not in p.ids:
                errors.append(f"{rel}: anchor {ref} has no target")
            continue
        parsed = urllib.parse.urlparse(ref)
        if parsed.scheme in ("http", "https"):
            allowed_external = {
                "www.ls-eau.fr", "ls-eau.fr", "127.0.0.1:8901",
                # Permitted third-party dependency: the OpenStreetMap embed.
                "www.openstreetmap.org",
            }
            if parsed.netloc not in allowed_external:
                errors.append(f"{rel}: external reference {ref}")
            continue
        target = urllib.parse.urljoin(BASE + url_path, ref)
        status = fetch(target)
        if status != 200:
            errors.append(f"{rel}: broken {kind} -> {ref} ({status})")

print(f"Checked {len(pages)} pages, {len(checked_urls)} unique asset URLs")
if errors:
    print(f"\n{len(errors)} ISSUES:")
    for e in errors:
        print(" -", e)
else:
    print("ALL CHECKS PASSED")