// Password gate for the Rift Nav test site on Cloudflare Pages.
// Every request needs the shared password (any username). Set it in
// Cloudflare: Pages project → Settings → Variables and Secrets → SITE_PASSWORD (encrypted).
// Change the secret and redeploy to revoke everyone's access.

const MAIN = '/Rift%20Finder%20Holo.dc.html';

async function same(a, b) {
  const enc = new TextEncoder();
  const [x, y] = await Promise.all([
    crypto.subtle.digest('SHA-256', enc.encode(a)),
    crypto.subtle.digest('SHA-256', enc.encode(b)),
  ]);
  const ax = new Uint8Array(x), by = new Uint8Array(y);
  let diff = 0;
  for (let i = 0; i < ax.length; i++) diff |= ax[i] ^ by[i];
  return diff === 0;
}

export async function onRequest({ request, env, next }) {
  const expected = env.SITE_PASSWORD;
  if (!expected) return new Response('SITE_PASSWORD is not set for this site.', { status: 500 });

  const [scheme, encoded] = (request.headers.get('Authorization') || '').split(' ');
  let ok = false;
  if (scheme === 'Basic' && encoded) {
    try {
      const decoded = atob(encoded);
      ok = await same(decoded.slice(decoded.indexOf(':') + 1), expected);
    } catch (e) { ok = false; }
  }
  if (!ok) {
    return new Response('Password required.', {
      status: 401,
      headers: { 'WWW-Authenticate': 'Basic realm="Rift Nav", charset="UTF-8"', 'Cache-Control': 'no-store' },
    });
  }

  const url = new URL(request.url);
  if (url.pathname === '/' || url.pathname === '/index.html') return Response.redirect(url.origin + MAIN, 302);

  const res = await next();
  const out = new Response(res.body, res);
  out.headers.set('Cache-Control', 'private, no-store');
  out.headers.set('X-Robots-Tag', 'noindex');
  return out;
}
