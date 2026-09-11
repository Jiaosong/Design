import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const devVarsPath = path.join(root, ".dev.vars");

if (!fs.existsSync(devVarsPath)) {
  throw new Error(".dev.vars is missing; OLEANDER_API_TOKEN is required.");
}

const lines = fs.readFileSync(devVarsPath, "utf8").split(/\r?\n/);
const apiLine = lines.find((line) => line.startsWith("OLEANDER_API_TOKEN="));
if (!apiLine) throw new Error("OLEANDER_API_TOKEN is missing from .dev.vars.");
const token = apiLine.slice("OLEANDER_API_TOKEN=".length).trim();
if (!token) throw new Error("OLEANDER_API_TOKEN is empty.");

const mode = process.argv[2] ?? "bounded";
const limitArg = Number.parseInt(process.argv[3] ?? "1", 10);
const payload = mode === "full" ? {} : { limit: Number.isFinite(limitArg) ? limitArg : 1 };

const response = await fetch(
  "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/reconcile",
  {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  },
);

const body = await response.text();
console.log(`HTTP ${response.status}`);
console.log(body);
if (!response.ok) process.exit(1);
