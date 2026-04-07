// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import vercel from '@astrojs/vercel';

// Revivum — headless Ghost frontend.
//
// Static by default: all content pages are prerendered at build time
// using Ghost content fetched via src/lib/ghost.ts. The single exception
// is src/pages/api/leads.ts which sets `export const prerender = false`
// to run as a Vercel serverless function for form POSTs. This matches
// Astro 5's "server islands on a static site" model: the content is
// fast static HTML, only the form endpoint runs server-side.
export default defineConfig({
  site: 'https://revivum.com.au',
  output: 'static',
  adapter: vercel(),
  vite: {
    plugins: [tailwindcss()],
  },
});
