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
const content = JSON.parse(
  readFileSync(join(import.meta.dirname, "..", "lib", "exams", "content", "fl1", "chem-phys.json"), "utf8"),
) as { passages: FullLengthExam["sections"][number]["passages"]; questions: ExamQuestion[] };

function examWithRealChemPhys(): FullLengthExam {
  return {
    id: "fl1",
    name: "Vitalis Full-Length 1",
    number: 1,
    blurb: "",
    sections: SECTIONS.map(section =>
      section.id === "chem-phys"
        ? { id: section.id, passages: content.passages, questions: content.questions }
        : { id: section.id, passages: [], questions: [] },
    ),
  };
}

/** A student who gets every nth question wrong and runs out of time at the end. */
function sitting(exam: FullLengthExam, wrongEvery: number, leaveBlank: number): Attempt {
  const questions = exam.sections.flatMap(section => section.questions);
  const answers: Attempt["answers"] = {};
  const timing: Attempt["timing"] = {};
  const answerable = questions.slice(0, Math.max(0, questions.length - leaveBlank));
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

  // The unwritten sections must not be scored, named as weak, or counted.
  assert.equal(report.complete, false);
  assert.equal(report.total, null);
  for (const empty of report.sections.filter(s => s.id !== "chem-phys")) {
    assert.equal(empty.scored, false, `${empty.id} has no questions and must not be scored`);
  }
  const advice = guidance.actions.join(" ") + " " + verdictFor(report);
  for (const name of ["CARS", "Bio/Biochem", "Psych/Soc"]) {
    assert.ok(!/dragging|holding it back|points below/.test(advice) || !advice.includes(name),
      `advice must not blame ${name}, which had no questions`);
  }
});

test("a blank paper and a perfect paper both produce a sane report", () => {
  const exam = examWithRealChemPhys();

  const blank = buildReport(exam, sitting(exam, 1, 59));
  assert.equal(blank.correct, 0);
  assert.equal(blank.sections.find(s => s.id === "chem-phys")!.blank, 59);
  // Only Chem/Phys is written, so there is deliberately no total yet.
  assert.equal(blank.complete, false);
  assert.equal(blank.total, null);
  assert.equal(blank.sections.find(s => s.id === "chem-phys")!.scaled, 118, "a blank section scores the floor, not NaN");
  assert.equal(guidanceFor(blank).band, "Partial form");

  const perfect = buildReport(exam, sitting(exam, 0, 0));
  assert.equal(perfect.sections.find(s => s.id === "chem-phys")!.correct, 59);
  assert.equal(perfect.recommendations.length, 0, "a perfect paper has nothing to recommend");
  assert.equal(perfect.sections.find(s => s.id === "chem-phys")!.scaled, 132);
});
