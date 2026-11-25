#!/usr/bin/env python3
"""Author the static LS'Eau pages from shared partials + per-page content.

Dev-time convenience only: the generated files in website/ are plain,
hand-editable HTML. No build step is required to deploy or modify the site.
All customer-facing content is French and preserved from the audited site.

Art direction: editorial / scientific-publication identity. Serif display,
grotesque body, monospace annotations, hairline rules, topographic motifs,
asymmetric compositions, progressive reveals.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent.parent / "website"
DOMAIN = "https://www.ls-eau.fr"

# --------------------------------------------------------------------------
# Shared partials
# --------------------------------------------------------------------------

ICONS = """<svg xmlns="http://www.w3.org/2000/svg" class="svg-defs" aria-hidden="true" focusable="false">
  <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
  <symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></symbol>
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6"/></symbol>
  <symbol id="i-chevron-left" viewBox="0 0 24 24"><path d="M14.5 5.5L8 12l6.5 6.5"/></symbol>
  <symbol id="i-chevron-right" viewBox="0 0 24 24"><path d="M9.5 5.5L16 12l-6.5 6.5"/></symbol>
  <symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 3h4l1.5 5-2.2 1.6a13 13 0 0 0 6.1 6.1L16 13.5l5 1.5v4a2 2 0 0 1-2.2 2A17.5 17.5 0 0 1 3 5.2 2 2 0 0 1 5 3z"/></symbol>
  <symbol id="i-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-7-6.1-7-11a7 7 0 0 1 14 0c0 4.9-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></symbol>
  <symbol id="i-droplet" viewBox="0 0 24 24"><path d="M12 3c3.5 4.2 6 7.4 6 10.2a6 6 0 0 1-12 0C6 10.4 8.5 7.2 12 3z"/></symbol>
  <symbol id="i-rain" viewBox="0 0 24 24"><path d="M7 14a4.5 4.5 0 1 1 .9-8.9A5.5 5.5 0 0 1 18.6 7.3 3.8 3.8 0 0 1 17.5 14H7z"/><path d="M8 17l-1 3M12 17l-1 3M16 17l-1 3"/></symbol>
  <symbol id="i-layers" viewBox="0 0 24 24"><path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 12.5l9 5 9-5"/><path d="M3 17l9 5 9-5"/></symbol>
  <symbol id="i-gauge" viewBox="0 0 24 24"><path d="M4 15a8 8 0 0 1 16 0"/><path d="M12 15l3.5-3.5"/><circle cx="12" cy="15" r="1.2"/><path d="M2.5 15H4M20 15h1.5"/></symbol>
  <symbol id="i-helmet" viewBox="0 0 24 24"><path d="M5 16a7 7 0 0 1 14 0"/><path d="M3 16h18v2.5H3z"/><path d="M12 9v7"/></symbol>
  <symbol id="i-file" viewBox="0 0 24 24"><path d="M6 2h8l5 5v15H6z"/><path d="M14 2v5h5"/><path d="M9 12h6M9 16h6"/></symbol>
  <symbol id="i-chat" viewBox="0 0 24 24"><path d="M4 4h16v12H10l-6 5V4z"/></symbol>
  <symbol id="i-target" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.8 2.8 5.7-6"/></symbol>
  <symbol id="i-book" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></symbol>
</svg>
"""

NAV_ITEMS = [
    ("", "Accueil"),
    ("assainissement", "Eaux usées"),
    ("eaux-pluviales", "Eaux pluviales"),
    ("eaux-souterraines", "Eaux souterraines"),
    ("hydrometrie", "Hydrométrie"),
    ("amo", "AMO"),
    ("dossiers-reglementaires", "Dossiers réglementaires"),
    ("galerie", "Galerie"),
]


def href(slug, prefix):
    if slug == "":
        return prefix if prefix else "./"
    return prefix + slug + "/"


def header(active, prefix, overlay=False):
    items = []
    for slug, label in NAV_ITEMS:
        cur = ' aria-current="page"' if slug == active else ""
        items.append(f'        <li><a href="{href(slug, prefix)}"{cur}>{label}</a></li>')
    cur = ' aria-current="page"' if active == "nous-contacter" else ""
    items.append(f'        <li class="nav-contact"><a href="{href("nous-contacter", prefix)}"{cur}>Contact</a></li>')
    links = "\n".join(items)
    cls = "site-header site-header--overlay" if overlay else "site-header"
    return f"""<a class="skip-link" href="#main">Aller au contenu</a>
{ICONS}<header class="{cls}">
  <div class="container header-inner">
    <a class="brand" href="{href('', prefix)}">
      <img src="{prefix}assets/images/ls-eau-logo.png" alt="LS'Eau — bureau d'études en hydrogéologie et assainissement" width="203" height="240">
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav">
      <svg class="icon" aria-hidden="true"><use href="#i-menu"/></svg>
      Menu
    </button>
    <nav id="main-nav" class="main-nav" aria-label="Navigation principale">
      <ul>
{links}
      </ul>
    </nav>
  </div>
</header>
"""


def footer(prefix):
    services = "\n".join(
        f'          <li><a href="{href(s, prefix)}">{l}</a></li>' for s, l in NAV_ITEMS[1:7]
    )
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{prefix}assets/images/ls-eau-logo.png" alt="LS'Eau" width="203" height="240" loading="lazy">
        <p>Bureau d'études en hydrogéologie et assainissement. Études et conception d'ouvrages pour l'assainissement, la gestion ou l'exploitation de la ressource en eau.</p>
      </div>
      <nav aria-label="Prestations">
        <h2>Prestations</h2>
        <ul>
{services}
        </ul>
      </nav>
      <nav aria-label="Informations">
        <h2>Informations</h2>
        <ul>
          <li><a href="{href('', prefix)}">Accueil</a></li>
          <li><a href="{href('galerie', prefix)}">Galerie</a></li>
          <li><a href="{href('nous-contacter', prefix)}">Contact</a></li>
          <li><a href="{href('mentions-legales', prefix)}">Mentions légales</a></li>
        </ul>
      </nav>
      <div>
        <h2>Contact</h2>
        <ul class="footer-contact">
          <li>
            <svg class="icon" aria-hidden="true"><use href="#i-pin"/></svg>
            <span>389, route des Courses<br>84300 Cavaillon, France</span>
          </li>
          <li>
            <svg class="icon" aria-hidden="true"><use href="#i-phone"/></svg>
            <a href="tel:+33651802623">06 51 80 26 23</a>
          </li>
          <li>
            <svg class="icon" aria-hidden="true"><use href="#i-mail"/></svg>
            <a href="mailto:contact@ls-eau.fr">contact@ls-eau.fr</a>
          </li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Copyright © LS'Eau — Tous droits réservés.</p>
      <p class="footer-credit">Conception et développement : Pierre Souchon</p>
      <p><a href="{href('mentions-legales', prefix)}">Mentions légales</a></p>
    </div>
  </div>
</footer>
"""


