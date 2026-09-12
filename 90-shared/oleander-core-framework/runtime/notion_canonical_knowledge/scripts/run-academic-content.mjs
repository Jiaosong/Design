import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const [pageId, oldPath, newPath] = process.argv.slice(2);
if (!pageId || !oldPath || !newPath) {
  throw new Error("usage: node scripts/run-academic-content.mjs <page_id> <old.txt> <new.txt>");
}

const raw = fs.readFileSync(path.join(root, ".dev.vars"), "utf8")
  .split(/\r?\n/)
  .find((line) => line.startsWith("OLEANDER_API_TOKEN="));
if (!raw) throw new Error("OLEANDER_API_TOKEN missing");
let token = raw.slice("OLEANDER_API_TOKEN=".length).trim();
if ((token.startsWith('"') && token.endsWith('"')) || (token.startsWith("'") && token.endsWith("'"))) token = token.slice(1, -1);

const oldStr = fs.readFileSync(path.resolve(oldPath), "utf8").trim();
const newStr = fs.readFileSync(path.resolve(newPath), "utf8").trim();
const response = await fetch("https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/academic-page/content", {
  method: "POST",
  headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
  body: JSON.stringify({ page_id: pageId, old_str: oldStr, new_str: newStr }),
});

console.log(`HTTP ${response.status}`);
console.log(await response.text());
if (!response.ok) process.exit(1);
