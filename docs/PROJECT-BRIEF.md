# Revivum — Project Brief & Technical Plan

**Project:** Revivum MVP Marketing Website
**Client:** [Client Name] / Revivum Pty Ltd
**Provider:** Cadre
**Date:** 29 March 2026
**Version:** 1.0

---

## 1. Background & Context

Revivum is an Australian peptide therapeutics company being incorporated by the client and their business partner (Kristen). The company will operate as a TGA-Registered Sponsor — not a clinic — providing regulated infrastructure that connects patients and practitioners to lawful peptide-based therapeutics in Australia.

The client has engaged Cadre to build the initial MVP marketing website. The business is pre-revenue and pre-incorporation, with the immediate goal of establishing an online presence to:

- Attract patient enquiries
- Attract practitioner sign-ups
- Present a professional, regulation-compliant image
- Capture leads for manual follow-up (phone calls, doctor referrals)

### Key Context from Discovery Call

- **Branding is TBD.** The client's business partner (Kristen) will handle branding. The site will launch with a placeholder design system (wireframe-quality) that can be reskinned later.
- **No CRM yet.** Lead capture goes to Google Sheets (equivalent of Excel). CRM integration is a future phase.
- **Regulatory sensitivity.** The site must comply with TGA (Therapeutic Goods Administration) advertising regulations. No promotional claims about therapeutic goods. Disclaimers on every page.
- **"Fail forward fast" mentality.** Get something live, iterate with marketing content later. Don't overthink the initial build.
- **Domain already secured.** The client owns the domain (revivum.com.au). DNS hookup to be handled separately after preview approval.
- **Marketing content will be provided later.** The current build uses placeholder copy aligned to the wireframe.

---

## 2. MVP Scope — What We're Building

A **4-page static marketing website** with lead capture forms, deployed to Vercel.

### Pages

| Page | URL | Purpose |
|------|-----|---------|
| Homepage | `/` | Hero, audience router (patient vs practitioner), trust section, CTA |
| For Patients | `/patients` | Peptide education, how it works, patient lead capture form |
| For Practitioners | `/practitioners` | Value propositions, credentials, practitioner sign-up form |
| About | `/about` | Mission statement, company role, credentials CTA |
| Privacy Policy | `/privacy` | Legal placeholder (copy to be provided by client) |
| Terms of Use | `/terms` | Legal placeholder (copy to be provided by client) |

### Lead Capture

Two forms submit to a single API endpoint (`POST /api/leads`) which writes rows to a Google Sheet:

**Patient Lead Form:**
- First name, last name, email, phone, state, referral source (optional), message (optional)
- Consent checkbox (mandatory)

**Practitioner Sign-Up Form:**
- First name, last name, AHPRA registration number, specialty, email, state, practice name (optional)
- AHPRA verification consent (mandatory), contact consent (mandatory), marketing consent (optional)

Both forms are validated client-side (react-hook-form + zod) and server-side (zod) before writing to Google Sheets.

### What's NOT Included (Future Phases)

- CRM integration
- E-commerce / product ordering
- Payment processing
- Patient portal / practitioner dashboard
- Blog / content management
- Email automation / drip campaigns
- SEO optimisation beyond basic meta tags
- Custom branding (logo, brand colours, typography — client to provide)
- Marketing copy (client to provide; current copy is placeholder)
- Legal copy for privacy/terms pages (client to provide)

---

## 3. Technical Architecture

### Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Framework | Next.js 16 (App Router) | Industry standard, SSR/SSG, Vercel-optimised |
| Language | TypeScript | Type safety, better DX |
| Styling | Tailwind CSS v4 | Utility-first, rapid development |
| Forms | react-hook-form + zod | Validation, type safety |
| Lead Storage | Google Sheets API v4 | Zero-cost, accessible to non-technical team |
| Hosting | Vercel (Free/Pro) | Zero-config deploys, global CDN, serverless functions |

### Design System (Placeholder)

The site ships with a curated wireframe aesthetic:

