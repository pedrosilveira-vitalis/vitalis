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

// GET /api/conversations/:id
// Returns a single conversation with all its messages
export async function GET(
  request: Request,
  context: { params: Promise<{ id: string }> }
) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  const params = await context.params;
  const conversationId = parseInt(params.id, 10);
  if (isNaN(conversationId)) {
    return Response.json({ error: "Invalid conversation ID" }, { status: 400 });
  }

  try {
    const userId = await getUserId(session.user.email);
    if (!userId) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }

    // Verify ownership
    const conv = await pool.query(
      `SELECT id, title, created_at, updated_at
       FROM tutor_conversations
       WHERE id = $1 AND "userId" = $2`,
      [conversationId, userId]
    );

    if (conv.rows.length === 0) {
      return Response.json({ error: "Conversation not found" }, { status: 404 });
    }

    const messages = await pool.query(
      `SELECT role, content, "messageIndex"
       FROM tutor_messages
       WHERE "conversationId" = $1
       ORDER BY "messageIndex" ASC`,
      [conversationId]
    );

    return Response.json({
      conversation: conv.rows[0],
      messages: messages.rows,
    });
  } catch (error) {
    console.error("GET conversation error:", error);
    return Response.json({ error: "Failed to load conversation" }, { status: 500 });
  }
}

// DELETE /api/conversations/:id
export async function DELETE(
  request: Request,
  context: { params: Promise<{ id: string }> }
) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  const params = await context.params;
  const conversationId = parseInt(params.id, 10);
  if (isNaN(conversationId)) {
    return Response.json({ error: "Invalid conversation ID" }, { status: 400 });
  }

  try {
    const userId = await getUserId(session.user.email);
    if (!userId) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }

    const result = await pool.query(
      `DELETE FROM tutor_conversations WHERE id = $1 AND "userId" = $2`,
      [conversationId, userId]
    );

    if (result.rowCount === 0) {
      return Response.json({ error: "Conversation not found or not yours" }, { status: 404 });
    }

    return Response.json({ success: true });
  } catch (error) {
    console.error("DELETE conversation error:", error);
    return Response.json({ error: "Failed to delete conversation" }, { status: 500 });
  }
}