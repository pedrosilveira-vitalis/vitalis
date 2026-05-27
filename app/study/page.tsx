"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type Lesson = {
  id: number;
  lesson_number: number;
  title: string;
  estimated_minutes: number;
  progress: { read_complete: boolean; questions_correct: number; questions_total: number } | null;
};

type Unit = {
  id: number;
  unit_number: number;
  title: string;
  description: string;
  lessons: Lesson[];
};

type SectionsData = {
  sections: Record<string, Unit[]>;
  isAuthenticated: boolean;
};

const SECTION_NAMES: Record<string, string> = {
  "bio-biochem": "Bio / Biochem",
  "chem-phys": "Chem / Phys",
  "psych-soc": "Psych / Soc",
  "cars": "CARS",
};

const SECTION_DESCRIPTIONS: Record<string, string> = {
  "bio-biochem": "Cells, organs, biochemistry, genetics, physiology. The largest content section.",
  "chem-phys": "General chemistry, organic, physics. Quantitative reasoning heavy.",
  "psych-soc": "Behavior, cognition, sociology, research methods, statistics.",
  "cars": "Critical analysis and reading. Less about content, more about strategy.",
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

export default function StudyLandingPage() {
  const [data, setData] = useState<SectionsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/study/sections")
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  function progressForSection(units: Unit[]): { read: number; total: number } {
    let read = 0;
    let total = 0;
    for (const u of units) {
      for (const l of u.lessons) {
        total++;
        if (l.progress?.read_complete) read++;
      }
    }
    return { read, total };
  }

  const allSections = ["bio-biochem", "chem-phys", "psych-soc", "cars"];

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[1000px] h-[500px] bg-[#0c1a2e] opacity-[0.05] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
      </div>

      <div className="relative z-10">
        <nav className="flex items-center justify-between px-10 py-5 border-b border-[#0c1a2e15]">
          <Logo />
          <div className="hidden md:flex gap-6 text-sm font-medium">
            <Link href="/" className="opacity-60 hover:opacity-100">Home</Link>
            <Link href="/tutor" className="opacity-60 hover:opacity-100">Tutor</Link>
            <Link href="/practice" className="opacity-60 hover:opacity-100">Practice</Link>
            <Link href="/flashcards" className="opacity-60 hover:opacity-100">Flashcards</Link>
            <Link href="/study" className="opacity-100 border-b border-[#a8324a] pb-0.5">Study</Link>
            <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
          </div>
          <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">Study Guides</div>
        </nav>

        <section className="px-10 pt-14 pb-10 border-b border-[#0c1a2e15]">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Mode · Study guides
          </div>
          <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(48px,6vw,88px)] max-w-4xl">
            Master the <span className="italic font-light text-[#a8324a]">material.</span>
          </h1>
          <p className="text-[15px] opacity-70 mt-4 max-w-2xl leading-relaxed">
            College-level study guides covering every MCAT topic. Read, highlight, take notes, and test yourself with end-of-lesson questions and unit tests. Built to be your primary study resource.
          </p>
          {data && !data.isAuthenticated && (
            <div className="mt-6 p-3 bg-[#a8324a08] border border-[#a8324a25] rounded-lg text-[13px] opacity-80 max-w-2xl">
              <Link href="/sign-in" className="text-[#a8324a] font-medium hover:underline">Sign in</Link> to save your highlights, notes, and progress across sessions.
            </div>
          )}
        </section>

        {loading ? (
          <div className="px-10 py-20 text-center">
            <div className="flex items-center justify-center gap-2 mb-3">
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" />
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.15s" }} />
              <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.3s" }} />
            </div>
            <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Loading study guides...</div>
          </div>
        ) : (
          <section className="grid grid-cols-1 md:grid-cols-2 gap-px bg-[#0c1a2e15]">
            {allSections.map((sectionKey) => {
              const units = data?.sections[sectionKey] || [];
              const { read, total } = progressForSection(units);
              const accent = SECTION_COLORS[sectionKey];
              return (
                <Link
                  key={sectionKey}
                  href={`/study/${sectionKey}`}
                  className="p-10 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-4 group min-h-[280px]"
                >
                  <div className="flex items-center justify-between">
                    <div className="font-mono text-[11px] tracking-[0.14em] uppercase opacity-55">25% of MCAT</div>
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: accent }} />
                  </div>
                  <h2 className="font-serif text-[36px] font-medium tracking-tight leading-none" style={{ color: accent }}>
                    {SECTION_NAMES[sectionKey]}
                  </h2>
                  <p className="text-[14px] opacity-75 leading-relaxed">
                    {SECTION_DESCRIPTIONS[sectionKey]}
                  </p>
                  <div className="mt-auto">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">
                        {total > 0 ? `${units.length} unit${units.length !== 1 ? "s" : ""} · ${total} lesson${total !== 1 ? "s" : ""}` : "Coming soon"}
                      </div>
                    </div>
                    {total > 0 && (
                      <div className="flex items-center gap-3 mb-2">
                        <div className="flex-1 h-1.5 bg-[#0c1a2e15] rounded-full overflow-hidden">
                          <div
                            className="h-full transition-all"
                            style={{ width: total > 0 ? `${(read / total) * 100}%` : "0%", backgroundColor: accent }}
                          />
                        </div>
                        <div className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-55 flex-shrink-0">
                          {read} / {total}
                        </div>
                      </div>
                    )}
                    <div className="mt-3 font-mono text-[11px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100 transition-opacity">
                      {total > 0 ? "Open section →" : "Content coming soon"}
                    </div>
                  </div>
                </Link>
              );
            })}
          </section>
        )}

        <div className="mx-10 my-7 p-3.5 px-5 border border-dashed border-[#0c1a2e25] rounded-lg font-mono text-[12px] leading-relaxed opacity-60">
          Study guides are AI-generated and reviewed for accuracy. They cover MCAT-relevant content at college level. Always cross-reference with official AAMC materials.
        </div>
      </div>
    </div>
  );
}