def cta_band(button_label="Appelez-nous"):
    return f"""<section class="section cta-band" aria-labelledby="cta-title">
  <span class="contours contours--paper" aria-hidden="true"></span>
  <div class="container cta-band__inner">
    <div data-reveal>
      <h2 id="cta-title">Nos prestations vous intéressent ? Nous sommes là pour vous aider !</h2>
      <p>Nous voulons en savoir plus sur votre projet pour vous soumettre une offre technico-économique adaptée à vos besoins.</p>
    </div>
    <div class="cta-band__actions" data-reveal style="--rd:.12s">
      <a class="btn btn--light" href="tel:+33651802623">
        <svg class="icon" aria-hidden="true"><use href="#i-phone"/></svg>
        {button_label} : 06 51 80 26 23
      </a>
      <a class="btn btn--ghost-light" href="mailto:contact@ls-eau.fr">
        <svg class="icon" aria-hidden="true"><use href="#i-mail"/></svg>
        contact@ls-eau.fr
      </a>
    </div>
  </div>
</section>
"""


def page_head(title, desc, canonical, prefix, extra="", body_class="", head_prefix=""):
    bc = f' class="{body_class}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
{head_prefix}  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="LS'Eau">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{DOMAIN}/assets/images/og-image.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0e2c4c">
  <link rel="icon" href="{prefix}assets/images/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{prefix}assets/images/favicon.png" type="image/png" sizes="57x57">
  <link rel="apple-touch-icon" href="{prefix}assets/images/favicon.png">
  <link rel="preload" href="{prefix}assets/fonts/manrope-latin-var.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{prefix}assets/fonts/source-serif-4-latin-var.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{prefix}css/style.css">
  <script>document.documentElement.classList.add("js");</script>
  <script src="{prefix}js/main.js" defer></script>
{extra}</head>
<body{bc}>
"""


def breadcrumb(page_label, prefix):
    return f"""  <nav class="breadcrumb" aria-label="Fil d'Ariane">
    <ol>
      <li><a href="{href('', prefix)}">Accueil</a></li>
      <li aria-current="page">{page_label}</li>
    </ol>
  </nav>
"""


def page_top(page_label, prefix, annotation):
    """Breadcrumb row with a contextual annotation aligned to the right."""
    bc = breadcrumb(page_label, prefix).rstrip("\n")
    bc = "\n".join("  " + line if line.strip() else line for line in bc.split("\n"))
    return f"""    <div class="page-head__top">
{bc}
      <p class="page-head__label">{annotation}</p>
    </div>
"""



def figure(stem, width, height, alt, caption, widths, sizes, prefix, cls="", reveal=True):
    srcset = ", ".join(f"{prefix}assets/images/{stem}-{w}w.webp {w}w" for w in widths)
    cap = f"\n    <figcaption>{caption}</figcaption>" if caption else ""
    klass = f' class="{cls}"' if cls else ""
    rv = ' data-reveal' if reveal else ""
    return f"""  <figure{klass}{rv}>
    <img src="{prefix}assets/images/{stem}-{widths[-1]}w.webp" srcset="{srcset}" sizes="{sizes}" width="{width}" height="{height}" alt="{alt}" loading="lazy" decoding="async">{cap}
  </figure>"""


SUFFIX = "LS'Eau, bureau d'études en hydrogéologie et assainissement"
PAGES = {}

# --------------------------------------------------------------------------
# Homepage
# --------------------------------------------------------------------------
home_services = [
    ("i-droplet", "Assainissement non collectif des eaux usées",
     "LS'Eau réalise les études de sols nécessaires à la mise en œuvre de ces ouvrages d'assainissement et vous accompagne jusqu'à l'obtention du visa de conformité délivré par les Services Publics d'Assainissement Non Collectifs (SPANC).",
     "assainissement"),
    ("i-layers", "Forages d'eau",
     "LS'Eau réalise un large panel d'études pour la définition de la faisabilité de forages que ce soit pour l'AEP, l'irrigation ou encore la géothermie sur nappe.",
     "eaux-souterraines"),
    ("i-rain", "Gestion des eaux pluviales",
     "LS'Eau étudie et dimensionne les dispositifs de gestion et d'assainissement des eaux pluviales au regard des règlements d'urbanisme locaux et des prescriptions de la Loi sur l'Eau.",
     "eaux-pluviales"),
    ("i-gauge", "Hydrométrie",
     "LS'Eau réalise une large gamme de prestations d'hydrométrie pour l'évaluation des paramètres qualité et quantité des eaux qu'elles soient usées, souterraines ou superficielles.",
     "hydrometrie"),
    ("i-helmet", "Assistance à Maîtrise d'Ouvrage",
     "Pour plus de sérénité, LS'Eau vous propose de consulter les entreprises à même de réaliser les travaux décrits dans nos études, de vous aider à faire le meilleur choix de prestataires, de piloter les travaux et de s'assurer de leur bonne exécution.",
     "amo"),
    ("i-file", "Dossiers réglementaires",
     "LS'Eau identifie vos besoins et élabore pour vous les dossiers requis au titre des Codes Général des Collectivités Territoriales, de la Santé Publique, de l'Environnement, et du Code Minier.",
     "dossiers-reglementaires"),
]
index_rows = "\n".join(
    f"""      <li data-reveal style="--rd:{i*0.06:.2f}s">
        <a href="{slug}/">
          <span class="service-index__num">{i+1:02d}<svg class="icon" aria-hidden="true"><use href="#{icon}"/></svg></span>
          <div><h3>{title}</h3><p>{text}</p></div>
          <svg class="icon service-index__arrow" aria-hidden="true"><use href="#i-arrow"/></svg>
        </a>
      </li>"""
    for i, (icon, title, text, slug) in enumerate(home_services)
)

mosaic = [
    ("sanitation-trench", 480, "Tranchée d'épandage d'une filière d'assainissement non collectif"),
    ("drilling-rig-orchard", 480, "Atelier de forage d'eau implanté dans un verger"),
    ("canal-bridge", 640, "Canal bordé de maçonnerie avec un pont de pierre"),
    ("drainage-ditch", 640, "Fossé empierré de gestion des eaux pluviales en bordure de voirie"),
]
mosaic_html = "\n".join(
    f'      <li data-reveal style="--rd:{i*0.08:.2f}s"><a href="galerie/"><img src="assets/images/{stem}-{w}w.webp" alt="{alt}" width="640" height="480" loading="lazy" decoding="async"></a></li>'
    for i, (stem, w, alt) in enumerate(mosaic)
)

home_body = f"""{header('', '', overlay=True)}<main id="main">
<section class="hero">
  <div class="hero__media">
    <img src="assets/images/drilling-rig-cypress-1920w.webp"
         srcset="assets/images/drilling-rig-cypress-640w.webp 640w, assets/images/drilling-rig-cypress-1280w.webp 1280w, assets/images/drilling-rig-cypress-1920w.webp 1920w"
         sizes="100vw" width="1920" height="1280"
         alt="Atelier de forage d'eau LS'Eau implanté dans un terrain arboré" fetchpriority="high" decoding="async">
  </div>
  <span class="contours contours--paper" aria-hidden="true"></span>
  <div class="container">
    <div class="hero__content">
      <span class="eyebrow" data-entrance style="--ed:.05s">Bienvenue chez LS'Eau</span>
      <h1 data-entrance style="--ed:.15s">Votre expert en hydrogéologie et environnement</h1>
      <p data-entrance style="--ed:.3s">Études et conception d'ouvrages permettant l'assainissement, la gestion ou l'exploitation de la ressource en eau.</p>
      <div class="hero__actions" data-entrance style="--ed:.45s">
        <a class="btn btn--light" href="#prestations">Découvrir nos prestations</a>
        <a class="btn btn--ghost-light" href="nous-contacter/">Nous contacter</a>
      </div>
    </div>
  </div>
  <span class="hero__scroll" aria-hidden="true">Défiler</span>
