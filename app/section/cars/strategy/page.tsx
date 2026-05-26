"use client";

import { useState } from "react";
import Link from "next/link";

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

const SECTIONS = [
  { id: "shift", number: "01", title: "The mental shift" },
  { id: "read", number: "02", title: "How to read a passage" },
  { id: "types", number: "03", title: "The 3 question types" },
  { id: "traps", number: "04", title: "Answer-elimination playbook" },
  { id: "pacing", number: "05", title: "Pacing & endurance" },
  { id: "example", number: "06", title: "Walked-through example" },
  { id: "card", number: "07", title: "Quick reference" },
];

export default function CarsStrategyPage() {
  const [activeSection, setActiveSection] = useState("shift");

  function scrollTo(id: string) {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
      setActiveSection(id);
    }
  }

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans">
      <nav className="flex items-center justify-between px-10 py-5 border-b border-[#0c1a2e15] sticky top-0 bg-[#f5f1ea] z-30">
        <Logo />
        <div className="hidden md:flex gap-6 text-sm font-medium">
          <Link href="/" className="opacity-60 hover:opacity-100">Home</Link>
          <Link href="/tutor" className="opacity-60 hover:opacity-100">Tutor</Link>
          <Link href="/practice" className="opacity-60 hover:opacity-100">Practice</Link>
          <Link href="/flashcards" className="opacity-60 hover:opacity-100">Flashcards</Link>
          <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
          <Link href="/score-calculator" className="opacity-60 hover:opacity-100">Score Calc</Link>
        </div>
        <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">CARS Strategy</div>
      </nav>

      <header className="px-10 pt-14 pb-10 border-b border-[#0c1a2e15] max-w-5xl">
        <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
          <span className="w-10 h-px bg-[#4a3b6b] opacity-60" />
          Section · CARS · Strategy guide
        </div>
        <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(40px,6vw,84px)] mb-4">
          How to <span className="italic font-light text-[#4a3b6b]">actually</span> beat CARS.
        </h1>
        <p className="text-[16px] opacity-75 leading-relaxed max-w-2xl">
          CARS isn&apos;t a knowledge test. It&apos;s a reading and reasoning test. Most students lose 5+ points here because they study it like a content section. This guide is built around the moves that actually work — taught the way a strong scorer would explain them to you.
        </p>
      </header>

      <div className="flex max-w-7xl mx-auto">
        <aside className="hidden lg:block w-64 sticky top-[73px] h-fit pl-10 pr-6 pt-10 self-start">
          <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-4">Sections</div>
          <ul className="space-y-2">
            {SECTIONS.map((s) => (
              <li key={s.id}>
                <button
                  onClick={() => scrollTo(s.id)}
                  className={`text-left text-[13px] leading-snug transition-colors block ${
                    activeSection === s.id ? "text-[#4a3b6b] font-medium" : "opacity-70 hover:opacity-100"
                  }`}
                >
                  <span className="font-mono text-[10px] opacity-50 mr-2">{s.number}</span>
                  {s.title}
                </button>
              </li>
            ))}
          </ul>
          <div className="mt-8 pt-6 border-t border-[#0c1a2e15]">
            <Link href="/tutor" className="block font-mono text-[10px] tracking-[0.1em] uppercase opacity-60 hover:opacity-100 leading-snug">
              Have a CARS question? →<br />Ask the tutor
            </Link>
          </div>
        </aside>

        <main className="flex-1 px-10 py-14 max-w-3xl">
          <section id="shift" className="mb-20 scroll-mt-24">
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-2">01 — The mental shift</div>
            <h2 className="font-serif text-[clamp(28px,4vw,44px)] font-medium tracking-tight mb-5 leading-tight">
              CARS rewards the careful reader, not the smart one.
            </h2>
            <p className="text-[15px] leading-relaxed mb-4">
              Almost every premed walks into CARS treating it like the other sections: read fast, look for the answer in the passage, move on. That approach scores about a 124. To score 128+, you need a different mindset.
            </p>
            <p className="text-[15px] leading-relaxed mb-4">
              Here&apos;s the shift: <strong>the passage is the entire universe.</strong> Anything you &quot;know&quot; from outside the passage is irrelevant, and worse, it&apos;s often the source of trap answers. CARS isn&apos;t asking what you know. It&apos;s asking <em>can you precisely understand and reason from what this author wrote?</em>
            </p>
            <p className="text-[15px] leading-relaxed mb-6">
              The strong CARS scorer doesn&apos;t read faster. They read with intention. They&apos;re tracking the author&apos;s argument like a detective tracking a suspect — noticing what they emphasize, where they hedge, when the tone shifts, who they&apos;re arguing against. The passage is alive. Questions are easier when you actually understand who&apos;s talking and what they want.
            </p>
            <div className="bg-[#4a3b6b0a] border border-[#4a3b6b25] rounded-2xl p-6 mb-2">
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Three principles to internalize</div>
              <ul className="space-y-2.5 text-[14px] leading-relaxed">
                <li className="flex gap-3"><span className="text-[#4a3b6b] font-semibold flex-shrink-0">→</span><span><strong>Trust the passage.</strong> Not your gut, not your prior knowledge, not what &quot;sounds right&quot; — only what the author actually argued.</span></li>
                <li className="flex gap-3"><span className="text-[#4a3b6b] font-semibold flex-shrink-0">→</span><span><strong>The author has a position.</strong> They&apos;re not a neutral encyclopedia. Find out what they think and how strongly.</span></li>
                <li className="flex gap-3"><span className="text-[#4a3b6b] font-semibold flex-shrink-0">→</span><span><strong>Wrong answers are usually almost right.</strong> The MCAT writes traps that match the passage in topic but distort it in scope, tone, or detail.</span></li>
              </ul>
            </div>
          </section>

          <section id="read" className="mb-20 scroll-mt-24">
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-2">02 — How to read a passage</div>
            <h2 className="font-serif text-[clamp(28px,4vw,44px)] font-medium tracking-tight mb-5 leading-tight">
              Active reading isn&apos;t taking notes. It&apos;s asking questions.
            </h2>
            <p className="text-[15px] leading-relaxed mb-4">
              Every paragraph should feel like you&apos;re interrogating the author. What are they claiming? Why? What would they say if I disagreed? When you read like this, the passage organizes itself in your head and the questions become navigation problems instead of recall problems.
            </p>
            <h3 className="font-serif text-[22px] font-medium mt-8 mb-3">The 4 questions to ask each paragraph</h3>
            <ol className="space-y-3 text-[14.5px] leading-relaxed mb-6 list-none">
              <li className="flex gap-3"><span className="font-mono font-medium text-[#4a3b6b] flex-shrink-0">01</span><span><strong>What is this paragraph doing?</strong> Setting up context? Making a claim? Giving an example? Refuting someone? Conceding a point? Knowing the <em>function</em> matters more than the content.</span></li>
              <li className="flex gap-3"><span className="font-mono font-medium text-[#4a3b6b] flex-shrink-0">02</span><span><strong>What does the author actually believe here?</strong> Underline (mentally) any opinion language: &quot;regrettably,&quot; &quot;clearly,&quot; &quot;one might argue,&quot; &quot;in truth.&quot; These are tells.</span></li>
              <li className="flex gap-3"><span className="font-mono font-medium text-[#4a3b6b] flex-shrink-0">03</span><span><strong>What is this paragraph reacting to?</strong> CARS authors are almost always in conversation with another viewpoint, even if it&apos;s implicit. Find the &quot;other side.&quot;</span></li>
              <li className="flex gap-3"><span className="font-mono font-medium text-[#4a3b6b] flex-shrink-0">04</span><span><strong>How does this connect to the last paragraph?</strong> Building on it? Pivoting from it? Contradicting it? The connective tissue between paragraphs is where the argument lives.</span></li>
            </ol>
            <h3 className="font-serif text-[22px] font-medium mt-8 mb-3">Watch for signal words</h3>
            <p className="text-[15px] leading-relaxed mb-4">
              CARS passages are dense, but they&apos;re also full of road signs. Train your eye to notice these — they tell you what&apos;s about to happen.
            </p>
            <div className="grid sm:grid-cols-2 gap-3 mb-6">
              <div className="border border-[#0c1a2e15] rounded-xl p-4 bg-[#0c1a2e0a]">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Contrast / shift</div>
                <div className="text-[13px] opacity-80 leading-relaxed">however · yet · but · although · in contrast · nevertheless · on the other hand · despite</div>
              </div>
              <div className="border border-[#0c1a2e15] rounded-xl p-4 bg-[#0c1a2e0a]">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Author&apos;s opinion</div>
                <div className="text-[13px] opacity-80 leading-relaxed">clearly · regrettably · in truth · arguably · should · must · ought to · unfortunately</div>
              </div>
              <div className="border border-[#0c1a2e15] rounded-xl p-4 bg-[#0c1a2e0a]">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Conclusion / claim</div>
                <div className="text-[13px] opacity-80 leading-relaxed">therefore · thus · in short · this suggests · what follows · the upshot</div>
              </div>
              <div className="border border-[#0c1a2e15] rounded-xl p-4 bg-[#0c1a2e0a]">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Concession (still author&apos;s opinion!)</div>
                <div className="text-[13px] opacity-80 leading-relaxed">admittedly · granted · while it&apos;s true that · one might object</div>
              </div>
            </div>
            <p className="text-[15px] leading-relaxed mb-4">
              <strong>Critical insight:</strong> when an author writes &quot;admittedly, some have argued X, but in fact Y,&quot; the author&apos;s real position is Y, not X. Concession language is a trick — they&apos;re acknowledging the opposing view only to dismiss it. Get this wrong and you&apos;ll miss every &quot;author would most agree with&quot; question.
            </p>
            <div className="bg-[#a8324a0a] border border-[#a8324a25] rounded-2xl p-5">
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Don&apos;t do this</div>
              <p className="text-[14px] leading-relaxed">
                Don&apos;t take written notes during CARS. You don&apos;t have time. The note-taking ritual is procrastination disguised as productivity. Build the active-reading habit so your brain takes mental notes by default.
              </p>
            </div>
          </section>

          <section id="types" className="mb-20 scroll-mt-24">
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-2">03 — Question types</div>
            <h2 className="font-serif text-[clamp(28px,4vw,44px)] font-medium tracking-tight mb-5 leading-tight">
              Recognize the question type in 5 seconds.
            </h2>
            <p className="text-[15px] leading-relaxed mb-6">
              The AAMC officially groups CARS questions into three categories. Each one wants something different from you. Knowing which type you&apos;re facing before you read the answer choices is what separates good scorers from great ones.
            </p>
            <div className="space-y-5">
              <div className="border border-[#0c1a2e15] rounded-2xl p-6 bg-[#f5f1ea]">
                <div className="flex items-baseline gap-3 mb-3">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">Type 01 · ~30% of questions</div>
                </div>
                <h3 className="font-serif text-[22px] font-medium mb-2">Foundations of Comprehension</h3>
                <p className="text-[14px] opacity-75 leading-relaxed mb-3"><strong>What it asks:</strong> Did you understand what the passage actually said? Definitions, main ideas, what a specific term meant in context, what the author&apos;s purpose was.</p>
                <p className="text-[14px] opacity-75 leading-relaxed mb-3"><strong>How to spot it:</strong> Questions starting with &quot;The main purpose of...&quot;, &quot;The author uses X to refer to...&quot;, &quot;Which best describes the passage?&quot;</p>
                <div className="bg-[#0c1a2e0a] border border-[#0c1a2e15] rounded-lg p-4">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-1.5">Strategy</div>
                  <p className="text-[13.5px] leading-relaxed">Go back to the relevant part of the passage. Don&apos;t answer from memory. The right answer paraphrases the passage; the trap answer is too narrow, too broad, or imports outside ideas.</p>
                </div>
              </div>
              <div className="border border-[#0c1a2e15] rounded-2xl p-6 bg-[#f5f1ea]">
                <div className="flex items-baseline gap-3 mb-3">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">Type 02 · ~30% of questions</div>
                </div>
                <h3 className="font-serif text-[22px] font-medium mb-2">Reasoning Within the Text</h3>
                <p className="text-[14px] opacity-75 leading-relaxed mb-3"><strong>What it asks:</strong> Can you integrate information across different parts of the passage? Can you find the implicit assumption, follow the argument, identify what evidence supports a claim?</p>
                <p className="text-[14px] opacity-75 leading-relaxed mb-3"><strong>How to spot it:</strong> &quot;The author&apos;s claim that X is best supported by...&quot;, &quot;Which assumption is required for...&quot;, &quot;The author would most likely respond to X by...&quot;</p>
                <div className="bg-[#0c1a2e0a] border border-[#0c1a2e15] rounded-lg p-4">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-1.5">Strategy</div>
                  <p className="text-[13.5px] leading-relaxed">Map the argument structure. Which paragraph is making the claim? Which paragraph is providing evidence? Trap answers often pull from the wrong part of the passage or invert the relationship between claim and support.</p>
                </div>
              </div>
              <div className="border border-[#0c1a2e15] rounded-2xl p-6 bg-[#f5f1ea]">
                <div className="flex items-baseline gap-3 mb-3">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">Type 03 · ~40% of questions · the hardest</div>
                </div>
                <h3 className="font-serif text-[22px] font-medium mb-2">Reasoning Beyond the Text</h3>
                <p className="text-[14px] opacity-75 leading-relaxed mb-3"><strong>What it asks:</strong> Can you apply the passage&apos;s argument to a NEW situation the author never mentions? Can you predict how the author would react to new information?</p>
                <p className="text-[14px] opacity-75 leading-relaxed mb-3"><strong>How to spot it:</strong> &quot;If the author learned that X (new fact not in passage), they would most likely...&quot;, &quot;Which of the following new scenarios is most analogous to...&quot;</p>
                <div className="bg-[#0c1a2e0a] border border-[#0c1a2e15] rounded-lg p-4">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-1.5">Strategy</div>
                  <p className="text-[13.5px] leading-relaxed">Don&apos;t answer about the new scenario directly. Answer based on what the passage&apos;s author <em>cares about</em>. The new info is a test — does it strengthen the author&apos;s argument, weaken it, or leave it untouched? The right answer reflects the author&apos;s priorities, not your common sense.</p>
                </div>
              </div>
            </div>
          </section><section id="traps" className="mb-20 scroll-mt-24">
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-2">04 — Answer-elimination playbook</div>
            <h2 className="font-serif text-[clamp(28px,4vw,44px)] font-medium tracking-tight mb-5 leading-tight">
              The 5 trap-answer patterns to memorize.
            </h2>
            <p className="text-[15px] leading-relaxed mb-6">
              You won&apos;t always know which answer is right. But you can almost always eliminate wrong ones. Most CARS traps follow predictable patterns — once you recognize them by sight, you&apos;ll cut wrong answers in seconds instead of debating with them.
            </p>
            <div className="space-y-4 mb-8">
              <div className="border-l-4 border-[#4a3b6b] pl-5 py-2">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-1">Trap 01</div>
                <div className="font-serif text-[20px] font-medium mb-1">Too extreme / too absolute</div>
                <p className="text-[14px] leading-relaxed opacity-80">
                  Words like &quot;all,&quot; &quot;never,&quot; &quot;always,&quot; &quot;only,&quot; &quot;cannot&quot; — almost always wrong in CARS. Authors hedge. They say &quot;tend to,&quot; &quot;often,&quot; &quot;in most cases.&quot; If an answer claims the author believes X is universally true, it&apos;s almost certainly a trap.
                </p>
              </div>
              <div className="border-l-4 border-[#4a3b6b] pl-5 py-2">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-1">Trap 02</div>
                <div className="font-serif text-[20px] font-medium mb-1">Out of scope</div>
                <p className="text-[14px] leading-relaxed opacity-80">
                  The answer is plausibly true in the real world, but the passage never addressed it. The author never said anything for OR against the claim. These are seductive because they &quot;sound right.&quot; If you can&apos;t point to specific passage support, eliminate.
                </p>
              </div>
              <div className="border-l-4 border-[#4a3b6b] pl-5 py-2">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-1">Trap 03</div>
                <div className="font-serif text-[20px] font-medium mb-1">Half-right, half-wrong</div>
                <p className="text-[14px] leading-relaxed opacity-80">
                  The answer correctly summarizes part of the passage, then adds an extra claim the passage never made — or distorts one detail. Read the WHOLE answer carefully. Half-right is still wrong.
                </p>
              </div>
              <div className="border-l-4 border-[#4a3b6b] pl-5 py-2">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-1">Trap 04</div>
                <div className="font-serif text-[20px] font-medium mb-1">Wrong scope (too narrow or too broad)</div>
                <p className="text-[14px] leading-relaxed opacity-80">
                  The answer focuses on a small detail when the question asks for the main idea (too narrow). Or it generalizes about &quot;all writers&quot; when the passage was only about a specific writer (too broad). Match the answer&apos;s scope to the question&apos;s scope.
                </p>
              </div>
              <div className="border-l-4 border-[#4a3b6b] pl-5 py-2">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-1">Trap 05</div>
                <div className="font-serif text-[20px] font-medium mb-1">Opposite-of-author</div>
                <p className="text-[14px] leading-relaxed opacity-80">
                  The classic. The answer captures the view the author was <em>arguing against</em>, not the author&apos;s own view. If you didn&apos;t track the author&apos;s position carefully while reading, you&apos;ll fall for this every time. Especially common in passages with concession structure (&quot;admittedly... but...&quot;).
                </p>
              </div>
            </div>
            <div className="bg-[#4a3b6b0a] border border-[#4a3b6b25] rounded-2xl p-6">
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">The elimination order</div>
              <p className="text-[14px] leading-relaxed">
                Don&apos;t pick an answer first. Eliminate first. Read all four choices, cross off ones with extreme language, then ones with out-of-scope claims, then ones with half-right distortions. Often you&apos;ll be left with one. If you&apos;re left with two, pick the one with more passage support and move on. <strong>Never spend more than 90 seconds on a single CARS question.</strong>
              </p>
            </div>
          </section>

          <section id="pacing" className="mb-20 scroll-mt-24">
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-2">05 — Pacing & endurance</div>
            <h2 className="font-serif text-[clamp(28px,4vw,44px)] font-medium tracking-tight mb-5 leading-tight">
              90 minutes. 9 passages. The clock is your real opponent.
            </h2>
            <p className="text-[15px] leading-relaxed mb-6">
              CARS gives you 90 minutes for 9 passages with 53 questions. That&apos;s exactly 10 minutes per passage. The students who run out of time aren&apos;t bad readers — they&apos;re slow on individual questions because they didn&apos;t commit. Pacing is half the section.
            </p>
            <div className="grid sm:grid-cols-3 gap-3 mb-6">
              <div className="border border-[#0c1a2e15] rounded-xl p-5 bg-[#0c1a2e0a]">
                <div className="font-serif text-3xl font-medium mb-1 text-[#4a3b6b]">3-4 min</div>
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">Read the passage</div>
                <div className="text-[13px] opacity-75 mt-2">Active reading. No re-reading entire paragraphs. Trust your first pass.</div>
              </div>
              <div className="border border-[#0c1a2e15] rounded-xl p-5 bg-[#0c1a2e0a]">
                <div className="font-serif text-3xl font-medium mb-1 text-[#4a3b6b]">~60s</div>
                <div className="font-mono text-[10px] uppercase tracking-[0.14em] opacity-55">Per question</div>
                <div className="text-[13px] opacity-75 mt-2">Identify the type. Predict the answer if you can. Eliminate. Commit.</div>
              </div>
              <div className="border border-[#0c1a2e15] rounded-xl p-5 bg-[#0c1a2e0a]">
                <div className="font-serif text-3xl font-medium mb-1 text-[#4a3b6b]">10 min</div>
                <div className="font-mono text-[10px] uppercase tracking-[0.14em] opacity-55">Total per passage</div>
                <div className="text-[13px] opacity-75 mt-2">If you&apos;re at 11 min and have 2 questions left, guess and move on. Hard rule.</div>
              </div>
            </div>
            <h3 className="font-serif text-[22px] font-medium mt-8 mb-3">The skip rule</h3>
            <p className="text-[15px] leading-relaxed mb-4">
              If you&apos;ve read a question twice and still can&apos;t commit, flag it and move on. Come back at the end if you have time. Sitting on a question for 3 minutes when 60 seconds didn&apos;t crack it is how students lose 5 questions they could&apos;ve gotten right on later passages.
            </p>
            <h3 className="font-serif text-[22px] font-medium mt-8 mb-3">Endurance is real</h3>
            <p className="text-[15px] leading-relaxed mb-4">
              CARS is the last section of the day before the lunch break (the official order is: Chem/Phys → CARS → break). By passage 6 or 7, your focus is shot. The students who score well train this specifically: do 4-passage timed sets daily, then 9-passage full sections weekly. Don&apos;t do CARS practice in fresh-morning conditions — that&apos;s not test day.
            </p>
          </section>

          <section id="example" className="mb-20 scroll-mt-24">
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-2">06 — Walked-through example</div>
            <h2 className="font-serif text-[clamp(28px,4vw,44px)] font-medium tracking-tight mb-5 leading-tight">
              See the strategy in action.
            </h2>
            <p className="text-[15px] leading-relaxed mb-7">
              Here&apos;s a CARS-style passage and two questions. I&apos;ll walk through exactly what to think at each step — the moves you should be making.
            </p>
            <div className="bg-[#ebe5d6] rounded-2xl p-7 mb-7">
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-3">Sample passage · Philosophy</div>
              <div className="text-[14.5px] leading-relaxed space-y-3 font-serif">
                <p>It has become fashionable in recent decades to dismiss the moral philosophy of the ancient Stoics as a curiosity of intellectual history — a noble but impractical attempt to insulate the self from a world it could not control. Critics argue that Stoic indifference to externals amounts, in practice, to a kind of emotional anesthesia, a withdrawal from the full texture of human life.</p>
                <p>This characterization, while widespread, badly misreads the tradition. The Stoics did not counsel indifference; they counseled discrimination. The relevant distinction is not between caring and not caring, but between caring about what is yours to govern and what is not. To pretend, for instance, that one&apos;s own choices and judgments are not subject to one&apos;s control is not realism but evasion — and the modern preference for explaining every personal failing in terms of forces beyond the self owes more to bad faith than to honest psychology.</p>
                <p>One might object that this picture demands a near-superhuman composure in the face of misfortune. But the objection conflates the Stoic ideal with the Stoic practice. The ideal — the sage who is unmoved by external calamity — was acknowledged by every Stoic from Zeno onward to be vanishingly rare, perhaps never realized. What the tradition actually offered was not a finished state but a direction: the slow, lifelong project of bringing one&apos;s reactions under the supervision of one&apos;s reason. That this project is difficult is not an argument against undertaking it.</p>
              </div>
            </div>
            <div className="border border-[#0c1a2e15] rounded-2xl p-6 mb-5">
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Question 1</div>
              <p className="text-[15px] leading-relaxed mb-4 font-medium">The author&apos;s primary purpose in the passage is to:</p>
              <div className="space-y-2 text-[14px] leading-relaxed mb-5">
                <div className="opacity-70"><strong>A.</strong> demonstrate that Stoic philosophy is incompatible with modern psychology.</div>
                <div className="opacity-70"><strong>B.</strong> defend an ancient philosophical tradition against a common misreading.</div>
                <div className="opacity-70"><strong>C.</strong> argue that emotional restraint is the highest moral virtue.</div>
                <div className="opacity-70"><strong>D.</strong> trace the historical development of Stoic ethics from Zeno onward.</div>
              </div>
              <div className="bg-[#4a3b6b0a] border border-[#4a3b6b25] rounded-lg p-4">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Walkthrough</div>
                <div className="text-[13.5px] leading-relaxed space-y-2">
                  <p><strong>Question type:</strong> Foundations of Comprehension (main purpose). Need to identify what the author is doing across the whole passage, not just one paragraph.</p>
                  <p><strong>Tracking the argument:</strong> Paragraph 1 sets up the critics&apos; view. Paragraph 2 says &quot;this badly misreads&quot; — author is correcting. Paragraph 3 handles an objection. So the author is <em>defending</em> Stoicism against a critique.</p>
                  <p><strong>Eliminating:</strong> (A) Opposite — author never says Stoicism is incompatible with anything; if anything, defends it. (C) Out of scope and too extreme — author never claims restraint is &quot;highest&quot; virtue. (D) Wrong scope — the passage mentions Zeno once, but isn&apos;t a history; it&apos;s an argument.</p>
                  <p className="pt-1"><strong>Answer: B.</strong> &quot;Defend a tradition against a common misreading&quot; matches paragraph 2&apos;s &quot;badly misreads&quot; and the whole argument flow.</p>
                </div>
              </div>
            </div>
            <div className="border border-[#0c1a2e15] rounded-2xl p-6 mb-5">
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Question 2</div>
              <p className="text-[15px] leading-relaxed mb-4 font-medium">The author would most likely respond to a contemporary self-help book that frames all unhappiness as a product of childhood trauma by:</p>
              <div className="space-y-2 text-[14px] leading-relaxed mb-5">
                <div className="opacity-70"><strong>A.</strong> endorsing it as consistent with Stoic teachings about external forces.</div>
                <div className="opacity-70"><strong>B.</strong> dismissing it as an example of the kind of evasion the passage critiques.</div>
                <div className="opacity-70"><strong>C.</strong> suggesting that childhood trauma is irrelevant to adult well-being.</div>
                <div className="opacity-70"><strong>D.</strong> arguing that the book&apos;s authors should study Zeno before writing further.</div>
              </div>
              <div className="bg-[#4a3b6b0a] border border-[#4a3b6b25] rounded-lg p-4">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Walkthrough</div>
                <div className="text-[13.5px] leading-relaxed space-y-2">
                  <p><strong>Question type:</strong> Reasoning Beyond the Text. New scenario (a self-help book) not in passage. Need to apply author&apos;s framework.</p>
                  <p><strong>Key passage move:</strong> Paragraph 2: &quot;the modern preference for explaining every personal failing in terms of forces beyond the self owes more to bad faith than to honest psychology.&quot; Author explicitly dislikes externalizing all personal struggles.</p>
                  <p><strong>Eliminating:</strong> (A) Opposite — the author would NOT endorse this book; it&apos;s exactly the kind of evasion they critique. (C) Too extreme — author doesn&apos;t say trauma is &quot;irrelevant,&quot; just that explaining EVERYTHING by external forces is bad faith. (D) Out of scope / silly — the author isn&apos;t advocating for studying Zeno specifically; it&apos;s a fake-specific answer.</p>
                  <p className="pt-1"><strong>Answer: B.</strong> Directly applies paragraph 2&apos;s critique to the new scenario.</p>
                </div>
              </div>
            </div>
            <div className="bg-[#4a3b6b0a] border border-[#4a3b6b25] rounded-2xl p-6">
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">What this example teaches</div>
              <p className="text-[14px] leading-relaxed">
                Notice how the &quot;walkthrough&quot; for each question was almost entirely about <em>finding the author&apos;s position</em> and matching answers to it. That&apos;s 80% of CARS. You don&apos;t need to be a philosopher to crush a philosophy passage. You need to read carefully, identify what the author actually believes, and refuse to import outside ideas.
              </p>
            </div>
          </section>

          <section id="card" className="mb-16 scroll-mt-24">
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-50 mb-2">07 — Quick reference card</div>
            <h2 className="font-serif text-[clamp(28px,4vw,44px)] font-medium tracking-tight mb-5 leading-tight">
              The one-screen summary.
            </h2>
            <p className="text-[15px] leading-relaxed mb-6">
              Screenshot this. Come back to it. Read it the morning of test day.
            </p>
            <div className="bg-[#0c1a2e] text-[#f5f1ea] rounded-2xl p-8 space-y-6">
              <div>
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-70 mb-2">The mindset</div>
                <p className="text-[14px] leading-relaxed opacity-90">The passage is the entire universe. The author has a position. Trust the passage, not your knowledge or your gut.</p>
              </div>
              <div className="border-t border-[#f5f1ea]/20 pt-5">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-70 mb-2">Reading the passage</div>
                <ul className="text-[13.5px] leading-relaxed space-y-1.5 opacity-90">
                  <li>· Ask: what is this paragraph DOING? What does the author BELIEVE?</li>
                  <li>· Watch for: however, yet, but, in truth, regrettably, clearly</li>
                  <li>· Concession trick: &quot;admittedly X, but Y&quot; → author believes Y</li>
                </ul>
              </div>
              <div className="border-t border-[#f5f1ea]/20 pt-5">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-70 mb-2">Question types</div>
                <ul className="text-[13.5px] leading-relaxed space-y-1.5 opacity-90">
                  <li>· <strong>Comprehension</strong> → go back to the passage, paraphrase what&apos;s there</li>
                  <li>· <strong>Within</strong> → map argument: claim vs. evidence vs. assumption</li>
                  <li>· <strong>Beyond</strong> → apply the author&apos;s priorities to the new scenario</li>
                </ul>
              </div>
              <div className="border-t border-[#f5f1ea]/20 pt-5">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-70 mb-2">The 5 trap patterns</div>
                <ul className="text-[13.5px] leading-relaxed space-y-1.5 opacity-90">
                  <li>· Too extreme (all, never, only)</li>
                  <li>· Out of scope (true in real world, not in passage)</li>
                  <li>· Half-right, half-wrong</li>
                  <li>· Wrong scope (too narrow or too broad)</li>
                  <li>· Opposite-of-author</li>
                </ul>
              </div>
              <div className="border-t border-[#f5f1ea]/20 pt-5">
                <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-70 mb-2">Pacing</div>
                <ul className="text-[13.5px] leading-relaxed space-y-1.5 opacity-90">
                  <li>· 10 min per passage. Hard ceiling.</li>
                  <li>· ~60s per question. If stuck after 90s, flag and move on.</li>
                  <li>· Eliminate first. Don&apos;t pick first.</li>
                </ul>
              </div>
            </div>
          </section>

          <div className="border-t border-[#0c1a2e15] pt-10 mt-10">
            <div className="bg-[#4a3b6b08] border border-[#4a3b6b25] rounded-2xl p-7 text-center">
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-3">Practice the strategy</div>
              <h3 className="font-serif text-[28px] font-medium tracking-tight mb-3">Time to drill.</h3>
              <p className="text-[14px] opacity-75 mb-5 max-w-md mx-auto">
                Strategy without reps is just theory. Try a CARS passage-based question and use the techniques above.
              </p>
              <div className="flex gap-3 justify-center flex-wrap">
                <Link href="/practice/cars?format=passage" className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]">
                  CARS practice →
                </Link>
                <Link href="/tutor" className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a]">
                  Ask the tutor
                </Link>
              </div>
            </div>
          </div>
        </main>
      </div>

      <footer className="px-10 py-10 border-t border-[#0c1a2e15] flex justify-between items-center font-mono text-[11px] tracking-[0.1em] uppercase opacity-60">
        <div>© 2026 Vitalis · CARS strategy guide</div>
        <div><Link href="/section/cars" className="hover:opacity-100 opacity-70">← Back to CARS section</Link></div>
      </footer>
    </div>
  );
}