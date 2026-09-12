import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const [metadataPath, markdownPath] = process.argv.slice(2);
if (!metadataPath || !markdownPath) throw new Error("usage: node scripts/run-academic-page.mjs <metadata.json> <page.md>");

const raw = fs.readFileSync(path.join(root, ".dev.vars"), "utf8").split(/\r?\n/).find((line) => line.startsWith("OLEANDER_API_TOKEN="));
if (!raw) throw new Error("OLEANDER_API_TOKEN missing");
let token = raw.slice("OLEANDER_API_TOKEN=".length).trim();
if ((token.startsWith('"') && token.endsWith('"')) || (token.startsWith("'") && token.endsWith("'"))) token = token.slice(1, -1);

const metadata = JSON.parse(fs.readFileSync(path.resolve(metadataPath), "utf8"));
const markdown = fs.readFileSync(path.resolve(markdownPath), "utf8");
const response = await fetch("https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/academic-page", {
  method: "POST",
  headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
  body: JSON.stringify({ ...metadata, markdown }),
});
console.log(`HTTP ${response.status}`);
console.log(await response.text());
if (!response.ok) process.exit(1);
