# LS'Eau — Visual Identity & UX Refinement (Phase 2)

Date: 2026-11-23. Builds on the completed reconstruction (`AUDIT.md`).
Scope: art direction, typography, layout composition, motion — functionality,
content, architecture and assets preserved.

> Historical record. The final Polish milestone (2026-11-25) supersedes a few
> details here — restrained Eaux pluviales band instead of full-bleed 21:9,
> corrected AMO step grid, contextual page-head annotations, contact map,
> redesigned 404 and footer credit. See `POLISH.md`.

## Art direction
Editorial / scientific-publication identity inspired by hydrogeology:
- Topographic contour motifs (`assets/images/contours-ink.svg`,
  `contours-paper.svg`) — generated original SVG, decorative, `aria-hidden`,
  placed in hero / page heads / CTA / depth sections at low opacity.
- Hairline rules + monospace technical annotations (section indices `01·`,
  captions, register references `R.01`) instead of boxed cards/badges.
- Asymmetric compositions; strong light ↔ deep-navy section contrast.
- Sharper radii (2–3px), restrained shadows (hover only).

## Typography (self-hosted, OFL verified)
- Display: **Source Serif 4** variable (400–700), latin woff2, 122 KB.
- Body/UI: **Manrope** variable (400–800), latin woff2, 24 KB.
- Annotations: system monospace stack (no download).
- `font-display: swap`, both preloaded; license texts stored in `assets/fonts/`.
- Hierarchy: hero clamp(2.6–4.35rem) serif; section h2 clamp(1.75–2.5rem);
  lead 1.125rem; body 1rem/1.7; mono captions 0.75rem.

## Homepage
- Full-viewport hero (`100svh`), transparent integrated header → compact solid
  bar on scroll; large serif headline; mono eyebrow; uppercase buttons;
  animated "Défiler" scroll indicator; restrained clamped parallax.
- Services: sticky-left heading + numbered editorial index (hairline rows,
  mono numbers, small icons, hover arrow) replacing six identical cards.
- About: photo + hairline value list. Realisations: varied-span photo mosaic.

## Service-page differentiation (content & IA unchanged)
- Eaux usées: head photo (trench) + spec columns + wide infiltration panorama.
- Eaux pluviales: full-bleed 21:9 water-flow photo band.
- Eaux souterraines: head photo (mast/casings) + dark "depth" navy section.
- Hydrométrie: measurement-register rows.
- AMO: numbered editorial phases + wide panorama.
- Dossiers réglementaires: documentary code register.

## Motion system
- Hero entrance (CSS, JS-gated, staggered); IntersectionObserver section
  reveals (`.reveal-init` added only when JS+IO available → no-JS safe);
  header transformation; clamped transform-only hero parallax (rAF).
- `prefers-reduced-motion` disables all of it (verified via emulated pass).
- No scroll-jacking, snapping, pinned panels, or animation libraries.

## Preserved
All 10 pages + 404, all French content & legal data, 14 owner photos, gallery
(5 categories, filters, keyboard lightbox, focus restoration, no-JS links),
breadcrumbs, contact tel:/mailto:, redirects, relative paths, static hosting.

## Validation (re-run after changes)
- Link/asset checker: 11 pages, 52 URLs — all pass.
- W3C Nu: all 11 pages 0 errors / 0 warnings.
- Firefox (BiDi): 10 pages × 5 viewports (1440/1024/820/390/360) — no overflow,
  images load, fonts load, single h1, nav intact; header/reveal/mobile-nav/
  gallery/lightbox/breadcrumb interactions pass; reduced-motion pass; 0 console
  errors. `file://` opening verified (fonts, fixed header, lightbox).
- Contrast: all text pairs ≥ 4.5:1 (WCAG AA).