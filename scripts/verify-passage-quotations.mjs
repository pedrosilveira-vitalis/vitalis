#!/usr/bin/env node
/**
 * Every phrase a question quotes has to exist in the passage it quotes from.
 *
 * Nothing else in the toolkit checks this. The screen looks at structure, the
 * tests look at distributions, the arithmetic verifiers look at numbers — and
 * all of them passed a CARS section in which five questions quoted words that
 * were no longer in their passage. The cause is mechanical: passages are
 * drafted long, the questions are written against the draft, and then the
 * passage is trimmed to its word limit. Every cut is a chance to orphan a
 * quotation, and a CARS question whose quoted phrase is not in the text is
 * unanswerable rather than merely hard.
 *
 * Quotations in this repo are written with single quotes inside the JSON
 * strings of explanations and distractor notes. Apostrophes make that
 * ambiguous, so a span is only treated as a quotation when it opens at a word
 * boundary and closes at one, and when it is long enough that an apostrophe
 * pair is implausible.
 *
 * Usage: node scripts/verify-passage-quotations.mjs [exam ...]
 */
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const ROOT = join(import.meta.dirname, "..", "lib", "exams", "content");
const MIN_WORDS = 3;

/** Compare on words alone: typesetting changes punctuation, not wording. */
const normalise = text =>
  text
    .replace(/[‘’]/g, "'")
    .replace(/[“”]/g, '"')
    .toLowerCase()
    .replace(/[^a-z0-9' ]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();

/**
 * Spans opening and closing on a word boundary. A trailing s-apostrophe or an
 * internal possessive would otherwise produce phantom quotations.
 */
function quotations(text) {
  const out = [];
  const pattern = /(?:^|[\s(\[—–-])'([^']+)'(?=$|[\s.,;:!?)\]—–-])/g;
  for (const match of text.matchAll(pattern)) {
    const phrase = match[1].trim();
    if (phrase.split(/\s+/).length >= MIN_WORDS) out.push(phrase);
  }
  return out;
}

const exams = process.argv.slice(2);
let checked = 0;
let missing = 0;

if (!existsSync(ROOT)) {
  console.log("no content directory yet");
  process.exit(0);
}

for (const exam of readdirSync(ROOT, { withFileTypes: true }).filter(entry => entry.isDirectory())) {
  if (exams.length && !exams.includes(exam.name)) continue;
  for (const file of readdirSync(join(ROOT, exam.name)).filter(name => name.endsWith(".json"))) {
    let data;
    try {
      data = JSON.parse(readFileSync(join(ROOT, exam.name, file), "utf8"));
    } catch {
      console.log(`  skipped ${exam.name}/${file}: not valid JSON yet (being written?)`);
      continue;
    }
    const passages = new Map((data.passages ?? []).map(passage => [passage.id, normalise(passage.paragraphs.join(" "))]));
    for (const question of data.questions ?? []) {
      const haystack = passages.get(question.passageId);
      if (!haystack) continue; // a discrete quotes nothing
      /**
       * Only explanations and distractor notes are checked. A stem may
       * legitimately invent quoted material — a new-information question
       * routinely puts words in a hypothetical writer's mouth — and a choice
       * may quote the stem's invention back. So those two are not checked,
       * but they join the haystack, because an explanation may fairly quote
       * the hypothetical it is discussing.
       */
      const invented = [question.stem, ...Object.values(question.choices ?? {})].map(normalise).join(" ");
      const sources = [
        ["explanation", question.explanation],
        ...Object.entries(question.wrong ?? {}).map(([letter, note]) => [`note ${letter}`, note]),
      ];
      for (const [where, text] of sources) {
        for (const phrase of quotations(text ?? "")) {
          checked += 1;
          // An elided quotation is legitimate: each fragment must appear,
          // and in the order the ellipsis implies.
          const fragments = phrase.split(/\s*\.\.\.\s*/).map(normalise).filter(Boolean);
          let cursor = 0;
          let orphan = null;
          for (const fragment of fragments) {
            const at = haystack.indexOf(fragment, cursor) === -1 && invented.includes(fragment)
              ? cursor
              : haystack.indexOf(fragment, cursor);
            if (at === -1) { orphan = fragment; break; }
            cursor = at + fragment.length;
          }
          if (orphan !== null) {
            missing += 1;
            const which = fragments.length > 1 ? ` (fragment "${orphan}")` : "";
            console.log(`  ${exam.name}/${file} ${question.id} ${where}: passage has no "${phrase}"${which}`);
          }
        }
      }
    }
  }
}

console.log(`\n${checked - missing}/${checked} quoted phrases found in their passage`);
process.exit(missing ? 1 : 0);
