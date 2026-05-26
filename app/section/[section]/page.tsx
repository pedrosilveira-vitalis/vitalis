"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

type SectionInfo = {
  id: string;
  shortName: string;
  fullName: string;
  percentage: string;
  description: string;
  testStyle: string;
  accent: string;
  topics: { name: string; subtopics: string[] }[];
};

const SECTIONS: Record<string, SectionInfo> = {
  "bio-biochem": {
    id: "bio-biochem",
    shortName: "Bio / Biochem",
    fullName: "Biological and Biochemical Foundations of Living Systems",
    percentage: "25% of MCAT",
    description: "Tests how living systems work at the molecular, cellular, and organ-system level. Heavy on biochemistry, cellular biology, physiology, and integration across systems.",
    testStyle: "Most questions are passage-based, often around a research study. You'll need to interpret data, apply concepts, and connect biology to biochemistry.",
    accent: "#a8324a",
    topics: [
      { name: "Biochemistry foundations", subtopics: ["Amino acids & protein structure", "Enzyme kinetics (Km, Vmax)", "Enzyme inhibition", "Protein folding & denaturation"] },
      { name: "Cellular metabolism", subtopics: ["Glycolysis & gluconeogenesis", "Krebs cycle & ETC", "ATP yield calculations", "Fatty acid metabolism"] },
      { name: "Molecular biology", subtopics: ["DNA replication", "Transcription & translation", "Mutations & repair", "Gene regulation"] },
      { name: "Genetics", subtopics: ["Mendelian patterns", "Non-Mendelian inheritance", "Population genetics", "Hardy-Weinberg"] },
      { name: "Cell biology", subtopics: ["Membrane transport", "Cell signaling", "Cell cycle & mitosis", "Apoptosis"] },
      { name: "Organ systems", subtopics: ["Cardiovascular & respiratory", "Renal physiology", "Endocrine & feedback loops", "Nervous system"] },
      { name: "Immunology", subtopics: ["Innate vs adaptive immunity", "Antibody structure & function", "T cell vs B cell"] },
      { name: "Microbiology", subtopics: ["Bacterial structure & reproduction", "Viral life cycles", "Microbial classification"] },
    ],
  },
  "chem-phys": {
    id: "chem-phys",
    shortName: "Chem / Phys",
    fullName: "Chemical and Physical Foundations of Biological Systems",
    percentage: "25% of MCAT",
    description: "Tests general and organic chemistry, physics, and biochemistry — all applied to biological systems. Quantitative reasoning heavy.",
    testStyle: "Expect dimensional analysis, equation manipulation, and applying physics/chemistry to physiology. Memorizing formulas isn't enough — you need to apply them.",
    accent: "#2e4a6b",
    topics: [
      { name: "Acid-base chemistry", subtopics: ["pH, pKa, & buffers", "Henderson-Hasselbalch", "Titration curves", "Strong vs weak acids/bases"] },
      { name: "Thermodynamics", subtopics: ["Gibbs free energy", "Entropy & enthalpy", "Coupled reactions", "Equilibrium"] },
      { name: "Kinetics", subtopics: ["Reaction rates", "Rate laws", "Activation energy", "Catalysts"] },
      { name: "Organic chemistry", subtopics: ["Functional groups", "SN1/SN2 reactions", "Stereochemistry & chirality", "IR & NMR spectroscopy"] },
      { name: "Electrochemistry", subtopics: ["Redox reactions", "Galvanic cells", "Standard reduction potentials"] },
      { name: "Mechanics", subtopics: ["Forces & Newton's laws", "Energy & work", "Momentum & collisions", "Rotational motion"] },
      { name: "Fluids", subtopics: ["Bernoulli's equation", "Poiseuille's law", "Surface tension", "Buoyancy"] },
      { name: "Electricity & circuits", subtopics: ["Coulomb's law", "Resistors in series/parallel", "Capacitors"] },
      { name: "Waves & optics", subtopics: ["Sound & Doppler effect", "Light & refraction", "Lenses & mirrors"] },
    ],
  },
  "psych-soc": {
    id: "psych-soc",
    shortName: "Psych / Soc",
    fullName: "Psychological, Social, and Biological Foundations of Behavior",
    percentage: "25% of MCAT",
    description: "Tests psychology, sociology, and biological bases of behavior. Heavy on research methodology, theories of behavior, and statistical reasoning.",
    testStyle: "Many questions describe a research study and ask you to interpret results, identify variables, or apply theories. Memorizing definitions is the foundation but isn't enough.",
    accent: "#8a6b2e",
    topics: [
      { name: "Learning & cognition", subtopics: ["Classical & operant conditioning", "Memory (encoding, storage, retrieval)", "Cognitive development (Piaget, Vygotsky)", "Problem solving & heuristics"] },
      { name: "Sensation & perception", subtopics: ["Signal detection theory", "Vision & hearing pathways", "Attention", "Gestalt principles"] },
      { name: "Emotion & motivation", subtopics: ["Emotion theories (James-Lange, etc.)", "Drive reduction & Maslow", "Stress & coping"] },
      { name: "Personality & disorders", subtopics: ["Big Five personality", "Freudian theory", "DSM categories", "Major psychological disorders"] },
      { name: "Social psychology", subtopics: ["Attribution theory", "Cognitive dissonance", "Conformity & obedience", "Group dynamics"] },
      { name: "Sociology foundations", subtopics: ["Demographic structures", "Stratification & class", "Socialization", "Cultural transmission"] },
      { name: "Research methods", subtopics: ["Experimental design", "Validity & reliability", "Bias & confounding variables", "Ethics in research"] },
      { name: "Statistics", subtopics: ["Mean, median, mode, SD", "Correlation vs causation", "p-values & statistical significance", "Type I vs Type II errors"] },
      { name: "Biological bases of behavior", subtopics: ["Neurotransmitters", "Brain regions & function", "Sleep stages & circadian rhythms", "Hormones & behavior"] },
    ],
  },
  "cars": {
    id: "cars",
    shortName: "CARS",
    fullName: "Critical Analysis and Reasoning Skills",
    percentage: "25% of MCAT",
    description: "Tests reading comprehension and reasoning with dense humanities and social science passages. No outside knowledge required — only the passage matters.",
    testStyle: "Each passage is 500-600 words and argument-driven. Questions test main idea, author's purpose, inference, and application. Practice and reading speed matter most.",
    accent: "#4a3b6b",
    topics: [
      { name: "Question types", subtopics: ["Foundations of comprehension", "Reasoning within the text", "Reasoning beyond the text"] },
      { name: "Passage genres", subtopics: ["Philosophy & ethics", "Literary criticism", "History & cultural studies", "Sociology & political theory"] },
      { name: "Reading strategy", subtopics: ["Identifying main argument", "Tracking author's voice", "Distinguishing fact from opinion", "Mapping passage structure"] },
      { name: "Question strategy", subtopics: ["Eliminating wrong-but-true answers", "Spotting answer traps", "Distinguishing scope", "Timing per passage"] },
    ],
  },
};

