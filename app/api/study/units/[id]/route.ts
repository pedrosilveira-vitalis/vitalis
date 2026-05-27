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

// GET /api/study/units/:id
// Returns a single unit with its lessons + unit test info + user progress
export async function GET(
  request: Request,
  context: { params: Promise<{ id: string }> }
) {
  try {
    const params = await context.params;
    const unitId = parseInt(params.id, 10);
    if (isNaN(unitId)) {
      return Response.json({ error: "Invalid unit ID" }, { status: 400 });
    }

    const session = await auth();
    const userId = session?.user?.email ? await getUserId(session.user.email) : null;

    // Get unit details
    const unitRes = await pool.query(
      `SELECT id, section, unit_number, title, description
       FROM study_units WHERE id = $1`,
      [unitId]
    );
    if (unitRes.rows.length === 0) {
      return Response.json({ error: "Unit not found" }, { status: 404 });
    }

    // Get lessons in this unit
    const lessonsRes = await pool.query(
      `SELECT id, lesson_number, title, description, estimated_minutes
       FROM study_lessons
       WHERE "unitId" = $1
       ORDER BY lesson_number`,
      [unitId]
    );

    // Get count of unit test questions (don't return them yet — only loaded when starting the test)
    const testRes = await pool.query(
      `SELECT COUNT(*) AS question_count FROM study_unit_questions WHERE "unitId" = $1`,
      [unitId]
    );

    // Get user progress if signed in
    let progressByLesson: Record<number, { read_complete: boolean; questions_correct: number; questions_total: number }> = {};
    let unitTestResults: { score: number; total: number; taken_at: string }[] = [];
    if (userId) {
      const progRes = await pool.query(
        `SELECT p."lessonId", p.read_complete, p.questions_correct, p.questions_total
         FROM study_progress p
         JOIN study_lessons l ON l.id = p."lessonId"
         WHERE p."userId" = $1 AND l."unitId" = $2`,
        [userId, unitId]
      );
      progressByLesson = Object.fromEntries(
        progRes.rows.map((r) => [r.lessonId, r])
      );

      const resultsRes = await pool.query(
        `SELECT score, total, taken_at
         FROM study_unit_results
         WHERE "userId" = $1 AND "unitId" = $2
         ORDER BY taken_at DESC
         LIMIT 5`,
        [userId, unitId]
      );
      unitTestResults = resultsRes.rows;
    }

    const lessons = lessonsRes.rows.map((l) => ({
      ...l,
      progress: progressByLesson[l.id] || null,
    }));

    return Response.json({
      unit: unitRes.rows[0],
      lessons,
      unitTestQuestionCount: parseInt(testRes.rows[0].question_count, 10),
      unitTestResults,
      isAuthenticated: !!userId,
    });
  } catch (error) {
    console.error("GET unit error:", error);
    return Response.json({ error: "Failed to load unit" }, { status: 500 });
  }
}