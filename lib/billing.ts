import type { Database } from "./portal-store";
import { isAdmin } from "./engagement";

/**
 * Plan catalogue.
 *
 * Prices are held here rather than in Stripe so the marketing page and the
 * checkout session can never disagree about what a student is being charged.
 * `listCents` is the real, published price; `priceCents` is what they pay.
 * Those are only allowed to differ when a genuine referral code is applied,
 * because advertising a reference price the product has never sold at is a
 * fictitious price under FTC guidance and breaches Stripe's terms.
 */
export type PlanId = "core" | "complete";
export type WindowDays = 90 | 180;

export interface PlanWindow {
  days: WindowDays;
  priceCents: number;
  listCents: number;
}

/**
 * What a plan unlocks. Split on question bank versus written lessons rather
 * than on a unit count: there are only 28 units, so any "first N units" line
 * either gives most of the course away or is too thin to sell. Questions and
 * lessons are two genuinely different products, which is also how the rest of
 * the market is drawn.
 */
export interface Capabilities {
  questions: boolean;
  lessons: boolean;
  liveReviews: boolean;
  /**
   * How many full-length forms this plan opens, counted from Full-Length 1.
   * Zero signed out, one with any account, two on Core, five on Complete.
   */
  fullLengths: number;
}

export interface Plan {
  id: PlanId;
  name: string;
  tagline: string;
  /** Higher rank wins when a student holds more than one live entitlement. */
  rank: number;
  capabilities: Capabilities;
  features: string[];
  missing: string[];
  windows: PlanWindow[];
}

export const QUESTION_COUNT = 1250;
export const LESSON_COUNT = 250;

export const PLANS: Plan[] = [
  {
    id: "core",
    name: "Core",
    tagline: "The whole question bank, with a written explanation on every answer.",
    rank: 1,
    capabilities: { questions: true, lessons: false, liveReviews: false, fullLengths: 2 },
    features: [
      `All ${QUESTION_COUNT.toLocaleString()} practice questions, every section`,
      "A full written explanation on every answer",
      "Full-Lengths 1 and 2, timed and scored like the real thing, with their full reports",
      "Flashcards, flagged questions and the score calculator",
      "Ask Nori, your AI tutor, without limits",
    ],
    missing: [
      `The ${LESSON_COUNT} written lessons`,
      "The 28 unit cheat sheets",
      "Full-Lengths 3, 4 and 5",
      "Live group review sessions",
      "Study guides",
    ],
    windows: [
      { days: 90, priceCents: 14900, listCents: 14900 },
      { days: 180, priceCents: 19900, listCents: 19900 },
    ],
  },
  {
    id: "complete",
    name: "Complete",
    tagline: "Everything in Core, plus all 250 lessons and a live review before each test date.",
    rank: 2,
    capabilities: { questions: true, lessons: true, liveReviews: true, fullLengths: 5 },
    features: [
      `All ${LESSON_COUNT} lessons, reviewed line by line against published sources`,
      "All 28 unit cheat sheets, printable as PDFs",
      `All ${QUESTION_COUNT.toLocaleString()} practice questions with full explanations`,
      "All five full-length practice exams, timed and scored like the real thing",
      "A live group review before every MCAT date in your window",
      "Any study guides we publish during your window, free",
      "Flashcards, flagged questions and the score calculator",
      "Ask Nori, your AI tutor, without limits",
    ],
    missing: [],
    windows: [
      { days: 90, priceCents: 49900, listCents: 59900 },
      { days: 180, priceCents: 64900, listCents: 74900 },
    ],
  },
];

export function findPlan(id: string): Plan | undefined {
  return PLANS.find(plan => plan.id === id);
}

export function findWindow(plan: Plan, days: number): PlanWindow | undefined {
  return plan.windows.find(window => window.days === days);
}

export function formatPrice(cents: number): string {
  return cents % 100 === 0 ? `$${cents / 100}` : `$${(cents / 100).toFixed(2)}`;
}

/**
 * Referral codes carry the discount a tutor gives a student. The tutor is paid
 * on the back of the same code, so the discount and the commission are one
 * number and cannot drift apart.
 */
export const REFERRAL_DISCOUNT_CENTS = 10000;

export function normalizeReferral(code: unknown): string | null {
  if (typeof code !== "string") return null;
  const trimmed = code.trim().toUpperCase();
  return /^[A-Z0-9][A-Z0-9-]{2,23}$/.test(trimmed) ? trimmed : null;
}