- **Fonts:** Playfair Display (headings), DM Sans (body), Courier Prime (labels/monospace)
- **Palette:** Dark ink (#0F1A14), moss green (#3A5C47), fog (#F4F1EC), parchment (#EDE8DF)
- **Audience colours:** Patient (green tones), Practitioner (blue tones)

This design system is built with CSS custom properties, making it trivial to reskin when branding is finalised.

### File Structure

```
revivum/
├── app/
│   ├── layout.tsx              # Root layout — nav, footer, TGA disclaimer
│   ├── page.tsx                # Homepage
│   ├── patients/page.tsx       # Patient page
│   ├── practitioners/page.tsx  # Practitioner page
│   ├── about/page.tsx          # About page
│   ├── privacy/page.tsx        # Privacy placeholder
│   ├── terms/page.tsx          # Terms placeholder
│   └── api/leads/route.ts      # Lead capture API endpoint
├── components/
│   ├── layout/                 # NavBar, Footer, TgaDisclaimer
│   ├── ui/                     # Button, SectionTag, ComplianceBox
│   ├── home/                   # Homepage sections (5 components)
│   ├── patients/               # Patient page sections (4 components)
│   ├── practitioners/          # Practitioner page sections (4 components)
│   └── about/                  # About page sections (3 components)
├── lib/
│   ├── schemas.ts              # Zod validation schemas
│   └── sheets.ts               # Google Sheets API helper
├── styles/globals.css          # Design tokens + Tailwind
└── .env.local.example          # Environment variable template
```

### Component Count

| Category | Components |
|----------|-----------|
| Layout | 3 (NavBar, Footer, TgaDisclaimer) |
| UI Primitives | 3 (Button, SectionTag, ComplianceBox) |
| Homepage | 5 (Hero, AudienceRouter, WhatWeAre, TrustBand, GlobalCta) |
| Patients | 4 (PatientHero, WhatArePeptides, HowItWorks, PatientLeadForm) |
| Practitioners | 4 (PractitionerHero, WhatWeProvide, Credentials, PractitionerSignUpForm) |
| About | 3 (MissionSection, OurRole, CredentialsCta) |
| **Total** | **22 components** |

Plus: 2 library modules, 1 API route, 6 page files, 1 root layout, 1 CSS file.

---

## 4. TGA Compliance Measures

The site implements these compliance safeguards:

1. **Global disclaimer bar** on every page (TgaDisclaimer component in root layout)
2. **ComplianceBox** components on patient-facing content sections
3. **No promotional claims** about therapeutic efficacy — copy uses neutral, educational language
4. **"Not a clinic" positioning** — clearly states Revivum is infrastructure, not a provider
5. **Consent checkboxes** on all forms — mandatory before submission
6. **Privacy placeholder** — client to provide privacy policy text (Kristen has one from previous ventures)

**Note:** Cadre is not a legal firm and does not provide legal advice. All compliance copy should be reviewed by the client's legal counsel before going live.

---

## 5. Delivery Timeline

| Milestone | Deliverable | Target |
|-----------|------------|--------|
| M1 | Project scaffold, design tokens, env setup | Day 1 |
| M2 | Lead capture API + Google Sheets integration | Day 1 |
| M3 | Layout components (nav, footer, disclaimer) | Day 1-2 |
| M4 | Homepage (all 5 sections) | Day 2 |
| M5 | Patients page + lead form | Day 2-3 |
| M6 | Practitioners page + sign-up form | Day 3 |
| M7 | About page | Day 3 |
| M8 | Privacy/Terms placeholders | Day 3 |
| M9 | Mobile responsive pass + QA | Day 4 |
| M10 | Vercel preview deployment for client review | Day 4 |

**Estimated total build time:** 3-4 working days

---

## 6. Client Responsibilities

The client is responsible for providing:

- [ ] Google Cloud service account credentials (for Sheets API)
- [ ] Google Sheet ID (with "Patient Leads" and "Practitioner Leads" tabs created)
- [ ] Privacy policy text
- [ ] Terms of use text
- [ ] Final branding assets when available (logo, colours, fonts)
- [ ] Final marketing copy when available
- [ ] Domain DNS configuration (or credentials for Cadre to configure)
- [ ] Review and approval of TGA compliance copy with legal counsel

---

## 7. Assumptions & Risks

| Assumption | Risk if Wrong |
|-----------|--------------|
| Google Sheets is sufficient for lead storage at launch volumes | Need to bring forward CRM integration |
| Client has/will obtain Google Cloud service account | Delays API integration |
| TGA compliance copy is sufficient for MVP | May need legal review before launch |
| Vercel free tier is adequate for initial traffic | May need Pro plan ($20/mo) |
| No custom animations or interactions needed | Would add scope |
| Content is static (no CMS) | Content updates require developer involvement |
