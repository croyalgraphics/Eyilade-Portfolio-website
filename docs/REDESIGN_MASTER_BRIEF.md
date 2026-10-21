# EYILADE — Portfolio Website Redesign & Interactive Web CV
  
**Primary objective:** Upgrade my website portfolio into a polished, distinctive, cohesive portfolio that functions as an interactive **Web CV** on the Home page, with dedicated **Works** and **Logofolio** pages.

> **Important asset context:** A folder named `Assets` already exists at the project's root on my laptop. It contains the available images, illustrations, logos, icons, and potentially font resources needed for this redesign. Inspect and use the actual contents of this folder. Do **not** invent filenames, assume missing assets exist, use generic stand-in imagery, or ask me to re-upload assets that are already available to the development agent locally. If any critical asset is genuinely missing, list precisely what is missing before substituting anything.
Replace all old logos and icons (Logofolio page, about me, home page, works page) with this in the Assets folder accordingly. Resize appropriately.

---

## 1. Design direction & experience principles

Treat this as a senior multidisciplinary creative's portfolio, **not** a generic SaaS landing page or AI-generated template.

- **Personality:** Editorial, distinctive, confident, sophisticated, welcoming, playful where appropriate, and creatively art-directed.
- **Visual unity:** Typography, color, shape language, spacing, motion, navigation, and interactive behavior must feel like one connected design system across Home, Works, Logofolio, and Contact.
- **Strong composition:** Establish a deliberate visual hierarchy with considered whitespace, asymmetrical composition where useful, and consistent alignment.
- **Less explanation, more personality:** Remove redundant eyebrow labels, filler descriptions, self-explanatory captions, and templated microcopy (examples: “Explore my creative universe,” “Scroll to discover,” “Crafted with passion,” or section labels that merely repeat a heading). **Do not remove essential content** such as the About text, job roles, employment dates, company names, skill names, accessible button names, or contact information.
- **Purposeful motion:** Animation should reinforce identity, rhythm, navigation, and comprehension—not distract from reading the CV.
- **Production quality:** Implement fully responsive layouts, optimized assets, accessible interactions, resilient fallbacks, and verified functional links. No fake functionality or generic placeholders in the finished website.

### Non-negotiable content boundaries

The Home page **must not** embed a Works gallery, project cards, or a Logofolio gallery. Those belong exclusively to their dedicated pages. The Home page **must** contain conspicuous, beautifully animated entry points to both pages.

---

## 2. Design system: fonts, colors, UI surfaces

### 2.1 Typography

Use only the following primary typefaces, subject to availability/licensing of the font files:

| Typeface | Intended application | Treatment |
|---|---|---|
| **BeachSound** | H1s, major editorial headings, signature statements, highlighted callouts, select oversized decorative text | Expressive display face; apply strategically, not to lengthy body copy |
| **Rubik** | Body copy, navigation, buttons, career details, captions that convey necessary meaning, numerics, dates, contact links, footer | Legible, consistent, clean UI typography |

**Implementation:** Search `Assets` for the actual font files. Define `@font-face` with appropriate formats and weights if supplied; do not silently relabel a substitute as BeachSound. If BeachSound is absent, report it and use a clearly identified temporary fallback until the font is supplied. Use responsive `clamp()`-based type scales, correct line heights, and coherent font weights. Prevent FOUT/CLS as far as practical.

### 2.2 Color system

**Primary accent / signature color: `#BF9724`**. Use it for selected decorative text, active states, accent strokes, graphic elements, interactive highlights, and distinctive UI objects. This is the website's main signature color.

- Establish an intentional **neutral supporting palette** (light and/or dark surfaces, ink-like text, subtle borders) that complements the accent; do not introduce unrelated competing accent colors.
- Use `#BF9724` as a signature accent, not indiscriminately on every element. Reserve contrast and whitespace to give it impact.
- **Accessibility note:** The accent on white is insufficient for small text in many contexts. Use a darker accessible tonal variant or dark background for text/button combinations where WCAG contrast demands it; keep `#BF9724` faithful for large decorative shapes and nonessential accent treatment.
- Use design tokens/CSS variables consistently (e.g., `--color-accent`, `--color-text`, `--color-surface`, `--color-border`, `--radius-*`, `--space-*`).
- Apply a consistent rounded/softened shape language where it complements the creative direction; avoid inconsistent button radii and mismatched cards.

---

