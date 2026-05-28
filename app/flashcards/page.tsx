"use client";

import Link from "next/link";
import MainNav from "@/components/MainNav";

const SECTIONS = [
  {
    id: "bio-biochem",
    name: "Bio / Biochem",
    description: "Amino acids, enzymes, glycolysis, the works.",
    color: "#a8324a",
  },
  {
    id: "chem-phys",
    name: "Chem / Phys",
    description: "Functional groups, equations, key constants.",
    color: "#2e4a6b",
  },
  {
    id: "psych-soc",
    name: "Psych / Soc",
    description: "Theorists, disorders, social phenomena, stats.",
    color: "#8a6b2e",
  },
  {
    id: "cars",
    name: "CARS",
    description: "Reasoning patterns, question types, strategy reminders.",
    color: "#4a3b6b",
  },
];

export default function FlashcardsLanding() {
  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[1000px] h-[500px] bg-[#a8324a] opacity-[0.05] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
      </div>

      <div className="relative z-10">
        <MainNav active="flashcards" badge="Flashcards" />

        <section className="px-10 pt-14 pb-10 border-b border-[#0c1a2e15]">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Mode · Active recall
          </div>
          <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(48px,6vw,88px)] max-w-4xl">
            Build the <span className="italic font-light text-[#a8324a]">recall.</span>
          </h1>
          <p className="text-[15px] opacity-70 mt-4 max-w-2xl leading-relaxed">
            High-yield AI-generated decks across the four MCAT sections, plus your own custom cards.
          </p>
        </section>

        <section className="px-10 pt-10 pb-4">
          <div className="flex items-end justify-between flex-wrap gap-3">
            <div>
              <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-2">Pre-built decks</div>
              <h2 className="font-serif text-[28px] font-medium tracking-tight">Generated, high-yield cards.</h2>
            </div>
            <Link
              href="/flashcards/my-cards"
              className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a]"
            >
              My custom cards →
            </Link>
          </div>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 gap-px bg-[#0c1a2e15] mx-10 my-10 rounded-2xl overflow-hidden border border-[#0c1a2e15]">
          {SECTIONS.map((s) => (
            <Link
              key={s.id}
              href={`/flashcards/${s.id}`}
              className="p-7 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-3 group min-h-[200px]"
            >
              <div className="flex items-center justify-between">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">MCAT Section</div>
                <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: s.color }} />
              </div>
              <div className="font-serif text-[26px] font-medium tracking-tight leading-tight" style={{ color: s.color }}>
                {s.name}
              </div>
              <div className="text-[13px] opacity-70 leading-relaxed">{s.description}</div>
              <div className="mt-auto pt-2 font-mono text-[10px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100 transition-opacity">
                Start deck →
              </div>
            </Link>
          ))}
        </section>

        <div className="mx-10 my-7 p-3.5 px-5 border border-dashed border-[#0c1a2e25] rounded-lg font-mono text-[12px] leading-relaxed opacity-60">
          Flashcards are generated fresh each session and aren&apos;t a substitute for active reading and practice questions. Use them between sessions to reinforce recall.
        </div>
      </div>
    </div>
  );
}