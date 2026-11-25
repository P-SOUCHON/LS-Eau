# LS'Eau — Static Website

Complete static reconstruction of https://www.ls-eau.fr/ — pure HTML5, CSS3 and
vanilla JavaScript. **No frameworks, no build step, no backend.** The
`website/` directory is the production deliverable: it can be uploaded as-is to
IONOS web hosting with FileZilla. The only third-party request is the optional,
lazy-loaded OpenStreetMap embed on the contact page (documented in §7).

---

## 1. Project structure

```
LS'Eau/
├── website/                  ← PRODUCTION DIRECTORY (upload its CONTENTS)
│   ├── index.html            Homepage
│   ├── assainissement/index.html        Eaux usées
│   ├── eaux-pluviales/index.html        Eaux pluviales (old URL: /hydrogéologie)
│   ├── eaux-souterraines/index.html     Eaux souterraines
│   ├── hydrometrie/index.html           Hydrométrie (old URL: /hydrométrie)
│   ├── amo/index.html                   Assistance à Maîtrise d'Ouvrage
│   ├── dossiers-reglementaires/index.html  Dossiers réglementaires
│   ├── galerie/index.html               Photo gallery (14 photos + lightbox)
│   ├── nous-contacter/index.html        Contact
│   ├── mentions-legales/index.html      Legal information
│   ├── 404.html              Custom not-found page
│   ├── assets/images/        Optimized WebP photos, logo, favicons, OG image,
│   │                         topographic contour motifs (contours-*.svg)
│   ├── assets/fonts/         Self-hosted OFL fonts (Manrope, Source Serif 4)
│   ├── css/style.css         All styles (design tokens + responsive rules)
│   ├── js/main.js            Mobile nav, header, reveals, parallax, gallery
│   ├── robots.txt
│   ├── sitemap.xml
│   └── .htaccess             301 redirects from old accented URLs + 404 page
├── audit/                    Development artifacts (NOT uploaded)
│   ├── AUDIT.md              Full audit of the old website
│   ├── REFINEMENT.md         Phase 2 visual identity record
│   ├── POLISH.md             Phase 3 final polish record + validation
│   ├── raw/                  Downloaded pages of the old site
│   ├── text/                 Extracted French content
│   ├── images/owner/         Original recovered photographs (full resolution)
│   ├── images/stock-inspection/  Old stock images (excluded, never deployed)
│   └── *.py                  Audit / authoring / QA scripts (dev only)
├── ASSET-INVENTORY.md        Image origins and licensing decisions
└── README.md                 This file
```

Each page lives in its own folder with an `index.html`, which produces clean
extensionless URLs (`/assainissement/`, `/galerie/`, …) identical to the old
site's structure. Three old URLs contained accented characters
(`/hydrogéologie`, `/hydrométrie`, `/dossiers-réglementaires`); the new ASCII
URLs are reached through permanent 301 redirects defined in `.htaccess`, so
existing search-engine rankings and external links are preserved.

## 2. Preview the website locally

**Option A — simply open the files.** Double-click `website/index.html`.
Everything (navigation, gallery, lightbox) works from the filesystem. The
custom `404.html` also works from disk: its internal links are relative and a
tiny inline `<base>` only activates over HTTP.

**Option B — local HTTP server (recommended, matches production):**

```bash
cd website
python3 -m http.server 8080
# then open http://localhost:8080/
```

No installation, no npm, no build command is ever required.

## 3. Modify text

All customer-facing text is plain French HTML inside the page files.
Open the relevant `index.html` in any text editor (VS Code, Notepad++, …),
find the sentence, edit it, save. Example: to change the homepage intro,
edit the `<p>` inside `<div class="hero__content">` in `website/index.html`.

- Page titles / SEO descriptions: `<title>` and `<meta name="description">`
  at the top of each file.
- Phone number / email: search for `06 51 80 26 23`, `tel:+33651802623`
  and `contact@ls-eau.fr` (they appear in the footer of every page, in the
  contact band, and on the contact/legal pages).
- Legal data: `website/mentions-legales/index.html`.

The header and footer are duplicated in every page file (standard for static
sites). If you change a navigation label or a footer detail, apply the same
change to all 11 HTML files.

