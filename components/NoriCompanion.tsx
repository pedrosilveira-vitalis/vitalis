"use client";
import { useEffect, useRef, useState } from "react";
import { usePathname } from "next/navigation";
import Nori from "./Nori";

type Message = { role: "user" | "assistant"; content: string };
export default function NoriCompanion() {
  const path = usePathname();
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const launcher = useRef<HTMLButtonElement>(null);
  const log = useRef<HTMLDivElement>(null);
  const request = useRef<AbortController | null>(null);
  useEffect(() => () => request.current?.abort(), []);
  useEffect(() => { if (open) inputRef.current?.focus(); }, [open]);
  useEffect(() => { if (log.current) log.current.scrollTop = log.current.scrollHeight; }, [messages, busy, open]);
  const close = () => { setOpen(false); launcher.current?.focus(); };
  function reset() {
    request.current?.abort(); request.current = null;
    setMessages([]); setInput(""); setError(""); setBusy(false);
    inputRef.current?.focus();
  }
  async function send() {
    const text = input.trim();
    if (!text || request.current) return;
    const pending: Message[] = [...messages, { role: "user", content: text }];
    const controller = new AbortController();
    request.current = controller; setBusy(true); setError(""); setInput(""); setMessages(pending);
    const timeout = setTimeout(() => controller.abort(), 60000);
    try {
      const response = await fetch("/api/chat", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: pending, mode: "companion" }), signal: controller.signal,
      });
      const data = await response.json();
      if (!response.ok || typeof data.reply !== "string" || !data.reply.trim()) throw new Error("No reply");
      if (request.current === controller) setMessages([...pending, { role: "assistant", content: data.reply }]);
    } catch {
      if (request.current === controller) {
        setMessages(messages); setInput(text);
        setError("Nori couldn’t respond. Your question is ready to send again.");
      }
    } finally {
      clearTimeout(timeout);
      if (request.current === controller) { request.current = null; setBusy(false); }
    }
  }
  if (path === "/sign-in") return null;
  return <>
    <button ref={launcher} type="button" className="nori-companion" aria-label="Chat with Nori on this page" aria-expanded={open} aria-controls="nori-chat-panel" onClick={() => open ? close() : setOpen(true)}>
      <span className="nori-hint">A little help?</span><Nori/><span className="nori-chat-label">Ask Nori <span aria-hidden="true">✦</span></span>
    </button>
    {open && <section id="nori-chat-panel" className="nori-chat-panel" role="dialog" aria-modal="false" aria-labelledby="nori-chat-title" onKeyDown={e => { if (e.key === "Escape") { e.stopPropagation(); close(); } }}>
      <header className="nori-panel-header"><div><strong id="nori-chat-title">Ask Nori</strong><small>A little help, right here.</small></div><button type="button" onClick={reset}>New chat</button><button type="button" onClick={close} aria-label="Minimize Nori chat">×</button></header>
      <div ref={log} className="nori-panel-messages" role="log" aria-live="polite" aria-relevant="additions text">
        {messages.length === 0 && <div className="nori-panel-welcome"><Nori/><h2>Let’s make it click.</h2><p>Ask me about what you’re studying. Your page stays right here.</p><small>This chat stays here while you browse. Refreshing starts fresh.</small></div>}
        {messages.map((message, index) => <div key={index} className={`nori-panel-message ${message.role}`}><strong>{message.role === "user" ? "You" : "Nori"}</strong><p>{message.content}</p></div>)}
        {busy && <p role="status">Nori is thinking…</p>}
      </div>
      {error && <p className="nori-panel-error" role="alert">{error}</p>}
      <form className="nori-panel-form" onSubmit={e => { e.preventDefault(); void send(); }}>
        <label className="sr-only" htmlFor="nori-question">Your question for Nori</label>
        <textarea id="nori-question" ref={inputRef} value={input} maxLength={6000} onChange={e => setInput(e.target.value)} rows={2} placeholder="What would you like help with?" onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); void send(); } }}/>
        <button type="submit" disabled={busy || !input.trim()}>Send</button>
      </form>
      <small className="nori-panel-note">Study support, not medical advice. Check important facts.</small>
    </section>}
  </>;
}
