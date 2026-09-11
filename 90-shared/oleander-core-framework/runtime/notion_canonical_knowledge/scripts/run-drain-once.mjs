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
if (!token) throw new Error("OLEANDER_API_TOKEN is empty.");

const response = await fetch(
  "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/drain-once",
  {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  },
);

const body = await response.text();
console.log(`HTTP ${response.status}`);
console.log(body);
if (!response.ok) process.exit(1);
