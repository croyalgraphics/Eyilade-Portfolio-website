# Supplied asset additions — 22 October 2026

Prepared with `node scripts/prepare_oct22_assets.mjs` using local Sharp. No external artwork or services were used. All seven originals remain unchanged. Exports use lossless WebP, Lanczos downsampling only where required, and no enlargement of raster sources. Original colours and the cropped artwork's aspect ratio are retained. Metadata is stripped.

The transparent sources are cropped to alpha bounds with a 2% safety margin. The opaque Citypartner, Redot and Ferman sources use visually reviewed explicit crops; no background replacement or logo recreation is performed. Citypartner's supplied pale gradient and the white backgrounds of the two JPEGs remain. The NYSC SVG is locally rasterised at 144 DPI before cropping/export.

## Export record

Crop notation: left, top, width, height in decoded source pixels. NYSC source dimensions in the table are its default 72 DPI raster bounds; it is decoded at 144 DPI.

| Artwork | Source dimensions | Decoded crop | Export dimensions | Source / export bytes |
|---|---|---|---|---|
| Citypartner | 640 × 640 | 160, 138, 322, 358 | 322 × 358 | 19,492 / 58,964 |
| Redot Digital | 1080 × 1080 | 250, 237, 579, 605 | 383 × 400 | 55,244 / 34,816 |
| Ferman | 400 × 400 | 0, 62, 400, 275 | 400 × 275 | 12,250 / 25,304 |
| NYSC | 294 × 372 | 0, 0, 1176, 1488 | 316 × 400 | 21,724 / 43,034 |
| Carex | 3840 × 2160 | 0, 0, 3840, 2160 | 462 × 260 | 691,025 / 56,424 |
| IOSA Freight | 460 × 214 | 37, 2, 388, 210 | 388 × 210 | 31,991 / 19,416 |
| Canva | 1000 × 1000 | 0, 0, 1000, 1000 | 192 × 192 | 188,483 / 21,480 |

## Provenance and original SHA-256

All source files were supplied by the site owner under `Assets/Career and skills/`. This export records provenance, not a new grant of trademark rights.

- **Citypartner**: `Assets/Career and skills/Citypartner healthcare.webp` → `/assets/master/logo-citypartner.webp`
  - SHA-256: `17560b11c7cf28b8d5e9fa18a92398a37a5b25056965efd04c385a161f0193e1`
- **Redot Digital**: `Assets/Career and skills/Redot-Icon.jpg` → `/assets/master/logo-redot.webp`
  - SHA-256: `6b71cc61a1b6bbc796b8c8562c57bbb0781326021dbdc96b00966d3359929bbf`
- **Ferman**: `Assets/Career and skills/Ferman digital.jpeg` → `/assets/master/logo-ferman.webp`
  - SHA-256: `1e2bccec18cca03ac62ef420c261bde9859d1b30de077f5309db6601204505f6`
- **NYSC**: `Assets/Career and skills/NYSC_LOGO.svg` → `/assets/master/logo-nysc.webp`
  - SHA-256: `822482bccad90cc86cb89b2a32af7e4b5aceb7afb89f193d73587b1755805435`
- **Carex**: `Assets/Career and skills/Carex-Logo.png` → `/assets/master/brand-carex.webp`
  - SHA-256: `61b9385f000db33de3bf6b9b477db702e658a3d84d5764f2c7ea6882b24d30f0`
- **IOSA Freight**: `Assets/Career and skills/IOSA-logo-1.png` → `/assets/master/brand-iosa-freight.webp`
  - SHA-256: `07ce2b2c5c77c339f349e788331e36c533b8fa0229a5a350b9ac18d644ac2ba1`
- **Canva**: `Assets/Career and skills/canva-icon-logo.png` → `/assets/master/tool-canva.webp`
  - SHA-256: `5a4857b266f876eea54c240c17013fed3a7a678bd5204e994bc36630f4fdf8b3`

## Artwork observations

- The file `Ferman digital.jpeg` visibly spells **Feman Media Agency**. Its original lettering and artwork are preserved; the timeline label remains the approved career name Ferman. No spelling correction has been painted into the logo.
- IOSA artwork visibly reads **iosa FREIGHT LIMITED**. It is mapped to the owner-requested display name IOSA Freight.
- The supplied Ferman JPEG artwork touches its left and right image edges. The export keeps the entire original width and does not invent missing pixels.
- Carex is the supplied Cussons Carex lockup; it is an additional brand entry alongside the separate PZ Cussons corporate mark.
- Existing four brands and nine toolkit entries are retained, with Carex / IOSA Freight and Canva appended.
