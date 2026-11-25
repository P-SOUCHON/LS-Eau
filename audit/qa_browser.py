#!/usr/bin/env python3
"""Browser QA (Firefox headless, WebDriver BiDi) for the refined LS'Eau site.

Per page/viewport: horizontal overflow, image loading, single h1, nav, fonts.
Interactions: mobile nav, header transformation, reveals, gallery filters,
lightbox keyboard controls, breadcrumbs. Reduced-motion pass. Screenshots.
"""
import io
import pathlib
import sys
import time
import urllib.parse

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait

BASE = "http://127.0.0.1:8901"
OUT = pathlib.Path(__file__).parent / "screenshots"
OUT.mkdir(exist_ok=True)

PAGES = [
    "/", "/assainissement/", "/eaux-pluviales/", "/eaux-souterraines/",
    "/hydrometrie/", "/amo/", "/dossiers-reglementaires/", "/galerie/",
    "/nous-contacter/", "/mentions-legales/", "/404.html",
]
VIEWPORTS = [(1440, 900, "desktop"), (1024, 800, "laptop"),
             (820, 1180, "tablet"), (390, 844, "mobile"), (360, 780, "small")]

opts = Options()
opts.add_argument("-headless")
opts.enable_bidi = True
service = Service(executable_path="/tmp/opencode/geckodriver")
driver = webdriver.Firefox(options=opts, service=service)

console_errors = []
try:
    driver.script.add_console_message_handler(
        lambda m: console_errors.append(f"{m.type}: {m.text}")
        if m.type == "error" else None
    )
except Exception as e:
    print("console capture unavailable:", e)

issues = []

# Headless Firefox clamps its window to a 500 px minimum width, which would
# silently turn 390/360 checks into 500 px checks. Narrow viewports are therefore
# rendered inside a fixed-width iframe: media queries and innerWidth then match
# the requested width exactly. Widths >= 500 use the real browser viewport.
MIN_WINDOW = 500


def load_viewport(url, w, h):
    if w < MIN_WINDOW:
        driver.set_window_size(MIN_WINDOW, h)
        html = (
            '<!doctype html><html><head><meta charset="utf-8">'
            "<style>html,body{margin:0;background:#fff}iframe{border:0;display:block}</style>"
            "</head><body>"
            f'<iframe id="vp" src="{BASE + url}" width="{w}" height="{h}"></iframe>'
            "</body></html>"
        )
        driver.get("data:text/html;charset=utf-8," + urllib.parse.quote(html))
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(0.4)
        driver.switch_to.frame(driver.find_element(By.ID, "vp"))
    else:
        driver.set_window_size(w, h)
        driver.get(BASE + url)
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script("return document.readyState") == "complete")
    time.sleep(0.3)


def leave_frame():
    driver.switch_to.default_content()