## 4. Replace or add photographs

Photos are stored in `website/assets/images/` as WebP files named
`<subject>-<width>w.webp` (e.g. `drilling-rig-orchard-729w.webp`).

To replace a photo:

1. Export your new photo as WebP at the same width(s) as the existing file(s)
   (keep the same filenames), or as JPG/PNG and update the `src`/`srcset`
   references in the HTML.
2. Keep the `width`/`height` attributes and the French `alt` text accurate.
3. Full-resolution originals of all current photos are kept in
   `audit/images/owner/` for reference.

To add a photo to the gallery, copy an existing `<li data-category="…">` block
in `website/galerie/index.html`, point it at the new files, and update the
caption and `alt`. Categories: `anc`, `forage`, `pluvial`, `superficiel`.

Image generation from originals can be repeated with
`python3 audit/process_images.py` (requires ImageMagick; dev machine only).

## 5. Add or remove a page

**Add:** create `website/<slug>/index.html` (copy an existing page as a
template — keep the `../` asset prefixes), then add a link in the header nav
and footer of the other pages, and a `<url>` entry in `sitemap.xml`.

**Remove:** delete the folder, remove its links from the other pages and from
`sitemap.xml`, and optionally add a `RedirectMatch 301` line in `.htaccess`.

## 6. Deploy with FileZilla (IONOS hosting)

> Do this only after the owner has approved the new site. Keep the old site
> running until the upload is verified.

### 6.1 Back up the current website first

1. Open FileZilla and connect to the IONOS webspace
   (Host / username / password from the IONOS control panel →
   *Hosting → SFTP & SSH / FTP access*; use the FTP credentials shown there).
2. In the remote pane, locate the current web root. On IONOS it is typically
   the folder the domain points to (check *Hosting → Domains → document
   root*; commonly `/` or a subfolder such as `/ls-eau` — **not** the
   `logs` folder).
3. Select all existing website files and download them to a local backup
   folder (e.g. `backup-ls-eau-YYYY-MM-DD/`). Verify the backup opens locally.

### 6.2 Upload the new site

1. In FileZilla's **local** pane, open the `website/` folder of this project.
2. Select **all of its contents** (index.html, the page folders, assets/,
   css/, js/, robots.txt, sitemap.xml, .htaccess — enable
   *Server → Force showing hidden files* to see `.htaccess`).
3. In the **remote** pane, open the web root directory.
4. Drag the selection across. When prompted, choose **Overwrite** for
   existing files. Upload in binary/automatic mode (FileZilla default).
5. Old editor files that are not part of the new site may remain harmlessly,
   but for a clean result delete the old site's files **after** confirming
   the backup and the new site works (keep the backup regardless).

### 6.3 Verify

- Visit `https://www.ls-eau.fr/` and each menu page.
- Check `https://www.ls-eau.fr/hydrogéologie` redirects to `/eaux-pluviales/`
  (proves `.htaccess` is active).
- Test on a phone: menu button, gallery lightbox, tap-to-call links.

### 6.4 IONOS-specific considerations (from the audit)

- The current site is served by the **IONOS MyWebsite editor product**, not
  by plain webspace files. For the static site to be served, the domain must
  point to the webspace directory where you upload the files. In the IONOS
  control panel, set the domain's target to the webspace folder (or use
  "Deploy webspace files" / disconnect the editor site). The editor
  subscription can then be cancelled — that is the cost saving goal.
- IONOS shared hosting runs Apache and supports `.htaccess`; the included
  file only adds 301 redirects and the 404 page. The site works even if
  `.htaccess` is ignored.
- Upload `.htaccess` explicitly (hidden file). If FileZilla skips it, the
  site still works; only old-URL redirects would be missing.
- No database, no PHP, no Node.js is used or needed.

## 7. Technical notes

### Art direction
The site uses an editorial / scientific-publication identity inspired by
hydrogeology: fine topographic contour motifs (`assets/images/contours-*.svg`,
purely decorative and `aria-hidden`), hairline rules, monospace technical
annotations (section indices, captions), asymmetric compositions and strong
contrast between light and deep-navy sections. Each service page has its own
composition (installation photography, restrained panoramic band, dark "depth"
section, measurement register, numbered phases, documentary code register)
while sharing one design system.

