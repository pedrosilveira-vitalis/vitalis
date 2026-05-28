"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import MainNav from "@/components/MainNav";

type Section = {
  id: string;
  name: string;
  fullName: string;
  description: string;
  color: string;
  topics: string[];
};

const SECTIONS: Section[] = [
  {
    id: "bio-biochem",
    name: "Bio / Biochem",
    fullName: "Biological and Biochemical Foundations of Living Systems",
    description: "Cells, organs, biochemistry, genetics, physiology. The largest content section.",
    color: "#a8324a",
    topics: ["Biochemistry", "Cell biology", "Genetics", "Physiology", "Molecular biology"],
  },
  {
    id: "chem-phys",
    name: "Chem / Phys",
    fullName: "Chemical and Physical Foundations of Biological Systems",
    description: "General chemistry, organic, physics. Quantitative reasoning heavy.",
    color: "#2e4a6b",
    topics: ["General chem", "Organic chem", "Physics", "Biochemistry"],
  },
  {
    id: "psych-soc",
    name: "Psych / Soc",
    fullName: "Psychological, Social, and Biological Foundations of Behavior",
    description: "Behavior, cognition, sociology, research methods, statistics.",
    color: "#8a6b2e",
    topics: ["Psychology", "Sociology", "Research methods", "Statistics"],
  },
  {
    id: "cars",
    name: "CARS",
    fullName: "Critical Analysis and Reasoning Skills",
    description: "Critical analysis and reading. Less about content, more about strategy.",
    color: "#4a3b6b",
    topics: ["Humanities passages", "Social science passages", "Reasoning skills"],
  },
  {
    id: "mixed",
    name: "Mixed",
    fullName: "Mixed practice across all four sections",
    description: "Random pull from all four sections. Simulates real test variety.",
    color: "#0c1a2e",
    topics: ["All four MCAT sections combined"],
  },
];

function SectionCard({ section, onClick }: { section: Section; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="text-left p-7 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-3 group min-h-[240px]"
    >
      <div className="flex items-center justify-between">
        <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">
          {section.id === "mixed" ? "Mixed mode" : "MCAT Section"}
        </div>
        <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: section.color }} />
      </div>
      <div className="font-serif text-[26px] font-medium tracking-tight leading-tight" style={{ color: section.color }}>
        {section.name}
      </div>
      <div className="text-[13px] opacity-70 leading-relaxed">{section.description}</div>
      <div className="mt-auto pt-2 font-mono text-[10px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100 transition-opacity">
        Start practicing →
      </div>
    </button>
  );
}

export default function PracticeLanding() {
  const router = useRouter();
  const [activeSection, setActiveSection] = useState<Section | null>(null);
  const [numQuestions, setNumQuestions] = useState(10);
  const [difficulty, setDifficulty] = useState<"mixed" | "easy" | "medium" | "hard">("mixed");

  function startSession() {
    if (!activeSection) return;
    const params = new URLSearchParams({
      n: numQuestions.toString(),
      d: difficulty,
    });
    router.push(`/practice/${activeSection.id}?${params}`);
  }

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[1000px] h-[500px] bg-[#a8324a] opacity-[0.05] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
      </div>

      <div className="relative z-10">
        <MainNav active="practice" badge="Practice Sets" />

        <section className="px-10 pt-14 pb-10 border-b border-[#0c1a2e15]">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Mode · Practice questions
          </div>
          <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(48px,6vw,88px)] max-w-4xl">
            Build the <span className="italic font-light text-[#a8324a]">instincts.</span>
          </h1>
          <p className="text-[15px] opacity-70 mt-4 max-w-2xl leading-relaxed">
            AAMC-style multiple choice with on-the-fly explanations. Tag a wrong answer to your tutor to dig deeper.
          </p>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-[#0c1a2e15] mx-10 my-10 rounded-2xl overflow-hidden border border-[#0c1a2e15]">
          {SECTIONS.map((s) => (
            <SectionCard key={s.id} section={s} onClick={() => setActiveSection(s)} />
          ))}
        </section>

        <div className="mx-10 my-7 p-3.5 px-5 border border-dashed border-[#0c1a2e25] rounded-lg font-mono text-[12px] leading-relaxed opacity-60">
          Practice questions are AI-generated and reviewed for AAMC-style fidelity. Always cross-reference with official AAMC materials for highest accuracy.
        </div>

        <div className="px-10 py-6 flex justify-between items-center text-[12px] opacity-60">
          <div>5 sections · Mixed-mode included</div>
          <Link href="/tutor" className="hover:opacity-100 underline decoration-[#a8324a] decoration-2 underline-offset-4">
            Or ask the tutor →
          </Link>
        </div>
      </div>

      {/* Configure modal */}
      {activeSection && (
        <div className="fixed inset-0 bg-[#0c1a2e66] z-50 flex items-center justify-center p-6" onClick={() => setActiveSection(null)}>
          <div className="bg-[#f5f1ea] rounded-2xl max-w-lg w-full p-8 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-3">Configure your session</div>
            <h2 className="font-serif text-[32px] font-medium tracking-tight mb-2" style={{ color: activeSection.color }}>
              {activeSection.name}
            </h2>
            <p className="text-[13px] opacity-65 mb-6">{activeSection.fullName}</p>

            <div className="mb-5">
              <label className="block font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-2">
                Number of questions
              </label>
              <div className="flex gap-2">
                {[5, 10, 15, 20].map((n) => (
                  <button
                    key={n}
                    onClick={() => setNumQuestions(n)}
                    className={`flex-1 py-2.5 px-3 rounded-xl text-sm font-medium border-2 transition-all ${
                      numQuestions === n
                        ? "border-[#0c1a2e] bg-[#0c1a2e] text-[#f5f1ea]"
                        : "border-[#0c1a2e25] hover:border-[#0c1a2e]"
                    }`}
                  >
                    {n}
                  </button>
                ))}
              </div>
            </div>

            <div className="mb-7">
              <label className="block font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-2">
                Difficulty
              </label>
              <div className="grid grid-cols-2 gap-2">
                {(["mixed", "easy", "medium", "hard"] as const).map((d) => (
                  <button
                    key={d}
                    onClick={() => setDifficulty(d)}
                    className={`py-2.5 px-3 rounded-xl text-sm font-medium border-2 transition-all capitalize ${
                      difficulty === d
                        ? "border-[#0c1a2e] bg-[#0c1a2e] text-[#f5f1ea]"
                        : "border-[#0c1a2e25] hover:border-[#0c1a2e]"
                    }`}
                  >
                    {d}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setActiveSection(null)}
                className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a]"
              >
                Cancel
              </button>
              <button
                onClick={startSession}
                className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]"
              >
                Start session →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}