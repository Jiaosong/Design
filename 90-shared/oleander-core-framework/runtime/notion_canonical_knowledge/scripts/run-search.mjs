import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const devVarsPath = path.join(root, ".dev.vars");
if (!fs.existsSync(devVarsPath)) throw new Error(".dev.vars is missing.");

const apiLine = fs
  .readFileSync(devVarsPath, "utf8")
  .split(/\r?\n/)
  .find((line) => line.startsWith("OLEANDER_API_TOKEN="));
if (!apiLine) throw new Error("OLEANDER_API_TOKEN is missing from .dev.vars.");
const token = apiLine.slice("OLEANDER_API_TOKEN=".length).trim();
const includeScoped = process.argv.includes("--scoped");
const query = process.argv.slice(2).filter((arg) => arg !== "--scoped").join(" ").trim();
if (!query) throw new Error("Usage: node scripts/run-search.mjs <query>");

const response = await fetch(
  "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/search",
  {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      top_k: 5,
      include_support: true,
      include_provenance: false,
      include_scoped: includeScoped,
    }),
  },
);

const body = await response.text();
console.log(`HTTP ${response.status}`);
console.log(body);
if (!response.ok) process.exit(1);