## 3. Asset audit, mapping & replacement

1. Inspect the root-level `Assets` directory recursively **before** editing sections that depend on media.
2. Create an internal asset map of: Eyilade illustration variants, personal photography, employer/client logos, software/tool icons, Works media, Logofolio files, and fonts.
3. Replace the previous profile picture everywhere relevant with the **new `Eyilade illustration`** from `Assets`. Prioritize the **full-pose/head-to-toe** version on the Home hero. Preserve the entire figure without unintended cropping or distortion.
4. Prefer provided logos and brand marks over external hotlinked images. Keep logos visually crisp and their aspect ratios intact; use appropriate transparent assets.
5. Do not alter the fundamental identity of any brand logo through recoloring, distortion, stretching, or clipping.
6. If multiple similarly named assets exist, inspect them visually and choose the correct versions; document ambiguous cases.
7. Optimize exported/display assets when appropriate (responsive sizes, lazy loading, modern delivery formats), while preserving originals.
8. Keep existing project references functional. Avoid broken import paths, case-sensitivity mistakes, missing image fallbacks, and unnecessary asset duplication.

**Reality check for interactivity:** A transparent PNG/WebP illustration is a **2D asset**, not an actual rigged 3D model. Three.js can create tasteful depth, parallax, shader, light, tilt, and pointer-reactive movement using a 2D plane or layered artwork. **Do not promise true 3D rotation, articulated character poses, or skeletal animation unless a suitable 3D model/rig or layered source assets actually exist.** Use progressive enhancement and a static/animated 2D fallback if WebGL is unsupported.

---

## 4. Responsive navigation architecture

Rework navigation for **desktop, tablet, and mobile** as a unified system rather than treating each as a disconnected design.

**Suggested information architecture** (keep existing verified routes when they already exist):

- **Home** — interactive Web CV, with anchored sections for Intro, Experience, Skills, Tools, Brands, and Contact.
- **Works** — dedicated project/case-study page.
- **Logofolio** — dedicated logo showcase page.
- **Contact** — can scroll to the Home contact section or use the website's established contact route; choose one clear, consistent behavior.

### Desktop

Use a refined, compact top navigation with clear active states and tasteful interaction feedback. Consider a high-quality sticky/scroll-responsive treatment only if it enhances usability and does not obscure page content. Make link targets obvious without relying on decorative directional arrows.

### Tablet

Rebalance density, spacing, and navigation visibility to the available viewport. Maintain the same identity and interaction language, not an unrelated intermediate UI.

### Mobile

Prioritize thumb reach, readable tap targets, no horizontal overflow, and a minimal but discoverable menu (e.g., an accessible compact menu/drawer). Preserve direct access to **Works** and **Logofolio**. Avoid crowding the top bar with every section link.

### Interaction standards

Keyboard access, proper focus states, accurate active/current page states, closed-menu focus restoration, touch behavior, and accessible labels are required. Keep transitions short and polished; navigation must not become slower due to animation.

---

## 5. Home page — interactive Web CV

The Home page should immediately convey **who I am, what I do, where I have worked, the brands I have worked with, what I use, and how to reach me**. Treat it as a beautifully art-directed professional CV—not a sequence of generic marketing sections.

### Recommended narrative flow

1. **Hero / identity:** Full-pose illustration, name, bold creative introduction, and primary page-entry actions.
2. **About / creative disciplines:** Compact but substantial personal positioning and core skills.
3. **Career / experience timeline:** Chronological, interactive, scroll-responsive career history, from earliest to present.
4. **Brands:** Employer/client logos with meaningful spacing and elegant motion.
5. **Tools:** Actual logos of the software I use.
6. **Dedicated-page pathways:** Two high-visibility animated buttons/tiles linking to **Works** and **Logofolio**—**not** embedded galleries.
7. **Contact:** Clean, inviting contact block and footer with working actions.

The order may be art-directed slightly if needed for the strongest visual story; **do not omit any of the above content requirements**.

### 5.1 Hero: illustration-led introduction

