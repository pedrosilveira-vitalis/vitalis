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

export async function PATCH(request: Request) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Not signed in" }, { status: 401 });
  }

  const userId = await getUserId(session.user.email);
  if (!userId) {
    return Response.json({ error: "User not found" }, { status: 404 });
  }

  try {
    const { itemId, completed } = await request.json() as { itemId: string; completed: boolean };

    if (typeof itemId !== "string" || typeof completed !== "boolean") {
      return Response.json({ error: "Invalid input" }, { status: 400 });
    }

    // Get current plan
    const planRes = await pool.query(
      `SELECT id, completed_items FROM study_plans
       WHERE "userId" = $1 AND is_current = TRUE
       ORDER BY created_at DESC LIMIT 1`,
      [userId]
    );

    if (planRes.rows.length === 0) {
      return Response.json({ error: "No current plan" }, { status: 404 });
    }

    const planId = planRes.rows[0].id;
    const currentCompleted: string[] = planRes.rows[0].completed_items || [];

    let newCompleted: string[];
    if (completed) {
      newCompleted = currentCompleted.includes(itemId)
        ? currentCompleted
        : [...currentCompleted, itemId];
    } else {
      newCompleted = currentCompleted.filter((id) => id !== itemId);
    }

    await pool.query(
      `UPDATE study_plans SET completed_items = $1, updated_at = NOW() WHERE id = $2`,
      [JSON.stringify(newCompleted), planId]
    );

    return Response.json({ success: true, completedItems: newCompleted });
  } catch (error) {
    console.error("Toggle plan item error:", error);
    return Response.json({ error: "Failed to update plan" }, { status: 500 });
  }
}