def check_page(url, w, h, label):
    load_viewport(url, w, h)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(0.3)
    m = driver.execute_script("""
      return {
        scrollW: document.documentElement.scrollWidth,
        innerW: window.innerWidth,
        imgs: Array.from(document.images).map(i => ({src: i.currentSrc || i.src, ok: i.complete && i.naturalWidth > 0})),
        h1: document.querySelectorAll('h1').length,
        navLinks: document.querySelectorAll('.main-nav a').length,
        fontsBody: document.fonts.check('16px Manrope'),
        fontsDisplay: document.fonts.check('16px "Source Serif 4"'),
        breadcrumb: document.querySelectorAll('.breadcrumb').length,
        footerCredit: document.body.innerText.indexOf('Conception et développement : Pierre Souchon') !== -1,
        map: (function () {
          var f = document.querySelector('.contact-map iframe');
          if (!f) return null;
          var r = document.querySelector('.contact-map__frame').getBoundingClientRect();
          return {title: f.getAttribute('title') || '', loading: f.getAttribute('loading'), w: r.width, h: r.height};
        })(),
        amoP: (function () {
          var p = document.querySelector('.study-grid--steps .study-card__body p');
          if (!p) return null;
          return {w: p.getBoundingClientRect().width, text: p.textContent.length};
        })(),
        photo: (function () {
          var img = document.querySelector('.photo-band img');
          if (!img) return null;
          var r = img.getBoundingClientRect();
          return {w: r.width, h: r.height, natural: img.naturalWidth / img.naturalHeight};
        })(),
        notfound: document.querySelector('.notfound') ? {
          home: !!document.querySelector('.notfound a[href="/"]'),
          services: document.querySelectorAll('.notfound__services a').length
        } : null
      };
    """)
    if m["scrollW"] > m["innerW"]:
        issues.append(f"{url} [{label}]: overflow {m['scrollW']} > {m['innerW']}")
    if abs(m["innerW"] - w) > 1:
        issues.append(f"{url} [{label}]: viewport width {m['innerW']} != requested {w}")
    if m["h1"] != 1:
        issues.append(f"{url} [{label}]: {m['h1']} h1")
    if m["navLinks"] != 9:
        issues.append(f"{url} [{label}]: nav {m['navLinks']}")
    if not m["fontsBody"] or not m["fontsDisplay"]:
        issues.append(f"{url} [{label}]: fonts not loaded (body={m['fontsBody']}, display={m['fontsDisplay']})")
    if url != "/" and url != "/mentions-legales/" and url != "/404.html" and m["breadcrumb"] != 1:
        issues.append(f"{url} [{label}]: breadcrumb missing")
    if not m["footerCredit"]:
        issues.append(f"{url} [{label}]: footer credit missing")
    if url == "/nous-contacter/":
        if not m["map"]:
            issues.append(f"{url} [{label}]: map iframe missing")
        else:
            if not m["map"]["title"]:
                issues.append(f"{url} [{label}]: map iframe has no title")
            if m["map"]["loading"] != "lazy":
                issues.append(f"{url} [{label}]: map iframe not lazy")
            if m["map"]["w"] < 200 or m["map"]["h"] < 150:
                issues.append(f"{url} [{label}]: map frame too small {m['map']}")
    if url == "/amo/":
        p = m["amoP"]
        if not p:
            issues.append(f"{url} [{label}]: AMO body missing")
        elif p["w"] < 220:
            issues.append(f"{url} [{label}]: AMO paragraph too narrow ({p['w']:.0f}px)")
    if url == "/eaux-pluviales/":
        p = m["photo"]
        if not p:
            issues.append(f"{url} [{label}]: photo band missing")
        else:
            if p["w"] > 800 and p["h"] > 420:
                issues.append(f"{url} [{label}]: photo band too tall ({p['h']:.0f}px)")
            if abs((p["w"] / p["h"]) - p["natural"]) > 0.05:
                issues.append(f"{url} [{label}]: photo band aspect distorted ({p['w'] / p['h']:.2f} vs {p['natural']:.2f})")
    if url == "/404.html":
        nf = m["notfound"]
        if not nf or not nf["home"] or nf["services"] < 6:
            issues.append(f"{url} [{label}]: 404 links incomplete {nf}")
    for im in m["imgs"]:
        if not im["ok"] and not im["src"].startswith("data:"):
            issues.append(f"{url} [{label}]: image not loaded {im['src']}")
    leave_frame()


print("== Page checks (5 viewports x 11 pages)")
for url in PAGES:
    for w, h, label in VIEWPORTS:
        check_page(url, w, h, label)
    print(f"  checked {url}")

print("== Header transformation + reveals (home)")
driver.set_window_size(1440, 900)
driver.get(BASE + "/")
time.sleep(0.4)
hdr = driver.find_element(By.CSS_SELECTOR, ".site-header")
assert "site-header--overlay" in hdr.get_attribute("class")
assert "is-scrolled" not in hdr.get_attribute("class"), "header should start transparent"
driver.execute_script("window.scrollTo(0, 600)")
time.sleep(0.5)
assert "is-scrolled" in driver.find_element(By.CSS_SELECTOR, ".site-header").get_attribute("class")
# reveal: an element in view should have become visible
driver.execute_script("document.getElementById('prestations').scrollIntoView()")
time.sleep(0.9)
revealed = driver.execute_script(
    "return Array.from(document.querySelectorAll('#prestations [data-reveal]')).some(e => e.classList.contains('is-in'))")
assert revealed, "no reveal triggered in services section"
print("  header + reveals OK")

print("== Mobile navigation (true 360 px viewport)")
load_viewport("/", 360, 780)
toggle = driver.find_element(By.CSS_SELECTOR, ".nav-toggle")
nav = driver.find_element(By.ID, "main-nav")
assert toggle.is_displayed() and not nav.is_displayed()
toggle.click()
assert nav.is_displayed() and toggle.get_attribute("aria-expanded") == "true"
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
assert not nav.is_displayed()
leave_frame()
# Follow a menu link at 820 px (the toggle is active up to 1120 px).
driver.set_window_size(820, 1180)
driver.get(BASE + "/")
driver.find_element(By.CSS_SELECTOR, ".nav-toggle").click()
driver.find_element(By.CSS_SELECTOR, '#main-nav a[href="assainissement/"]').click()
WebDriverWait(driver, 10).until(lambda d: "/assainissement/" in d.current_url)
assert not driver.find_element(By.ID, "main-nav").is_displayed()
print("  mobile nav OK")

