#!/usr/bin/env python3
"""Generate Project Quote PDF for Revivum."""

from fpdf import FPDF

# --- Design tokens (Cadre brand) ---
ORANGE = (249, 115, 22)       # #F97316
DARK = (17, 24, 39)           # #111827
MID_GRAY = (107, 114, 128)    # #6B7280
LIGHT_BORDER = (229, 231, 235)  # #E5E7EB
ALT_ROW = (249, 250, 251)     # #F9FAFB
WHITE = (255, 255, 255)
LIGHT_ORANGE = (255, 247, 237)

MARGIN = 25  # mm
PAGE_W = 210  # A4
CONTENT_W = PAGE_W - 2 * MARGIN


class QuotePDF(FPDF):
    def header(self):
        self.set_fill_color(*ORANGE)
        self.rect(0, 0, 210, 4, "F")

    def footer(self):
        self.set_y(-18)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*MID_GRAY)
        self.cell(0, 4, "Cadre Pty Ltd  |  ABN 34 689 834 928  |  hello@cadrelabs.io",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 4, f"Page {self.page_no()}/{{nb}}",
                  align="C")


def draw_line(pdf, y=None):
    if y is None:
        y = pdf.get_y()
    pdf.set_draw_color(*LIGHT_BORDER)
    pdf.line(MARGIN, y, PAGE_W - MARGIN, y)


def section_gap(pdf, h=8):
    pdf.ln(h)


def section_heading(pdf, text):
    """Render a section heading with orange left accent."""
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*ORANGE)
    y = pdf.get_y()
    pdf.set_fill_color(*ORANGE)
    pdf.rect(MARGIN, y + 1, 3, 5, "F")
    pdf.set_x(MARGIN + 6)
    pdf.cell(CONTENT_W - 6, 7, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)


def sub_heading(pdf, text):
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W, 5, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def body_text(pdf, text):
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK)
    pdf.multi_cell(CONTENT_W, 4.5, text, new_x="LMARGIN", new_y="NEXT")


def small_text(pdf, text):
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(*MID_GRAY)
    pdf.multi_cell(CONTENT_W, 4, text, new_x="LMARGIN", new_y="NEXT")


def check_space(pdf, needed_mm):
    """Add a new page if less than needed_mm remains."""
    if pdf.get_y() + needed_mm > 297 - 25:
        pdf.add_page()


def draw_phase_table(pdf, items):
    """Draw a line-item table for a phase.
    items: list of (num, name, description, cost_str)
    """
    col_num = 8
    col_name = 38
    col_desc = CONTENT_W - col_num - col_name - 22
    col_cost = 22

    # Table header
    pdf.set_fill_color(*DARK)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(col_num, 6, " #", fill=True)
    pdf.cell(col_name, 6, " Item", fill=True)
    pdf.cell(col_desc, 6, " Description", fill=True)
    pdf.cell(col_cost, 6, "Cost ", align="R", fill=True, new_x="LMARGIN", new_y="NEXT")

    for i, (num, name, desc, cost) in enumerate(items):
        alt = i % 2 == 0
        bg = ALT_ROW if alt else WHITE
        pdf.set_fill_color(*bg)

        pdf.set_font("Helvetica", "", 7)
        desc_lines = pdf.multi_cell(col_desc - 2, 4, desc, dry_run=True, output="LINES")
        row_h = max(len(desc_lines) * 4 + 2, 6)

        check_space(pdf, row_h + 2)

        y_start = pdf.get_y()

        pdf.set_fill_color(*bg)
        pdf.rect(MARGIN, y_start, CONTENT_W, row_h, "F")

        # Number
        pdf.set_xy(MARGIN, y_start + 1)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(*MID_GRAY)
        pdf.cell(col_num, 4, f" {num}")

        # Item name
        pdf.set_xy(MARGIN + col_num, y_start + 1)
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(*DARK)
        pdf.cell(col_name, 4, f" {name}")

        # Description (multi-line)
        pdf.set_xy(MARGIN + col_num + col_name, y_start + 1)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(*MID_GRAY)
        pdf.multi_cell(col_desc - 2, 4, desc)

        # Cost (right-aligned, vertically centred)
        cost_y = y_start + (row_h - 4) / 2
        pdf.set_xy(MARGIN + CONTENT_W - col_cost, cost_y)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.set_text_color(*DARK)
        pdf.cell(col_cost, 4, f"{cost} ", align="R")

        pdf.set_y(y_start + row_h)

    draw_line(pdf)


