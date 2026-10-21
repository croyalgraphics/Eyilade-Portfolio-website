# Eyilade Oridamisi Portfolio — Deep Website Review

**Date:** 21 October 2026 · Africa/Lagos  
**Review target:** the current local build at `http://127.0.0.1:4173/`  
**Status:** audit and recommendations only. No website changes, rebuild, deployment, or access changes were made during this review. Character modelling and rigging remain paused.

## Executive assessment

The site now has a coherent visual foundation: warm paper, cobalt type, rounded frames, a real personal portrait, and artwork that carries the colour. Its static architecture is lean, the cube and decorative arrows are gone, and the flowing logofolio is closer to the supplied recording.

The next improvement should be **greater clarity and stronger evidence of your design thinking**, supported by more predictable interactions. Adding more animation everywhere would not solve the main weaknesses. A recruiter needs to understand your contribution quickly; a client needs to recognise the kind of problem you can solve. The current pages show attractive outputs more clearly than they demonstrate those two things.

The site is a strong local prototype, but it is **not yet a verified public portfolio**. Sites currently reports zero saved versions, no live URL, and a restricted `custom` audience. This is a launch-readiness observation, not a request to publish or change access.

### Highest-value next steps

| Priority | Improvement | Why it matters |
| --- | --- | --- |
| P1 | Make mobile keyboard focus visible | The focus outline is the same blue as the menu background. |
| P1 | Increase essential small text | Several mobile labels are 6–9 px; fitting the viewport is not the same as being comfortably readable. |
| P1 | Add verified role, context and decisions to flagship case studies | The work needs to demonstrate authorship and judgement to clients and recruiters. |
| P1 | Complete production measurements and public-link validation before sharing | Local checks cannot establish real internet speed, deployed headers, or visitor access. |
| P2 | Reconcile explicit pause/resume with automatic hover/focus pausing | “Resume” currently changes the control state while the rows remain paused. |
| P2 | Improve artwork inspection and accessible alternatives | Print details are difficult to inspect on phones; both downloadable PDFs are untagged. |

**Priority key:** P1 = resolve before broad client/recruiter sharing; P2 = significant usability, quality or hardening improvement; P3 = optional refinement. No P0 critical vulnerability was established. Priorities describe practical importance, not a formal compliance certification.

**Evidence key:** Confirmed = reproduced or directly measured; Source-confirmed = present in code/output; Design judgement = a recommendation, not a defect; Unverified = requires a different device, deployed environment, or owner confirmation. Effort is relative: S = targeted change, M = component/page work, L = substantial content or release work.

## Scope, method and limits

- Reviewed all page templates, shared CSS/JavaScript, the page builder, project and logo data, local server, generated metadata/headers, dependency declarations, and existing checks.
- Ran the existing check successfully: **16 HTML documents, 536 internal references, 16 distinct original logo assets**.
- Requested **125 distinct internal page/asset targets**, including responsive image candidates and optional module/data files: all returned HTTP 200. A deliberately missing route returned a real HTTP 404 and the custom error page.
- Found no missing same-page anchors or duplicate IDs in the generated documents.
- Decoded **108 WebP files** without image-decoding errors.
- Checked six representative routes at **320 × 740, 390 × 844, 768 × 1024, and 1440 × 900**: homepage, work index, About, logofolio, LizCraft case study, and birthday-motion case study. Checked the other nine project routes at 320 px. This is **33 page/viewport combinations**. No document-width overflow or overflow in the inspected major layout groups was found.
- Exercised all work filters, logo index, 2D image viewer, next-image navigation, Escape/return focus, motion-off persistence, mobile menu, and About disclosures. No console errors were captured in this audit tab.
- Checked the public Behance destination in the browser. LinkedIn presented an authentication wall; profile ownership/content could not be verified.
- Reviewed the optional spatial module **in source only**. Its runtime was not activated while 3D work is paused.
- `npm audit` reported **zero known vulnerabilities** for the current lockfile. Recognisable credential-pattern scanning found no matches in the inspected source/content/generated text files. Public PDF text checks found no matches for the protected project terms checked by the build policy. These are bounded checks, not proof that every possible secret or confidential detail is absent.

**Not measured:** Lighthouse scores, a performance trace, field Core Web Vitals, cold-load internet timings, CPU-throttled performance, actual GPU memory, physical-device touch behaviour, screen-reader output, browser zoom/text resizing, or deployed security headers. No compatible trace tool was available in this review workflow. Do not interpret a quick localhost preview as a production speed score.

## What should be preserved

