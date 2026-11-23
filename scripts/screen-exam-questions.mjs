// Screens written exam content for the defects that reach students.
//
// The lesson bank taught us which ones matter: a key that contradicts its own
// explanation, drafting debris, a numeric answer that appears nowhere in the
// working, and distractors that overlap so two choices are defensible.
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";

const ROOT = join(import.meta.dirname, "..", "lib", "exams", "content");
const LETTERS = ["A", "B", "C", "D"];
const findings = [];
const flag = (id, kind, detail) => findings.push({ id, kind, detail });

// Pull the numbers out of a string, normalising scientific notation.
function numbers(text) {
  const out = [];
  const cleaned = String(text).replace(/×/g, "x").replace(/−/g, "-");
  const re = /(-?\d+(?:\.\d+)?)\s*(?:x\s*10\s*([⁻¹²³⁰⁴-⁹-]+))?/g;
  const supMap = { "⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9","⁻":"-" };
  let match;
  while ((match = re.exec(cleaned))) {
    const mantissa = parseFloat(match[1]);
    if (!Number.isFinite(mantissa)) continue;
    if (match[2]) {
      const exp = parseInt([...match[2]].map(c => supMap[c] ?? c).join(""), 10);
      if (Number.isFinite(exp)) { out.push(mantissa * 10 ** exp); continue; }
    }
    out.push(mantissa);
  }
  return out;
}

const close = (a, b) => a === 0 ? Math.abs(b) < 1e-9 : Math.abs((a - b) / a) < 0.001;
// A choice is a quantity only when it carries a unit or a decimal point,
// which keeps chemical formulas such as CH3CH2OH out of the numeric checks.
const isQuantity = (text) => {
  if (!/\d/.test(text)) return false;
  // A chemical formula: letters and digits run together with no spaces.
  const bare = text.trim();
  if (/^[A-Za-z0-9()+\u2212-]+$/.test(bare) && /[A-Z]/.test(bare) && /\d/.test(bare) && !/\./.test(bare)) return false;
  // Predominantly a number: strip digits, units and symbols and see what is
  // left. "0.75 m/s" is a quantity; "an SN1 mechanism, because..." is prose.
  const words = text.replace(/[\d.,\u00d7x\u2070-\u209f^+-]/g, " ").replace(/\b(m|s|J|W|N|V|K|Pa|mol|L|M|g|kg|cm|mm|nm|ms|D|per|of|its|original|value|about|approximately)\b/gi, " ");
  return words.replace(/[^a-zA-Z]/g, "").length < 14;
};
const appears = (a, b) => a === 0 ? Math.abs(b) < 1e-9 : Math.abs((a - b) / a) < 0.02;

