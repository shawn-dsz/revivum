# Revivum Session Handoff (Mac -> Henry)

**Date:** 2026-04-07
**From:** Quince (Claude Code on Mac, session red)
**To:** Fresh Claude Code session on Henry

## What this project is

Marketing website for **Revivum** - an Australian peptide therapeutics company operating as a TGA-Registered Sponsor. Headless Ghost CMS (not yet provisioned) + Astro 5 static frontend + single Vercel serverless function for lead form POSTs. Deploy target: Vercel. Two audiences: patients and medical practitioners (AHPRA-verified).

Source-of-truth docs:
- `docs/BUILD-PLAN.md` - full stack plan
- `docs/CONTRACT.md` - working doc (LIVES IN CADRE CONSULTING, do not touch)
- `revivum-mvp-wireframe.html` - original 628-line greyscale wireframe. **IA reference only, not visual reference.**
- `docs/design-v2.html` - the new visual direction (see below)

## Current state on origin/main

Last commit: `0e6192f docs: add v2 homepage design mock`

Committed and pushed:
- Astro scaffold, tokens, fonts, BaseLayout shell
- Ghost Content API client + settings parser (`src/lib/ghost.ts`, `src/lib/settings.ts`)
- Vercel adapter + stubbed `/api/leads` Zod-validated endpoint (patient + practitioner discriminated union)
- Homepage sections (`src/components/home/*`) + `src/pages/index.astro`
- Patients page (`src/components/patients/*`) + `src/pages/patients.astro`
- `docs/design-v2.html` - v2 homepage mock

**NOT yet committed anywhere** (only exist in Shawns Mac working tree):
- `src/components/practitioners/*` + `src/pages/practitioners.astro`
- `src/components/about/*` + `src/pages/about.astro`
- `src/pages/privacy.astro`, `src/pages/terms.astro`

These files were built by Wave 2 agents but never pushed because the client rejected the wireframe-literal visual direction before we could commit them. They will likely be rebuilt against the v2 design system rather than salvaged - do not restore them from the Mac unless Shawn asks.

## Why we pivoted to design v2

The first build faithfully reproduced the greyscale wireframe (grey placeholder bars, mock nav rectangles, 11px Courier Prime labels, dashed rules). Client feedback: "it doesn look professional. it looks like wireframe, its not ok."

Root cause: the wireframe was drawn to *look* like a wireframe (for stakeholder IA review). Translating it 1:1 into real CSS inherited the "unfinished" feeling.

## The v2 direction - `docs/design-v2.html`

Self-contained 1633-line HTML mock. Editorial clinical direction. Reference points: Eucalyptus Health, Hone Health, Juniper, Ro. **Not** wellness-startup energy.

Visual system:
- **Type:** Playfair Display (display headings, sparingly) + DM Sans (everything else). Courier Prime DROPPED entirely - it was reading as wireframe annotation.
- **Scale:** 16-17px body, section headings `clamp(32px, ..., 80px)`.
- **Colour:** Ink `#0F1A14` dominant. Moss `#3A5C47` as single confident accent. Parchment `#EDE8DF` + fog `#F4F1EC` for section rhythm. Amber `#B87333` used once, on the TGA disclaimer badge.
- **Imagery:** Real Unsplash URLs (clinical/scientific, not stock smiling doctors).
- **Layout:** Full-width. Two-column asymmetric hero. Audience router as two differentiated cards (patient sage, practitioner slate-blue). Compliance section on dark ink. Four-column footer.
- **Motion:** 150-180ms hover transitions only. No entrance animations.

Open it in a browser to see it:

    xdg-open docs/design-v2.html   # or just scp it to the Mac

## What Shawn needs next

He has not yet reacted to `docs/design-v2.html` in detail. Two possible paths:

### Path A - iterate on the mock (cheap)
If he wants changes to the v2 direction, edit `docs/design-v2.html` directly. Its one self-contained HTML file, no build step. This is the right path until he says "ship it".

### Path B - port v2 into Astro (expensive)
Once the mock is approved:

1. **Throw away the existing `src/styles/tokens.css` and `global.css`** - they encode the wireframe palette vocabulary. Rebuild from the v2 mock.
2. **Delete Courier Prime** from the font imports in `src/layouts/BaseLayout.astro`.
3. **Rebuild all 6 pages** against the v2 design system:
   - Homepage (`src/components/home/*`) - currently committed, needs replacement
   - Patients (`src/components/patients/*`) - currently committed, needs replacement
   - Practitioners - not committed, build fresh
   - About - not committed, build fresh
   - Privacy / Terms - not committed, build fresh
4. **Keep the following intact** (they are not design-concerned):
   - `src/lib/ghost.ts` and `src/lib/settings.ts` - Ghost CMS client
   - `src/pages/api/leads.ts` - Zod-validated serverless endpoint
   - `astro.config.mjs` - must stay `output: static` with `prerender = false` only on `/api/leads`
   - `.gitignore`
5. **Dispatch a swarm of parallel agents** for the page rebuild once the design system is in place (see Wave 2 pattern from earlier - one agent per page, disjoint file ownership, integration pass at the end).

## Toolchain on Henry

Verified working as of handoff:
- Node v22.22.2 (matches Vercel runtime)
- pnpm 10.33.0 (via corepack)
- git 2.43.0
- `pnpm install` + `pnpm build` both pass from a fresh clone

Not yet verified:
- Claude CLI on PATH in non-interactive shell (fish PATH issue, not a blocker)
- Ghost Content API env vars (`GHOST_CONTENT_API_URL`, `GHOST_CONTENT_API_KEY`) - not set, Ghost client is null-safe so build still works

## Rules of engagement (from Shawns global CLAUDE.md)

- British English in commit messages
- No em dashes or en dashes
- Use the `/commit` skill for all commits, never `git commit` direct
- No AI attribution in commits
- Logical commits grouped by intent, not one big commit
- Commit format: `type(scope): summary` with What:/Why: body sections

## Deferred tasks from earlier

- Task #10: Mobile responsive pass + README - blocked on v2 design direction landing
- Pricing analysis (Shawn said he would set up a separate agent)
- "Send a message" task (Shawn said he would come back to it)

## How to resume

1. Read this file
2. Read `docs/design-v2.html` to understand the target visual direction
3. Ask Shawn: "Have you reviewed docs/design-v2.html yet? Any changes needed before I rebuild the Astro components against it?"
4. Do NOT start rebuilding components until he explicitly approves the v2 mock.

