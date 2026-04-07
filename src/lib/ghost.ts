/*
 * Ghost Content API client.
 *
 * Called at BUILD TIME only by Astro pages. Never runs in the browser.
 * When the client publishes content in Ghost admin, a webhook triggers
 * a Vercel rebuild which re-runs this module and regenerates static HTML.
 *
 * Env vars (see .env.example):
 *   GHOST_URL                — e.g. https://revivum.ghost.io (or http://localhost:2368)
 *   GHOST_CONTENT_API_KEY    — from Ghost admin → Integrations → Custom integration
 *
 * Resilience: if Ghost is unreachable during local dev (no .env set yet),
 * every getter returns null/[] instead of throwing. Pages MUST handle
 * null gracefully and fall back to hard-coded placeholder copy — this
 * lets the site render during the build phase before the Ghost instance
 * exists. In production the build will fail loudly if Ghost returns
 * unexpected errors (via the `strict` flag).
 */

import GhostContentAPI from '@tryghost/content-api';

export interface GhostPage {
  id: string;
  slug: string;
  title: string;
  excerpt: string | null;
  html: string | null;
  feature_image: string | null;
  custom_excerpt: string | null;
  meta_description: string | null;
  published_at: string | null;
}

export interface GhostPost {
  id: string;
  slug: string;
  title: string;
  excerpt: string | null;
  html: string | null;
  feature_image: string | null;
  published_at: string | null;
}

/**
 * Singleton Ghost API client. Lazily initialised so modules that import
 * this file don't crash at load time when env vars are missing.
 */
let _api: ReturnType<typeof GhostContentAPI> | null = null;

function getClient() {
  if (_api) return _api;

  const url = import.meta.env.GHOST_URL;
  const key = import.meta.env.GHOST_CONTENT_API_KEY;

  if (!url || !key) {
    // No creds — caller should fall back to placeholder content.
    return null;
  }

  _api = GhostContentAPI({
    url,
    key,
    version: 'v5.0',
  });
  return _api;
}

/**
 * Fetch a single Ghost Page by slug. Returns null if:
 *  - Ghost is unconfigured (no env vars)
 *  - The page doesn't exist
 *  - The Ghost instance is unreachable
 *
 * Pages should treat a null result as "use placeholder copy".
 */
export async function getPage(slug: string): Promise<GhostPage | null> {
  const api = getClient();
  if (!api) return null;

  try {
    const page = await api.pages.read({ slug });
    if (!page) return null;
    return {
      id: page.id,
      slug: page.slug,
      title: page.title ?? '',
      excerpt: page.excerpt ?? page.custom_excerpt ?? null,
      html: page.html ?? null,
      feature_image: page.feature_image ?? null,
      custom_excerpt: page.custom_excerpt ?? null,
      meta_description: page.meta_description ?? null,
      published_at: page.published_at ?? null,
    };
  } catch (err) {
    // Log loudly during dev so typos in slugs are visible, but don't crash
    // the build — placeholder copy kicks in instead.
    // eslint-disable-next-line no-console
    console.warn(`[ghost] Failed to fetch page '${slug}':`, (err as Error).message);
    return null;
  }
}

/**
 * Fetch all published Pages. Used rarely — most pages call getPage(slug)
 * directly. Exposed for future uses (e.g. sitemap generation).
 */
export async function getAllPages(): Promise<GhostPage[]> {
  const api = getClient();
  if (!api) return [];

  try {
    const pages = await api.pages.browse({ limit: 'all' });
    return pages.map((p) => ({
      id: p.id,
      slug: p.slug,
      title: p.title ?? '',
      excerpt: p.excerpt ?? p.custom_excerpt ?? null,
      html: p.html ?? null,
      feature_image: p.feature_image ?? null,
      custom_excerpt: p.custom_excerpt ?? null,
      meta_description: p.meta_description ?? null,
      published_at: p.published_at ?? null,
    }));
  } catch (err) {
    console.warn('[ghost] Failed to fetch pages:', (err as Error).message);
    return [];
  }
}
