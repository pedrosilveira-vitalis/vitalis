import { auth } from "@/auth";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.POSTGRES_URL,
  ssl: { rejectUnauthorized: false },
});

// DELETE /api/flashcards/custom/:id
// Deletes a card if it belongs to the current user
export async function DELETE(
  request: Request,
  context: { params: Promise<{ id: string }> }
) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  const params = await context.params;
  const cardId = parseInt(params.id, 10);

  if (isNaN(cardId)) {
    return Response.json({ error: "Invalid card ID" }, { status: 400 });
  }

  try {
    const userRes = await pool.query(
      "SELECT id FROM users WHERE email = $1",
      [session.user.email]
    );
    if (userRes.rows.length === 0) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }
    const userId = userRes.rows[0].id;

    // Only delete if this card belongs to this user
    const result = await pool.query(
      `DELETE FROM custom_flashcards WHERE id = $1 AND "userId" = $2`,
      [cardId, userId]
    );

    if (result.rowCount === 0) {
      return Response.json({ error: "Card not found or not yours" }, { status: 404 });
    }

    return Response.json({ success: true });
  } catch (error) {
    console.error("DELETE custom flashcard error:", error);
    return Response.json({ error: "Failed to delete card" }, { status: 500 });
  }
}