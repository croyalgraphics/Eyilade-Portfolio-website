# Beans Central — expanded portfolio study

## Creative direction

**There’s more to beans.** Make the variety of West African bean dishes the central idea, then connect campaign, menu and takeaway applications through warm food photography, clear type and a limited palette.

The reference study informed the progression from a central idea to a complete visual system and applications. No reference logo, artwork, layout or photograph was copied. The specific shapes, copy, artwork compositions and application concepts in this extension were created for Beans Central.

## Original identity preserved

- Exact coloured logo and icon paths recovered from the PDF-compatible Illustrator file, without redrawing.
- Original red `#E0012E`, ochre `#DB8A1F`, brown `#2D120E`; warm paper added as a supporting neutral.
- Fredoka display and Quicksand body retained in the artwork. All SVG text is outlined for portability; only licensed Fredoka is embedded as a webfont.
- All six genuine embedded food images recovered: Honey Akara, Beans Porridge, Ewa Agoyin, Rice and Beans, Waakye, Moi Moi. Source food resolution ranges from 445–1029px; these are not represented as new high-resolution photographs.
- Original supplied source files remain untouched. The older campaign artwork is retained locally.

## New work

- Six individual dish campaign posters, with different compositions and shared brand signatures.
- Six-dish menu without invented prices, contact details, dietary claims or operational promises.
- Ingredient illustration and plate-line graphic language.
- Typography specimen.
- Bowl sleeve, carton panel, seal and tissue artwork.
- Carrier face artwork and carry-bag visualisation.
- Packaging family visualisation.
- Two vertical digital story compositions.
- Hero food campaign composition, dedicated carousel cover and a plain photographic scene.
- Website dish sequence with manual selection, play/pause, offscreen suspension and shared motion preference support.

Fourteen portable SVG masters plus three photographic visualisations are retained in `dist/assets/beans-central/`. PNG masters and generation originals are local under `artwork/beans-central/`, which is intentionally excluded from Git. SVG lettering is vector outlines, not live editable text. Embedded food photographs remain raster images.

## Honesty and scope

New applications are portfolio concepts, not evidence of manufactured packaging, an operating restaurant, a commissioned rollout, client approval or commercial results. Photographic mockups are AI-assisted and labelled on the case study. Their printing, materials and food detail are conceptual; the flat vector artwork is the authoritative design reference.

Only Beans Central’s case study and thumbnail were changed. The Works landing layout and the other project content were retained. The previously requested removal of Birthday Motion and On Paper remains a separate pending content decision in the development plan.

The default canonical origin was corrected to the existing Site’s currently returned public URL. This is metadata only; the Site audience was preserved.

## Files and reproducibility

- `scripts/create-beans-artwork.py`: builds outlined SVG masters, PNG review masters, responsive WebP exports and transparent food cutouts from local originals.
- `scripts/beans-case-study.mjs`: project-specific case-study composition.
- `src/beans-central.css`: styles scoped to this project.
- `src/beans-central.js`: the dish sequence.
- `dist/assets/beans-central/artwork-manifest.json`: artwork dimensions, palette and dish list.
- `dist/assets/beans-central/FONT-LICENSE.txt`: Fredoka copyright and full SIL OFL 1.1 text.

Art production requires local source files plus Python, Pillow, fontTools, Brotli and PyMuPDF. Normal website build and deployment use the committed prepared assets and do not need those tools or original files. No new browser runtime dependency or remote font request was added.

## Verification

- Website build: PASS. Sixteen HTML pages generated, including the new case study.
- Internal reference and asset checks: PASS, 657 references plus every responsive export in the new artwork manifest.
- Existing automated interaction tests: PASS, 9/9.
- Original vector equality: PASS. The two published logo/icon SVG files are byte-identical to their recovered source exports.
- Other case-study bodies: PASS. All ten unrelated project bodies match the preceding committed version exactly. Shared canonical metadata updates are outside those bodies.
- Browser review: 320, 390, 800 and 1440px widths; no horizontal overflow in the case study. One/two/three-column artwork layouts adapt at the intended breakpoints.
- Artwork viewer: enlargement, next-image navigation, Escape closing and focus return checked.
- Dish sequence: all six choices, single selected state, automatic advancement and offscreen suspension checked.
- Global motion preference: automatic sequence disabled when motion is off; manual dish selection remains available. Reduced-motion styling follows the same existing site preference resolution.
- Dark mode: checked; original brand artwork retains its intended colours.
- Browser console: no warnings/errors captured in the reviewed flow.
- Works carousel: new dedicated near-square cover checked in place; logo/message remain visible.
- No Lighthouse score, real-device lab measurement or exhaustive assistive-technology audit is claimed.

Reviewed browser screenshots and the 14-master artwork ZIP are available locally in `output/beans-central/`. Publication follows the existing Sites source workflow and preserves the currently public audience.
