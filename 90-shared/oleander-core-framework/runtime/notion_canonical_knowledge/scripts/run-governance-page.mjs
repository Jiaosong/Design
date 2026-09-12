import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const lines = fs.readFileSync(path.join(root, ".dev.vars"), "utf8").split(/\r?\n/);
const raw = lines.find((line) => line.startsWith("OLEANDER_API_TOKEN="));
if (!raw) throw new Error("OLEANDER_API_TOKEN missing");
let token = raw.slice("OLEANDER_API_TOKEN=".length).trim();
if ((token.startsWith('"') && token.endsWith('"')) || (token.startsWith("'") && token.endsWith("'"))) token = token.slice(1, -1);

const [mode, pageId, ...updateArgs] = process.argv.slice(2);
if (!mode || !pageId) throw new Error("usage: inspect <page_id> | set <page_id> key=value ...");
const updates = Object.fromEntries(
  updateArgs.map((arg) => {
    const i = arg.indexOf("=");
    if (i <= 0) throw new Error(`invalid update arg: ${arg}`);
    const key = arg.slice(0, i);
    const value = arg.slice(i + 1);
    return [key, value === "null" ? null : value];
  }),
);
const base = "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/governance-page";
const init = mode === "inspect"
  ? { headers: { Authorization: `Bearer ${token}` } }
  : {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({ page_id: pageId, updates }),
    };
const url = mode === "inspect" ? `${base}?page_id=${encodeURIComponent(pageId)}` : base;
const response = await fetch(url, init);
const body = await response.text();
console.log(`HTTP ${response.status}`);
try {
  const parsed = JSON.parse(body);
  if (mode === "inspect" && parsed.ok) {
    console.log(JSON.stringify({
      page: parsed.page,
      markdown_length: typeof parsed.markdown === "string" ? parsed.markdown.length : null,
      markdown_preview: typeof parsed.markdown === "string" ? parsed.markdown.slice(0, 500) : null,
      markdown_truncated: parsed.markdown_truncated,
      unknown_block_ids: parsed.unknown_block_ids,
    }, null, 2));
  } else {
    console.log(JSON.stringify(parsed, null, 2));
  }
} catch {
  console.log(body);
}
if (!response.ok) process.exit(1);
