# Master brief — asset audit and proposed implementation plan

Date: 21 October 2026

Source: [Eyilade master brief](</Users/joshuaoridamisi/Desktop/Eyilade_Portfolio_UI_UX_Redesign_Master_Brief.md>).

**Status:** preparation only. The website implementation remains unchanged. The previous explicit instruction was to defer implementation; confirmation is needed to replace that hold with this redesign scope. The brief’s own execution instruction is recorded as requested scope, not used by itself as permission to resume changes or publish.

## Direction

**Visual thesis:** a warm, editorial Web CV built around the supplied full-length illustration, expressive BeachSound headlines, readable Rubik detail, and a controlled gold signature (`#BF9724`).

**Content plan:** personal hero → About and disciplines → chronological experience → brands → tools → two animated dedicated-page entry points → contact. Home contains no project gallery and no logo gallery. Existing Work, Logofolio, About and case-study URLs remain functional.

**Interaction thesis:** a restrained 2D illustration response; an accessible timeline with scroll progression and expandable detail; three seamless CSS logo rows moving left to right on the dedicated Logofolio page. All content remains available without continuous motion. Character generation and rigging stay paused.

## What was inspected

- Current static HTML/CSS/JavaScript architecture, builder, project routes, package declarations and saved deep review.
- `Assets` recursively: **87 files**, excluding `.DS_Store`.
- Raster metadata for all supplied PNG/JPEG/WebP files.
- Full-pose illustration and a contact sheet of the close-up, brand and tool assets were visually inspected.
- BeachSound font name table and embedding metadata were read. No font file was renamed or substituted.

This is an initial mapping. Similar logo variants will receive a visual comparison before choosing final exports. Originals have not been edited.

## Illustration mapping

| Use | Actual source | Notes |
| --- | --- | --- |
| Home hero | `Assets/Eyilade illustration(full pose view).png` | 1024 × 1536, RGBA with real transparency. Full figure, including shoes, is present. Use `contain`/intrinsic proportions; preserve head and feet. |
| About/compact identity | `Assets/Eyilade illustration (close-up view).png` | 1254 × 1254, RGBA with transparency. Use this instead of the old photograph where a compact portrait is appropriate. |

These are **2D illustrations**. Pointer movement, a short tap/key reaction and a graceful return to rest can be implemented without pretending that the image is a rigged model. Prefer a lightweight CSS enhancement; a static image remains the fallback. No `.glb`, articulated pose, facial rig or new 3D generation is proposed in this phase.

## Fonts

| Typeface | Actual source | Availability |
| --- | --- | --- |
| BeachSound | `Assets/Fonts/BeachSound.otf` | Present. Internal family is “Beach Sound”; PostScript name is “BeachSound”; designer metadata is “Ikiikowrk”. No licence document was found beside it. Embedding flags are zero, which does not establish the scope of a webfont licence. Confirm that separately before public publication. |
| Rubik | `Assets/Fonts/Rubik/Rubik-VariableFont_wght.ttf` | Present, with `OFL.txt` and `README.txt`. |
| Rubik italic | `Assets/Fonts/Rubik/Rubik-Italic-VariableFont_wght.ttf` | Present. Use only if needed; avoid loading every static font file. |

The display font is available, so there is no reason to silently label another font as BeachSound. Typography export/optimisation should preserve the supplied originals and the required punctuation and character set.

## Brand and tool coverage

### Required brand strip

| Required brand | Source found in `Assets` |
| --- | --- |
| Dabur | `Assets/Career and skills/Dabur_Logo.svg.webp` |
| PZ Cussons | `Assets/Career and skills/PZ_Cussons_logo.svg.webp` |
| PwC | **No identifiable logo file found in `Assets`.** |
| Sandtex | **No identifiable logo file found in `Assets`.** |

Use the supplied relationship wording: work completed directly and through a marketing agency. A brand-strip logo must not imply employment by every brand.

### Explicitly named tools

