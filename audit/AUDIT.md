# LS'Eau — Existing Website Audit (Phase 1)

Audit date: 2026-11-23
Source: https://www.ls-eau.fr/ (IONOS "MyWebsite" editor, Duda-based — `website-editor.net` CDN)
Method: full download of every sitemap URL + recursive link inspection (`audit/raw/`),
text extraction (`audit/text/`), image recovery (`audit/images/`), visual classification.

## 1. Page inventory (10 pages — sitemap + navigation agree, no hidden pages found)

| # | Old URL | Nav label | Purpose | New URL (static rebuild) |
|---|---------|-----------|---------|--------------------------|
| 1 | `/` | Accueil | Homepage: hero, 6 service blocks, "Qui Sommes Nous", contact | `/` |
| 2 | `/assainissement` | Eaux usées | Non-collective wastewater sanitation studies | `/assainissement/` |
| 3 | `/hydrogéologie` | Eaux pluviales | Rainwater management studies (URL/title mismatch on old site: slug says hydrogéologie, content is "Eaux pluviales") | `/eaux-pluviales/` + 301 |
| 4 | `/eaux-souterraines` | Eaux souterraines | Groundwater / borehole feasibility & design | `/eaux-souterraines/` |
| 5 | `/hydrométrie` | Hydrométrie | Hydrometry services (wastewater, groundwater, surface water) | `/hydrometrie/` + 301 |
| 6 | `/amo` | AMO | Assistance à Maîtrise d'Ouvrage | `/amo/` |
| 7 | `/dossiers-réglementaires` | Dossiers réglementaires | Regulatory filings (drinking water, rainwater, geothermal) | `/dossiers-reglementaires/` + 301 |
| 8 | `/galerie` | Galerie (under "……" overflow menu) | Photo gallery, 26 items | `/galerie/` |
| 9 | `/nous-contacter` | Contact (overflow menu) | Contact form (IONOS widget) + email link | `/nous-contacter/` |
| 10 | `/mentions-legales` | Mentions Légales (overflow menu) | Legal information | `/mentions-legales/` |

`robots.txt`: allow all + sitemap reference. `sitemap.xml`: the 10 URLs above, lastmod 2022-05-25.
No other internal links exist. Only external links: IONOS self-promotion ("Crée avec IONOS"
badge + `ionos.fr/site-internet/creer-un-site-internet`) — removed in rebuild.
"Voir le portfolio" buttons on homepage are editor widgets wired by JS to the gallery → rebuilt as links to `/galerie/`.

## 2. Business information (authoritative, preserved verbatim)

- Company: **LS'Eau** — bureau d'études en hydrogéologie et assainissement (hydrogeology & environment consultancy)
- Manager: **M. Laurent SOUCHON** (gérant)
- Legal form: **SARL au capital de 5 000 €**
- Address: **389, Route des Courses, 84300 CAVAILLON, France**
- Phone (site-wide): **06 51 80 26 23**
- Email: **contact@ls-eau.fr**
- RCS: **889 694 923 R.C.S. Avignon**
- SIRET: **889694923 00018** (as printed on the old site)
- VAT: **FR 92889694923**
- Secondary phone **06 74 63 03 76** appears ONLY inside the contact-form technical-error
  message. Not displayed anywhere else. Kept out of the rebuild (obsolete widget text);
  flagged for owner confirmation.
- No opening hours, no map embed, no social links exist on the old site (contact text mentions
  "heures d'ouverture" but no hours are published anywhere — not invented in rebuild).
- Old contact form: IONOS-hosted submission widget. Cannot be reproduced statically → replaced
  by direct tel:/mailto: contact (per mission). Form intro sentence adapted accordingly.

## 3. SEO metadata (old site)

Titles follow `LS'Eau / Bureau d'études en hydrogéologie et assainissement / <Page>`.
Meta descriptions exist per page (see `audit/raw/*.html`); reused in rebuild.
Open Graph: type/url/title/description/image present on homepage. Fonts: Source Sans Pro /
Cabin / Helvetica via editor CDN. Brand colors sampled from logo: navy `#000080`,
turquoise `#22C2D4` / `#05D5E7`, silver `#B6DBDD`.

## 4. Image inventory & licensing classification

### A. Owner original photographs — REUSED (authorization obtained)
Uploaded under the site-specific CDN path `cdn.website-editor.net/ccd24da11b95483eb449a37841e09405/`.
Recovered at best available resolution into `audit/images/owner/`:

