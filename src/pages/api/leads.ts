import type { APIRoute } from 'astro';
import { z } from 'zod';

export const prerender = false;

const AU_STATE = z.enum(['VIC', 'NSW', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']);

const PatientLead = z.object({
  kind: z.literal('patient'),
  first_name: z.string().min(1).max(100),
  last_name: z.string().min(1).max(100),
  email: z.string().email(),
  phone: z.string().min(8).max(20),
  state: AU_STATE,
  message: z.string().max(2000).optional().default(''),
  consent: z.literal(true),
});

const PractitionerLead = z.object({
  kind: z.literal('practitioner'),
  first_name: z.string().min(1).max(100),
  last_name: z.string().min(1).max(100),
  ahpra_number: z.string().regex(/^[A-Z]{3}\d{10}$/, 'Invalid AHPRA number format'),
  specialty: z.string().min(1).max(100),
  email: z.string().email(),
  state: AU_STATE,
  practice_name: z.string().max(200).optional().default(''),
  ahpra_consent: z.literal(true),
  contact_consent: z.literal(true),
  marketing_consent: z.boolean().optional().default(false),
});

const LeadPayload = z.discriminatedUnion('kind', [PatientLead, PractitionerLead]);

export const POST: APIRoute = async ({ request }) => {
  try {
    const body: unknown = await request.json();
    const parsed = LeadPayload.safeParse(body);

    if (!parsed.success) {
      return new Response(
        JSON.stringify({
          ok: false,
          error: 'validation_failed',
          issues: parsed.error.flatten(),
        }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // TODO: append parsed.data to Google Sheets once credentials are provided.
    // Expected env vars: GOOGLE_SHEETS_SPREADSHEET_ID, GOOGLE_SHEETS_SERVICE_ACCOUNT_EMAIL, GOOGLE_SHEETS_PRIVATE_KEY
    // Target sheets: 'Patient Leads' tab for kind=patient, 'Practitioner Leads' for kind=practitioner.
    console.log('[leads] received:', parsed.data);

    return new Response(
      JSON.stringify({ ok: true }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (err) {
    console.error('[leads] error:', err);
    return new Response(
      JSON.stringify({ ok: false, error: 'internal_error' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};
