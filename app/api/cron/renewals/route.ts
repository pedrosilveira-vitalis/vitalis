import { PLANS } from "@/lib/billing";
import { sendRenewalWarning } from "@/lib/email";
import { portalDb } from "@/lib/portal-db";

/**
 * Daily renewal warnings.
 *
 * Runs on a Vercel cron. Guarded by CRON_SECRET so the endpoint cannot be used
 * by anyone else to spam students. Each student is warned once per purchase,
 * recorded in the entitlement row, so a daily run cannot mail them repeatedly.
 */
const WARN_AT_DAYS = 10;

function authorized(request: Request): boolean {
  const secret = process.env.CRON_SECRET;
  // Vercel sends the secret as a bearer token on scheduled invocations.
  if (!secret) return false;
  return request.headers.get("authorization") === `Bearer ${secret}`;
}

export async function GET(request: Request) {
  if (!authorized(request)) return Response.json({ error: "Not authorized." }, { status: 401 });

  try {
    const db = await portalDb();
    await db.query(`ALTER TABLE vitalis_entitlements ADD COLUMN IF NOT EXISTS warned_at TIMESTAMPTZ`);

    const due = await db.query(
      `SELECT id, email, plan, expires_at
       FROM vitalis_entitlements
       WHERE warned_at IS NULL
         AND expires_at > NOW()
         AND expires_at <= NOW() + ($1 || ' days')::interval
       LIMIT 200`,
      [String(WARN_AT_DAYS)],
    );

    let sent = 0;
    for (const row of due.rows) {
      const expires = new Date(String(row.expires_at));
      const daysLeft = Math.max(1, Math.ceil((expires.getTime() - Date.now()) / 86400000));
      const name = PLANS.find(plan => plan.id === row.plan)?.name ?? String(row.plan);
      const ok = await sendRenewalWarning(String(row.email), name, daysLeft);
      if (ok) {
        // Only mark it sent if it actually went, so a mail outage retries tomorrow.
        await db.query(`UPDATE vitalis_entitlements SET warned_at = NOW() WHERE id = $1`, [row.id]);
        sent += 1;
      }
    }

    return Response.json({ checked: due.rows.length, sent });
  } catch (error) {
    console.error("Renewal cron failed", error);
    return Response.json({ error: "Renewal run failed." }, { status: 503 });
  }
}
