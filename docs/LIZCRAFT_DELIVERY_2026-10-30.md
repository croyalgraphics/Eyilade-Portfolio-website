# LizCraft — expanded portfolio study

## The direction

**A little time. A lot of care.** The wider identity follows making, wearing and keeping a handmade piece. It develops the original maker’s personal thank-you message into a practical, tactile system rather than treating the logo as decoration.

The supplied Behance library was revisited, especially ANAHÍ, HREHEN, Crochê Ternura, MARROW and The Common Thread Club. The specific lessons were useful care information, the physical scale of tags and labels, varied pattern density, close material photography and a coherent campaign voice. Reference imagery, logos, slogans, artwork and layouts were not used as deliverables.

## Source fidelity

- Exact original horizontal/vertical signatures, icon and contour paths recovered from LizCraft.ai.
- Blue `#065784` and gold `#D2A857` retained; ivory paper added as a supporting surface.
- Fraunces retained for display type. Licensed Rubik supports new information layouts; the original guide’s SF Compact is documented locally and not redistributed.
- Reversed marks use the original monochrome compound paths, preserving the L knockouts.
- Original thank-you wording retained and signed LizCraft, matching the AI source. An earlier PNG export signed Opeyemi Elizabeth remains separate and unchanged locally.
- All five original care instructions retained: Hand wash gently; Use mild soap; Do not bleach; Do not machine wash; Do not iron.
- Original supplied bag and thank-you artwork remain visible as the starting work.
- No confirmed original product photography was found. Downloaded moodboard pictures and photographs featuring other brands were excluded from the new work.

## New artwork

Fifteen portable SVG compositions, each with a PNG master and responsive WebP exports:

1. Signature and palette study.
2. Fraunces type study.
3. Contour scale/density study.
4. Thank-you front.
5. Thank-you back with original personal message.
6. Five-instruction care foldout.
7. Contour-shaped hangtag pair.
8. Woven-label and small-format signature artwork.
9. Tissue, seal and parcel-band artwork.
10. Carrier artwork.
11. Making campaign.
12. Wearing campaign.
13. Care campaign.
14. Digital stories.
15. Dedicated portfolio carousel cover.

Five AI-assisted visualisations: making, wearing, woven-label detail, wrapped parcel and opened parcel. The two parcel images are related states of the same concept scene. Generated printing may contain small differences; flat vector artwork is the authoritative graphic design reference.

New garments, printed materials and packaging are **portfolio concepts**, not evidence of manufactured products, an actual production rollout, client approval, sales results or real customers. The model is fictional, and no founder identity or biography was invented. No collection names, prices, certifications, fibre labels or environmental claims were added.

## Website experience

- A project-specific, responsive editorial sequence with the exact signature and making image in the opening.
- Human imagery and an excerpt from the original maker’s note.
- Eight actual contour paths revealed through scroll, with keyboard-operable layer control, replay and pause.
- Wrapped/opened parcel controls with explicit selected state and an accessible status message.
- Original source pieces distinguished from the new concepts.
- Enlarged artwork through the shared viewer; readable care instructions also available as page text.
- Global motion preference, reduced-motion resolution, offscreen/hidden-page suspension and dark framing retained. Brand artwork keeps its intended colours.

Only LizCraft’s case study and its own carousel cover/content metadata were changed. The Works landing composition, Beans Central and the other project bodies remain unchanged.

## Deliverables and reproducibility

- `scripts/create-lizcraft-artwork.py` prepares original SVG/PNG compositions, outlined lettering, responsive exports, exact source identity copies and licensed font subsets.
- `scripts/lizcraft-case-study.mjs` composes the project-specific case study.
- `src/lizcraft.css` and `src/lizcraft.js` contain scoped styling and interactions.
- `dist/assets/lizcraft/artwork-manifest.json` records dimensions, palette and care text.
- `dist/assets/lizcraft/FONT-LICENSE.txt` contains Fraunces copyright and the full SIL OFL 1.1 text.
- Local originals, extraction records, photos and PNG masters remain under `artwork/lizcraft/`; prepared web assets are tracked.
- The local ZIP in `output/lizcraft/` includes all fifteen SVG masters, PNG previews, five visualisations and exact original identity vectors. Text in SVG masters is outlined, not live editable type; photography remains embedded raster content.

Normal website builds consume the prepared, committed assets. Art regeneration additionally needs the supplied local files, Python, Pillow, fontTools, Brotli and PyMuPDF. No new browser runtime dependency, external font request, paid service or additional plugin was introduced.

## Verification

- Build, internal references and responsive asset checks pass.
- Ten automated tests pass, including the new contour bounds/reading-order test and the existing character, carousel, career, preference and navigation checks.
- Responsive browser review at 320, 390, 768 and 1440px: no horizontal page overflow.
- All eight actual contour paths render. Manual selection, replay completion, pause stability and motion-off behavior reviewed.
- Both parcel states, single selected control, image enlargement, next-image navigation and Escape closing reviewed.
- New photography loads; no broken project images found in the reviewed flow.
- Final four-width review also confirms contour controls remain within bounds and exactly one parcel frame is visible.
- Dedicated LizCraft cover reviewed in the existing Works carousel.
- Browser console: no warnings/errors captured in the reviewed flow.
- Dark framing reviewed while brand canvas colours stay intact.
- Independent asset review: original logo/contour paths and message/care fidelity pass. Two findings were fixed: safe margin on the gold tag and valid namespaces in all masters. All fifteen final SVG masters pass strict XML parsing.
- Originals remain unchanged, and published identity copies are checked byte-for-byte against recovered originals.

No Lighthouse score, real-device lab measurement, exhaustive accessibility audit or human/client approval is claimed. Native publication and GitHub source synchronization are verified separately during release; the receipt is kept under `output/lizcraft/`.
