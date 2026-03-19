# Revivum Website — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Revivum Phase 1 MVP marketing website — a TGA-compliant, 4-page static Next.js site that captures patient and practitioner leads into Google Sheets.

**Architecture:** Next.js 15 App Router deployed to Vercel as a standard Next.js project (no `output: 'export'`). Static pages are automatically CDN-cached by Vercel at the edge. Forms POST to a Next.js API route (`/api/leads`) that writes tagged rows to Google Sheets via the Sheets API v4. The API route runs as a Vercel serverless function.

**Tech Stack:** Next.js 15, TypeScript, Tailwind CSS v4, Google Sheets API v4 (`googleapis`), Vercel (hosting), `react-hook-form` (form validation), `zod` (schema validation)

---

## File Map

```
revivum/
├── app/
│   ├── layout.tsx              # Root layout — nav, footer, TGA disclaimer, global fonts
│   ├── page.tsx                # Homepage /
│   ├── patients/
│   │   └── page.tsx            # /patients
│   ├── practitioners/
│   │   └── page.tsx            # /practitioners
│   ├── about/
│   │   └── page.tsx            # /about
│   ├── privacy/
│   │   └── page.tsx            # /privacy (placeholder)
│   ├── terms/
│   │   └── page.tsx            # /terms (placeholder)
│   └── api/
│       └── leads/
│           └── route.ts        # POST handler → Google Sheets
├── components/
│   ├── layout/
│   │   ├── NavBar.tsx          # Top navigation + sticky CTA
│   │   ├── Footer.tsx          # Footer with nav + legal links
│   │   └── TgaDisclaimer.tsx   # Bottom disclaimer bar (every page)
│   ├── ui/
│   │   ├── Button.tsx          # btn-primary, btn-outline, btn-dr variants
│   │   ├── SectionTag.tsx      # Eyebrow labels (monospace, uppercase)
│   │   └── ComplianceBox.tsx   # Amber warning box for TGA notices
│   ├── home/
│   │   ├── HeroSection.tsx     # §1 — dual CTA hero
│   │   ├── AudienceRouter.tsx  # §2 — patient/practitioner split cards
│   │   ├── WhatWeAre.tsx       # §3 — 3 role cards
│   │   ├── TrustBand.tsx       # §4 — dark compliance commitment section
│   │   └── GlobalCta.tsx       # §5 — repeat CTA at page bottom
│   ├── patients/
│   │   ├── PatientHero.tsx     # §1 — education hero
│   │   ├── WhatArePeptides.tsx # §2 — 3 info cards
│   │   ├── HowItWorks.tsx      # §3 — 3-step flow
│   │   └── PatientLeadForm.tsx # §4 — lead capture form
│   ├── practitioners/
│   │   ├── PractitionerHero.tsx      # §1 — dark hero
│   │   ├── WhatWeProvide.tsx         # §2 — 4 value prop cards
│   │   ├── Credentials.tsx           # §3 — regulatory credentials
│   │   └── PractitionerSignUpForm.tsx # §4 — sign-up form
│   └── about/
│       ├── MissionSection.tsx   # §1 — mission statement
│       ├── OurRole.tsx          # §2 — 3 role cards
│       └── CredentialsCta.tsx   # §3 — dark credentials + CTA
├── lib/
│   ├── sheets.ts               # Google Sheets write helper
│   └── schemas.ts              # Zod schemas for both lead forms
├── styles/
│   └── globals.css             # CSS custom properties (design tokens) + Tailwind base
├── public/
│   └── fonts/                  # Self-hosted font files (optional — Google Fonts CDN OK for MVP)
├── .env.local.example          # Template for required env vars
├── next.config.ts
├── tailwind.config.ts
└── tsconfig.json
```

---

## Task 1: Project Scaffold

**Files:**
- Create: `package.json`, `next.config.ts`, `tailwind.config.ts`, `tsconfig.json`
- Create: `styles/globals.css`
- Create: `.env.local.example`

- [ ] **Step 1: Bootstrap Next.js project**

```bash
cd /Users/shawn/proj/revivum
npx create-next-app@latest . \
  --typescript \
  --tailwind \
  --app \
  --src-dir=false \
  --import-alias="@/*" \
  --yes
```

Expected: Next.js project files created in `/Users/shawn/proj/revivum`

- [ ] **Step 2: Install additional dependencies**

```bash
npm install react-hook-form zod @hookform/resolvers googleapis
```

- [ ] **Step 3: Verify next.config.ts (no static export)**

`create-next-app` generates a valid `next.config.ts`. Leave it as-is — do NOT add `output: 'export'`. Vercel automatically CDN-caches static pages, so there is no need for a static export. The API route (`/api/leads`) will run as a Vercel serverless function.

The default generated file looks like:
```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {}

export default nextConfig
```

Leave it exactly like this.

- [ ] **Step 4: Wire up design tokens in globals.css**

Replace `styles/globals.css` (or `app/globals.css`) with:

```css
@import "tailwindcss";

:root {
  /* Colour palette */
  --color-ink:           #0F1A14;
  --color-moss:          #3A5C47;
  --color-moss-light:    #5A7D69;
  --color-fog:           #F4F1EC;
  --color-parchment:     #EDE8DF;
  --color-white:         #FAFAF8;
  --color-rule:          #D9D4CC;
  --color-muted:         #8A8478;
  --color-amber:         #B87333;

  /* Audience: Patient */
  --color-patient-text:  #2E5C48;
  --color-patient-bg:    #EAF2EC;
  --color-patient-border:#B8D9C4;

  /* Audience: Practitioner */
  --color-doctor-text:   #2C3E6B;
  --color-doctor-bg:     #EAEEf6;
  --color-doctor-border: #B8C4D9;

  /* Typography */
  --font-serif: 'Playfair Display', Georgia, serif;
  --font-sans:  'DM Sans', system-ui, sans-serif;
  --font-mono:  'Courier Prime', 'Courier New', monospace;

  /* Layout */
  --max-content: 860px;
  --form-max:    480px;
}

body {
  font-family: var(--font-sans);
  background: var(--color-white);
  color: var(--color-ink);
}
```

- [ ] **Step 5: Add Google Fonts to root layout head**

In `app/layout.tsx`, add to the `<head>`:

```tsx
<link
  href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&family=Courier+Prime:wght@400;700&display=swap"
  rel="stylesheet"
/>
```

- [ ] **Step 6: Create .env.local.example**

```bash
# Google Sheets API credentials
# Get these from Google Cloud Console → Service Account → JSON key
GOOGLE_SERVICE_ACCOUNT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"

# Google Sheet ID — found in the Sheet URL:
# https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
GOOGLE_SHEET_ID=your_sheet_id_here
```

- [ ] **Step 7: Commit**

```bash
git add .
git commit -m "feat: scaffold Next.js project with design tokens and env template"
```

---

## Task 2: Zod Schemas + Google Sheets Helper

**Files:**
- Create: `lib/schemas.ts`
- Create: `lib/sheets.ts`

- [ ] **Step 1: Write schemas**

Create `lib/schemas.ts`:

```typescript
import { z } from 'zod'

export const patientLeadSchema = z.object({
  firstName:  z.string().min(1, 'Required'),
  lastName:   z.string().min(1, 'Required'),
  email:      z.string().email('Valid email required'),
  phone:      z.string().min(8, 'Valid phone required'),
  state:      z.string().min(1, 'Required'),
  referral:   z.string().optional(),
  message:    z.string().optional(),
  consent:    z.literal(true, { errorMap: () => ({ message: 'Consent is required' }) }),
})

export const practitionerLeadSchema = z.object({
  firstName:   z.string().min(1, 'Required'),
  lastName:    z.string().min(1, 'Required'),
  ahpra:       z.string().min(1, 'AHPRA registration number required'),
  specialty:   z.string().min(1, 'Required'),
  email:       z.string().email('Valid email required'),
  state:       z.string().min(1, 'Required'),
  practice:    z.string().optional(),
  consentAhpra: z.literal(true, { errorMap: () => ({ message: 'Required' }) }),
  consentContact: z.literal(true, { errorMap: () => ({ message: 'Required' }) }),
  consentMarketing: z.boolean().optional(),
})

export type PatientLead       = z.infer<typeof patientLeadSchema>
export type PractitionerLead  = z.infer<typeof practitionerLeadSchema>
```

