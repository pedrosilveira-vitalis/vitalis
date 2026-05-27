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

// GET /api/study/lessons/:id
// Returns the lesson content, its 5 questions, user's highlights, and user's progress
export async function GET(
  request: Request,
  context: { params: Promise<{ id: string }> }
) {
  try {
    const params = await context.params;
    const lessonId = parseInt(params.id, 10);
    if (isNaN(lessonId)) {
      return Response.json({ error: "Invalid lesson ID" }, { status: 400 });
    }

    const session = await auth();
    const userId = session?.user?.email ? await getUserId(session.user.email) : null;

    // Lesson details with unit info
    const lessonRes = await pool.query(
      `SELECT l.id, l.lesson_number, l.title, l.description, l.content, l.estimated_minutes,
              l."unitId", u.title AS unit_title, u.section, u.unit_number
       FROM study_lessons l
       JOIN study_units u ON u.id = l."unitId"
       WHERE l.id = $1`,
      [lessonId]
    );
    if (lessonRes.rows.length === 0) {
      return Response.json({ error: "Lesson not found" }, { status: 404 });
    }

    // Questions for this lesson
    const questionsRes = await pool.query(
      `SELECT id, question_number, question_text, choice_a, choice_b, choice_c, choice_d, correct_answer, explanation
       FROM study_lesson_questions
       WHERE "lessonId" = $1
       ORDER BY question_number`,
      [lessonId]
    );

    // Get neighboring lessons for prev/next nav
    const neighborsRes = await pool.query(
      `SELECT id, lesson_number, title
       FROM study_lessons
       WHERE "unitId" = $1
       ORDER BY lesson_number`,
      [lessonRes.rows[0].unitId]
    );
    const currentIndex = neighborsRes.rows.findIndex((l) => l.id === lessonId);
    const prevLesson = currentIndex > 0 ? neighborsRes.rows[currentIndex - 1] : null;
    const nextLesson = currentIndex < neighborsRes.rows.length - 1 ? neighborsRes.rows[currentIndex + 1] : null;

    let highlights: { id: number; highlighted_text: string; start_offset: number; end_offset: number; note: string | null }[] = [];
    let progress: { read_complete: boolean; questions_correct: number; questions_total: number } | null = null;

    if (userId) {
      const hlRes = await pool.query(
        `SELECT id, highlighted_text, start_offset, end_offset, note
         FROM study_highlights
         WHERE "userId" = $1 AND "lessonId" = $2
         ORDER BY start_offset`,
        [userId, lessonId]
      );
      highlights = hlRes.rows;

      const progRes = await pool.query(
        `SELECT read_complete, questions_correct, questions_total
         FROM study_progress
         WHERE "userId" = $1 AND "lessonId" = $2`,
        [userId, lessonId]
      );
      if (progRes.rows.length > 0) progress = progRes.rows[0];

      // Mark as visited (creates progress row if not exists)
      await pool.query(
        `INSERT INTO study_progress ("userId", "lessonId", last_visited)
         VALUES ($1, $2, NOW())
         ON CONFLICT ("userId", "lessonId") DO UPDATE SET last_visited = NOW()`,
        [userId, lessonId]
      );
    }

    return Response.json({
      lesson: lessonRes.rows[0],
      questions: questionsRes.rows,
      highlights,
      progress,
      prevLesson,
      nextLesson,
      isAuthenticated: !!userId,
    });
  } catch (error) {
    console.error("GET lesson error:", error);
    return Response.json({ error: "Failed to load lesson" }, { status: 500 });
  }
}