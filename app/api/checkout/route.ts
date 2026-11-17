import { auth } from "@/auth";
import { findPlan, findWindow, formatPrice, normalizeReferral, priceFor } from "@/lib/billing";
import { stripeConfigured, stripePost } from "@/lib/stripe";

function origin(request: Request): string {
  const configured = process.env.NEXT_PUBLIC_SITE_URL;
  if (configured) return configured.replace(/\/$/, "");
  const header = request.headers.get("origin");
  if (header) return header.replace(/\/$/, "");
  return new URL(request.url).origin;
}

export async function POST(request: Request) {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ error: "Sign in before checking out so your access attaches to your account." }, { status: 401 });
  }
  if (!stripeConfigured()) {
    return Response.json({ error: "Checkout is not switched on yet. Add STRIPE_SECRET_KEY and try again." }, { status: 503 });
  }

  let input;
  try { input = await request.json(); } catch { return Response.json({ error: "Invalid request." }, { status: 400 }); }

  const plan = findPlan(String(input?.plan ?? ""));
  if (!plan) return Response.json({ error: "Choose a plan." }, { status: 400 });
  const window = findWindow(plan, Number(input?.days));
  if (!window) return Response.json({ error: "Choose an access window." }, { status: 400 });

  const referral = normalizeReferral(input?.referral);
  // The price is recomputed here from the catalogue. Nothing the browser sends
  // can set an amount, so a tampered request buys nothing cheaper.
  const amount = priceFor(plan, window, referral);
  const email = session.user.email.toLowerCase();

  try {
    const checkout = await stripePost<{ id: string; url: string }>("/checkout/sessions", {
      mode: "payment",
      customer_email: email,
      success_url: `${origin(request)}/plans/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${origin(request)}/plans?cancelled=1`,
      client_reference_id: email,
      // Carried through to the webhook so fulfilment never has to trust the browser.
      metadata: { email, plan: plan.id, window_days: String(window.days), referral: referral ?? "" },
      payment_intent_data: {
        description: `Vitalis ${plan.name} · ${window.days}-day access`,
        metadata: { email, plan: plan.id, window_days: String(window.days) },
      },
      line_items: [
        {
          quantity: 1,
          price_data: {
            currency: "usd",
            unit_amount: amount,
            product_data: {
              name: `Vitalis ${plan.name} — ${window.days} days`,
              description: plan.tagline,
            },
          },
        },
      ],
    });
    return Response.json({ url: checkout.url, amount: formatPrice(amount) }, { headers: { "Cache-Control": "no-store" } });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Checkout could not be started.";
    return Response.json({ error: message }, { status: 502 });
  }
}