- [ ] **Step 2: Write Google Sheets helper**

Create `lib/sheets.ts`:

```typescript
import { google } from 'googleapis'

// Authenticates using a service account and returns a Sheets client.
// Credentials are read from environment variables (never hardcode).
function getSheetsClient() {
  const auth = new google.auth.JWT({
    email: process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
    key: process.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
    scopes: ['https://www.googleapis.com/auth/spreadsheets'],
  })
  return google.sheets({ version: 'v4', auth })
}

// Appends a single row to the named sheet tab.
// sheetName must match exactly the tab name in Google Sheets (e.g. "Patient Leads").
export async function appendRow(sheetName: string, values: string[]): Promise<void> {
  const spreadsheetId = process.env.GOOGLE_SHEET_ID
  if (!spreadsheetId) throw new Error('GOOGLE_SHEET_ID environment variable is not set')

  const sheets = getSheetsClient()

  await sheets.spreadsheets.values.append({
    spreadsheetId,
    range: `${sheetName}!A1`,
    valueInputOption: 'USER_ENTERED',
    requestBody: { values: [values] },
  })
}
```

- [ ] **Step 3: Commit**

```bash
git add lib/
git commit -m "feat: add zod schemas and Google Sheets append helper"
```

---

## Task 3: API Route — Lead Capture Endpoint

**Files:**
- Create: `app/api/leads/route.ts`

- [ ] **Step 1: Write the API route**

Create `app/api/leads/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server'
import { patientLeadSchema, practitionerLeadSchema } from '@/lib/schemas'
import { appendRow } from '@/lib/sheets'

export async function POST(req: NextRequest) {
  const body = await req.json()
  const { type, ...data } = body

  if (type === 'patient') {
    const result = patientLeadSchema.safeParse(data)
    if (!result.success) {
      return NextResponse.json({ error: result.error.flatten() }, { status: 400 })
    }
    const d = result.data
    const timestamp = new Date().toISOString()
    await appendRow('Patient Leads', [
      timestamp, d.firstName, d.lastName, d.email, d.phone,
      d.state, d.referral ?? '', d.message ?? '',
    ])
    return NextResponse.json({ ok: true })
  }

  if (type === 'practitioner') {
    const result = practitionerLeadSchema.safeParse(data)
    if (!result.success) {
      return NextResponse.json({ error: result.error.flatten() }, { status: 400 })
    }
    const d = result.data
    const timestamp = new Date().toISOString()
    await appendRow('Practitioner Leads', [
      timestamp, d.firstName, d.lastName, d.ahpra, d.specialty,
      d.email, d.state, d.practice ?? '',
      String(d.consentMarketing ?? false),
    ])
    return NextResponse.json({ ok: true })
  }

  return NextResponse.json({ error: 'Invalid type' }, { status: 400 })
}
```

- [ ] **Step 2: Manually test the endpoint**

Once the dev server is running (`npm run dev`), test with curl:

```bash
curl -X POST http://localhost:3000/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "type": "patient",
    "firstName": "Test",
    "lastName": "User",
    "email": "test@example.com",
    "phone": "0400000000",
    "state": "NSW",
    "consent": true
  }'
```

Expected: `{"ok":true}` and a new row in the "Patient Leads" sheet.

- [ ] **Step 3: Commit**

```bash
git add app/api/
git commit -m "feat: add /api/leads POST route for patient and practitioner forms"
```

---

## Task 4: Layout Components — Nav, Footer, TGA Disclaimer

**Files:**
- Create: `components/layout/NavBar.tsx`
- Create: `components/layout/Footer.tsx`
- Create: `components/layout/TgaDisclaimer.tsx`
- Modify: `app/layout.tsx`

- [ ] **Step 1: Build NavBar**

Create `components/layout/NavBar.tsx`:

```tsx
'use client'
import Link from 'next/link'
import { useState } from 'react'

export function NavBar() {
  const [open, setOpen] = useState(false)

  return (
    <nav className="sticky top-0 z-50 bg-[var(--color-ink)] border-b border-white/5">
      <div className="max-w-[var(--max-content)] mx-auto px-6 h-14 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="font-serif text-lg text-white tracking-wide">
          Revivum
        </Link>

        {/* Desktop links */}
        <div className="hidden md:flex items-center gap-6 text-sm text-white/60">
          <Link href="/patients"      className="hover:text-white transition-colors">For Patients</Link>
          <Link href="/practitioners" className="hover:text-white transition-colors">For Practitioners</Link>
          <Link href="/about"         className="hover:text-white transition-colors">About</Link>
          <Link
            href="/patients"
            className="bg-[var(--color-moss)] text-white text-xs font-mono tracking-wider uppercase px-4 py-2 rounded hover:bg-[var(--color-moss-light)] transition-colors"
          >
            Join the Network →
          </Link>
        </div>

        {/* Mobile hamburger */}
        <button
          className="md:hidden text-white/60 hover:text-white"
          onClick={() => setOpen(!open)}
          aria-label="Toggle menu"
        >
          <span className="block w-5 h-0.5 bg-current mb-1" />
          <span className="block w-5 h-0.5 bg-current mb-1" />
          <span className="block w-5 h-0.5 bg-current" />
        </button>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden bg-[var(--color-ink)] border-t border-white/5 px-6 py-4 flex flex-col gap-4 text-white/70 text-sm">
          <Link href="/patients"      onClick={() => setOpen(false)}>For Patients</Link>
          <Link href="/practitioners" onClick={() => setOpen(false)}>For Practitioners</Link>
          <Link href="/about"         onClick={() => setOpen(false)}>About</Link>
        </div>
      )}

      {/* Mobile sticky CTA (bottom of screen, separate from hamburger menu) */}
      {/* Add to body via a portal if needed — optional for Phase 1 */}
    </nav>
  )
}
```

- [ ] **Step 2: Build Footer**

Create `components/layout/Footer.tsx`:

```tsx
import Link from 'next/link'

export function Footer() {
  return (
    <footer className="bg-[var(--color-ink)] text-white">
      <div className="max-w-[var(--max-content)] mx-auto px-6 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Brand */}
        <div>
          <p className="font-mono text-[10px] uppercase tracking-widest text-[#5A9A80] mb-3">Revivum</p>
          <p className="text-[11px] text-white/35 leading-relaxed max-w-xs">
            Healthcare infrastructure for compliant peptide therapeutics in Australia.
            TGA-Registered Sponsor. Not a clinic.
          </p>
        </div>

        {/* Navigate */}
        <div>
          <p className="font-mono text-[10px] uppercase tracking-widest text-[#5A9A80] mb-3">Navigate</p>
          <div className="flex flex-col gap-2 text-[11px] text-white/40">
            <Link href="/patients"      className="hover:text-white/70 transition-colors">For Patients</Link>
            <Link href="/practitioners" className="hover:text-white/70 transition-colors">For Practitioners</Link>
            <Link href="/about"         className="hover:text-white/70 transition-colors">About</Link>
          </div>
        </div>

        {/* Legal */}
        <div>
          <p className="font-mono text-[10px] uppercase tracking-widest text-[#5A9A80] mb-3">Legal</p>
          <div className="flex flex-col gap-2 text-[11px] text-white/40">
            <Link href="/privacy" className="hover:text-white/70 transition-colors">Privacy Policy</Link>
            <Link href="/terms"   className="hover:text-white/70 transition-colors">Terms of Use</Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
```

- [ ] **Step 3: Build TgaDisclaimer**

Create `components/layout/TgaDisclaimer.tsx`:

```tsx
// This component is MANDATORY on every page per TGA compliance requirements.
// Do not remove or shorten the disclaimer text without legal review.
export function TgaDisclaimer() {
  return (
    <div className="bg-[#0A1310] border-t border-white/5 px-6 py-3 text-[9px] text-white/25 leading-relaxed">
      ⚠️ IMPORTANT: This website contains general health information only and does not constitute
      medical advice. Revivum does not advertise or promote therapeutic goods. Access to medicines
      requires a clinical consultation with a registered Australian healthcare practitioner.
      Revivum Pty Ltd — TGA Registered Sponsor. revivum.com.au
    </div>
  )
}
```

- [ ] **Step 4: Wire up root layout**

Replace `app/layout.tsx` with:

```tsx
import type { Metadata } from 'next'
import { NavBar } from '@/components/layout/NavBar'
import { Footer } from '@/components/layout/Footer'
import { TgaDisclaimer } from '@/components/layout/TgaDisclaimer'
import '@/styles/globals.css'

export const metadata: Metadata = {
  title: 'Revivum — Regulated Access to Emerging Therapies',
  description:
    'Revivum provides the regulated infrastructure connecting patients and practitioners to lawful peptide-based therapeutics in Australia.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&family=Courier+Prime:wght@400;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="flex flex-col min-h-screen">
        <NavBar />
        <main className="flex-1">{children}</main>
        <Footer />
        <TgaDisclaimer />
      </body>
    </html>
  )
}
```

- [ ] **Step 5: Start dev server and verify layout renders**

```bash
npm run dev
# Open http://localhost:3000
# Expected: dark nav with "Revivum" logo, placeholder main content, dark footer, TGA disclaimer
```

- [ ] **Step 6: Commit**

```bash
git add components/layout/ app/layout.tsx
git commit -m "feat: add NavBar, Footer, and TGA disclaimer layout components"
```

---

## Task 5: Shared UI Primitives

**Files:**
- Create: `components/ui/Button.tsx`
- Create: `components/ui/SectionTag.tsx`
- Create: `components/ui/ComplianceBox.tsx`

- [ ] **Step 1: Button component**

Create `components/ui/Button.tsx`:

```tsx
import { type ButtonHTMLAttributes } from 'react'
import Link from 'next/link'

type Variant = 'primary' | 'outline' | 'outline-white' | 'white' | 'doctor'

const variantClasses: Record<Variant, string> = {
  primary:         'bg-[var(--color-moss)] text-white hover:bg-[var(--color-moss-light)]',
  outline:         'border-[1.5px] border-[var(--color-ink)] text-[var(--color-ink)] hover:bg-[var(--color-ink)] hover:text-white',
  'outline-white': 'border-[1.5px] border-white/40 text-white hover:bg-white/10',
  white:           'bg-white text-[var(--color-ink)] hover:bg-[var(--color-fog)]',
  doctor:          'bg-[#2C3E6B] text-white hover:bg-[#3A5080]',
}

const base = 'inline-flex items-center font-mono text-[9.5px] font-semibold tracking-wider uppercase px-5 py-2.5 rounded transition-colors cursor-pointer'

// Link variant — rendered as <a> via Next.js Link, no button props
type LinkProps = {
  href: string
  variant?: Variant
  children: React.ReactNode
  className?: string
}

// Button variant — rendered as <button>, supports all button HTML attributes
type ButtonProps = {
  href?: never
  variant?: Variant
  children: React.ReactNode
  className?: string
} & ButtonHTMLAttributes<HTMLButtonElement>

type Props = LinkProps | ButtonProps

export function Button({ variant = 'primary', children, className = '', ...props }: Props) {
  const classes = `${base} ${variantClasses[variant]} ${className}`

  if ('href' in props && props.href) {
    const { href } = props
    return <Link href={href} className={classes}>{children}</Link>
  }

  // Safe to spread — we're in the ButtonProps branch, href is never present
  const { href: _href, ...buttonProps } = props as ButtonProps & { href?: never }
  return <button className={classes} {...buttonProps}>{children}</button>
}
```

- [ ] **Step 2: SectionTag (eyebrow label)**

Create `components/ui/SectionTag.tsx`:

```tsx
type Props = {
  children: React.ReactNode
  light?: boolean  // true = white/teal variant for dark backgrounds
}

export function SectionTag({ children, light = false }: Props) {
  return (
    <p className={`font-mono text-[8.5px] uppercase tracking-[0.18em] mb-1.5 ${
      light ? 'text-[#5A9A80]' : 'text-[var(--color-moss)]'
    }`}>
      {children}
    </p>
  )
}
```

- [ ] **Step 3: ComplianceBox**

Create `components/ui/ComplianceBox.tsx`:

```tsx
// Renders the amber TGA compliance notice.
// Required on patient-facing content sections per TGA guidelines.
export function ComplianceBox({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-[#FEF8E8] border border-[#E8D090] border-l-4 border-l-[var(--color-amber)] rounded p-3 mt-3 text-[9.5px] text-[#7A5C20] leading-relaxed max-w-lg">
      {children}
    </div>
  )
}
```

- [ ] **Step 4: Commit**

```bash
git add components/ui/
git commit -m "feat: add Button, SectionTag, and ComplianceBox UI primitives"
```

---

## Task 6: Homepage

**Files:**
- Create: `components/home/HeroSection.tsx`
- Create: `components/home/AudienceRouter.tsx`
- Create: `components/home/WhatWeAre.tsx`
- Create: `components/home/TrustBand.tsx`
- Create: `components/home/GlobalCta.tsx`
- Modify: `app/page.tsx`

- [ ] **Step 1: Trust bar strip**

