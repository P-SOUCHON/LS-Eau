# LS'Eau — Asset Inventory & Licensing

Audit date: 2026-11-23. Full context in `audit/AUDIT.md`.

## A. Reused assets — owner originals (authorization obtained)

Recovered from the site-specific IONOS editor CDN path
`cdn.website-editor.net/ccd24da11b95483eb449a37841e09405/` (the owner's own
upload library). Full-resolution originals preserved in `audit/images/owner/`;
optimized WebP derivatives deployed in `website/assets/images/`.

| Deployed file(s) | Original file | Dimensions (orig.) | Subject |
|---|---|---|---|
| soil-survey-field-*.webp | ANC001.jpg | 1296×972 | Soil-study site, olive grove |
| sanitation-trench-*.webp | ANC002.jpg | 729×972 | Sanitation trench excavation |
| manual-soil-auger-*.webp | ANC003.jpg | 1296×972 | Manual soil auger, orchard |
| infiltration-bed-*.webp | assainissement-autonome_1.jpg | 1480×366 | Gravel infiltration bed |
| pond-dusk-*.webp | DSC_0046.JPG | 1920×1080 | Pond at dusk (surface water) |
| drilling-rig-property-*.webp | DSC05628.jpg | 1920×435 | Drilling rig at a residence |
| drilling-discharge-*.webp | Forage001.jpg | 729×972 | Drilling-water discharge |
| borehole-flow-*.webp | Forage002.jpg | 1080×1920 | Water flow at borehole head |
| drilling-rig-orchard-*.webp | Forage003.jpg | 729×972 | Drilling rig in orchard |
| piezometric-reel-*.webp | Forage004.jpg | 1296×972 | Piezometric reel at well head |
| drilling-mast-casings-*.webp | IMG_6717.jpg | 1920×2880 | Drilling mast + casings |
| drainage-ditch-*.webp | IMG_6784 - IMG_6792.jpg | 1413×576 | Stone-lined drainage ditch |
| canal-bridge-*.webp | IMG_6855 - IMG_6861_blended_fused.jpg | 1920×1240 | Canal with stone bridge |
| drilling-rig-cypress-*.webp | IMG_9435.JPG | 1920×1280 | Drilling rig among cypress |
| ls-eau-logo.png | LOGO REDUIT LS-Eau.png | 695×820 | Company logo (trimmed, 240px h) |
| favicon.png | LOGO ICONE 57.png | 57×57 | Droplet icon |

Derived assets created for the rebuild (no third-party content):
- `favicon.svg` — vector droplet redrawn from the logo's brand colors.
- `og-image.jpg` — 1200×630 social-share card composed from IMG_9435.JPG
  with the company name and activity line.
- `contours-ink.svg` / `contours-paper.svg` — original topographic contour
  motifs generated for the art direction (decorative, `aria-hidden`).

### Fonts (added in the visual refinement, self-hosted)
| File | Family | License | Size |
|---|---|---|---|
| manrope-latin-var.woff2 | Manrope (variable 400–800) | SIL OFL 1.1 (`OFL-Manrope.txt`) | 24 KB |
| source-serif-4-latin-var.woff2 | Source Serif 4 (variable 400–700) | SIL OFL 1.1 (`OFL-SourceSerif4.txt`) | 122 KB |

Both fonts are free for commercial use and self-hosting under the SIL Open
Font License; license texts are stored alongside the files. Latin subset only
(covers French). No external font service is used at runtime.

Processing: auto-orient, downscale only (never upscaled), WebP quality 70–82,
metadata stripped. Technical photographs kept at sufficient resolution;
large variants load on demand (lightbox), 480–640px variants inline.

## B. Third-party assets — NOT redistributed

Licensing could not be verified for use outside the IONOS editor service,
so none of these are deployed. Inspection copies are kept locally only, in
`audit/images/stock-inspection/` (never uploaded).

### B1. IONOS stock library (`md/and1/` CDN path) — 15 images
10360 (pouring water), 10604 (splash), 113127 (hand under water),
113536 (drawing instruments), 114575 (hose on grass), 116592 (rainbow),
116875 (laptop on grass), 121125 (forest bridge), 123700 (PVC pipes),
15229 (concrete pipes), 2470 (water vortex), 125229 (engineers),
126057 (signing hand), 126242 (law books), 13218 (water surface).
Old usage: service-page hero backgrounds and 12 of 26 gallery items.

### B2. IONOS editor template images (`md/dmtmpl/`) — 2 images
businessman-using-a-computer-talking-on-the-mobile-phone,
meeting-room-with-black-chairs. Old usage: decorative section backgrounds.

### B3. Stock/publisher images cached in the owner's library — 5 images
- 100334_IMG_54279_HR.jpg — Code de la Santé Publique + pills (staged stock)
- 33914_large.jpg — Code de l'Environnement on grass (stock-style)
- p14cgct300_1_1.jpg — CGCT volume set (publisher product photo)
- Instruction.jpg — Code Minier book (stock-style)
- cc8fe49be53f…jpeg — construction workers silhouette (stock)

### B4. Non-image
- 3f9ab32fc5…jpeg — flat gray placeholder, not a photograph.
- 1und1-logo8.svg — IONOS branding badge (removed by design).

## C. Replacement strategy

No substitute stock imagery was introduced. The rebuilt site relies exclusively
on the 14 authentic company photographs plus typographic/iconographic design.
The regulatory page presents the legal codes as text reference cards; every
piece of textual legal content from the old site is preserved. If the owner
wishes to restore book imagery later, they must supply properly licensed files.