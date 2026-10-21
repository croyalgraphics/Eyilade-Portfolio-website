# Portfolio refinement — audit and implementation plan

Date: 21 October 2026

This refines the existing portfolio in place. All fifteen routes, eleven project records, original logo assets, curated downloads, and useful interactions are retained.

## Evidence reviewed

- Existing templates, shared CSS, page builder, interaction module and Three.js module.
- Desktop and phone previews of the homepage, work, about, logofolio and project pages.
- Supplied redesign brief, read in full.
- Supplied 6.75-second screen recording, opened and sampled at nine timestamps from 0 to 6.4 seconds.

The recording shows two horizontal rows of evenly spaced white logo tiles. The upper row travels left, the lower row travels right, with continuous, steady motion rather than individual slides or an orbit. Marks keep their proportions, while thin borders and consistent spacing make the presentation coherent. This rhythm will be adapted using original portfolio logos, rounded surfaces, pausable movement, touch access and full-size viewing.

## Why the first version feels disconnected

| Finding | Change |
| --- | --- |
| Sharp project frames, square dialogs, small button radii and isolated pill shapes use different material languages. | Introduce a shared radius scale, paper surfaces, borders and restrained shadows across pages. |
| Blue full-bleed rooms, lime strips, cream galleries and charcoal video blocks read as separate chapters without enough shared treatment. | Use a common warm base, consistent content widths and recurring softly tinted rounded panels. |
| The oversized name dominates the opening while the role and personal introduction are small. | Make a concise personal introduction and supplied portrait the primary composition. |
| The rotating cube competes with the person and work. | Delete its markup, scene styles, listeners and animation logic. |
| Decorative arrows are repeated through navigation, CTAs and thumbnails. | Remove decorative arrows; use shape, contrast, emphasis, press and focus feedback. Keep necessary image/gallery navigation understandable. |
| Different animation rhythms compete while basic button feedback is subtle. | Define calm reveal timing, responsive press states, a consistent spring-like emphasis and clear keyboard/touch feedback. |

## Assets and limits

The original sixteen logo artworks are available. The supplied recording is accessible and has been visually reviewed. Portraits and visual-design assets are available. No rigged `.glb`, `.gltf`, `.fbx`, `.blend`, animation clips or facial controls have been supplied for the requested caricature.

Use the existing portrait as an honest **2D fallback**: whole-image pointer tilt, focus/press feedback and a greeting bubble. Do not claim independent head movement, expressions, skeletal animation or a rig. The true character work remains pending a supplied model and inspection of its capabilities.

## Controlled implementation

1. **Design system:** shared type/spacing/radius/surface/motion tokens; consistent page widths and navigation; remove decorative arrows and the cube.
2. **Experience:** personal hero with reactive introductory words; purposeful portrait interaction; reference-led opposite-flow logo rows; preserve the optional spatial view and complete index; strengthen site-wide hover/press/focus behavior.
3. **QA:** verify routes, filters, image dialogs, logo browsing, motion controls and downloads; repeat relevant checks at 320, 390, 768 and 1440 px; confirm private software details remain excluded.

## Dependencies and risks

Keep the existing static site and separately bundled Three.js. Add no framework or rendering stack. Continuous rows must pause on intentional interaction and respect motion preferences. Repeated decorative logos must be hidden from assistive technology. Text must remain readable and fully available on touch. The portrait fallback must not be presented as a 3D model. Do not finalize character-expression claims until the asset is supplied.
