"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import MainNav from "@/components/MainNav";
import Celebration from "@/components/Celebration";
import { PLANS, type PlanId } from "@/lib/billing";

type Access = { signedIn: boolean; entitlement: { plan: PlanId; daysLeft: number } | null };

/**
 * Stripe sends the student here the moment they pay, but the webhook that
 * actually grants access lands separately and can be a second or two behind.
 * So this page polls for the entitlement rather than claiming success on the
 * strength of a redirect anyone could type into the address bar.
 */
export default function CheckoutSuccessPage() {
  const [access, setAccess] = useState<Access | null>(null);
  const [slow, setSlow] = useState(false);

  useEffect(() => {
    let live = true;
    let attempts = 0;
    const tick = async () => {
      attempts += 1;
      try {
        const data: Access = await fetch("/api/entitlement").then(response => response.json());
        if (!live) return;
        if (data.entitlement) { setAccess(data); return; }
        setAccess(data);
      } catch { /* keep polling */ }
      if (!live) return;
      if (attempts >= 8) { setSlow(true); return; }
      setTimeout(tick, 1500);
    };
    tick();
    return () => { live = false; };
  }, []);

  const entitlement = access?.entitlement;
  const plan = entitlement && PLANS.find(item => item.id === entitlement.plan);

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[900px] h-[500px] bg-[#5b7a64] opacity-[0.06] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
      </div>

      <div className="relative z-10">
        <MainNav badge="Checkout" />

        <section className="px-10 pt-16 pb-12 max-w-3xl">
          <div className="font-sans text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            {entitlement ? "You’re in" : "Confirming"}
          </div>

          {entitlement && plan ? (
            <>
              <Celebration />
              <h1 className="font-sans font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(40px,5vw,72px)]">
                Let&rsquo;s get to work.
              </h1>
              <p className="text-[15px] opacity-70 mt-5 leading-relaxed max-w-xl">
                {entitlement.daysLeft === null
                  ? `${plan.name} is live on your account.`
                  : `${plan.name} is live. You have ${entitlement.daysLeft} days of access, starting now.`}{" "}
                A receipt is on its way to your email from Stripe.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Link href="/study" className="rounded-xl bg-[#245574] text-[#f5f1ea] px-6 py-4 font-sans text-sm font-medium">
                  Start studying
                </Link>
                <Link href="/study-plan" className="rounded-xl border-2 border-[#0c1a2e] px-6 py-4 font-sans text-sm font-medium hover:bg-[#0c1a2e] hover:text-[#f5f1ea] transition-colors">
                  Build a study plan
                </Link>
              </div>
            </>
          ) : slow ? (
            <>
              <h1 className="font-sans font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(40px,5vw,72px)]">
                Payment received.
              </h1>
              <p className="text-[15px] opacity-70 mt-5 leading-relaxed max-w-xl">
                Your access is taking a moment longer than usual to switch on. Refresh in a minute and it should
                be there. If it isn&rsquo;t, email us with the receipt Stripe sent you and we&rsquo;ll sort it
                out the same day &mdash; you will not be charged twice.
              </p>
              <Link href="/plans" className="inline-block mt-8 font-sans text-[11px] tracking-[0.14em] uppercase opacity-60 hover:opacity-100">
                Back to plans
              </Link>
            </>
          ) : (
            <>
              <h1 className="font-sans font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(40px,5vw,72px)] opacity-60">
                Switching on your access&hellip;
              </h1>
              <p className="text-[15px] opacity-70 mt-5 leading-relaxed max-w-xl">
                This usually takes a second or two. You don&rsquo;t need to do anything.
              </p>
            </>
          )}
        </section>
      </div>
    </div>
  );
}
