# Master redesign — implementation record

Authorised by the user on 21 October 2026: start implementation, use the new reference image and navigation/timeline recordings, use newly supplied brand assets, and correct the tool checklist to **six**.

## Direction and plan

Visual thesis: an illustration-led editorial Web CV, with BeachSound display lettering, Rubik text, warm neutral surfaces and #BF9724 as the signature gold.

Content plan: Home contains identity, About, five creative disciplines, thirteen chronological career records, four brands, six named tools, two strong Works/Logofolio entry points and contact. Galleries remain on their dedicated routes. Existing project pages and original source assets are preserved.

Interaction thesis: a travelling navigation pill; a restrained 2D character response; a horizontally browsable, scroll-responsive career rail on desktop with Earlier/Later controls, transforming into a vertical timeline on mobile; three seamless CSS logo rows moving left to right with accessible static alternatives.

1. Audit and map the actual Assets; inspect the references. Completed before implementation.
2. Prepare optimised media and font delivery; establish shared colour/type/spacing/motion tokens.
3. Rebuild Home, navigation, chronological timeline and career data.
4. Rebuild Logofolio around three same-direction rows; retain a complete nonmoving index.
5. Carry the design system through Works, About, contact and case-study routes.
6. Validate routes, content, interaction, accessibility and representative responsive layouts. Package and publish through the existing private Site workflow; preserve audience.

## Reference observations

- Hero reference: confident name at the left, a dominant central figure and a shorter introduction to the right. Adopt the hierarchy, using Eyilade’s actual art, fonts and palette.
- Navigation recording: a dark capsule moves smoothly between labels, with small text-motion feedback. Use one shared moving indicator, with focus and non-hover alternatives.
- Career recording: a horizontal dated rail advances between milestones using compact previous/next controls. Use native scrolling and explicit controls, keeping every date and role in the document; avoid hijacking vertical page scroll.

## Accepted content correction

Exactly six tools: Adobe Photoshop, Adobe Illustrator, Adobe InDesign, Adobe After Effects, Adobe Premiere Pro and Codex. Lightroom is supplied but is not included in this six-tool set.

## Boundaries

No character generation or rigging. The supplied full-pose and close-up images are 2D illustrations. No private software concepts or functionality are exposed. No invented company logos, job dates, claims or case-study outcomes. Concurrent roles and the separate Ferman entries remain separate. New career facts follow the user’s latest master brief.

## Implementation acceptance checklist

- [x] BeachSound display and Rubik body/UI typography use actual supplied fonts.
- [x] Signature gold, readable neutrals, coherent surfaces and interaction states.
- [x] New full-pose hero illustration; no old photo in personal portrait components.
- [x] Functional desktop, tablet and mobile navigation, with visible keyboard focus.
- [x] Home contains About, five disciplines, all thirteen career records and exactly six tools.
- [x] Four actual brand logos: PwC, Dabur, PZ Cussons and Sandtex use supplied artwork.
- [x] Home contains no embedded Works or Logofolio galleries.
- [x] Two conspicuous page-entry actions reach /work/ and /logofolio/.
- [x] Three Logofolio rows travel left to right with seamless stable duplication.
- [x] Motion-off/static, keyboard and touch alternatives work.
- [x] Existing case-study pages, contact and downloads remain functional.
- [x] Build and meaningful checks pass; actual browser verification recorded.

## Verification completed

- `npm run build` and `npm run check`: PASS. Sixteen HTML pages, 578 internal file references, 19 unique logo assets, supplied fonts, image dimensions, exact contact phone, chronology, tool set and privacy boundaries validated.
- HTTP HEAD checks: 94 distinct page/asset/download references, all successful locally.
- Browser review: Home at 320, 390, 601, 768, 901, 1024, 1280, 1440 and 1920 pixels; key secondary routes at 320, all eleven case studies and the 404 at 390. No document horizontal overflow observed. Full figure remains contained. BeachSound renders as the actual supplied typeface.
- Desktop career controls reached 13/13; Earlier/Later and the active-state progress are functional. Mobile shows all thirteen records in a vertical rail without horizontal scrolling. Concurrent roles and Ferman records remain separate; PwC stages share one employer grouping.
- Mobile native menu opens, labels remain visible, Escape closes it and restores focus. Keyboard character activation displays its brief greeting and announces it.
- Logofolio: three rows, positive (left-to-right) translation, linear timing; repeated group HTML exactly matches in each lane. Group widths exceed 1920px. No interactive elements in decorative clones. Pause/resume verified; motion-off disables animation and hides repeated copies. Still index contains all nineteen identities and seven verified project links.
- Works Motion filter returns exactly its one project. LizCraft viewer loads imagery, advances its live caption and restores trigger focus after Escape. Motion video reached readyState 4 without error. About and every preserved case-study route open without captured console errors/warnings.
- The OS reduced-motion branch is implemented in both preflight, CSS and JS; the equivalent site motion-off state was exercised. Browser controls do not expose OS preference emulation, so no claim of emulated system-setting testing is made.
- Shared JS: 9.3 KB / 3.1 KB gzip. Shared CSS: 38.1 KB / 8.7 KB gzip. New prepared artwork and fonts total 1.25 MB; full hero 1024-wide export is 178 KB. No Three.js runtime is requested. No Lighthouse or field Core Web Vitals score is claimed.

Evidence is retained locally under `output/master-redesign/`. Original artwork is unchanged; source-to-export mappings are in `docs/MASTER_ASSET_MAP.json`.

## Supplied PwC artwork update

The newly supplied `Assets/Career and skills/PwC_logo_rgb_colour_pos.svg` now appears in the brand section and all three PwC career stages. Its original colours and proportions are preserved; the optimised transparent WebP is 6,662 bytes. The original SVG is unchanged. The private publication remains an owner-only review version.

BeachSound was supplied by the owner with no accompanying licence document; provenance is recorded in the asset map. Rubik includes its supplied OFL. No new paid service was used.
