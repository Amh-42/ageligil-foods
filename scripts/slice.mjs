#!/usr/bin/env node
// Cut AI-generated 5x5 food grids into 25 single photos named by dish slug.
//
//   node slice.mjs                      # grids from /Volumes/Vault/Ageligil/foods/grids
//   node slice.mjs --in DIR --out DIR   # other folders (must be on the Vault, or pass --scratch)
//   node slice.mjs --force              # redo grids already cut
//   node slice.mjs --by-time 1          # files without a grid number: oldest = grid 1, next = 2, ...
//
// A grid's number comes from its file name: "grid-07.png", "Grid 7.jpg", "07.webp".
// Gutters are found, not assumed: AI tools rarely draw even cells, so each cut line is
// placed on the most uniform column/row near where it should be. Every grid gets a
// preview with the cut lines drawn, so a bad cut is visible before anything is uploaded.

import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const require = createRequire(import.meta.url);
const sharp = require(path.join(os.homedir(), 'Documents/Projects/Personal/ageligil-et/node_modules/sharp'));

const HERE = path.dirname(new URL(import.meta.url).pathname);
const N = 5;                 // cells per side
const MAX_SIDE = 1024;       // longest side of an output photo (never upscaled)
const THUMB = 400;           // small version for menus
const QUALITY = 86;

// ---------- args ----------
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const flag = (k) => args.includes(k);
const IN = path.resolve(opt('--in', '/Volumes/Vault/Ageligil/foods/grids'));
const OUT = path.resolve(opt('--out', '/Volumes/Vault/Ageligil/foods/photos'));
const FORCE = flag('--force');
const BY_TIME = opt('--by-time', null);
// fixes.json (next to the grids): when the AI put a dish in the wrong cell or drew a duplicate.
//   { "1": { "21": "yekey-wot-firfir", "16": "skip" } }   grid -> cell -> correct slug, or "skip"
const FIXES_FILE = opt('--fixes', null);
// --map grids-map.json: { "use": { "<file name>": <grid> } } for AI files with random names.
// Only files listed under "use" are cut; spares, rejects and duplicates are ignored.
const MAP = opt('--map', null) ? JSON.parse(fs.readFileSync(path.resolve(opt('--map')), 'utf8')).use : null;

// Heavy output belongs on the Vault (Second Brain CLAUDE.md §1c0). Refuse, never fall back.
if (!OUT.startsWith('/Volumes/Vault/') && !flag('--scratch')) {
  console.error(`Refusing: output ${OUT} is not on /Volumes/Vault. Mount the Vault (or pass --scratch for a small test).`);
  process.exit(1);
}
if (OUT.startsWith('/Volumes/Vault/') && !fs.existsSync('/Volumes/Vault')) {
  console.error('Vault not mounted: nothing was cut. Attach it and run again.');
  process.exit(1);
}
if (!fs.existsSync(IN)) { console.error(`No grids folder: ${IN}`); process.exit(1); }

const foods = JSON.parse(fs.readFileSync(path.join(HERE, 'foods.json'), 'utf8')).items;
const byGrid = new Map();
for (const f of foods) { if (!byGrid.has(f.grid)) byGrid.set(f.grid, []); byGrid.get(f.grid).push(f); }
const GRIDS = byGrid.size;
const bySlug = new Map(foods.map((f) => [f.slug, f]));
const fixesPath = FIXES_FILE ? path.resolve(FIXES_FILE) : path.join(IN, 'fixes.json');
const fixes = fs.existsSync(fixesPath) ? JSON.parse(fs.readFileSync(fixesPath, 'utf8')) : {};
for (const [g, m] of Object.entries(fixes)) for (const [c, slug] of Object.entries(m))
  if (slug !== 'skip' && !bySlug.has(slug)) { console.error(`fixes.json: grid ${g} cell ${c}: unknown slug "${slug}"`); process.exit(1); }