Add a `TrustBar` component inline in `app/page.tsx` (it's only used here):

```tsx
function TrustBar() {
  const items = [
    'TGA-Registered Sponsor',
    'GMP-Verified Supply',
    'Pharmacist-Led Support',
    'SAS-B · Authorised Prescriber',
    'AHPRA Network',
  ]
  return (
    <div className="flex flex-wrap gap-5 items-center px-6 py-3 bg-white border-b border-[var(--color-rule)]">
      {items.map(item => (
        <div key={item} className="flex items-center gap-1.5 text-[9.5px] text-[var(--color-muted)] font-medium">
          <span className="w-3.5 h-3.5 rounded bg-[var(--color-rule)]" />
          {item}
        </div>
      ))}
    </div>
  )
}
```

- [ ] **Step 2: HeroSection**

Create `components/home/HeroSection.tsx`:

```tsx
import { Button } from '@/components/ui/Button'
import { SectionTag } from '@/components/ui/SectionTag'
import { ComplianceBox } from '@/components/ui/ComplianceBox'

export function HeroSection() {
  return (
    <section className="bg-[var(--color-fog)] px-6 py-10">
      <div className="max-w-[var(--max-content)] mx-auto">
        <SectionTag>Healthcare Infrastructure · Australia</SectionTag>
        <h1 className="font-serif text-[clamp(22px,4vw,28px)] text-[var(--color-ink)] leading-tight max-w-xl mb-3">
          Regulated Access to <em>Emerging Therapies.</em>
        </h1>
        <p className="text-[13px] text-[#555] leading-relaxed max-w-lg mb-5">
          Revivum provides the infrastructure that connects patients and practitioners to
          lawful, GMP-quality peptide-based therapeutics in Australia — safely, compliantly,
          and with pharmacist-led clinical support.
        </p>
        <div className="flex flex-wrap gap-2">
          <Button href="/patients">I'm a Patient →</Button>
          <Button variant="outline" href="/practitioners">I'm a Practitioner →</Button>
        </div>
        <ComplianceBox>
          This website contains general health information only. It does not promote therapeutic
          goods or constitute medical advice. Always consult a registered healthcare practitioner.
        </ComplianceBox>
      </div>
    </section>
  )
}
```

- [ ] **Step 3: AudienceRouter**

Create `components/home/AudienceRouter.tsx`:

```tsx
import { Button } from '@/components/ui/Button'

export function AudienceRouter() {
  return (
    <section className="bg-white px-6 py-10">
      <div className="max-w-[var(--max-content)] mx-auto">
        <p className="font-mono text-[8.5px] uppercase tracking-widest text-[var(--color-moss)] mb-4">Who Is This For?</p>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="bg-[var(--color-patient-bg)] border-[1.5px] border-[var(--color-patient-border)] rounded-lg p-5">
            <p className="font-mono text-[8px] uppercase tracking-widest text-[var(--color-patient-text)] mb-2">For Patients</p>
            <h2 className="font-serif text-base text-[var(--color-ink)] mb-2">Curious About Emerging Therapies?</h2>
            <p className="text-[11px] text-[#5A5248] leading-relaxed mb-4">
              Learn what peptide-based therapies are and how to access them lawfully through a registered Australian practitioner.
            </p>
            <Button href="/patients">Learn More →</Button>
          </div>
          <div className="bg-[var(--color-doctor-bg)] border-[1.5px] border-[var(--color-doctor-border)] rounded-lg p-5">
            <p className="font-mono text-[8px] uppercase tracking-widest text-[var(--color-doctor-text)] mb-2">For Practitioners</p>
            <h2 className="font-serif text-base text-[var(--color-ink)] mb-2">Ready to Expand Your Practice?</h2>
            <p className="text-[11px] text-[#5A5248] leading-relaxed mb-4">
              Join our network and access GMP supply, TGA pathway support, and pharmacist-led clinical guidance.
            </p>
            <Button variant="doctor" href="/practitioners">Join the Network →</Button>
          </div>
        </div>
      </div>
    </section>
  )
}
```

- [ ] **Step 4: WhatWeAre**

Create `components/home/WhatWeAre.tsx`:

```tsx
import { SectionTag } from '@/components/ui/SectionTag'

const roles = [
  { icon: '📚', title: 'Education', body: 'General health information for patients. Regulatory support for practitioners.' },
  { icon: '🧭', title: 'Navigation', body: 'Connecting curious patients with AHPRA-registered practitioners through a lawful pathway.' },
  { icon: '🏭', title: 'Supply',     body: 'TGA-registered wholesale infrastructure. GMP-verified compounding supply for practitioners.' },
]

export function WhatWeAre() {
  return (
    <section className="bg-[var(--color-fog)] px-6 py-10">
      <div className="max-w-[var(--max-content)] mx-auto">
        <SectionTag>Our Role</SectionTag>
        <h2 className="font-serif text-xl text-[var(--color-ink)] mb-2">We Are Infrastructure. Not a Clinic.</h2>
        <p className="text-[13px] text-[#555] leading-relaxed max-w-lg mb-6">
          Revivum operates as the regulated backbone behind compliant peptide prescribing in Australia.
          We don't treat patients — we support the practitioners who do.
        </p>
        <div className="grid md:grid-cols-3 gap-3">
          {roles.map(r => (
            <div key={r.title} className="bg-[var(--color-fog)] border border-[var(--color-rule)] rounded-md p-4">
              <div className="text-xl mb-2">{r.icon}</div>
              <h3 className="text-[12px] font-semibold text-[var(--color-ink)] mb-1">{r.title}</h3>
              <p className="text-[10px] text-[#5A5248] leading-relaxed">{r.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

- [ ] **Step 5: TrustBand (dark section)**

Create `components/home/TrustBand.tsx`:

```tsx
import { Button } from '@/components/ui/Button'
import { SectionTag } from '@/components/ui/SectionTag'

export function TrustBand() {
  return (
    <section className="bg-[var(--color-ink)] px-6 py-12">
      <div className="max-w-[var(--max-content)] mx-auto">
        <SectionTag light>Our Commitment</SectionTag>
        <h2 className="font-serif text-[18px] text-white max-w-md leading-snug mb-3">
          Compliance Is the Foundation.<br />Not an Afterthought.
        </h2>
        <p className="text-[11px] text-white/55 leading-relaxed max-w-lg mb-5">
          We operate within TGA regulations, AHPRA professional standards, and the SAS-B and
          Authorised Prescriber access pathways. Our infrastructure is built for a regulated world.
        </p>
        <Button variant="outline-white" href="/about">About Revivum →</Button>
      </div>
    </section>
  )
}
```

- [ ] **Step 6: GlobalCta**

Create `components/home/GlobalCta.tsx`:

```tsx
import { Button } from '@/components/ui/Button'

export function GlobalCta() {
  return (
    <section className="bg-[var(--color-parchment)] px-6 py-14 text-center">
      <div className="max-w-[var(--max-content)] mx-auto">
        <p className="font-mono text-[8.5px] uppercase tracking-widest text-[var(--color-moss)] mb-2">Get Started</p>
        <h2 className="font-serif text-xl text-[var(--color-ink)] mb-5">
          Patient or Practitioner — Start Here.
        </h2>
        <div className="flex flex-wrap justify-center gap-3">
          <Button href="/patients">I'm a Patient →</Button>
          <Button variant="outline" href="/practitioners">I'm a Practitioner →</Button>
        </div>
      </div>
    </section>
  )
}
```

- [ ] **Step 7: Wire up app/page.tsx**

Replace `app/page.tsx`:

```tsx
import { HeroSection }    from '@/components/home/HeroSection'
import { AudienceRouter } from '@/components/home/AudienceRouter'
import { WhatWeAre }      from '@/components/home/WhatWeAre'
import { TrustBand }      from '@/components/home/TrustBand'
import { GlobalCta }      from '@/components/home/GlobalCta'

const trustItems = [
  'TGA-Registered Sponsor', 'GMP-Verified Supply',
  'Pharmacist-Led Support', 'SAS-B · Authorised Prescriber', 'AHPRA Network',
]

export default function HomePage() {
  return (
    <>
      {/* Trust bar */}
      <div className="flex flex-wrap gap-5 items-center px-6 py-3 bg-white border-b border-[var(--color-rule)]">
        {trustItems.map(item => (
          <div key={item} className="flex items-center gap-1.5 text-[9.5px] text-[var(--color-muted)] font-medium">
            <span className="w-3.5 h-3.5 rounded bg-[var(--color-rule)]" />
            {item}
          </div>
        ))}
      </div>
      <HeroSection />
      <AudienceRouter />
      <WhatWeAre />
      <TrustBand />
      <GlobalCta />
    </>
  )
}
```

- [ ] **Step 8: Verify homepage in browser**

```bash
# Dev server should still be running. Open http://localhost:3000
# Check: trust bar, hero with dual CTAs, audience cards, 3-role section, dark trust band, repeat CTA
```

- [ ] **Step 9: Commit**

```bash
git add components/home/ app/page.tsx
git commit -m "feat: build homepage with all 5 sections"
```

---

## Task 7: Patient Lead Form Component

**Files:**
- Create: `components/patients/PatientLeadForm.tsx`

This is the most complex component — it handles form state, validation, and API submission.

- [ ] **Step 1: Build PatientLeadForm**

Create `components/patients/PatientLeadForm.tsx`:

```tsx
'use client'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { patientLeadSchema, type PatientLead } from '@/lib/schemas'
import { Button } from '@/components/ui/Button'
import { useState } from 'react'

const states = ['ACT','NSW','NT','QLD','SA','TAS','VIC','WA']

export function PatientLeadForm() {
  const [submitted, setSubmitted] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<PatientLead>({ resolver: zodResolver(patientLeadSchema) })

  async function onSubmit(data: PatientLead) {
    setError(null)
    const res = await fetch('/api/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'patient', ...data }),
    })
    if (res.ok) {
      setSubmitted(true)
    } else {
      setError('Something went wrong. Please try again or email us directly.')
    }
  }

  if (submitted) {
    return (
      <div className="bg-[var(--color-patient-bg)] border border-[var(--color-patient-border)] rounded-lg p-6 max-w-[var(--form-max)]">
        <h3 className="font-serif text-lg text-[var(--color-ink)] mb-2">Thank you — we'll be in touch.</h3>
        <p className="text-[11px] text-[var(--color-muted)] leading-relaxed">
          A member of the Revivum team will contact you within a few business days to guide your next steps.
        </p>
      </div>
    )
  }

  const field = 'w-full h-9 bg-[var(--color-fog)] border-[1.5px] border-[var(--color-rule)] rounded px-3 text-[11px] font-mono text-[var(--color-muted)] focus:outline-none focus:border-[var(--color-moss)]'
  const err   = 'text-[9.5px] text-red-600 mt-0.5'
  const label = 'block text-[10px] font-medium text-[var(--color-ink)] mb-1'

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="max-w-[var(--form-max)] space-y-3">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className={label}>First Name *</label>
          <input {...register('firstName')} className={field} />
          {errors.firstName && <p className={err}>{errors.firstName.message}</p>}
        </div>
        <div>
          <label className={label}>Last Name *</label>
          <input {...register('lastName')} className={field} />
          {errors.lastName && <p className={err}>{errors.lastName.message}</p>}
        </div>
      </div>

      <div>
        <label className={label}>Email Address *</label>
        <input {...register('email')} type="email" className={field} />
        {errors.email && <p className={err}>{errors.email.message}</p>}
      </div>

      <div>
        <label className={label}>Phone Number *</label>
        <input {...register('phone')} type="tel" className={field} />
        {errors.phone && <p className={err}>{errors.phone.message}</p>}
      </div>

      <div>
        <label className={label}>State / Territory *</label>
        <select {...register('state')} className={field}>
          <option value="">Select…</option>
          {states.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        {errors.state && <p className={err}>{errors.state.message}</p>}
      </div>

      <div>
        <label className={label}>How did you hear about us? (optional)</label>
        <input {...register('referral')} className={field} />
      </div>

      <div>
        <label className={label}>Anything you'd like us to know? (optional)</label>
        <textarea
          {...register('message')}
          className={`${field} !h-16 py-2 resize-none`}
        />
      </div>

      {/* Consent — mandatory, specific copy required for TGA compliance */}
      <div className="bg-[var(--color-patient-bg)] border border-[var(--color-patient-border)] rounded p-3">
        <label className="flex gap-2 items-start cursor-pointer text-[9.5px] text-[var(--color-patient-text)] leading-relaxed">
          <input {...register('consent')} type="checkbox" className="mt-0.5 flex-shrink-0" />
          <span>
            By submitting this form, I confirm I am seeking general information only.
            I understand that Revivum is not a medical provider and that any clinical decisions
            will be made by a registered healthcare practitioner. I consent to being contacted
            by a member of the Revivum team.
          </span>
        </label>
        {errors.consent && <p className={err}>{errors.consent.message}</p>}
      </div>

      {error && <p className="text-[11px] text-red-600">{error}</p>}

      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting…' : 'Register My Interest →'}
      </Button>
    </form>
  )
}
```

- [ ] **Step 2: Commit**

```bash
git add components/patients/PatientLeadForm.tsx
git commit -m "feat: add patient lead capture form with validation and Sheets submission"
```

---

## Task 8: Patients Page

**Files:**
- Create: `components/patients/PatientHero.tsx`
- Create: `components/patients/WhatArePeptides.tsx`
- Create: `components/patients/HowItWorks.tsx`
- Create: `app/patients/page.tsx`

- [ ] **Step 1: PatientHero**

Create `components/patients/PatientHero.tsx`:

```tsx
import { SectionTag } from '@/components/ui/SectionTag'
import { ComplianceBox } from '@/components/ui/ComplianceBox'

