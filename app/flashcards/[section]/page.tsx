"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import MainNav from "@/components/MainNav";

type Card = { front: string; back: string };

const SECTION_NAMES: Record<string, string> = {
  "bio-biochem": "Bio / Biochem",
  "chem-phys": "Chem / Phys",
  "psych-soc": "Psych / Soc",
  "cars": "CARS",
};

const SECTION_COLORS: Record<string, string> = {
  "bio-biochem": "#a8324a",
  "chem-phys": "#2e4a6b",
  "psych-soc": "#8a6b2e",
  "cars": "#4a3b6b",
};

export default function FlashcardSession() {
  const params = useParams();
  const router = useRouter();
  const sectionId = (params.section as string) || "";
  const [cards, setCards] = useState<Card[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [knownCount, setKnownCount] = useState(0);
  const [reviewCount, setReviewCount] = useState(0);

  const accent = SECTION_COLORS[sectionId] || "#0c1a2e";
  const sectionName = SECTION_NAMES[sectionId] || sectionId;

  const loadCards = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/flashcards/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ section: sectionId, count: 20 }),
      });
      const data = await res.json();
      if (!data.cards || data.cards.length === 0) {
        setError("Couldn't load cards. Try again.");
        setLoading(false);
        return;
      }
      setCards(data.cards);
      setLoading(false);
    } catch {
      setError("Couldn't load cards. Try again.");
      setLoading(false);
    }
  }, [sectionId]);

  useEffect(() => {
    loadCards();
  }, [loadCards]);

  function handleKnown() {
    setKnownCount(knownCount + 1);
    handleNext();
  }
  function handleReview() {
    setReviewCount(reviewCount + 1);
    handleNext();
  }
  function handleNext() {
    if (currentIdx + 1 >= cards.length) {
      setCurrentIdx(cards.length);
      return;
    }
    setCurrentIdx(currentIdx + 1);
    setFlipped(false);
  }

  if (!SECTION_NAMES[sectionId]) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] flex items-center justify-center p-10">
        <div className="text-center max-w-md">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-50 mb-4">404</div>
          <h1 className="font-serif text-3xl font-medium mb-4">No such section.</h1>
          <Link href="/flashcards" className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full">← Back</Link>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] flex items-center justify-center">
        <div className="text-center">
          <div className="flex items-center justify-center gap-2 mb-3">
            <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" />
            <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.15s" }} />
            <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.3s" }} />
          </div>
          <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Generating {sectionName} cards...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] flex items-center justify-center p-10">
        <div className="text-center max-w-md">
          <h1 className="font-serif text-3xl font-medium mb-4">{error}</h1>
          <button onClick={loadCards} className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full">Try again</button>
        </div>
      </div>
    );
  }

  if (currentIdx >= cards.length) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e]">
        <MainNav active="flashcards" badge="Deck complete" />
        <div className="max-w-2xl mx-auto px-10 py-20 text-center">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4">Deck complete</div>
          <h1 className="font-serif text-[clamp(48px,6vw,88px)] font-medium tracking-tight mb-3" style={{ color: accent }}>
            {knownCount} / {cards.length}
          </h1>
          <p className="font-mono text-[14px] tracking-[0.1em] uppercase opacity-65 mb-10">cards known</p>
          <div className="flex gap-3 justify-center flex-wrap">
            <button onClick={() => { setCurrentIdx(0); setKnownCount(0); setReviewCount(0); setFlipped(false); loadCards(); }} className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]">
              New deck →
            </button>
            <button onClick={() => router.push("/flashcards")} className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a]">
              Pick another section
            </button>
          </div>
        </div>
      </div>
    );
  }

  const card = cards[currentIdx];

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e]">
      <MainNav active="flashcards" badge={`${currentIdx + 1} / ${cards.length}`} />
      <div className="max-w-3xl mx-auto px-10 py-10">
        <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-3 flex items-center gap-2">
          <Link href="/flashcards" className="hover:opacity-100 opacity-70">Flashcards</Link>
          <span className="opacity-40">/</span>
          <span style={{ color: accent }}>{sectionName}</span>
        </div>
        <div className="mb-6 flex items-center gap-3">
          <div className="flex-1 h-1.5 bg-[#0c1a2e15] rounded-full overflow-hidden">
            <div className="h-full transition-all" style={{ width: `${(currentIdx / cards.length) * 100}%`, backgroundColor: accent }} />
          </div>
          <div className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-55 flex-shrink-0">
            {currentIdx + 1} / {cards.length}
          </div>
        </div>

        <div
          onClick={() => setFlipped(!flipped)}
          className="min-h-[300px] md:min-h-[400px] p-10 md:p-14 border-2 border-[#0c1a2e15] rounded-3xl flex items-center justify-center text-center cursor-pointer hover:border-[#0c1a2e] transition-all bg-[#f5f1ea] mb-7"
        >
          <div>
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-4">
              {flipped ? "Back" : "Front"} · click to flip
            </div>
            <div className="font-serif text-[clamp(20px,2.6vw,28px)] leading-snug">
              {flipped ? card.back : card.front}
            </div>
          </div>
        </div>

        {flipped ? (
          <div className="flex gap-3 justify-center flex-wrap">
            <button onClick={handleReview} className="flex-1 md:flex-none font-mono text-xs uppercase tracking-[0.08em] border-2 border-[#a8324a] text-[#a8324a] px-7 py-3.5 rounded-full hover:bg-[#a8324a] hover:text-[#f5f1ea] transition-all">
              Review again
            </button>
            <button onClick={handleKnown} className="flex-1 md:flex-none font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-7 py-3.5 rounded-full hover:bg-[#1a2c4a]">
              Got it ✓
            </button>
          </div>
        ) : (
          <div className="text-center font-mono text-[11px] tracking-[0.12em] uppercase opacity-55">
            Click the card to reveal the back
          </div>
        )}
      </div>
    </div>
  );
}