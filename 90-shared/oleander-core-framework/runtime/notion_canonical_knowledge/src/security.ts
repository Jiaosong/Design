const encoder = new TextEncoder();
const decoder = new TextDecoder();

function bytesToHex(bytes: ArrayBuffer): string {
  return [...new Uint8Array(bytes)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function timingSafeStringEqual(left: string, right: string): boolean {
  const a = encoder.encode(left);
  const b = encoder.encode(right);
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i += 1) diff |= (a[i] ?? 0) ^ (b[i] ?? 0);
  return diff === 0;
}

export async function verifyNotionSignature(rawBody: string, token: string, signature: string | null): Promise<boolean> {
  if (!token || !signature) return false;
  const key = await crypto.subtle.importKey("raw", encoder.encode(token), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const digest = await crypto.subtle.sign("HMAC", key, encoder.encode(rawBody));
  const expected = `sha256=${bytesToHex(digest)}`;
  return timingSafeStringEqual(expected, signature);
}

export function isAuthorized(request: Request, token: string): boolean {
  if (!token) return false;
  const authorization = request.headers.get("Authorization");
  return authorization === `Bearer ${token}`;
}

function bytesToBase64(bytes: Uint8Array): string {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary);
}

function base64ToBytes(value: string): Uint8Array {
  const binary = atob(value);
  return Uint8Array.from(binary, (char) => char.charCodeAt(0));
}

async function setupKey(apiToken: string): Promise<CryptoKey> {
  const digest = await crypto.subtle.digest("SHA-256", encoder.encode(`oleander:webhook-setup:${apiToken}`));
  return crypto.subtle.importKey("raw", digest, "AES-GCM", false, ["encrypt", "decrypt"]);
}

export async function encryptSetupSecret(value: string, apiToken: string): Promise<string> {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encrypted = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, await setupKey(apiToken), encoder.encode(value));
  return `${bytesToBase64(iv)}.${bytesToBase64(new Uint8Array(encrypted))}`;
}

export async function decryptSetupSecret(value: string, apiToken: string): Promise<string> {
  const [ivPart, cipherPart] = value.split(".");
  if (!ivPart || !cipherPart) throw new Error("invalid encrypted setup secret");
  const ivDecoded = base64ToBytes(ivPart);
  const cipherDecoded = base64ToBytes(cipherPart);
  const iv = new Uint8Array(ivDecoded.length);
  const cipher = new Uint8Array(cipherDecoded.length);
  iv.set(ivDecoded);
  cipher.set(cipherDecoded);
  const decrypted = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv },
    await setupKey(apiToken),
    cipher,
  );
  return decoder.decode(decrypted);
}
