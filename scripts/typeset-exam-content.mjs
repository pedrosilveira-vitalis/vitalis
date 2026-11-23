// Converts the ASCII shorthand used while drafting into the typeset notation
// the real exam shows. Run over a content file before it ships.
//
// Chemistry and physics on screen for seven hours is not a cosmetic matter: a
// student who has only ever read "HCO3-" and "r^4" has to translate on test
// day, and translation costs seconds they do not have.
import { readFileSync, writeFileSync } from "node:fs";

const ELEMENTS = new Set((
  "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr " +
  "Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb " +
  "Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr"
).split(" "));
const SUB = "₀₁₂₃₄₅₆₇₈₉";
const SUP = { "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
              "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
              "-": "⁻", "+": "⁺" };
const sub = (digits) => [...digits].map(d => SUB[Number(d)] ?? d).join("");
const sup = (chars) => [...chars].map(c => SUP[c] ?? c).join("");

// Order matters: named species first, so the generic formula rules below
// cannot mangle them.
const RULES = [
  [/\[HCO3-\]/g, "[HCO₃⁻]"],
  [/\bHCO3-/g, "HCO₃⁻"],
  [/\bPCO2\b/g, "PCO₂"],
  [/\bPO2\b/g, "PO₂"],
  [/\bCO2\b/g, "CO₂"],
  [/\bH2O\b/g, "H₂O"],
  [/\bO2\b/g, "O₂"],
  [/\bNH4\+/g, "NH₄⁺"],
  [/\bH\+/g, "H⁺"],
  [/\bOH-/g, "OH⁻"],
  // Exponents written as ^n, including negative and multi-digit.
  [/\^\(?(-?\d+)\)?/g, (_m, digits) => sup(digits)],
  // Greek and deltas spelled out while drafting.
  [/\bpi\b/g, "π"],
  [/\beta\b/g, "η"],
  [/\brho\b/g, "ρ"],
  [/\blambda\b/g, "λ"],
  [/\bomega\b/g, "ω"],
  [/\bmicro\b/g, "μ"],
  [/\bdP\b/g, "ΔP"],
  [/\bdT\b/g, "ΔT"],
  [/\bdG\b/g, "ΔG"],
  [/\bEa\b/g, "Eₐ"],
  [/\bdeg\s+([CF])\b/g, "°$1"],
  [/\bdeg\b/g, "°"],
  [/°\s+([CF])\b/g, "°$1"],
  [/->/g, "→"],
  [/\bdS\b/g, "\u0394S"],
  [/\bdH\b/g, "\u0394H"],
  [/\bSN1\b/g, "S\u20991"],
  [/\bSN2\b/g, "S\u20992"],
  [/\bE1\b/g, "E1"],
  [/\bC2O4 2-/g, "C\u2082O\u2084\u00b2\u207b"],
  [/\bCa2\+/g, "Ca\u00b2\u207a"],
  // Ionic charges: Fe2+ -> Fe2+ with a superscript charge.
  [/\b([A-Z][a-z]?)(\d)([+\u2212-])(?![\w])/g, (_m, el, n, sign) =>
    el + (n === "1" ? "" : SUP[n]) + (sign === "+" ? "\u207a" : "\u207b")],
  // Any remaining chemical formula. A token qualifies only if it decomposes
  // entirely into real element symbols, which keeps protein and gene names
  // out: CaC2O4 is Ca + C2 + O4, but SGLT2 would need an element "G", E2F an
  // element "E", and cytochrome P450 is excluded by the two-digit cap.
  [/\b((?:[A-Z][a-z]?\d{0,2}){2,})\b/g, (whole) => {
    if (!/\d/.test(whole)) return whole;
    const parts = whole.match(/[A-Z][a-z]?\d{0,2}/g) ?? [];
    if (parts.join("") !== whole) return whole;
    if (!parts.every(part => ELEMENTS.has(part.replace(/\d+$/, "")))) return whole;
    return whole.replace(/\d/g, (digit) => SUB[Number(digit)]);
  }],
  // Variable subscripts: v1, A2, do, di.
  [/\b([vAPQr])([12])\b/g, (_m, letter, digit) => letter + sub(digit)],
  [/(1\s*\/\s*)do\b/g, "$1dₒ"],
  [/(1\s*\/\s*)di\b/g, "$1dᵢ"],
  // Multiplication, either side numeric or symbolic.
  [/([\d)\]])\s*x\s*(\d)/g, (_m, l, r) => `${l} × ${r}`],
  [/([\d)\]])\s+x\s+([A-Za-z(])/g, (_m, l, r) => `${l} × ${r}`],
  // Numeric ranges take an en dash.
  [/\b(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\b/g, (_m, a, b) => `${a}–${b}`],
];

function typeset(text) {
  let out = text;
  for (const [pattern, replacement] of RULES) out = out.replace(pattern, replacement);
  return out;
}

const SKIP = new Set(["id", "passageId", "url", "correct", "category", "skill", "difficulty", "unit", "kind"]);

function walk(value) {
  if (typeof value === "string") return typeset(value);
  if (Array.isArray(value)) return value.map(walk);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, inner]) => [key, SKIP.has(key) ? inner : walk(inner)]));
  }
  return value;
}

const path = process.argv[2];
if (!path) { console.error("usage: node scripts/typeset-exam-content.mjs <file.json>"); process.exit(1); }
const data = JSON.parse(readFileSync(path, "utf8"));
writeFileSync(path, JSON.stringify(walk(data), null, 1) + "\n");
console.log(`typeset ${path}`);