export function PatientHero() {
  return (
    <section className="bg-[var(--color-patient-bg)] px-6 py-10">
      <div className="max-w-[var(--max-content)] mx-auto">
        <SectionTag>For Patients · General Information</SectionTag>
        <h1 className="font-serif text-[clamp(20px,3.5vw,24px)] text-[var(--color-ink)] max-w-xl mb-3 leading-tight">
          Understanding Peptide-Based Therapies in Australia.
        </h1>
        <p className="text-[13px] text-[#555] leading-relaxed max-w-lg">
          Peptide therapies are an emerging area of clinical interest. This page provides general,
          educational information to help you understand what they are and how lawful access works
          in Australia — through a registered healthcare practitioner.
        </p>
        <ComplianceBox>
          This page is for general information only. It does not constitute medical advice and does
          not promote any therapeutic product. Individual suitability is determined by a registered
          practitioner.
        </ComplianceBox>
      </div>
    </section>
  )
}
```

- [ ] **Step 2: WhatArePeptides**

Create `components/patients/WhatArePeptides.tsx`:

```tsx
import { SectionTag } from '@/components/ui/SectionTag'

const cards = [
  { icon: '🧬', title: 'Naturally Occurring',  body: 'Peptides are found throughout the body. Insulin is one of the most well-known peptide-based medicines.' },
  { icon: '🔭', title: 'An Evolving Field',     body: 'Peptide therapeutics represent a growing area of clinical research and medical interest globally.' },
  { icon: '🏥', title: 'Regulated Access',      body: "In Australia, certain peptide therapies are accessed via the TGA's SAS-B or Authorised Prescriber pathways — through a registered doctor." },
]

