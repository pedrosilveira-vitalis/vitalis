"use client";

import { useState } from "react";
import Link from "next/link";

type Scores = {
  bio: string;
  chem: string;
  psych: string;
  cars: string;
};

// MCAT percentile lookup based on AAMC published data (approximate)
const PERCENTILE_TABLE: { score: number; percentile: number }[] = [
  { score: 528, percentile: 100 }, { score: 525, percentile: 100 }, { score: 522, percentile: 99 },
  { score: 520, percentile: 98 }, { score: 518, percentile: 96 }, { score: 515, percentile: 92 },
  { score: 512, percentile: 85 }, { score: 510, percentile: 80 }, { score: 508, percentile: 73 },
  { score: 505, percentile: 64 }, { score: 502, percentile: 53 }, { score: 500, percentile: 47 },
  { score: 498, percentile: 39 }, { score: 495, percentile: 30 }, { score: 492, percentile: 21 },
  { score: 490, percentile: 16 }, { score: 488, percentile: 12 }, { score: 485, percentile: 7 },
  { score: 482, percentile: 4 }, { score: 478, percentile: 1 }, { score: 472, percentile: 0 },
];

// Schools with similar median MCAT for matriculants — approximate, from publicly reported MSAR data
// (these are MEDIANS, not minimums — interpretation: "students at these schools typically scored around this")
const SCHOOL_TIERS: { minScore: number; schools: { name: string; median: number }[] }[] = [
  {
    minScore: 520,
    schools: [
      { name: "Harvard Medical School", median: 520 },
      { name: "Johns Hopkins School of Medicine", median: 521 },
      { name: "Stanford School of Medicine", median: 519 },
      { name: "NYU Grossman School of Medicine", median: 522 },
      { name: "Washington University in St. Louis", median: 521 },
    ],
  },
  {
    minScore: 515,
    schools: [
      { name: "University of Michigan Medical School", median: 516 },
      { name: "Yale School of Medicine", median: 519 },
      { name: "Cornell (Weill Cornell Medicine)", median: 518 },
      { name: "Northwestern Feinberg", median: 519 },
      { name: "UCLA David Geffen", median: 517 },
    ],
  },
  {
    minScore: 510,
    schools: [
      { name: "University of Pittsburgh", median: 514 },
      { name: "Emory University School of Medicine", median: 514 },
      { name: "Ohio State University College of Medicine", median: 514 },
      { name: "University of Miami Miller", median: 512 },
      { name: "University of Florida College of Medicine", median: 514 },
    ],
  },
  {
    minScore: 505,
    schools: [
      { name: "Wayne State University", median: 510 },
      { name: "University of South Florida (Morsani)", median: 511 },
      { name: "University of Kentucky", median: 509 },
      { name: "Drexel University", median: 510 },
      { name: "Many state MD programs", median: 508 },
    ],
  },
  {
    minScore: 500,
    schools: [
      { name: "Most DO programs (median 504–507)", median: 504 },
      { name: "Some state MD programs (with strong holistic review)", median: 505 },
      { name: "Caribbean MD programs (varies widely)", median: 500 },
    ],
  },
  {
    minScore: 0,
    schools: [
      { name: "Below average for US MD applicants", median: 0 },
      { name: "Some DO programs may still accept (varies)", median: 500 },
      { name: "Consider retaking + strengthening other parts of application", median: 0 },
    ],
  },
];

function lookupPercentile(total: number): number {
  for (const row of PERCENTILE_TABLE) {
    if (total >= row.score) return row.percentile;
  }
  return 0;
}

function lookupSchools(total: number): { name: string; median: number }[] {
  for (const tier of SCHOOL_TIERS) {
    if (total >= tier.minScore) return tier.schools;
  }
  return [];
}

function scoreInterpretation(total: number): { tier: string; description: string; color: string } {
  if (total >= 520) return {
    tier: "Top-tier",
    description: "Competitive at every US medical school, including top-10 programs. Strong applications often pair this with research and clinical experience.",
    color: "#3e5641",
  };
  if (total >= 515) return {
    tier: "Excellent",
    description: "Competitive at most top-30 medical schools. Above the average accepted score at most MD programs.",
    color: "#3e5641",
  };
  if (total >= 510) return {
    tier: "Strong",
    description: "Competitive at most US MD programs. Around the average accepted score at many mid-tier schools.",
    color: "#d9a441",
  };
  if (total >= 505) return {
    tier: "Solid",
    description: "Competitive at many MD programs and most DO programs. Often paired with strong GPA and ECs.",
    color: "#d9a441",
  };
  if (total >= 500) return {
    tier: "Average",
    description: "Around the average MCAT score for applicants. Competitive primarily at DO programs and some MD programs with strong holistic review.",
    color: "#c54a2a",
  };
  return {
    tier: "Below average",
    description: "Below the average matriculant score. Consider retaking if your GPA is strong, or strengthening other parts of your application.",
    color: "#c54a2a",
  };
}