</section>

<section class="section" id="prestations" aria-labelledby="prestations-title">
  <div class="container index-layout">
    <div class="index-aside" data-reveal>
      <span class="eyebrow">01 · Prestations</span>
      <h2 id="prestations-title">Nos domaines d'expertise</h2>
      <a class="link-arrow" href="galerie/">Voir le portfolio<svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
    </div>
    <ol class="service-index">
{index_rows}
    </ol>
  </div>
</section>

<section class="section section--alt" aria-labelledby="about-title">
  <div class="container">
    <div class="about-grid">
{figure('soil-survey-field', 1280, 960, "Matériel d'étude de sols installé dans une oliveraie", "Étude de sols sur le terrain, en amont d'un projet d'assainissement.", [640, 1280], '(min-width: 1024px) 45vw, 100vw', '')}
      <div data-reveal>
        <span class="eyebrow">02 · Le bureau d'études</span>
        <h2 id="about-title">Qui sommes-nous ?</h2>
        <p class="lead">Notre bureau d'études met ses compétences en hydrogéologie et en assainissement au service des particuliers, entreprises et collectivités. Notre équipe expérimentée a le savoir-faire nécessaire pour que nos clients soient pleinement satisfaits de notre travail.</p>
        <ul class="values-list">
          <li>
            <svg class="icon" aria-hidden="true"><use href="#i-chat"/></svg>
            <div><h3>Une équipe disponible</h3><p>Nous nous tenons constamment à votre disposition pour répondre à vos questions.</p></div>
          </li>
          <li>
            <svg class="icon" aria-hidden="true"><use href="#i-target"/></svg>
            <div><h3>Des prestations au plus près de vos besoins</h3><p>Nous prêtons la plus grande attention à vos besoins, attentes et contraintes.</p></div>
          </li>
          <li>
            <svg class="icon" aria-hidden="true"><use href="#i-check"/></svg>
            <div><h3>Des solutions rationnelles</h3><p>Nos études de conceptions visent à la mise en œuvre d'ouvrages parfaitement fonctionnels et adaptés à vos projets tant du point de vue technique qu'économique.</p></div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="realisations-title">
  <div class="container">
    <div class="mosaic-head" data-reveal>
      <div>
        <span class="eyebrow">03 · Galerie</span>
        <h2 id="realisations-title">Nos réalisations en images</h2>
      </div>
      <a class="link-arrow" href="galerie/">Voir la galerie<svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
    </div>
    <ul class="mosaic">
{mosaic_html}
    </ul>
  </div>
</section>

{cta_band()}</main>
{footer('')}"""

PAGES["index.html"] = {
    "title": "LS'Eau — Bureau d'études en hydrogéologie et assainissement",
    "desc": "Spécialisé dans l'étude et la conception d'ouvrages permettant l'assainissement, la gestion ou l'exploitation de la ressource en eau. Assainissement des eaux usées ou pluviales / forages pour l'eau potable ou la géothermie / hydrométrie / dossiers réglementaires.",
    "canonical": DOMAIN + "/",
    "body": home_body,
    "body_class": "has-hero",
}

# --------------------------------------------------------------------------
# Service pages
# --------------------------------------------------------------------------

def study_card(title, paragraphs, index, body_wrapper=False):
    ps = "\n".join(f"        <p>{p}</p>" for p in paragraphs)
    if body_wrapper:
        body = f"""      <div class="study-card__body">
        <h3>{title}</h3>
{ps}
      </div>"""
    else:
        body = f"""      <h3>{title}</h3>
{ps}"""
    return f"""    <li class="study-card" data-reveal style="--rd:{index*0.07:.2f}s">
      <span class="study-card__index">{index+1:02d}</span>
{body}
    </li>"""


def service_page(slug, nav_label, h1, lead, expertise_h2, cards, commitment_h2,
                 commitment_ps, media_html, cta_label, desc,
                 head_media=None, photo_band=None, study_variant="",
                 commitment_section="section section--alt", extra_section="",
                 annotation="Prestations"):
    prefix = "../"
    wrap_body = study_variant == "study-grid--steps"
    cards_html = "\n".join(study_card(t, ps, i, body_wrapper=wrap_body) for i, (t, ps) in enumerate(cards))
    grid_cls = f"study-grid {study_variant}".strip()

    head_media_html = ""
    head_inner_open = ""
    head_inner_close = ""
    if head_media:
        head_inner_open = '<div class="page-head__grid"><div>'
        head_inner_close = "</div>" + head_media + "</div>"

    band_html = (
        f"""
<section class="section section--tight-top" aria-label="Photographie de réalisation">
  <div class="container">
{photo_band}
  </div>
</section>""" if photo_band else ""
    )
    commitment_media = f"\n{media_html}" if media_html else ""
    commitment_cls = "commitment" if media_html else "commitment commitment--text"

    body = f"""{header(slug, prefix)}<main id="main">
