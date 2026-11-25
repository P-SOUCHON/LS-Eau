#!/usr/bin/env python3
"""Download site assets for the audit.

Owner images live under the site-specific CDN path (ccd24da...). We try the
unsigned original first, then fall back to the largest signed variant found
in the raw HTML. Stock-library images (md/and1, md/dmtmpl) are downloaded for
inspection only, into a separate folder.
"""
import pathlib
import re
import subprocess
import urllib.parse

BASE = pathlib.Path(__file__).parent
RAW = BASE / "raw"
OWN = BASE / "images" / "owner"
STOCK = BASE / "images" / "stock-inspection"
OWN.mkdir(parents=True, exist_ok=True)
STOCK.mkdir(parents=True, exist_ok=True)

SITE = "ccd24da11b95483eb449a37841e09405"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"

owner_names = [
    "LOGO+REDUIT+LS-Eau.png",
    "LOGO+ICONE+57.png",
    "ANC001.jpg", "ANC002.jpg", "ANC003.jpg",
    "Forage001.jpg", "Forage002.jpg", "Forage003.jpg", "Forage004.jpg",
    "IMG_6717.jpg", "IMG_9435.JPG", "DSC05628.jpg", "DSC_0046.JPG",
    "IMG_6784+-+IMG_6792.jpg",
    "IMG_6855+-+IMG_6861_blended_fused.jpg",
    "Instruction.jpg", "100334_IMG_54279_HR.jpg", "33914_large.jpg",
    "p14cgct300_1_1.jpg",
    "assainissement-autonome_1.jpg",
    "3f9ab32fc5c170726b023dadca08dff2336540ea3a624ba54317bed694e66740.jpeg",
    "cc8fe49be53f6e5859dab491b27bbc80ef3ba6aa0cb414f9b0056e88d8b583a9.jpeg",
]

# Collect all signed URLs from raw pages, keyed by decoded base name
signed = {}
for f in RAW.glob("*.html"):
    src = f.read_text(encoding="utf-8", errors="replace")
    for u in re.findall(r'https://le-cdn\.website-editor\.net/s/' + SITE + r'/dms3rep/multi/opt/[^"\'\s<>\\)]+', src):
        fname = urllib.parse.unquote(u.split("/opt/")[1].split("?")[0])
        signed.setdefault(fname, []).append(u)


def fetch(url, dest):
    r = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "60", "-o", str(dest), "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    code = r.stdout.strip()
    ok = code == "200" and dest.exists() and dest.stat().st_size > 1000
    if not ok and dest.exists():
        dest.unlink()
    return ok, code


def best_signed(name):
    """Find largest signed variant for an original file name."""
    stem = name.rsplit(".", 1)[0]
    ext = name.rsplit(".", 1)[1]
    cands = []
    for fname, urls in signed.items():
        m = re.match(re.escape(stem) + r"-(\d+)w\." + re.escape(ext) + r"$", fname, re.I)
        if m:
            cands.append((int(m.group(1)), urls[0]))
    if cands:
        return max(cands)[1]
    return None


results = []
for name in owner_names:
    dest = OWN / urllib.parse.unquote(name).replace("+", " ")
    url = f"https://cdn.website-editor.net/{SITE}/dms3rep/multi/{name}"
    ok, code = fetch(url, dest)
    how = "original"
    if not ok:
        u2 = best_signed(urllib.parse.unquote(name).replace("+", " "))
        if u2:
            ok, code = fetch(u2, dest)
            how = "signed-opt"
    results.append((name, ok, code, how))
    print(f"{'OK ' if ok else 'FAIL'} {name} [{how} {code}]")

stock_ids = ["10360", "10604", "113127", "114575", "116875", "121125",
             "123700", "13218", "15229", "2470", "113536", "116592",
             "125229", "126057", "126242"]
for sid in stock_ids:
    dest = STOCK / f"{sid}.jpeg"
    url = f"https://le-cdn.website-editor.net/md/and1/dms3rep/multi/opt/{sid}-1920w.jpeg"
    ok, code = fetch(url, dest)
    print(f"{'OK ' if ok else 'FAIL'} stock {sid} [{code}]")

for tpl in ["businessman-using-a-computer-talking-on-the-mobile-phone", "meeting-room-with-black-chairs"]:
    dest = STOCK / f"{tpl}.jpg"
    url = f"https://le-cdn.website-editor.net/md/dmtmpl/dms3rep/multi/opt/{tpl}-1920w.jpg"
    ok, code = fetch(url, dest)
    print(f"{'OK ' if ok else 'FAIL'} template {tpl} [{code}]")