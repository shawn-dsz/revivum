/*
 * Site settings — parsed from a hidden Ghost Page with slug '_settings'.
 *
 * The client edits global strings (nav CTA labels, footer contact,
 * TGA disclaimer copy) by editing the _settings Page body in Ghost admin.
 * The body is plain text formatted as `key: value` pairs, one per line.
 *
 * Example _settings Page body:
 *
 *   nav_cta_label: Contact Us
 *   footer_email: hello@revivum.com.au
 *   footer_phone: +61 2 0000 0000
 *   tga_disclaimer: Revivum is a TGA-Registered Sponsor and not a clinic...
 *
 * If the _settings page doesn't exist (e.g. local dev without Ghost),
 * getSettings() returns a Settings object populated entirely from the
 * DEFAULTS constant below. All call sites use the returned object without
 * null checks.
 */

import { getPage } from './ghost';

export interface Settings {
  nav_cta_label: string;
  footer_email: string;
  footer_phone: string;
  footer_tagline: string;
  tga_disclaimer: string;
  patient_cta_label: string;
  practitioner_cta_label: string;
}

const DEFAULTS: Settings = {
  nav_cta_label: 'Contact',
  footer_email: 'hello@revivum.com.au',
  footer_phone: '+61 2 0000 0000',
  footer_tagline:
    'Australian peptide therapeutics infrastructure. Connecting patients and practitioners to lawful, regulated therapies.',
  tga_disclaimer:
    'Revivum is a TGA-Registered Sponsor and not a clinic. Information on this site is for educational purposes only and does not constitute medical advice. All content should be reviewed with your healthcare practitioner. No promotional claims about therapeutic goods are made on this site.',
  patient_cta_label: 'Find a Practitioner',
  practitioner_cta_label: 'Join the Network',
};

/**
 * Strip Ghost's HTML wrapping from a rendered Page body so we can parse
 * the raw `key: value` text. Ghost wraps each line in <p> tags.
 */
function stripHtml(html: string): string {
  return html
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ');
}

/**
 * Parse `key: value` lines into a partial Settings object. Unknown keys
 * are silently ignored so the client can add notes in the _settings page
 * without breaking the build.
 */
function parseKeyValue(body: string): Partial<Settings> {
  const result: Record<string, string> = {};
  const lines = body.split('\n');
  for (const raw of lines) {
    const line = raw.trim();
    if (!line) continue;
    const colonIdx = line.indexOf(':');
    if (colonIdx === -1) continue;
    const key = line.slice(0, colonIdx).trim();
    const value = line.slice(colonIdx + 1).trim();
    if (!key || !value) continue;
    result[key] = value;
  }
  return result as Partial<Settings>;
}

let _cached: Settings | null = null;

/**
 * Fetch and parse the global site settings. Cached per-build so multiple
 * calls across components make a single Ghost request.
 *
 * Missing keys fall back to DEFAULTS. If Ghost is unreachable, returns
 * DEFAULTS unchanged.
 */
export async function getSettings(): Promise<Settings> {
  if (_cached) return _cached;

  const page = await getPage('_settings');
  if (!page || !page.html) {
    _cached = { ...DEFAULTS };
    return _cached;
  }

  const parsed = parseKeyValue(stripHtml(page.html));
  _cached = { ...DEFAULTS, ...parsed };
  return _cached;
}
