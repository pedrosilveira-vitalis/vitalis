import test from "node:test";
import assert from "node:assert/strict";
import { SECTIONS, TOTAL_QUESTIONS, TESTING_MINUTES, BREAK_MINUTES, percentileFor, scaledFor } from "../lib/exams/blueprint";
import { buildReport, guidanceFor, verdictFor } from "../lib/exams/score";
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

  // Two of the four sections carried no questions, so there is no total: a
  // figure built from two real sections and two empty ones would be wrong,
  // not merely low, and a student would act on it.
  assert.equal(report.complete, false);
  assert.equal(report.total, null);
  assert.equal(report.percentile, null);
  assert.equal(report.sections.filter(s => s.scored).length, 2);
});

test("a form with every section written produces a total; a partial one does not", () => {
  const full = examOf(Object.fromEntries(
    SECTIONS.map(section => [section.id, [question(`${section.id}-1`), question(`${section.id}-2`)]]),
  ));
  const complete = buildReport(full, attemptOf(full, Object.fromEntries(
    full.sections.flatMap(s => s.questions).map(q => [q.id, "A" as const]),
  )));
  assert.equal(complete.complete, true);
  assert.equal(complete.total, complete.sections.reduce((sum, s) => sum + s.scaled, 0));
  assert.ok(complete.total! >= 472 && complete.total! <= 528);
  assert.ok(complete.totalLow! <= complete.total! && complete.total! <= complete.totalHigh!);
  assert.ok(complete.percentile !== null);

  const partial = examOf({ cars: [question("cars-1", { unit: null, category: "", skill: "cars-comprehension" })] });
  const partialReport = buildReport(partial, attemptOf(partial, {}));
  assert.equal(partialReport.complete, false);
  assert.equal(partialReport.total, null);
  assert.match(verdictFor(partialReport), /still being written|no total/i);
  assert.equal(guidanceFor(partialReport).band, "Partial form");
});

test("the verdict calls out pacing before content when answers are missing", () => {
  // A complete form, so the pacing logic is reached rather than the
  // partial-form message.
  const exam = examOf(Object.fromEntries(
    SECTIONS.map(section => [section.id, Array.from({ length: 5 }, (_, i) => question(`${section.id}-${i}`))]),
  ));
  const report = buildReport(exam, attemptOf(exam, { "bio-biochem-0": "A", "bio-biochem-1": "A" }));
  assert.equal(report.complete, true);
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
  assert.equal(bio.scored, true);
  assert.equal(report.sections.find(s => s.id === "cars")!.scored, false);
});

test("guidance changes with the band, and names pacing before content", () => {
  const exam = examOf(Object.fromEntries(
    SECTIONS.map(section => [section.id, Array.from({ length: 5 }, (_, i) => question(`${section.id}-${i}`))]),
  ));

  // Nothing answered: the advice must lead on pacing, not on content.
  const abandoned = buildReport(exam, attemptOf(exam, {}));
  const abandonedGuidance = guidanceFor(abandoned);
  assert.match(abandonedGuidance.actions[0], /pacing|timing/i);

  // A strong paper gets protective advice rather than a content rebuild.
  const perfect = buildReport(exam, attemptOf(exam, Object.fromEntries(exam.sections
    .flatMap(section => section.questions)
    .map(q => [q.id, "A" as const]))));
  assert.equal(perfect.complete, true);
  const strong = guidanceFor(perfect);
  assert.ok(strong.actions.length >= 2);
  assert.ok(strong.headline.length > 20);

  // Every band returns something usable rather than an empty list.
  for (const report of [abandoned, perfect]) {
    const guidance = guidanceFor(report);
    assert.ok(guidance.band.length > 0);
    assert.ok(guidance.actions.every(action => action.length > 30), "advice must be specific enough to act on");
  }
});
