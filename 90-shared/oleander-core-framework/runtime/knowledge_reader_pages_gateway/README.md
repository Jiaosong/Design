# OLEANDER Private Reader Pages Gateway

This Worker is a fixed-origin transport compatibility layer for networks that cannot complete TLS to `*.pages.dev`.

It proxies only to the existing private Pages Reader at `https://oleander-knowledge-reader-private.pages.dev` and deliberately has:

- no Notion credentials;
- no D1 binding;
- no Reader Service Binding;
- no owner resolver;
- no canonical knowledge state;
- no authentication secret of its own.

The existing Pages login/session gate remains authoritative for browser access. The gateway only relays GET/HEAD traffic and POST `/login`, preserves cookies, rewrites absolute redirects back to the gateway origin, and fails closed when the Pages origin is unavailable.

Notion remains the sole canonical authority. This Worker is transport only.