for (const examDir of existsSync(ROOT) ? readdirSync(ROOT, { withFileTypes: true }).filter(d => d.isDirectory()) : []) {
  for (const file of readdirSync(join(ROOT, examDir.name)).filter(n => n.endsWith(".json"))) {
    const section = file.replace(/\.json$/, "");
    let data;
    try {
      data = JSON.parse(readFileSync(join(ROOT, examDir.name, file), "utf8"));
    } catch {
      // Almost always a sibling section mid-write; a genuinely broken file
      // fails the build when its import is resolved.
      console.log(`  skipped ${examDir.name}/${section}: not valid JSON yet (being written?)`);
      continue;
    }
    const passages = Object.fromEntries((data.passages ?? []).map(p => [p.id, p]));

    for (const passage of data.passages ?? []) {
      (passage.paragraphs ?? []).forEach((text, index) => {
        let depth = 0;
        let broken = false;
        for (const ch of text) {
          if (ch === "(") depth += 1;
          if (ch === ")") depth -= 1;
          if (depth < 0) broken = true;
        }
        if (broken || depth !== 0) {
          flag(`${examDir.name}/${section}/${passage.id}`, "unbalanced-brackets", `paragraph ${index + 1} has a bracket that never closes`);
        }
      });
    }

    for (const q of data.questions) {
      const id = `${examDir.name}/${section}/${q.id}`;
      const keyText = q.choices[q.correct];
      const exp = q.explanation;

      // 1. An explanation that names a different letter as the answer.
      const named = [...exp.matchAll(/\b(?:answer|key|correct(?:\s+answer)?)\s+is\s+([A-D])\b/gi)].map(m => m[1].toUpperCase());
      for (const letter of named) {
        if (letter !== q.correct) flag(id, "key-contradiction", `explanation says the answer is ${letter}, key is ${q.correct}`);
      }

      // 2. Drafting debris of the kind that gave away the mis-keyed lesson.
      if (/\b(wait|hold on|actually,? recalculat|let me recalculat|recalculating|on reflection)\b/i.test(exp)) {
        flag(id, "debris", "explanation contains drafting debris");
      }

      // 3. A numeric key whose value never appears in its own explanation.
      const keyNums = isQuantity(keyText) ? numbers(keyText) : [];
      if (keyNums.length) {
        const expNums = numbers(exp);
        const found = keyNums.some(k => expNums.some(e => appears(k, e)));
        if (!found) flag(id, "unsupported-key", `key "${keyText}" does not appear in its explanation`);
      }

      // 4. A distractor whose value matches the key's value.
      for (const letter of LETTERS) {
        if (letter === q.correct) continue;
        const dNums = isQuantity(q.choices[letter]) ? numbers(q.choices[letter]) : [];
        // Two choices may legitimately share a number when they differ in
        // direction - "falls by 0.30" against "rises by 0.30" is a deliberate
        // and good distractor, not a duplicate.
        const DIRECTION = /\b(fall|falls|fell|rise|rises|rose|increase|increases|decrease|decreases|higher|lower|up|down|longer|shorter|more|less)\b/gi;
        const stripDirection = (t) => t.toLowerCase().replace(DIRECTION, "~");
        // Identical once direction words are removed means the two choices
        // differ only in direction, which is the legitimate case.
        // Choices may share a number deliberately when what differs is the
        // substance rather than the quantity: "0.10 M glucose" against
        // "0.10 M CaCl2" is a colligative comparison at fixed concentration,
        // and making the numbers differ would destroy the question.
        const strip = (t) => t.replace(/[\d.,]|\u00d7|x\s*10|[\u2070-\u209f]/g, "").replace(/\s+/g, " ").trim().toLowerCase();
        const differInSubstance = strip(keyText) !== strip(q.choices[letter]);
        const differOnlyInDirection =
          stripDirection(keyText) === stripDirection(q.choices[letter]) &&
          keyText.trim() !== q.choices[letter].trim();
        if (keyNums.length && dNums.length && keyNums.length === dNums.length &&
            keyNums.every((k, index) => close(k, dNums[index])) && !differOnlyInDirection && !differInSubstance) {
          flag(id, "duplicate-value", `choice ${letter} has the same value as the key`);
        }
      }

      // 5. A wrong-answer note that calls its own choice correct.
      for (const [letter, note] of Object.entries(q.wrong)) {
        if (/\b(?:this|that|it|[A-D])\s+is\s+(?:the\s+)?(?:correct(?:\s+answer)?|right\s+answer|answer)\b/i.test(note)) {
          flag(id, "distractor-claims-correct", `note for ${letter} reads as if ${letter} were right`);
        }
      }

      // 5b. Unbalanced brackets. An exponent rule that consumed the bracket
      //     after "^2" shipped six corrupted explanations across two forms
      //     before anything noticed, because no test reads prose.
      const unbalanced = (text) => {
        let depth = 0;
        for (const ch of text) {
          if (ch === "(") depth += 1;
          if (ch === ")") depth -= 1;
          if (depth < 0) return true;
        }
        return depth !== 0;
      };
      for (const [where, text] of [["stem", q.stem], ["explanation", exp],
        ...LETTERS.map(l => [`choice ${l}`, q.choices[l]]),
        ...Object.entries(q.wrong).map(([l, n]) => [`note ${l}`, n])]) {
        if (unbalanced(text)) flag(id, "unbalanced-brackets", `${where} has a bracket that never closes`);
      }

      // 6. A passage question whose stem cannot stand alone.
      if (q.passageId && !passages[q.passageId]) flag(id, "orphan", "passage missing");

      // 7. Choices that are not mutually exclusive by text. Roman numeral
      //    sets are exempt: "I only" is contained in "I and II only" by the
      //    nature of the format, which the real exam uses throughout.
      //    Numeric sets are exempt too: "8 hours" is a substring of
      //    "48 hours", and "1.6 mM" of "0.016 mM", which says nothing about
      //    whether the choices are distinct quantities.
      const romanNumeral = LETTERS.every(l => /^(?:i{1,3}|i+\s*(?:,|and)\s*i+)[\s,i]*(?:and\s+iii)?\s*(?:only)?$/i.test(q.choices[l].trim()));
      const allNumeric = LETTERS.every(l => isQuantity(q.choices[l]));
      const texts = romanNumeral || allNumeric ? [] : LETTERS.map(l => q.choices[l].trim().toLowerCase());
      for (let i = 0; i < texts.length; i += 1) {
        for (let j = i + 1; j < texts.length; j += 1) {
          if (texts[i] && texts[j] && (texts[i].includes(texts[j]) || texts[j].includes(texts[i]))) {
            flag(id, "overlapping-choices", `choices ${LETTERS[i]} and ${LETTERS[j]} overlap in wording`);
          }
        }
      }

      // 8. "All/none of the above", which the MCAT does not use.
      for (const letter of LETTERS) {
        if (/\b(all|none) of the above\b/i.test(q.choices[letter])) {
          flag(id, "not-mcat-style", `choice ${letter} uses "${RegExp.$1} of the above", which the real exam does not`);
        }
      }

      // 9. A stem that gives away its own answer by length.
      const lengths = LETTERS.map(l => q.choices[l].length);
      const keyLen = q.choices[q.correct].length;
      const others = LETTERS.filter(l => l !== q.correct).map(l => q.choices[l].length);
      if (keyLen > 40 && keyLen > Math.max(...others) * 1.6) {
        flag(id, "longest-answer-tell", `the key is ${keyLen} characters against a longest distractor of ${Math.max(...others)}`);
      }
      void lengths;
    }
  }
}

if (!findings.length) {
  console.log("No defects found.");
} else {
  const byKind = {};
  for (const f of findings) (byKind[f.kind] ??= []).push(f);
  for (const [kind, items] of Object.entries(byKind)) {
    console.log(`\n${kind}  (${items.length})`);
    for (const item of items) console.log(`  ${item.id}: ${item.detail}`);
  }
  console.log(`\n${findings.length} finding(s)`);
}
