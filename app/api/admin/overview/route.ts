import { auth } from "@/auth";
import { isAdmin } from "@/lib/engagement";
import { PLANS, formatPrice } from "@/lib/billing";
import { portalDb } from "@/lib/portal-db";

/**
 * Everything the admin page needs in one call: who has signed up, what they
 * bought, and what it came to. Admin-only, checked server side — the page also
 * gates, but a page gate alone is a suggestion, not a control.
 */
export async function GET() {
  const email = (await auth())?.user?.email;
  if (!email) return Response.json({ error: "Sign in." }, { status: 401 });
  if (!isAdmin(email)) return Response.json({ error: "Administrator access required." }, { status: 403 });

  try {
    const db = await portalDb();

    const people = await db.query(`
      SELECT u.email, u.name,
             e.plan, e.window_days, e.amount_cents, e.referral_code, e.expires_at
      FROM users u
      LEFT JOIN LATERAL (
        SELECT plan, window_days, amount_cents, referral_code, expires_at
        FROM vitalis_entitlements
        WHERE email = LOWER(u.email) AND expires_at > NOW()
        ORDER BY expires_at DESC LIMIT 1
      ) e ON TRUE
      ORDER BY (e.plan IS NULL), e.expires_at DESC NULLS LAST, u.email
      LIMIT 500
    `);

    const totals = await db.query(`
      SELECT COUNT(*)::int AS purchases,
             COALESCE(SUM(amount_cents), 0)::bigint AS gross_cents,
             COUNT(*) FILTER (WHERE expires_at > NOW())::int AS active,
             COUNT(*) FILTER (WHERE referral_code IS NOT NULL)::int AS referred
      FROM vitalis_entitlements
    `);

    const byReferral = await db.query(`
      SELECT referral_code AS code, COUNT(*)::int AS sales
      FROM vitalis_entitlements
      WHERE referral_code IS NOT NULL
      GROUP BY referral_code ORDER BY sales DESC LIMIT 50
    `);

    const summary = totals.rows[0] ?? {};

    return Response.json(
      {
        people: people.rows.map(row => ({
          email: row.email,
          name: row.name,
          plan: row.plan ? PLANS.find(p => p.id === row.plan)?.name ?? row.plan : null,
          windowDays: row.window_days,
          paid: row.amount_cents == null ? null : formatPrice(Number(row.amount_cents)),
          referral: row.referral_code,
          expiresAt: row.expires_at,
        })),
        totals: {
          signups: people.rows.length,
          purchases: Number(summary.purchases ?? 0),
          active: Number(summary.active ?? 0),
          referred: Number(summary.referred ?? 0),
          gross: formatPrice(Number(summary.gross_cents ?? 0)),
          tutorOwed: formatPrice(Number(summary.referred ?? 0) * 10000),
        },
        referrals: byReferral.rows,
      },
      { headers: { "Cache-Control": "no-store" } },
    );
  } catch {
    return Response.json({ error: "Could not load the overview." }, { status: 503 });
  }
}