/**
 * A referral only ever reduces a price that is genuinely listed higher. On Core,
 * where list and price are equal, a code changes nothing rather than cutting
 * into a margin that is not there.
 */
export function priceFor(plan: Plan, window: PlanWindow, referral: string | null): number {
  if (!referral) return window.priceCents;
  if (window.listCents <= window.priceCents) return window.priceCents;
  return Math.max(window.priceCents - REFERRAL_DISCOUNT_CENTS, 0) || window.priceCents;
}

export interface Entitlement {
  plan: PlanId;
  capabilities: Capabilities;
  expiresAt: Date;
  daysLeft: number;
}

const LOCKED: Capabilities = { questions: false, lessons: false, liveReviews: false, fullLengths: 0 };
/**
 * Someone signed in without a plan. Full-Length 1 is free with any account:
 * sitting a full-length and reading the report is the only honest way to find
 * out whether the course is worth buying.
 */
const FREE_TIER: Capabilities = { questions: false, lessons: false, liveReviews: false, fullLengths: 1 };

export function capabilitiesOf(entitlement: Entitlement | null): Capabilities {
  return entitlement ? entitlement.capabilities : FREE_TIER;
}

/**
 * The one question the rest of the app asks: what is this student allowed to
 * see right now? Returns null for signed-out or lapsed students.
 */
export async function entitlementFor(db: Database, email: string, now = new Date()): Promise<Entitlement | null> {
  const result = await db.query(
    `SELECT plan, expires_at FROM vitalis_entitlements
     WHERE email = $1 AND expires_at > $2
     ORDER BY expires_at DESC`,
    [email.toLowerCase(), now],
  );
  if (!result.rows.length) return null;
  let best: { plan: Plan; expiresAt: Date } | null = null;
  for (const row of result.rows) {
    const plan = findPlan(String(row.plan));
    if (!plan) continue;
    const expiresAt = new Date(String(row.expires_at));
    if (!best || plan.rank > best.plan.rank || (plan.rank === best.plan.rank && expiresAt > best.expiresAt)) {
      best = { plan, expiresAt };
    }
  }
  if (!best) return null;
  return {
    plan: best.plan.id,
    capabilities: best.plan.capabilities,
    expiresAt: best.expiresAt,
    daysLeft: Math.max(0, Math.ceil((best.expiresAt.getTime() - now.getTime()) / 86400000)),
  };
}

/**
 * Accounts that get everything without paying: you, your tutors, and any beta
 * students. Set FREE_ACCESS_EMAILS in Vercel as a comma-separated list.
 * Without this the owner cannot read his own lessons, which is a silly way to
 * find out the gate works.
 */
export function hasStandingAccess(email: string): boolean {
  const list = process.env.FREE_ACCESS_EMAILS;
  if (!list) return false;
  const target = email.trim().toLowerCase();
  return list.split(",").some(entry => entry.trim().toLowerCase() === target && entry.trim().length > 0);
}

const EVERYTHING: Capabilities = { questions: true, lessons: true, liveReviews: true, fullLengths: 5 };

/**
 * The gate every protected route calls. Returns the student's capabilities, and
 * is deliberately fail-closed: if the database cannot be reached we lock rather
 * than open, because the failure mode of guessing wrong is giving the product
 * away.
 */
export async function capabilitiesFor(db: Database, email: string | null | undefined): Promise<Capabilities> {
  if (!email) return LOCKED;
  // An administrator can always see the product. Nobody should have to buy
  // their own site to look at it, and a separate env var for that is a step
  // waiting to be forgotten.
  if (isAdmin(email) || hasStandingAccess(email)) return EVERYTHING;
  try {
    return capabilitiesOf(await entitlementFor(db, email));
  } catch {
    // Fail closed on everything paid, but an account still opens the free form.
    return FREE_TIER;
  }
}

/**
 * Written once per Stripe session id, so a webhook that Stripe retries — which
 * it will — cannot hand a student two access windows for one payment.
 */
export async function grantEntitlement(
  db: Database,
  input: { sessionId: string; email: string; plan: PlanId; windowDays: number; amountCents: number; referral: string | null },
  now = new Date(),
): Promise<void> {
  const expiresAt = new Date(now.getTime() + input.windowDays * 86400000);
  await db.query(
    `INSERT INTO vitalis_entitlements (id, email, plan, window_days, amount_cents, referral_code, starts_at, expires_at)
     VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
     ON CONFLICT (id) DO NOTHING`,
    [input.sessionId, input.email.toLowerCase(), input.plan, input.windowDays, input.amountCents, input.referral, now, expiresAt],
  );
}