<div class="page-head">
  <span class="contours contours--ink" aria-hidden="true"></span>
  <div class="container">
{page_top(nav_label, prefix, annotation)}    {head_inner_open}<h1>{h1}</h1>
    <p class="lead">{lead}</p>{head_inner_close}
  </div>
</div>
{band_html}
<section class="section" aria-labelledby="expertise-title">
  <div class="container">
    <div class="expertise-intro" data-reveal>
      <h2 id="expertise-title">{expertise_h2}</h2>
    </div>
    <ul class="{grid_cls}">
{cards_html}
    </ul>
  </div>
</section>
{extra_section}
<section class="{commitment_section}" aria-labelledby="engagement-title">
  <span class="contours contours--paper" aria-hidden="true"></span>
  <div class="container">
    <div class="{commitment_cls}">
      <div data-reveal>
        <h2 id="engagement-title">{commitment_h2}</h2>
{chr(10).join(f'        <p>{p}</p>' for p in commitment_ps)}
      </div>{commitment_media}
    </div>
  </div>
</section>

{cta_band(cta_label)}</main>
{footer(prefix)}"""
    return {
        "title": f"{h1} — {SUFFIX}",
        "desc": desc,
        "canonical": f"{DOMAIN}/{slug}/",
        "body": body,
    }


# --- Eaux usées : installation photography, asymmetric figures ------------
PAGES["assainissement/index.html"] = service_page(
    "assainissement", "Eaux usées", "Eaux usées",
    "Nous réalisons les études d'assainissement non collectif des eaux usées et nous vous accompagnons jusqu'au terme de votre projet.",
    "Notre expertise en assainissement des eaux usées",
    [
        ("Études de sols", ["Pour l'identification des horizons pédologiques en présence avec définition de leur agencement et de leur perméabilité et description de la nappe phréatique qui pourrait se tenir dans ces formations."]),
        ("Études hydrogéologiques", ["Pour l'évaluation du risque sanitaire induit par la proximité entre la zone disponible pour l'implantation de la filière d'assainissement et le/les captage(s) d'eau potable proche(s)."]),
        ("Études de conception", ["Pour la définition des caractéristiques techniques de la (des) filière(s) d'assainissement adaptée(s) aux bâtiments du projet."]),
    ],
    "Des projets rationnels conformes à la réglementation.",
    [
        "Notre objectif premier est l'élaboration de solutions techniques rationnelles, adaptées à vos projets ainsi qu'à leur environnement, respectant la réglementation et les normes en vigueur.",
        "L'ensemble des prestations proposées par LS'Eau vise à l'édification de dispositifs de traitement des eaux usées conformes, selon le cas, à l'arrêté du 7 septembre 2009 ou à celui du 21 juillet 2015 et conformes à la norme NF DTU 64.1 d'août 2013.",
    ],
    figure("manual-soil-auger", 1280, 960, "Tarière manuelle posée au sol lors d'une étude de sols en verger", "Sondage à la tarière manuelle lors d'une étude de sols.", [640, 1280], "(min-width: 1024px) 45vw, 100vw", "../"),
    "Appelez-nous",
    "LS'Eau Bureau d'études en hydrogéologie et environnement / Études d'assainissement non collectif / Études de sols.",
    head_media=figure("sanitation-trench", 729, 972, "Tranchée d'épandage creusée pour une filière d'assainissement non collectif", "Terrassement d'une filière d'assainissement non collectif.", [480, 729], "(min-width: 1024px) 35vw, 100vw", "../", cls="page-head__media", reveal=False),
    extra_section=f"""
<section class="section section--tight-top" aria-label="Photographie de réalisation">
  <div class="container">
{figure('infiltration-bed', 1480, 366, "Filière d'infiltration des eaux usées en cours de construction, lit de gravier", "Filière d'infiltration en cours de réalisation.", [640, 1280, 1480], '100vw', '../', cls='figure-wide')}
  </div>
</section>
""",
    annotation="Assainissement",
)

# --- Eaux pluviales : full-bleed water-flow band ----------------------------
PAGES["eaux-pluviales/index.html"] = service_page(
    "eaux-pluviales", "Eaux pluviales", "Eaux pluviales",
    "Nous réalisons des études de conception de dispositifs de gestion et d'assainissement des eaux pluviales adaptés à vos projets et conformes à la réglementation.",
    "Notre expertise en gestion des eaux pluviales",
    [
        ("Études hydrauliques", ["Pour la définition des volumes et débits d'eaux pluviales à prendre en compte dans le dimensionnement des filières de gestion et d'assainissement des eaux de ruissellement."]),
        ("Études de sols", ["Pour la définition des contraintes pédologiques et hydrogéologiques pouvant avoir un impact sur la conception des dispositifs de gestion et d'assainissement des eaux pluviales."]),
        ("Études de conception", ["Pour la définition des caractéristiques techniques des filières de gestion et d'assainissement des eaux de ruissellement adaptées à votre projet."]),
    ],
    "Concertation / Maîtrise technique et réglementaire.",
    [
        "Afin d'élaborer des projets de filières de gestion et d'assainissement des eaux pluviales rationnelles, nous consacrons toute l'énergie nécessaire pour parfaire notre connaissance de vos projets et des contraintes techniques et réglementaires attenantes.",
        "Pleinement conscient de la complexité à concevoir des projets immobiliers sur lesquels doivent se greffer des dispositifs de gestion des eaux pluviales, nous usons de notre capacité à la concertation pour proposer des solutions techniques réglementaires et rationnelles aisément intégrables.",
    ],
    "",
    "Appelez-nous",
    "LS'Eau Bureau d'études en hydrogéologie et environnement / études de conception de dispositifs de gestion et d'assainissement des eaux pluviales",
    photo_band=f"""<figure class="photo-band" data-reveal>
  <img src="../assets/images/drainage-ditch-1413w.webp" srcset="../assets/images/drainage-ditch-640w.webp 640w, ../assets/images/drainage-ditch-1280w.webp 1280w, ../assets/images/drainage-ditch-1413w.webp 1413w" sizes="(min-width: 960px) 960px, 100vw" width="1413" height="576" alt="Fossé empierré longeant une route, destiné à la gestion des eaux pluviales" loading="lazy" decoding="async">
  <figcaption>Fossé empierré de gestion des eaux pluviales en bordure de voirie.</figcaption>