print("== Gallery filters + lightbox + breadcrumbs")
driver.set_window_size(1440, 900)
driver.get(BASE + "/galerie/")
assert driver.find_element(By.CSS_SELECTOR, ".breadcrumb").is_displayed()
driver.find_element(By.CSS_SELECTOR, '[data-filter="forage"]').click()
vis = driver.execute_script("return Array.from(document.querySelectorAll('.gallery-grid > li')).filter(li=>!li.hidden).length")
assert vis == 7, vis
driver.find_element(By.CSS_SELECTOR, '[data-filter="all"]').click()
vis = driver.execute_script("return Array.from(document.querySelectorAll('.gallery-grid > li')).filter(li=>!li.hidden).length")
assert vis == 14, vis
driver.find_element(By.CSS_SELECTOR, ".gallery-grid a[data-lightbox]").click()
dialog = driver.find_element(By.ID, "lightbox")
assert dialog.get_attribute("open") is not None
assert driver.find_element(By.CSS_SELECTOR, ".lightbox__count").text == "1 / 14"
driver.find_element(By.CSS_SELECTOR, ".lightbox__nav--next").click()
assert driver.find_element(By.CSS_SELECTOR, ".lightbox__count").text == "2 / 14"
driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.ARROW_RIGHT)
assert driver.find_element(By.CSS_SELECTOR, ".lightbox__count").text == "3 / 14"
driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.ESCAPE)
assert dialog.get_attribute("open") is None
print("  gallery + lightbox + breadcrumb OK")

print("== Reduced motion pass")
rm_opts = Options()
rm_opts.add_argument("-headless")
rm_opts.set_preference("ui.prefersReducedMotion", 1)
rm_driver = webdriver.Firefox(options=rm_opts, service=Service(executable_path="/tmp/opencode/geckodriver"))
rm_driver.set_window_size(1440, 900)
rm_driver.get(BASE + "/")
time.sleep(0.5)
rm = rm_driver.execute_script("""
  var hero = document.querySelector('.hero [data-entrance]');
  var reveal = document.querySelector('[data-reveal]');
  return {
    heroOpacity: getComputedStyle(hero).opacity,
    revealOpacity: reveal ? getComputedStyle(reveal).opacity : '1',
    reduced: matchMedia('(prefers-reduced-motion: reduce)').matches
  };
""")
assert rm["reduced"], "reduced motion not emulated"
assert rm["heroOpacity"] == "1", f"hero hidden under reduced motion: {rm['heroOpacity']}"
assert rm["revealOpacity"] == "1", f"reveal hidden under reduced motion: {rm['revealOpacity']}"
rm_driver.quit()
print("  reduced motion OK (content visible, animations disabled)")

print("== Screenshots")
shots = [
    ("/", 1440, 900, "home-hero-desktop"),
    ("/", 1440, 3600, "home-full-desktop"),
    ("/", 390, 844, "home-mobile"),
    ("/", 820, 3000, "home-tablet"),
    ("/assainissement/", 1440, 2900, "assainissement-desktop"),
    ("/eaux-souterraines/", 1440, 3200, "eaux-souterraines-desktop"),
    ("/hydrometrie/", 1440, 2800, "hydrometrie-desktop"),
    ("/dossiers-reglementaires/", 1440, 2600, "dossiers-desktop"),
    ("/galerie/", 1440, 2400, "galerie-desktop"),
    ("/nous-contacter/", 1440, 1800, "contact-desktop"),
    ("/nous-contacter/", 390, 2200, "contact-mobile"),
    ("/eaux-pluviales/", 1440, 2400, "eaux-pluviales-desktop"),
    ("/eaux-pluviales/", 360, 1400, "eaux-pluviales-small"),
    ("/amo/", 1440, 2200, "amo-desktop"),
    ("/amo/", 360, 2300, "amo-small"),
    ("/404.html", 1440, 1200, "404-desktop"),
    ("/404.html", 390, 844, "404-mobile"),
]
for url, w, h, name in shots:
    if w < MIN_WINDOW:
        load_viewport(url, w, h)
        driver.execute_script(
            "document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
        driver.execute_script(
            "document.querySelectorAll('[data-reveal]').forEach(e=>e.classList.add('is-in'))")
        time.sleep(0.9)
        leave_frame()
        png = driver.get_screenshot_as_png()
        im = Image.open(io.BytesIO(png)).crop((0, 0, w, h))
        im.save(str(OUT / f"{name}.png"))
    else:
        driver.set_window_size(w, h)
        driver.get(BASE + url)
        time.sleep(0.5)
        driver.execute_script(
            "document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
        # force reveals visible for a complete static capture
        driver.execute_script(
            "document.querySelectorAll('[data-reveal]').forEach(e=>e.classList.add('is-in'))")
        time.sleep(1.0)
        driver.save_screenshot(str(OUT / f"{name}.png"))
    print(f"  {name}.png")

driver.quit()
real = [e for e in console_errors if "favicon" not in e.lower()]
if real:
    issues.append("console errors: " + " | ".join(real[:10]))
print()
if issues:
    print(f"{len(issues)} ISSUES:")
    for i in issues:
        print(" -", i)
    sys.exit(1)
print("ALL BROWSER CHECKS PASSED")