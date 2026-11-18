"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import NoriPose from "./NoriPose";
import { PLANS, type PlanId } from "@/lib/billing";
import { tourFor, type TourStep } from "@/lib/tour";

/**
 * The window that pops up the first time someone lands on the site with a live
 * plan. Nori walks them through what they just bought, one card at a time.
 *
 * Which cards appear depends on the plan, so a Core student is never shown a
 * door that is locked for them — the last card tells them what Complete adds
 * instead. It fires once per plan per browser; after that it is reachable from
 * the sidebar, because a tour you cannot replay is a tour you will never
 * finish.
 */
const SEEN_KEY = "vitalis.tour.seen";
export const TOUR_EVENT = "vitalis:tour";

type Access = {
  signedIn: boolean;
  standing?: boolean;
  entitlement: { plan: PlanId; daysLeft: number | null } | null;
};

export default function WelcomeTour() {
  const [steps, setSteps] = useState<TourStep[]>([]);
  const [plan, setPlan] = useState<PlanId | null>(null);
  const [open, setOpen] = useState(false);
  const [index, setIndex] = useState(0);
  const card = useRef<HTMLDivElement>(null);

  const load = useCallback(async (): Promise<{ steps: TourStep[]; plan: PlanId } | null> => {
    try {
      const access: Access = await fetch("/api/entitlement").then(response => response.json());
      const id = access.entitlement?.plan;
      if (!id) return null;
      const found = PLANS.find(item => item.id === id);
      if (!found) return null;
      return { steps: tourFor(found.capabilities), plan: id };
    } catch {
      return null;
    }
  }, []);

  // First visit with a live plan: open on its own. Later visits: only on ask.
  useEffect(() => {
    let live = true;
    (async () => {
      const result = await load();
      if (!live || !result) return;
      setSteps(result.steps);
      setPlan(result.plan);
      let seen: string | null = null;
      try { seen = window.localStorage.getItem(SEEN_KEY); } catch { seen = null; }
      if (seen !== result.plan) { setIndex(0); setOpen(true); }
    })();
    return () => { live = false; };
  }, [load]);

  // The sidebar's "Tour of your plan" asks for it by event, so the tour can
  // live here in the layout and still be opened from anywhere.
  useEffect(() => {
    const replay = async () => {
      let next = steps;
      let id = plan;
      if (!next.length) {
        const result = await load();
        if (!result) return;
        next = result.steps;
        id = result.plan;
        setSteps(next);
        setPlan(id);
      }
      setIndex(0);
      setOpen(true);
    };
    window.addEventListener(TOUR_EVENT, replay);
    return () => window.removeEventListener(TOUR_EVENT, replay);
  }, [steps, plan, load]);

  const close = useCallback(() => {
    setOpen(false);
    if (plan) { try { window.localStorage.setItem(SEEN_KEY, plan); } catch { /* private mode */ } }
  }, [plan]);

  useEffect(() => {
    if (!open) return;
    card.current?.focus();
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") close();
      if (event.key === "ArrowRight") setIndex(current => Math.min(current + 1, steps.length - 1));
      if (event.key === "ArrowLeft") setIndex(current => Math.max(current - 1, 0));
    };
    window.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open, close, steps.length]);

  if (!open || !steps.length) return null;

  const step = steps[index];
  const first = index === 0;
  const last = index === steps.length - 1;
  const planName = PLANS.find(item => item.id === plan)?.name ?? "Vitalis";

  return (
    <div className="tour-scrim" role="presentation" onClick={event => { if (event.target === event.currentTarget) close(); }}>
      <div
        className="tour-card"
        role="dialog"
        aria-modal="true"
        aria-label={`${planName} tour, step ${index + 1} of ${steps.length}`}
        tabIndex={-1}
        ref={card}
      >
        <div className="tour-head">
          <span className="tour-kicker">
            {planName} is live <span aria-hidden="true">·</span> step {index + 1} of {steps.length}
          </span>
          <button type="button" className="tour-close" onClick={close} aria-label="Close the tour">
            &times;
          </button>
        </div>

        <div className="tour-body">
          <div className="tour-stage" style={{ "--tour-accent": step.accent } as React.CSSProperties}>
            <p className="tour-bubble">{step.says}</p>
            <NoriPose prop={step.prop} pose={step.pose} accent={step.accent} />
          </div>

          <div className="tour-copy">
            <h2>{step.heading}</h2>
            <p>{step.body}</p>
            <Link href={step.href} className={step.locked ? "tour-link tour-link-muted" : "tour-link"} onClick={close}>
              {step.cta} <span aria-hidden="true">&rarr;</span>
            </Link>
          </div>
        </div>

        <div className="tour-foot">
          <div className="tour-dots" aria-hidden="true">
            {steps.map((item, dot) => (
              <button
                key={item.id}
                type="button"
                className={dot === index ? "tour-dot is-on" : "tour-dot"}
                onClick={() => setIndex(dot)}
                tabIndex={-1}
              />
            ))}
          </div>
          <div className="tour-controls">
            <button
              type="button"
              className="tour-back"
              onClick={() => setIndex(current => Math.max(current - 1, 0))}
              disabled={first}
            >
              Back
            </button>
            {last ? (
              <button type="button" className="tour-next" onClick={close}>
                Let&rsquo;s get to work <span aria-hidden="true">&rarr;</span>
              </button>
            ) : (
              <button type="button" className="tour-next" onClick={() => setIndex(current => current + 1)}>
                Next <span aria-hidden="true">&rarr;</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
