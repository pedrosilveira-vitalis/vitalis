import { createHmac, timingSafeEqual } from "node:crypto";

/**
 * A thin Stripe client over their REST API.
 *
 * Deliberately not the Stripe SDK: this workspace cannot install packages, and
 * the two calls we need are a form-encoded POST and an HMAC check. Fewer
 * dependencies on the path that touches money is a feature, not a compromise.
 */
const API = "https://api.stripe.com/v1";

export function stripeConfigured(): boolean {
  return Boolean(process.env.STRIPE_SECRET_KEY);
}

function secretKey(): string {
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) throw new Error("STRIPE_SECRET_KEY is not set.");
  return key;
}

/** Stripe takes nested params as bracketed form fields, not JSON. */
export function encodeForm(value: unknown, prefix = "", out: string[] = []): string {
  if (value === null || value === undefined) return out.join("&");
  if (Array.isArray(value)) {
    value.forEach((item, index) => encodeForm(item, `${prefix}[${index}]`, out));
  } else if (typeof value === "object") {
    for (const [key, item] of Object.entries(value as Record<string, unknown>)) {
      encodeForm(item, prefix ? `${prefix}[${key}]` : key, out);
    }
  } else {
    out.push(`${encodeURIComponent(prefix)}=${encodeURIComponent(String(value))}`);
  }
  return out.join("&");
}

export async function stripePost<T>(path: string, body: Record<string, unknown>, idempotencyKey?: string): Promise<T> {
  const response = await fetch(`${API}${path}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${secretKey()}`,
      "Content-Type": "application/x-www-form-urlencoded",
      ...(idempotencyKey ? { "Idempotency-Key": idempotencyKey } : {}),
    },
    body: encodeForm(body),
  });
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const message = payload?.error?.message || `Stripe returned ${response.status}.`;
    throw new Error(message);
  }
  return payload as T;
}

/**
 * Verifies the Stripe-Signature header against the raw request body.
 *
 * Without this, anyone who learns the webhook URL can post themselves a free
 * subscription, so an unverifiable payload is rejected rather than trusted.
 */
export function verifyWebhook(rawBody: string, header: string | null, secret: string, toleranceSeconds = 300): boolean {
  if (!header) return false;
  // Stripe sends every v1 signature it considers valid, and sends more than
  // one while a signing secret is being rotated. Taking only the last would
  // reject good events during a rotation, so each is checked.
  let timestamp = "";
  const signatures: string[] = [];
  for (const piece of header.split(",")) {
    const [key, ...rest] = piece.trim().split("=");
    const value = rest.join("=");
    if (key === "t") timestamp = value;
    else if (key === "v1") signatures.push(value);
  }
  if (!timestamp || !signatures.length) return false;

  const age = Math.abs(Date.now() / 1000 - Number(timestamp));
  if (!Number.isFinite(age) || age > toleranceSeconds) return false;

  const expected = createHmac("sha256", secret).update(`${timestamp}.${rawBody}`).digest("hex");
  const mine = Buffer.from(expected, "utf8");
  return signatures.some(candidate => {
    const given = Buffer.from(candidate, "utf8");
    return given.length === mine.length && timingSafeEqual(given, mine);
  });
}