// what each cell of a grid actually holds, after fixes
function cellsOf(grid) {
  const fx = fixes[String(grid)] || fixes[String(grid).padStart(2, '0')] || {};
  return byGrid.get(grid).map((it) => {
    const f = fx[String(it.cell)];
    if (f === 'skip') return null;
    const d = f ? bySlug.get(f) : it;
    return { ...d, cell: it.cell, row: it.row, col: it.col };
  }).filter(Boolean);
}

for (const d of ['', 'thumbs', 'previews']) fs.mkdirSync(path.join(OUT, d), { recursive: true });

// ---------- which file is which grid ----------
const IMG = /\.(png|jpe?g|webp|avif|heic|tiff?)$/i;
const files = fs.readdirSync(IN).filter((f) => IMG.test(f) && !f.startsWith('.'));
function gridNo(name) {
  const base = path.parse(name).name;
  let m = base.match(/grid[\s_-]*0*(\d{1,2})(?!\d)/i) || base.match(/^0*(\d{1,2})(?!\d)/);
  const n = m ? Number(m[1]) : null;
  return n && n >= 1 && n <= GRIDS ? n : null;
}
const jobs = [];
const unnamed = [];
const taken = new Map();
for (const f of files) {
  if (MAP && !(f in MAP)) continue;
  const n = MAP ? Number(MAP[f]) : gridNo(f);
  if (n == null) { unnamed.push(f); continue; }
  if (taken.has(n)) { console.warn(`! grid ${n}: two files (${taken.get(n)}, ${f}); using the first`); continue; }
  taken.set(n, f); jobs.push({ file: f, grid: n });
}
if (unnamed.length && BY_TIME) {
  let n = Number(BY_TIME);
  const sorted = unnamed.map((f) => ({ f, t: fs.statSync(path.join(IN, f)).mtimeMs })).sort((a, b) => a.t - b.t);
  for (const { f } of sorted) {
    while (taken.has(n)) n++;
    if (n > GRIDS) { console.warn(`! no grid number left for ${f}`); continue; }
    console.log(`  ${f} -> grid ${n} (by time; check its preview)`);
    taken.set(n, f); jobs.push({ file: f, grid: n, byTime: true }); n++;
  }
} else if (unnamed.length) {
  console.warn(`! ${unnamed.length} file(s) without a grid number in the name, skipped: ${unnamed.join(', ')}`);
  console.warn('  Rename them grid-01 ... grid-40, or run with --by-time <first grid number>.');
}
jobs.sort((a, b) => a.grid - b.grid);

// ---------- gutter finding ----------
// For each column (or row), how uniform is it along its length? Gutters are one flat colour;
// a line through five different dishes never is. Score = 1 - normalised std of luminance.
function profile(lum, w, h, axis) {
  const len = axis === 'x' ? w : h, across = axis === 'x' ? h : w;
  const mean = new Float64Array(len), score = new Float64Array(len);
  for (let i = 0; i < len; i++) {
    let s = 0, s2 = 0;
    for (let j = 0; j < across; j++) {
      const v = axis === 'x' ? lum[j * w + i] : lum[i * w + j];
      s += v; s2 += v * v;
    }
    const m = s / across, sd = Math.sqrt(Math.max(0, s2 / across - m * m));
    mean[i] = m; score[i] = 1 - Math.min(1, sd / 40);
  }
  return { mean, score };
}

// Outer frame: trim uniform bands at the edges (white page around the grid).
function trimEdges(score) {
  let a = 0, b = score.length - 1;
  while (a < b && score[a] > 0.92) a++;
  while (b > a && score[b] > 0.92) b--;
  return [a, b + 1];
}

