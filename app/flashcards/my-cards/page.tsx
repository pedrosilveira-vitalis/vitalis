"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import MainNav from "@/components/MainNav";

type Card = {
  id: number;
  section: string;
  front: string;
  back: string;
  created_at: string;
};

const SECTIONS = [
  { id: "bio-biochem", name: "Bio / Biochem", color: "#a8324a" },
  { id: "chem-phys", name: "Chem / Phys", color: "#2e4a6b" },
  { id: "psych-soc", name: "Psych / Soc", color: "#8a6b2e" },
  { id: "cars", name: "CARS", color: "#4a3b6b" },
];

export default function MyCardsPage() {
  const [cards, setCards] = useState<Card[]>([]);
  const [loading, setLoading] = useState(true);
  const [authed, setAuthed] = useState<boolean | null>(null);
  const [filterSection, setFilterSection] = useState<string>("all");
  const [showForm, setShowForm] = useState(false);
  const [newFront, setNewFront] = useState("");
  const [newBack, setNewBack] = useState("");
  const [newSection, setNewSection] = useState("bio-biochem");
  const [saving, setSaving] = useState(false);
  const [studyMode, setStudyMode] = useState(false);
  const [studyIdx, setStudyIdx] = useState(0);
  const [studyFlipped, setStudyFlipped] = useState(false);

  useEffect(() => { loadCards(); }, []);

  async function loadCards() {
    setLoading(true);
    try {
      const res = await fetch("/api/flashcards/custom");
      if (res.status === 401) {
        setAuthed(false);
        setLoading(false);
        return;
      }
      const data = await res.json();
      setCards(data.cards || []);
      setAuthed(true);
    } catch {}
    setLoading(false);
  }

  async function saveCard() {
    if (!newFront.trim() || !newBack.trim()) return;
    setSaving(true);
    try {
      const res = await fetch("/api/flashcards/custom", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ section: newSection, front: newFront.trim(), back: newBack.trim() }),
      });
      if (res.ok) {
        setNewFront(""); setNewBack(""); setShowForm(false);
        loadCards();
      }
    } catch {}
    setSaving(false);
  }

  async function deleteCard(id: number) {
    if (!confirm("Delete this card?")) return;
    try {
      await fetch(`/api/flashcards/custom/${id}`, { method: "DELETE" });
      setCards(cards.filter((c) => c.id !== id));
    } catch {}
  }

  const filteredCards = filterSection === "all" ? cards : cards.filter((c) => c.section === filterSection);

  if (authed === false) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e]">
        <MainNav active="flashcards" badge="My cards" />
        <div className="max-w-md mx-auto px-10 py-20 text-center">
          <h1 className="font-serif text-3xl font-medium mb-4">Sign in to save cards.</h1>
          <p className="text-sm opacity-70 mb-7">Custom flashcards are tied to your account so you can build a personal study deck across sessions.</p>
          <Link href="/sign-in" className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]">Sign in →</Link>
        </div>
      </div>
    );
  }

  if (studyMode) {
    if (filteredCards.length === 0) { setStudyMode(false); return null; }
    if (studyIdx >= filteredCards.length) {
      return (
        <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e]">
          <MainNav active="flashcards" badge="Done" />
          <div className="max-w-2xl mx-auto px-10 py-20 text-center">
            <h1 className="font-serif text-5xl font-medium mb-4">Deck complete.</h1>
            <button onClick={() => { setStudyMode(false); setStudyIdx(0); }} className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full">Back to my cards</button>
          </div>
        </div>
      );
    }
    const c = filteredCards[studyIdx];
    return (
      <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e]">
        <MainNav active="flashcards" badge={`${studyIdx + 1} / ${filteredCards.length}`} />
        <div className="max-w-3xl mx-auto px-10 py-10">
          <div onClick={() => setStudyFlipped(!studyFlipped)} className="min-h-[400px] p-14 border-2 border-[#0c1a2e15] rounded-3xl flex items-center justify-center text-center cursor-pointer hover:border-[#0c1a2e] transition-all bg-[#f5f1ea] mb-7">
            <div>
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-4">{studyFlipped ? "Back" : "Front"} · click to flip</div>
              <div className="font-serif text-[clamp(20px,2.6vw,28px)] leading-snug">{studyFlipped ? c.back : c.front}</div>
            </div>
          </div>
          <div className="flex gap-3 justify-center">
            <button onClick={() => { setStudyMode(false); }} className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full">Exit</button>
            <button onClick={() => { setStudyIdx(studyIdx + 1); setStudyFlipped(false); }} className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full">Next →</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e]">
      <MainNav active="flashcards" badge="My custom cards" />
      <section className="px-10 pt-10 pb-6 border-b border-[#0c1a2e15]">
        <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
          <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
          <Link href="/flashcards" className="opacity-70 hover:opacity-100">Flashcards</Link>
          <span className="opacity-40">/</span>
          <span>My custom cards</span>
        </div>
        <div className="flex items-end justify-between gap-4 flex-wrap">
          <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(40px,5vw,72px)]">
            My <span className="italic font-light text-[#a8324a]">cards.</span>
          </h1>
          <button onClick={() => setShowForm(true)} className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]">
            + New card
          </button>
        </div>
      </section>

      <section className="px-10 py-7 flex flex-wrap items-center gap-3">
        <button onClick={() => setFilterSection("all")} className={`font-mono text-xs uppercase tracking-[0.08em] px-4 py-2 rounded-full border ${filterSection === "all" ? "bg-[#0c1a2e] text-[#f5f1ea] border-[#0c1a2e]" : "border-[#0c1a2e25] hover:bg-[#0c1a2e0a]"}`}>
          All ({cards.length})
        </button>
        {SECTIONS.map((s) => {
          const count = cards.filter((c) => c.section === s.id).length;
          return (
            <button key={s.id} onClick={() => setFilterSection(s.id)} className={`font-mono text-xs uppercase tracking-[0.08em] px-4 py-2 rounded-full border ${filterSection === s.id ? "text-[#f5f1ea] border-transparent" : "border-[#0c1a2e25] hover:bg-[#0c1a2e0a]"}`} style={filterSection === s.id ? { backgroundColor: s.color } : {}}>
              {s.name} ({count})
            </button>
          );
        })}
        {filteredCards.length > 0 && (
          <button onClick={() => { setStudyIdx(0); setStudyFlipped(false); setStudyMode(true); }} className="ml-auto font-mono text-xs uppercase tracking-[0.08em] border-2 border-[#a8324a] text-[#a8324a] px-5 py-2 rounded-full hover:bg-[#a8324a] hover:text-[#f5f1ea]">
            Study {filteredCards.length} →
          </button>
        )}
      </section>

      {loading ? (
        <div className="px-10 py-20 text-center"><div className="font-mono text-[11px] uppercase opacity-60">Loading...</div></div>
      ) : filteredCards.length === 0 ? (
        <div className="px-10 py-20 text-center max-w-md mx-auto">
          <h2 className="font-serif text-2xl font-medium mb-3">No cards yet.</h2>
          <p className="text-sm opacity-65 mb-6">Make your first custom card — your weak spots, formulas to memorize, anything.</p>
          <button onClick={() => setShowForm(true)} className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full">+ Create a card</button>
        </div>
      ) : (
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 px-10 pb-12">
          {filteredCards.map((c) => {
            const sectionInfo = SECTIONS.find((s) => s.id === c.section);
            return (
              <div key={c.id} className="border border-[#0c1a2e15] rounded-2xl p-5 bg-[#f5f1ea] hover:border-[#0c1a2e30] transition-colors group">
                <div className="flex items-center justify-between mb-3">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55" style={{ color: sectionInfo?.color }}>
                    {sectionInfo?.name}
                  </div>
                  <button onClick={() => deleteCard(c.id)} className="opacity-0 group-hover:opacity-100 font-mono text-[10px] uppercase tracking-[0.1em] hover:text-[#a8324a]">Delete</button>
                </div>
                <div className="text-[14px] font-medium leading-relaxed mb-3 line-clamp-3">{c.front}</div>
                <div className="text-[12.5px] opacity-65 leading-relaxed line-clamp-3 pt-3 border-t border-[#0c1a2e15]">{c.back}</div>
              </div>
            );
          })}
        </section>
      )}

      {showForm && (
        <div className="fixed inset-0 bg-[#0c1a2e66] z-50 flex items-center justify-center p-6" onClick={() => setShowForm(false)}>
          <div className="bg-[#f5f1ea] rounded-2xl max-w-lg w-full p-7 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-3">New card</div>
            <h2 className="font-serif text-2xl font-medium mb-5">Create a card</h2>
            <div className="mb-4">
              <label className="block font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-2">Section</label>
              <div className="grid grid-cols-2 gap-2">
                {SECTIONS.map((s) => (
                  <button key={s.id} onClick={() => setNewSection(s.id)} className={`py-2 px-3 rounded-xl border-2 text-sm font-medium ${newSection === s.id ? "border-[#0c1a2e] bg-[#0c1a2e] text-[#f5f1ea]" : "border-[#0c1a2e25]"}`}>{s.name}</button>
                ))}
              </div>
            </div>
            <div className="mb-4">
              <label className="block font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-2">Front (question/prompt)</label>
              <textarea value={newFront} onChange={(e) => setNewFront(e.target.value)} rows={3} className="w-full px-3 py-2.5 border border-[#0c1a2e25] rounded-xl bg-[#f5f1ea] outline-none text-sm focus:border-[#0c1a2e] resize-none" />
            </div>
            <div className="mb-5">
              <label className="block font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-2">Back (answer)</label>
              <textarea value={newBack} onChange={(e) => setNewBack(e.target.value)} rows={4} className="w-full px-3 py-2.5 border border-[#0c1a2e25] rounded-xl bg-[#f5f1ea] outline-none text-sm focus:border-[#0c1a2e] resize-none" />
            </div>
            <div className="flex gap-3 justify-end">
              <button onClick={() => setShowForm(false)} className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a]">Cancel</button>
              <button onClick={saveCard} disabled={saving || !newFront.trim() || !newBack.trim()} className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a] disabled:opacity-30">
                {saving ? "Saving..." : "Save card"}
              </button>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        .line-clamp-3 { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
      `}</style>
    </div>
  );
}