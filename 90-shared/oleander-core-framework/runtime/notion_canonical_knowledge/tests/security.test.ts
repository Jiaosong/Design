import { describe, expect, it } from "vitest";
import { decryptSetupSecret, encryptSetupSecret, verifyNotionSignature } from "../src/security";

async function hmac(body: string, token: string): Promise<string> {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey("raw", encoder.encode(token), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const digest = await crypto.subtle.sign("HMAC", key, encoder.encode(body));
  const hex = [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
  return `sha256=${hex}`;
}

describe("webhook security", () => {
  it("validates the Notion HMAC over the raw body", async () => {
    const token = "secret-test";
    const body = JSON.stringify({ id: "event-1", type: "page.content_updated" });
    expect(await verifyNotionSignature(body, token, await hmac(body, token))).toBe(true);
    expect(await verifyNotionSignature(`${body}x`, token, await hmac(body, token))).toBe(false);
  });

  it("encrypts the one-time setup token at rest", async () => {
    const encrypted = await encryptSetupSecret("notion-verification-token", "api-token");
    expect(encrypted).not.toContain("notion-verification-token");
    expect(await decryptSetupSecret(encrypted, "api-token")).toBe("notion-verification-token");
  });
});
