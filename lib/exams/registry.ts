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
}

export const EXAMS: ExamSummary[] = [
  {
    id: "fl1",
    name: "Vitalis Full-Length 1",
    number: 1,
    blurb:
      "A first full-length, weighted the way the real exam is: experimental data in the science sections, and nine CARS passages drawn from the humanities and social sciences.",
    ready: false,
  },
  {
    id: "fl2",
    name: "Vitalis Full-Length 2",
    number: 2,
    blurb:
      "A second form at the same difficulty, with no repeated passages or concepts, so a second sitting measures progress rather than memory.",
    ready: false,
  },
];

export function examSummary(id: string): ExamSummary | undefined {
  return EXAMS.find(exam => exam.id === id);
}

type SectionFile = { passages: ExamSection["passages"]; questions: ExamQuestion[] };

/**
 * Content files are added one section at a time as they are written, so a
 * missing file is an expected state rather than an error: the exam simply is
 * not ready yet.
 */
async function sectionFile(examId: string, sectionId: ExamSectionId): Promise<SectionFile | null> {
  try {
    const loaded = await import(`./content/${examId}/${sectionId}.json`);
    const data = (loaded.default ?? loaded) as SectionFile;
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
