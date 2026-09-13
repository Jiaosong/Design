import test from "node:test";
import assert from "node:assert/strict";
import { handleRequest } from "./worker.mjs";

const upstreamOrigin = "https://oleander-knowledge-reader-private.pages.dev";

function mockFetch(handler) {
  return async (request, init) => handler(request, init);
}

test("anonymous root is relayed without widening authority", async () => {
  const response = await handleRequest(
    new Request("https://gateway.example/"),
    mockFetch((request, init) => {
      assert.equal(request.url, `${upstreamOrigin}/`);
      assert.equal(init.redirect, "manual");
      return new Response(null, { status: 302, headers: { Location: "/login" } });
    }),
  );
  assert.equal(response.status, 302);
  assert.equal(response.headers.get("location"), "/login");
  assert.equal(response.headers.get("x-oleander-gateway-role"), "fixed-origin-transport-only");
});

test("absolute Pages redirect is rewritten to gateway origin", async () => {
  const response = await handleRequest(
    new Request("https://gateway.example/login", { method: "POST", body: new URLSearchParams({ password: "x" }) }),
    mockFetch(() => new Response(null, { status: 303, headers: { Location: `${upstreamOrigin}/` } })),
  );
  assert.equal(response.status, 303);
  assert.equal(response.headers.get("location"), "https://gateway.example/");
});

test("cookie is relayed to fixed Pages origin", async () => {
  const response = await handleRequest(
    new Request("https://gateway.example/api/reader-snapshot", { headers: { Cookie: "oleander_reader_session=abc" } }),
    mockFetch((request) => {
      assert.equal(request.url, `${upstreamOrigin}/api/reader-snapshot`);
      assert.equal(request.headers.get("cookie"), "oleander_reader_session=abc");
      return Response.json({ source: { authority: "Notion" } });
    }),
  );
  assert.equal(response.status, 200);
  assert.equal((await response.json()).source.authority, "Notion");
});

test("gateway does not become a generic write tunnel", async () => {
  const post = await handleRequest(new Request("https://gateway.example/api/reader-snapshot", { method: "POST" }), mockFetch(() => { throw new Error("should not fetch"); }));
  assert.equal(post.status, 405);
  assert.equal((await post.json()).error, "post_only_allowed_for_login");

  const put = await handleRequest(new Request("https://gateway.example/", { method: "PUT" }), mockFetch(() => { throw new Error("should not fetch"); }));
  assert.equal(put.status, 405);
  assert.equal((await put.json()).error, "method_not_allowed");
});

test("origin failure fails closed", async () => {
  const response = await handleRequest(new Request("https://gateway.example/"), async () => { throw new Error("offline"); });
  assert.equal(response.status, 502);
  const body = await response.json();
  assert.equal(body.gatewayRole, "FIXED_ORIGIN_TRANSPORT_ONLY");
  assert.equal(body.authority, "NOTION");
});
