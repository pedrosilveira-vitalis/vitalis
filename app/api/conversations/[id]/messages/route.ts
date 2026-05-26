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

// POST /api/conversations/:id/messages
// Body: { role: "user" | "assistant", content: string }
// Appends a message to the conversation, returns the messageIndex
export async function POST(
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
    const { role, content } = await request.json();
    if (!role || !content || (role !== "user" && role !== "assistant")) {
      return Response.json({ error: "Invalid message" }, { status: 400 });
    }

    const userId = await getUserId(session.user.email);
    if (!userId) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }

    // Verify ownership
    const ownership = await pool.query(
      `SELECT id FROM tutor_conversations WHERE id = $1 AND "userId" = $2`,
      [conversationId, userId]
    );
    if (ownership.rows.length === 0) {
      return Response.json({ error: "Conversation not found or not yours" }, { status: 404 });
    }

    // Get the next messageIndex
    const indexRes = await pool.query(
      `SELECT COALESCE(MAX("messageIndex"), -1) + 1 AS next_index
       FROM tutor_messages WHERE "conversationId" = $1`,
      [conversationId]
    );
    const messageIndex = indexRes.rows[0].next_index;

    // Insert the message
    await pool.query(
      `INSERT INTO tutor_messages ("conversationId", role, content, "messageIndex")
       VALUES ($1, $2, $3, $4)`,
      [conversationId, role, content, messageIndex]
    );

    // If this is the first user message and the conversation title is still default, set the title
    if (messageIndex === 0 && role === "user") {
      const title = content.length > 60 ? content.slice(0, 60) + "..." : content;
      await pool.query(
        `UPDATE tutor_conversations SET title = $1, updated_at = NOW() WHERE id = $2 AND title = 'New conversation'`,
        [title, conversationId]
      );
    } else {
      await pool.query(
        `UPDATE tutor_conversations SET updated_at = NOW() WHERE id = $1`,
        [conversationId]
      );
    }

    return Response.json({ messageIndex });
  } catch (error) {
    console.error("POST message error:", error);
    return Response.json({ error: "Failed to save message" }, { status: 500 });
  }
}