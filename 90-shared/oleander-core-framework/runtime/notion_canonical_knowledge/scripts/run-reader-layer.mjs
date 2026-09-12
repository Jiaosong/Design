import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const raw = fs.readFileSync(path.join(root, ".dev.vars"), "utf8").split(/\r?\n/).find((line) => line.startsWith("OLEANDER_API_TOKEN="));
if (!raw) throw new Error("OLEANDER_API_TOKEN missing");
let token = raw.slice("OLEANDER_API_TOKEN=".length).trim();
if ((token.startsWith('"') && token.endsWith('"')) || (token.startsWith("'") && token.endsWith("'"))) token = token.slice(1, -1);

const response = await fetch("https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/reader-layer", {
  method: "POST",
  headers: { Authorization: `Bearer ${token}` },
});
console.log(`HTTP ${response.status}`);
console.log(await response.text());
if (!response.ok) process.exit(1);
