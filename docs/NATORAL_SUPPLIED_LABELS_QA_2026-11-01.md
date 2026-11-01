# Natoral supplied-label revision — validation

## Implemented

All eight designer-supplied N1–N8 PNGs replace earlier generated packaging in the active Natoral case study. The project includes 23 compositions: supplied-product boards, category photography, an eight-product hero, range architecture, a product close-up, family and fitness scenes, campaign posters, dispatch material, digital compositions and original identity context. Six new product-free photographic scene plates were generated with the built-in image tool. Exact prompts are recorded in NATORAL_SCENE_BRIEFS_2026-11-01.json.

Original label images are embedded directly in native SVG layouts. They are uniformly scaled and clipped to a product viewport; lettering is never regenerated. Previous generated-label explorations and the first artwork delivery remain preserved outside the active page. New responsive exports use a dedicated natoral-supplied asset directory and content hashes in their URLs.

## Evidence

- Eight supplied originals match their Desktop inputs byte-for-byte; original hashes are in the artwork manifest.
- 43 native PNG embeddings match one of those eight source hashes. Every supplied master is represented.
- 23 native compositions with PNG previews and three responsive WebP sizes each; the hero can open in the artwork viewer.
- 13 unrelated HTML pages match the opening commit byte-for-byte. The Works listing changes only its Natoral cover revision.
- `npm run build`: 15 routes plus 404, seven career records, ten toolkit entries, 19 identities.
- `npm run check`: metadata, dimensions, internal references, supplied-image hashes and absence of superseded packaging URLs pass.
- `npm test`: 14 tests pass, including range/view preservation and shared interaction regressions.
- Browser checks at 320×568, 390×844, 820×1180 and 1440×900: no horizontal overflow or broken loaded images.
- Range selection preserves Supplied packaging mode; Photography can be restored. Lightbox opens the correct asset, advances, closes with Escape and restores focus. Motion toggle works.
- Hero changed to contain its complete image rather than cropping the lower labels.

## Scope and limits

This validates the portfolio presentation and supplied-file fidelity. It does not verify the ingredient, age, nutrition, benefit or testing statements printed on the supplied labels. The website identifies them as supplied artwork and describes surrounding scenes as fictional AI-assisted visualisations. Native SVG compositions are editable layouts, not production dielines. Site publication and GitHub synchronization receipts are retained separately under output/natoral-supplied.