</figure>""",
    annotation="Gestion pluviale",
)

# --- Eaux souterraines : depth / dark section -------------------------------
PAGES["eaux-souterraines/index.html"] = service_page(
    "eaux-souterraines", "Eaux souterraines", "Eaux souterraines",
    "Nous élaborons des études de faisabilité et des études de conception visant la création d'ouvrages permettant l'exploitation de la ressource en eaux souterraines.",
    "Notre expertise en hydrogéologie",
    [
        ("Études de faisabilité administrative", ["Pour la définition du contexte réglementaire dans lequel s'inscrit votre projet de captage d'eaux souterraines et pour s'assurer de sa faisabilité administrative."]),
        ("Études de faisabilité hydrogéologique", ["Pour l'identification et la caractérisation des ressources en eaux souterraines en présence mais également pour l'estimation des chances de succès d'un forage d'eau sur votre propriété."]),
        ("Études de conception", ["Pour la définition des caractéristiques techniques de projets de forages ainsi que l'estimation des coûts de travaux."]),
        ("Études diagnostic", ["Pour la définition des caractéristiques techniques de captages existants ou pour l'identification de l'origine de baisse de productivité de ce type d'ouvrages."]),
    ],
    "Des études de haute technicité pour des projets rationnels.",
    [
        "Notre but premier est de vous fournir un conseil objectif et d'élaborer des projets rationnels, adaptés à vos projets et leur environnement en respectant la réglementation et les normes en vigueur.",
        "Grâce à notre connaissance approfondie de la géologie régionale et notre parfaite maîtrise des techniques de forage et de la réglementation, nous vous fournissons un conseil des plus éclairés sur la faisabilité de vos projets visant à exploiter les ressources en eaux souterraines.",
    ],
    figure("borehole-flow", 1080, 1920, "Eau s'écoulant en tête d'un forage en cours de réalisation", "Venue d'eau en tête de forage.", [640, 1080], "(min-width: 1024px) 45vw, 100vw", "../"),
    "Prenez rendez-vous",
    "LS'Eau Bureau d'études en hydrogéologie et environnement / Études hydrogéologiques pour la création et la réhabilitation de captages d'eaux souterraines.",
    head_media=figure("drilling-mast-casings", 1920, 2880, "Mât de forage dressé et tubages bleus alignés au sol", "Mât de forage et tubages.", [640, 1280, 1920], "(min-width: 1024px) 35vw, 100vw", "../", cls="page-head__media", reveal=False),
    commitment_section="section section--depth",
    extra_section=f"""
<section class="section section--tight-top" aria-label="Photographies de réalisations">
  <div class="container">
    <div class="figure-row">
{figure('drilling-rig-orchard', 729, 972, 'Atelier de forage d’eau implanté dans un verger', 'Atelier de forage d’eau en verger.', [480, 729], '(min-width: 960px) 45vw, 100vw', '../')}
{figure('drilling-discharge', 729, 972, 'Eaux de forage rejetées par une canalisation bleue', 'Rejet des eaux de forage.', [480, 729], '(min-width: 960px) 45vw, 100vw', '../')}
    </div>
  </div>
</section>
""",
    annotation="Hydrogéologie",
)

# --- Hydrométrie : measurement register -------------------------------------
PAGES["hydrometrie/index.html"] = service_page(
    "hydrometrie", "Hydrométrie", "Hydrométrie",
    "Nous effectuons un large panel de prestations d'hydrométrie pour répondre à vos questions quant à la ressource en eaux souterraines, usées ou pluviales.",
    "Nos compétences en hydrométrie",
    [
        ("Eaux usées", ["LS'Eau réalise une large gamme de prestations d'hydrométrie sur les ouvrages d'assainissement des eaux usées : prélèvements et analyses ponctuelles, bilans de pollution 24 h, campagnes de débitmétrie."]),
        ("Eaux souterraines", ["LS'Eau réalise un large panel de prestations d'hydrométrie sur les eaux souterraines : campagnes de mesures piézométriques, prélèvements et analyses ponctuelles."]),
        ("Eaux superficielles", ["LS'Eau réalise une large gamme de prestations d'hydrométrie sur les eaux superficielles : prélèvements et analyses ponctuelles, campagnes de débitmétrie."]),
    ],
    "La précision dans la mesure et une analyse critique éclairée",
    [
        "Notre objectif premier est de proposer des prestations d'hydrométrie de qualité apportant les éléments indispensables à une analyse pertinente des problématiques concernant l'eau.",
        "Aguerri à l'utilisation d'un large panel de matériels et de techniques d'hydrométrie, nous vous apportons un conseil des plus pertinents pour l'élaboration et la mise en œuvre de programmes de mesures adaptés et nous vous fournissons une analyse critique des résultats de haute technicité.",
    ],
    figure("piezometric-reel", 1280, 960, "Dévidoir de sonde piézométrique bleu installé près d'un captage d'eau souterraine", "Sonde piézométrique en bordure de captage.", [640, 1280], "(min-width: 1024px) 45vw, 100vw", "../"),
    "Prenez rendez-vous",
    "LS'Eau Bureau d'études en hydrogéologie et environnement / Prestations d'hydrométrie sur les eaux usées, les eaux souterraines et les eaux superficielles.",
    study_variant="study-grid--rows",
    annotation="Mesures",
    extra_section=f"""
<section class="section section--tight-top" aria-label="Photographies de réalisations">
  <div class="container">
    <div class="figure-row">
{figure('pond-dusk', 1280, 720, 'Plan d’eau au crépuscule — eaux superficielles', 'Eaux superficielles : plan d’eau.', [640, 1280, 1920], '(min-width: 960px) 45vw, 100vw', '../')}
{figure('canal-bridge', 1280, 827, 'Canal en eau bordé de maçonnerie, avec un pont de pierre', 'Eaux superficielles : canal.', [640, 1280, 1920], '(min-width: 960px) 45vw, 100vw', '../')}
    </div>
  </div>
