# Revivum Website — Build Plan (v2: Headless Ghost)

**Status:** Draft for approval
**Author:** Rhodium (Claude)
**Date:** 2026-04-07
**Supersedes:** v1 (Hugo plan) and the Next.js stack in `docs/PROJECT-BRIEF.md` §3

---

## 1. Decisions (locked from your answers)

| # | Decision | Choice |
|---|---|---|
| 1 | Architecture | **Headless Ghost** — Ghost as content backend, separate static frontend |
| 2 | Ghost hosting | **Ghost(Pro)** — managed, ~$9-25 USD/month, zero ops |
| 3 | Primary goal | **Client edits all visible copy without a developer** |
| 4 | Frontend SSG | **Astro** (recommended) — build-time content fetch, ships zero JS by default, first-class Tailwind+DaisyUI support, free deploy on Vercel/Netlify/Cloudflare |
| 5 | CSS framework | **Tailwind v4 + DaisyUI** (per your earlier decision) |
| 6 | Frontend hosting | **Vercel** (per original quote) — Astro deploys zero-config, free tier covers MVP traffic |
| 7 | Repo layout | **Greenfield in `/Users/shawn/proj/revivum/`** alongside `docs/` and the wireframe HTML |
| 8 | Forms | Stub `/api/leads` Vercel function today; wire to Google Sheets when client provides creds |

> If you'd rather use **Eleventy** instead of Astro (smaller, simpler, also great Ghost integration), say so and I'll swap. Astro is the default because of its component model and zero-JS-by-default policy — both useful for keeping the site fast.

---

## 2. The Big Idea: editable content model

**Everything the client should be able to edit lives in Ghost. Everything else lives in code.**

### What goes in Ghost (editable)