def draw_payment_table(pdf, rows):
    """Draw a payment schedule mini-table.
    rows: list of (milestone, amount, when)
    """
    col1 = CONTENT_W * 0.4
    col2 = CONTENT_W * 0.35
    col3 = CONTENT_W * 0.25

    pdf.set_fill_color(*DARK)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(col1, 5, " Milestone", fill=True)
    pdf.cell(col2, 5, " Amount", fill=True)
    pdf.cell(col3, 5, " When", fill=True, new_x="LMARGIN", new_y="NEXT")

    for i, (milestone, amount, when) in enumerate(rows):
        bg = ALT_ROW if i % 2 == 0 else WHITE
        pdf.set_fill_color(*bg)
        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "", 7)
        pdf.cell(col1, 5, f" {milestone}", fill=True)
        pdf.cell(col2, 5, f" {amount}", fill=True)
        pdf.cell(col3, 5, f" {when}", fill=True, new_x="LMARGIN", new_y="NEXT")


def bullet_list(pdf, items):
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(*DARK)
    for item in items:
        check_space(pdf, 5)
        pdf.cell(5, 4, "-")
        pdf.multi_cell(CONTENT_W - 5, 4, item, new_x="LMARGIN", new_y="NEXT")


def build():
    pdf = QuotePDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.set_margins(MARGIN, 12, MARGIN)
    pdf.add_page()

    pdf.set_y(16)

    # -- Title block --
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*DARK)
    pdf.cell(CONTENT_W / 2, 5, "Cadre Pty Ltd", new_x="RIGHT", new_y="TOP")

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*ORANGE)
    pdf.cell(CONTENT_W / 2, 8, "PROJECT QUOTE", align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*MID_GRAY)
    pdf.cell(CONTENT_W, 4, "ABN: 34 689 834 928  |  hello@cadrelabs.io", new_x="LMARGIN", new_y="NEXT")

    section_gap(pdf, 8)
    draw_line(pdf)
    section_gap(pdf, 6)

    # -- Meta info --
    meta_left = MARGIN
    meta_right = MARGIN + CONTENT_W / 2 + 5
    col_w = CONTENT_W / 2 - 5
    top_y = pdf.get_y()

    meta_items_left = [
        ("Prepared for", "Revivum Pty Ltd"),
    ]
    meta_items_right = [
        ("Prepared by", "Cadre"),
        ("Date", "31 March 2026"),
        ("Valid until", "30 April 2026"),
    ]

    pdf.set_xy(meta_left, top_y)
    for label, value in meta_items_left:
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(*MID_GRAY)
        pdf.cell(28, 5, label)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*DARK)
        pdf.cell(col_w - 28, 5, value, new_x="LMARGIN", new_y="NEXT")

    pdf.set_xy(meta_right, top_y)
    for label, value in meta_items_right:
        pdf.set_x(meta_right)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(*MID_GRAY)
        pdf.cell(24, 5, label)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*DARK)
        pdf.cell(col_w - 24, 5, value, new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(max(pdf.get_y(), top_y + 18))
    section_gap(pdf, 6)
    draw_line(pdf)
    section_gap(pdf, 8)

    # -- Project Summary --
    section_heading(pdf, "Project Summary")
    body_text(pdf, (
        "Design and build a professional marketing website for Revivum, a peptide therapeutics "
        "company operating as a TGA-Registered Sponsor in Australia. The site will attract patient "
        "enquiries and practitioner sign-ups, with lead capture forms that feed into a Google Sheet "
        "for your team to follow up manually."
    ))

    section_gap(pdf, 4)
    small_text(pdf, (
        "Built to healthcare industry standards with TGA compliance in mind. "
        "Branding can be applied later when finalised with your business partner."
    ))

    section_gap(pdf, 6)
    draw_line(pdf)
    section_gap(pdf, 8)

    # ================================================================
    # PHASE 1
    # ================================================================
    section_heading(pdf, "Phase 1 -- Marketing Website ($5,500)")

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*MID_GRAY)
    pdf.cell(CONTENT_W, 5,
             "Timeline: 1-2 weeks  |  Get a professional presence online and start capturing leads.",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    phase1_items = [
        ("1", "Marketing Website",
         "Custom-designed, mobile-responsive website based on your wireframe. Homepage with audience "
         "routing (patients vs practitioners), patient information page with educational content, "
         "practitioner page with value propositions and credentials, about page with mission and "
         "positioning. Privacy policy and terms of use placeholder pages (your legal copy to be "
         "provided). TGA-compliant disclaimer framework on every page.",
         "$3,000"),
        ("2", "Lead Capture Forms",
         "Patient enquiry form and practitioner sign-up form with validation. Patient form captures "
         "name, email, phone, state, and referral source. Practitioner form captures name, AHPRA "
         "number, specialty, email, state, and practice. Both forms include consent checkboxes for "
         "regulatory compliance.",
         "$1,200"),
        ("3", "Google Sheets Integration",
         "Forms submit to a Google Sheet so your team can see leads immediately. Two tabs: Patient "
         "Leads and Practitioner Leads. Each submission is timestamped and includes consent status. "
         "No CRM needed to get started.",
         "$500"),
        ("4", "Hosting & Deployment",
         "Hosted on Vercel. Staging preview for your review before go-live, production deployment, "
         "environment configuration, SSL included automatically. DNS preparation notes for connecting "
         "your domain.",
         "$500"),
        ("5", "Cross-Device Testing",
         "Tested on mobile, tablet, and desktop across Safari, Chrome, and Firefox. Forms tested on "
         "mobile devices to make sure the experience is smooth for everyone.",
         "$300"),
    ]
    draw_phase_table(pdf, phase1_items)

    # Phase 1 total
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*ORANGE)
    pdf.set_fill_color(*LIGHT_ORANGE)
    pdf.cell(CONTENT_W - 22, 7, " Phase 1 Total", fill=True)
    pdf.cell(22, 7, "$5,500 ", align="R", fill=True, new_x="LMARGIN", new_y="NEXT")

    section_gap(pdf, 6)

    sub_heading(pdf, "Payment")
    draw_payment_table(pdf, [
        ("Deposit", "$2,750 ($3,025 incl. GST)", "On signing"),
        ("Go-live payment", "$2,750 ($3,025 incl. GST)", "On launch day"),
    ])

    section_gap(pdf, 4)
    sub_heading(pdf, "What You Get")
    bullet_list(pdf, [
        "A live, professional marketing website with 4 content pages and 2 legal placeholders",
        "Patients can learn about peptide therapeutics and submit an enquiry",
        "Practitioners can learn about the partnership model and apply to join the network",
        "All leads land in a Google Sheet your team can access immediately",
        "TGA-compliant disclaimer on every page",
        "Fully responsive -- works on phones, tablets, and desktops",
        "Hosted and deployed -- ready to connect to your domain",
    ])

    section_gap(pdf, 6)
    draw_line(pdf)
    section_gap(pdf, 8)

    # ================================================================
    # PROJECT TOTAL
    # ================================================================
    check_space(pdf, 30)
    section_heading(pdf, "Project Total")

    col1 = CONTENT_W * 0.5
    col2 = CONTENT_W * 0.25
    col3 = CONTENT_W * 0.25

    pdf.set_fill_color(*DARK)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(col1, 5, " Phase", fill=True)
    pdf.cell(col2, 5, " Cost", fill=True)
    pdf.cell(col3, 5, " Timeline", fill=True, new_x="LMARGIN", new_y="NEXT")

    rows = [
        ("Phase 1 -- Marketing Website", "$5,500", "1-2 weeks"),
    ]
    for i, (phase, cost, timeline) in enumerate(rows):
        bg = ALT_ROW if i % 2 == 0 else WHITE
        pdf.set_fill_color(*bg)
        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "", 7)
        pdf.cell(col1, 5, f" {phase}", fill=True)
        pdf.cell(col2, 5, f" {cost}", fill=True)
        pdf.cell(col3, 5, f" {timeline}", fill=True, new_x="LMARGIN", new_y="NEXT")

    # Totals
    pdf.set_fill_color(*LIGHT_ORANGE)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*DARK)
    pdf.cell(col1, 6, " Total (excl. GST)", fill=True)
    pdf.cell(col2, 6, " $5,500", fill=True)
    pdf.cell(col3, 6, "", fill=True, new_x="LMARGIN", new_y="NEXT")

    pdf.set_fill_color(*ORANGE)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(col1, 6, " Total (incl. GST)", fill=True)
    pdf.cell(col2, 6, " $6,050", fill=True)
    pdf.cell(col3, 6, "", fill=True, new_x="LMARGIN", new_y="NEXT")

    section_gap(pdf, 6)
    draw_line(pdf)
    section_gap(pdf, 8)

    # ================================================================
    # INCLUDED / NOT INCLUDED
    # ================================================================
    check_space(pdf, 55)
    section_heading(pdf, "What's Included")
    bullet_list(pdf, [
        "Fully designed and built marketing website based on your wireframe",
        "4 content pages: homepage, patients, practitioners, about",
        "2 legal placeholder pages: privacy policy, terms of use (your legal copy to be provided)",
        "Patient enquiry form with validation and consent capture",
        "Practitioner sign-up form with AHPRA details and consent capture",
        "Google Sheets integration for lead storage",
        "TGA compliance framework (disclaimers, non-promotional language, consent management)",
        "Mobile-responsive design across all pages",
        "Hosting on Vercel with staging and production environments",
        "Up to 2 rounds of revisions within scope",
        "30 days of post-launch support for bugs",
    ])

    section_gap(pdf, 6)

    check_space(pdf, 35)
    section_heading(pdf, "What's Not Included")
    bullet_list(pdf, [
        "Branding design (logo, brand colours, typography) -- to be provided by your team",
        "Marketing copywriting -- current copy is placeholder; your team provides final content",
        "Privacy policy and terms of use text -- to be provided by your legal counsel",
        "CRM integration (quoted separately when you're ready)",
        "E-commerce or payment processing",
        "Email automation or marketing campaigns",
        "SEO beyond basic meta tags",
        "Ongoing content updates after launch (quoted separately)",
    ])

    section_gap(pdf, 6)
    draw_line(pdf)
    section_gap(pdf, 8)

    # ================================================================
    # WHAT WE NEED
    # ================================================================
    check_space(pdf, 40)
    section_heading(pdf, "What We Need From You")
    bullet_list(pdf, [
        "Brand direction or confirmation that the wireframe look is good to start",
        "Privacy policy text (mentioned having one from previous ventures)",
        "Terms of use text",
        "Google Cloud service account credentials (we can walk you through setup)",
        "A Google Sheet with Patient Leads and Practitioner Leads tabs",
        "Confirmation of exact form fields and any regulatory requirements",
        "Domain access when you're ready to connect (after preview approval)",
    ])

    section_gap(pdf, 6)
    draw_line(pdf)
    section_gap(pdf, 8)

    # ================================================================
    # AFTER PHASE 1
    # ================================================================
    check_space(pdf, 30)
    section_heading(pdf, "After Phase 1")
    body_text(pdf, (
        "Once your site is live and capturing leads, we can add features like CRM integration, "
        "e-commerce capabilities, email automation, and advanced SEO. These are quoted separately "
        "when you're ready -- no obligation."
    ))

    section_gap(pdf, 6)
    draw_line(pdf)
    section_gap(pdf, 8)

    # ================================================================
    # NEXT STEPS
    # ================================================================
    check_space(pdf, 40)
    section_heading(pdf, "Next Steps")

    steps = [
        "Review this quote and confirm the scope",
        "Sign off and pay the $2,750 deposit ($3,025 incl. GST) to begin",
        "We schedule a quick kickoff to get your Google Cloud credentials and confirm form fields",
    ]
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK)
    for i, step in enumerate(steps, 1):
        pdf.cell(8, 6, f"{i}.")
        pdf.cell(CONTENT_W - 8, 6, step, new_x="LMARGIN", new_y="NEXT")

    section_gap(pdf, 8)

    # Closing
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MID_GRAY)
    pdf.cell(CONTENT_W, 5, "Questions? Contact us -- happy to walk through any line item.",
             new_x="LMARGIN", new_y="NEXT")

    # --- Output ---
    output_path = "/Users/shawn/proj/worktrees/revivum/highly-herring/.context/Quote-Revivum.pdf"
    pdf.output(output_path)
    print(f"Quote generated: {output_path}")


if __name__ == "__main__":
    build()
