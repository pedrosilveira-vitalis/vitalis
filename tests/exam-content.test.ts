import test from "node:test";
import assert from "node:assert/strict";
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { CONTENT_CATEGORIES, SECTIONS, SKILLS } from "../lib/exams/blueprint";
import { UNITS } from "../lib/cheatsheets";
import { DIFFICULTY_MIX, SPECS, TOLERANCE, conceptOf } from "../lib/exams/spec";

/**
 * Structural checks on every written exam section.
 *
 * These run on whatever content exists, so a half-written form is not a
 * failure — but anything already written has to be sound. The point is that a
 * defect in 230 hand-written questions is found here rather than by a student
 * paying for the exam.
 */
const ROOT = join(import.meta.dirname, "..", "lib", "exams", "content");

type Question = {
  id: string; passageId: string | null; stem: string;
  choices: Record<string, string>; correct: string; explanation: string;
  wrong: Record<string, string>; category: string; skill: string;
  difficulty: string; unit: string | null;
};
type Section = { passages: { id: string; title: string; paragraphs: string[] }[]; questions: Question[] };

function files() {
  if (!existsSync(ROOT)) return [] as { exam: string; section: string; data: Section }[];
  const out: { exam: string; section: string; data: Section }[] = [];
  for (const exam of readdirSync(ROOT, { withFileTypes: true }).filter(entry => entry.isDirectory())) {
    for (const file of readdirSync(join(ROOT, exam.name)).filter(name => name.endsWith(".json"))) {
      out.push({
        exam: exam.name,
        section: file.replace(/\.json$/, ""),
        data: JSON.parse(readFileSync(join(ROOT, exam.name, file), "utf8")) as Section,
      });
    }
  }
  return out;
}

const SECTION_IDS = new Set(SECTIONS.map(section => section.id));
const UNIT_IDS = new Set(UNITS.map(unit => String(unit.id)));
const LETTERS = ["A", "B", "C", "D"] as const;

test("every content file belongs to a real section of a real form", () => {
  for (const { exam, section } of files()) {
    assert.ok(SECTION_IDS.has(section as never), `${exam}/${section}: not a section of the exam`);
    assert.match(exam, /^fl\d+$/, `${exam}: unexpected form name`);
  }
});

test("question ids are unique across the whole form and passages are never orphaned", () => {
  const byExam = new Map<string, Set<string>>();
  for (const { exam, section, data } of files()) {
    const seen = byExam.get(exam) ?? new Set<string>();
    const passageIds = new Set(data.passages.map(passage => passage.id));
    for (const question of data.questions) {
      assert.ok(!seen.has(question.id), `${exam}/${section}: duplicate question id ${question.id}`);
      seen.add(question.id);
      if (question.passageId !== null) {
        assert.ok(passageIds.has(question.passageId), `${question.id}: points at missing passage ${question.passageId}`);
      }
    }
    byExam.set(exam, seen);
    const used = new Set(data.questions.map(question => question.passageId));
    for (const passage of data.passages) {
      assert.ok(used.has(passage.id), `${exam}/${section}: passage ${passage.id} has no questions`);
      assert.ok(passage.paragraphs.length >= 2, `${passage.id}: a passage needs at least two paragraphs`);
      assert.ok(passage.title.length > 4, `${passage.id}: passage needs a real title`);
    }
  }
});

test("every question has four distinct choices and a key among them", () => {
  for (const { section, data } of files()) {
    for (const question of data.questions) {
      assert.deepEqual(Object.keys(question.choices).sort(), ["A", "B", "C", "D"], `${question.id}: choice letters`);
      assert.ok(LETTERS.includes(question.correct as never), `${question.id}: key ${question.correct} is not a letter`);
      const texts = LETTERS.map(letter => question.choices[letter].trim().toLowerCase());
      assert.equal(new Set(texts).size, 4, `${question.id}: two choices say the same thing`);
      for (const letter of LETTERS) {
        assert.ok(question.choices[letter].trim().length > 0, `${question.id}: choice ${letter} is empty`);
      }
      assert.ok(question.stem.trim().length > 20, `${question.id}: stem is too thin to be a real question`);
      assert.ok(section === "cars" || question.explanation.trim().length > 60, `${question.id}: explanation is too thin`);
    }
  }
});

test("every wrong choice is explained, and the key is not", () => {
  for (const { data } of files()) {
    for (const question of data.questions) {
      const expected = LETTERS.filter(letter => letter !== question.correct).sort();
      assert.deepEqual(Object.keys(question.wrong).sort(), expected, `${question.id}: wrong-answer notes must cover exactly the distractors`);
      for (const [letter, note] of Object.entries(question.wrong)) {
        assert.ok(note.trim().length > 25, `${question.id}: the note for ${letter} says nothing useful`);
      }
    }
  }
});

test("no drafting debris survives into content", () => {
  // The mis-keyed question found in the lesson bank announced itself with
  // exactly this kind of leftover, so it is worth a standing check.
  const debris = /\b(wait,?\s+recalculat|TODO|FIXME|placeholder|lorem ipsum|XXX)\b/i;
  for (const { data } of files()) {
    for (const question of data.questions) {
      const whole = [question.stem, question.explanation, ...Object.values(question.choices), ...Object.values(question.wrong)].join(" ");
      assert.ok(!debris.test(whole), `${question.id}: drafting debris left in the text`);
    }
  }
});