function Logo() {
  return (
    <div className="flex items-center gap-2.5">
      <svg width="36" height="20" viewBox="0 0 60 28" fill="none" className="flex-shrink-0">
        <path
          d="M2 14 L12 14 L16 6 L22 22 L28 4 L34 18 L38 14 L48 14"
          stroke="#a8324a"
          strokeWidth="2.4"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        <circle cx="50" cy="14" r="2.2" fill="#a8324a" />
      </svg>
      <span className="font-serif font-semibold text-[22px] tracking-tight text-[#0c1a2e]">Vitalis</span>
    </div>
  );
}

export default function SectionPage() {
  const params = useParams();
  const sectionId = (params.section as string) || "";
  const section = SECTIONS[sectionId];

  const [tutorQuestion, setTutorQuestion] = useState("");

  if (!section) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] flex items-center justify-center p-10">
        <div className="text-center max-w-md">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-50 mb-4">404 · Section not found</div>
          <h1 className="font-serif text-3xl font-medium mb-4">No such section.</h1>
          <p className="text-[14px] opacity-65 mb-6">Try one of the four MCAT sections.</p>
          <Link href="/" className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]">
            ← Home
          </Link>
        </div>
      </div>
    );
  }return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="absolute top-0 right-0 w-[1000px] h-[500px] opacity-[0.05] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4"
          style={{ backgroundColor: section.accent }}
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
            <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
            <Link href="/score-calculator" className="opacity-60 hover:opacity-100">Score Calc</Link>
          </div>
          <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">{section.shortName}</div>
        </nav>

        <section className="px-10 pt-14 pb-10 border-b border-[#0c1a2e15]">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px opacity-40" style={{ backgroundColor: section.accent }} />
            Section · {section.percentage}
          </div>
          <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(40px,5vw,80px)] max-w-4xl mb-4">
            <span style={{ color: section.accent }}>{section.shortName}</span>
          </h1>
          <p className="font-mono text-[12px] tracking-[0.1em] uppercase opacity-60 mb-6">{section.fullName}</p>
          <p className="text-[16px] opacity-75 leading-relaxed max-w-3xl mb-4">{section.description}</p>
          <p className="text-[14px] opacity-65 leading-relaxed max-w-3xl italic">{section.testStyle}</p>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-px bg-[#0c1a2e15]">
          <Link
            href={`/practice/${section.id}?format=passage`}
            className="p-8 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-3 group"
          >
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50">Action 01</div>
            <div className="font-serif text-[28px] font-medium tracking-tight leading-tight">Practice questions</div>
            <div className="text-[13px] opacity-65 leading-relaxed">AAMC-style questions for {section.shortName}. Get them wrong? Vitalis explains.</div>
            <div className="mt-2 font-mono text-[11px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100">
              Start practicing →
            </div>
          </Link>
          <Link
            href="/tutor"
            className="p-8 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-3 group"
          >
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50">Action 02</div>
            <div className="font-serif text-[28px] font-medium tracking-tight leading-tight">Ask the tutor</div>
            <div className="text-[13px] opacity-65 leading-relaxed">Conversational explanations for any {section.shortName} concept.</div>
            <div className="mt-2 font-mono text-[11px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100">
              Open tutor →
            </div>
          </Link>
          {section.id !== "cars" ? (
            <Link
              href="/voice-cases"
              className="p-8 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-3 group"
            >
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50">Action 03</div>
              <div className="font-serif text-[28px] font-medium tracking-tight leading-tight">Voice cases</div>
              <div className="text-[13px] opacity-65 leading-relaxed">Talk through clinical scenarios that test {section.shortName} concepts.</div>
              <div className="mt-2 font-mono text-[11px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100">
                Start a case →
              </div>
            </Link>
         ) : (
            <Link
              href="/section/cars/strategy"
              className="p-8 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-3 group"
            >
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50">Action 03</div>
              <div className="font-serif text-[28px] font-medium tracking-tight leading-tight">CARS strategy</div>
              <div className="text-[13px] opacity-65 leading-relaxed">Reading technique, question types, trap patterns, pacing — the complete CARS guide.</div>
              <div className="mt-2 font-mono text-[11px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100">
                Open guide →
              </div>
            </Link>
          )}
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 gap-px bg-[#0c1a2e15] border-t border-[#0c1a2e15]">
          <Link
            href={`/flashcards/${section.id}`}
            className="p-8 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex items-center gap-5 group"
          >
            <div className="w-10 h-10 rounded-full border-2 border-[#0c1a2e25] flex items-center justify-center flex-shrink-0 group-hover:border-[#0c1a2e]">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="4" width="18" height="16" rx="2" />
                <line x1="8" y1="10" x2="16" y2="10" />
                <line x1="8" y1="14" x2="13" y2="14" />
              </svg>
            </div>
            <div className="flex-1">
              <div className="font-serif text-xl font-medium">Flashcards</div>
              <div className="text-[13px] opacity-65">High-yield {section.shortName} flashcards. AI-generated decks.</div>
            </div>
            <div className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100">
              Start →
            </div>
          </Link>
          <div className="p-8 bg-[#f5f1ea] flex items-center gap-5 cursor-not-allowed opacity-65">
            <div className="w-10 h-10 rounded-full border-2 border-[#0c1a2e25] flex items-center justify-center flex-shrink-0">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
              </svg>
            </div>
            <div>
              <div className="font-serif text-xl font-medium">Study guides</div>
              <div className="text-[13px] opacity-65">Structured notes for every {section.shortName} topic — coming soon</div>
            </div>
          </div>
        </section>

        <section className="px-10 py-14">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-6 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Topics covered
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl">
            {section.topics.map((topic, i) => (
              <div key={i} className="border border-[#0c1a2e15] rounded-2xl p-6 bg-[#0c1a2e0a]">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-2">{String(i + 1).padStart(2, "0")}</div>
                <h3 className="font-serif text-xl font-medium mb-3 tracking-tight">{topic.name}</h3>
                <ul className="space-y-1.5">
                  {topic.subtopics.map((st, j) => (
                    <li key={j} className="text-[13px] opacity-70 leading-relaxed flex gap-2">
                      <span className="opacity-40">·</span>
                      <span>{st}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        <section className="px-10 py-12 border-t border-[#0c1a2e15] bg-[#0c1a2e0a]">
          <div className="max-w-2xl mx-auto text-center">
            <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-3">Quick start</div>
            <h2 className="font-serif text-3xl font-medium tracking-tight mb-4">Ask Vitalis about {section.shortName}</h2>
            <div className="flex gap-2">
              <input
                value={tutorQuestion}
                onChange={(e) => setTutorQuestion(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    window.location.href = `/tutor`;
                  }
                }}
                placeholder={`e.g., "Explain ${section.topics[0].name.toLowerCase()}"`}
                className="flex-1 px-4 py-3 border-2 border-[#0c1a2e25] rounded-xl bg-[#f5f1ea] outline-none text-[14px] focus:border-[#0c1a2e]"
              />
              <Link
                href="/tutor"
                className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-xl hover:bg-[#1a2c4a] flex items-center"
              >
                Open tutor →
              </Link>
            </div>
          </div>
        </section>

        <footer className="px-10 py-10 border-t border-[#0c1a2e15] flex justify-between items-center font-mono text-[11px] tracking-[0.1em] uppercase opacity-60">
          <div>© 2026 Vitalis · Built for future physicians</div>
          <div>
            <Link href="/" className="hover:opacity-100 opacity-70">← Back home</Link>
          </div>
        </footer>
      </div>
    </div>
  );
}