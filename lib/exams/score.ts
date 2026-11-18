import { CONTENT_CATEGORIES, SECTIONS, SKILLS, percentileFor, scaledFor, type ExamSectionId, type SkillId } from "./blueprint";
import type { Attempt, ExamQuestion, FullLengthExam } from "./types";

/**
 * Turning a finished attempt into a report a student can act on.
 *
 * The number at the top is the least useful part. What changes a score is
 * knowing which content category is leaking points, whether the misses are
 * content or reasoning, and which unit to go read tonight — so that is what
 * the rest of this computes.
 */

export interface MissedQuestion {
  id: string;
  section: ExamSectionId;
  /** 1-based position within its section, as the student saw it. */
  position: number;
  stem: string;
  chosen: "A" | "B" | "C" | "D" | null;
  correct: "A" | "B" | "C" | "D";
  category: string;
  categoryName: string;
  skill: SkillId;
  skillName: string;
  difficulty: string;
  unit: string | null;
  /** Seconds spent, when we captured it. */
  seconds: number | null;
}

export interface Breakdown {
  key: string;
  name: string;
  correct: number;
  total: number;
  percent: number;
}

export interface SectionScore {
  id: ExamSectionId;
  name: string;
  short: string;
  nickname: string;
  correct: number;
  total: number;
  answered: number;
  percent: number;
  scaled: number;
  low: number;
  high: number;
  /** Seconds of the section's allowance that went unused. */
  secondsRemaining: number;
  /** Questions left blank — nearly always a pacing problem, not a content one. */
  blank: number;
  categories: Breakdown[];
  skills: Breakdown[];
}

export interface Recommendation {
  unit: string;
  section: ExamSectionId;
  missed: number;
  total: number;
  /** The content categories behind the misses, for the "why this unit" line. */
  categories: string[];
}

export interface ExamReport {
  examId: string;
  examName: string;
  startedAt: string;
  finishedAt: string | null;
  total: number;
  totalLow: number;
  totalHigh: number;
  percentile: number | null;
  correct: number;
  questions: number;
  sections: SectionScore[];
  missed: MissedQuestion[];
  /** Units to read next, worst first. */
  recommendations: Recommendation[];
  /** Skills that are weak across the whole exam, worst first. */
  weakestSkills: Breakdown[];
  /** Content categories that are weak across the whole exam, worst first. */
  weakestCategories: Breakdown[];
}

function tally(questions: ExamQuestion[], answers: Attempt["answers"], keyOf: (q: ExamQuestion) => string, nameOf: (key: string) => string): Breakdown[] {
  const buckets = new Map<string, { correct: number; total: number }>();
  for (const question of questions) {
    const key = keyOf(question);
    if (!key) continue;
    const bucket = buckets.get(key) ?? { correct: 0, total: 0 };
    bucket.total += 1;
    if (answers[question.id] === question.correct) bucket.correct += 1;
    buckets.set(key, bucket);
  }
  return [...buckets.entries()]
    .map(([key, bucket]) => ({
      key,
      name: nameOf(key),
      correct: bucket.correct,
      total: bucket.total,
      percent: Math.round((bucket.correct / bucket.total) * 100),
    }))
    .sort((a, b) => a.percent - b.percent || b.total - a.total);
}