| File | Dimensions | Content (visual inspection) |
|------|-----------|------------------------------|
| ANC001.jpg | 1296×972 | Soil-study site in olive grove, field equipment |
| ANC002.jpg | 729×972 | Excavated sanitation trench, mini-excavator |
| ANC003.jpg | 1296×972 | Manual soil auger (tarière) in orchard |
| assainissement-autonome_1.jpg | 1480×366 | Gravel infiltration bed under construction |
| DSC_0046.JPG | 1920×1080 | Pond at dusk (surface water) |
| DSC05628.jpg | 1920×435 | Drilling rig at a residential property (panorama) |
| Forage001.jpg | 729×972 | Drilling-water discharge from blue pipe |
| Forage002.jpg | 1080×1920 | Water flow at borehole head during drilling |
| Forage003.jpg | 729×972 | Drilling rig in orchard |
| Forage004.jpg | 1296×972 | Piezometric reel/probe beside well head |
| IMG_6717.jpg | 1920×2880 | Drilling mast and blue casing pipes |
| IMG_6784 - IMG_6792.jpg | 1413×576 | Stone-lined roadside drainage ditch (panorama) |
| IMG_6855 - IMG_6861_blended_fused.jpg | 1920×1240 | Canal with stone bridge (panorama) |
| IMG_9435.JPG | 1920×1280 | Drilling rig among cypress trees |
| LOGO REDUIT LS-Eau.png | 695×820 | Company logo (turquoise droplet + navy "LS'Eau") |
| LOGO ICONE 57.png | 57×57 | Droplet icon (favicon) |

### B. Third-party images — NOT REDISTRIBUTED (licensing unverifiable outside IONOS editor)
1. **IONOS stock library** (`md/and1/` path, numeric IDs) — generic stock photos, confirmed by
   visual inspection: 10360 (pouring water), 10604 (water splash), 113127 (hand under water),
   113536 (drawing instruments), 114575 (hose on grass), 116592 (rainbow landscape),
   116875 (laptop on grass), 121125 (forest stone bridge), 123700 (PVC pipes),
   15229 (concrete pipes), 2470 (water vortex), 125229 (engineers with hard hats),
   126057 (hand signing document), 126242 (law books shelf), 13218 (water surface).
   Used on old site as page heroes and 12 of the 26 gallery items.
2. **Editor template images** (`md/dmtmpl/`): "businessman-using-a-computer-talking-on-the-mobile-phone",
   "meeting-room-with-black-chairs" — decorative section backgrounds.
3. **Stock/publisher images cached in the site library** (excluded despite site-path hosting):
   - `100334_IMG_54279_HR.jpg` — Code de la Santé Publique with pills (staged stock composition)
   - `33914_large.jpg` — Code de l'Environnement on grass (stock-style)
   - `p14cgct300_1_1.jpg` — CGCT 4-volume set (publisher product photo)
   - `Instruction.jpg` — Code Minier book (stock-style)
   - `cc8fe49be53f...jpeg` — construction workers silhouette at dusk (stock)
4. **Placeholder**: `3f9ab32fc5...jpeg` — flat gray rectangle, not a photograph.

Replacement strategy: no substitute stock imagery. Pages rely on the 14 authentic owner
photographs; the regulatory page uses typographic code-reference cards (all textual legal
content preserved). Old stock heroes replaced by owner photos or clean typographic headers.
Stock inspection copies kept locally in `audit/images/stock-inspection/` (never deployed).

### C. Old gallery composition
26 items = 14 owner photos (all reused) + 12 third-party images (excluded, listed above).
Rebuilt gallery: 14 authentic photos, categorized, with French captions and alt text.

## 5. Content preservation notes

All French headings/paragraphs extracted to `audit/text/*.txt` and reused verbatim in the
rebuild, except unambiguous typographical corrections (accents/grammar):
"mets ses compétences"→"met ses compétences", "aux services des particuliers"→"au service des
particuliers", "normes en vigueurs"→"normes en vigueur", "captage privée"→"captage privé",
"ll'exploitation"→"l'exploitation", "vous aidez"→"vous aider", "necessaires"→"nécessaires",
"à votre services"→"à votre service", "débitmètrie"→"débitmétrie", "qu'elles soit"→"qu'elles soient",
"en terme de"→"en termes de", "avant à la mise en œuvre"→"avant la mise en œuvre".
Removed: IONOS badge ("Crée avec"), "Share by:" social widget, form success/error widget texts.

## 6. Hosting observations

- Old site is generated by the IONOS editor; all assets hotlinked to `website-editor.net` CDNs
  with signed, expiring URLs → full local asset recovery required (done).
- Target: standard IONOS web hosting (Apache, `.htaccess` supported). Clean extensionless URLs
  implemented as `<slug>/index.html`. Three old slugs contain accents; rebuilt with ASCII slugs
  + `.htaccess` 301 redirects to preserve SEO. Site remains fully functional without `.htaccess`.
- Owner must point the domain to the webspace (leave the editor product) at deployment time —
  manual action, documented in README.