- Actual portfolio artwork is the main visual material; it has not been replaced by generic decorative imagery.
- Two typefaces and shared spacing/radius tokens establish a recognisable system.
- Static HTML, self-hosted runtime assets, a small shared script, and an optional dynamically imported spatial bundle are good architectural choices.
- The complete 16-mark index provides an alternative to movement. Global motion-off persists across reloads and removes duplicated flow groups from display.
- Main action controls generally have generous padding/minimum heights. This review did not establish a general touch-target-size failure.
- Semantic buttons, named navigation, a skip link, one H1 per page, image dimensions, and native dialogs provide a useful accessibility foundation.
- The site uses direct email links and supplies a copy-address option rather than pretending to submit an unconnected contact form.
- External links use `noopener noreferrer`. There are no third-party tracking/runtime scripts in the inspected build.
- No invented awards, testimonials, business results, or client metrics are needed to improve the presentation.

## 1. UI, art direction and content hierarchy

### UI-01 — Essential small text needs a readable floor

**P1 · Confirmed · Effort M**

At 390 and 320 px, the computed sizes include: motion control **8 px**, hero name/role **8 px**, portrait footnote **7 px**, discipline strip **6 px**, project type **8 px**, logofolio eyebrow **7 px**, and footer text **7 px**. The result is elegant at a glance but asks visitors to work too hard to read supporting information.

**Recommendation:** establish separate minimum sizes for body copy, controls and metadata. As a design starting point, use approximately 15–17 px body text, 12–14 px essential labels, and 11–12 px restrained secondary metadata; refine by visual testing rather than treating these as WCAG-mandated sizes. Reduce copy or adjust layout before shrinking important information.

**Acceptance:** essential controls and project information remain comfortably readable at normal phone zoom, and enlarged text is checked separately. Evidence: [mobile CSS][css-mobile], [responsive measurements][responsive-data].

### UI-02 — Make the personal positioning more specific

**P2 · Design judgement · Effort M**

“A curious mind. A little character. A considered touch.” has personality, but it could introduce many designers. Your full name is confined to a small eyebrow, and the strongest differentiators—senior professional experience, visual systems, and a Computer Science foundation—appear later.

**Recommendation:** lead with a clearer personal statement that connects your name, specialism and value. Keep the warmth and serif character, while allowing visitors to understand who you are within a few seconds. Mention verified professional context briefly; avoid adding badges or an unsupported availability claim.

**Acceptance:** someone who sees only the first screen can identify you, describe your primary design offer, and find the work. Evidence: [hero copy and composition][hero].

### UI-03 — Adapt the hero to tall tablet screens

**P2 · Confirmed layout; design judgement about improvement · Effort S–M**

At 768 × 1024, the hero fills the viewport. The portrait begins around **335 px** and the introduction around **352 px**, leaving a large quiet area below the header. There is no clipping, but the composition feels less purposeful than the desktop and phone versions, and work is pushed out of the first screen.

**Recommendation:** tune height and vertical alignment by aspect ratio, not width alone. Consider a shorter tablet hero or a visible beginning of the selected-work section. Preserve breathing room without centring the whole introduction in a large empty field.

**Acceptance:** portrait and text feel intentionally placed on portrait tablets and short landscape screens. Evidence: [tablet screenshot][tablet-image], [hero layout rules][css-hero].

### UI-04 — Give the visual language one more unmistakably personal detail

**P3 · Design judgement · Effort M**

The paper/cobalt palette and rounded frames are coherent, but repeated oversized italic headings, pill controls and generic phrases can still feel familiar. The same LizCraft packaging also appears in the selected work and the About preview, where it adds less new information.

**Recommendation:** introduce one restrained motif drawn from your own design process or supplied graphic work—for example a considered contour reveal or typographic annotation—and use it at a few meaningful moments. Replace redundant imagery with a genuine process detail if available. Keep original logos intact and avoid unrelated floating objects.

**Acceptance:** the site is recognisable without depending on a generic animated ornament. This is an authorship opportunity, not a reason to add more visual noise. Evidence: [homepage sections][hero], [shared styling][css-system].

## 2. UX, navigation and recruiter/client journeys

### UX-01 — Flagship case studies need stronger evidence of contribution

**P1 · Source-confirmed; editorial recommendation · Effort L, with owner input**

Project pages currently explain the visual language and show finished artwork. Their structured facts are mainly “Design focus” and “By”. The data has no dedicated fields for date, role, collaborators, brief, constraints, process evidence or verified outcome. “By Eyilade” alone cannot explain the boundary of an agency contribution.

**Recommendation:** deepen three or four flagship projects first. Add a short brief, your precise role, constraints, two or three meaningful decisions, and supplied sketches/iterations where appropriate. Distinguish commissioned, agency, personal and concept work. Include outcomes only when evidence exists; qualitative completion facts are sufficient.

**Acceptance:** each flagship tells a compact problem → decision → execution story, with accurate attribution. Evidence: [project records][projects], [case-study generator][case-build].

### UX-02 — Explain grouped collections and preserve the visitor’s place

**P2 · Source-confirmed · Effort M**

