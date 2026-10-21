# Portfolio refinement implementation report

Date: 21 October 2026  
Review target: existing Eyilade portfolio, retaining its current private audience  
Site: https://eyilade-oridamisi.bubblydill512.chatgpt.site

## Delivered career content

The Experience section now contains **seven chronological milestones**, beginning in 2017. The latest typed career directive takes precedence over older instructions to preserve separate roles.

| Stop | Period | Organization | Role / presentation |
|---|---|---|---|
| 01 | Oct 2017–Apr 2020 | Intelligentsia Orb Worldwide Limited | Volunteer Lead ICT Director; existing details retained |
| 02 | Jun 2019–May 2020 | Federal Government | National Youth Service Corps (NYSC); existing details retained |
| 03 | Jul 2019–May 2020 | Running Jack IT Firm | Senior Graphics Designer; existing details retained |
| 04 | Sept–Dec 2020 | Citypartner Healthcare | Facility & Designer; one consolidated entry |
| 05 | Dec 2020–Mar 2021 | Ferman | Graphic Designer & Motion Graphic Artist; one consolidated entry |
| 06 | Mar 2021–Jan 2022 | Redot Digital Marketing and Consultancy Agency | Graphic Designer; existing description retained |
| 07 | **2022–Present** | **PwC Nigeria** | **Senior Graphic Designer**, highlighted as the current position |

PwC is one timeline stop containing an ordered progression: Graphic Designer → Experienced Graphic Designer → Senior Graphic Designer. The complete approved professional description is available under “My work at PwC”. Internal promotions create no additional timeline stops. MaxyStuff UK and the separate Citypartner ICT Manager entry are removed. The former 2016 CRG timeline stop is removed so the timeline begins in 2017; broader creative/ideator positioning elsewhere is preserved. Citypartner retains its verified facilities and healthcare consultancy responsibilities without inventing design achievements.

## Interaction and layout changes

- **Career:** native document scrolling drives a bidirectional sticky rail on desktop viewports at least 1100px wide and 900px high. Milestones, years, connectors and progress respond together. The finite scroll run releases into Brand Experience and Toolkit. Earlier/Later and keyboard controls remain available. Mobile uses the readable vertical timeline. Smaller desktop/tablet and motion-off views retain native browsing. Expanding responsibilities releases the sticky presentation to accommodate long descriptions.
- **Hero:** removed the three visible reaction buttons. Accepted clicks alternate thumbs-up, wave, thumbs-up, wave. Rapid repeated clicks are ignored while a user gesture completes. Thinking occurs automatically after a randomized 14–26 seconds of idle time and yields to a user interaction. Speech and thought bubbles have distinct treatments and dismiss with their reactions. Idle breathing remains; **blink is excluded**.
- **Works:** implemented the recording’s centred three-card perspective arrangement using the existing visual system. Desktop shows three cards; tablet and mobile show a dominant central card with neighbouring previews. Previous/Next, keyboard, swipe, wraparound and all category filters work. All eleven original project destinations remain present. Autoplay pauses for manual interaction, hover, focus, offscreen visibility, hidden tabs and motion-off preferences; an explicit control resumes it. The unenhanced page remains a normal project grid.
- **Toolkit:** added the supplied Figma, GitHub and Leonardo AI marks, bringing the toolkit to nine. Added staggered reveals and subtle icon hover motion without changing the palette or typography.
- **Navigation/About:** About now targets `/about/` throughout desktop and mobile navigation. Homepage scrolling does not activate About. Active navigation reflects the route. The About portrait is flipped left toward its heading.
- **Shared footer:** restored the original full-body illustration, flipped left toward the CTA, with a bounded tilt/greeting response. LinkedIn and Behance sit at the left of the contact action group, followed by the phone and copy action. Existing email, telephone, profile, CV and portfolio destinations remain unchanged. The footer is generated consistently on all sixteen pages.

## Assets and implementation

New toolkit exports use `Figma-logo.svg.webp`, `Github.png` and `Leonardo.Ai-Symbol.png` from `Assets/Career and skills`. Their lossless WebP exports total approximately 13 KB. Original source files are untouched. The footer reuses the existing optimized full-body illustration; the hero reuses the approved smooth four-state character assets. CSS transforms preserve the original artwork when changing orientation.

Contact icons are local SVG copies from Font Awesome and Lucide, with upstream notices retained. Exact sources and licence locations are documented in [ICON_PROVENANCE.md](ICON_PROVENANCE.md).

Career content remains in `content/career.json`. Dedicated `src/career.js` and `src/carousel.js` modules contain the new behaviour; the shared builder generates navigation and footer markup. No additional website runtime dependency, external image service, WebGL canvas or remote runtime request was introduced. Existing CSP and external-link protections remain in place.

## Validation evidence

- `npm run build`: PASS — fifteen routes plus the 404 page; seven career records, nine tools and nineteen identities.
- `npm run check`: PASS — sixteen pages and 642 internal file references; image dimensions, metadata, project links, consolidated career order, tool membership, shared footer, dedicated About routing and private-product content boundary checked.
- `npm test`: PASS — three fake-clock behavioural tests covering click alternation/debouncing, automatic thinking and user priority, offscreen/hidden suspension, and reduced-motion still reactions.
- `git diff --check`: PASS.
- Browser checks covered 320×740, 390×844, 768×1024, 1280×720, 1280×900 and 1440×900 layouts. Checked Home, About, Works, Logofolio and representative identity/motion case studies. No document-level horizontal overflow was observed in these checks.
- Verified mobile menu, About refresh/back/forward navigation, hero click/keyboard reactions, mobile PwC description, sticky progression/release, carousel autoplay/manual pause/filter/keyboard/swipe, footer greeting and successful email copying.
- Existing image viewer still advances, closes with Escape and restores focus to its trigger. The motion case study retains its native video controls and correct local media source. Logofolio pause/resume, All marks and a linked project destination passed.
- The inspected final Home session reported no captured browser warnings or errors.
- Bundled output: JavaScript 16.4 KB / 5.3 KB gzip; CSS 50.1 KB / 10.9 KB gzip. No Lighthouse score or field Core Web Vitals result is claimed.

Local evidence screenshots are retained in `output/refinements-2026-10-21/`: `career-pwc-mobile.png` and `footer-desktop.png`. The provided video was inspected through a twelve-frame contact sheet in the same folder’s `reference/` directory.

## Limits and review notes

Responsive checks use the in-app browser; physical iOS/Android devices and separate Safari/Firefox runs have not been tested. Motion-off behaviour was verified through the site control and deterministic tests; no operating-system preference setting was changed. This is a focused refinement validation, not a complete accessibility certification, security penetration test or measured performance audit.

The character remains animated 2D artwork. Actual 3D mesh/rig work remains paused. The Works arrangement adapts the supplied recording’s geometry and movement to the portfolio’s established art direction, without reproducing its purple advertising treatment.

The existing Site audience is owner-private and is preserved. Publishing this revision does not make the portfolio publicly accessible to recruiters. Deployment confirmation and the resulting review URL are provided with the final delivery.
