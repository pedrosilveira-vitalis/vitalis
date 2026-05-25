"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

type Section = {
  id: string;
  name: string;
  description: string;
  number: string;
  accent: string;
};

const SECTIONS: Section[] = [
  { id: "bio-biochem", name: "Bio / Biochem", description: "Amino acids, metabolism, genetics, organ systems, immunology.", number: "01", accent: "#a8324a" },
  { id: "chem-phys", name: "Chem / Phys", description: "Acid-base, thermodynamics, organic, physics, electricity.", number: "02", accent: "#2e4a6b" },
  { id: "psych-soc", name: "Psych / Soc", description: "Conditioning, memory, theories, sociology, statistics.", number: "03", accent: "#8a6b2e" },
  { id: "cars", name: "CARS", description: "Critical analysis, reading strategy, question types.", number: "04", accent: "#4a3b6b" },
  { id: "mixed", name: "Mixed Review", description: "High-yield cards from every section in one mixed deck.", number: "05", accent: "#0c1a2e" },
];

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

export default function FlashcardsLandingPage() {
  const router = useRouter();

  function startDeck(sectionId: string) {
    router.push(`/flashcards/${sectionId}`);
  }

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[1000px] h-[500px] bg-[#a8324a] opacity-[0.05] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
      </div>

      <div className="relative z-10">
        <nav className="flex items-center justify-between px-10 py-5 border-b border-[#0c1a2e15]">
          <Logo />
          <div className="hidden md:flex gap-6 text-sm font-medium">
            <Link href="/" className="opacity-60 hover:opacity-100">Home</Link>
            <Link href="/tutor" className="opacity-60 hover:opacity-100">Tutor</Link>
            <Link href="/practice" className="opacity-60 hover:opacity-100">Practice</Link>
            <Link href="/flashcards" className="opacity-100 border-b border-[#a8324a] pb-0.5">Flashcards</Link>
            <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
            <Link href="/score-calculator" className="opacity-60 hover:opacity-100">Score Calc</Link>
          </div>
          <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">Flashcards · Beta</div>
        </nav>

        <section className="px-10 pt-14 pb-8 border-b border-[#0c1a2e15]">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Mode · Flashcards
          </div>
          <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(48px,6vw,88px)] max-w-4xl">
            Memorize <span className="italic font-light text-[#a8324a]">high-yield.</span>
          </h1>
          <p className="text-[15px] opacity-70 mt-4 max-w-xl leading-relaxed">
            Quick decks of MCAT-high-yield flashcards. Flip to check. Mark what stuck and what didn&apos;t. Build the recall muscle.
          </p>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-[#0c1a2e15]">
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              onClick={() => startDeck(s.id)}
              className="p-8 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors text-left group min-h-[180px] flex flex-col gap-3"
            >
              <div className="flex items-center justify-between">
                <div className="font-mono text-[11px] tracking-[0.14em] opacity-50">{s.number}</div>
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: s.accent }} />
              </div>
              <div className="font-serif text-[28px] font-medium tracking-tight leading-tight">{s.name}</div>
              <div className="text-[13px] opacity-65 leading-relaxed">{s.description}</div>
              <div className="mt-auto font-mono text-[11px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100 transition-opacity">
                Start deck →
              </div>
            </button>
          ))}
        </section>

        <div className="mx-10 my-7 p-3.5 px-5 border border-dashed border-[#0c1a2e25] rounded-lg font-mono text-[12px] leading-relaxed opacity-60">
          AI-generated flashcards focused on high-yield MCAT content. Always verify critical concepts with official AAMC materials.
        </div>
      </div>
    </div>
  );
}