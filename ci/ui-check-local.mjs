#!/usr/bin/env node
/*
 * Lance les règles UXKIN UI Check en local, sur des fichiers entiers
 * (pas seulement les lignes d'une PR). Pratique pour auditer les prototypes
 * HTML avant de les pousser.
 *
 * Prérequis : cloner l'action une fois
 *   git clone --depth 1 https://github.com/uxkin/ui-check .tools/ui-check
 * Usage :
 *   node ci/ui-check-local.mjs prototypes/<fichiers>.html src/<dossiers>/<fichiers>.css
 * Options :
 *   --tokens tokens.css   fichier dont les couleurs sont considérées comme la charte
 *   --disable a,b         identifiants de règles à ignorer
 *   --json                sortie JSON (pour un script ou un rapport)
 */
import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args.splice(i, 2)[1] : def; };
const flag = name => { const i = args.indexOf(name); if (i >= 0) { args.splice(i, 1); return true; } return false; };
const tokensPath = opt("--tokens", null);
const disabled = new Set((opt("--disable", "") || "").split(",").map(s => s.trim()).filter(Boolean));
const asJson = flag("--json");
const files = args;

const rulesPath = [".tools/ui-check/src/rules.mjs", "node_modules/uxkin-ui-check/src/rules.mjs", "/home/claude/uxkin/ui-check/src/rules.mjs"]
  .map(p => resolve(p)).find(p => existsSync(p));
if (!rulesPath) { console.error("Règles introuvables : git clone --depth 1 https://github.com/uxkin/ui-check .tools/ui-check"); process.exit(2); }
const { checkFile, colorsIn } = await import(pathToFileURL(rulesPath).href);

// Charte : couleurs du fichier de tokens + couleurs utilisées ≥ 2 fois dans l'ensemble des fichiers.
const known = new Set();
if (tokensPath && existsSync(tokensPath)) for (const c of colorsIn(readFileSync(tokensPath, "utf8"))) known.add(c);
// Occurrences réelles (pas l'ensemble unique) : une couleur employée au moins deux fois est un choix, pas une dérive.
const count = new Map();
const RX = /#[0-9a-fA-F]{3,8}\b|rgba?\( *[0-9]+ *, *[0-9]+ *, *[0-9]+/g;
for (const f of files) for (const m of readFileSync(f, "utf8").matchAll(RX)) { const [c] = colorsIn(m[0]); if (c) count.set(c, (count.get(c) || 0) + 1); }
for (const [c, n] of count) if (n >= 2) known.add(c);

const out = [];
for (const f of files) {
  const text = readFileSync(f, "utf8");
  const added = new Set(text.split("\n").map((_, i) => i + 1));
  out.push(...checkFile({ path: f, text, added, disabled, knownColors: known, isTokenFile: p => tokensPath && resolve(p) === resolve(tokensPath) }));
}
if (asJson) { console.log(JSON.stringify(out, null, 1)); process.exit(0); }

const rank = { error: 3, warning: 2, notice: 1 };
out.sort((a, b) => rank[b.severity] - rank[a.severity] || a.path.localeCompare(b.path) || a.line - b.line);
const byFile = {};
for (const r of out) (byFile[r.path] = byFile[r.path] || []).push(r);
for (const [f, rs] of Object.entries(byFile)) {
  console.log(`\n${f}  —  ${rs.length} constat${rs.length > 1 ? "s" : ""}`);
  for (const r of rs) console.log(`  ${r.severity.padEnd(7)} l.${String(r.line).padEnd(5)} ${r.id.padEnd(18)} ${r.message}`);
}
const n = s => out.filter(r => r.severity === s).length;
console.log(`\n${n("error")} erreur(s) · ${n("warning")} avertissement(s) · ${n("notice")} notice(s)`);
process.exit(n("error") ? 1 : 0);
