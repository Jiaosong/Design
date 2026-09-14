import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const commonGitDir = execFileSync("git", ["rev-parse", "--path-format=absolute", "--git-common-dir"], { cwd: root, encoding: "utf8" }).trim();
const mainCheckoutRoot = path.dirname(commonGitDir);
const varsPath = [
  process.env.OLEANDER_DEV_VARS,
  path.join(root, ".dev.vars"),
  path.join(mainCheckoutRoot, "90-shared", "oleander-core-framework", "runtime", "notion_canonical_knowledge", ".dev.vars"),
].filter(Boolean).find((candidate) => fs.existsSync(candidate));
if (!varsPath && !process.env.OLEANDER_API_TOKEN) throw new Error("OLEANDER_API_TOKEN missing and no .dev.vars found");
const vars = Object.fromEntries(
  (varsPath ? fs.readFileSync(varsPath, "utf8") : "")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#") && line.includes("="))
    .map((line) => {
      const i = line.indexOf("=");
      let value = line.slice(i + 1).trim();
      if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) value = value.slice(1, -1);
      return [line.slice(0, i), value];
    }),
);
const token = process.env.OLEANDER_API_TOKEN || vars.OLEANDER_API_TOKEN;
if (!token) throw new Error("OLEANDER_API_TOKEN missing");
const base = "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/knowledge-graph-schema";
const mode = process.argv[2] ?? "inspect";
const init = mode === "ensure"
  ? {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({ action: "ENSURE_FRAMEWORK_TYPE", reason: "Install the governed Framework Type taxonomy required by the approved OLEANDER knowledge-graph reclassification." }),
    }
  : { headers: { Authorization: `Bearer ${token}` } };
const response = await fetch(base, init);
const text = await response.text();
console.log(`HTTP ${response.status}`);
try { console.log(JSON.stringify(JSON.parse(text), null, 2)); } catch { console.log(text); }
if (!response.ok) process.exit(1);
