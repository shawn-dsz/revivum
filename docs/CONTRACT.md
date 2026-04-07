# Services Agreement

**Between:**
- **Provider:** Cadre ("Cadre", "we", "us")
- **Client:** [Client Name] on behalf of Revivum Pty Ltd (ABN: TBC) ("the Client", "you")

**Date:** 29 March 2026
**Project:** Revivum Phase 1 — MVP Marketing Website

---

## 1. Scope of Work

Cadre will design and develop a marketing website for Revivum ("the Website") as described in the attached Project Brief (Appendix A). The scope comprises:

### Phase 1 — MVP Build (Fixed Price)

**Deliverables:**

1. **4-page marketing website** built with Next.js, TypeScript, and Tailwind CSS
   - Homepage with hero, audience routing, trust section, and call-to-action
   - Patient information page with educational content and lead capture form
   - Practitioner page with value propositions, credentials, and sign-up form
   - About page with mission statement and company positioning

2. **Lead capture system**
   - Two validated forms (patient enquiry + practitioner sign-up)
   - Server-side API endpoint with input validation
   - Google Sheets integration for lead storage
   - Consent capture for regulatory compliance

3. **Legal page placeholders**
   - Privacy Policy page (copy to be provided by Client)
   - Terms of Use page (copy to be provided by Client)

4. **TGA compliance framework**
   - Global disclaimer bar on every page
   - Compliance notice boxes on patient-facing content
   - Non-promotional, education-focused copy throughout

5. **Responsive design**
   - Mobile-first responsive layout
   - Mobile navigation with hamburger menu
   - Optimised for desktop, tablet, and mobile viewports