- Make the **full-pose Eyilade illustration** a central compositional feature. Allow it to interact spatially with the headline/introduction rather than placing it mechanically beside a generic text column.
- Apply pointer-responsive Three.js effects where technically appropriate: subtle cursor-following parallax, dimensional tilt, hover response, spring-like easing, or restrained lighting/shadow changes. Clicking/tapping should trigger one meaningful, delightful response (e.g., a brief pose-like tilt, bounce, ripple, or short visual reaction), then return cleanly to idle.
- Interactions should feel responsive but **not** jittery, oversized, distracting, or trapped in endless gratuitous movement.
- Support mouse, touch, keyboard-focus equivalent, and reduced-motion/static behavior.
- Layout must protect text readability and preserve the full illustration on desktop, tablet, and mobile.
- Use BeachSound for the signature headline and Rubik for readable supporting content.

**Suggested original hero copy — use as a starting point, refine to suit the final design:**

> **I'm Eyilade. I give ideas a visual voice.**  
> I'm a senior graphic designer and creative thinker working across brand identity, visual storytelling, motion, photography, and emerging creative technology. I build work that looks considered, feels human, and communicates with purpose.

**Creative direction for copy layout:** Break the statement into expressive, intentionally placed text fragments near/around the illustration. Use restrained animation on key words or phrases, with hover responses that do not interfere with reading. Do **not** scatter text randomly or obscure the figure's face.

### 5.2 Professional skills / disciplines

Present the following as a sophisticated typographic or interactive system, not a stack of templated cards:

- Ideator / Creator
- Brand Identity
- Graphic Design
- Photography
- AI Creative Technology / Creative Technologist

Support brief, accurate explanatory text only where it helps a visitor understand capability. Do not invent quantified achievements, titles, awards, or credentials.

### 5.3 Career timeline — chronological storytelling

**Core interaction:** Build a professional, scroll-driven timeline that visibly moves from early career to current work. Use **employer logos, role, date range, location, employment type (where given), and relevant details**.

**UX requirements:**

- Chronology must be **2016 → Present**, not reverse LinkedIn order.
- Establish a legible timeline spine, progress indicator, or alternative editorial motion system that communicates progression as the page scrolls.
- Reveal each milestone using subtle vertical/horizontal motion and soft easing; emphasize the current/active milestone and make each state accessible without animation.
- Feature company logo, role/title, organization, date, and location in a strong visual hierarchy. Allow optional expansion for responsibilities without making the baseline timeline excessively tall.
- On mobile, convert gracefully to a **single-column timeline** with no horizontal scroll requirement.
- **Do not collapse concurrent roles automatically:** overlapping dates are legitimate unless later verified otherwise.
- **Do not merge Ferman Media Agency and Ferman Digital Agency** without verification; the submitted source contains both as separate entries with overlapping dates.
- Do not label an experience "remote," "on-site," or "hybrid" unless the source specifies it. Distinguish **employment type** (full-time/part-time) from **work arrangement** (hybrid/remote/on-site).
- Keep current entries marked **Present**, not a hard-coded end date.

#### Required timeline data

| # | Role | Company | Employment type | Work arrangement | Location | Dates |
|---|---|---|---|---|---|---|
| 1 | Ideator / Creator, Founder | CRG | Not specified | Not specified | Lagos, Nigeria | Mar 2016 – Present |
| 2 | Volunteer Lead ICT Director | Intelligentsia Orb Worldwide Limited | Part-time | Not specified | Nigeria | Oct 2017 – Apr 2020 |
| 3 | National Youth Service Corps (NYSC) | Federal Government | Not specified | Not specified | Gusau, Zamfara, Nigeria | Jun 2019 – May 2020 |
| 4 | Senior Graphics Designer | Running Jack IT Firm | Part-time | Not specified | Gusau, Zamfara, Nigeria | Jul 2019 – May 2020 |
| 5 | ICT Manager | Citypartner Healthcare | Full-time | Not specified | Lagos, Nigeria | Sep 2020 – Dec 2020 |
| 6 | Facilities Manager | Citypartner Healthcare | Full-time | Not specified | Lagos, Nigeria | Sep 2020 – Dec 2020 |
| 7 | Graphic Designer | Ferman Media Agency | Not specified | Not specified | Not specified | Dec 2020 – Mar 2021 |
| 8 | Graphic Designer & Motion Graphic Artist | Ferman Digital Agency | Full-time | Not specified | Lagos, Nigeria | Dec 2020 – Mar 2021 |
| 9 | Digital Content Visualiser | MaxyStuff UK | Full-time | Not specified | Not specified | Mar 2021 – Jan 2022 |
| 10 | Graphic Designer | Redot Digital Marketing and Consultancy Agency | Not specified | Not specified | Not specified | Mar 2021 – Jan 2022 |
| 11 | Graphic Designer | PwC Nigeria | Full-time | Hybrid | Lagos, Nigeria | Feb 2022 – Jul 2023 |
| 12 | Experienced Graphic Designer | PwC Nigeria | Full-time | Hybrid | Lagos, Nigeria | Jul 2023 – Jul 2025 |
| 13 | Senior Graphic Designer | PwC Nigeria | Full-time | Hybrid | Lagos, Nigeria | Jul 2025 – Present |

