"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

type Conversation = {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
  first_message: string | null;
  message_count: string | number;
};

function Logo() {
  return (
    <div className="flex items-center gap-2.5">
      <svg width="36" height="20" viewBox="0 0 60 28" fill="none" className="flex-shrink-0">
        <path d="M2 14 L12 14 L16 6 L22 22 L28 4 L34 18 L38 14 L48 14" stroke="#a8324a" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" fill="none" />
        <circle cx="50" cy="14" r="2.2" fill="#a8324a" />
      </svg>
      <span className="font-serif font-semibold text-[22px] tracking-tight text-[#0c1a2e]">Vitalis</span>
    </div>
  );
}

function formatRelativeDate(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  const diffHr = Math.floor(diffMs / 3600000);
  const diffDay = Math.floor(diffMs / 86400000);

  if (diffMin < 1) return "just now";
  if (diffMin < 60) return `${diffMin}m ago`;
  if (diffHr < 24) return `${diffHr}h ago`;
  if (diffDay < 7) return `${diffDay}d ago`;
  if (diffDay < 30) return `${Math.floor(diffDay / 7)}w ago`;
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadConversations();
  }, []);

  async function loadConversations() {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/conversations");
      if (res.status === 401) {
        setError("Please sign in to view your past conversations.");
        setLoading(false);
        return;
      }
      const data = await res.json();
      setConversations(data.conversations || []);
    } catch {
      setError("Couldn't load your conversations. Try again?");
    }
    setLoading(false);
  }

  async function handleDelete(id: number, title: string) {
    if (!confirm(`Delete "${title}"?`)) return;
    try {
      const res = await fetch(`/api/conversations/${id}`, { method: "DELETE" });
      if (res.ok) {
        setConversations(conversations.filter((c) => c.id !== id));
      } else {
        alert("Couldn't delete the conversation.");
      }
    } catch {
      alert("Connection issue.");
    }
  }

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans">
      <header className="flex items-center justify-between px-8 py-4 border-b border-[#0c1a2e15] sticky top-0 bg-[#f5f1ea] z-30">
        <Logo />
        <div className="hidden md:flex gap-6 text-sm font-medium">
          <Link href="/" className="opacity-60 hover:opacity-100">Home</Link>
          <Link href="/tutor" className="opacity-100 border-b border-[#a8324a] pb-0.5">Tutor</Link>
          <Link href="/practice" className="opacity-60 hover:opacity-100">Practice</Link>
          <Link href="/flashcards" className="opacity-60 hover:opacity-100">Flashcards</Link>
          <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
          <Link href="/score-calculator" className="opacity-60 hover:opacity-100">Score Calc</Link>
        </div>
        <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">Past Chats</div>
      </header>

      <section className="px-10 pt-10 pb-6 border-b border-[#0c1a2e15]">
        <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
          <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
          Tutor history
        </div>
        <div className="flex items-end justify-between gap-6 flex-wrap">
          <div>
            <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(40px,5vw,72px)]">
              Past <span className="italic font-light text-[#a8324a]">conversations.</span>
            </h1>
            <p className="text-[14px] opacity-70 mt-3 max-w-xl">
              Pick up where you left off. Conversations save automatically when you&apos;re signed in.
            </p>
          </div>
          <Link
            href="/tutor"
            className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]"
          >
            + New chat
          </Link>
        </div>
      </section>

      <section className="px-10 py-10 max-w-4xl">
        {loading && (
          <div className="text-center py-12">
            <div className="flex items-center justify-center gap-2 mb-3">
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" />
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.15s" }} />
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.3s" }} />
            </div>
            <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Loading...</div>
          </div>
        )}

        {!loading && error && (
          <div className="text-center py-12 max-w-md mx-auto">
            <div className="text-[#a8324a] text-sm mb-4">{error}</div>
            <Link
              href="/sign-in"
              className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a] inline-block"
            >
              Sign in →
            </Link>
          </div>
        )}

        {!loading && !error && conversations.length === 0 && (
          <div className="text-center py-16 max-w-md mx-auto">
            <h2 className="font-serif text-2xl font-medium mb-3">No past conversations yet.</h2>
            <p className="text-[14px] opacity-65 mb-6">
              Start chatting with the tutor and your conversations will appear here.
            </p>
            <Link
              href="/tutor"
              className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a] inline-block"
            >
              Start a chat →
            </Link>
          </div>
        )}

        {!loading && !error && conversations.length > 0 && (
          <div className="space-y-3">
            {conversations.map((conv) => (
              <div
                key={conv.id}
                className="group border border-[#0c1a2e15] rounded-2xl p-5 bg-[#f5f1ea] hover:border-[#0c1a2e30] hover:bg-[#0c1a2e04] transition-all flex items-start gap-4"
              >
                <Link
                  href={`/tutor?c=${conv.id}`}
                  className="flex-1 min-w-0"
                >
                  <div className="font-serif text-[17px] font-medium mb-1.5 leading-snug truncate">
                    {conv.title}
                  </div>
                  {conv.first_message && (
                    <div className="text-[13px] opacity-65 leading-relaxed line-clamp-2 mb-2">
                      {conv.first_message}
                    </div>
                  )}
                  <div className="flex items-center gap-3 font-mono text-[10px] tracking-[0.1em] uppercase opacity-50">
                    <span>{formatRelativeDate(conv.updated_at)}</span>
                    <span>·</span>
                    <span>{conv.message_count} messages</span>
                  </div>
                </Link>
                <button
                  onClick={() => handleDelete(conv.id, conv.title)}
                  className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-30 hover:opacity-100 hover:text-[#a8324a] transition-opacity flex-shrink-0"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </section>

      <style jsx>{`
        .line-clamp-2 {
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }
      `}</style>
    </div>
  );
}