“On paper” and “In the feed” group several executions under one project, while identity pages are individual brands. The index and next-project link treat both types similarly. Filters work, but selection is not encoded in the URL; a reload returns to the default collection.

**Recommendation:** identify collections clearly, give individual images useful captions, and make the selected-work order an explicit editorial choice. Consider shareable category state and restoring the visitor’s context when returning from a case study. Do not split every execution into a new page merely to increase the project count.

**Acceptance:** visitors understand what each entry contains and can return to the same browsing context. Evidence: [project records][projects], [filter handling][filters].

### UX-03 — Mobile navigation needs a no-JavaScript fallback

**P2 · Source-confirmed; not fault-injected in browser · Effort S–M**

Below the mobile breakpoint the desktop navigation is hidden. The mobile navigation starts with `hidden` and relies on JavaScript to open. If the interaction script fails or is disabled, the Menu control cannot reveal it. Some pages retain useful body links, but that does not replace consistent main navigation.

**Recommendation:** keep a usable navigation path before JavaScript enhancement, or provide a deliberate no-script fallback. A script failure should reduce polish, not strand the visitor.

**Acceptance:** Work, Logofolio, About and Contact remain reachable on a phone when the main script does not execute. Evidence: [header generator][header-build], [menu script][menu-script], [mobile CSS][css-mobile].

### UX-04 — Surface practical recruiter information earlier

**P2 · Design judgement · Effort S–M**

The CV and portfolio download live in the footer, while the About page also offers the CV. Contact paths are clear once reached, but practical hiring information is less prominent than the expressive headings.

**Recommendation:** add a restrained CV link near the About introduction or main work summary; keep project and hiring contact paths distinct. If desired, state verified work preferences or availability in plain text. Preserve the visible email address as a fallback for visitors without a configured mail client.

**Acceptance:** a recruiter can quickly find experience, CV and contact without traversing the entire site. Evidence: [About content][about], [footer generator][footer-build].

## 3. Animation, logofolio and slideshow behaviour

### MOT-01 — “Resume flow” does not describe the effective movement state

**P2 · Confirmed · Effort S–M**

Reproduction: select Pause flow, then Resume flow while focus remains on that control. `aria-pressed` becomes `false`, but both tracks still have `animation-play-state: paused` because the flow component contains focus. Clicking the heading outside the component returns both tracks to `running`.

Automatic pausing around keyboard interaction is useful. The problem is the mismatch between the explicit control and the effective state.

**Recommendation:** define the precedence of manual pause, focus, hover, hidden-tab state and reduced motion. Either communicate temporary focus/hover pausing, or design the resume action so it behaves predictably without sacrificing safe keyboard access.

