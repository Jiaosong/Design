const PAGES_ORIGIN = "https://oleander-knowledge-reader-private.pages.dev";
const ALLOWED_METHODS = new Set(["GET", "HEAD", "POST"]);
const ALLOWED_POST_PATHS = new Set(["/login", "/api/reader-content-patch"]);

function securityHeaders(headers = new Headers()) {
  const out = new Headers(headers);
  out.set("Cache-Control", "no-store");
  out.set("Pragma", "no-cache");
  out.set("Referrer-Policy", "no-referrer");
  out.set("X-Content-Type-Options", "nosniff");
  out.set("X-Frame-Options", "DENY");
  out.set("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=(), usb=()");
  return out;
}

function fail(status, error) {
  return Response.json(
    {
      error,
      authority: "NOTION",
      gatewayRole: "FIXED_ORIGIN_TRANSPORT_ONLY",
      upstream: "OLEANDER_PRIVATE_READER_PAGES",
    },
    { status, headers: securityHeaders() },
  );
}

function upstreamRequest(request) {
  const incoming = new URL(request.url);
  const upstream = new URL(incoming.pathname + incoming.search, PAGES_ORIGIN);
  return new Request(upstream, request);
}

function rewriteLocation(request, headers) {
  const location = headers.get("Location");
  if (!location) return;
  if (!location.startsWith(PAGES_ORIGIN)) return;
  const gatewayOrigin = new URL(request.url).origin;
  headers.set("Location", gatewayOrigin + location.slice(PAGES_ORIGIN.length));
}

export async function handleRequest(request, fetchImpl = fetch) {
  const url = new URL(request.url);
  if (!ALLOWED_METHODS.has(request.method)) return fail(405, "method_not_allowed");
  if (request.method === "POST" && !ALLOWED_POST_PATHS.has(url.pathname)) return fail(405, "post_route_not_allowed");

  let upstream;
  try {
    upstream = await fetchImpl(upstreamRequest(request), { redirect: "manual" });
  } catch {
    return fail(502, "private_reader_origin_unavailable");
  }

  const headers = securityHeaders(upstream.headers);
  rewriteLocation(request, headers);
  headers.set("X-OLEANDER-Gateway-Role", "fixed-origin-transport-only");

  return new Response(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
    headers,
  });
}

export default {
  fetch(request) {
    return handleRequest(request);
  },
};