| Tool named in brief | Source found |
| --- | --- |
| Photoshop | `Assets/Career and skills/Adobe_Photoshop_CC_icon.svg.webp` |
| Illustrator | `Assets/Career and skills/Adobe_Illustrator_CC_icon.svg.webp` |
| InDesign | `Assets/Career and skills/Adobe_InDesign_CC_icon.svg.webp` |
| After Effects | `Assets/Career and skills/Adobe_After_Effects_CC_icon.svg.webp` |
| Premiere Pro | **No identifiable icon found in `Assets`.** |
| Codex | `Assets/Career and skills/codex-logo.png` |

An additional Lightroom icon exists: `Assets/Career and skills/Adobe_Photoshop_Lightroom_CC_logo.svg.webp`.

**Content ambiguity:** the tool table names **six** tools, while the acceptance checklist requires **eight**. Lightroom is available as an additional asset but is not in the named table. Confirm the intended final tool list rather than inventing two capabilities or silently counting Lightroom as specified.

### Timeline marks

CRG artwork is available in `Assets/CRG logos/`; the Intelligentsia Orb mark is available as `Assets/Intelligentsial orb.png`.

No dedicated, identifiable employer marks were found for Running Jack, Citypartner, either Ferman entry, MaxyStuff, Redot, or PwC. No specific NYSC/Federal Government mark was supplied. These are coverage gaps, not permission to fabricate company logos. Accurate organisation text can remain useful if a logo is unavailable, subject to the final presentation decision.

## Logofolio replacement map

Each row below identifies an actual candidate source. Final optical sizing and variant selection require comparison; brand colours and aspect ratios must remain intact.

| Existing identity | New source candidate |
| --- | --- |
| Agrohub | `Assets/Agrohub investment/Agrohub investment main logo.png` |
| Beans Central | `Assets/Beans Cental Logo/Beans Cental Logo.png` |
| ClenStreet | `Assets/ClenStreet/Main logo.svg` / `Assets/ClenStreet/Logo 2.svg` |
| Doc’s Apothecary | `Assets/Doc's Apothecary.png` |
| Efame | `Assets/Efame real estate.png` |
| Feasts & Flavours | `Assets/Feast and flavours/Feast and flavours Full colored logo.png` |
| Genesis Orb | `Assets/Genesis Orb/Genesis orb Logo 1.png` / `Genesis orb  Logo 2.png` |
| Intelligentsia Orb | `Assets/Intelligentsial orb.png` |
| Lecco Inn | `Assets/Lecco Inn/Lecco Inn Logo 1.png` / `Lecco Inn Logo 2.png` |
| LizCraft | `Assets/Lizcraft/LizCraft Logo 1.png` / `LizCraft Logo 2.png` |
| LizInterior | `Assets/LizInterior/Liz Interior Main Logo.png` |
| PPCL | `Assets/PPCL Logo.svg` / `Assets/PPCL logo.png` |
| Pure Hive Honey | `Assets/Pure Hive Honey.png` |
| Rebeks Savour | `Assets/Rebeks savour.png` |
| Swift Tern | `Assets/Swift tern/Swift Tern Logo.png` |
| Natoral | `Assets/Natoral/Natoral Logo 1.png` / `Natoral Logo 2.png` |

Additional identity families are supplied for **CRG**, **PrimeFits** and **Yoma**. If the new asset collection is intended as the full logofolio, these bring it to **19 identity families**; variants should not be counted as separate brands. The existing checker’s hard-coded count of sixteen will need to be replaced by a content-derived check when the set is confirmed.

New work media also exists for Feasts & Flavours, the LizCraft bag and Swift Tern. Retain valid existing case-study media unless the corresponding new file supersedes it. A new logo is not automatically a replacement for a project’s product mockup.

**Delivery concern:** some logo files are 10,222–14,223 pixels across; the largest inspected raster exceeds 202 million pixels. Their small compressed file sizes do not make them safe choices for direct browser delivery. Export appropriately sized, crisp web derivatives and preserve the originals. Do not copy the 191 MB PSD into public assets.

