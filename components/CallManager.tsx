"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { CallDetails, type Call } from "./UpcomingCalls";
import { fetchJson } from "@/lib/fetch-json";
function localInput(iso: string) {
  const date = new Date(iso);
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
}
export default function CallManager() {
  const [calls, setCalls] = useState<Call[]>([]);
  const [editing, setEditing] = useState<Call | null>(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [listError, setListError] = useState("");
  const [loading, setLoading] = useState(true);
  const [confirmId, setConfirmId] = useState<string | null>(null);
  const [timeZone, setTimeZone] = useState("");
  const createId = useRef("");
  const form = useRef<HTMLFormElement>(null);
  const load = useCallback(async () => {
    try { const data = await fetchJson("/api/calls?manage=1", {}, 12000); setCalls(data.calls); setListError(""); }
    catch (e) { setListError(e instanceof Error ? e.message : "Could not load calls."); }
    finally { setLoading(false); }
  }, []);
  useEffect(() => { setTimeZone(Intl.DateTimeFormat().resolvedOptions().timeZone); load(); }, [load]);
  async function save(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); if (busy) return;
    setError(""); setMessage(""); setBusy(true);
    const fields = new FormData(event.currentTarget);
    createId.current ||= crypto.randomUUID();
    try {
      const startsAt = new Date(String(fields.get("startsAt")));
      if (!Number.isFinite(startsAt.getTime())) throw new Error("Choose a date and time.");
      // Reject normalized nonexistent local times at the spring daylight-saving jump.
      if (localInput(startsAt.toISOString()) !== fields.get("startsAt")) throw new Error("That local time does not exist due to daylight saving. Choose another time.");
      await fetchJson(editing ? `/api/calls/${editing.id}` : "/api/calls", {
        method: editing ? "PATCH" : "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: createId.current, studentEmail: fields.get("studentEmail"), title: fields.get("title"),
          startsAt: startsAt.toISOString(), durationMinutes: Number(fields.get("durationMinutes")), zoomUrl: fields.get("zoomUrl"), notes: fields.get("notes") }),
      }, 15000);
      createId.current = ""; form.current?.reset(); setEditing(null);
      setMessage("Saved. The student will see this call when signed in with that email.");
      await load();
    } catch (e) { setError(e instanceof Error ? e.message : "Could not save the call."); }
    finally { setBusy(false); }
  }
  async function cancel(id: string) {
    setBusy(true); setError(""); setMessage("");
    try {
      await fetchJson(`/api/calls/${id}`, { method: "DELETE" }, 15000);
      if (editing?.id === id) setEditing(null);
      setConfirmId(null); setMessage("Call cancelled and removed from the student’s portal."); await load();
    } catch (e) { setError(e instanceof Error ? e.message : "Could not cancel this call."); }
    finally { setBusy(false); }
  }
  return <><p>Assign a call using the student’s Google sign-in email. You can schedule it before their first visit. Paste the Zoom link you’ve created for them.</p>
    <form ref={form} key={editing?.id || "new"} className="call-form" onSubmit={save}>
      <h2>{editing ? "Edit appointment" : "Schedule a call"}</h2><fieldset disabled={busy}>
        <label>Student sign-in email<input name="studentEmail" type="email" required maxLength={254} defaultValue={editing?.studentEmail} placeholder="student@example.com"/></label>
        <label>Call title<input name="title" required maxLength={120} defaultValue={editing?.title} placeholder="MCAT study check-in"/></label>
        <label>Date and time ({timeZone || "your local timezone"})<input name="startsAt" type="datetime-local" required defaultValue={editing ? localInput(editing.startsAt) : undefined}/></label>
        <label>Duration in minutes<input name="durationMinutes" type="number" required min={5} max={180} defaultValue={editing?.durationMinutes || 30}/></label>
        <label className="full-width">Zoom meeting link<input name="zoomUrl" type="url" required defaultValue={editing?.zoomUrl} placeholder="https://us02web.zoom.us/j/…"/></label>
        <label className="full-width">Note for the student (optional)<textarea name="notes" maxLength={1000} defaultValue={editing?.notes} placeholder="What to prepare before we meet"/></label>
        <div className="full-width form-actions"><button className="button-primary" type="submit">{busy ? "Saving…" : editing ? "Save changes" : "Schedule call"}</button>{editing && <button type="button" className="button-outline" onClick={() => { setEditing(null); setError(""); }}>Discard edits</button>}</div>
      </fieldset>
    </form>
    {error && <p className="portal-error" role="alert">{error}</p>}{message && <p className="portal-success" role="status">{message}</p>}
    <section className="calls-card"><h2>Upcoming student calls</h2>{loading && <p>Loading calls…</p>}{listError && <p role="alert">{listError} <button className="text-button" onClick={load}>Retry</button></p>}{!loading && !listError && !calls.length && <p>Your scheduled calls will appear here.</p>}
      {calls.map(call => <article className="managed-call" key={call.id}><p className="student-email">{call.studentEmail}</p><CallDetails call={call}/>
        <div className="form-actions"><button disabled={busy} className="button-outline" onClick={() => { setEditing(call); setMessage(""); setError(""); form.current?.scrollIntoView({ behavior: "smooth", block: "start" }); }}>Edit</button>
        {confirmId === call.id ? <><span>Cancel this appointment?</span><button disabled={busy} className="button-outline" onClick={() => cancel(call.id)}>Yes, cancel</button><button disabled={busy} className="text-button" onClick={() => setConfirmId(null)}>Keep call</button></> : <button disabled={busy} className="text-button" onClick={() => setConfirmId(call.id)}>Cancel appointment</button>}</div>
      </article>)}
    </section></>;
}
