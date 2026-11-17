import { findPlan, grantEntitlement, normalizeReferral } from "@/lib/billing";
import { portalDb } from "@/lib/portal-db";
import { verifyWebhook } from "@/lib/stripe";
import { PLANS } from "@/lib/billing";
import { sendPurchase } from "@/lib/email";

/**
 * Access is granted here and nowhere else.
 *
 * The success page only tells a student the payment went through; it is a
 * redirect they could visit by hand. Stripe calling this route, signed, is the
 * only evidence that money actually moved.
 */
export async function POST(request: Request) {
  const secret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!secret) return Response.json({ error: "Webhook is not configured." }, { status: 503 });

  const raw = await request.text();
  if (!verifyWebhook(raw, request.headers.get("stripe-signature"), secret)) {
    return Response.json({ error: "Signature could not be verified." }, { status: 400 });
  }

  let event;
  try { event = JSON.parse(raw); } catch { return Response.json({ error: "Invalid payload." }, { status: 400 }); }

  if (event?.type !== "checkout.session.completed") {
    // Everything else is acknowledged so Stripe stops retrying it.
    return Response.json({ received: true });
  }

  const checkout = event.data?.object ?? {};
  if (checkout.payment_status !== "paid") return Response.json({ received: true });

  const metadata = checkout.metadata ?? {};
  const email = String(metadata.email || checkout.customer_email || checkout.client_reference_id || "").toLowerCase();
  const plan = findPlan(String(metadata.plan ?? ""));
  const windowDays = Number(metadata.window_days);
  const sessionId = String(checkout.id ?? "");

  if (!email || !plan || !Number.isInteger(windowDays) || windowDays < 1 || !sessionId) {
    // Returning 200 here: the payload is genuinely from Stripe but we cannot act
    // on it, and retrying will not change that. It is logged for a human.
    console.error("Unfulfillable checkout session", { sessionId, email, plan: metadata.plan, windowDays });
    return Response.json({ received: true, fulfilled: false });
  }

  try {
    await grantEntitlement(await portalDb(), {
      sessionId,
      email,
      plan: plan.id,
      windowDays,
      amountCents: Number(checkout.amount_total ?? 0),
      referral: normalizeReferral(metadata.referral),
    });
  } catch (error) {
    // A 500 asks Stripe to retry, which is what we want if the database blinked.
    console.error("Entitlement write failed", error);
    return Response.json({ error: "Could not record the purchase." }, { status: 500 });
  }

  try {
    const name = PLANS.find(entry => entry.id === plan.id)?.name ?? plan.id;
    await sendPurchase(email, name, windowDays, new Date(Date.now() + windowDays * 86400000));
  } catch (error) {
    // The student has their access; a missing email is not worth a retry storm.
    console.error("Purchase email failed", error);
  }

  return Response.json({ received: true, fulfilled: true });
}
