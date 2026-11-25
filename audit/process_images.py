#!/usr/bin/env python3
"""Generate optimized production image assets (WebP variants) from recovered owner photos."""
import pathlib
import subprocess

BASE = pathlib.Path(__file__).parent
SRC = BASE / "images" / "owner"
DEST = BASE.parent / "website" / "assets" / "images"
DEST.mkdir(parents=True, exist_ok=True)

# source file -> (output stem, [widths])
MAP = {
    "ANC001.jpg": ("soil-survey-field", [640, 1280]),
    "ANC002.jpg": ("sanitation-trench", [480, 729]),
    "ANC003.jpg": ("manual-soil-auger", [640, 1280]),
    "assainissement-autonome_1.jpg": ("infiltration-bed", [640, 1280, 1480]),
    "DSC_0046.JPG": ("pond-dusk", [640, 1280, 1920]),
    "DSC05628.jpg": ("drilling-rig-property", [640, 1280, 1920]),
    "Forage001.jpg": ("drilling-discharge", [480, 729]),
    "Forage002.jpg": ("borehole-flow", [640, 1080]),
    "Forage003.jpg": ("drilling-rig-orchard", [480, 729]),
    "Forage004.jpg": ("piezometric-reel", [640, 1280]),
    "IMG_6717.jpg": ("drilling-mast-casings", [640, 1280, 1920]),
    "IMG_6784 - IMG_6792.jpg": ("drainage-ditch", [640, 1280, 1413]),
    "IMG_6855 - IMG_6861_blended_fused.jpg": ("canal-bridge", [640, 1280, 1920]),
    "IMG_9435.JPG": ("drilling-rig-cypress", [640, 1280, 1920]),
}

for src_name, (stem, widths) in MAP.items():
    src = SRC / src_name
    for w in widths:
        out = DEST / f"{stem}-{w}w.webp"
        subprocess.run(
            ["magick", str(src), "-auto-orient", "-resize", f"{w}x>", "-strip",
             "-quality", "82", "-define", "webp:method=6", str(out)],
            check=True)
        print(f"{out.name}: {out.stat().st_size // 1024} KB")

# Logo: keep PNG transparency, trim transparent border, cap height at 240px for retina headers
subprocess.run(["magick", str(SRC / "LOGO REDUIT LS-Eau.png"), "-auto-orient", "-trim",
                "+repage", "-resize", "x240>", "-strip",
                str(DEST / "ls-eau-logo.png")], check=True)
print("logo:", (DEST / "ls-eau-logo.png").stat().st_size // 1024, "KB")

# Favicon PNG (original icon)
subprocess.run(["magick", str(SRC / "LOGO ICONE 57.png"), "-strip",
                str(DEST / "favicon.png")], check=True)

# Open Graph image 1200x630 from the hero photo with a navy gradient band + title
subprocess.run([
    "magick", str(SRC / "IMG_9435.JPG"), "-auto-orient", "-resize", "1200x630^",
    "-gravity", "center", "-extent", "1200x630",
    "(" , "+clone", "-fill", "rgba(10,32,60,0.55)", "-colorize", "100", ")",
    "-compose", "over", "-composite",
    "-gravity", "southwest", "-fill", "white", "-font", "DejaVu-Sans-Bold",
    "-pointsize", "54", "-annotate", "+60+150", "LS'Eau",
    "-font", "DejaVu-Sans", "-pointsize", "30",
    "-annotate", "+60+95", "Bureau d'études en hydrogéologie et assainissement",
    "-strip", "-quality", "85", str(DEST / "og-image.jpg")], check=True)
print("og-image:", (DEST / "og-image.jpg").stat().st_size // 1024, "KB")