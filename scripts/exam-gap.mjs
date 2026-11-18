// What each written section still needs to match the blueprint.
// Run: node scripts/exam-gap.mjs fl1
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";

const exam = process.argv[2] ?? "fl1";
const dir = join(import.meta.dirname, "..", "lib", "exams", "content", exam);

// Mirrors lib/exams/spec.ts; kept in sync by tests/exam-content.test.ts.
const SPECS = {
  "chem-phys": { total: 59, discretes: 15, passages: 10, concepts: { 4: 0.40, 5: 0.60 } },
  "cars": { total: 53, discretes: 0, passages: 9, concepts: {} },
  "bio-biochem": { total: 59, discretes: 15, passages: 10, concepts: { 1: 0.55, 2: 0.20, 3: 0.25 } },
  "psych-soc": { total: 59, discretes: 15, passages: 10, concepts: { 6: 0.25, 7: 0.35, 8: 0.20, 9: 0.15, 10: 0.05 } },
};
const SKILLS = { "skill-1": 0.35, "skill-2": 0.45, "skill-3": 0.10, "skill-4": 0.10 };
const CARS_SKILLS = { "cars-comprehension": 0.30, "cars-reasoning-within": 0.30, "cars-reasoning-beyond": 0.40 };
const DIFFICULTY = { easy: 0.25, medium: 0.5, hard: 0.25 };

const pad = (value, width) => String(value).padStart(width);

for (const [section, spec] of Object.entries(SPECS)) {
  const path = join(dir, `${section}.json`);
  const data = existsSync(path) ? JSON.parse(readFileSync(path, "utf8")) : { passages: [], questions: [] };
  const questions = data.questions ?? [];
  const need = (share) => Math.round(share * spec.total);
  const count = (predicate) => questions.filter(predicate).length;

  console.log(`\n${section}  ${questions.length}/${spec.total} written, ${data.passages?.length ?? 0}/${spec.passages} passages`);
  if (questions.length >= spec.total) { console.log("  complete"); continue; }
  console.log(`  discretes still needed: ${spec.discretes - count(q => q.passageId === null)}`);
  const parts = [];
  for (const [concept, share] of Object.entries(spec.concepts)) {
    parts.push(`FC${concept} ${pad(need(share) - count(q => String(q.category).startsWith(concept)), 3)}`);
  }
  if (parts.length) console.log(`  by concept: ${parts.join("  ")}`);
  const skillSet = section === "cars" ? CARS_SKILLS : SKILLS;
  console.log(`  by skill:   ${Object.entries(skillSet).map(([skill, share]) => `${skill} ${pad(need(share) - count(q => q.skill === skill), 3)}`).join("  ")}`);
  console.log(`  by level:   ${Object.entries(DIFFICULTY).map(([level, share]) => `${level} ${pad(need(share) - count(q => q.difficulty === level), 3)}`).join("  ")}`);
}
console.log();