</section>
""",
)

# --- AMO : numbered editorial phases ----------------------------------------
PAGES["amo/index.html"] = service_page(
    "amo", "AMO", "Assistance à Maîtrise d'Ouvrage (AMO)",
    "Nous vous aidons à préparer et piloter les travaux nécessaires à la mise en œuvre des ouvrages que nous concevons au travers de nos études de faisabilité.",
    "Nos compétences au service des maîtres d'ouvrages",
    [
        ("Notre assistance pour la mise en œuvre de vos projets", ["LS'Eau vous assiste dans la mise en œuvre des ouvrages décrits dans nos études de faisabilité traitant de l'assainissement des eaux usées ou de l'exploitation des eaux souterraines."]),
        ("Assistance en phase préparatoire", ["LS'Eau met sa connaissance des secteurs du BTP à votre service et vous assiste pour consulter les entreprises à même de réaliser les travaux d'assainissement ou de forages prévus et vous aide à faire le meilleur choix de prestataires."]),
        ("Assistance en phase exécution", ["LS'Eau vous aide à piloter les travaux nécessaires à la mise en œuvre de votre projet et s'assure de leur bonne exécution."]),
    ],
    "Nos compétences à votre service.",
    [
        "Notre objectif est de vous accompagner jusqu'au terme de vos projets et de vous assurer de leur bonne exécution.",
        "Piloter la mise en œuvre des ouvrages que nous prescrivons dans nos études de faisabilité requiert des compétences techniques que nous possédons et que nous mettons à votre service.",
    ],
    "",
    "Appelez-nous",
    "LS'Eau Bureau d'études en hydrogéologie et environnement / Assistance à Maitrise d'Ouvrage (AMO) pour la mise en œuvre des ouvrages décrits dans nos études.",
    study_variant="study-grid--steps",
    annotation="Pilotage de travaux",
    extra_section=f"""
<section class="section section--tight-top" aria-label="Photographie de réalisation">
  <div class="container">
{figure('drilling-rig-property', 1920, 435, 'Atelier de forage chez un particulier, devant une maison', 'Forage d’eau chez un particulier, accompagné par LS’Eau.', [640, 1280, 1920], '100vw', '../', cls='figure-wide')}
  </div>
</section>
""",
)

# --- Dossiers réglementaires : documentary register -------------------------
code_register = """
<section class="section section--tight-top" aria-labelledby="codes-title">
  <div class="container">
    <div data-reveal><h2 id="codes-title">Les cadres réglementaires concernés</h2></div>
    <ul class="code-register">
      <li data-reveal><span class="code-register__num">R.01</span><span class="code-register__name">Code de la Santé Publique</span><svg class="icon" aria-hidden="true"><use href="#i-book"/></svg></li>
      <li data-reveal style="--rd:.06s"><span class="code-register__num">R.02</span><span class="code-register__name">Code Général des Collectivités Territoriales</span><svg class="icon" aria-hidden="true"><use href="#i-book"/></svg></li>
      <li data-reveal style="--rd:.12s"><span class="code-register__num">R.03</span><span class="code-register__name">Code de l'Environnement</span><svg class="icon" aria-hidden="true"><use href="#i-book"/></svg></li>
      <li data-reveal style="--rd:.18s"><span class="code-register__num">R.04</span><span class="code-register__name">Code Minier</span><svg class="icon" aria-hidden="true"><use href="#i-book"/></svg></li>
    </ul>
  </div>
</section>
"""

PAGES["dossiers-reglementaires/index.html"] = service_page(
    "dossiers-reglementaires", "Dossiers réglementaires", "Dossiers réglementaires",
    "Nous élaborons les dossiers de déclarations ou demandes d'autorisations réglementaires indispensables avant la mise en œuvre de vos projets.",
    "Notre maîtrise de la réglementation en matière d'environnement",
    [
        ("Eaux potables", [
            "LS'Eau élabore les dossiers de demande d'autorisation, requis au titre du Code de la Santé Publique, pour l'alimentation en eau potable, à partir d'un captage privé, de vos établissements recevant du public.",
            "Les dossiers de déclarations de captages privés requis au titre du Code Général des Collectivités Territoriales et du Code Minier.",
        ]),
        ("Eaux pluviales", ["LS'Eau élabore les dossiers de déclaration, requis au titre du Code de l'Environnement, pour la mise en œuvre de dispositifs de gestion et assainissement des eaux pluviales desservant un bassin versant naturel d'une superficie de moins de 20 hectares."]),
        ("Eaux pour la géothermie sur nappe", ["LS'Eau élabore les dossiers de déclaration, requis au titre du Code minier pour l'exploitation de la ressource en eaux souterraines dans le but de faire fonctionner une pompe à chaleur sur nappe."]),
    ],
    "Notre maîtrise de la réglementation pour plus d'efficacité dans vos projets.",
    [
        "Notre mission : vous aider à identifier vos besoins en termes de dossiers réglementaires et élaborer les documents requis pour que vos projets avancent.",
        "Grâce à notre maîtrise de la réglementation en matière d'environnement, nous sommes à même de vous guider efficacement dans la conduite des procédures administratives à mener pour les déclarations et demandes d'autorisations réglementaires indispensables avant la mise en œuvre de vos projets.",
    ],
    "",
    "Prenez rendez-vous",
    "LS'Eau Bureau d'études en hydrogéologie et environnement / Dossiers réglementaires pour les captages d'eaux souterraines et filières d'assainissement des eaux usées ou pluviales.",
    extra_section=code_register,
    annotation="Réglementation",
)

# --------------------------------------------------------------------------
# Gallery
# --------------------------------------------------------------------------
GALLERY = [
    ("anc", "soil-survey-field", [640, 1280], "Étude de sols : terrain d'assainissement non collectif", "Matériel d'étude de sols installé dans une oliveraie"),
    ("anc", "sanitation-trench", [480, 729], "Tranchée d'épandage — assainissement non collectif", "Tranchée d'épandage creusée pour une filière d'assainissement non collectif"),
    ("anc", "manual-soil-auger", [640, 1280], "Sondage à la tarière manuelle — étude de sols", "Tarière manuelle posée au sol lors d'une étude de sols en verger"),
    ("anc", "infiltration-bed", [640, 1280, 1480], "Filière d'infiltration en cours de réalisation", "Filière d'infiltration des eaux usées en cours de construction, lit de gravier"),
    ("forage", "drilling-rig-orchard", [480, 729], "Atelier de forage en verger", "Atelier de forage d'eau implanté dans un verger"),
    ("forage", "borehole-flow", [640, 1080], "Venue d'eau en tête de forage", "Eau s'écoulant en tête d'un forage en cours de réalisation"),
    ("forage", "drilling-discharge", [480, 729], "Rejet des eaux de forage", "Eaux de forage rejetées par une canalisation bleue"),
    ("forage", "piezometric-reel", [640, 1280], "Sonde piézométrique en bordure de captage", "Dévidoir de sonde piézométrique bleu installé près d'un captage"),
    ("forage", "drilling-mast-casings", [640, 1280, 1920], "Mât de forage et tubages", "Mât de forage dressé et tubages bleus alignés au sol"),
    ("forage", "drilling-rig-cypress", [640, 1280, 1920], "Forage d'eau en terrain arboré", "Atelier de forage d'eau au milieu de cyprès"),
    ("forage", "drilling-rig-property", [640, 1280, 1920], "Forage chez un particulier", "Atelier de forage chez un particulier, devant une maison"),
    ("pluvial", "drainage-ditch", [640, 1280, 1413], "Fossé empierré de gestion des eaux pluviales", "Fossé empierré longeant une route, destiné à la gestion des eaux pluviales"),
    ("superficiel", "pond-dusk", [640, 1280, 1920], "Plan d'eau — eaux superficielles", "Plan d'eau au crépuscule, eaux superficielles"),
    ("superficiel", "canal-bridge", [640, 1280, 1920], "Canal — eaux superficielles", "Canal en eau bordé de maçonnerie, avec un pont de pierre"),
]

gallery_items = []
for i, (cat, stem, widths, caption, alt) in enumerate(GALLERY):
    thumb = widths[0]
    large = widths[-1]
    gallery_items.append(
        f"""    <li data-category="{cat}" data-reveal style="--rd:{(i%3)*0.07:.2f}s">
      <figure>
        <a href="../assets/images/{stem}-{large}w.webp" data-lightbox data-caption="{caption}">
          <img src="../assets/images/{stem}-{thumb}w.webp" alt="{alt}" width="640" height="480" loading="lazy" decoding="async">
        </a>
        <figcaption>{caption}</figcaption>
      </figure>
    </li>"""
    )

gallery_body = f"""{header('galerie', '../')}<main id="main">
<div class="page-head">
  <span class="contours contours--ink" aria-hidden="true"></span>
  <div class="container">
{page_top('Galerie', '../', 'Réalisations')}    <h1>Galerie</h1>
    <p class="lead">Vous trouverez ici un aperçu de ce que nous faisons et quelques projets sur lesquels nous avons travaillé.</p>
  </div>
