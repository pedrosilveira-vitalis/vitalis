import { auth } from "@/auth";
import { capabilitiesFor } from "@/lib/billing";
import { portalDb } from "@/lib/portal-db";
import { SECTIONS } from "@/lib/exams/blueprint";
import { canTake, examSummary, loadSection, publicSection } from "@/lib/exams/registry";
import { abandonAttempt, attemptById, endBreak, liveAttempt, saveProgress, startAttempt, submitSection } from "@/lib/exams/store";
import type { AnswerMap, Attempt, TimingMap } from "@/lib/exams/types";

const NO_STORE = { headers: { "Cache-Control": "no-store" } };
const LETTERS = new Set(["A", "B", "C", "D"]);

/**
 * The exam runner's only server contact.
 *
 * Two rules hold throughout. The answer key never goes out while an exam is
 * running — the browser is sent `publicSection`, which has no keys and no
 * explanations. And the clock is read from the server on every call, never
 * taken from the client, so a student cannot buy themselves time by editing a
 * timer in the page.
 */

async function student(examId: string) {
  const session = await auth();
  const email = session?.user?.email;
  if (!email) return { error: Response.json({ error: "Sign in to take a full-length." }, { status: 401 }) };
  const db = await portalDb();
  const allowance = (await capabilitiesFor(db, email)).fullLengths;
  if (!canTake(examId, allowance)) {
    return { error: Response.json({ error: "That form is not part of your plan yet." }, { status: 403 }) };
  }
  return { email, db };
}

/** The attempt plus only the content the student is allowed to hold right now. */
async function view(attempt: Attempt) {
  const blueprint = SECTIONS[attempt.sectionIndex];
  const onBreak = Boolean(attempt.breakEndsAt && new Date(attempt.breakEndsAt).getTime() > Date.now());
  const breakSecondsRemaining = attempt.breakEndsAt
    ? Math.max(0, Math.round((new Date(attempt.breakEndsAt).getTime() - Date.now()) / 1000))
    : 0;

  // While a break is running the next section's questions are withheld: the
  // break is not reading time.
  const section = blueprint && !onBreak ? await loadSection(attempt.examId, blueprint.id) : null;

  return {
    attempt: {
      id: attempt.id,
      examId: attempt.examId,
      startedAt: attempt.startedAt,
      finishedAt: attempt.finishedAt,
      sectionIndex: attempt.sectionIndex,
      secondsRemaining: attempt.secondsRemaining,
      answers: attempt.answers,
      flagged: attempt.flagged,
    },
    onBreak,
    breakSecondsRemaining,
    section: blueprint
      ? {
          id: blueprint.id,
          name: blueprint.name,
          short: blueprint.short,
          nickname: blueprint.nickname,
          minutes: blueprint.minutes,
          questions: blueprint.questions,
          breakAfterMinutes: blueprint.breakAfterMinutes,
          breakLabel: blueprint.breakLabel,
          index: attempt.sectionIndex,
          count: SECTIONS.length,
          /* A periodic table is on screen for Chem/Phys on the real exam. */
          periodicTable: blueprint.id === "chem-phys",
        }
      : null,
    content: section ? publicSection(section) : null,
  };
}

export async function GET(request: Request) {
  const examId = new URL(request.url).searchParams.get("exam") ?? "";
  if (!examSummary(examId)) return Response.json({ error: "Unknown exam." }, { status: 404 });
  const who = await student(examId);
  if ("error" in who) return who.error;
  const attempt = await liveAttempt(who.db, who.email, examId);
  if (!attempt) return Response.json({ attempt: null }, NO_STORE);
  return Response.json(await view(attempt), NO_STORE);
}

function cleanAnswers(value: unknown): AnswerMap {
  const out: AnswerMap = {};
  if (value && typeof value === "object" && !Array.isArray(value)) {
    for (const [id, choice] of Object.entries(value as Record<string, unknown>)) {
      if (typeof id === "string" && id.length <= 64 && typeof choice === "string" && LETTERS.has(choice)) {
        out[id] = choice as "A" | "B" | "C" | "D";
      }
    }
  }
  return out;
}

function cleanTiming(value: unknown): TimingMap {
  const out: TimingMap = {};
  if (value && typeof value === "object" && !Array.isArray(value)) {
    for (const [id, seconds] of Object.entries(value as Record<string, unknown>)) {
      const number = Number(seconds);
      // Capped: a tab left open overnight must not report a four-hour question.
      if (typeof id === "string" && id.length <= 64 && Number.isFinite(number) && number >= 0) {
        out[id] = Math.min(Math.round(number), 7200);
      }
    }
  }
  return out;
}

export async function POST(request: Request) {
  let body: Record<string, unknown>;
  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "Bad request." }, { status: 400 });
  }

  const action = String(body.action ?? "");
  const examId = String(body.exam ?? "");
  if (!examSummary(examId)) return Response.json({ error: "Unknown exam." }, { status: 404 });

  const who = await student(examId);
  if ("error" in who) return who.error;

  if (action === "start") {
    const attempt = await startAttempt(who.db, who.email, examId);
    return Response.json(await view(attempt), NO_STORE);
  }

  const attemptId = String(body.attempt ?? "");
  if (!/^[0-9a-f-]{36}$/i.test(attemptId)) return Response.json({ error: "Bad request." }, { status: 400 });

  const current = await attemptById(who.db, who.email, attemptId);
  if (!current) return Response.json({ error: "No such attempt." }, { status: 404 });
  if (current.finishedAt) return Response.json({ error: "That exam is already finished.", finished: true }, { status: 409 });

  if (action === "save") {
    const saved = await saveProgress(who.db, who.email, attemptId, {
      answers: cleanAnswers(body.answers),
      timing: cleanTiming(body.timing),
      flagged: Array.isArray(body.flagged) ? (body.flagged as unknown[]).map(String).slice(0, 300) : undefined,
    });
    if (!saved) return Response.json({ error: "Could not save." }, { status: 409 });
    // Only the clock goes back on a save; resending the content every few
    // seconds would be wasteful.
    return Response.json({ secondsRemaining: saved.secondsRemaining, sectionIndex: saved.sectionIndex }, NO_STORE);
  }

  if (action === "submit-section") {
    const next = await submitSection(who.db, who.email, attemptId, body.takeBreak !== false);
    if (!next) return Response.json({ error: "Could not hand in the section." }, { status: 409 });
    if (next.finishedAt) return Response.json({ finished: true, attemptId: next.id }, NO_STORE);
    return Response.json(await view(next), NO_STORE);
  }

  if (action === "end-break") {
    const next = await endBreak(who.db, who.email, attemptId);
    if (!next) return Response.json({ error: "No break is running." }, { status: 409 });
    return Response.json(await view(next), NO_STORE);
  }

  if (action === "abandon") {
    await abandonAttempt(who.db, who.email, attemptId);
    return Response.json({ abandoned: true }, NO_STORE);
  }

  return Response.json({ error: "Unknown action." }, { status: 400 });
}
