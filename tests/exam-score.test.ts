import test from "node:test";
import assert from "node:assert/strict";
import { SECTIONS, TOTAL_QUESTIONS, TESTING_MINUTES, BREAK_MINUTES, percentileFor, scaledFor } from "../lib/exams/blueprint";
import { buildReport, verdictFor } from "../lib/exams/score";
import type { Attempt, ExamQuestion, FullLengthExam } from "../lib/exams/types";

test("the blueprint matches the published MCAT format", () => {
  assert.equal(TOTAL_QUESTIONS, 230);
  assert.equal(TESTING_MINUTES, 375);           // 6h15 of testing
  assert.equal(BREAK_MINUTES, 50);              // 10 + 30 + 10
  assert.deepEqual(SECTIONS.map(s => s.id), ["chem-phys", "cars", "bio-biochem", "psych-soc"]);
  assert.deepEqual(SECTIONS.map(s => s.questions), [59, 53, 59, 59]);
  assert.deepEqual(SECTIONS.map(s => s.minutes), [95, 90, 95, 95]);
  for (const section of SECTIONS) {
    assert.equal(section.passageQuestions + section.discreteQuestions, section.questions);
  }
});

test("the scaled estimate stays inside the real scale and rises with the raw score", () => {
  assert.equal(scaledFor("bio-biochem", 0, 59).scaled, 118);
  assert.equal(scaledFor("bio-biochem", 59, 59).scaled, 132);
  let previous = 0;
  for (let correct = 0; correct <= 59; correct += 1) {
    const { scaled, low, high } = scaledFor("bio-biochem", correct, 59);
    assert.ok(scaled >= 118 && scaled <= 132, `scaled ${scaled} out of range`);
    assert.ok(scaled >= previous, "the curve must never go down as raw score rises");
    assert.ok(low <= scaled && scaled <= high);
    assert.ok(low >= 118 && high <= 132);
    previous = scaled;
  }
  // CARS is set harsher: the same percentage earns no more than the sciences.
  assert.ok(scaledFor("cars", 30, 53).scaled <= scaledFor("bio-biochem", 34, 59).scaled);
  assert.equal(scaledFor("cars", 0, 0).scaled, 118);
});

test("total percentiles are bounded and monotone", () => {
  assert.equal(percentileFor(400), null);
  assert.equal(percentileFor(600), null);
  assert.equal(percentileFor(472), 1);
  let previous = 0;
  for (let total = 472; total <= 528; total += 1) {
    const value = percentileFor(total);
    assert.ok(value !== null && value >= previous && value <= 100);
    previous = value;
  }
});

function question(id: string, overrides: Partial<ExamQuestion> = {}): ExamQuestion {
  return {
    id,
    passageId: null,
    stem: `Stem ${id}`,
    choices: { A: "a", B: "b", C: "c", D: "d" },
    correct: "A",
    explanation: "Because.",
    wrong: { B: "no", C: "no", D: "no" },
    category: "1D",
    skill: "skill-1",
    difficulty: "medium",
    unit: "metabolism",
    ...overrides,
  };
}

function examOf(counts: Record<string, ExamQuestion[]>): FullLengthExam {
  return {
    id: "test-1",
    name: "Test Form",
    number: 1,
    blurb: "A test form.",
    sections: SECTIONS.map(section => ({ id: section.id, passages: [], questions: counts[section.id] ?? [] })),
  };
}

function attemptOf(exam: FullLengthExam, answers: Attempt["answers"]): Attempt {
  return {
    id: "attempt-1",
    examId: exam.id,
    email: "student@example.com",
    startedAt: "2026-11-18T14:00:00.000Z",
    finishedAt: "2026-11-18T21:30:00.000Z",
    sectionIndex: 4,
    secondsRemaining: 0,
    breakEndsAt: null,
    answers,
    flagged: [],
    timing: {},
    sectionStates: SECTIONS.map(section => ({ id: section.id, secondsRemaining: 0, submittedAt: "2026-11-18T21:30:00.000Z" })),
  };
}

test("the report counts, ranks weak units, and never credits a blank", () => {
  const exam = examOf({
    "bio-biochem": [
      question("bb-1", { unit: "metabolism", category: "1D" }),
      question("bb-2", { unit: "metabolism", category: "1D" }),
      question("bb-3", { unit: "genetics", category: "1B", skill: "skill-4" }),
    ],
    "cars": [question("cars-1", { unit: null, category: "", skill: "cars-comprehension" })],
  });
  // Gets bb-1 right, bb-2 wrong, bb-3 wrong, leaves CARS blank.
  const report = buildReport(exam, attemptOf(exam, { "bb-1": "A", "bb-2": "B", "bb-3": "C" }));

  assert.equal(report.correct, 1);
  assert.equal(report.questions, 4);
  assert.equal(report.missed.length, 3);

  const bio = report.sections.find(s => s.id === "bio-biochem")!;
  assert.equal(bio.correct, 1);
  assert.equal(bio.total, 3);
  assert.equal(bio.answered, 3);
  assert.equal(bio.blank, 0);

  const cars = report.sections.find(s => s.id === "cars")!;
  assert.equal(cars.blank, 1);
  assert.equal(cars.correct, 0);

  // A blank is a miss, with no chosen letter.
  const blank = report.missed.find(m => m.id === "cars-1")!;
  assert.equal(blank.chosen, null);
  assert.equal(blank.correct, "A");

  // Metabolism cost one mark, genetics one; both surface, worst first by count.
  assert.deepEqual(report.recommendations.map(r => r.unit).sort(), ["genetics", "metabolism"]);
  const metabolism = report.recommendations.find(r => r.unit === "metabolism")!;
  assert.equal(metabolism.missed, 1);
  assert.equal(metabolism.total, 2);
  assert.deepEqual(metabolism.categories, ["1D"]);

  // CARS has no unit, so it must never appear as something to "go read".
  assert.ok(!report.recommendations.some(r => r.unit === null || r.unit === ""));

  // The total is the sum of the four section estimates and sits in range.
  assert.equal(report.total, report.sections.reduce((sum, s) => sum + s.scaled, 0));
  assert.ok(report.total >= 472 && report.total <= 528);
  assert.ok(report.totalLow <= report.total && report.total <= report.totalHigh);
});

test("the verdict calls out pacing before content when answers are missing", () => {
  const exam = examOf({ "bio-biochem": Array.from({ length: 20 }, (_, i) => question(`bb-${i}`)) });
  const report = buildReport(exam, attemptOf(exam, { "bb-0": "A", "bb-1": "A" }));
  assert.match(verdictFor(report), /blank/);
});

test("a perfect paper scores the ceiling and recommends nothing", () => {
  const exam = examOf({
    "bio-biochem": [question("bb-1"), question("bb-2")],
    "chem-phys": [question("cp-1", { unit: "acids-bases", category: "5E" })],
  });
  const report = buildReport(exam, attemptOf(exam, { "bb-1": "A", "bb-2": "A", "cp-1": "A" }));
  assert.equal(report.missed.length, 0);
  assert.equal(report.recommendations.length, 0);
  const bio = report.sections.find(s => s.id === "bio-biochem")!;
  assert.equal(bio.scaled, 132);
});
