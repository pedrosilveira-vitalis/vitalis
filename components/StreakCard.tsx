"use client";
import Link from "next/link";
import Nori from "./Nori";
import { useActivity } from "./ActivityProvider";
export default function StreakCard() {
  const { data, guest, loading, error, retry } = useActivity();
  const streak = data?.streak;
  const current = streak?.current || 0;
  const goal = current < 7 ? 7 : current < 14 ? 14 : current < 30 ? 30 : Math.ceil((current + 1) / 30) * 30;
  return <section className={`streak-card ${streak?.completedToday ? "streak-complete" : ""}`} aria-labelledby="streak-title">
    <div className="streak-top"><div><p className="eyebrow">SHOW UP FOR YOURSELF</p><h2 id="streak-title">Your streak<span className="sparkle" aria-hidden="true">✦</span></h2></div><span className="streak-badge">{streak?.completedToday ? "Today ✓" : "Daily practice"}</span></div>
    <div className="streak-body"><Nori className="streak-nori"/><div><strong className="streak-count">{loading ? "…" : current}<span> day{current === 1 ? "" : "s"}</span></strong><p>{guest ? "Your next chapter starts with one question." : streak?.completedToday ? "You showed up. Nori’s proud of you." : "One answer today keeps you moving."}</p></div></div>
    <div className="streak-goal"><span>Your path toward 528</span><strong>{current} / {goal} days</strong></div>
    <progress max={goal} value={current} aria-label={`Daily practice goal: ${current} of ${goal} days`}/>
    <p className="streak-caption">Build a {goal}-day practice habit. This bar tracks consistency, not a predicted score.</p>
    {streak && <div className="streak-week" aria-label="Past seven days">{streak.week.map(day => <span key={day.date} className={day.done ? "done" : ""} title={day.date + (day.done ? " — practiced" : " — no answer recorded")}><small>{new Date(day.date + "T12:00:00Z").toLocaleDateString("en", { weekday: "narrow", timeZone: "UTC" })}</small><b aria-label={day.date + (day.done ? " completed" : " incomplete")}>{day.done ? "✓" : "·"}</b></span>)}</div>}
    {data && <div className="streak-stats"><span><b>{data.visitDays}</b> days visited</span><span><b>{streak?.best}</b> best streak</span></div>}
    <p className="streak-caption">Sign in and answer a practice, lesson, or warm-up question each day. {data && <>Day resets at midnight in {data.timeZone.replaceAll("_", " ")}.</>}</p>
    {error && <p className="portal-error" role="alert">{error} <button onClick={retry}>Retry saving</button></p>}
    <Link className="button-primary" href={guest ? "/sign-in" : "/practice/bio-biochem?n=5&d=mixed"}>{guest ? "Sign in to start your streak" : streak?.completedToday ? "Explore your next session" : "Make today count"} <span aria-hidden="true">→</span></Link>
  </section>;
}