export function buildReport(exam: FullLengthExam, attempt: Attempt): ExamReport {
  const sections: SectionScore[] = [];
  const missed: MissedQuestion[] = [];
  const everything: ExamQuestion[] = [];

  for (const section of exam.sections) {
    const blueprint = SECTIONS.find(item => item.id === section.id);
    if (!blueprint) continue;
    const state = attempt.sectionStates.find(item => item.id === section.id);
    let correct = 0;
    let answered = 0;
    let blank = 0;

    section.questions.forEach((question, index) => {
      everything.push(question);
      const chosen = attempt.answers[question.id] ?? null;
      if (chosen) answered += 1; else blank += 1;
      if (chosen === question.correct) {
        correct += 1;
        return;
      }
      missed.push({
        id: question.id,
        section: section.id,
        position: index + 1,
        stem: question.stem,
        chosen,
        correct: question.correct,
        category: question.category,
        categoryName: CONTENT_CATEGORIES[question.category] ?? "Critical analysis and reasoning",
        skill: question.skill,
        skillName: SKILLS[question.skill]?.short ?? "Reasoning",
        difficulty: question.difficulty,
        unit: question.unit,
        seconds: attempt.timing[question.id] ?? null,
      });
    });

    const total = section.questions.length;
    const scale = scaledFor(section.id, correct, total);
    sections.push({
      id: section.id,
      name: blueprint.name,
      short: blueprint.short,
      nickname: blueprint.nickname,
      correct,
      total,
      answered,
      blank,
      percent: scale.percent,
      scaled: scale.scaled,
      low: scale.low,
      high: scale.high,
      secondsRemaining: state?.secondsRemaining ?? 0,
      categories: tally(section.questions, attempt.answers, q => q.category, key => CONTENT_CATEGORIES[key] ?? key),
      skills: tally(section.questions, attempt.answers, q => q.skill, key => SKILLS[key as SkillId]?.short ?? key),
    });
  }

  const total = sections.reduce((sum, section) => sum + section.scaled, 0);
  const totalLow = sections.reduce((sum, section) => sum + section.low, 0);
  const totalHigh = sections.reduce((sum, section) => sum + section.high, 0);

  // Units to read next: ranked by how many points they cost, not by percentage,
  // because a unit that cost six marks matters more than one that cost one.
  const unitBuckets = new Map<string, { section: ExamSectionId; missed: number; total: number; categories: Set<string> }>();
  for (const section of exam.sections) {
    for (const question of section.questions) {
      if (!question.unit) continue;
      const bucket = unitBuckets.get(question.unit) ?? {
        section: section.id,
        missed: 0,
        total: 0,
        categories: new Set<string>(),
      };
      bucket.total += 1;
      if (attempt.answers[question.id] !== question.correct) {
        bucket.missed += 1;
        if (question.category) bucket.categories.add(question.category);
      }
      unitBuckets.set(question.unit, bucket);
    }
  }

  const recommendations: Recommendation[] = [...unitBuckets.entries()]
    .filter(([, bucket]) => bucket.missed > 0)
    .map(([unit, bucket]) => ({
      unit,
      section: bucket.section,
      missed: bucket.missed,
      total: bucket.total,
      categories: [...bucket.categories],
    }))
    .sort((a, b) => b.missed - a.missed || a.unit.localeCompare(b.unit));

  return {
    examId: exam.id,
    examName: exam.name,
    startedAt: attempt.startedAt,
    finishedAt: attempt.finishedAt,
    total,
    totalLow,
    totalHigh,
    percentile: percentileFor(total),
    correct: sections.reduce((sum, section) => sum + section.correct, 0),
    questions: everything.length,
    sections,
    missed,
    recommendations,
    weakestSkills: tally(everything, attempt.answers, q => q.skill, key => SKILLS[key as SkillId]?.short ?? key).filter(row => row.total >= 3),
    weakestCategories: tally(everything, attempt.answers, q => q.category, key => CONTENT_CATEGORIES[key] ?? key).filter(row => row.total >= 2),
  };
}


/**
 * The one-line verdict at the top of the report. Written to be useful rather
 * than encouraging: a student deciding whether to sit the exam in three weeks
 * needs the truth, and a false "great job" costs them a test fee.
 */
export function verdictFor(report: ExamReport): string {
  const blank = report.sections.reduce((sum, section) => sum + section.blank, 0);
  const worst = report.sections.slice().sort((a, b) => a.scaled - b.scaled)[0];
  const best = report.sections.slice().sort((a, b) => b.scaled - a.scaled)[0];
  if (blank >= 10) {
    return `You left ${blank} questions blank, so this score is a pacing result before it is a content result. Fixing timing is worth more than any content review right now.`;
  }
  if (worst && best && best.scaled - worst.scaled >= 4) {
    return `${best.nickname} is carrying this score and ${worst.nickname} is holding it back. The fastest points on the table are in ${worst.nickname}.`;
  }
  return "Your four sections are within a few points of each other, so the gains come from content, not from one broken section.";
}