// Find the 4 inner cut bands between start and end.
function findCuts(score, start, end) {
  const span = end - start, cell = span / N, win = Math.round(cell * 0.18);
  const cuts = [];
  let method = 'gutter';
  for (let k = 1; k < N; k++) {
    const exp = Math.round(start + k * cell);
    const lo = Math.max(start + 1, exp - win), hi = Math.min(end - 1, exp + win);
    // runs of uniform lines
    let best = null;
    for (let i = lo; i <= hi; i++) {
      if (score[i] < 0.85) continue;
      let j = i; while (j + 1 <= hi && score[j + 1] >= 0.85) j++;
      const c = (i + j) / 2, d = Math.abs(c - exp);
      const sc = (j - i + 1) * 2 - d * 0.05;
      if (!best || sc > best.sc) best = { a: i, b: j + 1, sc };
      i = j;
    }
    if (best) { cuts.push([best.a, best.b]); continue; }
    // no gutter: take the most uniform single line, else the expected position
    let bi = exp; for (let i = lo; i <= hi; i++) if (score[i] > score[bi]) bi = i;
    if (score[bi] > 0.6) { cuts.push([bi, bi + 1]); method = method === 'even' ? 'even' : 'seam'; }
    else { cuts.push([exp, exp]); method = 'even'; }
  }
  // cell spans: [start, cut1.a], [cut1.b, cut2.a], ...
  const edges = [start, ...cuts.flat(), end];
  const spans = [];
  for (let i = 0; i < N; i++) spans.push([edges[i * 2], edges[i * 2 + 1]]);
  return { spans, method };
}

// ---------- main ----------
const report = { when: new Date().toISOString(), in: IN, out: OUT, grids: [] };
let made = 0, warnings = 0;

