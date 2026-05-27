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

// POST /api/study/lessons/:id/highlights
// Body: { highlighted_text, start_offset, end_offset, note? }
// Creates a new highlight for the current user on this lesson
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
    const { highlighted_text, start_offset, end_offset, note } = await request.json();
    if (typeof highlighted_text !== "string" || typeof start_offset !== "number" || typeof end_offset !== "number") {
      return Response.json({ error: "Invalid input" }, { status: 400 });
    }

    const userId = await getUserId(session.user.email);
    if (!userId) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }

    const result = await pool.query(
      `INSERT INTO study_highlights ("userId", "lessonId", highlighted_text, start_offset, end_offset, note)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING id, highlighted_text, start_offset, end_offset, note, created_at`,
      [userId, lessonId, highlighted_text, start_offset, end_offset, note || null]
    );

    return Response.json({ highlight: result.rows[0] });
  } catch (error) {
    console.error("POST highlight error:", error);
    return Response.json({ error: "Failed to save highlight" }, { status: 500 });
  }
}