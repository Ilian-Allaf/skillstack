// Runs every rule test of the plugin; exits 1 when one fails.
import { spawnSync } from "node:child_process";
import { readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const rules = join(here, "plugin", "rules");
const tsx = join(here, "node_modules", ".bin", process.platform === "win32" ? "tsx.cmd" : "tsx");
const failed = [];
for (const name of readdirSync(rules).filter((file) => file.endsWith(".test.ts")).sort()) {
  const run = spawnSync(tsx, [join(rules, name)], { stdio: "inherit", shell: process.platform === "win32" });
  if (run.status !== 0) failed.push(name);
}
if (failed.length > 0) {
  console.error(`FAILED: ${failed.join(", ")}`);
  process.exit(1);
}
console.log("All rule tests passed.");
