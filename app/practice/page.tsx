"use client";

import { useState } from "react";
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
  {
    id: "bio-biochem",
    name: "Bio / Biochem",
    description: "Cells, organs, metabolism, molecular biology, biochemistry.",
    number: "01",
    accent: "#c54a2a",
  },
  {
    id: "chem-phys",
    name: "Chem / Phys",
    description: "General chemistry, organic, physics, biochemistry of physical systems.",
    number: "02",
    accent: "#3e5641",
  },
  {
    id: "psych-soc",
    name: "Psych / Soc",
    description: "Behavior, cognition, sociology, statistics, research methods.",
    number: "03",
    accent: "#d9a441",
  },
  {
    id: "cars",
    name: "CARS",
    description: "Critical analysis & reasoning skills — humanities & social science passages.",
    number: "04",
    accent: "#7a4b8c",
  },
  {
    id: "mixed",
    name: "Mixed Practice",
    description: "Random questions across all four sections — like real test day.",
    number: "05",
    accent: "#161410",
  },
];

export default function PracticePage() {
  const router = useRouter();
  const [selectedSection, setSelectedSection] = useState<Section | null>(null);

  function handleStart(format: "standalone" | "passage") {
    if (!selectedSection) return;
    router.push(`/practice/${selectedSection.id}?format=${format}`);
  }

  return (
    <div className="min-h-screen bg-[#f3efe7] text-[#161410] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[1000px] h-[500px] bg-[#d9a441] opacity-10 blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
      </div>

      <div className="relative z-10">
        {/* Nav */}
        <nav className="flex items-center justify-between px-10 py-5 border-b border-[#16141015]">
          <div className="flex items-center gap-3">
            <span className="w-2.5 h-2.5 rounded-full bg-[#c54a2a] shadow-[0_0_0_4px_#c54a2a22]" />
            <span className="font-serif font-semibold text-[22px] tracking-tight">Vitalis</span>
          </div>
          <div className="hidden md:flex gap-7 text-sm font-medium">
            <Link href="/" className="opacity-60 hover:opacity-100">Home</Link>
            <Link href="/tutor" className="opacity-60 hover:opacity-100">Tutor</Link>
            <Link href="/practice" className="opacity-100 border-b border-[#c54a2a] pb-0.5">Practice</Link>
            <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
          </div>
          <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">Practice · Beta</div>
        </nav>

        {/* Header */}
        <section className="px-10 pt-14 pb-8 border-b border-[#16141015]">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#161410] opacity-40" />
            Mode 04 · Practice questions
          </div>
          <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(48px,6vw,88px)] max-w-4xl">
            Pick a section. <span className="italic font-light text-[#c54a2a]">Get to work.</span>
          </h1>
          <p className="text-[15px] opacity-70 mt-4 max-w-xl leading-relaxed">
            MCAT-style questions in AAMC format. Get one wrong? Vitalis walks you through it — and you can ask follow-ups until it clicks.
          </p>
        </section>

        {/* Section boxes */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-[#16141015]">
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              onClick={() => setSelectedSection(s)}
              className="p-8 bg-[#f3efe7] hover:bg-[#1614100a] transition-colors text-left group min-h-[180px] flex flex-col gap-3"
            >
              <div className="flex items-center justify-between">
                <div className="font-mono text-[11px] tracking-[0.14em] opacity-50">{s.number}</div>
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: s.accent }} />
              </div>
              <div className="font-serif text-[28px] font-medium tracking-tight leading-tight">{s.name}</div>
              <div className="text-[13px] opacity-65 leading-relaxed">{s.description}</div>
              <div className="mt-auto font-mono text-[11px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100 transition-opacity">
                Start →
              </div>
            </button>
          ))}
        </section>

        {/* Disclaimer */}
        <div className="mx-10 my-7 p-3.5 px-5 border border-dashed border-[#16141025] rounded-lg font-mono text-[12px] leading-relaxed opacity-60">
          AI-generated MCAT-style questions designed to mirror AAMC format and difficulty. Not real exam questions. Always verify critical concepts with official AAMC materials.
        </div>
      </div>

      {/* Format chooser modal */}
      {selectedSection && (
        <div
          className="fixed inset-0 bg-[#16141099] z-50 flex items-center justify-center p-6"
          onClick={() => setSelectedSection(null)}
        >
          <div
            className="bg-[#f3efe7] rounded-2xl max-w-md w-full p-8 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-2">{selectedSection.number}</div>
            <h2 className="font-serif text-3xl font-medium tracking-tight mb-2">{selectedSection.name}</h2>
            <p className="text-[14px] opacity-70 mb-6">Choose your practice format:</p>

            <div className="space-y-3">
              <button
                onClick={() => handleStart("standalone")}
                disabled={selectedSection.id === "cars"}
                className="w-full p-4 border border-[#16141025] rounded-xl text-left hover:bg-[#1614100a] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                <div className="font-serif text-lg font-medium">Standalone questions</div>
                <div className="text-[13px] opacity-65 mt-1">One question at a time. Quick reps.</div>
                {selectedSection.id === "cars" && (
                  <div className="text-[11px] opacity-50 mt-2 font-mono">(CARS is always passage-based)</div>
                )}
              </button>

              <button
                onClick={() => handleStart("passage")}
                className="w-full p-4 border border-[#16141025] rounded-xl text-left hover:bg-[#1614100a] transition-colors"
              >
                <div className="font-serif text-lg font-medium">Passage-based</div>
                <div className="text-[13px] opacity-65 mt-1">Read a passage, then answer linked questions. Like the real test.</div>
              </button>
            </div>

            <button
              onClick={() => setSelectedSection(null)}
              className="mt-6 font-mono text-[10px] tracking-[0.1em] uppercase opacity-50 hover:opacity-100"
            >
              ← Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}