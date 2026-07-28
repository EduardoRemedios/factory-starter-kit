import { readFile, readdir } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const appDir = path.join(root, "app");
const publicDir = path.join(root, "public");
const requiredFiles = ["app/page.tsx", "app/site.tsx", "app/globals.css"];
const errors = [];

async function text(relative) {
  return readFile(path.join(root, relative), "utf8");
}

for (const relative of requiredFiles) {
  try {
    await text(relative);
  } catch {
    errors.push(`missing ${relative}`);
  }
}

const source = `${await text("app/site.tsx")}\n${await text("app/globals.css")}`;
const page = await text("app/page.tsx");
const layout = await text("app/layout.tsx");

const assertions = [
  ["English hero", "AI builds the software."],
  ["English human control", "Humans stay in control."],
  ["Spanish hero", "La IA construye el software."],
  ["Spanish human control", "Las personas mantienen el control."],
  ["AI principal framing", "AI is principal for"],
  ["AI architecture responsibility", "Solution design and architecture"],
  ["human authority", "Humans own intent, constraints, approvals and accountability"],
  ["three-person default", "three people, many AI specialist lanes"],
  ["lower-risk two-person variant", "For lower-risk work"],
  ["designer attribution", "Factory was designed by Eduardo A dos Remedios."],
  ["Codex release ref", "factory-plugin-v0.1.0-rc.1"],
  ["Claude doctor", "/factory:doctor"],
  ["Codex doctor", "$factory-doctor"],
  ["reduced motion", "prefers-reduced-motion: reduce"],
  ["visible focus", ":focus-visible"],
  ["shareable Spanish state", 'lang === "es"'],
];

for (const [label, needle] of assertions) {
  if (!source.includes(needle) && !page.includes(needle) && !layout.includes(needle)) {
    errors.push(`${label}: expected ${JSON.stringify(needle)}`);
  }
}

for (const prohibitedLink of ["github.com", "View on GitHub", "Ver en GitHub", "Explore Factory on GitHub"]) {
  if (source.includes(prohibitedLink)) {
    errors.push(`public GitHub link text remains: ${JSON.stringify(prohibitedLink)}`);
  }
}

for (const [relative, expectedWidth, expectedHeight] of [
  ["public/og.png", 1200, 630],
  ["public/favicon.png", 64, 64],
]) {
  try {
    const image = await readFile(path.join(root, relative));
    const isPng = image.subarray(1, 4).toString("ascii") === "PNG";
    const width = isPng ? image.readUInt32BE(16) : 0;
    const height = isPng ? image.readUInt32BE(20) : 0;
    if (!isPng || width !== expectedWidth || height !== expectedHeight) {
      errors.push(`${relative}: expected PNG ${expectedWidth}x${expectedHeight}, got ${width}x${height}`);
    }
  } catch {
    errors.push(`missing ${relative}`);
  }
}

const prohibited = [
  "tamaran",
  "symphony",
  "theo",
  "mark synenkyy",
  "sasha",
  "client name",
  "customer name",
];
const publicFiles = [
  ...(await readdir(appDir)).map((name) => path.join(appDir, name)),
  ...(await readdir(publicDir)).map((name) => path.join(publicDir, name)),
];

for (const file of publicFiles) {
  if (!/\.(tsx?|css|json|txt|md|svg)$/i.test(file)) continue;
  const contents = (await readFile(file, "utf8")).toLowerCase();
  for (const term of prohibited) {
    if (contents.includes(term)) errors.push(`prohibited term ${JSON.stringify(term)} in ${path.relative(root, file)}`);
  }
}

if (errors.length) {
  console.error(`site verification failed (${errors.length})`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`site verification passed (${assertions.length} assertions, ${publicFiles.length} public files scanned)`);
