"use client";

import { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

type Flashcard = {
  id: string;
  front: string;
  back: string;
  concept: string;
  difficulty: string;
};

type DeckPhase = "loading" | "studying" | "summary" | "error";

const SECTION_NAMES: Record<string, string> = {
  "bio-biochem": "Bio / Biochem",
  "chem-phys": "Chem / Phys",
  "psych-soc": "Psych / Soc",
  "cars": "CARS",
  "mixed": "Mixed Review",
};

function Logo() {
  return (
    <div className="flex items-center gap-2.5">
      <svg width="32" height="18" viewBox="0 0 60 28" fill="none" className="flex-shrink-0">
        <path d="M2 14 L12 14 L16 6 L22 22 L28 4 L34 18 L38 14 L48 14" stroke="#a8324a" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" fill="none" />
        <circle cx="50" cy="14" r="2.2" fill="#a8324a" />
      </svg>
      <span className="font-serif font-semibold text-xl tracking-tight text-[#0c1a2e]">Vitalis</span>
    </div>
  );
}

function formatBack(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(/\n/g, "<br/>");
}

export default function FlashcardSessionPage() {
  const params = useParams();
  const section = (params.section as string) || "mixed";

  const [phase, setPhase] = useState<DeckPhase>("loading");
  const [deck, setDeck] = useState<Flashcard[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [knownIds, setKnownIds] = useState<Set<string>>(new Set());
  const [unknownIds, setUnknownIds] = useState<Set<string>>(new Set());
  const [reviewMode, setReviewMode] = useState(false);

  const loadDeck = useCallback(async () => {
    setPhase("loading");
    setKnownIds(new Set());
    setUnknownIds(new Set());
    setCurrentIdx(0);
    setFlipped(false);
    setReviewMode(false);
    try {
      const res = await fetch("/api/flashcards/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ section }),
      });
      const data = await res.json();
      if (data.deck && data.deck.length > 0) {
        setDeck(data.deck);
        setPhase("studying");
      } else {
        setPhase("error");
      }
    } catch {
      setPhase("error");
    }
  }, [section]);

  useEffect(() => {
    loadDeck();
  }, [loadDeck]);

  function handleKnown() {
    if (!deck[currentIdx]) return;
    const id = deck[currentIdx].id;
    setKnownIds((s) => new Set([...s, id]));
    advanceCard();
  }

  function handleUnknown() {
    if (!deck[currentIdx]) return;
    const id = deck[currentIdx].id;
    setUnknownIds((s) => new Set([...s, id]));
    advanceCard();
  }

  function advanceCard() {
    setFlipped(false);
    if (currentIdx < deck.length - 1) {
      setTimeout(() => setCurrentIdx(currentIdx + 1), 200);
    } else {
      setTimeout(() => setPhase("summary"), 200);
    }
  }

  function reviewMissed() {
    const missed = deck.filter((c) => unknownIds.has(c.id));
    if (missed.length === 0) return;
    setDeck(missed);
    setCurrentIdx(0);
    setFlipped(false);
    setKnownIds(new Set());
    setUnknownIds(new Set());
    setReviewMode(true);
    setPhase("studying");
  }

  const current = deck[currentIdx];
  const progress = deck.length > 0 ? ((currentIdx + (flipped ? 0.5 : 0)) / deck.length) * 100 : 0;
  const knownCount = knownIds.size;
  const unknownCount = unknownIds.size;
  const accuracy = deck.length > 0 ? Math.round((knownCount / deck.length) * 100) : 0;

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans flex flex-col">
      <header className="flex items-center justify-between px-8 py-4 border-b border-[#0c1a2e15] sticky top-0 bg-[#f5f1ea] z-30">
        <Logo />
        <div className="hidden md:flex gap-6 text-sm font-medium">
          <Link href="/" className="opacity-60 hover:opacity-100">Home</Link>
          <Link href="/tutor" className="opacity-60 hover:opacity-100">Tutor</Link>
          <Link href="/practice" className="opacity-60 hover:opacity-100">Practice</Link>
          <Link href="/flashcards" className="opacity-100 border-b border-[#a8324a] pb-0.5">Flashcards</Link>
          <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
          <Link href="/score-calculator" className="opacity-60 hover:opacity-100">Score Calc</Link>
        </div>
        <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">
          {SECTION_NAMES[section] || section}{reviewMode ? " · review" : ""}
        </div>
      </header>

      {/* Progress bar */}
      {phase === "studying" && deck.length > 0 && (
        <div className="px-8 py-3 border-b border-[#0c1a2e15] flex items-center gap-4">
          <div className="flex-1 h-1.5 bg-[#0c1a2e15] rounded-full overflow-hidden">
            <div
              className="h-full bg-[#a8324a] transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
          <div className="font-mono text-[11px] uppercase tracking-[0.1em] opacity-60">
            {currentIdx + 1} / {deck.length}
          </div>
          <Link
            href="/flashcards"
            className="text-[10px] tracking-[0.1em] uppercase opacity-60 hover:opacity-100 px-2 py-1 border border-[#0c1a2e25] rounded"
          >
            ← Exit
          </Link>
        </div>
      )}

      {/* Loading */}
      {phase === "loading" && (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-3">
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" />
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.15s" }} />
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.3s" }} />
            </div>
            <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Generating your deck...</div>
          </div>
        </div>
      )}

      {/* Error */}
      {phase === "error" && (
        <div className="flex-1 flex items-center justify-center px-8">
          <div className="text-center max-w-md">
            <div className="text-[#a8324a] text-sm mb-4">Couldn&apos;t generate a deck. Try again?</div>
            <button
              onClick={loadDeck}
              className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]"
            >
              Try again
            </button>
          </div>
        </div>
      )}

      {/* Studying */}
      {phase === "studying" && current && (
        <div className="flex-1 flex flex-col items-center justify-center px-8 py-8">
          <div
            onClick={() => setFlipped(!flipped)}
            className="w-full max-w-2xl cursor-pointer perspective"
            style={{ perspective: "1200px" }}
          >
            <div
              className="relative w-full transition-transform duration-500"
              style={{
                transformStyle: "preserve-3d",
                transform: flipped ? "rotateY(180deg)" : "rotateY(0deg)",
                minHeight: "320px",
              }}
            >
              {/* Front */}
              <div
                className="absolute inset-0 rounded-3xl bg-[#f5f1ea] border-2 border-[#0c1a2e15] flex flex-col p-10 shadow-sm"
                style={{ backfaceVisibility: "hidden" }}
              >
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-3 flex items-center justify-between">
                  <span>Card {currentIdx + 1} · {current.difficulty}</span>
                  <span className="opacity-40">{current.concept}</span>
                </div>
                <div className="flex-1 flex items-center justify-center text-center">
                  <p className="font-serif text-[24px] md:text-[28px] font-medium leading-[1.3] tracking-tight">
                    {current.front}
                  </p>
                </div>
                <div className="text-center font-mono text-[10px] tracking-[0.14em] uppercase opacity-40 mt-3">
                  Click to flip →
                </div>
              </div>

              {/* Back */}
              <div
                className="absolute inset-0 rounded-3xl bg-[#0c1a2e] text-[#f5f1ea] border-2 border-[#0c1a2e] flex flex-col p-10 shadow-sm"
                style={{ backfaceVisibility: "hidden", transform: "rotateY(180deg)" }}
              >
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-3">
                  Answer
                </div>
                <div className="flex-1 flex items-center justify-center text-center overflow-y-auto">
                  <div
                    className="text-[16px] md:text-[18px] leading-relaxed"
                    dangerouslySetInnerHTML={{ __html: formatBack(current.back) }}
                  />
                </div>
                <div className="text-center font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mt-3">
                  ← Click to flip back
                </div>
              </div>
            </div>
          </div>

          {/* Action buttons (only shown when flipped) */}
          <div className={`mt-7 flex gap-4 transition-opacity duration-300 ${flipped ? "opacity-100" : "opacity-0 pointer-events-none"}`}>
            <button
              onClick={handleUnknown}
              className="flex items-center gap-2 font-mono text-xs uppercase tracking-[0.08em] border-2 border-[#a8324a] text-[#a8324a] px-5 py-3 rounded-full hover:bg-[#a8324a15]"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
              Didn&apos;t get it
            </button>
            <button
              onClick={handleKnown}
              className="flex items-center gap-2 font-mono text-xs uppercase tracking-[0.08em] bg-[#3e6b4a] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#2e5638]"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              Got it
            </button>
          </div>

          {!flipped && (
            <div className="mt-7 font-mono text-[10px] tracking-[0.1em] uppercase opacity-40">
              Read the prompt → click the card to see the answer
            </div>
          )}
        </div>
      )}

      {/* Summary */}
      {phase === "summary" && (
        <div className="flex-1 flex items-center justify-center px-8 py-12">
          <div className="max-w-xl w-full text-center">
            <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4">Deck complete</div>
            <h2 className="font-serif text-4xl font-medium tracking-tight mb-6">
              {accuracy >= 80 ? "Strong work." : accuracy >= 50 ? "Solid pass." : "Worth another round."}
            </h2>

            <div className="grid grid-cols-3 gap-4 mb-8">
              <div className="border-2 border-[#3e6b4a40] bg-[#3e6b4a15] rounded-2xl p-5">
                <div className="font-serif text-3xl font-medium text-[#3e6b4a]">{knownCount}</div>
                <div className="font-mono text-[10px] uppercase tracking-[0.12em] opacity-60 mt-1">Got it</div>
              </div>
              <div className="border-2 border-[#a8324a40] bg-[#a8324a15] rounded-2xl p-5">
                <div className="font-serif text-3xl font-medium text-[#a8324a]">{unknownCount}</div>
                <div className="font-mono text-[10px] uppercase tracking-[0.12em] opacity-60 mt-1">Missed</div>
              </div>
              <div className="border-2 border-[#0c1a2e25] rounded-2xl p-5">
                <div className="font-serif text-3xl font-medium">{accuracy}%</div>
                <div className="font-mono text-[10px] uppercase tracking-[0.12em] opacity-60 mt-1">Accuracy</div>
              </div>
            </div>

            <div className="flex gap-3 justify-center flex-wrap">
              {unknownCount > 0 && (
                <button
                  onClick={reviewMissed}
                  className="font-mono text-xs uppercase tracking-[0.08em] bg-[#a8324a] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#8a283c]"
                >
                  Review missed ({unknownCount})
                </button>
              )}
              <button
                onClick={loadDeck}
                className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]"
              >
                New deck
              </button>
              <Link
                href="/flashcards"
                className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a]"
              >
                Change section
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}