#### Supporting role descriptions (use in expanded timeline views if relevant)

- **CRG:** Founder / Ideator / Creator; I generate a high volume of fresh concepts.
- **Intelligentsia Orb Worldwide Limited:** Lead ICT Director. No further verified description provided.
- **NYSC:** Federal Government national service in Gusau, Zamfara; service certificate shown in source imagery.
- **Running Jack IT Firm:** Senior graphics design.
- **Citypartner Healthcare:** ICT management, facilities management, and health management consultancy for hospitals.
- **Ferman Media / Ferman Digital Agency:** Advertising creatives, graphic design, motion graphics, event and social campaign assets, content calendars, animated assets and GIFs.
- **MaxyStuff UK:** Digital content visualization, design and corporate identity.
- **Redot Digital:** Visual content/campaigns, wireframes, mockups, interactive prototypes, social scheduling, collaboration with marketing strategists, CTR/impression-informed creative refinements, and mobile/web content.
- **PwC Nigeria:** Digital/social designs, job adverts, newsletters, proposal and pitch presentations, reports, print/press assets, corporate event visuals, and multimedia deliverables. Show the **three internal career stages** as a clear professional progression rather than three unrelated employers.

> **Data integrity:** These descriptions are a summary of the provided screenshots; portions of original screenshots were cropped. Do not fabricate missing details or measurable outcomes. Where practical, leave uncertain information out of the public UI instead of showing "Not specified" to site visitors.

### 5.4 Brands I've worked with

Display the **actual brand logos** available in `Assets` for:

1. PwC
2. Dabur
3. PZ Cussons
4. Sandtex

Use an editorial logo treatment with balanced optical sizing and high-quality hover/scroll behavior. The source wording is that I worked with these brands **directly and through a marketing agency**; do not imply every logo represents a direct employment relationship.

### 5.5 Software / creative tools

Use the actual software logos/icons from the local `Assets` directory where available:

| Tool | Abbreviation |
|---|---|
| Adobe Photoshop | Ps |
| Adobe Illustrator | Ai |
| Adobe InDesign | Id |
| Adobe After Effects | Ae |
| Adobe Premiere Pro | Pr |
| Codex

Lay these out as a visually organized, responsive tool system, not an oversized list. Maintain each brand icon's recognizable identity and provide readable tool names via visible labels or accessible tooltips/labels as appropriate.

### 5.6 Conspicuous Works / Logofolio CTAs

**Remove all Works previews and Logofolio preview grids from the Home page.** Replace those sections with **two prominent animated entry points**:

- **View My Works** → existing Works route.
- **Explore Logofolio** → existing Logofolio route.

UI direction: Oversized editorial buttons or compact interactive feature tiles with an unmistakable clickable affordance. Use refined hover/tap states, elastic or eased surface motion, accent color responses, and a tactile focus state. Avoid generic arrow clutter; the CTA copy itself should be clear. Confirm route destinations rather than guessing pathnames.

### 5.7 Contact / footer

Show these exact details and make each actionable:

| Method | Value | Behavior |
|---|---|---|
| Phone | +234 811 999 5647 | `tel:+2348119995647` |
| Email | eyilade@gmail.com | `mailto:eyilade@gmail.com` |
| LinkedIn | linkedin.com/in/eyiladeoridamisi | External link to `https://linkedin.com/in/eyiladeoridamisi` |
| Behance | behance.net/eyiladeoridamisi | External link to `https://behance.net/eyiladeoridamisi` |

Keep contact visually inviting but not cluttered. Ensure icons are meaningful, consistent and accessible; show the actual contact details rather than icon-only mystery links. Do not include extraneous tracking parameters in links.

---

## 6. Logofolio page — 3-row continuous motion gallery

This page needs a significant art-direction upgrade. It should feel like a premium kinetic identity gallery, not a basic icon list or a repetitive carousel template.

### 6.1 Layout

