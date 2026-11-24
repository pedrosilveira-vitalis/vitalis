import { SECTIONS, type ExamSectionId } from "./blueprint";
import type { ExamQuestion, ExamSection, FullLengthExam } from "./types";

/**
 * The exam catalogue, and the two views of it.
 *
 * Content is held as JSON per section and loaded only for the section being
 * served, so a 230-question form never has to be parsed whole to answer one
 * request. The important part of this file is the split between the two views:
 *
 *   publicSection()  — what the browser is allowed to see mid-exam
 *   loadSection()    — the full thing, server-side only
 *
 * The answer key, the explanation and the wrong-answer notes never leave the
 * server while an exam is running. A student with the dev tools open can read
 * anything the page was sent, so sending the key and hiding it in the UI would
 * be the same as printing it on the screen.
 */

export interface ExamSummary {
  id: string;
  name: string;
  number: number;
  blurb: string;
  /** False until every section's content is written and reviewed. */
  ready: boolean;
  /**
   * One form is free to anyone with an account. A full-length is the only
   * honest way to find out whether a course is worth buying, and a student who
   * has sat ours and seen the report is a far warmer prospect than one who has
   * read a sales page.
   */
  free: boolean;
}

export const EXAMS: ExamSummary[] = [
  {
    id: "fl1",
    name: "Vitalis Full-Length 1",
    number: 1,
    blurb:
      "A first full-length, weighted the way the real exam is: experimental data in the science sections, and nine CARS passages drawn from the humanities and social sciences. Free with any account.",
    ready: true,
    free: true,
  },
  {
    id: "fl2",
    name: "Vitalis Full-Length 2",
    number: 2,
    blurb:
      "A second form at the same difficulty, with no repeated passages or concepts, so a second sitting measures progress rather than memory. Included with Core and Complete.",
    ready: true,
    free: false,
  },
  {
    id: "fl3",
    name: "Vitalis Full-Length 3",
    number: 3,
    blurb:
      "Written to sit mid-course, when content review is mostly done and the question is whether it holds up under seven hours of pressure. Part of Complete.",
    ready: true,
    free: false,
  },
  {
    id: "fl4",
    name: "Vitalis Full-Length 4",
    number: 4,
    blurb:
      "A late form, weighted toward the reasoning and data-interpretation questions that separate a good score from a great one. Part of Complete.",
    ready: false,
    free: false,
  },
  {
    id: "fl5",
    name: "Vitalis Full-Length 5",
    number: 5,
    blurb:
      "The last form before test day, meant to be sat two weeks out at the hour your real exam starts. Part of Complete.",
    ready: false,
    free: false,
  },
];

/**
 * Whether this student may open a given form.
 *
 * Access is tiered by how far up the list a plan reaches: an account opens
 * Full-Length 1, Core opens the first two, Complete opens all five.
 */
export function canTake(examId: string, allowance: number): boolean {
  const exam = examSummary(examId);
  if (!exam) return false;
  return exam.number <= allowance;
}

export function examSummary(id: string): ExamSummary | undefined {
  return EXAMS.find(exam => exam.id === id);
}

type SectionFile = { passages: ExamSection["passages"]; questions: ExamQuestion[] };

/**
 * Written content, one entry per finished section.
 *
 * The specifiers are literals rather than a template so the bundler can
 * resolve and split them; a section that is not listed here has not been
 * written yet, which is a normal state while a form is in progress rather
 * than an error.
 */
const CONTENT: Record<string, () => Promise<SectionFile>> = {
  "fl1/chem-phys": () => import("./content/fl1/chem-phys.json").then(file => file.default as unknown as SectionFile),
  "fl1/cars": () => import("./content/fl1/cars.json").then(file => file.default as unknown as SectionFile),
  "fl1/bio-biochem": () => import("./content/fl1/bio-biochem.json").then(file => file.default as unknown as SectionFile),
  "fl1/psych-soc": () => import("./content/fl1/psych-soc.json").then(file => file.default as unknown as SectionFile),
  "fl2/chem-phys": () => import("./content/fl2/chem-phys.json").then(file => file.default as unknown as SectionFile),
  "fl2/cars": () => import("./content/fl2/cars.json").then(file => file.default as unknown as SectionFile),
  "fl2/bio-biochem": () => import("./content/fl2/bio-biochem.json").then(file => file.default as unknown as SectionFile),
  "fl2/psych-soc": () => import("./content/fl2/psych-soc.json").then(file => file.default as unknown as SectionFile),
  "fl3/chem-phys": () => import("./content/fl3/chem-phys.json").then(file => file.default as unknown as SectionFile),
  "fl3/cars": () => import("./content/fl3/cars.json").then(file => file.default as unknown as SectionFile),
  "fl3/bio-biochem": () => import("./content/fl3/bio-biochem.json").then(file => file.default as unknown as SectionFile),
  "fl3/psych-soc": () => import("./content/fl3/psych-soc.json").then(file => file.default as unknown as SectionFile),
};

async function sectionFile(examId: string, sectionId: ExamSectionId): Promise<SectionFile | null> {
  const load = CONTENT[`${examId}/${sectionId}`];
  if (!load) return null;
  try {
    const data = await load();
    if (!Array.isArray(data?.questions) || !data.questions.length) return null;
    return data;
  } catch {
    return null;
  }
}

export async function loadSection(examId: string, sectionId: ExamSectionId): Promise<ExamSection | null> {
  const data = await sectionFile(examId, sectionId);
  return data ? { id: sectionId, passages: data.passages ?? [], questions: data.questions } : null;
}

export async function loadExam(examId: string): Promise<FullLengthExam | null> {
  const summary = examSummary(examId);
  if (!summary) return null;
  const sections: ExamSection[] = [];
  for (const blueprint of SECTIONS) {
    const section = await loadSection(examId, blueprint.id);
    if (!section) return null;
    sections.push(section);
  }
  return { id: summary.id, name: summary.name, number: summary.number, blurb: summary.blurb, sections };
}

/** How complete each section is, for the catalogue page and for admin. */
export async function examProgress(examId: string) {
  const rows = [];
  for (const blueprint of SECTIONS) {
    const section = await loadSection(examId, blueprint.id);
    rows.push({
      id: blueprint.id,
      short: blueprint.short,
      written: section?.questions.length ?? 0,
      needed: blueprint.questions,
    });
  }
  return rows;
}

/** True only when all four sections are written to their full question count. */
export async function examIsReady(examId: string): Promise<boolean> {
  const rows = await examProgress(examId);
  return rows.every(row => row.written >= row.needed);
}

/* ------------------------------------------------------------------ *
 * The two views
 * ------------------------------------------------------------------ */

export interface PublicQuestion {
  id: string;
  passageId: string | null;
  stem: string;
  choices: { A: string; B: string; C: string; D: string };
}

export interface PublicSection {
  id: ExamSectionId;
  passages: ExamSection["passages"];
  questions: PublicQuestion[];
}

/** Strips the key, the explanation and the wrong-answer notes. */
export function publicSection(section: ExamSection): PublicSection {
  return {
    id: section.id,
    passages: section.passages.map(passage => ({
      id: passage.id,
      title: passage.title,
      paragraphs: passage.paragraphs,
      ...(passage.figure ? { figure: passage.figure } : {}),
    })),
    questions: section.questions.map(question => ({
      id: question.id,
      passageId: question.passageId,
      stem: question.stem,
      choices: question.choices,
    })),
  };
}
