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

// GET /api/study/sections
// Returns all units across all sections, with each unit's lessons and any user progress
export async function GET() {
  try {
    const session = await auth();
    const userId = session?.user?.email ? await getUserId(session.user.email) : null;

    // Get all units
    const unitsRes = await pool.query(
      `SELECT id, section, unit_number, title, description
       FROM study_units
       ORDER BY section, unit_number`
    );

    // Get all lessons grouped by unit
    const lessonsRes = await pool.query(
      `SELECT id, "unitId", lesson_number, title, description, estimated_minutes
       FROM study_lessons
       ORDER BY "unitId", lesson_number`
    );

    // Get progress per lesson (only if user is logged in)
    let progressByLesson: Record<number, { read_complete: boolean; questions_correct: number; questions_total: number }> = {};
    if (userId) {
      const progRes = await pool.query(
        `SELECT "lessonId", read_complete, questions_correct, questions_total
         FROM study_progress
         WHERE "userId" = $1`,
        [userId]
      );
      progressByLesson = Object.fromEntries(
        progRes.rows.map((r) => [r.lessonId, r])
      );
    }

    // Group lessons by unit
    const lessonsByUnit: Record<number, typeof lessonsRes.rows> = {};
    for (const l of lessonsRes.rows) {
      if (!lessonsByUnit[l.unitId]) lessonsByUnit[l.unitId] = [];
      const progress = progressByLesson[l.id] || null;
      lessonsByUnit[l.unitId].push({ ...l, progress });
    }

    // Build the response: sections → units → lessons
    const sections: Record<string, typeof unitsRes.rows> = {};
    for (const u of unitsRes.rows) {
      if (!sections[u.section]) sections[u.section] = [];
      sections[u.section].push({
        ...u,
        lessons: lessonsByUnit[u.id] || [],
      });
    }

    return Response.json({ sections, isAuthenticated: !!userId });
  } catch (error) {
    console.error("GET study sections error:", error);
    return Response.json({ error: "Failed to load study content" }, { status: 500 });
  }
}