- Use **exactly three horizontal rows** of logos as the core layout.
- Increase logos **slightly** relative to their current size; use consistent optical weight rather than enforcing the same width on every brand mark.
- Introduce much more considered **spacing**: generous row separation, consistent logo-to-logo gaps, and a breathable overall rhythm.
- Keep logos crisp and fully visible. Do not stretch, awkwardly crop, recolor, or mask marks.
- Adapt logo dimensions and spacing for tablet/mobile while retaining the three-row identity where practical.

### 6.2 Direction and seamless looping

- All three rows should continuously travel **from left to right** across the Logofolio viewport.
- Loops must be **seamless**, with no visible jump, gap, flash, or abrupt reset at the repeat boundary.
- Create a true **infinite marquee track** with enough items and duplicated/mirrored sequences for uninterrupted motion.
- Give the three rows distinct starting offsets and modestly varied speeds to avoid an overly uniform look.
- Keep the baseline motion smooth. **Use a linear translation for the infinite track** to avoid a slowdown or pause at every loop seam; reserve elegant `ease-in-out` transitions for **initial reveal, hover/focus reaction, expansion, speed changes, and other bounded interactions**. This is the technically correct way to satisfy both *continuous looping* and the desired *eased, premium feeling*.

### 6.3 Controlled variation rather than chaotic random motion

- Distribute logos across rows in a well-balanced arrangement; vary relative neighbors and start offsets so visitors do not immediately see identical patterns.
- Shuffle or reseed the logo ordering **on page initialization only**, using a stable ordering during a mounted session. If using server rendering, ensure the initial client/server sequences match to avoid hydration errors.
- Duplicate each row's **already finalized sequence** exactly to guarantee seamless continuity. Do **not** independently randomize the repeated copies or reshuffle during an active animation.
- Optionally vary subtle logo-scale/opacity reactions on interaction; do not constantly move logos out of alignment.

### 6.4 Interaction quality

- Add restrained hover and focus responses such as slight scale-up, sharpness/contrast emphasis, and a subtle eased transition.
- Optional row pause or slowdown on hover/focus is acceptable if it supports logo inspection; ensure smooth acceleration back to the base speed.
- If logos open project details, link to valid, existing project destinations. Do not fabricate click-through pages or misleading clickable states.
- Avoid introducing unnecessary modal windows or demanding user gestures simply to view logos.
- For `prefers-reduced-motion: reduce`, stop the continuous marquee and present the logos in an accessible, browsable, nonmoving arrangement.
- Respect keyboard access, logical reading order, and accessible semantics; repeated decorative track copies must not produce duplicate announcements/focus targets.

### 6.5 Implementation recommendations

- Prefer a lightweight GPU-composited CSS `transform: translate3d(...)` marquee for the logo tracks; do not use Three.js for ordinary logo translation.
- Use a correctly measured loop distance and full-track duplication to prevent visible seams, including across responsive breakpoints and when images load asynchronously.
- Use `requestAnimationFrame` only if the selected animation approach truly needs dynamic physics/control; otherwise keep it CSS-driven.
- Avoid heavy scroll-triggered reflows, image flicker, large layout shifts, and unnecessary re-renders.

---

## 7. Interaction design & motion language across the site

Define one coherent motion system so the website feels like **one designed product**.

| Interaction | Expected quality |
|---|---|
| Initial section reveal | Subtle, directional, well-paced, no exaggerated flying elements |
| Hover/tap states | Deliberate, tactile, polished, quick to respond |
| Illustration response | Responsive, delightful, restrained, graceful return to rest |
| Timeline scroll | Fluid progression with readable stages and clear active context |
| Works / Logofolio CTAs | Noticeably interactive without obscuring label or destination |
| Logofolio marquee | Seamless constant traversal; distinct row rhythms; eased secondary reactions |
| Page transitions | Minimal interruption; preserve responsiveness and navigation predictability |

Use consistent easing tokens and durations (for example, a short interactive range and a somewhat longer entrance range), but tune by actual visual testing rather than blindly applying the same animation everywhere. Respect reduced-motion preferences and avoid costly effects on low-end devices.

---

## 8. Engineering, responsiveness & quality requirements

