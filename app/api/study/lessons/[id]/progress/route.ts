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

// POST /api/study/lessons/:id/progress
// Body: { read_complete?: boolean, questions_correct?: number, questions_total?: number }
// Updates progress for the current user on this lesson
export async function POST(
  request: Request,
  context: { params: Promise<{ id: string }> }
) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  const params = await context.params;
  const lessonId = parseInt(params.id, 10);
  if (isNaN(lessonId)) {
    return Response.json({ error: "Invalid lesson ID" }, { status: 400 });
  }

  try {
    const body = await request.json();
    const read_complete = body.read_complete;
    const questions_correct = body.questions_correct;
    const questions_total = body.questions_total;

    const userId = await getUserId(session.user.email);
    if (!userId) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }

    // Build the dynamic SET clause based on which fields were provided
    const updates: string[] = ["last_visited = NOW()"];
    const values: (number | boolean)[] = [];
    let paramIdx = 1;

    if (typeof read_complete === "boolean") {
      updates.push(`read_complete = $${paramIdx++}`);
      values.push(read_complete);
    }
    if (typeof questions_correct === "number" && typeof questions_total === "number") {
      updates.push(`questions_correct = $${paramIdx++}`);
      values.push(questions_correct);
      updates.push(`questions_total = $${paramIdx++}`);
      values.push(questions_total);
    }

    values.push(userId);
    values.push(lessonId);
    const userIdParam = paramIdx++;
    const lessonIdParam = paramIdx++;

    const result = await pool.query(
      `INSERT INTO study_progress ("userId", "lessonId", read_complete, questions_correct, questions_total, last_visited)
       VALUES ($${userIdParam}, $${lessonIdParam}, $1, $2, $3, NOW())
       ON CONFLICT ("userId", "lessonId") DO UPDATE
       SET ${updates.join(", ")}
       RETURNING read_complete, questions_correct, questions_total`,
      [
        typeof read_complete === "boolean" ? read_complete : false,
        typeof questions_correct === "number" ? questions_correct : 0,
        typeof questions_total === "number" ? questions_total : 0,
        ...values,
      ]
    );

    return Response.json({ progress: result.rows[0] });
  } catch (error) {
    console.error("POST progress error:", error);
    return Response.json({ error: "Failed to save progress" }, { status: 500 });
  }
}