### Typography (self-hosted, SIL Open Font License)
- **Source Serif 4** (variable, 400–700) — display/headings. Editorial serif.
- **Manrope** (variable, 400–800) — body, navigation, buttons, UI.
- System **monospace** stack — technical annotations (no extra download).
Files live in `assets/fonts/` with their OFL license texts; both are preloaded
and use `font-display: swap`. Only the latin subset is shipped (covers French).
No external font service is contacted.

### Motion system (progressive, accessible)
- Hero entrance: staggered fade/rise on load (CSS, JS-gated).
- Section reveals: `IntersectionObserver` adds `.is-in`; elements are only
  hidden after JS confirms support, so content is always visible without JS.
- Header: transparent over the homepage hero, becomes a compact solid bar on
  scroll; inner pages use a solid fixed header.
- Restrained hero parallax (transform-only, clamped, rAF-throttled).
- All motion respects `prefers-reduced-motion` (verified) and never blocks
  content, hijacks scroll, or snaps sections.

### OpenStreetMap embed (only external dependency)
The contact page shows a compact map of the registered office. It uses the
standard OpenStreetMap iframe embed — no API key, no paid service, no mapping
library, no analytics:

```
https://www.openstreetmap.org/export/embed.html?bbox=…&layer=mapnik&marker=…
```

- **Coordinates:** 43.830722 N, 5.042786 E, geocoded from the published address
  (389, route des Courses, 84300 Cavaillon) with the official French
  **Base Adresse Nationale** (`api-adresse.data.gouv.fr`), not estimated.
- **Behaviour:** `loading="lazy"`, descriptive `title`, 4:3 responsive frame.
  The address, a plain-text location note and a direct
  `https://www.openstreetmap.org/...` link sit outside the iframe, so they
  remain available if the embed is blocked or offline.
- **Privacy:** the iframe is the only request made to a third party; it loads
  only when the contact page is visited and the map approaches the viewport.
  No tracking script, cookie banner or analytics is added by the site.
  OpenStreetMap's own page/attribution appears inside the frame.
- **Maintenance:** to move the map, edit the two attributes (`src` and the
  external link) in `website/nous-contacter/index.html` (and in
  `audit/build_pages.py` if pages are regenerated). Keep the marker and the
  bbox consistent.

### Foundations
- **Design tokens** (colors, spacing, type) are CSS custom properties at the
  top of `css/style.css`. Palette derives from the logo (navy + turquoise).
- **Responsive breakpoints:** 1120px (mobile nav), 1024px, 960px, 640px, 380px.
  Validated at 1440 / 1024 / 820 / 390 / 360. Mobile menu works without JS.
- **Accessibility:** skip link, keyboard menu/lightbox (Esc/arrows), visible
  focus rings, `aria-current`/`aria-expanded`/`aria-pressed`, WCAG AA contrast,
  reduced-motion support, descriptive French alt text, decorative SVG hidden
  from assistive tech.
- **Performance:** responsive WebP `srcset`, lazy loading, `fetchpriority` on
  the hero, two small self-hosted fonts, no analytics/cookies; the sole
  third-party request is the lazy OpenStreetMap embed on the contact page.
- **SEO:** unique titles/descriptions, canonical URLs, Open Graph, sitemap,
  robots, 301 redirects for changed URLs, semantic headings.

## 8. Known limitations / manual actions

- The old IONOS contact form cannot exist on a static site; it is replaced by
  direct phone/e-mail contact (no form data is collected anywhere).
- A secondary phone number (`06 74 63 03 76`) appeared only inside the old
  form's error message; it is not displayed on the new site. Confirm with the
  owner whether it should be added.
- Opening hours were mentioned on the old contact page but never published;
  none were invented. Add them if the owner provides them.
- 12 stock images and 5 stock/publisher book photos from the old site were
  **not** reused (licensing unverifiable outside the IONOS editor). See
  `ASSET-INVENTORY.md`. All 14 authentic company photographs were recovered
  and reused.
- The domain/document-root switch in the IONOS panel (section 6.4) is a
  manual step for the owner at deployment time.