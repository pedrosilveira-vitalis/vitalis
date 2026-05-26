import { auth } from "@/auth";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.POSTGRES_URL,
  ssl: { rejectUnauthorized: false },
});

// GET /api/flashcards/custom?section=bio-biochem
// Returns all of the current user's custom cards, optionally filtered by section
export async function GET(request: Request) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const section = searchParams.get("section");

  try {
    // Get the user's ID from their email
    const userRes = await pool.query(
      "SELECT id FROM users WHERE email = $1",
      [session.user.email]
    );
    if (userRes.rows.length === 0) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }
    const userId = userRes.rows[0].id;

    let cardsRes;
    if (section && section !== "all") {
      cardsRes = await pool.query(
        `SELECT id, section, front, back, concept, difficulty, created_at
         FROM custom_flashcards
         WHERE "userId" = $1 AND section = $2
         ORDER BY created_at DESC`,
        [userId, section]
      );
    } else {
      cardsRes = await pool.query(
        `SELECT id, section, front, back, concept, difficulty, created_at
         FROM custom_flashcards
         WHERE "userId" = $1
         ORDER BY created_at DESC`,
        [userId]
      );
    }

    return Response.json({ cards: cardsRes.rows });
  } catch (error) {
    console.error("GET custom flashcards error:", error);
    return Response.json({ error: "Failed to fetch cards" }, { status: 500 });
  }
}

// POST /api/flashcards/custom
// Body: { section, front, back, concept, difficulty }
// Creates a new custom card for the current user
export async function POST(request: Request) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  try {
    const { section, front, back, concept, difficulty } = await request.json();

    if (!section || !front || !back) {
      return Response.json(
        { error: "section, front, and back are required" },
        { status: 400 }
      );
    }

    const userRes = await pool.query(
      "SELECT id FROM users WHERE email = $1",
      [session.user.email]
    );
    if (userRes.rows.length === 0) {
      return Response.json({ error: "User not found" }, { status: 404 });
    }
    const userId = userRes.rows[0].id;

    const insertRes = await pool.query(
      `INSERT INTO custom_flashcards ("userId", section, front, back, concept, difficulty)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING id, section, front, back, concept, difficulty, created_at`,
      [userId, section, front, back, concept || null, difficulty || "medium"]
    );

    return Response.json({ card: insertRes.rows[0] });
  } catch (error) {
    console.error("POST custom flashcard error:", error);
    return Response.json({ error: "Failed to create card" }, { status: 500 });
  }
}