**Acceptance:** button state, wording and visible movement agree for pointer and keyboard users. Evidence: [flow CSS][css-flow], [pause handler][flow-script], [interaction record][interaction-data]. W3C recommends understandable user control over carousel movement: [carousel guidance](https://www.w3.org/WAI/tutorials/carousels/).

### MOT-02 — Make the motion preference internally consistent

**P2 · Source-confirmed · Effort M**

JavaScript can restore a saved “on” preference while CSS still forcibly disables animation under `prefers-reduced-motion: reduce`. The label can therefore say “Motion on” while the CSS rows remain still. The optional spatial module follows the JavaScript state, which would create another policy difference when that work resumes. Saved motion-off is also applied after the page’s CSS entrance can begin.

**Recommendation:** define one documented policy for device preference and explicit visitor choice. A “Use device setting / On / Off” model is one option. Apply a saved reduced-motion choice before animated first paint, and keep all renderers aligned with it.

**Acceptance:** label, CSS, entrance animation and optional renderer agree across first visit, reload and OS preference changes. Evidence: [preference code][motion-script], [reduced-motion CSS][css-reduced], [spatial state source][room-source].

### MOT-03 — Separate touch browsing from desktop marquee behaviour

**P2 · Source-confirmed; physical touch validation pending · Effort M**

The rows combine a continuously translated track with native horizontal overflow. No explicit drag/swipe state pauses or reconciles that translation. Logo captions become permanently visible at a narrow width, rather than for all non-hover inputs. The `hover:none` override can also supersede the viewer’s pause rule because it does not exclude `.viewer-open`.

**Recommendation:** test and define swipe behaviour on real touch hardware. Ensure deliberate dragging wins over automatic motion, captions remain available on touch tablets, and an open viewer reliably suspends the background rows. Use input capability alongside viewport width; add a discreet swipe cue when motion is off.

**Acceptance:** a touch visitor can browse and select every mark without fighting movement or relying on hover. Evidence: [flow rules][css-flow], [touch override][css-touch], [viewer state code][viewer-script]. This is a source risk to validate, not a reproduced physical-device failure.

### MOT-04 — Prefer a selective, manual slideshow over more automatic carousels

**P3 · Design opportunity · Effort M**

The logofolio is a continuous marquee; project pages use a static sequence plus a manual lightbox. There is currently no dedicated project slideshow. That is not itself a defect.

**Recommendation:** if a slideshow adds value, use one on a strong case study to reveal a meaningful sequence—logo, system, application—with visible position, direct selection, keyboard controls and optional swipe. Keep the first useful image visible without interaction. Avoid an autoplay hero that hides your best work in later slides.

**Acceptance:** the sequence improves understanding, remains fully navigable without movement, and does not materially increase initial page cost. Reference: [accessible carousel structure and controls](https://www.w3.org/WAI/tutorials/carousels/).

## 4. Accessibility, artwork viewing and icons

### A11Y-01 — Mobile keyboard focus disappears into the menu background

**P1 · Confirmed · Effort S**

At 390 px, open Menu and press Tab. The focused “The Mark Room” link matches `:focus-visible`; its 3 px outline is `rgb(36, 69, 220)`, the same as the mobile menu background. The contrast between those two colours is **1:1**.

**Recommendation:** use a context-aware focus colour, or a two-colour indicator that remains visible on both paper and blue surfaces. Test the whole focus path, not just a button on the homepage.

**Acceptance:** every mobile menu link has an unmistakable keyboard indicator. Evidence: [global focus rule][css-system], [menu surface][css-nav], [screenshot][focus-image]. See [W3C Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html).

### A11Y-02 — Decorative duplicates still contain focusable buttons

**P2 · Source-confirmed · Effort M**

Each flow duplicates eight buttons inside an `aria-hidden="true"` group. The clones have `tabindex="-1"` and pointer-down focus is suppressed, which reduces accidental focus, but they remain programmatically focusable interactive elements inside a hidden accessibility subtree.

**Recommendation:** make duplicate presentation genuinely non-focusable/non-semantic while preserving an accessible way to activate each original mark. Review both visual copies and the original keyboard sequence. Do not simply remove access to the marks currently visible in the duplicate portion.

**Acceptance:** no interactive element can receive focus inside an `aria-hidden` subtree, and every logo still has one clear accessible entry. Evidence: [flow generation][flow-build], [clone interaction handling][viewer-script]. See [MDN on aria-hidden and focus](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-hidden).

### A11Y-03 — Announce image changes and describe the artwork more usefully

**P2 · Source-confirmed; screen-reader output unverified · Effort M**

The dialog is labelled “Project image viewer” even for logos. Its caption is neither connected as a description nor a live region. Next/Previous changes the image and caption while focus stays on the button. Many gallery alternatives are generic “design detail 1”, rather than descriptions of what is shown.

**Recommendation:** connect the current caption to the dialog, announce intentional item changes politely, and replace generic alternatives/captions with useful descriptions. Keep decorative text from being announced twice. Preserve native Escape and return-focus behaviour, which passed this review.

**Acceptance:** a screen-reader user can identify the current artwork and position after navigation without hunting through the dialog. Evidence: [dialog markup][page-build], [caption changes][viewer-script], [case image text][case-build].

### GAL-01 — “Enlarge” needs a way to inspect fine artwork details

**P2 · Confirmed capability limit · Effort M**

The viewer offers Previous, Next and Close, but no zoom, pan, fit/reset or open-original action. At 320 px, the image area is about 274 px wide. Case artwork is capped at a 1280 px export, so fitting a print label to that screen does not make small typography inspectable.

**Recommendation:** provide an accessible fit/zoom/reset path or an explicit higher-resolution image link. Support touch inspection without blocking normal page zoom. Keep large source files on demand.

**Acceptance:** a visitor can examine label typography and brand details, then return predictably to the fitted image. Evidence: [viewer markup][page-build], [image loading code][viewer-script], [320 px viewer screenshot][viewer-image].

### GAL-02 — Add image loading and failure feedback inside the viewer

**P2 · Source-confirmed; network failure not injected · Effort S–M**

The viewer assigns the new `src` and immediately changes the caption. There are no loading, error, retry or adjacent-image preload handlers. On a slow connection, an item change has no explicit progress signal; a failed image has no recovery UI.

**Recommendation:** preserve a stable viewing area, show a subtle loading state, handle failure with retry or an image link, and preload at most the adjacent items when justified. Avoid a heavy slideshow library for this small need.

**Acceptance:** slow and failed image requests produce an understandable, recoverable state. Evidence: [showImage/openImage][viewer-script].

### ICON-01 — Standardise functional icons without bringing back arrow decoration

**P3 · Source-confirmed; design judgement · Effort S**

The site mixes text glyphs such as `+`, `×`, `⧉` and a tiny motion indicator with the custom wordmark. Glyph size and alignment vary by font/platform. Most controls already have clear names, which should be retained.

**Recommendation:** use a small consistent set of inline SVGs for copy, close, enlarge and motion where an icon helps. Use consistent stroke weight, optical sizing and hit areas. Keep text for ambiguous actions; do not replace labels with unexplained icons or reintroduce decorative arrows.

**Acceptance:** controls remain understandable at phone size, with decorative SVGs hidden from assistive technology and named buttons preserved. Evidence: [footer controls][footer-build], [dialog controls][page-build], [tile markup][flow-build].

## 5. Performance, speed and adaptive delivery

### Measured file sizes—not page-speed scores

| Resource | Raw size | Locally calculated gzip size | Interpretation |
| --- | ---: | ---: | --- |
| Shared `main.js` | 7.1 KiB | 2.5 KiB | Already small; preserve this. |
| Shared CSS | 40.9 KiB | 9.0 KiB | Not a reason for a framework rewrite. |
| Optional `room.js` | 529.0 KiB | 132.7 KiB | Deferred until Spatial is selected; keep it out of initial loading. |
| Both font files combined | 230.8 KiB | 101.3 KiB | Early-loading optimisation candidate. |
| All 16 logo textures combined | 348.7 KiB | Not assessed | Shared images; duplicate elements do not mean duplicate file downloads. |
| Portrait, 640 / 1280 export | 60.5 / 208.5 KiB | Not assessed | Choice should match display size/density. |
| Selected-work PDF | 8.42 MiB | Not assessed | Optional download; not an initial homepage payload. |
| Birthday video | 2.94 MiB | Not assessed | On the motion project page; not homepage playback. |
| Entire `dist` directory | 17.91 MiB | Not assessed | Deployment inventory, **not** one visitor’s initial transfer. |

Gzip figures are calculated from local files. They do not prove the deployed host sends compressed responses.

### PERF-01 — Match responsive image hints to actual layouts

**P2 · Source-confirmed · Effort M**

The shared image helper declares `100vw` below 700 px and `65vw` otherwise. Actual display widths vary: two-column project cards, full-width case images, and smaller gallery cells use the same helper. The About and homepage preview images use only a fixed 640 px source.

**Recommendation:** supply layout-specific `sizes`, consider a useful intermediate export, and add responsive candidates to fixed-size images where larger displays need them. Inspect actual resource selection at multiple pixel densities before claiming savings. For example, Beans Central’s 640 export is 43,154 bytes versus 110,568 bytes at 1280; the smaller file is appropriate only when it still meets the display requirement.

**Acceptance:** the browser receives accurate slot sizes and artwork remains sharp without unnecessary transfer. Evidence: [image helper][image-build], [homepage preview][hero], [About portrait][about]. Reference: [web.dev responsive image selection](https://web.dev/learn/images/descriptive).

### PERF-02 — Measure WOFF2/subsetting and font-swap stability

**P2 · Source-confirmed · Effort S–M**

Both TTF fonts are preloaded on every page. Together they are about 231 KiB raw. `font-display: swap` is present, but there is no explicit fallback metric adjustment.

**Recommendation:** compare WOFF2 and appropriately licensed subsets, preserving required characters and punctuation. Keep only justified critical preloads, and evaluate fallback metrics for headline wrapping/shift. Measure the resulting file savings and rendering changes rather than assuming a fixed percentage.

**Acceptance:** a cold-load trace shows prompt readable text and no material headline jump. Evidence: [font declarations][css-fonts], [preload generation][page-build]. Reference: [web.dev font loading](https://web.dev/articles/optimize-webfont-loading).

### PERF-03 — Verify real loading and interaction speed before claiming “very fast”

**P1 release gate · Unverified · Effort M**

There is no production trace or field data. The hero’s opacity entrance lasts 0.85 seconds, with staggered delays; its contribution to perceived/rendered readiness needs measurement. A successful link checker cannot establish LCP, INP or CLS.

**Recommendation:** after an authorised deployment, run repeatable cold/warm mobile audits with network and CPU constraints. Check homepage, work index, a large case study and logofolio. Inspect the entrance effect and sticky header/backdrop rendering on a modest device. Keep first meaningful text useful immediately if the animation delays it.

| Metric | Current result | Future good target |
| --- | --- | --- |
| LCP | Not measured | ≤ 2.5 s |
| INP | Not measured | ≤ 200 ms |
| CLS | Not measured | ≤ 0.1 |
| Lighthouse performance | Not measured | Record a repeatable lab result; do not invent a score. |

The Core Web Vitals targets apply at the 75th percentile of real visits; lab checks help diagnose but do not establish a field pass. Reference: [web.dev Core Web Vitals](https://web.dev/articles/vitals).

### PERF-04 — Pair caching with versioned asset names

**P2 · Source-confirmed; production behaviour unverified · Effort M**

The generated header rules cache `/assets/*` for one day, while exported assets keep stable filenames. Root JavaScript/CSS have no explicit cache rule in that file. The development server intentionally responds with `no-cache`; it is not representative of CDN behaviour.

**Recommendation:** define a production cache strategy using content-versioned assets and appropriately refreshed HTML. Verify actual compression, validators, cache hits and media range requests on the host. Do not simply make unchanged filenames immutable for a year, which can leave old artwork visible after an update.

**Acceptance:** repeat visits are efficient and deployments cannot combine stale artwork/scripts with new HTML. Evidence: [generated headers][headers-build], [local server][server].

### DOC-01 — Improve downloadable PDF size and accessibility

**P2 · Confirmed · Effort M**

The 18-page portfolio PDF is **8,825,251 bytes**. Both the public CV and selected-work PDF contain extractable text, but neither has a PDF structure tree or marking information in the inspected files. Extractable text is not equivalent to a tagged, accessible reading order.

**Recommendation:** offer a visibly labelled lighter portfolio download, with file size/page count. Create properly tagged exports with tested reading order, headings and meaningful image alternatives. Preserve artwork legibility, links and the private-content exclusions. Do not equate successful text extraction with PDF/UA conformance.

**Acceptance:** download weight is clear before selection, and both documents are usable with assistive technology. Evidence: [download assets][downloads], [privacy/PDF evidence][privacy-data].

## 6. Security and resilience

### SEC-01 — Tighten the script policy as defence in depth

**P2 · Security severity: Medium hardening finding · Source-confirmed · Effort M**

**Rule:** JS-CSP-001 / JS-CSP-002.  
**Location:** [header generator, line 48][headers-build]; generated [header rules][headers-file].

The configured policy contains:

```text
script-src 'self' 'unsafe-inline'
style-src 'self' 'unsafe-inline'
```

**Impact:** if HTML injection were introduced later, permitting arbitrary inline scripts would weaken CSP’s ability to contain it. **No attacker-controlled input-to-execution path was established in this static portfolio.** This is not a claim of a demonstrated XSS exploit.

**Recommendation:** remove the broad script exception using a CSP-compatible approach for any necessary inline blocks, such as build-generated hashes. Review style exceptions separately: current templates and interactions use inline/custom styles, so indiscriminately removing them could break presentation. Verify compatibility with the hosting environment before enforcement.

**Acceptance:** hosted responses deliver the intended tested policy without breaking structured data, interactions or asset loading. See [MDN CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP).

### SEC-02 — Verify the host actually applies the intended protections

**P1 release verification · Security severity: not yet assessable · Unverified · Effort S–M**

**Location:** [generated header configuration][headers-build], [hosting binding][hosting]. The local server sends `nosniff`, but does not apply the full generated header file. No live deployment exists to inspect.

**Impact:** source configuration alone cannot demonstrate that CSP, framing restrictions, referrer and permission policies protect the eventual public response. This does **not** establish that the final host lacks them.

**Recommendation:** inspect deployed response headers and visitor access on every relevant route and asset class. Confirm hosting-specific header support and CSP compatibility. Retain the local server’s loopback binding; do not expose that preview server as the production deployment.

**Acceptance:** evidence comes from actual HTTPS responses and an unauthenticated visitor session, not just the presence of `_headers` in a folder.

### SEC-03 — Keep trusted-content boundaries explicit as editing grows

**P3 · Security severity: Low preventive recommendation · Source-confirmed · Effort S–M**

**Location:** [page/project generation][case-build], [copy-label reset][copy-script]. Some project strings are interpolated directly into HTML at build time. They currently come from local, author-controlled content. The shared script’s one `innerHTML` assignment contains a fixed constant, not user input.

**Recommendation:** document this trust boundary and consistently escape text/validate asset paths if a CMS or external content source is introduced. Keep secrets out of browser code and retain pinned dependencies. Do not add authentication, sanitisation libraries or a backend merely to address a hypothetical threat absent from this static site.

**Acceptance:** future content editing cannot silently turn an external string into executable markup. No current exploitable injection or exposed credential was found in the inspected paths.

## 7. Links, publication, metadata and maintainability

### LINK-01 — Resolve the LinkedIn discrepancy before launch

**P2 · Confirmed discrepancy; correct destination unverified · Effort S with owner confirmation**

The website and supplied CV use [linkedin.com/in/eyiladeoridamisi](https://www.linkedin.com/in/eyiladeoridamisi). Your public [Behance profile](https://www.behance.net/eyiladeoridamisi) links to `linkedin.com/in/joshuaoridamisi`. The site’s LinkedIn destination reached an authentication wall, so the difference is **not proof of a broken link**.

**Recommendation:** confirm the current canonical profile, then synchronise website, public CV and Behance when authorised. Retain the existing destinations until confirmed. Check mailto composition on actual devices; no email was sent during this audit.

**Acceptance:** every professional-profile link reaches the intended identity and the public portfolio/downloads agree. Evidence: [footer link][footer-build], original/public CV link inspection, browser review of Behance.

### LAUNCH-01 — Establish a real, visitor-accessible portfolio address

**P1 release gate · Confirmed current state · Effort M**

Sites reports **zero saved versions**, `current_live_url: null`, and access mode `custom`. The expected-origin string embedded in the build is not evidence of a live, publicly accessible portfolio.

**Recommendation:** after the review is approved and implementation is complete, publish through the existing project, confirm the intended audience, and test the actual link in a signed-out visitor session. A custom domain could strengthen professional presentation later, but a working shareable address comes first. No publication or audience change is authorised by this report itself.

**Acceptance:** a prospective client can open the exact shared URL and all case-study/download links without an owner-only session. Evidence: read-only Sites metadata lookup and [hosting binding][hosting].

### SEO-01 — Make production metadata configurable and project-specific

**P2 · Source-confirmed · Effort M**

The canonical origin is hard-coded. Every page uses the same social preview image, and the 404 page receives ordinary canonical/social metadata rather than an explicit `noindex` instruction. The sitemap does exclude the 404, and unique titles/descriptions are already present.

**Recommendation:** bind canonical metadata to the verified deployed origin, give important projects their own share image and useful image alternatives, and give error pages intentional indexing metadata. Check social previews on the actual domain. Do not add speculative schema fields or claims.

**Acceptance:** sharing a case study previews that project, links resolve to the real production host, and the error document is intentionally treated. Evidence: [origin and metadata generation][page-build], [404 generation][notfound-build].

### QA-01 — Expand checks around the failures the current checker cannot see

**P2 · Source-confirmed · Effort M**

The existing checker is useful, but its 536-reference pass does not test focus contrast, interaction states, real image quality, responsive geometry, deployed headers, production speed, or dynamic announcements. It also does not cover every source of an asset reference, such as all `srcset` candidates; this audit checked those separately.

**Recommendation:** keep the fast static checker and add a small, meaningful regression suite for menu keyboard access, filtering, viewer focus/announcements, motion preference, and the critical responsive layouts. Keep deployment checks distinct from local passes. Record visual baselines for a few important page types, rather than mirroring every CSS rule in tests.

**Acceptance:** a successful check has a precise scope and the high-impact regressions in this report can be detected before release. Evidence: [current checker][checker], [audit evidence files][audit-folder].

### MAINT-01 — Update documentation and make future refinements easier to review

**P3 · Confirmed · Effort S–M**

The README still describes a homepage cube, and the design-direction document still lists the cube/interactive sketch. The CSS source is roughly 42 KiB across only 34 very long lines; the builder places large templates on single lines. Counts such as “11” and “16” are also repeated in markup.

**Recommendation:** update documentation to the final interaction model, format source into readable component sections, and derive repeated counts from content where practical. Keep the current lightweight architecture; this does not require migrating frameworks.

**Acceptance:** another developer can locate a component, assess a change, and update content without inconsistent counts or stale instructions. Evidence: [README][readme], [design direction][direction], [stylesheet][css-system], [page builder][page-build].

### SPATIAL-01 — Defer optional-scene refinements, but retain its fallback requirements

**P3 · Source-only review; runtime deliberately not activated · Effort M when resumed**

The spatial module correctly sits behind a dynamic import. However, it loads the logo JSON before registering controls, waits for all textures before displaying the scene, and the import failure path offers no explicit retry/status message. Its 1024 px textures also deserve a future GPU-memory review; the small compressed image files do not represent decoded texture memory.

**Recommendation when 3D work resumes:** make load/failure states explicit, keep a usable 2D fallback and controls, measure first-use cost, and tune texture resolution to actual rendering needs. Keep the optional scene visually related to the rounded 2D presentation. Do not add the pending character or resume rigging as part of the current audit.

**Acceptance:** the optional view cannot leave an apparently active but unresponsive control set after a failed load, and it remains optional on limited devices. Evidence: [dynamic import][room-loader], [spatial module][room-source].

## Page-by-page emphasis

| Page | Main opportunity |
| --- | --- |
| Home | More specific personal positioning; readable labels; tighter tablet composition; one distinctive interaction connected to real work. |
| Work | Clarify individual projects versus collections; strengthen curation and category context; retain filter accessibility. |
| About | Keep the thoughtful process disclosures; make practical experience/CV information easy to find; avoid shrinking supporting copy. |
| Logofolio | Reconcile effective motion state, touch browsing and cloned semantics; retain the complete static index. |
| Flagship identity pages | Show brief, contribution, decisions and real process evidence alongside finished applications. |
| Print/editorial collections | Add meaningful captions and a better way to inspect fine typography. |
| Motion page | Keep native controls and no autoplay. The supplied 9.87-second H.264 file has no audio stream, so a speech-caption defect was not established; offer a concise text equivalent for meaningful visual content. |
| Error page | Preserve the real 404 response and clear way home; improve indexing metadata. |
| Shared footer | Increase small text, make downloads’ formats/sizes clear, and reconcile professional-profile URLs. |

## Suggested sequence after owner approval

1. **Access and clarity:** address A11Y-01 and UI-01; confirm LinkedIn; define the professional positioning and verified case-study facts.
2. **Core interaction quality:** address MOT-01–03, A11Y-02–03, GAL-01–02 and the mobile no-script path.
3. **Delivery quality:** optimise measured image/font/download costs; improve tagged PDFs; establish production caching and CSP compatibility.
4. **Release evidence:** authorised publication, visitor-access check, deployed headers, cross-browser/device checks and repeatable performance measurements.
5. **Signature refinement:** selectively improve graphic authorship or one manual slideshow. Revisit optional 3D only when that work is explicitly resumed.

### Remaining verification before launch

- Physical iPhone/Safari and Android/Chrome touch/swipe behaviour; tablet with touch and keyboard; Firefox/desktop Safari.
- Text enlargement at 200%, reflow at 400%, short landscape screens, high pixel density and focus not obscured by the sticky header. The 320 px checks here do not substitute for a full zoom audit; see [W3C Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).
- VoiceOver or another screen reader through navigation, mode controls, filters and the changing image viewer.
- Slow/failed script and image requests; blocked storage/clipboard; no-JavaScript navigation; media range/seeking on the actual host.
- Real shared-URL access, PDF opening/download, email-client behaviour, canonical URL and social-preview rendering.
- Cold/warm loading and interaction measurements. Keep any performance claim proportional to the evidence collected.

## Evidence and source index

All evidence is local to this review. Hash comparison against the start-of-audit baseline confirmed zero changes to the website source, content, package files, hosting binding, or generated build files. The review created only this report and audit artefacts.

- [Responsive measurements][responsive-data] — 24 representative page/viewport observations.
- [Additional project checks][extra-responsive] — nine remaining project routes at 320 px.
- [Interaction observations][interaction-data] — filters, dialog, motion preference, menu focus and disclosures.
- [Static/HTTP/size observations][static-data] — generated document checks, 125 requested targets and raw/gzip inventory.
- [PDF/privacy observations][privacy-data] — bounded protected-term and credential-pattern checks.
- [Mobile menu focus screenshot][focus-image], [tablet composition][tablet-image], [phone artwork viewer][viewer-image], [desktop logofolio][flow-image].

[hero]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/index.html:4>
[about]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/about.html:1>
[projects]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/content/projects.json:1>
[css-fonts]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/styles.css:1>
[css-system]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/styles.css:4>
[css-nav]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/styles.css:8>
[css-hero]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/styles.css:10>
[css-flow]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/styles.css:14>
[css-mobile]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/styles.css:30>
[css-touch]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/styles.css:31>
[css-reduced]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/styles.css:34>
[image-build]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/scripts/build.mjs:11>
[header-build]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/scripts/build.mjs:13>
[footer-build]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/scripts/build.mjs:14>
[flow-build]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/scripts/build.mjs:17>
[page-build]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/scripts/build.mjs:23>
[case-build]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/scripts/build.mjs:34>
[notfound-build]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/scripts/build.mjs:37>
[headers-build]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/scripts/build.mjs:48>
[headers-file]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/dist/_headers:5>
[menu-script]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/main.js:19>
[filters]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/main.js:57>
[motion-script]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/main.js:1>
[copy-script]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/main.js:74>
[viewer-script]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/main.js:98>
[flow-script]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/main.js:129>
[room-loader]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/main.js:140>
[room-source]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/src/room.js:4>
[server]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/scripts/serve.mjs:1>
[checker]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/scripts/check.mjs:9>
[hosting]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/.openai/hosting.json:1>
[readme]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/README.md:1>
[direction]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/docs/DESIGN_DIRECTION.md:1>
[downloads]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/dist/assets/>
[audit-folder]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/audit-2026-10-21/>
[responsive-data]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/audit-2026-10-21/responsive-dom.json>
[extra-responsive]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/audit-2026-10-21/extra-responsive-dom.json>
[interaction-data]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/audit-2026-10-21/interactions.json>
[static-data]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/audit-2026-10-21/static-audit.json>
[privacy-data]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/audit-2026-10-21/privacy-check.json>
[focus-image]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/audit-2026-10-21/mobile-menu-focus.png>
[tablet-image]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/audit-2026-10-21/home-tablet.png>
[viewer-image]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/audit-2026-10-21/label-viewer-320.png>
[flow-image]: </Users/joshuaoridamisi/projects/Joshua Portfolio Website/output/audit-2026-10-21/logofolio-desktop.png>
