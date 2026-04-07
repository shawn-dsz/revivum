// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// Revivum — headless Ghost frontend.
// Output is fully static; forms POST to /api/leads (Vercel function added later).
export default defineConfig({
  site: 'https://revivum.com.au',
  output: 'static',
  vite: {
    plugins: [tailwindcss()],
  },
});
