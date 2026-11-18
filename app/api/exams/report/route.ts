import { auth } from "@/auth";
import { capabilitiesFor } from "@/lib/billing";
import { portalDb } from "@/lib/portal-db";
import { loadExam } from "@/lib/exams/registry";
import { attemptById } from "@/lib/exams/store";
import { buildReport, verdictFor } from "@/lib/exams/score";
import { SECTIONS } from "@/lib/exams/blueprint";

const NO_STORE = { headers: { "Cache-Control": "no-store" } };

/**
 * The score report. This is the only route that returns answer keys and
 * explanations, and it returns them only for a finished attempt belonging to
 * the signed-in student — otherwise starting an attempt and reading its report
 * would be a way to download the key mid-exam.
 */
export async function GET(request: Request) {
  const session = await auth();
  const email = session?.user?.email;
  if (!email) return Response.json({ error: "Sign in to see your report." }, { status: 401 });

  const attemptId = new URL(request.url).searchParams.get("attempt") ?? "";
  if (!/^[0-9a-f-]{36}$/i.test(attemptId)) return Response.json({ error: "Bad request." }, { status: 400 });

  const db = await portalDb();
  if (!(await capabilitiesFor(db, email)).fullLengths) {
    return Response.json({ error: "Full-length exams are part of Complete." }, { status: 403 });
  }

  const attempt = await attemptById(db, email, attemptId);
  if (!attempt) return Response.json({ error: "No such attempt." }, { status: 404 });
  if (!attempt.finishedAt) return Response.json({ error: "That exam is still running.", running: true }, { status: 409 });

  const exam = await loadExam(attempt.examId);
  if (!exam) return Response.json({ error: "That exam's content is unavailable." }, { status: 404 });

  const report = buildReport(exam, attempt);

  // The missed questions carry their full explanation here, which is the whole
  // point of the review: a number without the reasoning teaches nothing.
  const detail = report.missed.map(miss => {
    const section = exam.sections.find(item => item.id === miss.section);
    const question = section?.questions.find(item => item.id === miss.id);
    const passage = question?.passageId ? section?.passages.find(item => item.id === question.passageId) : undefined;
    return {
      ...miss,
      choices: question?.choices ?? null,
      explanation: question?.explanation ?? "",
      whyWrong: miss.chosen ? question?.wrong[miss.chosen] ?? "" : "",
      passageTitle: passage?.title ?? null,
    };
  });

  return Response.json(
    {
      report: { ...report, missed: detail },
      verdict: verdictFor(report),
      sections: SECTIONS.map(section => ({ id: section.id, short: section.short, nickname: section.nickname, minutes: section.minutes })),
    },
    NO_STORE,
  );
}
