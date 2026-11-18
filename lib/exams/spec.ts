import type { ExamSectionId, SkillId } from "./blueprint";

/**
 * The AAMC's published distribution for each section, and the shape of a form.
 *
 * Every figure here is from the AAMC's own "What's on the MCAT Exam?" and
 * section overview pages. The AAMC states these are approximated to the
 * nearest 5% and vary from one test form to another, so the validator that
 * reads this file allows a tolerance rather than demanding the exact count.
 *
 * Why encode it at all: the common failure of third-party full-lengths is not
 * bad questions, it is a form weighted differently from the real exam and
 * pitched harder than it. A student who practises on a deflated form walks
 * into test day with a wrong idea of where they stand. Holding our forms to
 * the published weighting, and to a difficulty mix that is not stacked toward
 * "hard", is what makes the score estimate worth anything.
 */

export interface SectionSpec {
  id: ExamSectionId;
  /** Passage sets, and how many questions hang off each. */
  passages: { count: number; questionsEach: [min: number, max: number] };
  passageQuestions: number;
  discreteQuestions: number;
  /** Share of the section's questions per foundational concept, as a fraction. */
  foundationalConcepts: Record<string, number>;
  /** Share per reasoning skill, as a fraction. */
  skills: Partial<Record<SkillId, number>>;
  /**
   * Share per undergraduate discipline. Recorded for authoring guidance; we do
   * not tag questions by discipline, because the AAMC's own mapping from a
   * content category to a discipline is not published question by question.
   */
  disciplines: Record<string, number>;
  /** Roughly how long a passage should run, in words. */
  passageWords: [min: number, max: number];
}

/**
 * Difficulty mix we hold every section to.
 *
 * Deliberately not stacked toward "hard". The research on third-party forms is
 * consistent: they run harder than the real exam, which makes their scores
 * pessimistic and their guidance useless. A roughly 25/50/25 spread, with the
 * hard quarter concentrated in reasoning rather than in obscure recall, is
 * what the real exam feels like.
 */
export const DIFFICULTY_MIX: Record<"easy" | "medium" | "hard", number> = {
  easy: 0.25,
  medium: 0.5,
  hard: 0.25,
};

/** How far a written section may drift from the published share. */
export const TOLERANCE = 0.08;

export const SPECS: Record<ExamSectionId, SectionSpec> = {
  "chem-phys": {
    id: "chem-phys",
    passages: { count: 10, questionsEach: [4, 6] },
    passageQuestions: 44,
    discreteQuestions: 15,
    foundationalConcepts: { "4": 0.40, "5": 0.60 },
    skills: { "skill-1": 0.35, "skill-2": 0.45, "skill-3": 0.10, "skill-4": 0.10 },
    disciplines: {
      "general chemistry": 0.30,
      "first-semester biochemistry": 0.25,
      "introductory physics": 0.25,
      "organic chemistry": 0.15,
      "introductory biology": 0.05,
    },
    passageWords: [250, 500],
  },
  cars: {
    id: "cars",
    passages: { count: 9, questionsEach: [5, 7] },
    passageQuestions: 53,
    discreteQuestions: 0,
    foundationalConcepts: {},
    skills: { "cars-comprehension": 0.30, "cars-reasoning-within": 0.30, "cars-reasoning-beyond": 0.40 },
    disciplines: { humanities: 0.50, "social sciences": 0.50 },
    passageWords: [500, 600],
  },
  "bio-biochem": {
    id: "bio-biochem",
    passages: { count: 10, questionsEach: [4, 6] },
    passageQuestions: 44,
    discreteQuestions: 15,
    foundationalConcepts: { "1": 0.55, "2": 0.20, "3": 0.25 },
    skills: { "skill-1": 0.35, "skill-2": 0.45, "skill-3": 0.10, "skill-4": 0.10 },
    disciplines: {
      "introductory biology": 0.65,
      "first-semester biochemistry": 0.25,
      "general chemistry": 0.05,
      "organic chemistry": 0.05,
    },
    passageWords: [250, 500],
  },
  "psych-soc": {
    id: "psych-soc",
    passages: { count: 10, questionsEach: [4, 6] },
    passageQuestions: 44,
    discreteQuestions: 15,
    foundationalConcepts: { "6": 0.25, "7": 0.35, "8": 0.20, "9": 0.15, "10": 0.05 },
    skills: { "skill-1": 0.35, "skill-2": 0.45, "skill-3": 0.10, "skill-4": 0.10 },
    disciplines: {
      psychology: 0.65,
      sociology: 0.30,
      "introductory biology": 0.05,
    },
    passageWords: [250, 500],
  },
};

/** The foundational concept a content category belongs to: "4B" -> "4". */
export function conceptOf(category: string): string {
  return category.match(/^\d+/)?.[0] ?? "";
}

/**
 * How many questions of each kind a section still needs. Used while authoring
 * so each batch is aimed at the gap rather than at whatever is easiest to
 * write, which is how a form ends up 70% content-recall questions.
 */
export function remaining(
  spec: SectionSpec,
  written: { category: string; skill: string; difficulty: string; passageId: string | null }[],
) {
  const total = spec.passageQuestions + spec.discreteQuestions;
  const target = (share: number) => Math.round(share * total);
  const countBy = <T,>(items: T[], predicate: (item: T) => boolean) => items.filter(predicate).length;

  return {
    total: total - written.length,
    discretes: spec.discreteQuestions - countBy(written, item => item.passageId === null),
    concepts: Object.fromEntries(
      Object.entries(spec.foundationalConcepts).map(([concept, share]) => [
        concept,
        target(share) - countBy(written, item => conceptOf(item.category) === concept),
      ]),
    ),
    skills: Object.fromEntries(
      Object.entries(spec.skills).map(([skill, share]) => [
        skill,
        target(share as number) - countBy(written, item => item.skill === skill),
      ]),
    ),
    difficulty: Object.fromEntries(
      Object.entries(DIFFICULTY_MIX).map(([level, share]) => [
        level,
        target(share) - countBy(written, item => item.difficulty === level),
      ]),
    ),
  };
}