6. **Deployment**
   - Hosted on Vercel (Client's account or Cadre-managed)
   - Preview URL for Client review before go-live
   - Production deployment on Client approval

### Explicitly Excluded from Phase 1

The following are **not** included in this agreement and would be scoped separately:

- CRM integration (Salesforce, HubSpot, etc.)
- E-commerce or payment processing
- Patient/practitioner portals or dashboards
- Blog or content management system
- Email automation or marketing integrations
- Search engine optimisation (beyond basic meta tags)
- Custom branding design (logo, brand guidelines, typography selection)
- Marketing copywriting
- Legal document drafting (privacy policy, terms of use)
- Domain registration or transfer
- SSL certificate management (handled automatically by Vercel)
- Ongoing content updates

---

## 2. Pricing

### Cost Estimate Methodology

Pricing is based on estimated development effort at Cadre's standard rate, with a 60% buffer applied to account for:

- Bug fixes and edge cases discovered during development
- Cross-browser and device testing iterations
- Client feedback rounds and revisions
- Integration troubleshooting (Google Sheets API)
- Responsive design refinements
- Deployment and environment configuration

### Phase 1 — MVP Build

| Item | Est. Hours | Rate | Subtotal |
|------|-----------|------|----------|
| Project setup, tooling, design tokens | 2 hrs | $150/hr | $300 |
| Lead capture API + Google Sheets integration | 2 hrs | $150/hr | $300 |
| Layout components (nav, footer, TGA disclaimer) | 2 hrs | $150/hr | $300 |
| Homepage (5 sections) | 3 hrs | $150/hr | $450 |
| Patients page + lead capture form | 3 hrs | $150/hr | $450 |
| Practitioners page + sign-up form | 3 hrs | $150/hr | $450 |
| About page | 1.5 hrs | $150/hr | $225 |
| Privacy & Terms placeholders | 0.5 hrs | $150/hr | $75 |
| Responsive pass + QA + cross-device testing | 3 hrs | $150/hr | $450 |
| Deployment + environment config + handover | 1 hr | $150/hr | $150 |
| **Base estimate** | **21 hrs** | | **$3,150** |
| **60% buffer** (bugs, revisions, edge cases) | **12.6 hrs** | | **$1,890** |
| **Total Phase 1** | **33.6 hrs** | | **$5,040** |

### Recommended: Ongoing Maintenance

| Item | Frequency | Rate |
|------|-----------|------|
| Hosting monitoring + uptime checks | Monthly | Included in retainer |
| Dependency updates + security patches | Monthly | Included in retainer |
| Minor content updates (text, images) | As needed | Included in retainer |
| Bug fixes | As needed | Included in retainer |
| Vercel hosting costs (if on Cadre account) | Monthly | Pass-through at cost |
| **Monthly maintenance retainer** | **Monthly** | **$300/month** |

The maintenance retainer covers up to **2 hours** of work per month. Additional hours are billed at the standard rate ($150/hr). Unused hours do not roll over.

### Summary

| Component | Amount |
|-----------|--------|
| Phase 1 MVP Build (one-off) | **$5,040** |
| Ongoing Maintenance (monthly) | **$300/month** |

---

## 3. Payment Terms

### Phase 1

| Milestone | Amount | Due |
|-----------|--------|-----|
| Deposit (on signing) | $2,520 (50%) | On execution of this agreement |
| Balance (on delivery) | $2,520 (50%) | On delivery of preview URL for review |

### Maintenance

- Billed monthly in advance
- Commences from the date of production deployment
- Either party may cancel with 30 days' written notice

### Payment Method

Bank transfer to Cadre's nominated account. Payment details provided on invoice.

### Late Payment

Invoices unpaid after 14 days from the due date will incur a late fee of 2% per month on the outstanding balance. Cadre reserves the right to suspend services on accounts overdue by more than 30 days.

---

## 4. Timeline

| Event | Target Date |
|-------|------------|
| Agreement signed + deposit received | [Date TBC] |
| Development commences | Within 2 business days of deposit |
| Preview URL delivered for review | 4-5 business days from commencement |
| Client review period | Up to 5 business days |
| Revisions (if any) | 2-3 business days |
| Production deployment (go-live) | On Client approval |

**Total estimated timeline:** 2-3 weeks from deposit to go-live (depending on client review turnaround and provision of required assets).

---

## 5. Client Responsibilities

The Client agrees to:

1. Provide Google Cloud service account credentials for Sheets API integration
2. Create and share a Google Sheet with required tab structure ("Patient Leads", "Practitioner Leads")
3. Provide privacy policy and terms of use text before go-live
4. Provide domain DNS access or credentials when ready to connect
5. Review deliverables within 5 business days of preview delivery
6. Ensure all content published on the site complies with TGA regulations (Cadre does not provide legal or regulatory compliance advice)
7. Obtain independent legal review of website content before go-live

---

## 6. Intellectual Property

- All code, design, and content created by Cadre for this project is assigned to the Client upon receipt of final payment in full.
- Until final payment is received, Cadre retains ownership of all deliverables.
- Third-party open-source components (Next.js, Tailwind CSS, etc.) remain under their respective licences.
- Cadre retains the right to showcase the project in its portfolio (with Client's prior consent).

---

## 7. Revisions & Change Requests

- Phase 1 includes **up to 2 rounds of revisions** on the delivered preview.
- Revisions are limited to changes within the agreed scope (e.g., copy changes, colour adjustments, layout tweaks).
- Requests that fall outside the agreed scope (new pages, new features, CRM integration, etc.) will be treated as change requests and quoted separately.
- Cadre will advise the Client when a request constitutes a change to scope before proceeding.

---

## 8. Warranties & Limitations

- Cadre warrants that the Website will function substantially as described in the Project Brief for 30 days following production deployment.
- Bugs reported within this warranty period will be fixed at no additional cost.
- Cadre does not warrant that the Website will be uninterrupted, error-free, or compatible with all devices and browsers.
- Cadre does not provide legal, medical, or regulatory compliance advice. The Client is solely responsible for ensuring all content complies with applicable laws and regulations, including TGA advertising requirements.
- Cadre's total liability under this agreement is limited to the total fees paid by the Client.

---

## 9. Termination

- Either party may terminate this agreement with 14 days' written notice.
- If the Client terminates before completion, Cadre will invoice for work completed to date at the hourly rate ($150/hr).
- If Cadre terminates, all completed work and source code will be delivered to the Client, and any prepaid amounts for undelivered work will be refunded.

---

## 10. Confidentiality

Both parties agree to keep confidential any proprietary business information shared during the course of this engagement, including but not limited to: business plans, pricing, client lists, and technical implementations. This obligation survives termination of this agreement.

---

## 11. Dispute Resolution

Any disputes arising from this agreement will be resolved through:

1. Good-faith negotiation between the parties (14 days)
2. Mediation by a mutually agreed mediator (if negotiation fails)
3. Binding arbitration under the laws of the relevant Australian state/territory

---

## 12. Acceptance

By signing below, both parties agree to the terms of this agreement and the attached Project Brief (Appendix A).

| | Provider | Client |
|--|---------|--------|
| **Name** | [Your Name] | [Client Name] |
| **Company** | Cadre | Revivum Pty Ltd |
| **Signature** | _________________ | _________________ |
| **Date** | _________________ | _________________ |

---

## Appendix A: Project Brief

See `PROJECT-BRIEF.md` for the full technical specification and scope of work.

## Appendix B: Pricing Rationale

### Why These Rates

The $150/hr rate reflects:

- **Full-stack TypeScript development** — Next.js, React, API development, database integration
- **Production-quality code** — TypeScript, validation, error handling, security best practices
- **Healthcare compliance awareness** — TGA-sensitive content handling, consent management
- **Deployment and DevOps** — Vercel configuration, environment management, CI/CD

### Why the 60% Buffer

The 60% buffer is standard practice for fixed-price engagements and covers:

| Factor | Why It Matters |
|--------|---------------|
| **Cross-browser bugs** | Safari, Chrome, Firefox all render differently; mobile-specific layout issues |
| **Form edge cases** | Validation UX, error states, loading states, success/failure feedback |
| **Google Sheets API** | Auth setup, quota limits, error handling, retry logic |
| **Client revision rounds** | Feedback from client and business partner |
| **Responsive refinement** | Pixel-perfect on mobile, tablet, and desktop takes iteration |
| **TGA compliance review** | May need copy adjustments after legal review |
| **Environment/deployment** | DNS, SSL, environment variables, production readiness |

Without the buffer, the base estimate of $3,150 assumes zero friction, which is unrealistic for any client-facing web project. The buffer ensures the fixed price covers the full engagement without surprise invoices.

### Market Context

For a custom-coded, production-deployed Next.js website with:
- 4 content pages + 2 legal placeholders
- 2 validated lead capture forms with API backend
- Google Sheets integration
- TGA compliance framework
- Responsive design
- Vercel deployment

Comparable Australian agency quotes typically range **$5,000–$15,000** depending on design complexity and agency overhead. This quote sits at the lower end, reflecting the MVP scope and placeholder branding approach.
