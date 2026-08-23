import fs from "node:fs";

const target=new URL("./index.html",import.meta.url);
const html=fs.readFileSync(target,"utf8");

if(html.includes('id="ai3d"')&&html.includes('data-section="18"')){
  console.log("C04 public portfolio already contains the integrated game/design/process system. Legacy 112-surface injection is retired.");
  process.exit(0);
}

throw new Error("Expected the current C04 public portfolio runtime. Do not reapply the legacy 112-surface game-line injector to a different source.");
