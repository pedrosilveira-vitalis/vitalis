"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

type Lesson = {
  id: number;
  lesson_number: number;
  title: string;
  description: string;
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

const SECTION_NAMES: Record<string, string> = {
  "bio-biochem": "Bio / Biochem",
  "chem-phys": "Chem / Phys",
  "psych-soc": "Psych / Soc",
  "cars": "CARS",
};

const SECTION_FULL_NAMES: Record<string, string> = {
  "bio-biochem": "Biological and Biochemical Foundations of Living Systems",
  "chem-phys": "Chemical and Physical Foundations of Biological Systems",
  "psych-soc": "Psychological, Social, and Biological Foundations of Behavior",
  "cars": "Critical Analysis and Reasoning Skills",
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

export default function StudySectionPage() {
  const params = useParams();
  const sectionId = (params.section as string) || "";
  const [units, setUnits] = useState<Unit[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/study/sections")
      .then((r) => r.json())
      .then((d) => {
        setUnits(d.sections[sectionId] || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [sectionId]);

  if (!SECTION_NAMES[sectionId]) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] flex items-center justify-center p-10">
        <div className="text-center max-w-md">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-50 mb-4">404 · Not found</div>
          <h1 className="font-serif text-3xl font-medium mb-4">No such section.</h1>
          <Link href="/study" className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]">
            ← All sections
          </Link>
        </div>
      </div>
    );
  }

  const accent = SECTION_COLORS[sectionId];
  const totalLessons = units.reduce((sum, u) => sum + u.lessons.length, 0);
  const readLessons = units.reduce(
    (sum, u) => sum + u.lessons.filter((l) => l.progress?.read_complete).length,
    0
  );

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="absolute top-0 right-0 w-[1000px] h-[500px] opacity-[0.05] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4"
          style={{ backgroundColor: accent }}
        />
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
          <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">{SECTION_NAMES[sectionId]}</div>
        </nav>

        <section className="px-10 pt-14 pb-10 border-b border-[#0c1a2e15]">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px opacity-40" style={{ backgroundColor: accent }} />
            <Link href="/study" className="hover:opacity-100 opacity-70">Study guides</Link>
            <span className="opacity-40">/</span>
            <span>{SECTION_NAMES[sectionId]}</span>
          </div>
          <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(40px,5vw,80px)] mb-3" style={{ color: accent }}>
            {SECTION_NAMES[sectionId]}
          </h1>
          <p className="font-mono text-[12px] tracking-[0.1em] uppercase opacity-60 mb-6">{SECTION_FULL_NAMES[sectionId]}</p>
          {totalLessons > 0 && (
            <div className="flex items-center gap-4 max-w-md">
              <div className="flex-1 h-2 bg-[#0c1a2e15] rounded-full overflow-hidden">
                <div className="h-full transition-all" style={{ width: `${(readLessons / totalLessons) * 100}%`, backgroundColor: accent }} />
              </div>
              <div className="font-mono text-[11px] tracking-[0.1em] uppercase opacity-60 flex-shrink-0">
                {readLessons} / {totalLessons} lessons
              </div>
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
            <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Loading...</div>
          </div>
        ) : units.length === 0 ? (
          <div className="px-10 py-20 text-center max-w-md mx-auto">
            <h2 className="font-serif text-2xl font-medium mb-3">Content coming soon.</h2>
            <p className="text-[14px] opacity-65 mb-6">
              This section&apos;s study guides are still being written. Check back soon, or use the tutor or flashcards in the meantime.
            </p>
            <Link href="/study" className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a] inline-block">
              ← All sections
            </Link>
          </div>
        ) : (
          <section className="px-10 py-10 max-w-5xl">
            <div className="space-y-8">
              {units.map((unit) => {
                const unitRead = unit.lessons.filter((l) => l.progress?.read_complete).length;
                return (
                  <div key={unit.id} className="border border-[#0c1a2e15] rounded-2xl overflow-hidden">
                    <div className="p-6 pb-4 border-b border-[#0c1a2e15] bg-[#0c1a2e0a]">
                      <div className="flex items-center justify-between mb-2 flex-wrap gap-2">
                        <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">
                          Unit {String(unit.unit_number).padStart(2, "0")}
                        </div>
                        <div className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-60">
                          {unitRead} / {unit.lessons.length} lessons read
                        </div>
                      </div>
                      <h2 className="font-serif text-[26px] font-medium tracking-tight mb-2">{unit.title}</h2>
                      <p className="text-[14px] opacity-70 leading-relaxed">{unit.description}</p>
                    </div>

                    <div className="divide-y divide-[#0c1a2e15]">
                      {unit.lessons.map((lesson) => {
                        const isRead = lesson.progress?.read_complete;
                        return (
                          <Link
                            key={lesson.id}
                            href={`/study/lessons/${lesson.id}`}
                            className="flex items-center gap-4 p-5 hover:bg-[#0c1a2e08] transition-colors group"
                          >
                            <div className="w-9 h-9 rounded-full border-2 flex items-center justify-center flex-shrink-0 font-mono text-[11px]"
                                 style={{
                                   borderColor: isRead ? "#3e6b4a" : "#0c1a2e25",
                                   backgroundColor: isRead ? "#3e6b4a15" : "transparent",
                                   color: isRead ? "#3e6b4a" : "#0c1a2e",
                                 }}>
                              {isRead ? (
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                                  <polyline points="20 6 9 17 4 12" />
                                </svg>
                              ) : (
                                String(lesson.lesson_number).padStart(2, "0")
                              )}
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="font-serif text-[17px] font-medium leading-snug mb-1">{lesson.title}</div>
                              <div className="text-[13px] opacity-65 leading-relaxed mb-1 truncate">{lesson.description}</div>
                              <div className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-50">
                                {lesson.estimated_minutes} min read
                                {lesson.progress?.questions_total ? ` · quiz ${lesson.progress.questions_correct}/${lesson.progress.questions_total}` : ""}
                              </div>
                            </div>
                            <div className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-40 group-hover:opacity-100 transition-opacity flex-shrink-0">
                              {isRead ? "Review →" : "Read →"}
                            </div>
                          </Link>
                        );
                      })}
                    </div>

                    <div className="p-5 border-t border-[#0c1a2e15] bg-[#0c1a2e0a] flex items-center justify-between flex-wrap gap-3">
                      <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">
                        End-of-unit test · 15 questions
                      </div>
                      <button
                        disabled
                        className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-40 cursor-not-allowed px-3 py-2 border border-[#0c1a2e25] rounded-full"
                        title="Coming after lesson questions are wired up"
                      >
                        Unit test — coming soon
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        )}

        <div className="mx-10 my-7 p-3.5 px-5 border border-dashed border-[#0c1a2e25] rounded-lg font-mono text-[12px] leading-relaxed opacity-60">
          Read each lesson, highlight important passages, take notes, and use the end-of-lesson questions to check yourself. Sign in to save your progress across sessions.
        </div>
      </div>
    </div>
  );
}