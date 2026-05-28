import { auth } from "@/auth";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.POSTGRES_URL,
  ssl: { rejectUnauthorized: false },
});

async function getUserId(email: string): Promise<number | null> {
  const res = await pool.query("SELECT id FROM users WHERE email = $1", [email]);
  return res.rows.length > 0 ? res.rows[0].id : null;
}

export async function GET() {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in", plan: null }, { status: 401 });
  }

  const userId = await getUserId(session.user.email);
  if (!userId) {
    return Response.json({ error: "User not found", plan: null }, { status: 404 });
  }

  try {
    const planRes = await pool.query(
      `SELECT p.id, p.weeks_count, p.plan_data, p.completed_items, p.created_at, p.updated_at,
              s.bio_score, s.chem_score, s.psych_score, s.cars_score, s.total_score,
              s.topic_ratings, s.test_date, s.weeks_until_test, s.created_at AS submission_created_at
       FROM study_plans p
       JOIN score_submissions s ON s.id = p."submissionId"
       WHERE p."userId" = $1 AND p.is_current = TRUE
       ORDER BY p.created_at DESC
       LIMIT 1`,
      [userId]
    );

    if (planRes.rows.length === 0) {
      return Response.json({ plan: null });
    }

    const row = planRes.rows[0];

    // Get all unit-to-first-lesson mappings so frontend can link directly to lessons
    const unitLessonRes = await pool.query(
      `SELECT DISTINCT ON ("unitId") "unitId", id AS lesson_id, lesson_number
       FROM study_lessons
       ORDER BY "unitId", lesson_number ASC`
    );
    const unitToFirstLesson: Record<number, number> = {};
    for (const r of unitLessonRes.rows) {
      unitToFirstLesson[r.unitId] = r.lesson_id;
    }

    return Response.json({
      plan: {
        id: row.id,
        weeksCount: row.weeks_count,
        planData: row.plan_data,
        completedItems: row.completed_items || [],
        createdAt: row.created_at,
        updatedAt: row.updated_at,
        unitToFirstLesson,
        submission: {
          bio: row.bio_score,
          chem: row.chem_score,
          psych: row.psych_score,
          cars: row.cars_score,
          total: row.total_score,
          topicRatings: row.topic_ratings,
          testDate: row.test_date,
          weeksUntilTest: row.weeks_until_test,
          submittedAt: row.submission_created_at,
        },
      },
    });
  } catch (error) {
    console.error("Get plan error:", error);
    return Response.json({ error: "Failed to load plan", plan: null }, { status: 500 });
  }
}