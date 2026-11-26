// Generates responsive WebP derivatives (and a few crops) for the static site.
// Dev-only. Requires `sharp`:  npm i --no-save sharp@0.33.5
// Usage (from the repo root):  node tools/optimize-images.mjs
//
// Source JPEGs stay in site/assets/img/ and remain the <picture> fallback.
// Derivatives are written to site/assets/img/opt/<name>-<width>.webp.
import sharp from "sharp";
import fs from "node:fs";
import path from "node:path";

const IMG = path.resolve("site/assets/img");
const OUT = path.join(IMG, "opt");
fs.mkdirSync(OUT, { recursive: true });

// Crops made from existing assets. Each one records why it exists.
const CROPS = [
  // Reef wall without the recreational divers (keeps the image about the
  // underwater environment rather than diving tourism).
  { src: "reef.jpg", out: "reef-wall.jpg", extract: { left: 0, top: 0, width: 860, height: 1067 } },
];
// Note: marcie-merksamer.jpg is a 4:5 crop of the headshot embedded in
// content/M. Merksamer_Short Bio 2026.docx (550x366 source, too small for
// retina screens). Replace it with a high-resolution original when supplied.

const WIDTHS = [640, 1200, 2000];

for (const c of CROPS) {
  const src = path.join(IMG, c.src);
  if (!fs.existsSync(src)) { if (!c.optional) console.warn("missing", c.src); continue; }
  await sharp(src).extract(c.extract).jpeg({ quality: 86, mozjpeg: true }).toFile(path.join(IMG, c.out));
  console.log("crop", c.out);
}

for (const f of fs.readdirSync(IMG).filter((n) => n.endsWith(".jpg"))) {
  const name = f.replace(/\.jpg$/, "");
  const meta = await sharp(path.join(IMG, f)).metadata();
  const widths = WIDTHS.filter((w) => w < meta.width).concat(meta.width <= 2000 ? [meta.width] : []);
  for (const w of [...new Set(widths)]) {
    const out = path.join(OUT, `${name}-${w}.webp`);
    await sharp(path.join(IMG, f)).resize({ width: w }).webp({ quality: 74, effort: 5 }).toFile(out);
  }
  console.log(name, meta.width + "x" + meta.height, "->", widths.join(", "));
}
