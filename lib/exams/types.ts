import type { ExamSectionId, SkillId } from "./blueprint";

/**
 * A full-length exam, stored in the repository rather than the database.
 *
 * Exam content is the most expensive thing on the site to get wrong and the
 * thing we are most often asked to correct, so it lives in version control
 * where a change is reviewable and a mistake is traceable to a commit. The
 * database holds attempts, not questions.
 */

export interface ExamPassage {
  id: string;
  /** Shown above the passage, as the real exam does for science passages. */
  title: string;
  /** Paragraphs. Rendered in order with a blank line between. */
  paragraphs: string[];
  /** Optional figure or table, as a self-contained SVG or an HTML table. */
  figure?: { kind: "svg" | "table"; caption: string; markup: string };
  /** Where the passage's factual content came from, so claims are checkable. */
  sources?: { label: string; url: string }[];
}

export interface ExamQuestion {
  id: string;
  /** Null for a discrete (standalone) question. */
  passageId: string | null;
  stem: string;
  choices: { A: string; B: string; C: string; D: string };
  correct: "A" | "B" | "C" | "D";
  /** Why the key is right. Written to stand on its own. */
  explanation: string;
  /** Why each wrong choice is wrong — the part students actually need. */
  wrong: Partial<Record<"A" | "B" | "C" | "D", string>>;
  /** AAMC content category code, e.g. "1D". Empty for CARS. */
  category: string;
  skill: SkillId;
  difficulty: "easy" | "medium" | "hard";
  /**
   * The unit slug this question maps to, so a miss can point at the lesson and
   * the cheat sheet to read. Null only for CARS, which has no content unit.
   */
  unit: string | null;
}

export interface ExamSection {
  id: ExamSectionId;
  passages: ExamPassage[];
  questions: ExamQuestion[];
}

export interface FullLengthExam {
  id: string;
  /** "Vitalis Full-Length 1" */
  name: string;
  number: number;
  /** One line on what this form emphasises, shown before they start. */
  blurb: string;
  sections: ExamSection[];
}

/** A student's answers so far, keyed by question id. */
export type AnswerMap = Record<string, "A" | "B" | "C" | "D">;

/** Seconds spent per question id, for the pacing part of the report. */
export type TimingMap = Record<string, number>;

export interface AttemptSectionState {
  id: ExamSectionId;
  /** Seconds left when the section was handed in. */
  secondsRemaining: number;
  submittedAt: string | null;
}

export interface Attempt {
  id: string;
  examId: string;
  email: string;
  startedAt: string;
  finishedAt: string | null;
  /** Index into the exam's sections; equals sections.length once finished. */
  sectionIndex: number;
  /** Seconds left in the section being worked on right now. */
  secondsRemaining: number;
  /** Set while the student is on a break, so the break timer survives a reload. */
  breakEndsAt: string | null;
  answers: AnswerMap;
  flagged: string[];
  timing: TimingMap;
  sectionStates: AttemptSectionState[];
}