export function WhatArePeptides() {
  return (
    <section className="bg-white px-6 py-10">
      <div className="max-w-[var(--max-content)] mx-auto">
        <SectionTag>General Health Information</SectionTag>
        <h2 className="font-serif text-xl text-[var(--color-ink)] mb-3">What Are Peptide Therapies?</h2>
        <p className="text-[13px] text-[#555] leading-relaxed max-w-lg mb-6">
          Peptides are short chains of amino acids that occur naturally in the body. In clinical
          settings, certain peptide-based compounds are being explored as therapeutic options —
          available in Australia through regulated access pathways.
        </p>
        <div className="grid md:grid-cols-3 gap-3">
          {cards.map(c => (
            <div key={c.title} className="bg-[var(--color-fog)] border border-[var(--color-rule)] rounded-md p-4">
              <div className="text-xl mb-2">{c.icon}</div>
              <h3 className="text-[12px] font-semibold text-[var(--color-ink)] mb-1">{c.title}</h3>
              <p className="text-[10px] text-[#5A5248] leading-relaxed">{c.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

- [ ] **Step 3: HowItWorks**

Create `components/patients/HowItWorks.tsx`:

```tsx
import { SectionTag } from '@/components/ui/SectionTag'

const steps = [
  { n: 1, label: 'Register Your Interest',    sub: 'Submit your details below. Our team reviews your enquiry.' },
  { n: 2, label: 'Speak to a Practitioner',   sub: 'We connect you with a registered doctor in our network for a clinical consultation.' },
  { n: 3, label: 'Lawful, Supported Access',  sub: 'If suitable, your doctor manages prescribing and supply through regulated channels.' },
]

export function HowItWorks() {
  return (
    <section className="bg-[var(--color-fog)] px-6 py-10">
      <div className="max-w-[var(--max-content)] mx-auto">
        <SectionTag>The Process</SectionTag>
        <h2 className="font-serif text-xl text-[var(--color-ink)] mb-2">How Does Lawful Access Work?</h2>
        <p className="text-[13px] text-[#555] leading-relaxed mb-8">Three simple steps — all involving a registered Australian practitioner.</p>
        <div className="flex flex-col md:flex-row gap-0 items-start">
          {steps.map((s, i) => (
            <div key={s.n} className="flex-1 text-center px-3 relative">
              {i < steps.length - 1 && (
                <span className="hidden md:block absolute right-0 top-3.5 text-[var(--color-moss-light)] text-lg">→</span>
              )}
              <div className="w-7 h-7 rounded-full bg-[var(--color-moss)] text-white text-[11px] font-bold flex items-center justify-center mx-auto mb-2">
                {s.n}
              </div>
              <p className="text-[10px] font-semibold text-[var(--color-ink)] mb-1">{s.label}</p>
              <p className="text-[9px] text-[var(--color-muted)] leading-relaxed">{s.sub}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

- [ ] **Step 4: Wire up patients page**

Create `app/patients/page.tsx`:

```tsx
import { PatientHero }      from '@/components/patients/PatientHero'
import { WhatArePeptides }  from '@/components/patients/WhatArePeptides'
import { HowItWorks }       from '@/components/patients/HowItWorks'
import { PatientLeadForm }  from '@/components/patients/PatientLeadForm'
import { SectionTag }       from '@/components/ui/SectionTag'

export const metadata = {
  title: 'For Patients — Revivum',
}

export default function PatientsPage() {
  return (
    <>
      <PatientHero />
      <WhatArePeptides />
      <HowItWorks />

      {/* Lead capture */}
      <section className="bg-[var(--color-parchment)] px-6 py-10">
        <div className="max-w-[var(--max-content)] mx-auto">
          <SectionTag>Register Your Interest</SectionTag>
          <h2 className="font-serif text-xl text-[var(--color-ink)] mb-2">Ready to Learn More?</h2>
          <p className="text-[13px] text-[#555] leading-relaxed max-w-lg mb-6">
            Submit your details and a member of our team will be in touch to guide you
            through your next steps — with no obligation.
          </p>
          <PatientLeadForm />
        </div>
      </section>
    </>
  )
}
```

- [ ] **Step 5: Verify patients page**

```bash
# Open http://localhost:3000/patients
# Check: green hero, 3 info cards, 3-step flow, lead capture form
# Try submitting the form — should show success state (Sheets write will fail without credentials, that's OK for now)
```

- [ ] **Step 6: Commit**

```bash
git add components/patients/ app/patients/
git commit -m "feat: build /patients page with education sections and lead form"
```

---

## Task 9: Practitioner Sign-Up Form + Page

**Files:**
- Create: `components/practitioners/PractitionerSignUpForm.tsx`
- Create: `components/practitioners/PractitionerHero.tsx`
- Create: `components/practitioners/WhatWeProvide.tsx`
- Create: `components/practitioners/Credentials.tsx`
- Create: `app/practitioners/page.tsx`

- [ ] **Step 1: PractitionerSignUpForm**

Create `components/practitioners/PractitionerSignUpForm.tsx`:

```tsx
'use client'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { practitionerLeadSchema, type PractitionerLead } from '@/lib/schemas'
import { Button } from '@/components/ui/Button'
import { useState } from 'react'

const states     = ['ACT','NSW','NT','QLD','SA','TAS','VIC','WA']
const specialties = ['General Practice','Sports Medicine','Endocrinology','Anti-Ageing Medicine','Integrative Medicine','Other']

export function PractitionerSignUpForm() {
  const [submitted, setSubmitted] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<PractitionerLead>({ resolver: zodResolver(practitionerLeadSchema) })

  async function onSubmit(data: PractitionerLead) {
    setError(null)
    const res = await fetch('/api/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'practitioner', ...data }),
    })
    if (res.ok) {
      setSubmitted(true)
    } else {
      setError('Something went wrong. Please try again or contact us directly.')
    }
  }

  if (submitted) {
    return (
      <div className="bg-[var(--color-doctor-bg)] border border-[var(--color-doctor-border)] rounded-lg p-6 max-w-[var(--form-max)]">
        <h3 className="font-serif text-lg text-[var(--color-ink)] mb-2">Application received — we'll be in touch within 48 hours.</h3>
        <p className="text-[11px] text-[var(--color-muted)] leading-relaxed">
          Our team will verify your AHPRA registration and contact you to complete onboarding.
        </p>
      </div>
    )
  }

  const field = 'w-full h-9 bg-[var(--color-fog)] border-[1.5px] border-[var(--color-rule)] rounded px-3 text-[11px] font-mono text-[var(--color-muted)] focus:outline-none focus:border-[#2C3E6B]'
  const err   = 'text-[9.5px] text-red-600 mt-0.5'
  const label = 'block text-[10px] font-medium text-[var(--color-ink)] mb-1'

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="max-w-[var(--form-max)] space-y-3">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className={label}>First Name *</label>
          <input {...register('firstName')} className={field} />
          {errors.firstName && <p className={err}>{errors.firstName.message}</p>}
        </div>
        <div>
          <label className={label}>Last Name *</label>
          <input {...register('lastName')} className={field} />
          {errors.lastName && <p className={err}>{errors.lastName.message}</p>}
        </div>
      </div>

      <div>
        <label className={label}>AHPRA Registration Number *</label>
        <input {...register('ahpra')} className={field} placeholder="e.g. MED0001234567" />
        {errors.ahpra && <p className={err}>{errors.ahpra.message}</p>}
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className={label}>Medical Specialty *</label>
          <select {...register('specialty')} className={field}>
            <option value="">Select…</option>
            {specialties.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
          {errors.specialty && <p className={err}>{errors.specialty.message}</p>}
        </div>
        <div>
          <label className={label}>State / Territory *</label>
          <select {...register('state')} className={field}>
            <option value="">Select…</option>
            {states.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
          {errors.state && <p className={err}>{errors.state.message}</p>}
        </div>
      </div>

      <div>
        <label className={label}>Work Email Address *</label>
        <input {...register('email')} type="email" className={field} />
        {errors.email && <p className={err}>{errors.email.message}</p>}
      </div>

      <div>
        <label className={label}>Practice / Clinic Name (optional)</label>
        <input {...register('practice')} className={field} />
      </div>

      {/* Consent — two required, one optional */}
      <div className="bg-[var(--color-doctor-bg)] border border-[var(--color-doctor-border)] rounded p-3 space-y-2">
        <label className="flex gap-2 items-start cursor-pointer text-[9.5px] text-[#2C3E6B] leading-relaxed">
          <input {...register('consentAhpra')} type="checkbox" className="mt-0.5 flex-shrink-0" />
          <span>I confirm I am currently registered with AHPRA and authorised to practice medicine in Australia.</span>
        </label>
        {errors.consentAhpra && <p className={err}>{errors.consentAhpra.message}</p>}

        <label className="flex gap-2 items-start cursor-pointer text-[9.5px] text-[#2C3E6B] leading-relaxed">
          <input {...register('consentContact')} type="checkbox" className="mt-0.5 flex-shrink-0" />
          <span>I understand access to Revivum's network and supply infrastructure is for registered healthcare professionals only, and consent to being contacted by Revivum.</span>
        </label>
        {errors.consentContact && <p className={err}>{errors.consentContact.message}</p>}

        <label className="flex gap-2 items-start cursor-pointer text-[9.5px] text-[#2C3E6B] leading-relaxed">
          <input {...register('consentMarketing')} type="checkbox" className="mt-0.5 flex-shrink-0" />
          <span>I consent to receiving clinical updates and network communications from Revivum. (optional)</span>
        </label>
      </div>

      {error && <p className="text-[11px] text-red-600">{error}</p>}

      <Button variant="doctor" type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting…' : 'Apply to Join the Network →'}
      </Button>
    </form>
  )
}
```

- [ ] **Step 2: PractitionerHero**

Create `components/practitioners/PractitionerHero.tsx`:

```tsx
import { Button } from '@/components/ui/Button'
import { SectionTag } from '@/components/ui/SectionTag'

export function PractitionerHero() {
  return (
    <section className="bg-[var(--color-ink)] px-6 py-14">
      <div className="max-w-[var(--max-content)] mx-auto">
        <SectionTag light>For AHPRA-Registered Practitioners</SectionTag>
        <h1 className="font-serif text-[clamp(20px,3.5vw,24px)] text-white max-w-xl leading-tight mb-3">
          The Infrastructure Behind<br />Compliant Peptide Prescribing.
        </h1>
        <p className="text-[11px] text-white/55 leading-relaxed max-w-lg mb-6">
          Revivum is a TGA-registered wholesale infrastructure provider. We give Australian
          practitioners the supply reliability, regulatory framework, and pharmacist-led support
          needed to prescribe peptide therapeutics with confidence.
        </p>
        <div className="flex flex-wrap gap-2">
          <Button variant="white" href="#apply">Apply to Join →</Button>
          <Button variant="outline-white" href="#what-we-provide">What We Provide ↓</Button>
        </div>
      </div>
    </section>
  )
}
```

- [ ] **Step 3: WhatWeProvide**

Create `components/practitioners/WhatWeProvide.tsx`:

```tsx
import { SectionTag } from '@/components/ui/SectionTag'

const cards = [
  { icon: '📦', title: 'GMP Supply Chain',        body: 'Pharmaceutical-grade finished goods. Verified compounding partners. Consistent, reliable availability.' },
  { icon: '📋', title: 'TGA Pathway Support',     body: 'SAS-B notification and Authorised Prescriber application support. Compliance documentation and templates.' },
  { icon: '💊', title: 'Pharmacist-Led Guidance', body: 'Direct access to our clinical pharmacist team. Dosing support, product queries, and complex case guidance.' },
  { icon: '📡', title: 'Patient Referral Flow',   body: 'Network-listed practitioners receive pre-educated patient enquiries via our patient-facing pathway.' },
]

export function WhatWeProvide() {
  return (
    <section id="what-we-provide" className="bg-white px-6 py-10">
      <div className="max-w-[var(--max-content)] mx-auto">
        <SectionTag>What We Provide</SectionTag>
        <h2 className="font-serif text-xl text-[var(--color-ink)] mb-6">Everything You Need. Simply Delivered.</h2>
        <div className="grid md:grid-cols-2 gap-4">
          {cards.map(c => (
            <div key={c.title} className="bg-white border border-[var(--color-rule)] border-l-4 border-l-[var(--color-moss)] rounded-md p-5">
              <div className="text-xl mb-2">{c.icon}</div>
              <h3 className="text-[12px] font-semibold text-[var(--color-ink)] mb-1">{c.title}</h3>
              <p className="text-[11px] text-[#5A5248] leading-relaxed">{c.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

- [ ] **Step 4: Credentials**

Create `components/practitioners/Credentials.tsx`:

```tsx
import { SectionTag } from '@/components/ui/SectionTag'

const creds = [
  { title: 'TGA Registered Sponsor', body: 'Registered under the Therapeutic Goods Act 1989 to supply therapeutic goods in Australia.' },
  { title: 'GMP Manufacturing',      body: 'All products sourced from GMP-compliant facilities. Quality documentation available on request.' },
  { title: 'SAS-B & AP Pathways',    body: 'Full operational infrastructure for both TGA unapproved medicine access pathways.' },
]

export function Credentials() {
  return (
    <section className="bg-[var(--color-fog)] px-6 py-10">
      <div className="max-w-[var(--max-content)] mx-auto">
        <SectionTag>Our Credentials</SectionTag>
        <h2 className="font-serif text-xl text-[var(--color-ink)] mb-6">Built on Regulatory Foundations</h2>
        <div className="grid md:grid-cols-3 gap-4">
          {creds.map(c => (
            <div key={c.title} className="bg-white border border-[var(--color-rule)] rounded-md p-4">
              <h3 className="text-[10px] font-bold text-[var(--color-ink)] mb-1">{c.title}</h3>
              <p className="text-[9.5px] text-[var(--color-muted)] leading-relaxed">{c.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

- [ ] **Step 5: Wire up practitioners page**

Create `app/practitioners/page.tsx`:

```tsx
import { PractitionerHero }     from '@/components/practitioners/PractitionerHero'
import { WhatWeProvide }        from '@/components/practitioners/WhatWeProvide'
import { Credentials }          from '@/components/practitioners/Credentials'
import { PractitionerSignUpForm } from '@/components/practitioners/PractitionerSignUpForm'
import { SectionTag }           from '@/components/ui/SectionTag'

export const metadata = {
  title: 'For Practitioners — Revivum',
}

export default function PractitionersPage() {
  return (
    <>
      <PractitionerHero />
      <WhatWeProvide />
      <Credentials />

      {/* Sign-up form */}
      <section id="apply" className="bg-[var(--color-parchment)] px-6 py-10">
        <div className="max-w-[var(--max-content)] mx-auto">
          <SectionTag>Apply to Join</SectionTag>
          <h2 className="font-serif text-xl text-[var(--color-ink)] mb-1">Join the Revivum Practitioner Network</h2>
          <p className="text-[13px] text-[#555] mb-6">
            Membership is free. AHPRA verification required. We'll be in touch within 48 hours.
          </p>
          <PractitionerSignUpForm />
        </div>
      </section>
    </>
  )
}
```

- [ ] **Step 6: Verify practitioners page**

```bash
# Open http://localhost:3000/practitioners
# Check: dark hero, 4 value prop cards, credentials grid, sign-up form with AHPRA field
```

- [ ] **Step 7: Commit**

```bash
git add components/practitioners/ app/practitioners/
git commit -m "feat: build /practitioners page with value prop sections and sign-up form"
```

---

## Task 10: About, Privacy, Terms Pages

**Files:**
- Create: `app/about/page.tsx`
- Create: `app/privacy/page.tsx`
- Create: `app/terms/page.tsx`

- [ ] **Step 1: About page**

Create `app/about/page.tsx`:

```tsx
import { SectionTag } from '@/components/ui/SectionTag'
import { Button } from '@/components/ui/Button'

export const metadata = { title: 'About — Revivum' }

export default function AboutPage() {
  return (
    <>
      {/* §1 Mission */}
      <section className="bg-[var(--color-fog)] px-6 py-12">
        <div className="max-w-[var(--max-content)] mx-auto">
          <SectionTag>About Us</SectionTag>
          <h1 className="font-serif text-[clamp(20px,3.5vw,26px)] text-[var(--color-ink)] max-w-xl leading-tight mb-4">
            Infrastructure for Responsible Innovation in Australian Healthcare.
          </h1>
          <p className="text-[13px] text-[#555] leading-relaxed max-w-lg">
            Revivum is a TGA-registered sponsor and healthcare infrastructure company. We are not
            a clinic, not a pharmacy, and not a direct-to-consumer service. We build the regulated
            supply and support layer that makes lawful access to emerging peptide therapeutics
            possible for Australian practitioners and their patients.
          </p>
        </div>
      </section>

      {/* §2 Our Role */}
      <section className="bg-white px-6 py-10">
        <div className="max-w-[var(--max-content)] mx-auto">
          <SectionTag>What We Do</SectionTag>
          <h2 className="font-serif text-xl text-[var(--color-ink)] mb-6">Three Roles. One Purpose.</h2>
          <div className="grid md:grid-cols-3 gap-3">
            {[
              { icon: '📚', title: 'Education Layer',       body: 'General health information for patients. Clinical and regulatory support for practitioners.' },
              { icon: '🧭', title: 'Navigation Layer',      body: 'Connecting patients with registered practitioners through a lawful access pathway.' },
              { icon: '🏭', title: 'Supply Infrastructure', body: 'TGA-registered wholesale distribution. GMP-verified product supply for qualified prescribers.' },
            ].map(c => (
              <div key={c.title} className="bg-[var(--color-fog)] border border-[var(--color-rule)] rounded-md p-4">
                <div className="text-xl mb-2">{c.icon}</div>
                <h3 className="text-[12px] font-semibold text-[var(--color-ink)] mb-1">{c.title}</h3>
                <p className="text-[10px] text-[#5A5248] leading-relaxed">{c.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* §3 Credentials + CTA */}
      <section className="bg-[var(--color-ink)] px-6 py-12">
        <div className="max-w-[var(--max-content)] mx-auto">
          <SectionTag light>Regulatory Standing</SectionTag>
          <h2 className="font-serif text-[17px] text-white mb-6">Built Within the Framework. Always.</h2>
          <div className="grid md:grid-cols-3 gap-3 mb-8">
            {[
              { title: 'TGA Registered Sponsor', sub: 'Sponsor ID: [To be inserted]' },
              { title: 'GMP-Verified Supply',    sub: 'GMP-compliant manufacturing' },
              { title: 'Pharmacist-Led Team',    sub: 'Clinical pharmacist support for network practitioners' },
            ].map(c => (
              <div key={c.title} className="p-4 bg-white/5 border border-white/8 rounded-md">
                <p className="text-[10px] font-semibold text-white mb-1">{c.title}</p>
                <p className="text-[9px] text-white/40 leading-relaxed">{c.sub}</p>
              </div>
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            <Button variant="white"        href="/patients">For Patients →</Button>
            <Button variant="outline-white" href="/practitioners">For Practitioners →</Button>
          </div>
        </div>
      </section>
    </>
  )
}
```

- [ ] **Step 2: Privacy page (placeholder)**

Create `app/privacy/page.tsx`:

```tsx
export const metadata = { title: 'Privacy Policy — Revivum' }

export default function PrivacyPage() {
  return (
    <section className="px-6 py-14">
      <div className="max-w-[860px] mx-auto">
        <p className="font-mono text-[8.5px] uppercase tracking-widest text-[var(--color-moss)] mb-2">Legal</p>
        <h1 className="font-serif text-2xl text-[var(--color-ink)] mb-6">Privacy Policy</h1>
        <p className="text-[13px] text-[#555] leading-relaxed mb-4">
          <strong>Last updated:</strong> [Date to be inserted]
        </p>
        <p className="text-[13px] text-[#555] leading-relaxed bg-[var(--color-fog)] border border-[var(--color-rule)] rounded p-4">
          This Privacy Policy will be updated prior to launch with full details on how Revivum
          collects, stores, and uses personal information in compliance with the Australian Privacy
          Act 1988 and the Australian Privacy Principles.
        </p>
      </div>
    </section>
  )
}
```

- [ ] **Step 3: Terms page (placeholder)**

Create `app/terms/page.tsx`:

```tsx
export const metadata = { title: 'Terms of Use — Revivum' }

export default function TermsPage() {
  return (
    <section className="px-6 py-14">
      <div className="max-w-[860px] mx-auto">
        <p className="font-mono text-[8.5px] uppercase tracking-widest text-[var(--color-moss)] mb-2">Legal</p>
        <h1 className="font-serif text-2xl text-[var(--color-ink)] mb-6">Terms of Use</h1>
        <p className="text-[13px] text-[#555] leading-relaxed mb-4">
          <strong>Last updated:</strong> [Date to be inserted]
        </p>
        <p className="text-[13px] text-[#555] leading-relaxed bg-[var(--color-fog)] border border-[var(--color-rule)] rounded p-4">
          Full Terms of Use will be published prior to launch. By using this website, you agree
          that it is for general informational purposes only and does not constitute medical advice.
        </p>
      </div>
    </section>
  )
}
```

- [ ] **Step 4: Commit**

```bash
git add app/about/ app/privacy/ app/terms/
git commit -m "feat: add About, Privacy, and Terms pages"
```

---

## Task 11: Google Sheets Setup

This task is done in the browser, not in code.

- [ ] **Step 1: Create the Google Sheet**

  1. Go to sheets.google.com, create a new sheet called **"Revivum Leads"**
  2. Rename **Sheet1** → `Patient Leads`
  3. Add a second sheet → rename to `Practitioner Leads`
  4. In **Patient Leads** row 1, add headers:
     `Timestamp | First Name | Last Name | Email | Phone | State | Referral | Message`
  5. In **Practitioner Leads** row 1, add headers:
     `Timestamp | First Name | Last Name | AHPRA | Specialty | Email | State | Practice | Marketing Opt-In`
  6. Note the Sheet ID from the URL: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`

- [ ] **Step 2: Create a Google Cloud service account**

  1. Go to console.cloud.google.com → New project: `revivum-leads`
  2. APIs & Services → Enable the **Google Sheets API**
  3. Credentials → Create Credentials → Service Account
     - Name: `revivum-sheets-writer`
     - Role: **Editor** (or create a custom role with Sheets write only)
  4. Click the service account → Keys → Add Key → JSON → Download
  5. Open the JSON — copy `client_email` and `private_key`

- [ ] **Step 3: Share the Sheet with the service account**

  In the Google Sheet, click Share → paste the `client_email` → give **Editor** access

- [ ] **Step 4: Set environment variables**

  ```bash
  cp .env.local.example .env.local
  # Edit .env.local — fill in GOOGLE_SERVICE_ACCOUNT_EMAIL, GOOGLE_PRIVATE_KEY, GOOGLE_SHEET_ID
  ```

  **Important:** `GOOGLE_PRIVATE_KEY` in `.env.local` must wrap the key in double quotes and use literal `\n` for newlines:
  ```
  GOOGLE_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\nABC123...\n-----END RSA PRIVATE KEY-----\n"
  ```

- [ ] **Step 5: Verify end-to-end**

  ```bash
  npm run dev
  # Submit the patient form at http://localhost:3000/patients
  # Check Google Sheet — new row should appear in "Patient Leads"
  ```

---

## Task 12: Vercel Deployment

- [ ] **Step 1: Push to GitHub**

  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/revivum.git
  git push -u origin main
  ```

- [ ] **Step 2: Deploy to Vercel**

  1. Go to vercel.com → New Project → Import the GitHub repo
  2. Framework: **Next.js** (auto-detected)
  3. Before deploying, add Environment Variables in the Vercel dashboard:
     - `GOOGLE_SERVICE_ACCOUNT_EMAIL`
     - `GOOGLE_PRIVATE_KEY` (paste the full key including `\n` literals)
     - `GOOGLE_SHEET_ID`
  4. Click Deploy

- [ ] **Step 3: Add custom domain**

  In Vercel project Settings → Domains → Add `revivum.com.au`
  Follow DNS configuration instructions (add the provided CNAME/A records at your registrar)

- [ ] **Step 4: Verify production form submission**

  ```bash
  # Submit both forms on the production URL
  # Check Google Sheet for new rows
  ```

- [ ] **Step 5: Final compliance check before sharing publicly**

  - [ ] Every page has TGA disclaimer in footer
  - [ ] No product names appear anywhere in the site
  - [ ] No "book a consultation" or "start treatment" language
  - [ ] Consent checkbox copy matches the approved text verbatim
  - [ ] Privacy Policy and Terms pages are live (even as placeholders)
  - [ ] No clinical efficacy claims on patient-facing pages

- [ ] **Step 6: Commit final state**

  ```bash
  git add .
  git commit -m "feat: production deployment — Revivum Phase 1 MVP"
  ```

---

## Deferred to Phase 2

These were explicitly removed from Phase 1 scope (per wireframe):

- Eligibility quiz or clinical assessment flows
- Clinic finder / practitioner directory
- Booking or triage flows
- Practitioner portal / account login
- CME / educational resources section
- Product-specific pages
- Automated email follow-up (can add via Resend in Phase 2)
- Full Privacy Policy and Terms (placeholder only for Phase 1)
- CRM integration (Airtable/HubSpot) — start with Google Sheets, migrate when volume justifies it
- Animations / scroll effects (keep static for Phase 1 compliance simplicity)

---

## Setup Checklist (Before Starting)

- [ ] Node.js 20+ installed
- [ ] Google account with access to Google Sheets + Google Cloud Console
- [ ] GitHub account (for Vercel deployment)
- [ ] Vercel account (free tier is sufficient)
- [ ] Domain purchased (revivum.com.au) and registrar access available
- [ ] Branding assets (logo, colour palette) — optional for Phase 1, add in Phase 4
