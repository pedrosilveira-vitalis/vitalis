import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { SECTIONS } from "../lib/exams/blueprint";
import { buildReport, guidanceFor, verdictFor } from "../lib/exams/score";
import type { Attempt, ExamQuestion, FullLengthExam } from "../lib/exams/types";

/**
 * Sits the real Chem/Phys section and reads the report that comes back.
 *
 * Unit tests on synthetic questions prove the arithmetic; this proves the
 * thing a student actually receives. It runs against the shipped content, so
 * a question whose unit tag points nowhere, or an explanation that never got
 * written, shows up as a broken report rather than as a surprise on test day.
 */
type SectionFile = { passages: FullLengthExam["sections"][number]["passages"]; questions: ExamQuestion[] };

function load(section: string): SectionFile | null {
  const path = join(import.meta.dirname, "..", "lib", "exams", "content", "fl1", `${section}.json`);
  try {
    return JSON.parse(readFileSync(path, "utf8")) as SectionFile;
  } catch {
    return null;
  }
}

const content = load("chem-phys")!;

/** Full-Length 1 as it stands on disk, whichever sections are written. */
function examWithRealChemPhys(): FullLengthExam {
  return {
    id: "fl1",
    name: "Vitalis Full-Length 1",
    number: 1,
    blurb: "",
    sections: SECTIONS.map(section => {
      const file = load(section.id);
      return { id: section.id, passages: file?.passages ?? [], questions: file?.questions ?? [] };
    }),
  };
}

/**
 * A student who gets every nth question wrong and runs out of time at the end
 * of one named section, which is what running short of time actually looks
 * like: the blanks cluster at the end of a section, not of the paper.
 */
function sitting(exam: FullLengthExam, wrongEvery: number, leaveBlank: number, blankIn = "chem-phys"): Attempt {
  const questions = exam.sections.flatMap(section =>
    section.id === blankIn
      ? section.questions.slice(0, Math.max(0, section.questions.length - leaveBlank))
      : section.questions,
  );
  const answers: Attempt["answers"] = {};
  const timing: Attempt["timing"] = {};
  const answerable = questions;
  answerable.forEach((question, index) => {
    const letters = ["A", "B", "C", "D"] as const;
    const wrong = wrongEvery > 0 && index % wrongEvery === 0;
    answers[question.id] = wrong ? letters.find(letter => letter !== question.correct)! : question.correct;
    timing[question.id] = 60 + (index % 40);
  });
  return {
    id: "11111111-1111-4111-8111-111111111111",
    examId: exam.id,
    email: "student@example.com",
    startedAt: "2026-11-22T13:00:00.000Z",
    finishedAt: "2026-11-22T20:30:00.000Z",
    sectionIndex: 4,
    secondsRemaining: 0,
    breakEndsAt: null,
    answers,
    flagged: [],
    timing,
    sectionStates: SECTIONS.map(section => ({
      id: section.id,
      secondsRemaining: section.id === "chem-phys" ? 120 : 0,
      submittedAt: "2026-11-22T20:30:00.000Z",
    })),
  };
}

test("the shipped Chem/Phys section produces a complete, usable report", () => {
  const exam = examWithRealChemPhys();
  const attempt = sitting(exam, 4, 3);
  const report = buildReport(exam, attempt);
  const cp = report.sections.find(section => section.id === "chem-phys")!;

  assert.equal(cp.total, 59, "the shipped section must hold 59 questions");
  assert.equal(cp.correct + report.missed.filter(m => m.section === "chem-phys").length, 59);
  assert.ok(cp.scaled >= 118 && cp.scaled <= 132);
  assert.equal(cp.blank, 3, "three unanswered questions must be reported as blank");

  // Every missed question must be reviewable: a student who cannot see why
  // they were wrong has paid for a number, not for teaching.
  for (const miss of report.missed.filter(m => m.section === "chem-phys")) {
    const question = content.questions.find(q => q.id === miss.id)!;
    assert.ok(question.explanation.trim().length > 60, `${miss.id}: no usable explanation`);
    if (miss.chosen) {
      assert.ok((question.wrong[miss.chosen] ?? "").trim().length > 25, `${miss.id}: nothing explains the choice they made`);
    }
    assert.ok(miss.categoryName && miss.categoryName !== miss.category, `${miss.id}: content category did not resolve to a name`);
    assert.ok(miss.skillName.length > 3, `${miss.id}: reasoning skill did not resolve to a name`);
    assert.ok(miss.unit, `${miss.id}: no unit to send the student back to`);
  }

  // Recommendations must be real units, ranked by marks lost.
  assert.ok(report.recommendations.length > 0, "a student missing 15 questions must get somewhere to go");
  const counts = report.recommendations.map(row => row.missed);
  assert.deepEqual(counts, [...counts].sort((a, b) => b - a), "units must be ranked by marks lost");

  // The breakdowns must carry resolved names, not raw codes.
  for (const row of [...cp.categories, ...cp.skills]) {
    assert.ok(row.name && row.name !== row.key, `breakdown row ${row.key} shows a raw code`);
    assert.ok(row.correct <= row.total);
  }

  assert.ok(verdictFor(report).length > 40);
  const guidance = guidanceFor(report);
  assert.ok(guidance.actions.length >= 2);

  // A section with no questions must never be scored or blamed.
  for (const section of report.sections) {
    const written = load(section.id);
    assert.equal(section.scored, Boolean(written?.questions.length), `${section.id}: scored flag must follow whether it is written`);
  }
  if (report.complete) {
    assert.ok(report.total !== null && report.total >= 472 && report.total <= 528);
    assert.ok(report.percentile !== null);
    assert.equal(report.questions, 230, "a complete form is 230 questions");
  } else {
    assert.equal(report.total, null);
  }
});

test("a blank paper and a perfect paper both produce a sane report", () => {
  const exam = examWithRealChemPhys();

  // Every question in every section left unanswered.
  const everything = exam.sections.reduce((sum, section) => sum + section.questions.length, 0);
  const blank = buildReport(exam, sitting(exam, 1, everything, "chem-phys"));
  const noneAnswered = buildReport(exam, { ...sitting(exam, 1, everything, "chem-phys"), answers: {} });
  assert.equal(noneAnswered.correct, 0);
  void blank;
  assert.equal(blank.sections.find(s => s.id === "chem-phys")!.blank, 59);
  assert.equal(blank.correct, 0);
  assert.equal(noneAnswered.sections.find(s => s.id === "chem-phys")!.scaled, 118, "a blank section scores the floor, not NaN");
  if (noneAnswered.complete) {
    assert.equal(noneAnswered.total, 472, "a wholly blank paper scores the floor of the scale, not NaN");
    assert.match(guidanceFor(noneAnswered).actions[0], /pacing|timing/i);
  } else {
    assert.equal(noneAnswered.total, null);
    assert.equal(guidanceFor(noneAnswered).band, "Partial form");
  }

  const perfect = buildReport(exam, sitting(exam, 0, 0));
  assert.equal(perfect.sections.find(s => s.id === "chem-phys")!.correct, 59);
  assert.equal(perfect.recommendations.length, 0, "a perfect paper has nothing to recommend");
  assert.equal(perfect.sections.find(s => s.id === "chem-phys")!.scaled, 132);
});
