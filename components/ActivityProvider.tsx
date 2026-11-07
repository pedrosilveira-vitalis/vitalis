"use client";
import { createContext, useContext, useEffect, useRef, useState, useCallback } from "react";
import type { Streak } from "@/lib/engagement";
type Activity = { streak: Streak; visitDays: number; timeZone: string; warmupToken?: string };
type State = { data: Activity | null; guest: boolean; loading: boolean; error: string; record: (token: string | undefined, answer: string) => void; retry: () => void };
const Context = createContext<State>({ data: null, guest: false, loading: true, error: "", record: () => {}, retry: () => {} });
export function useActivity() { return useContext(Context); }
export default function ActivityProvider({ children }: { children: React.ReactNode }) {
  const [data, setData] = useState<Activity | null>(null);
  const [guest, setGuest] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const pending = useRef<{ token?: string; answer: string } | null>(null);
  const queue = useRef(Promise.resolve());
  const sync = useCallback((kind: "visit" | "answer", token?: string, answer?: string) => {
    // Serialize responses so an earlier visit cannot overwrite a completed answer.
    queue.current = queue.current.then(async () => {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 15000);
      try {
        const response = await fetch("/api/activity", {
          method: "POST", headers: { "Content-Type": "application/json" }, signal: controller.signal,
          body: JSON.stringify({ kind, token, answer, timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone }),
        });
        if (response.status === 401) { setGuest(true); setData(null); setError(""); pending.current = null; return; }
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || "Could not save your progress.");
        setData(result); setGuest(false);
        if (!pending.current || kind === "answer") setError("");
        if (kind === "answer") pending.current = null;
      } catch (e) { setError(e instanceof Error && e.name !== "AbortError" ? e.message : "Could not save your progress. Please retry."); }
      finally { clearTimeout(timer); setLoading(false); }
    });
  }, []);
  useEffect(() => {
    sync("visit");
    const refresh = () => { if (document.visibilityState === "visible") sync("visit"); };
    window.addEventListener("focus", refresh);
    document.addEventListener("visibilitychange", refresh);
    const timer = setInterval(refresh, 60000);
    return () => { clearInterval(timer); window.removeEventListener("focus", refresh); document.removeEventListener("visibilitychange", refresh); };
  }, [sync]);
  function record(token: string | undefined, answer: string) {
    if (guest) return;
    if (!token) { setError("Reload this question to enable streak saving."); return; }
    pending.current = { token, answer };
    sync("answer", token, answer);
  }
  function retry() { const item = pending.current; item ? sync("answer", item.token, item.answer) : sync("visit"); }
  return <Context.Provider value={{ data, guest, loading, error, record, retry }}>{children}</Context.Provider>;
}