## Proposed phased implementation

### 1. Content and asset reconciliation

- Resolve the six-versus-eight tool list, missing required brand/tool marks, and BeachSound licence provenance.
- Visually compare similarly named logo variants; record a canonical file per identity.
- Prepare optimised illustration, logo, icon and selected work derivatives without modifying source assets.
- Store the 13 supplied career entries as structured data. Preserve concurrent roles, the separate Ferman entries, and all three PwC stages. Keep missing details out of the public UI.

### 2. Shared design system and navigation

- Replace the current Manrope/Instrument system with BeachSound/Rubik.
- Introduce neutral/gold tokens, accessible darker accent tones, a coherent type/spacing scale and readable metadata.
- Apply the system across existing routes, including case studies and dialogs.
- Make Home, Works, Logofolio and Contact destinations clear. Retain the About route as useful existing content; do not break bookmarks.
- Correct the audited mobile focus issue and provide resilient navigation with short, predictable transitions.

### 3. Home as an interactive Web CV

- Remove the featured project grid and logo-flow preview from Home.
- Build the full-figure illustration-led introduction with clear name and discipline hierarchy.
- Add substantive About/skills, chronological experience, brands and tool sections.
- Present all 13 career records in ascending order from 2016 to Present, with an accessible single-column mobile timeline and optional detail disclosures.
- Add two conspicuous animated page-entry actions for the existing `/work/` and `/logofolio/` routes.
- Add the supplied phone, email and professional-profile links with accurate accessible labels. No email or other message will be sent.

### 4. Dedicated Logofolio

- Render exactly three CSS-driven rows, all moving left to right.
- Finalise each row’s sequence once per initialisation, then duplicate that exact sequence for a seamless loop.
- Use distinct offsets and modest speed differences; keep translation linear and secondary interactions eased.
- Make duplicates decorative without duplicate focus targets. Resolve manual and automatic pause states coherently.
- Provide a complete nonmoving presentation for reduced motion, keyboard and low-power use.
- Use existing project destinations where relevant; do not fabricate pages for logo-only work. Avoid forcing a modal just to see the logos.

### 5. Works and existing route integration

- Preserve project text, valid gallery assets, native viewing controls and route structure.
- Replace outdated standalone logo assets with the mapped new originals where relevant.
- Carry through the new typography, neutral/gold UI, accessible interaction states and required readability improvements.
- Retain independent-study labels and the boundary around private product concepts.

### 6. Verification and handoff

- Run the existing production build and relevant checks, updated for the agreed content set.
- Review mobile 320–390 px, tablet 768–1024 px, desktop 1280–1920 px and important intermediate widths.
- Verify all 13 career records, no Home galleries, two working dedicated-page entry points, three correctly moving logo rows, reduced-motion/static access, keyboard/touch states, contacts and downloads.
- Check seams after image loading and resizing, absent/failed media states, image proportions, console errors and document overflow.
- Report actual measurements and limitations; do not claim unmeasured Core Web Vitals or a live public URL.
- No publication or audience change occurs during this preparation. Any subsequent release must follow the confirmed scope and existing hosting workflow.

## Clarifications needed

1. Does this master brief now replace the previous instruction to defer implementation?
2. Which tool names should satisfy the checklist’s total of eight? Six are explicitly listed; Lightroom is additionally available.
3. How should the missing PwC, Sandtex and Premiere Pro assets be supplied or sourced? None was found under the current `Assets` tree. No stand-in has been inserted.
4. Confirm BeachSound webfont licence coverage before public publication; the font file is present, but no associated licence document was found.

## Local review evidence

- [Raster metadata](</Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/master-brief-review/image-metadata.json>)
- [Illustration, brand and tool contact sheet](</Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/master-brief-review/asset-contact-sheet.jpg>)
- [Existing deep review](</Users/joshuaoridamisi/projects/Joshua Portfolio Website/docs/WEBSITE_DEEP_REVIEW_2026-10-21.md>)
