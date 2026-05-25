import Link from "next/link";

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

export default function Home() {
  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[1200px] h-[600px] bg-[#0c1a2e] opacity-[0.05] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
        <div className="absolute bottom-0 left-0 w-[900px] h-[500px] bg-[#a8324a] opacity-[0.05] blur-[120px] rounded-full translate-y-1/3 -translate-x-1/4" />
      </div>

      <div className="relative z-10">
        <nav className="flex items-center justify-between px-10 py-5 border-b border-[#0c1a2e15]">
          <Logo />
          <div className="hidden md:flex gap-5 text-sm font-medium">
            <Link href="/" className="opacity-100 border-b border-[#a8324a] pb-0.5">Home</Link>
            <Link href="/tutor" className="opacity-60 hover:opacity-100 transition-opacity">Tutor</Link>
            <Link href="/practice" className="opacity-60 hover:opacity-100 transition-opacity">Practice</Link>
            <Link href="/flashcards" className="opacity-60 hover:opacity-100 transition-opacity">Flashcards</Link>
            <Link href="/voice-cases" className="opacity-60 hover:opacity-100 transition-opacity">Voice Cases</Link>
            <Link href="/score-calculator" className="opacity-60 hover:opacity-100 transition-opacity">Score Calc</Link>
          </div>
          <Link
            href="/tutor"
            className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-4 py-2.5 rounded-full hover:bg-[#1a2c4a] transition-colors"
          >
            Start free →
          </Link>
        </nav>

        <section className="grid md:grid-cols-[1.2fr_0.8fr] gap-10 px-10 pt-20 pb-14 items-end border-b border-[#0c1a2e15]">
          <div>
            <div className="flex items-center gap-3 mb-6 font-mono text-[11px] tracking-[0.18em] uppercase opacity-60">
              <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
              MCAT prep, reimagined · 2026
            </div>
            <h1 className="font-serif font-normal leading-[0.92] tracking-[-0.03em] text-[clamp(56px,8vw,128px)]">
              Think <span className="italic font-light text-[#a8324a]">like</span><br />
              a physician.
              <span className="block font-sans font-medium not-italic text-[#0c1a2e] mt-2 text-[0.55em] tracking-[-0.02em]">
                Built to bring out the physician in you.
              </span>
            </h1>
            <div className="flex gap-6 mt-7">
              <div>
                <div className="font-serif font-semibold text-4xl tracking-tight">10k+</div>
                <div className="font-mono text-[10px] uppercase tracking-[0.12em] opacity-60 mt-1">Practice items</div>
              </div>
              <div>
                <div className="font-serif font-semibold text-4xl tracking-tight">4</div>
                <div className="font-mono text-[10px] uppercase tracking-[0.12em] opacity-60 mt-1">MCAT sections</div>
              </div>
              <div>
                <div className="font-serif font-semibold text-4xl tracking-tight">24/7</div>
                <div className="font-mono text-[10px] uppercase tracking-[0.12em] opacity-60 mt-1">AI tutor</div>
              </div>
            </div>
          </div>
          <div className="text-[15px] leading-relaxed max-w-sm text-[#0c1a2ecc]">
            Practice across Bio/Biochem, Chem/Phys, Psych/Soc, and CARS. Ask anything. Hear feedback. Build the instincts that score 520+.
          </div>
        </section>

        <section className="px-10 pt-14 pb-4">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-3 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Browse by section
          </div>
          <h2 className="font-serif text-[clamp(28px,4vw,44px)] font-medium tracking-tight mb-2">Pick your section.</h2>
          <p className="text-[14px] opacity-65 max-w-2xl">Every section gets its own hub: topics covered, practice questions, the tutor, and study resources.</p>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-px bg-[#0c1a2e15] mx-10 mt-2 rounded-2xl overflow-hidden border border-[#0c1a2e15]">
          <Link href="/section/bio-biochem" className="p-7 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-3 group min-h-[200px]">
            <div className="flex items-center justify-between">
              <div className="font-mono text-[10px] tracking-[0.14em] opacity-50">25%</div>
              <div className="w-2.5 h-2.5 rounded-full bg-[#a8324a]" />
            </div>
            <div className="font-serif text-[24px] font-medium tracking-tight leading-tight">Bio / Biochem</div>
            <div className="text-[12.5px] opacity-65 leading-relaxed">Biology, biochemistry, physiology, genetics, cells.</div>
            <div className="mt-auto font-mono text-[10px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100">Open section →</div>
          </Link>
          <Link href="/section/chem-phys" className="p-7 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-3 group min-h-[200px]">
            <div className="flex items-center justify-between">
              <div className="font-mono text-[10px] tracking-[0.14em] opacity-50">25%</div>
              <div className="w-2.5 h-2.5 rounded-full bg-[#2e4a6b]" />
            </div>
            <div className="font-serif text-[24px] font-medium tracking-tight leading-tight">Chem / Phys</div>
            <div className="text-[12.5px] opacity-65 leading-relaxed">General chem, organic, physics, quantitative reasoning.</div>
            <div className="mt-auto font-mono text-[10px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100">Open section →</div>
          </Link>
          <Link href="/section/psych-soc" className="p-7 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-3 group min-h-[200px]">
            <div className="flex items-center justify-between">
              <div className="font-mono text-[10px] tracking-[0.14em] opacity-50">25%</div>
              <div className="w-2.5 h-2.5 rounded-full bg-[#8a6b2e]" />
            </div>
            <div className="font-serif text-[24px] font-medium tracking-tight leading-tight">Psych / Soc</div>
            <div className="text-[12.5px] opacity-65 leading-relaxed">Behavior, cognition, sociology, research methods, stats.</div>
            <div className="mt-auto font-mono text-[10px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100">Open section →</div>
          </Link>
          <Link href="/section/cars" className="p-7 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-3 group min-h-[200px]">
            <div className="flex items-center justify-between">
              <div className="font-mono text-[10px] tracking-[0.14em] opacity-50">25%</div>
              <div className="w-2.5 h-2.5 rounded-full bg-[#4a3b6b]" />
            </div>
            <div className="font-serif text-[24px] font-medium tracking-tight leading-tight">CARS</div>
            <div className="text-[12.5px] opacity-65 leading-relaxed">Critical analysis, reading, reasoning. Humanities passages.</div>
            <div className="mt-auto font-mono text-[10px] tracking-[0.1em] uppercase opacity-50 group-hover:opacity-100">Open section →</div>
          </Link>
        </section><section className="px-10 pt-20 pb-4">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-3 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Practice modes
          </div>
          <h2 className="font-serif text-[clamp(28px,4vw,44px)] font-medium tracking-tight mb-2">Train how you want.</h2>
          <p className="text-[14px] opacity-65 max-w-2xl">Six tools, each designed for a different learning style. Use them alone or stack them.</p>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-[#0c1a2e15] mx-10 mt-2 mb-4 rounded-2xl overflow-hidden border border-[#0c1a2e15]">
          <Link href="/tutor" className="p-7 bg-[#0c1a2e] text-[#f5f1ea] hover:bg-[#1a2c4a] transition-colors flex flex-col gap-2 min-h-[180px]">
            <div className="font-mono text-[11px] opacity-70 tracking-[0.12em]">01</div>
            <div className="font-serif text-[20px] font-medium tracking-tight">Ask the tutor</div>
            <div className="text-[12.5px] opacity-75 leading-relaxed">Conversational explanations for any MCAT concept.</div>
            <div className="mt-auto font-mono text-[10px] tracking-[0.1em] uppercase opacity-70">Start →</div>
          </Link>
          <Link href="/voice-cases" className="p-7 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-2 min-h-[180px]">
            <div className="font-mono text-[11px] opacity-50 tracking-[0.12em]">02</div>
            <div className="font-serif text-[20px] font-medium tracking-tight">Voice cases</div>
            <div className="text-[12.5px] opacity-65 leading-relaxed">Talk through patient scenarios out loud.</div>
            <div className="mt-auto font-mono text-[10px] tracking-[0.1em] uppercase opacity-50">Start →</div>
          </Link>
          <Link href="/practice" className="p-7 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-2 min-h-[180px]">
            <div className="font-mono text-[11px] opacity-50 tracking-[0.12em]">03</div>
            <div className="font-serif text-[20px] font-medium tracking-tight">Practice sets</div>
            <div className="text-[12.5px] opacity-65 leading-relaxed">AAMC-style questions with on-the-fly tutoring.</div>
            <div className="mt-auto font-mono text-[10px] tracking-[0.1em] uppercase opacity-50">Start →</div>
          </Link>
          <Link href="/flashcards" className="p-7 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-2 min-h-[180px]">
            <div className="font-mono text-[11px] opacity-50 tracking-[0.12em]">04</div>
            <div className="font-serif text-[20px] font-medium tracking-tight">Flashcards</div>
            <div className="text-[12.5px] opacity-65 leading-relaxed">High-yield decks. Flip, mark, repeat. Build the recall muscle.</div>
            <div className="mt-auto font-mono text-[10px] tracking-[0.1em] uppercase opacity-50">Start →</div>
          </Link>
          <Link href="/score-calculator" className="p-7 bg-[#f5f1ea] hover:bg-[#0c1a2e08] transition-colors flex flex-col gap-2 min-h-[180px]">
            <div className="font-mono text-[11px] opacity-50 tracking-[0.12em]">05</div>
            <div className="font-serif text-[20px] font-medium tracking-tight">Score calculator</div>
            <div className="text-[12.5px] opacity-65 leading-relaxed">Check what your MCAT score means + comparable schools.</div>
            <div className="mt-auto font-mono text-[10px] tracking-[0.1em] uppercase opacity-50">Open →</div>
          </Link>
          <div className="p-7 bg-[#f5f1ea] flex flex-col gap-2 cursor-not-allowed opacity-60 min-h-[180px]">
            <div className="font-mono text-[11px] opacity-50 tracking-[0.12em]">06</div>
            <div className="font-serif text-[20px] font-medium tracking-tight">Study guides</div>
            <div className="text-[12.5px] opacity-65 leading-relaxed">Structured notes for every topic — coming soon.</div>
            <div className="mt-auto font-mono text-[10px] tracking-[0.1em] uppercase opacity-50">Coming soon</div>
          </div>
        </section>

        <section className="px-10 py-24 text-center border-t border-[#0c1a2e15] mt-6">
          <h2 className="font-serif italic font-light text-[clamp(36px,5vw,64px)] leading-[1.05] tracking-[-0.02em] max-w-3xl mx-auto">
            Ready to think like a <span className="text-[#a8324a] not-italic font-medium">physician?</span>
          </h2>
          <Link href="/tutor" className="inline-block mt-8 font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-6 py-3.5 rounded-full hover:bg-[#1a2c4a] transition-colors">
            Start the tutor →
          </Link>
        </section>

        <div className="mx-10 my-7 p-3.5 px-5 border border-dashed border-[#0c1a2e25] rounded-lg font-mono text-[12px] leading-relaxed opacity-60">
          Vitalis is a study aid. It is not medical advice and is not a substitute for a clinical educator. All content is for MCAT preparation only.
        </div>

        <footer className="px-10 py-10 border-t border-[#0c1a2e15] flex justify-between items-center font-mono text-[11px] tracking-[0.1em] uppercase opacity-60">
          <div>© 2026 Vitalis · Built for future physicians</div>
          <div>v0.3 — beta</div>
        </footer>
      </div>
    </div>
  );
}