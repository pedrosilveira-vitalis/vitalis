"use client";

import { useState, useEffect, useCallback } from "react";
import Link from "next/link";

type CustomCard = {
  id: number;
  section: string;
  front: string;
  back: string;
  concept: string | null;
  difficulty: string;
  created_at: string;
};

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

export default function MyCardsPage() {
  const [cards, setCards] = useState<CustomCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [sectionFilter, setSectionFilter] = useState("all");

  // Create card modal state
  const [showCreate, setShowCreate] = useState(false);
  const [newSection, setNewSection] = useState("bio-biochem");
  const [newFront, setNewFront] = useState("");
  const [newBack, setNewBack] = useState("");
  const [newConcept, setNewConcept] = useState("");
  const [saving, setSaving] = useState(false);

  const loadCards = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const url = sectionFilter === "all"
        ? "/api/flashcards/custom"
        : `/api/flashcards/custom?section=${sectionFilter}`;
      const res = await fetch(url);
      if (res.status === 401) {
        setError("Please sign in to view your custom cards.");
        setLoading(false);
        return;
      }
      const data = await res.json();
      setCards(data.cards || []);
    } catch {
      setError("Couldn't load your cards. Try again?");
    }
    setLoading(false);
  }, [sectionFilter]);

  useEffect(() => {
    loadCards();
  }, [loadCards]);

  async function handleCreate() {
    if (!newFront.trim() || !newBack.trim()) return;
    setSaving(true);
    try {
      const res = await fetch("/api/flashcards/custom", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          section: newSection,
          front: newFront.trim(),
          back: newBack.trim(),
          concept: newConcept.trim() || null,
          difficulty: "medium",
        }),
      });
      if (res.ok) {
        setShowCreate(false);
        setNewFront("");
        setNewBack("");
        setNewConcept("");
        loadCards();
      } else {
        const data = await res.json();
        alert(data.error || "Couldn't save the card.");
      }
    } catch {
      alert("Connection issue. Try again?");
    }
    setSaving(false);
  }

  async function handleDelete(id: number) {
    if (!confirm("Delete this card?")) return;
    try {
      const res = await fetch(`/api/flashcards/custom/${id}`, { method: "DELETE" });
      if (res.ok) {
        setCards(cards.filter((c) => c.id !== id));
      } else {
        alert("Couldn't delete the card.");
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
          <Link href="/tutor" className="opacity-60 hover:opacity-100">Tutor</Link>
          <Link href="/practice" className="opacity-60 hover:opacity-100">Practice</Link>
          <Link href="/flashcards" className="opacity-100 border-b border-[#a8324a] pb-0.5">Flashcards</Link>
          <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
          <Link href="/score-calculator" className="opacity-60 hover:opacity-100">Score Calc</Link>
        </div>
        <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">My Cards</div>
      </header>

      <section className="px-10 pt-10 pb-6 border-b border-[#0c1a2e15]">
        <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
          <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
          Your custom flashcards
        </div>
        <div className="flex items-end justify-between gap-6 flex-wrap">
          <div>
            <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(40px,5vw,72px)]">
              My <span className="italic font-light text-[#a8324a]">cards.</span>
            </h1>
            <p className="text-[14px] opacity-70 mt-3 max-w-xl">
              Cards you&apos;ve made. Build a personal deck of the things you keep getting wrong.
            </p>
          </div>
          <button
            onClick={() => setShowCreate(true)}
            className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]"
          >
            + Create card
          </button>
        </div>
      </section>

      {/* Filter */}
      <section className="px-10 py-4 border-b border-[#0c1a2e15] flex items-center gap-3 flex-wrap font-mono text-[11px] uppercase tracking-[0.1em]">
        <span className="opacity-50">Filter:</span>
        {["all", "bio-biochem", "chem-phys", "psych-soc", "cars"].map((s) => (
          <button
            key={s}
            onClick={() => setSectionFilter(s)}
            className={`px-3 py-1.5 border rounded-full transition-colors ${
              sectionFilter === s
                ? "bg-[#0c1a2e] text-[#f5f1ea] border-[#0c1a2e]"
                : "border-[#0c1a2e25] hover:bg-[#0c1a2e08]"
            }`}
          >
            {s === "all" ? "All" : SECTION_NAMES[s]}
          </button>
        ))}
      </section>

      {/* Content */}
      <section className="px-10 py-10">
        {loading && (
          <div className="text-center py-12">
            <div className="flex items-center justify-center gap-2 mb-3">
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" />
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.15s" }} />
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.3s" }} />
            </div>
            <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Loading your cards...</div>
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

        {!loading && !error && cards.length === 0 && (
          <div className="text-center py-16 max-w-md mx-auto">
            <h2 className="font-serif text-2xl font-medium mb-3">No custom cards yet.</h2>
            <p className="text-[14px] opacity-65 mb-6">Click &quot;Create card&quot; to add your first one.</p>
          </div>
        )}

        {!loading && !error && cards.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-w-6xl">
            {cards.map((card) => (
              <div
                key={card.id}
                className="border border-[#0c1a2e15] rounded-2xl p-6 bg-[#f5f1ea] hover:border-[#0c1a2e30] transition-colors flex flex-col gap-3"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: SECTION_COLORS[card.section] || "#0c1a2e" }} />
                    <span className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60">
                      {SECTION_NAMES[card.section] || card.section}
                    </span>
                  </div>
                  <button
                    onClick={() => handleDelete(card.id)}
                    className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-40 hover:opacity-100 hover:text-[#a8324a]"
                  >
                    Delete
                  </button>
                </div>
                <div className="font-serif text-[18px] font-medium leading-snug">{card.front}</div>
                <div className="text-[13px] opacity-75 leading-relaxed border-t border-[#0c1a2e15] pt-3">{card.back}</div>
                {card.concept && (
                  <div className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-50 mt-1">
                    {card.concept}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Create Card Modal */}
      {showCreate && (
        <div
          className="fixed inset-0 bg-[#0c1a2e99] z-50 flex items-center justify-center p-6"
          onClick={() => setShowCreate(false)}
        >
          <div
            className="bg-[#f5f1ea] rounded-2xl max-w-lg w-full p-8 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="font-serif text-3xl font-medium tracking-tight mb-1">Create a card</h2>
            <p className="text-[13px] opacity-65 mb-6">Add something you want to remember.</p>

            <div className="space-y-4">
              <div>
                <label className="block font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-1.5">Section</label>
                <select
                  value={newSection}
                  onChange={(e) => setNewSection(e.target.value)}
                  className="w-full px-3 py-2.5 border border-[#0c1a2e25] rounded-xl bg-[#f5f1ea] outline-none text-[14px] focus:border-[#0c1a2e]"
                >
                  <option value="bio-biochem">Bio / Biochem</option>
                  <option value="chem-phys">Chem / Phys</option>
                  <option value="psych-soc">Psych / Soc</option>
                  <option value="cars">CARS</option>
                </select>
              </div>

              <div>
                <label className="block font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-1.5">Front (the prompt)</label>
                <textarea
                  value={newFront}
                  onChange={(e) => setNewFront(e.target.value)}
                  placeholder="e.g., What is the resting membrane potential of a neuron?"
                  rows={2}
                  className="w-full px-3 py-2.5 border border-[#0c1a2e25] rounded-xl bg-[#f5f1ea] outline-none text-[14px] focus:border-[#0c1a2e] resize-none"
                />
              </div>

              <div>
                <label className="block font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-1.5">Back (the answer)</label>
                <textarea
                  value={newBack}
                  onChange={(e) => setNewBack(e.target.value)}
                  placeholder="e.g., About -70 mV, maintained by leak K+ channels and the Na+/K+ ATPase pump."
                  rows={4}
                  className="w-full px-3 py-2.5 border border-[#0c1a2e25] rounded-xl bg-[#f5f1ea] outline-none text-[14px] focus:border-[#0c1a2e] resize-none"
                />
              </div>

              <div>
                <label className="block font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-1.5">Concept (optional)</label>
                <input
                  value={newConcept}
                  onChange={(e) => setNewConcept(e.target.value)}
                  placeholder="e.g., resting membrane potential"
                  className="w-full px-3 py-2.5 border border-[#0c1a2e25] rounded-xl bg-[#f5f1ea] outline-none text-[14px] focus:border-[#0c1a2e]"
                />
              </div>
            </div>

            <div className="mt-7 flex gap-3 justify-end">
              <button
                onClick={() => setShowCreate(false)}
                className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a]"
              >
                Cancel
              </button>
              <button
                onClick={handleCreate}
                disabled={!newFront.trim() || !newBack.trim() || saving}
                className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a] disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {saving ? "Saving..." : "Save card"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}