import { randomUUID } from "node:crypto";
import { SECTIONS } from "./blueprint";
import type { Attempt, AnswerMap, TimingMap } from "./types";
import type { Database } from "../portal-store";

/**
 * Attempts live in Postgres, not the browser.
 *
 * A full-length is seven and a half hours. People close laptops, lose wifi and
 * come back on another machine, and a score they paid for cannot depend on
 * localStorage surviving that. The clock is also held server-side: a timer kept
 * only in the page is a timer a student can edit, which would make every score
 * on the site worthless.
 */
export const examSchema = [
  `CREATE TABLE IF NOT EXISTS vitalis_exam_attempts (
    id UUID PRIMARY KEY,
    email TEXT NOT NULL,
    exam_id TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    section_index INTEGER NOT NULL DEFAULT 0,
    /* When the current section's clock runs out, held server-side. */
    section_deadline TIMESTAMPTZ,
    break_ends_at TIMESTAMPTZ,
    answers JSONB NOT NULL DEFAULT '{}'::jsonb,
    flagged JSONB NOT NULL DEFAULT '[]'::jsonb,
    timing JSONB NOT NULL DEFAULT '{}'::jsonb,
    section_states JSONB NOT NULL DEFAULT '[]'::jsonb
  )`,
  `CREATE INDEX IF NOT EXISTS vitalis_exam_attempts_email ON vitalis_exam_attempts(email, started_at DESC)`,
  /* One unfinished attempt per exam per student: starting a second one while
     the first is live would let someone preview a section, abandon, and retake
     it with the questions already seen. */
  `CREATE UNIQUE INDEX IF NOT EXISTS vitalis_exam_attempts_live
     ON vitalis_exam_attempts(email, exam_id) WHERE finished_at IS NULL`,
];

type Row = Record<string, unknown>;

function asAnswers(value: unknown): AnswerMap {
  const out: AnswerMap = {};
  if (value && typeof value === "object" && !Array.isArray(value)) {
    for (const [key, choice] of Object.entries(value as Record<string, unknown>)) {
      if (choice === "A" || choice === "B" || choice === "C" || choice === "D") out[key] = choice;
    }
  }
  return out;
}

function asTiming(value: unknown): TimingMap {
  const out: TimingMap = {};
  if (value && typeof value === "object" && !Array.isArray(value)) {
    for (const [key, seconds] of Object.entries(value as Record<string, unknown>)) {
      const number = Number(seconds);
      if (Number.isFinite(number) && number >= 0) out[key] = Math.round(number);
    }
  }
  return out;
}

function iso(value: unknown): string | null {
  if (!value) return null;
  const date = value instanceof Date ? value : new Date(String(value));
  return Number.isNaN(date.getTime()) ? null : date.toISOString();
}

function toAttempt(row: Row): Attempt {
  const index = Number(row.section_index) || 0;
  const deadline = iso(row.section_deadline);
  return {
    id: String(row.id),
    examId: String(row.exam_id),
    email: String(row.email),
    startedAt: iso(row.started_at) ?? new Date().toISOString(),
    finishedAt: iso(row.finished_at),
    sectionIndex: index,
    secondsRemaining: deadline ? Math.max(0, Math.round((new Date(deadline).getTime() - Date.now()) / 1000)) : 0,
    breakEndsAt: iso(row.break_ends_at),
    answers: asAnswers(row.answers),
    flagged: Array.isArray(row.flagged) ? (row.flagged as unknown[]).map(String) : [],
    timing: asTiming(row.timing),
    sectionStates: Array.isArray(row.section_states)
      ? (row.section_states as Row[]).map(state => ({
          id: String(state.id) as Attempt["sectionStates"][number]["id"],
          secondsRemaining: Number(state.secondsRemaining) || 0,
          submittedAt: iso(state.submittedAt),
        }))
      : [],
  };
}

export async function liveAttempt(db: Database, email: string, examId: string): Promise<Attempt | null> {
  const result = await db.query(
    "SELECT * FROM vitalis_exam_attempts WHERE email = $1 AND exam_id = $2 AND finished_at IS NULL",
    [email.toLowerCase(), examId],
  );
  return result.rows[0] ? toAttempt(result.rows[0]) : null;
}

export async function attemptById(db: Database, email: string, id: string): Promise<Attempt | null> {
  const result = await db.query("SELECT * FROM vitalis_exam_attempts WHERE id = $1 AND email = $2", [id, email.toLowerCase()]);
  return result.rows[0] ? toAttempt(result.rows[0]) : null;
}

export async function finishedAttempts(db: Database, email: string) {
  const result = await db.query(
    `SELECT id, exam_id, started_at, finished_at, answers, timing, section_states, section_index
       FROM vitalis_exam_attempts WHERE email = $1 AND finished_at IS NOT NULL ORDER BY finished_at DESC`,
    [email.toLowerCase()],
  );
  return result.rows.map(toAttempt);
}