for (const job of jobs) {
  const items = cellsOf(job.grid);
  const done = items.every((it) => fs.existsSync(path.join(OUT, `${it.slug}.webp`)));
  if (done && !FORCE) { console.log(`grid ${String(job.grid).padStart(2, '0')}: already cut (use --force to redo)`); continue; }

  const src = path.join(IN, job.file);
  const img = sharp(src, { failOn: 'none' }).rotate();
  const { data, info } = await img.clone().greyscale().raw().toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height;
  const notes = [];
  if (Math.abs(w / h - 1) > 0.03) notes.push(`not square (${w}x${h})`);

  const px = profile(data, w, h, 'x'), py = profile(data, w, h, 'y');
  const [x0, x1] = trimEdges(px.score), [y0, y1] = trimEdges(py.score);
  const cx = findCuts(px.score, x0, x1), cy = findCuts(py.score, y0, y1);
  const method = [cx.method, cy.method].includes('even') ? 'even' : [cx.method, cy.method].includes('seam') ? 'seam' : 'gutter';
  if (method === 'even') notes.push('no gutters found: cut into equal parts');

  const exp = ((x1 - x0) + (y1 - y0)) / 2 / N;
  const sizes = [...cx.spans, ...cy.spans].map(([a, b]) => b - a);
  const off = Math.max(...sizes.map((s) => Math.abs(s - exp) / exp));
  if (off > 0.15) notes.push(`uneven cells (one is ${Math.round(off * 100)}% off the average)`);

  const base = sharp(src, { failOn: 'none' }).rotate();
  const cells = [];
  for (const it of items) {
    const [ya, yb] = cy.spans[it.row - 1], [xa, xb] = cx.spans[it.col - 1];
    // inset 1.5% so no gutter sliver survives, then centre-crop to a square
    const ix = Math.round((xb - xa) * 0.015), iy = Math.round((yb - ya) * 0.015);
    let left = xa + ix, top = ya + iy, cw = xb - xa - 2 * ix, ch = yb - ya - 2 * iy;
    const side = Math.min(cw, ch);
    left += Math.floor((cw - side) / 2); top += Math.floor((ch - side) / 2);

    // blank-cell check: a cell that is almost one flat colour means a merged or missing dish
    let s = 0, s2 = 0, n = 0;
    for (let y = top; y < top + side; y += 4) for (let x = left; x < left + side; x += 4) { const v = data[y * w + x]; s += v; s2 += v * v; n++; }
    const sd = Math.sqrt(Math.max(0, s2 / n - (s / n) ** 2));
    const cellNote = sd < 12 ? 'looks blank' : null;
    if (cellNote) notes.push(`cell ${it.cell} (${it.name}) looks blank`);

    const crop = base.clone().extract({ left, top, width: side, height: side });
    const full = side > MAX_SIDE ? crop.clone().resize(MAX_SIDE, MAX_SIDE) : crop.clone();
    await full.webp({ quality: QUALITY }).toFile(path.join(OUT, `${it.slug}.webp`));
    await crop.clone().resize(Math.min(THUMB, side), Math.min(THUMB, side)).webp({ quality: 80 }).toFile(path.join(OUT, 'thumbs', `${it.slug}.webp`));
    cells.push({ cell: it.cell, id: it.id, slug: it.slug, name: it.name, px: side, note: cellNote });
    made++;
  }
  if (Math.min(...cells.map((c) => c.px)) < 300) notes.push(`small cells (${Math.min(...cells.map((c) => c.px))} px): generate at a higher resolution`);

  // preview: the grid at 1200 px with cut lines and cell numbers drawn on top
  const pw = 1200, sc = pw / w, ph = Math.round(h * sc);
  const lines = [];
  for (const [a, b] of cx.spans) lines.push(`<rect x="${a * sc}" y="0" width="${(b - a) * sc}" height="${ph}" fill="none" stroke="#ff2d55" stroke-width="3"/>`);
  for (const [a, b] of cy.spans) lines.push(`<rect x="0" y="${a * sc}" width="${pw}" height="${(b - a) * sc}" fill="none" stroke="#ff2d55" stroke-width="3"/>`);
  for (const it of items) {
    const [xa] = cx.spans[it.col - 1], [ya] = cy.spans[it.row - 1];
    const label = `${it.cell}. ${it.name}`.replace(/&/g, '&amp;').replace(/</g, '&lt;').slice(0, 26);
    lines.push(`<rect x="${xa * sc + 6}" y="${ya * sc + 6}" width="${label.length * 7.4 + 10}" height="20" rx="4" fill="rgba(0,0,0,.72)"/><text x="${xa * sc + 11}" y="${ya * sc + 20}" font-family="Helvetica" font-size="12" fill="#fff">${label}</text>`);
  }
  const svg = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${pw}" height="${ph}">${lines.join('')}</svg>`);
  await sharp(src, { failOn: 'none' }).rotate().resize(pw, ph).composite([{ input: svg }]).jpeg({ quality: 80 })
    .toFile(path.join(OUT, 'previews', `grid-${String(job.grid).padStart(2, '0')}.jpg`));

  warnings += notes.length;
  report.grids.push({ grid: job.grid, file: job.file, byTime: !!job.byTime, size: `${w}x${h}`, method, notes, cells });
  console.log(`grid ${String(job.grid).padStart(2, '0')}: ${items.length} photos (${method}, ~${cells[0].px}px)${notes.length ? '  ! ' + notes.join('; ') : ''}`);
}

const notCut = foods.filter((f) => !fs.existsSync(path.join(OUT, `${f.slug}.webp`)) && taken.has(f.grid));
if (notCut.length) {
  fs.writeFileSync(path.join(OUT, 'still-needed.txt'), notCut.map((f) => `${f.slug}\t${f.name}\t${f.desc}`).join('\n') + '\n');
  console.log(`${notCut.length} dish(es) from cut grids still have no photo (skipped or misplaced): see still-needed.txt`);
}
const missing = [...byGrid.keys()].filter((g) => !taken.has(g));
report.missing = missing;
fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 2));
console.log(`\n${made} photos written to ${OUT}`);
if (warnings) console.log(`${warnings} warning(s): open previews/ for the grids marked ! above`);
if (missing.length) console.log(`Grids not in the folder yet: ${missing.join(', ')}`);