test("tags are real: content category, reasoning skill, difficulty and unit", () => {
  for (const { section, data } of files()) {
    for (const question of data.questions) {
      assert.ok(["easy", "medium", "hard"].includes(question.difficulty), `${question.id}: difficulty`);
      assert.ok(question.skill in SKILLS, `${question.id}: unknown skill ${question.skill}`);
      if (section === "cars") {
        assert.equal(question.category, "", `${question.id}: CARS questions carry no content category`);
        assert.equal(question.unit, null, `${question.id}: CARS questions have no content unit`);
        assert.ok(question.skill.startsWith("cars-"), `${question.id}: CARS needs a CARS reasoning skill`);
      } else {
        assert.ok(question.category in CONTENT_CATEGORIES, `${question.id}: unknown content category ${question.category}`);
        assert.ok(question.unit && UNIT_IDS.has(question.unit), `${question.id}: unit ${question.unit} is not a real unit`);
        assert.ok(question.skill.startsWith("skill-"), `${question.id}: science needs a numbered reasoning skill`);
      }
    }
  }
});

test("no section is overfull, and a finished section matches the blueprint exactly", () => {
  for (const { exam, section, data } of files()) {
    const blueprint = SECTIONS.find(item => item.id === section);
    assert.ok(blueprint, `${section}: no blueprint`);
    assert.ok(
      data.questions.length <= blueprint.questions,
      `${exam}/${section}: ${data.questions.length} questions written but the blueprint allows ${blueprint.questions}`,
    );
    if (data.questions.length === blueprint.questions) {
      const discretes = data.questions.filter(question => question.passageId === null).length;
      assert.equal(discretes, blueprint.discreteQuestions, `${exam}/${section}: discrete count must match the blueprint`);
    }
  }
});

test("the answer key is spread across all four letters", () => {
  // A form whose key is 40% one letter is guessable, which makes the score
  // meaningless. Only checked once a section has enough questions to judge.
  for (const { exam, section, data } of files()) {
    if (data.questions.length < 40) continue;
    for (const letter of LETTERS) {
      const share = data.questions.filter(question => question.correct === letter).length / data.questions.length;
      assert.ok(share >= 0.15 && share <= 0.35, `${exam}/${section}: ${letter} is the key ${Math.round(share * 100)}% of the time`);
    }
  }
});

/* ------------------------------------------------------------------ *
 * Blueprint accuracy
 *
 * These fire only once a section is complete, because a half-written
 * section is legitimately lopsided. They are what let us say the forms are
 * built to the AAMC's published weighting rather than to our own taste.
 * ------------------------------------------------------------------ */

test("a finished section matches the AAMC's published distribution", () => {
  for (const { exam, section, data } of files()) {
    const spec = SPECS[section as keyof typeof SPECS];
    const blueprint = SECTIONS.find(item => item.id === section);
    if (!spec || !blueprint || data.questions.length !== blueprint.questions) continue;
    const total = data.questions.length;
    const share = (count: number) => count / total;

    for (const [concept, target] of Object.entries(spec.foundationalConcepts)) {
      const actual = share(data.questions.filter(question => conceptOf(question.category) === concept).length);
      assert.ok(
        Math.abs(actual - target) <= TOLERANCE,
        `${exam}/${section}: foundational concept ${concept} is ${Math.round(actual * 100)}% but should be about ${Math.round(target * 100)}%`,
      );
    }

    for (const [skill, target] of Object.entries(spec.skills)) {
      const actual = share(data.questions.filter(question => question.skill === skill).length);
      assert.ok(
        Math.abs(actual - (target as number)) <= TOLERANCE,
        `${exam}/${section}: ${skill} is ${Math.round(actual * 100)}% but should be about ${Math.round((target as number) * 100)}%`,
      );
    }

    // Not stacked toward hard: that is the single most common defect in
    // third-party forms, and it makes the score estimate pessimistic.
    for (const [level, target] of Object.entries(DIFFICULTY_MIX)) {
      const actual = share(data.questions.filter(question => question.difficulty === level).length);
      assert.ok(
        Math.abs(actual - target) <= TOLERANCE + 0.04,
        `${exam}/${section}: ${level} questions are ${Math.round(actual * 100)}% but should be about ${Math.round(target * 100)}%`,
      );
    }

    const passageCount = data.passages.length;
    assert.equal(passageCount, spec.passages.count, `${exam}/${section}: should have ${spec.passages.count} passage sets`);
    for (const passage of data.passages) {
      const attached = data.questions.filter(question => question.passageId === passage.id).length;
      const [min, max] = spec.passages.questionsEach;
      assert.ok(
        attached >= min && attached <= max,
        `${exam}/${section}: passage ${passage.id} carries ${attached} questions, outside the ${min}-${max} the real exam uses`,
      );
    }
  }
});

test("passages are the length the real exam uses", () => {
  for (const { exam, section, data } of files()) {
    const spec = SPECS[section as keyof typeof SPECS];
    if (!spec) continue;
    const [min, max] = spec.passageWords;
    for (const passage of data.passages) {
      const words = passage.paragraphs.join(" ").trim().split(/\s+/).length;
      // A generous floor while authoring; the ceiling is the part that matters,
      // because an over-long passage changes the pacing of the whole section.
      assert.ok(words <= max * 1.25, `${exam}/${section}: ${passage.id} runs ${words} words, well over the ${max} the real exam uses`);
      assert.ok(words >= min * 0.6, `${exam}/${section}: ${passage.id} is only ${words} words, too thin to carry its questions`);
    }
  }
});
