"use client";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
export type Call = { id: string; studentEmail: string; title: string; startsAt: string; durationMinutes: number; zoomUrl: string; notes: string };
export function CallDetails({ call }: { call: Call }) {
  const date = new Date(call.startsAt);
  return <div className="call-details"><div className="call-date"><strong>{date.toLocaleDateString(undefined, { day: "2-digit" })}</strong><span>{date.toLocaleDateString(undefined, { month: "short" })}</span></div>
    <div><h3>{call.title}</h3><p>{date.toLocaleString(undefined, { weekday: "short", hour: "numeric", minute: "2-digit", timeZoneName: "short" })} · {call.durationMinutes} min</p>{call.notes && <p className="call-note">{call.notes}</p>}
    <a className="button-primary" href={call.zoomUrl} target="_blank" rel="noopener noreferrer">Open Zoom <span aria-hidden="true">↗</span></a></div></div>;
}
export default function UpcomingCalls({ compact = false }: { compact?: boolean }) {
  const [calls, setCalls] = useState<Call[]>([]);
  const [status, setStatus] = useState("loading");
  const [admin, setAdmin] = useState(false);
  const load = useCallback(async () => {
    try {
      const res = await fetch("/api/calls", { signal: AbortSignal.timeout(12000), cache: "no-store" });
      if (res.status === 401) { setStatus("guest"); setCalls([]); setAdmin(false); return; }
      const data = await res.json();
      if (!res.ok) throw new Error();
      setCalls(data.calls); setAdmin(data.isAdmin); setStatus("ready");
    } catch { setStatus("error"); }
  }, []);
  useEffect(() => {
    load();
    const timer = setInterval(() => { if (document.visibilityState === "visible") load(); }, 60000);
    window.addEventListener("focus", load);
    return () => { clearInterval(timer); window.removeEventListener("focus", load); };
  }, [load]);
  return <section className="calls-card" aria-labelledby="calls-title">
    <div className="section-heading"><h2 id="calls-title">Your upcoming calls</h2><span aria-hidden="true" className="call-symbol">↗</span></div>
    {status === "loading" && <p role="status">Loading your appointments…</p>}
    {status === "guest" && <p><Link href="/sign-in">Sign in</Link> to see the calls scheduled for you.</p>}
    {status === "error" && <p role="alert">Could not load your calls. <button onClick={load} className="text-button">Retry</button></p>}
    {status === "ready" && calls.length === 0 && <div className="calls-empty"><span aria-hidden="true">◷</span><h3>A little guidance, when you need it.</h3><p>When your advisor schedules a call, your time and Zoom link will appear here.</p></div>}
    {status === "ready" && (compact ? calls.slice(0, 2) : calls).map(call => <CallDetails key={call.id} call={call}/>)}
    <div className="calls-links">{compact && <Link href="/calls">View all calls →</Link>}{admin && <Link href="/admin/calls">Schedule student calls →</Link>}</div>
  </section>;
}
