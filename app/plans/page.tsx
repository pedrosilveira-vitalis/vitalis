"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import MainNav from "@/components/MainNav";
import { PLANS, formatPrice, type PlanId, type WindowDays } from "@/lib/billing";

type Access = { signedIn: boolean; entitlement: { plan: PlanId; daysLeft: number } | null };

const WINDOWS: { days: WindowDays; label: string; note: string }[] = [
  { days: 90, label: "90 days", note: "One focused test cycle" },
  { days: 180, label: "180 days", note: "Room for a retake" },
];

export default function PlansPage() {
  const [days, setDays] = useState<WindowDays>(90);
  const [referral, setReferral] = useState("");
  const [busy, setBusy] = useState<PlanId | null>(null);
  const [error, setError] = useState("");
  const [access, setAccess] = useState<Access | null>(null);

  useEffect(() => {
    let live = true;
    fetch("/api/entitlement")
      .then(response => response.json())
      .then(data => { if (live) setAccess(data); })
      .catch(() => { if (live) setAccess({ signedIn: false, entitlement: null }); });
    return () => { live = false; };
  }, []);

  async function checkout(plan: PlanId) {
    setBusy(plan);
    setError("");
    try {
      const response = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plan, days, referral: referral.trim() || undefined }),
      });
      const data = await response.json();
      if (!response.ok || !data.url) throw new Error(data.error || "Checkout could not be started.");
      window.location.href = data.url;
    } catch (problem) {
      setError(problem instanceof Error ? problem.message : "Checkout could not be started.");
      setBusy(null);
    }
  }

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[900px] h-[500px] bg-[#245574] opacity-[0.05] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
      </div>

      <div className="relative z-10">
        <MainNav badge="Plans" />

        <section className="px-10 pt-14 pb-8 border-b border-[#0c1a2e15]">
          <div className="font-sans text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Plans
          </div>
          <h1 className="font-sans font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(48px,6vw,88px)] max-w-4xl">
            Buy the <span className="italic font-light text-[#245574]">window</span> you&rsquo;ll actually study in.
          </h1>
          <p className="text-[15px] opacity-70 mt-4 max-w-xl leading-relaxed">
            No monthly subscription to remember to cancel. You pick a stretch of time, pay once, and it runs
            from the day you buy it.
          </p>

          {access?.entitlement && (
            <div className="mt-6 inline-flex items-center gap-3 rounded-2xl border-2 border-[#5b7a64] bg-[#5b7a6412] px-5 py-3">
              <span className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-60">Current access</span>
              <span className="font-sans text-sm font-medium">
                {PLANS.find(plan => plan.id === access.entitlement?.plan)?.name} &middot; {access.entitlement.daysLeft} days left
              </span>
            </div>
          )}
        </section>

        <section className="px-10 py-10 max-w-5xl mx-auto">
          <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-55 mb-3">Access window</div>
          <div className="inline-flex rounded-2xl border-2 border-[#0c1a2e25] overflow-hidden">
            {WINDOWS.map(window => (
              <button
                key={window.days}
                type="button"
                onClick={() => setDays(window.days)}
                aria-pressed={days === window.days}
                className={`px-6 py-3 text-left transition-colors ${
                  days === window.days ? "bg-[#0c1a2e] text-[#f5f1ea]" : "hover:bg-[#0c1a2e0a]"
                }`}
              >
                <div className="font-sans text-lg font-medium leading-none">{window.label}</div>
                <div className={`font-sans text-[11px] mt-1 ${days === window.days ? "opacity-70" : "opacity-55"}`}>{window.note}</div>
              </button>
            ))}
          </div>
        </section>

        <section className="px-10 pb-10 grid md:grid-cols-2 gap-6 max-w-5xl mx-auto items-start">
          {PLANS.map(plan => {
            const window = plan.windows.find(option => option.days === days)!;
            const discounted = window.listCents > window.priceCents;
            const featured = plan.id === "complete";
            return (
              <div
                key={plan.id}
                className={`rounded-2xl p-8 border-2 flex flex-col h-full ${featured ? "border-[#245574] bg-[#24557408]" : "border-[#0c1a2e25]"}`}
              >
                {featured && (
                  <div className="font-sans text-[10px] tracking-[0.14em] uppercase text-[#245574] mb-3">Most complete</div>
                )}
                <h2 className="font-sans text-3xl font-medium tracking-tight leading-none">{plan.name}</h2>
                <p className="text-[14px] opacity-70 mt-3 leading-relaxed min-h-[44px]">{plan.tagline}</p>

                <div className="mt-6 flex items-baseline gap-3">
                  <span className="font-sans text-6xl font-medium tracking-tight leading-none">{formatPrice(window.priceCents)}</span>
                  {discounted && (
                    <span className="font-sans text-xl opacity-45 line-through">{formatPrice(window.listCents)}</span>
                  )}
                </div>
                <div className="font-sans text-[11px] tracking-[0.14em] uppercase opacity-55 mt-2">
                  {days} days of access &middot; paid once
                </div>
                {discounted && (
                  <div className="font-sans text-[12px] text-[#245574] mt-2">
                    Launch price. A tutor&rsquo;s referral code takes another {formatPrice(10000)} off.
                  </div>
                )}

                <ul className="mt-6 space-y-2.5 flex-1">
                  {plan.features.map(feature => (
                    <li key={feature} className="flex gap-3 text-[14px] leading-relaxed">
                      <span className="text-[#5b7a64] mt-0.5" aria-hidden="true">&#10003;</span>
                      <span>{feature}</span>
                    </li>
                  ))}
                  {plan.missing.map(feature => (
                    <li key={feature} className="flex gap-3 text-[14px] leading-relaxed opacity-45">
                      <span className="mt-0.5" aria-hidden="true">&times;</span>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>

                <button
                  type="button"
                  onClick={() => checkout(plan.id)}
                  disabled={busy !== null}
                  className={`mt-7 w-full rounded-xl px-6 py-4 font-sans text-sm font-medium tracking-wide transition-opacity disabled:opacity-50 ${
                    featured ? "bg-[#245574] text-[#f5f1ea]" : "border-2 border-[#0c1a2e] hover:bg-[#0c1a2e] hover:text-[#f5f1ea]"
                  }`}
                >
                  {busy === plan.id ? "Opening checkout…" : `Get ${plan.name}`}
                </button>
              </div>
            );
          })}
        </section>

        <section className="px-10 pb-12 max-w-5xl mx-auto">
          <label className="block max-w-sm">
            <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Referral code (optional)</div>
            <input
              value={referral}
              onChange={event => setReferral(event.target.value)}
              placeholder="From your tutor"
              className="w-full px-4 py-3 border-2 border-[#0c1a2e25] rounded-xl bg-transparent outline-none focus:border-[#245574] transition-colors font-sans"
            />
          </label>

          {error && (
            <div className="mt-5 rounded-xl border-2 border-[#a8324a] bg-[#a8324a10] px-5 py-4 text-[14px] max-w-xl">
              {error}
              {!access?.signedIn && (
                <>
                  {" "}
                  <Link href="/sign-in" className="underline">Sign in</Link> and try again.
                </>
              )}
            </div>
          )}

          <div className="mt-10 grid md:grid-cols-3 gap-8 border-t border-[#0c1a2e15] pt-8">
            <div>
              <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">How you pay</div>
              <p className="text-[13px] opacity-70 leading-relaxed">
                Card, Apple&nbsp;Pay, Google&nbsp;Pay, Cash&nbsp;App&nbsp;Pay or Link, all through Stripe. Your card
                details never touch our servers.
              </p>
            </div>
            <div>
              <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">The live sessions</div>
              <p className="text-[13px] opacity-70 leading-relaxed">
                Complete includes a live group review before every MCAT test date that falls inside your access
                window. They&rsquo;re recorded if you can&rsquo;t make one.
              </p>
            </div>
            <div>
              <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">What you get</div>
              <p className="text-[13px] opacity-70 leading-relaxed">
                1,265 practice questions across 250 units. Every one of them has been checked against published
                sources, and every answer carries a written explanation.
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
