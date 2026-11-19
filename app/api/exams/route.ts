import { auth } from "@/auth";
import { capabilitiesFor } from "@/lib/billing";
import { portalDb } from "@/lib/portal-db";
import { SECTIONS } from "@/lib/exams/blueprint";
import { EXAMS, canTake, examProgress, loadExam } from "@/lib/exams/registry";
import { finishedAttempts, liveAttempt } from "@/lib/exams/store";
import { buildReport } from "@/lib/exams/score";

const NO_STORE = { headers: { "Cache-Control": "no-store" } };

/** The exam catalogue, with this student's history against each form. */
export async function GET() {
  const session = await auth();
  const email = session?.user?.email ?? null;

  const catalogue = [];
  for (const exam of EXAMS) {
    const progress = await examProgress(exam.id);
    const written = progress.reduce((sum, row) => sum + row.written, 0);
    const needed = progress.reduce((sum, row) => sum + row.needed, 0);
    catalogue.push({ ...exam, ready: written >= needed, written, needed, progress, allowed: exam.free });
  }

  if (!email) return Response.json({ signedIn: false, allowed: false, exams: catalogue, attempts: [] }, NO_STORE);

  let allowed = false;
  let attempts: unknown[] = [];
  try {
    const db = await portalDb();
    allowed = (await capabilitiesFor(db, email)).fullLengths;
    for (const entry of catalogue) entry.allowed = canTake(entry.id, allowed);
    {
      const live = [];
      for (const exam of EXAMS) {
        const running = await liveAttempt(db, email, exam.id);
        if (running) live.push({ examId: exam.id, attemptId: running.id, startedAt: running.startedAt, sectionIndex: running.sectionIndex });
      }
      const done = await finishedAttempts(db, email);
      const scored = [];
      for (const attempt of done) {
        const exam = await loadExam(attempt.examId);
        if (!exam) continue;
        const report = buildReport(exam, attempt);
        scored.push({
          attemptId: attempt.id,
          examId: attempt.examId,
          finishedAt: attempt.finishedAt,
          total: report.total,
          low: report.totalLow,
          high: report.totalHigh,
          sections: report.sections.map(section => ({ short: section.short, scaled: section.scaled })),
        });
      }
      attempts = [...live.map(item => ({ ...item, status: "live" })), ...scored.map(item => ({ ...item, status: "scored" }))];
    }
  } catch {
    // The catalogue is still worth showing if the database blinks.
  }

  return Response.json({ signedIn: true, allowed, exams: catalogue, attempts, sections: SECTIONS }, NO_STORE);
}
