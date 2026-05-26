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

// GET /api/conversations
// Returns all of the current user's conversations, ordered by most recent
export async function GET() {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  try {
    const userId = await getUserId(session.user.email);
    if (!userId) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }

    const result = await pool.query(
      `SELECT c.id, c.title, c.created_at, c.updated_at,
              (SELECT content FROM tutor_messages WHERE "conversationId" = c.id ORDER BY "messageIndex" ASC LIMIT 1) AS first_message,
              (SELECT COUNT(*) FROM tutor_messages WHERE "conversationId" = c.id) AS message_count
       FROM tutor_conversations c
       WHERE c."userId" = $1
       ORDER BY c.updated_at DESC`,
      [userId]
    );

    return Response.json({ conversations: result.rows });
  } catch (error) {
    console.error("GET conversations error:", error);
    return Response.json({ error: "Failed to fetch conversations" }, { status: 500 });
  }
}

// POST /api/conversations
// Body: { title?: string }
// Creates a new conversation. Returns the new conversation ID.
export async function POST(request: Request) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  try {
    const body = await request.json().catch(() => ({}));
    const title = body.title || "New conversation";

    const userId = await getUserId(session.user.email);
    if (!userId) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }

    const result = await pool.query(
      `INSERT INTO tutor_conversations ("userId", title)
       VALUES ($1, $2)
       RETURNING id, title, created_at, updated_at`,
      [userId, title]
    );

    return Response.json({ conversation: result.rows[0] });
  } catch (error) {
    console.error("POST conversation error:", error);
    return Response.json({ error: "Failed to create conversation" }, { status: 500 });
  }
}