</div>

<section class="section" aria-label="Photographies de réalisations">
  <div class="container">
    <div class="gallery-filters" role="group" aria-label="Filtrer les photos par catégorie">
      <button class="filter-btn" type="button" data-filter="all" aria-pressed="true">Tout</button>
      <button class="filter-btn" type="button" data-filter="anc" aria-pressed="false">Assainissement non collectif</button>
      <button class="filter-btn" type="button" data-filter="forage" aria-pressed="false">Forages d'eau</button>
      <button class="filter-btn" type="button" data-filter="pluvial" aria-pressed="false">Eaux pluviales</button>
      <button class="filter-btn" type="button" data-filter="superficiel" aria-pressed="false">Eaux superficielles</button>
    </div>
    <ul class="gallery-grid">
{chr(10).join(gallery_items)}
    </ul>
    <p class="gallery-empty" hidden>Aucune photo dans cette catégorie.</p>
  </div>
</section>

<dialog class="lightbox" id="lightbox" aria-label="Visionneuse de photos">
  <div class="lightbox__frame">
    <img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="">
    <button class="lightbox__btn lightbox__close" type="button" aria-label="Fermer la visionneuse">
      <svg class="icon" aria-hidden="true"><use href="#i-close"/></svg>
    </button>
    <button class="lightbox__btn lightbox__nav lightbox__nav--prev" type="button" aria-label="Photo précédente">
      <svg class="icon" aria-hidden="true"><use href="#i-chevron-left"/></svg>
    </button>
    <button class="lightbox__btn lightbox__nav lightbox__nav--next" type="button" aria-label="Photo suivante">
      <svg class="icon" aria-hidden="true"><use href="#i-chevron-right"/></svg>
    </button>
    <div class="lightbox__bar">
      <p class="lightbox__caption"></p>
      <span class="lightbox__count" aria-live="polite"></span>
    </div>
  </div>
</dialog>

{cta_band()}</main>
{footer('../')}"""

PAGES["galerie/index.html"] = {
    "title": f"Galerie photos — {SUFFIX}",
    "desc": "LS'Eau Bureau d'études en hydrogéologie et environnement / Galerie photos",
    "canonical": DOMAIN + "/galerie/",
    "body": gallery_body,
}

# --------------------------------------------------------------------------
# Contact
# --------------------------------------------------------------------------
contact_body = f"""{header('nous-contacter', '../')}<main id="main">
<div class="page-head">
  <span class="contours contours--ink" aria-hidden="true"></span>
  <div class="container">
{page_top('Contact', '../', 'Coordonnées')}    <h1>Nous contacter</h1>
    <p class="lead">Si vous avez des questions à propos de nos prestations, veuillez nous contacter par e-mail ou par téléphone : nous vous répondrons dans les plus brefs délais. Vous avez aussi la possibilité de nous appeler pendant nos heures d'ouverture. Nous espérons avoir de vos nouvelles bientôt !</p>
  </div>
</div>

<section class="section" aria-label="Coordonnées et localisation">
  <div class="container">
    <div class="contact-layout">
      <div class="contact-layout__info">
        <ul class="contact-register">
          <li data-reveal>
            <span class="contact-register__icon"><svg class="icon" aria-hidden="true"><use href="#i-phone"/></svg></span>
            <h2>Téléphone</h2>
            <div class="contact-register__value"><a href="tel:+33651802623">06 51 80 26 23</a><span class="contact-register__hint">Nous appeler</span></div>
          </li>
          <li data-reveal style="--rd:.08s">
            <span class="contact-register__icon"><svg class="icon" aria-hidden="true"><use href="#i-mail"/></svg></span>
            <h2>E-mail</h2>
            <div class="contact-register__value"><a href="mailto:contact@ls-eau.fr">contact@ls-eau.fr</a><span class="contact-register__hint">Envoyez-nous un e-mail</span></div>
          </li>
          <li data-reveal style="--rd:.16s">
            <span class="contact-register__icon"><svg class="icon" aria-hidden="true"><use href="#i-pin"/></svg></span>
            <h2>Adresse</h2>
            <div class="contact-register__value"><address>389, route des Courses<br>84300 Cavaillon, France</address><span class="contact-register__hint">Où nous trouver</span></div>
          </li>
        </ul>
        <p class="contact-sign"><strong>Laurent SOUCHON</strong> — Gérant de LS'Eau</p>
      </div>
      <aside class="contact-map" aria-labelledby="map-title" data-reveal style="--rd:.2s">
        <h2 id="map-title" class="contact-map__title">Nous trouver à Cavaillon</h2>
        <div class="contact-map__frame">
          <iframe
            title="Carte OpenStreetMap — LS'Eau, 389 route des Courses, 84300 Cavaillon"
            src="https://www.openstreetmap.org/export/embed.html?bbox=5.037786%2C43.827722%2C5.047786%2C43.833722&amp;layer=mapnik&amp;marker=43.830722%2C5.042786"
            width="600" height="450" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
        <p class="contact-map__note">Siège de LS'Eau : 389, route des Courses, 84300 Cavaillon.<br>
          <a href="https://www.openstreetmap.org/?mlat=43.830722&amp;mlon=5.042786#map=17/43.830722/5.042786" target="_blank" rel="noopener">Ouvrir la carte dans OpenStreetMap</a></p>
        <p class="contact-map__credit">Fond cartographique © les <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">contributeurs OpenStreetMap</a>.</p>
      </aside>
    </div>
  </div>
