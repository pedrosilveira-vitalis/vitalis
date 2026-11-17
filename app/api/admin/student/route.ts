import { auth } from "@/auth";
import { isAdmin } from "@/lib/engagement";
import { portalDb } from "@/lib/portal-db";

/** One student in detail: how they are doing, and what they keep missing. */
export async function GET(request: Request) {
  const viewer = (await auth())?.user?.email;
  if (!viewer) return Response.json({ error: "Sign in." }, { status: 401 });
  if (!isAdmin(viewer)) return Response.json({ error: "Administrator access required." }, { status: 403 });

  const email = (new URL(request.url).searchParams.get("email") || "").toLowerCase().trim();
  if (!email) return Response.json({ error: "Which student?" }, { status: 400 });

  try {
    const db = await portalDb();

    const study = await db.query(
      `SELECT COUNT(*) FILTER (WHERE p.read_complete)::int AS lessons_read,
              COALESCE(SUM(p.questions_correct), 0)::int AS correct,
              COALESCE(SUM(p.questions_total), 0)::int AS attempted,
              MAX(p.last_visited) AS last_seen
       FROM study_progress p JOIN users u ON u.id = p."userId"
       WHERE LOWER(u.email) = $1`,
      [email],
    );

    const missed = await db.query(
      `SELECT a.question_id, a.chosen, a.answered_at, a.lesson_id,
              q.question_text, q.correct_answer, l.title AS lesson_title
       FROM vitalis_answers a
       LEFT JOIN study_lesson_questions q ON q.id = a.question_id
       LEFT JOIN study_lessons l ON l.id = a.lesson_id
       WHERE a.email = $1 AND a.correct = FALSE
       ORDER BY a.answered_at DESC LIMIT 40`,
      [email],
    );

    const streak = await db.query(
      `SELECT COUNT(*)::int AS days_active FROM vitalis_days WHERE email = $1 AND answered`,
      [email],
    );

    const access = await db.query(
      `SELECT plan, amount_cents, window_days, expires_at, referral_code
       FROM vitalis_entitlements WHERE email = $1 ORDER BY expires_at DESC LIMIT 5`,
      [email],
    );

    const row = study.rows[0] ?? {};
    const attempted = Number(row.attempted ?? 0);
    const correct = Number(row.correct ?? 0);

    return Response.json(
      {
        email,
        lessonsRead: Number(row.lessons_read ?? 0),
        attempted,
        correct,
        accuracy: attempted ? Math.round((correct / attempted) * 100) : null,
        lastSeen: row.last_seen ?? null,
        daysActive: Number(streak.rows[0]?.days_active ?? 0),
        missed: missed.rows.map(item => ({
          questionId: item.question_id,
          lesson: item.lesson_title,
          lessonId: item.lesson_id,
          question: item.question_text,
          chose: item.chosen,
          answer: item.correct_answer,
          at: item.answered_at,
        })),
        purchases: access.rows.map(item => ({
          plan: item.plan,
          windowDays: item.window_days,
          amountCents: Number(item.amount_cents ?? 0),
          expiresAt: item.expires_at,
          referral: item.referral_code,
        })),
      },
      { headers: { "Cache-Control": "no-store" } },
    );
  } catch {
    return Response.json({ error: "Could not load this student." }, { status: 503 });
  }
}
