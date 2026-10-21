# Approved smooth hero character integration

Owner approval: proceed with the smooth v2 character, explicitly excluding blink.

Visual thesis: preserve the editorial name / figure / introduction composition, using the approved smooth illustration as the personal anchor.

Content plan: update only the Home character and its interaction affordances; retain CV, Works and Logofolio entry points and the rest of the Web CV.

Interaction thesis: restrained breathing at rest; a short wave on character activation; explicit thinking and thumbs-up reactions. Keyboard and touch use the same controls. Device/site reduced motion uses still poses. Playback stops offscreen and in hidden tabs; failed rendering retains an image fallback.

Only idle, wave, thinking and thumbs-up are allowed in public assets and playback configuration. No blink file, control or animation schedule is included. Earlier review packs remain local; originals are preserved.

Implementation: export optimised four-state WebP sprite atlases plus static responsive posters, with a lightweight timed 2D canvas player. Idle loads after the hero poster; gesture atlases load on demand. No WebGL, rig, external service, per-frame network requests or continuously running animation frame loop.

Validation will cover state selection, return to idle, pause/resume, static motion-off reactions, poster fallback, mobile/desktop composition, asset boundaries and production build.

## Verification

- Production build and `npm run check` pass: 16 pages and 578 internal references, four allowed character states, timing/geometry contracts and no blink in the public Home/runtime/character assets.
- Nine transparent WebP exports decode with the expected geometry: four 1536×1536 atlases, four 512×768 still poses and a 320×480 responsive idle poster. The four animations contain 24 approved source drawings in total.
- Breathing plays at rest. Keyboard activation of the character triggers wave; Think and Thumbs up select their correct states and gestures return to idle.
- Motion-off hides the canvas and uses the selected static pose. Turning motion on restarts breathing. Scrolling past the hero sets playback to stopped; returning to the hero resumes it.
- Browser review at 320, 390, 768, 1024 and 1440 pixels: no page horizontal overflow; controls retain 44px heights. Full figure remains visible. Works and the three-row Logofolio still open without captured console warnings/errors.
- Static image fallback remains in the document and holds layout if canvas or atlas loading is unavailable. Motion-off image behavior is exercised; network-failure injection and OS preference emulation were not available in the browser controls and are not claimed as tested.
- Initial responsive poster is 58KB at 512px; idle atlas is 331KB and starts after page load. Gesture atlases are 321–361KB each, loaded on demand. Shared main JS is 4.1KB gzip. No continuous animation-frame loop or third-party runtime request is added.

Browser evidence is retained in `output/hero-character/`. The existing owner-only Site audience is preserved for publication.
