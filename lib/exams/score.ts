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
  /** False when the section carried no questions, so it was never sat. */
  scored: boolean;
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
  /**
   * Null unless all four sections were sat. A total built from three real
   * sections and one empty one is not a low score, it is a wrong one, and a
   * student would act on it.
   */
  total: number | null;
  totalLow: number | null;
  totalHigh: number | null;
  percentile: number | null;
  /** True only when every section carried questions. */
  complete: boolean;
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
      scored: total > 0,
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

  // Only a form where every section carried questions produces a total.
  const scoredSections = sections.filter(section => section.scored);
  const complete = scoredSections.length === SECTIONS.length;
  const total = complete ? scoredSections.reduce((sum, section) => sum + section.scaled, 0) : null;
  const totalLow = complete ? scoredSections.reduce((sum, section) => sum + section.low, 0) : null;
  const totalHigh = complete ? scoredSections.reduce((sum, section) => sum + section.high, 0) : null;

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
    complete,
    percentile: total === null ? null : percentileFor(total),
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
  const scored = report.sections.filter(section => section.scored);
  const blank = scored.reduce((sum, section) => sum + section.blank, 0);
  const worst = scored.slice().sort((a, b) => a.scaled - b.scaled)[0];
  const best = scored.slice().sort((a, b) => b.scaled - a.scaled)[0];
  if (!report.complete) {
    const names = scored.map(section => section.nickname).join(", ") || "no section";
    return `This form is still being written, so there is no total score. What follows covers ${names} only.`;
  }
  if (blank >= 10) {
    return `You left ${blank} questions blank, so this score is a pacing result before it is a content result. Fixing timing is worth more than any content review right now.`;
  }
  if (worst && best && best.scaled - worst.scaled >= 4) {
    return `${best.nickname} is carrying this score and ${worst.nickname} is holding it back. The fastest points on the table are in ${worst.nickname}.`;
  }
  return "Your four sections are within a few points of each other, so the gains come from content, not from one broken section.";
}

export interface Guidance {
  band: string;
  headline: string;
  /** What to do with the weeks remaining, in priority order. */
  actions: string[];
}

/**
 * What to do next, given where the score actually landed.
 *
 * A student at 495 and a student at 515 have almost nothing in common in what
 * should change, and telling both of them to "review your weak areas" is the
 * sort of advice that fills a report without helping anyone. The bands below
 * are drawn from where the published percentile curve bends: the middle of the
 * distribution is crowded, so a few raw marks move a score a long way there,
 * and much less at the top.
 */
export function guidanceFor(report: ExamReport): Guidance {
  const scoredSections = report.sections.filter(section => section.scored);
  const blank = scoredSections.reduce((sum, section) => sum + section.blank, 0);
  const sorted = scoredSections.slice().sort((a, b) => a.scaled - b.scaled);
  const worst = sorted[0];
  const spread = sorted.length > 1 ? sorted[sorted.length - 1].scaled - worst.scaled : 0;
  const cars = scoredSections.find(section => section.id === "cars");
  const rushed = scoredSections.filter(section => section.blank >= 3).map(section => section.nickname);

  // Pacing leads in every band when it is the problem. A student who left ten
  // questions blank is not short of content, whatever their score says, and
  // burying that under "go and read the lessons" wastes the report.
  const urgent: string[] = [];
  if (blank >= 10) {
    urgent.push(`Fix pacing before anything else. You left ${blank} questions unanswered, and every one was a free guess you did not take - there is no penalty for a wrong answer.`);
  } else if (rushed.length) {
    urgent.push(`Work on timing in ${rushed.join(" and ")}: you ran out of time there, and no amount of content review fixes a clock problem.`);
  }

  const actions: string[] = [];

  if (spread >= 4 && worst) {
    actions.push(`${worst.nickname} is ${spread} points below your best section. That gap is the cheapest place to gain, because the ceiling there is furthest away.`);
  }

  const average = scoredSections.length
    ? scoredSections.reduce((sum, section) => sum + section.scaled, 0) / scoredSections.length
    : 0;
  if (cars && cars.scaled <= average - 1) {
    actions.push("CARS is dragging the total. It responds to daily practice rather than to study: one timed passage set every day, reviewed properly, beats a long session once a week.");
  }

  const top = report.weakestSkills[0];
  if (top && top.percent < 60 && top.total >= 5) {
    actions.push(`Your weakest reasoning skill is ${top.name.toLowerCase()} at ${top.percent}%. That is a technique problem, not a content gap, so re-reading units will not move it.`);
  }

  if (report.recommendations.length) {
    actions.push("Work through the units listed below in order. They are ranked by how many marks each cost you, not by percentage.");
  }

  if (!report.complete) {
    return {
      band: "Partial form",
      headline: "This form is not finished, so there is no total score to act on.",
      actions: [
        `Only ${scoredSections.map(section => section.nickname).join(", ") || "part of the exam"} carried questions, so treat what follows as section practice rather than as a full-length result.`,
        ...urgent,
        ...actions.slice(0, 3),
      ],
    };
  }

  if (report.total >= 515) {
    return {
      band: "515+",
      headline: "You are in range for almost every school. The work now is protecting this, not raising it.",
      actions: [
        ...urgent,
        "Sit the remaining full-lengths under real conditions, at the hour your exam starts. At this level stamina and consistency decide the score, not content.",
        ...actions.slice(0, 2),
        "Resist a content rebuild. At this score the marks lost are nearly all single careless errors, and the fix is a slower read of the stem.",
      ],
    };
  }

  if (report.total >= 505) {
    return {
      band: "505-514",
      headline: "A competitive score, with a clear path to a stronger one.",
      actions: [
        ...urgent,
        ...actions,
        "Review every question you got right but were unsure of. At this band those are the marks that swing a form.",
      ],
    };
  }

  if (report.total >= 495) {
    return {
      band: "495-504",
      headline: "Around the middle of the distribution, where a handful of raw marks moves the score a long way.",
      actions: [
        ...urgent,
        ...actions,
        "The percentile curve is steepest here: two or three extra correct answers per section is worth several scaled points. Pick the two weakest units and finish them properly before moving on.",
      ],
    };
  }

  return {
    band: "Below 495",
    headline: "Content first. The gaps here are wide enough that technique work would not stick yet.",
    actions: [
      ...urgent,
      "Go back to the lessons for your weakest units and work them end to end, rather than drilling questions. Questions diagnose; they do not teach.",
      ...actions.filter(action => !action.startsWith("Work through the units")),
      "Give yourself enough weeks. A score in this band usually reflects material not yet learned, and that is a matter of time rather than of strategy.",
    ],
  };
}
