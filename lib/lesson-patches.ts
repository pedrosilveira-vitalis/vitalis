import { createHash } from "node:crypto";
import { patchReviews } from "./lesson-reviews";

// Patch-based lesson reviews (lessons 65+). Instead of replacing a whole field,
// each patch swaps one exact passage. The review is all-or-nothing: if any
// guarded field changed, or any "old" passage is missing or ambiguous, the
// original lesson is shown unchanged.

type Row = { id: number; [key: string]: unknown };

export type PatchReview = {
  lessonId: number;
  reviewedAt: string;
  questionIds: number[];
  /** sha256 of title, content and every quiz field, joined with "\u0000" (see fingerprint()). */
  fingerprint: string;
  patches: { field: string; old: string; new: string; reason?: string }[];
  sources: { title: string; url: string }[];
  visual: {
    title: string;
    src: string;
    width: number;
    height: number;
    alt: string;
    caption: string;
    beforeHeading?: string;
  };
};

function locate(field: string, lesson: Row, questions: Row[]): [Row | undefined, string] {
  const parts = field.split(".");
  if (parts[0] === "lesson") return [lesson, parts[1]];
  if (parts[0] === "questions") return [questions.find(q => q.id === Number(parts[1])), parts[2]];
  return [undefined, ""];
}

const QUESTION_KEYS = ["question_text", "choice_a", "choice_b", "choice_c", "choice_d", "correct_answer", "explanation"];

export function fingerprint(lesson: Row, questions: Row[], questionIds: number[]) {
  const parts: unknown[] = [lesson.title, lesson.content];
  for (const id of questionIds) {
    const q = questions.find(x => x.id === id);
    for (const key of QUESTION_KEYS) parts.push(q?.[key]);
  }
  if (parts.some(p => typeof p !== "string")) return null;
  return createHash("sha256").update(parts.join("\u0000")).digest("hex");
}

export function applyPatchReview<L extends Row, Q extends Row>(review: PatchReview, lesson: L, questions: Q[]) {
  const unchanged = { lesson, questions, review: null };
  const ids = new Set(questions.map(q => q.id));
  if (questions.length !== review.questionIds.length || ids.size !== questions.length ||
      review.questionIds.some(id => !ids.has(id))) {
    console.warn("Lesson review skipped: question set changed", lesson.id);
    return unchanged;
  }
  if (fingerprint(lesson, questions, review.questionIds) !== review.fingerprint) {
    console.warn("Lesson review skipped: source changed", lesson.id);
    return unchanged;
  }
  const updatedLesson: Row = { ...lesson };
  const updatedQuestions: Row[] = questions.map(q => ({ ...q }));
  for (const patch of review.patches) {
    const [target, key] = locate(patch.field, updatedLesson, updatedQuestions);
    const value = target?.[key];
    if (typeof value !== "string") return unchanged;
    const first = value.indexOf(patch.old);
    if (first === -1 || value.indexOf(patch.old, first + 1) !== -1) {
      console.warn("Lesson review skipped: patch text not unique", lesson.id, patch.field);
      return unchanged;
    }
    target![key] = value.slice(0, first) + patch.new + value.slice(first + patch.old.length);
  }
  return {
    lesson: updatedLesson as L,
    questions: updatedQuestions as Q[],
    review: { reviewedAt: review.reviewedAt, sources: review.sources, visual: review.visual },
  };
}

export function findPatchReview(lessonId: number) {
  return patchReviews.find(r => r.lessonId === lessonId);
}
