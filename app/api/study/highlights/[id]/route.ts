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

// PATCH /api/study/highlights/:id
// Body: { note: string | null }
// Updates the note attached to a highlight
export async function PATCH(
  request: Request,
  context: { params: Promise<{ id: string }> }
) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  const params = await context.params;
  const highlightId = parseInt(params.id, 10);
  if (isNaN(highlightId)) {
    return Response.json({ error: "Invalid highlight ID" }, { status: 400 });
  }

  try {
    const { note } = await request.json();
    const userId = await getUserId(session.user.email);
    if (!userId) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }

    const result = await pool.query(
      `UPDATE study_highlights
       SET note = $1, updated_at = NOW()
       WHERE id = $2 AND "userId" = $3
       RETURNING id, note`,
      [note ?? null, highlightId, userId]
    );

    if (result.rowCount === 0) {
      return Response.json({ error: "Highlight not found or not yours" }, { status: 404 });
    }

    return Response.json({ highlight: result.rows[0] });
  } catch (error) {
    console.error("PATCH highlight error:", error);
    return Response.json({ error: "Failed to update highlight" }, { status: 500 });
  }
}

// DELETE /api/study/highlights/:id
export async function DELETE(
  request: Request,
  context: { params: Promise<{ id: string }> }
) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  const params = await context.params;
  const highlightId = parseInt(params.id, 10);
  if (isNaN(highlightId)) {
    return Response.json({ error: "Invalid highlight ID" }, { status: 400 });
  }

  try {
    const userId = await getUserId(session.user.email);
    if (!userId) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }

    const result = await pool.query(
      `DELETE FROM study_highlights WHERE id = $1 AND "userId" = $2`,
      [highlightId, userId]
    );

    if (result.rowCount === 0) {
      return Response.json({ error: "Highlight not found or not yours" }, { status: 404 });
    }

    return Response.json({ success: true });
  } catch (error) {
    console.error("DELETE highlight error:", error);
    return Response.json({ error: "Failed to delete highlight" }, { status: 500 });
  }
}