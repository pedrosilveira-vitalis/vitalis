import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#f3efe7] text-[#161410] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[1200px] h-[600px] bg-[#d9a441] opacity-10 blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
        <div className="absolute bottom-0 left-0 w-[900px] h-[500px] bg-[#3e5641] opacity-10 blur-[120px] rounded-full translate-y-1/3 -translate-x-1/4" />
      </div>

      <div className="relative z-10">
        <nav className="flex items-center justify-between px-10 py-5 border-b border-[#16141015]">
          <div className="flex items-center gap-3">
            <span className="w-2.5 h-2.5 rounded-full bg-[#c54a2a] shadow-[0_0_0_4px_#c54a2a22]" />
            <span className="font-serif font-semibold text-[22px] tracking-tight">Vitalis</span>
          </div>
          <div className="hidden md:flex gap-7 text-sm font-medium">
            <Link href="/" className="opacity-100 border-b border-[#c54a2a] pb-0.5">Home</Link>
            <Link href="/tutor" className="opacity-60 hover:opacity-100 transition-opacity">Tutor</Link>
            <span className="opacity-40 cursor-not-allowed">Practice</span>
            <Link href="/voice-cases" className="opacity-60 hover:opacity-100 transition-opacity">Voice Cases</Link>
            <span className="opacity-40 cursor-not-allowed">About</span>
          </div>
          <Link
            href="/tutor"
            className="font-mono text-xs uppercase tracking-[0.08em] bg-[#161410] text-[#f3efe7] px-4 py-2.5 rounded-full hover:bg-[#2a2620] transition-colors"
          >
            Start free →
          </Link>
        </nav>

        <section className="grid md:grid-cols-[1.2fr_0.8fr] gap-10 px-10 pt-16 pb-8 items-end border-b border-[#16141015]">
          <div>
            <div className="flex items-center gap-3 mb-6 font-mono text-[11px] tracking-[0.18em] uppercase opacity-60">
              <span className="w-10 h-px bg-[#161410] opacity-40" />
              MCAT prep, reimagined · 2026
            </div>
            <h1 className="font-serif font-normal leading-[0.92] tracking-[-0.03em] text-[clamp(56px,8vw,128px)]">
              Think <span className="italic font-light text-[#c54a2a]">like</span><br />
              a physician.
              <span className="block font-sans font-medium not-italic text-[#161410] mt-2 text-[0.55em] tracking-[-0.02em]">
                Built to bring out the physician in you.
              </span>
            </h1>
            <div className="flex gap-6 mt-7">
              <div>
                <div className="font-serif font-semibold text-4xl tracking-tight">10k+</div>
                <div className="font-mono text-[10px] uppercase tracking-[0.12em] opacity-60 mt-1">Practice items</div>
              </div>
              <div>
                <div className="font-serif font-semibold text-4xl tracking-tight">7</div>
                <div className="font-mono text-[10px] uppercase tracking-[0.12em] opacity-60 mt-1">Content areas</div>
              </div>
              <div>
                <div className="font-serif font-semibold text-4xl tracking-tight">24/7</div>
                <div className="font-mono text-[10px] uppercase tracking-[0.12em] opacity-60 mt-1">Voice tutor</div>
              </div>
            </div>
          </div>
          <div className="text-[15px] leading-relaxed max-w-sm text-[#161410cc]">
            Practice across Bio/Biochem, Chem/Phys, Psych/Soc, and CARS. Ask anything. Hear feedback. Build the instincts that score 520+.
          </div>
        </section>

        <section className="grid grid-cols-2 md:grid-cols-4 border-b border-[#16141015]">
          <Link
            href="/tutor"
            className="p-7 border-r border-[#16141015] cursor-pointer transition-colors bg-[#161410] text-[#f3efe7] hover:bg-[#2a2620] flex flex-col gap-2"
          >
            <div className="font-mono text-[11px] opacity-70 tracking-[0.12em]">01</div>
            <div className="font-serif text-[22px] font-medium tracking-tight">Ask the tutor</div>
            <div className="text-[13px] opacity-70 leading-relaxed">Conversational explanations for any MCAT concept.</div>
          </Link>
          <Link
            href="/voice-cases"
            className="p-7 border-r border-[#16141015] hover:bg-[#1614100a] transition-colors flex flex-col gap-2"
          >
            <div className="font-mono text-[11px] opacity-50 tracking-[0.12em]">02</div>
            <div className="font-serif text-[22px] font-medium tracking-tight">Voice cases</div>
            <div className="text-[13px] opacity-70 leading-relaxed">Talk through patient scenarios out loud.</div>
          </Link>
          <div className="p-7 border-r border-[#16141015] flex flex-col gap-2 cursor-not-allowed opacity-70">
            <div className="font-mono text-[11px] opacity-50 tracking-[0.12em]">03</div>
            <div className="font-serif text-[22px] font-medium tracking-tight">Study guides</div>
            <div className="text-[13px] opacity-70 leading-relaxed">Personalized summaries — coming soon.</div>
          </div>
          <div className="p-7 flex flex-col gap-2 cursor-not-allowed opacity-70">
            <div className="font-mono text-[11px] opacity-50 tracking-[0.12em]">04</div>
            <div className="font-serif text-[22px] font-medium tracking-tight">Practice sets</div>
            <div className="text-[13px] opacity-70 leading-relaxed">Adaptive question bank — coming soon.</div>
          </div>
        </section>

        <section className="px-10 py-20 text-center">
          <h2 className="font-serif italic font-light text-[clamp(36px,5vw,64px)] leading-[1.05] tracking-[-0.02em] max-w-3xl mx-auto">
            Ready to think like a <span className="text-[#c54a2a] not-italic font-medium">physician?</span>
          </h2>
          <Link
            href="/tutor"
            className="inline-block mt-8 font-mono text-xs uppercase tracking-[0.08em] bg-[#161410] text-[#f3efe7] px-6 py-3.5 rounded-full hover:bg-[#2a2620] transition-colors"
          >
            Start the tutor →
          </Link>
        </section>

        <div className="mx-10 my-7 p-3.5 px-5 border border-dashed border-[#16141025] rounded-lg font-mono text-[12px] leading-relaxed opacity-60">
          Vitalis is a study aid. It is not medical advice and is not a substitute for a clinical educator. All content is for MCAT preparation only.
        </div>

        <footer className="px-10 py-10 border-t border-[#16141015] flex justify-between items-center font-mono text-[11px] tracking-[0.1em] uppercase opacity-60">
          <div>© 2026 Vitalis · Built for future physicians</div>
          <div>v0.1 — beta</div>
        </footer>
      </div>
    </div>
  );
}