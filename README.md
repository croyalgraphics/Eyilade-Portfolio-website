# Eyilade Oridamisi — portfolio & Web CV

An editorial portfolio with an illustration-led Web CV, thirteen chronological career records, dedicated Works and Logofolio pages, and eleven existing case studies. BeachSound and Rubik fonts, artwork, scripts and video are self-hosted.

## Development

Use Node 24 or newer. Install with `npm ci --cache /private/tmp/eyilade-npm-cache`, then run `npm run build` and `npm run dev`. Preview: http://127.0.0.1:4173.

`npm run check` validates metadata, image dimensions, internal links/assets, nineteen logo families, thirteen career records, exactly six tools, Home gallery boundaries and private-content boundaries.

## Editing

- `src/`: page templates, shared interactions and design tokens/styles.
- `content/career.json`: chronological source data; concurrent roles remain distinct.
- `content/projects.json`: existing project descriptions and galleries.
- `content/logos.json`, `content/master-assets.json`: prepared artwork metadata.
- `scripts/prepare_master_assets.py`: reproducible artwork/font preparation from local `Assets/`.
- `scripts/build.mjs`: generation and bundling; output in `dist/`.
- `docs/MASTER_ASSET_MAP.json`: source mapping, variant decisions, sizes and hashes.
- `docs/MASTER_REDESIGN_IMPLEMENTATION.md`: implementation decisions and verification.

Original `Assets/` stay local and unchanged. Optimised derivatives and curated downloads are in `dist/assets/`. Public CV/selected-work PDFs exclude private software ideas. New career data follows the supplied master brief; the PDF CV is a separate existing download.

## Interaction

The navigation uses a travelling capsule and native mobile disclosure. The supplied character is a 2D illustration with bounded pointer/click feedback; no rigged model is claimed. Desktop career history supports native horizontal scrolling, keyboard and Earlier/Later controls; phones show a vertical timeline.

Logofolio has exactly three CSS rows moving left to right. Each row duplicates its finalised sequence exactly, with different durations and initial offsets. A complete still index, motion switch, device reduced-motion support and row pause controls provide alternatives. Repeated copies are noninteractive and hidden from assistive technology. The former Three.js room remains unused source and is excluded from the build.

Works filters, native image dialogs, contact links and email copying require no backend. No tracking scripts or external runtime resources are loaded. No fake form submissions or success states are used.

## Hosting

Reuse the project in `.openai/hosting.json`. Preserve the existing owner-only audience unless the owner explicitly changes sharing. Source packaging and publication use the Sites workflow, with credentials kept in memory/stdin only.