</section>

{cta_band()}</main>
{footer('../')}"""

PAGES["nous-contacter/index.html"] = {
    "title": f"Contact — {SUFFIX}",
    "desc": "LS'Eau Bureau d'études en hydrogéologie et environnement / Nous contacter",
    "canonical": DOMAIN + "/nous-contacter/",
    "body": contact_body,
}

# --------------------------------------------------------------------------
# Legal
# --------------------------------------------------------------------------
legal_body = f"""{header('mentions-legales', '../')}<main id="main">
<div class="page-head">
  <span class="contours contours--ink" aria-hidden="true"></span>
  <div class="container">
{page_top('Mentions légales', '../', 'Informations légales')}    <h1>Mentions légales</h1>
  </div>
</div>

<div class="section">
  <div class="container legal">
    <section aria-labelledby="legal-siege">
      <h2 id="legal-siege">Siège social</h2>
      <dl>
        <dt>Nom de l'entreprise</dt><dd>LS'Eau</dd>
        <dt>Forme juridique</dt><dd>SARL au capital de 5 000 €</dd>
        <dt>Gérant</dt><dd>M. Laurent SOUCHON</dd>
        <dt>Adresse</dt><dd>389, route des Courses, 84300 Cavaillon</dd>
      </dl>
    </section>
    <section aria-labelledby="legal-contact">
      <h2 id="legal-contact">Contact</h2>
      <dl>
        <dt>Tél.</dt><dd><a href="tel:+33651802623">06 51 80 26 23</a></dd>
        <dt>E-mail</dt><dd><a href="mailto:contact@ls-eau.fr">contact@ls-eau.fr</a></dd>
      </dl>
    </section>
    <section aria-labelledby="legal-rcs">
      <h2 id="legal-rcs">Représentant légal</h2>
      <dl>
        <dt>Inscription au registre du commerce et des sociétés</dt>
        <dd>Numéro d'inscription : 889 694 923 R.C.S. Avignon</dd>
      </dl>
    </section>
    <section aria-labelledby="legal-siret">
      <h2 id="legal-siret">Immatriculation</h2>
      <dl>
        <dt>SIRET</dt><dd>889694923 00018</dd>
      </dl>
    </section>
    <section aria-labelledby="legal-tva">
      <h2 id="legal-tva">Numéro de TVA intracommunautaire</h2>
      <dl>
        <dt>Numéro de TVA intracommunautaire</dt><dd>FR 92889694923</dd>
      </dl>
    </section>
  </div>
</div>
</main>
{footer('../')}"""

PAGES["mentions-legales/index.html"] = {
    "title": f"Mentions légales — {SUFFIX}",
    "desc": "LS'Eau Bureau d'études en hydrogéologie et environnement / Mentions légales",
    "canonical": DOMAIN + "/mentions-legales/",
    "body": legal_body,
}

# --------------------------------------------------------------------------
# 404
# --------------------------------------------------------------------------
notfound_body = f"""{header('', '')}<main id="main">
<section class="notfound" aria-labelledby="notfound-title">
  <span class="contours contours--ink notfound__contours" aria-hidden="true"></span>
  <span class="notfound__strata" aria-hidden="true"></span>
  <div class="container notfound__inner">
    <p class="notfound__code" aria-hidden="true">404</p>
    <div class="notfound__grid">
      <div class="notfound__main">
        <p class="notfound__eyebrow">Erreur 404 · secteur non cartographié</p>
        <h1 id="notfound-title">Page introuvable</h1>
        <p class="notfound__line">Cette page s'est perdue dans la nappe.</p>
        <p class="lead">La page demandée n'existe pas ou a été déplacée. Revenez à l'accueil, ou rejoignez directement l'une de nos prestations.</p>
        <div class="hero__actions notfound__actions">
          <a class="btn btn--primary" href="/">Retour à l'accueil</a>
          <a class="btn btn--outline" href="/nous-contacter/">Nous contacter</a>
        </div>
        <p class="notfound__coords" aria-hidden="true"><span>43.830722° N</span><span>5.042786° E</span><span>Cavaillon</span></p>
      </div>
      <nav class="notfound__services" aria-label="Accès direct aux prestations">
        <p class="notfound__caption">Prestations</p>
        <ul>
          <li><a href="/assainissement/"><span>01</span>Eaux usées</a></li>
          <li><a href="/eaux-pluviales/"><span>02</span>Eaux pluviales</a></li>
          <li><a href="/eaux-souterraines/"><span>03</span>Eaux souterraines</a></li>
          <li><a href="/hydrometrie/"><span>04</span>Hydrométrie</a></li>
          <li><a href="/amo/"><span>05</span>AMO</a></li>
          <li><a href="/dossiers-reglementaires/"><span>06</span>Dossiers réglementaires</a></li>
          <li><a href="/galerie/"><span>07</span>Galerie</a></li>
        </ul>
      </nav>
    </div>
  </div>
</section>
</main>
{footer('')}"""

PAGES["404.html"] = {
    "title": f"Page introuvable — {SUFFIX}",
    "desc": "La page demandée n'existe pas ou a été déplacée.",
    "canonical": DOMAIN + "/404.html",
    "body": notfound_body,
    "head_prefix": '  <script>if(location.protocol!=="file:"){document.write(\'<base href="/">\');}</script>\n',
    "extra": '  <meta name="robots" content="noindex">\n',
}

# --------------------------------------------------------------------------
# Emit files
# --------------------------------------------------------------------------
for rel, page in PAGES.items():
    dest = ROOT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    prefix = "" if "/" not in rel else "../"
    html = page_head(page["title"], page["desc"], page["canonical"], prefix,
                     page.get("extra", ""), page.get("body_class", ""),
                     page.get("head_prefix", "")) + page["body"] + "\n</body>\n</html>\n"
    dest.write_text(html, encoding="utf-8")
    print(f"wrote {rel} ({len(html) // 1024} KB)")