1. **Inspect before modifying.** Review the existing app framework, components, routes, styles, dependency versions, current navigation, and asset structure. Reuse what works rather than creating duplicate UI systems.
2. **Create a phased implementation plan** before changing code: audit → design tokens/layout → Home/hero → timeline/data → Logofolio → responsive/accessibility/performance QA.
3. **Preserve functional pages.** The redesign must not break Works, Logofolio, navigation, links, or existing project content.
4. **Responsive review.** Test representative widths around **320–390 px mobile**, **768–1024 px tablet**, and **1280–1920 px desktop**, plus intermediate widths. These are validation targets, not rigid breakpoints.
5. **Accessibility.** Maintain readable contrast; keyboard/focus navigation; pointer and touch alternatives; meaningful alt text; semantic headings; accessible links; reduced-motion accommodation. Decorative illustration layers should not flood screen readers with duplicate content.
6. **Performance.** Prioritize fast first render and good Core Web Vitals. Defer nonessential 3D/interactive code, lazy-load below-the-fold media, avoid oversized images, and use lightweight transforms where possible. Pause offscreen continuous motion if it saves device resources.
7. **Motion resilience.** Ensure interactions work on low-power/mobile devices without relying on hover or sustained WebGL performance. Handle context loss or unsupported rendering cleanly.
8. **Content accuracy.** Preserve supplied spelling, dates, company associations, role names, tools, contact details and links. Flag source ambiguities; never guess.
9. **Visual cohesion.** Remove legacy styling that makes sections look like disconnected mini-sites. Use one spacing, type, color, button, icon, and motion system.
10. **No premature claims.** Do not report a feature as complete without opening/testing it. Build and lint/test the application using the project's existing commands and address actual failures.

---

## 9. Implementation acceptance checklist

### Identity and assets

- [ ] BeachSound is applied to primary display moments; Rubik is applied to UI/body/numeric content.
- [ ] `#BF9724` is used as the signature accent, with readable accessible text states.
- [ ] The root `Assets` folder has been audited and actual assets are used.
- [ ] The old personal image has been replaced with the correct Eyilade illustration.

### Navigation and Home

- [ ] Desktop, tablet, and mobile navigation are visually and functionally coherent.
- [ ] The hero prominently features the **full-pose** illustration and compelling, non-generic introductory copy.
- [ ] Hover, click/tap, keyboard and reduced-motion illustration states are supported with graceful fallback.
- [ ] The Home page presents About, skills, chronological career history, brands, tools, and contact.
- [ ] All **13** supplied timeline records appear in chronological order, with overlapping roles preserved.
- [ ] PwC's career progression from 2022 to Present is visibly clear.
- [ ] The four listed brand logos and six software tools are represented accurately.
- [ ] The Home page **does not contain** embedded Works or Logofolio galleries.
- [ ] Two prominent animated **Works** and **Logofolio** buttons navigate to working dedicated pages.

### Logofolio

- [ ] Exactly **three** continuous marquee rows are presented.
- [ ] Logos are slightly larger and more elegantly spaced than before.
- [ ] All rows move **left → right**, continuously and without seam jumps.
- [ ] Rows have differentiated offset/speed/order while remaining visually balanced.
- [ ] Animation is eased where appropriate without breaking constant marquee continuity.
- [ ] Logo assets are sharp and proportional; no distorted marks.
- [ ] Reduced-motion, mobile and keyboard behavior are functional.

### Final verification

- [ ] No dead links, missing assets, misleading interaction states, major console errors, or horizontal overflow.
- [ ] No content has been fabricated or silently altered.
- [ ] Production build and relevant checks pass.
- [ ] Desktop, tablet, mobile and reduced-motion modes have been manually reviewed.

---

## 10. Required agent handoff / completion report

After implementation, report concisely:

1. **What changed:** sections, routes, components, fonts, tokens, and animation behavior.
2. **Which assets were used:** actual filenames/paths mapped from the root `Assets` folder.
3. **How the illustration works:** clarify whether it is a Three.js-enhanced 2D illustration or a true 3D model, and describe fallbacks.
4. **How the Logofolio loops:** state row count, direction, seamless repeat strategy, offsets, and reduced-motion behavior.
5. **Validation results:** build/lint/tests and actual responsive/accessibility checks.
6. **Outstanding items:** only genuine blockers such as a missing BeachSound font file, missing illustration variant, ambiguous Ferman entries, or unavailable logo assets.

**Execution instruction:** This brief is a directive to redesign and implement the **existing live project**, not merely to create mockups, generic demo components, or a theoretical plan. Deliver a coherent, polished, functional website update grounded in the real project and the supplied local assets.