export default function ScoreCalculatorPage() {
  const [scores, setScores] = useState<Scores>({ bio: "", chem: "", psych: "", cars: "" });

  function updateScore(section: keyof Scores, value: string) {
    if (value === "") {
      setScores({ ...scores, [section]: "" });
      return;
    }
    const n = parseInt(value, 10);
    if (!isNaN(n) && n >= 118 && n <= 132) {
      setScores({ ...scores, [section]: value });
    } else if (!isNaN(n) && value.length <= 3) {
      setScores({ ...scores, [section]: value });
    }
  }

  const allFilled = scores.bio && scores.chem && scores.psych && scores.cars;
  const allValid = allFilled && Object.values(scores).every((s) => {
    const n = parseInt(s, 10);
    return !isNaN(n) && n >= 118 && n <= 132;
  });
  const total = allValid
    ? parseInt(scores.bio, 10) + parseInt(scores.chem, 10) + parseInt(scores.psych, 10) + parseInt(scores.cars, 10)
    : 0;
  const percentile = total > 0 ? lookupPercentile(total) : 0;
  const interpretation = total > 0 ? scoreInterpretation(total) : null;
  const schools = total > 0 ? lookupSchools(total) : [];

  function reset() {
    setScores({ bio: "", chem: "", psych: "", cars: "" });
  }

  const sections: { key: keyof Scores; label: string; full: string }[] = [
    { key: "chem", label: "Chem / Phys", full: "Chemical and Physical Foundations" },
    { key: "cars", label: "CARS", full: "Critical Analysis and Reasoning Skills" },
    { key: "bio", label: "Bio / Biochem", full: "Biological and Biochemical Foundations" },
    { key: "psych", label: "Psych / Soc", full: "Psychological, Social, and Biological Foundations" },
  ];return (
    <div className="min-h-screen bg-[#f3efe7] text-[#161410] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[900px] h-[500px] bg-[#d9a441] opacity-10 blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
      </div>

      <div className="relative z-10">
        <nav className="flex items-center justify-between px-10 py-5 border-b border-[#16141015]">
          <div className="flex items-center gap-3">
            <span className="w-2.5 h-2.5 rounded-full bg-[#c54a2a] shadow-[0_0_0_4px_#c54a2a22]" />
            <span className="font-serif font-semibold text-[22px] tracking-tight">Vitalis</span>
          </div>
          <div className="hidden md:flex gap-7 text-sm font-medium">
            <Link href="/" className="opacity-60 hover:opacity-100">Home</Link>
            <Link href="/tutor" className="opacity-60 hover:opacity-100">Tutor</Link>
            <Link href="/practice" className="opacity-60 hover:opacity-100">Practice</Link>
            <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
          </div>
          <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">Score Tools</div>
        </nav>

        <section className="px-10 pt-14 pb-8 border-b border-[#16141015]">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#161410] opacity-40" />
            Tool · Score calculator
          </div>
          <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(48px,6vw,88px)] max-w-4xl">
            What does your <span className="italic font-light text-[#c54a2a]">score</span> mean?
          </h1>
          <p className="text-[15px] opacity-70 mt-4 max-w-xl leading-relaxed">
            Enter your section scores (each 118–132) to see your total, approximate percentile, and example medical schools where students with similar scores tend to matriculate.
          </p>
        </section>

        <section className="px-10 py-12 grid md:grid-cols-2 gap-10 max-w-5xl mx-auto">
          {/* Inputs */}
          <div className="space-y-5">
            {sections.map((s) => {
              const val = scores[s.key];
              const n = parseInt(val, 10);
              const valid = val !== "" && !isNaN(n) && n >= 118 && n <= 132;
              const invalid = val !== "" && !valid;
              return (
                <div key={s.key}>
                  <label className="block">
                    <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">{s.full}</div>
                    <div className="flex items-center gap-3">
                      <div className="font-serif text-lg font-medium w-32">{s.label}</div>
                      <input
                        type="text"
                        inputMode="numeric"
                        value={val}
                        onChange={(e) => updateScore(s.key, e.target.value)}
                        placeholder="118–132"
                        className={`flex-1 px-4 py-3 border-2 rounded-xl bg-transparent outline-none transition-colors text-lg font-serif font-medium ${
                          invalid ? "border-[#c54a2a]" : valid ? "border-[#3e5641]" : "border-[#16141025] focus:border-[#161410]"
                        }`}
                      />
                    </div>
                    {invalid && <div className="text-[12px] text-[#c54a2a] mt-1.5 font-mono">Score must be between 118 and 132</div>}
                  </label>
                </div>
              );
            })}

            <button
              onClick={reset}
              className="mt-4 font-mono text-[10px] tracking-[0.1em] uppercase opacity-50 hover:opacity-100"
            >
              Reset all
            </button>
          </div>

          {/* Result */}
          <div>
            {!allValid ? (
              <div className="border-2 border-dashed border-[#16141025] rounded-2xl p-10 text-center">
                <div className="font-mono text-[11px] tracking-[0.14em] uppercase opacity-50 mb-3">Result</div>
                <div className="font-serif text-2xl font-light opacity-60">Enter all four scores to see your total.</div>
              </div>
            ) : (
              <div className="rounded-2xl p-8 border-2" style={{ borderColor: interpretation?.color || "#161410" }}>
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Total MCAT score</div>
                <div className="font-serif text-7xl font-medium tracking-tight leading-none mb-4">{total}</div>
                <div className="text-[14px] opacity-70 mb-6">out of 528 · approximately <strong>{percentile}th percentile</strong></div>

                <div className="border-t border-[#16141015] pt-5">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Tier</div>
                  <div className="font-serif text-2xl font-medium mb-3" style={{ color: interpretation?.color }}>
                    {interpretation?.tier}
                  </div>
                  <p className="text-[14px] leading-relaxed opacity-80">{interpretation?.description}</p>
                </div>

                <div className="mt-6 pt-5 border-t border-[#16141015]">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-3">Schools with similar median MCAT</div>
                  <ul className="space-y-2">
                    {schools.map((school, i) => (
                      <li key={i} className="flex items-center justify-between gap-4 text-[14px]">
                        <span className="leading-relaxed">{school.name}</span>
                        {school.median > 0 && (
                          <span className="font-mono text-[11px] tracking-[0.05em] opacity-60 flex-shrink-0">
                            median {school.median}
                          </span>
                        )}
                      </li>
                    ))}
                  </ul>
                  <div className="mt-4 font-mono text-[10px] tracking-[0.08em] opacity-50 leading-relaxed">
                    Medians shown are approximate from publicly reported MSAR data. School competitiveness depends on many factors beyond MCAT.
                  </div>
                </div>

                <div className="mt-6 pt-5 border-t border-[#16141015]">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-3">Section breakdown</div>
                  <div className="grid grid-cols-4 gap-2 text-center">
                    <div>
                      <div className="font-serif text-2xl font-medium">{scores.chem}</div>
                      <div className="font-mono text-[9px] uppercase tracking-[0.1em] opacity-50 mt-1">C/P</div>
                    </div>
                    <div>
                      <div className="font-serif text-2xl font-medium">{scores.cars}</div>
                      <div className="font-mono text-[9px] uppercase tracking-[0.1em] opacity-50 mt-1">CARS</div>
                    </div>
                    <div>
                      <div className="font-serif text-2xl font-medium">{scores.bio}</div>
                      <div className="font-mono text-[9px] uppercase tracking-[0.1em] opacity-50 mt-1">B/B</div>
                    </div>
                    <div>
                      <div className="font-serif text-2xl font-medium">{scores.psych}</div>
                      <div className="font-mono text-[9px] uppercase tracking-[0.1em] opacity-50 mt-1">P/S</div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>

        <div className="mx-10 my-7 p-3.5 px-5 border border-dashed border-[#16141025] rounded-lg font-mono text-[12px] leading-relaxed opacity-60">
          MCAT alone does not determine admissions. GPA, research, clinical experience, essays, interviews, and state residency all factor in. Use this tool as a rough orientation, not a prediction.
        </div>
      </div>
    </div>
  );
}