| Ghost entity | Used for | Editable fields |
|---|---|---|
| **Page: "Home"** (slug `home`) | Homepage hero + body content | Title, excerpt (= hero subtitle), feature image, body (= mission/what-we-are sections via Ghost's editor) |
| **Page: "For Patients"** (slug `patients`) | Patient page body | Title, excerpt, feature image, body (peptides intro, how-it-works steps) |
| **Page: "For Practitioners"** (slug `practitioners`) | Practitioner page body | Title, excerpt, feature image, body (value props, credentials) |
| **Page: "About"** (slug `about`) | About page body | Title, excerpt, body (mission, role) |
| **Page: "Privacy Policy"** (slug `privacy`) | Legal | Title, body |
| **Page: "Terms of Use"** (slug `terms`) | Legal | Title, body |
| **Page: "Site Settings"** (slug `_settings`, hidden from nav) | Global strings — nav CTAs, footer text, TGA disclaimer copy, contact email/phone | Body parsed as key:value blocks |
| **Posts** (later) | Blog/news, when ready | Standard Ghost post fields |
| **Tags** | Section labels (e.g. `audience-patient`, `audience-practitioner`) | Used to filter and route content |
| **Navigation** (Ghost's built-in) | Header links, footer links | Edited in Ghost admin → Settings → Navigation |

### What stays in code (not editable)

- Page **layout and structure** (where the hero sits, how the audience-router grid is arranged)
- **Design tokens** (colours, fonts, spacing — wireframe palette)
- **Forms** (field definitions, validation rules, submit logic)
- **TGA disclaimer placement** (the *copy* of the disclaimer is editable via the `_settings` page; the *position* is hard-coded)
- **Image assets** that ship with the site (logo, favicons)

### Why a `_settings` page?

Ghost doesn't have a "global custom fields" feature. The clean workaround is a hidden Ghost Page whose body is parsed as key:value pairs at build time:

```
nav_cta_label: Contact Us
footer_email: hello@revivum.com.au
footer_phone: +61 2 0000 0000
tga_disclaimer: Revivum is a TGA-Registered Sponsor and not a clinic...
```

The Astro build reads this page once and exposes it as a global `site` object available to every component. Client edits one page in Ghost admin → all globals update site-wide on next build.

---

## 3. Architecture diagram (in words)

```
┌─────────────────────────────┐         ┌──────────────────────────┐
│  Ghost(Pro) at               │  HTTPS  │  Astro frontend          │
│  cms.revivum.com.au          │ ──────> │  on Vercel                │
│  ─ admin UI (client logs in) │ Content │  ─ revivum.com.au         │
│  ─ MySQL (managed)           │   API   │  ─ static HTML output     │
│  ─ Members API (later)       │         │  ─ /api/leads function    │
└─────────────────────────────┘         └──────────────────────────┘
        │                                        ▲
        │ webhook on publish                     │
        └────────────────────────────────────────┘
              triggers Vercel rebuild

                                                 │ POST
                                                 ▼
                                    ┌─────────────────────────┐
                                    │  Google Sheets          │
                                    │  (when creds provided)  │
                                    └─────────────────────────┘
```

**Flow when the client edits a page:**
1. Client logs into `cms.revivum.com.au/ghost`
2. Edits the "Home" Page, hits Publish
3. Ghost fires `post.published`/`page.published` webhook → Vercel deploy hook
4. Vercel rebuilds the Astro site (~30 seconds)
5. New content live on `revivum.com.au`

---

## 4. Stack & file layout

```
revivum/
├── astro.config.mjs              # Astro config: integrations (tailwind), output: 'static'
├── package.json                  # astro, @astrojs/tailwind, tailwindcss, daisyui, @tryghost/content-api
├── tailwind.config.mjs           # DaisyUI plugin + custom 'revivum' theme mapped to wireframe palette
├── tsconfig.json
├── .env.example                  # GHOST_URL, GHOST_CONTENT_API_KEY
├── public/
│   └── (favicons, og-image once provided, fonts if self-hosted)
├── src/
│   ├── lib/
│   │   ├── ghost.ts              # Ghost Content API client + typed wrappers
│   │   ├── settings.ts           # parses the _settings Ghost Page into a typed object
│   │   └── schemas.ts            # Zod schemas for the two lead forms
│   ├── layouts/
│   │   └── BaseLayout.astro      # <html>, <head>, header, footer, TGA disclaimer slot
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.astro
│   │   │   ├── Footer.astro
│   │   │   └── TgaDisclaimer.astro
│   │   ├── ui/
│   │   │   ├── Button.astro
│   │   │   ├── SectionTag.astro
│   │   │   └── ComplianceBox.astro
│   │   ├── home/
│   │   │   ├── Hero.astro
│   │   │   ├── AudienceRouter.astro
│   │   │   ├── WhatWeAre.astro
│   │   │   ├── TrustBand.astro
│   │   │   └── GlobalCta.astro
│   │   ├── patients/
│   │   │   ├── PatientHero.astro
│   │   │   ├── WhatArePeptides.astro
│   │   │   ├── HowItWorks.astro
│   │   │   └── PatientLeadForm.astro
│   │   ├── practitioners/
│   │   │   ├── PractitionerHero.astro
│   │   │   ├── WhatWeProvide.astro
│   │   │   ├── Credentials.astro
│   │   │   └── PractitionerSignUpForm.astro
│   │   └── about/
│   │       ├── MissionSection.astro
│   │       ├── OurRole.astro
│   │       └── CredentialsCta.astro
│   ├── pages/
│   │   ├── index.astro           # fetches Ghost page slug 'home', renders home components
│   │   ├── patients.astro
│   │   ├── practitioners.astro
│   │   ├── about.astro
│   │   ├── privacy.astro
│   │   ├── terms.astro
│   │   └── api/
│   │       └── leads.ts          # Vercel serverless function — stubbed
│   └── styles/
│       ├── tokens.css            # CSS custom properties from wireframe
│       └── global.css            # @import "tailwindcss"; @plugin "daisyui";
├── .gitignore
└── README.md                     # how to run, .env setup, deploy notes, content model docs
```

---

## 5. Design tokens (direct port from wireframe)

```css
/* src/styles/tokens.css */
:root {
  --ink:#0F1A14; --moss:#3A5C47; --moss-lt:#5A7D69;
  --fog:#F4F1EC; --parchment:#EDE8DF; --white:#FAFAF8;
  --rule:#D9D4CC; --muted:#8A8478;
  --label-p:#2E5C48; --label-dr:#2C3E6B;
  --bg-p:#EAF2EC; --bg-dr:#EAEEF6;
  --amber:#B87333; --red:#922; --green:#2E6B3E;
}
```

DaisyUI custom theme `revivum` maps `primary → --moss`, `neutral → --ink`, `base-100 → --fog`. Fonts loaded via Google Fonts `<link>` in `BaseLayout.astro` (Playfair Display, DM Sans, Courier Prime — same as wireframe).

---

## 6. Forms — same as before

Both forms POST JSON to `/api/leads` with a `kind` discriminator (`patient` | `practitioner`). Client-side validation in vanilla JS, server-side mirror via Zod. Stub function returns `200 { ok: true }` and logs the payload until creds arrive. AHPRA format check: 3 letters + 10 digits.

---

## 7. Build sequence (revised for Astro + Ghost)

| Step | Output | Verifiable by |
|---|---|---|
| 1 | Astro scaffold + Tailwind v4 + DaisyUI wired in | `pnpm dev` runs, blank styled page |
| 2 | Design tokens + custom DaisyUI `revivum` theme + fonts | Palette and type match wireframe |
| 3 | `BaseLayout.astro` shell — header, footer, disclaimer slot | All routes inherit shell |
| 4 | Ghost Content API client (`src/lib/ghost.ts`) with typed wrappers | `pnpm dev` fetches Pages from a real or mocked Ghost instance |
| 5 | `_settings` page parser (`src/lib/settings.ts`) | Returns typed `Settings` object from Ghost |
| 6 | Homepage: 5 sections wired to Ghost Page `home` content | Visual diff vs wireframe at 1280px and 375px |
| 7 | Patients page + lead form (stub submit) | Form validates and POSTs successfully |
| 8 | Practitioners page + signup form (stub submit) | Form validates and POSTs successfully |
| 9 | About page wired to Ghost Page `about` | Renders content from Ghost |
| 10 | Privacy + Terms pages wired to Ghost Pages | Render with placeholder copy from Ghost |
| 11 | Mobile responsive pass — nav toggle, form layout, padding | Chrome devtools 375 / 768 / 1280 |
| 12 | `/api/leads` Vercel function stub with payload logging | `curl -X POST .../api/leads` returns 200 |
| 13 | README: local dev, env vars, content model, Ghost setup, Vercel deploy hook config | New dev or client editor can follow it cold |
| 14 | Commit cleanup — logical commits per `/commit` workflow | `git log` shows clean history |

Each step is one commit. Step 4 onwards depends on having a Ghost instance to fetch from — see §8.

---

## 8. Ghost instance — what we do during the build

You have two options for the build phase:

**(a) Local Ghost via Docker** — I spin up Ghost in Docker on your machine, seed it with the placeholder Pages and `_settings` content, point Astro at `http://localhost:2368`. Zero cost, exact production behaviour. **Recommended for the build.**

**(b) Sign up for Ghost(Pro) trial today** — 14-day free trial, gives you the real `revivum.ghost.io` URL immediately. Switches to paid before the trial ends. Worth doing **before launch** but not strictly needed during the build.

I'd do **(a) during the build**, then **(b) right before client handover**, with a one-shot script to export Pages from local and re-import into Ghost(Pro).

---

## 9. What's editable vs hard-coded — explicit map

This is the contract with the client. If they ask "can I change X", the answer should already be in this table.

| Element | Editable in Ghost? | How |
|---|---|---|
| Page titles | Yes | Page → Title |
| Hero subtitles | Yes | Page → Excerpt |
| Body copy on every page | Yes | Page → Body (Ghost editor) |
| Hero images | Yes | Page → Feature Image |
| Nav links (label + URL) | Yes | Settings → Navigation |
| Footer links | Yes | Settings → Secondary Navigation |
| Footer email/phone | Yes | `_settings` Page → key:value |
| TGA disclaimer copy | Yes | `_settings` Page → key:value |
| Primary CTA labels (e.g. "Find a Practitioner") | Yes | `_settings` Page → key:value |
| Site title, meta description | Yes | Ghost → General Settings |
| Brand colours | **No** (hard-coded in Tailwind theme) | Developer change |
| Fonts | **No** (hard-coded) | Developer change |
| Page layout / section order | **No** (hard-coded) | Developer change |
| Form fields | **No** (hard-coded in Astro components) | Developer change |
| Adding/removing entire pages | **No, not without dev help** | Adding pages requires a new Astro route file |

Documented in the README so the client knows the boundaries up front.

---

## 10. Hosting & cost (monthly, AUD-ish)

| Component | Service | Cost |
|---|---|---|
| Ghost CMS | Ghost(Pro) Starter | ~$14 USD/mo (~$22 AUD) |
| Frontend hosting | Vercel Hobby | $0 (free tier covers MVP traffic) |
| Domain | revivum.com.au | client owns |
| Google Sheets API | Google Cloud free tier | $0 |
| **Total runtime** | | **~$22 AUD/month** |

Worth flagging to the client before they sign — the original quote didn't include CMS hosting. This is a real ongoing cost they need to know about.

---

## 11. Out of scope for this build (defer)

- Real Google Sheets write (waiting on creds)
- Final privacy/terms copy (waiting on legal — placeholder Pages will exist in Ghost)
- Real branding (logo, final colours) — wireframe palette stands in
- DNS cutover to revivum.com.au and cms.revivum.com.au
- Ghost(Pro) signup and content migration from local → cloud
- Vercel deploy (config scaffolded, but no push without your nod)
- Webhook wiring (Ghost → Vercel rebuild hook)
- Ghost Members / newsletters (later phase)
- Blog posts (later phase)

---

## 12. Risks

| Risk | Mitigation |
|---|---|
| Ghost(Pro) cost surprises the client | Flag in handover doc; offer self-hosted Ghost as alt |
| Client edits Ghost body but layout assumes specific structure | `_settings` page pattern + clear README + lock layout to Ghost fields, not free-form HTML |
| Webhook rebuilds are slow or flaky | Webhook is async; client sees "publishing..." state; fallback is daily scheduled rebuild |
| DaisyUI components don't match wireframe aesthetic | Override DaisyUI theme tokens; fall back to raw Tailwind for bespoke sections |
| Astro + Ghost integration has version drift | Pin `@tryghost/content-api` and Astro versions in `package.json` |
| TGA copy in wireframe is placeholder | Already flagged in brief — README will require legal review pre-launch |

---

## 13. What I need from you to start

1. **Confirm Astro** as the frontend SSG (vs Eleventy). Default is Astro.
2. **Confirm option (a)** — local Docker Ghost during the build, Ghost(Pro) at handover. (Or say (b) and I'll wait for trial credentials.)
3. **Green-light Step 1** (Astro scaffold + Tailwind/DaisyUI wiring) and I begin.

Pricing and the message remain parked.