/** Starts an attempt, or hands back the one already running. */
export async function startAttempt(db: Database, email: string, examId: string): Promise<Attempt> {
  const existing = await liveAttempt(db, email, examId);
  if (existing) return existing;
  const first = SECTIONS[0];
  const result = await db.query(
    `INSERT INTO vitalis_exam_attempts (id, email, exam_id, section_index, section_deadline)
     VALUES ($1, $2, $3, 0, NOW() + make_interval(mins => $4::int))
     ON CONFLICT DO NOTHING
     RETURNING *`,
    [randomUUID(), email.toLowerCase(), examId, first.minutes],
  );
  if (result.rows[0]) return toAttempt(result.rows[0]);
  // Lost the race against another tab; the other one is the live attempt.
  const raced = await liveAttempt(db, email, examId);
  if (!raced) throw new Error("Could not start the exam. Try again.");
  return raced;
}

/**
 * Saves answers mid-section. Writes are merged rather than replaced so a stale
 * tab cannot wipe answers a newer one has saved, and the clock is never taken
 * from the client.
 */
export async function saveProgress(
  db: Database,
  email: string,
  attemptId: string,
  input: { answers?: AnswerMap; flagged?: string[]; timing?: TimingMap },
): Promise<Attempt | null> {
  const result = await db.query(
    `UPDATE vitalis_exam_attempts
        SET answers = answers || $3::jsonb,
            timing = timing || $4::jsonb,
            flagged = COALESCE($5::jsonb, flagged)
      WHERE id = $1 AND email = $2 AND finished_at IS NULL
      RETURNING *`,
    [
      attemptId,
      email.toLowerCase(),
      JSON.stringify(input.answers ?? {}),
      JSON.stringify(input.timing ?? {}),
      input.flagged ? JSON.stringify(input.flagged) : null,
    ],
  );
  return result.rows[0] ? toAttempt(result.rows[0]) : null;
}

/**
 * Hands in the current section and moves on: either into the break that
 * follows it, or straight to the next section when the student skips the
 * break, or to the end of the exam.
 */
export async function submitSection(db: Database, email: string, attemptId: string, takeBreak: boolean): Promise<Attempt | null> {
  const attempt = await attemptById(db, email, attemptId);
  if (!attempt || attempt.finishedAt) return null;

  const current = SECTIONS[attempt.sectionIndex];
  if (!current) return null;
  const next = SECTIONS[attempt.sectionIndex + 1];

  const states = [
    ...attempt.sectionStates.filter(state => state.id !== current.id),
    { id: current.id, secondsRemaining: attempt.secondsRemaining, submittedAt: new Date().toISOString() },
  ];

  if (!next) {
    const done = await db.query(
      `UPDATE vitalis_exam_attempts
          SET finished_at = NOW(), section_index = $3, section_deadline = NULL,
              break_ends_at = NULL, section_states = $4::jsonb
        WHERE id = $1 AND email = $2 AND finished_at IS NULL
        RETURNING *`,
      [attemptId, email.toLowerCase(), SECTIONS.length, JSON.stringify(states)],
    );
    return done.rows[0] ? toAttempt(done.rows[0]) : null;
  }

  // A break the student declines is forfeited, exactly as on the real exam.
  const breakMinutes = takeBreak ? current.breakAfterMinutes ?? 0 : 0;
  const result = await db.query(
    `UPDATE vitalis_exam_attempts
        SET section_index = $3,
            section_states = $4::jsonb,
            break_ends_at = CASE WHEN $5::int > 0 THEN NOW() + make_interval(mins => $5::int) ELSE NULL END,
            section_deadline = NOW() + make_interval(mins => $6::int)
      WHERE id = $1 AND email = $2 AND finished_at IS NULL
      RETURNING *`,
    [attemptId, email.toLowerCase(), attempt.sectionIndex + 1, JSON.stringify(states), breakMinutes, breakMinutes + next.minutes],
  );
  return result.rows[0] ? toAttempt(result.rows[0]) : null;
}

/** Ends the break early and starts the next section's clock now. */
export async function endBreak(db: Database, email: string, attemptId: string): Promise<Attempt | null> {
  const attempt = await attemptById(db, email, attemptId);
  if (!attempt || attempt.finishedAt || !attempt.breakEndsAt) return null;
  const section = SECTIONS[attempt.sectionIndex];
  if (!section) return null;
  const result = await db.query(
    `UPDATE vitalis_exam_attempts
        SET break_ends_at = NULL, section_deadline = NOW() + make_interval(mins => $3::int)
      WHERE id = $1 AND email = $2 AND finished_at IS NULL
      RETURNING *`,
    [attemptId, email.toLowerCase(), section.minutes],
  );
  return result.rows[0] ? toAttempt(result.rows[0]) : null;
}

/** Abandons a live attempt, so a student can restart the form from scratch. */
export async function abandonAttempt(db: Database, email: string, attemptId: string) {
  await db.query("DELETE FROM vitalis_exam_attempts WHERE id = $1 AND email = $2 AND finished_at IS NULL", [attemptId, email.toLowerCase()]);
}
