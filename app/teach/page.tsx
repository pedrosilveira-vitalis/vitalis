"use client";

import { useState } from "react";
import MainNav from "@/components/MainNav";

const TERMS = [
  { amount: "100%", label: "of your own rate", note: "We take nothing from your sessions. You set your price and bill your students however you already do." },
  { amount: "$100", label: "per student who joins", note: "Every time a student signs up for Complete on your referral code. Paid monthly." },
  { amount: "$200", label: "per group review", note: "For each live review you run before a test date. One session, every Complete student." },
];

export default function TeachPage() {
  const [sent, setSent] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError("");
    const form = new FormData(event.currentTarget);
    try {
      const response = await fetch("/api/teach", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: form.get("name"),
          email: form.get("email"),
          score: Number(form.get("score")),
          experience: form.get("experience"),
          students: form.get("students"),
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Could not send that.");
      setSent(data.code);
    } catch (problem) {
      setError(problem instanceof Error ? problem.message : "Could not send that.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[900px] h-[500px] bg-[#5b7a64] opacity-[0.06] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
      </div>
      <div className="relative z-10">
        <MainNav badge="Teach" />

        <section className="px-10 pt-14 pb-8 border-b border-[#0c1a2e15]">
          <div className="font-sans text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Tutor with Vitalis
          </div>
          <h1 className="font-sans font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(42px,5.5vw,78px)] max-w-4xl">
            Keep your rate. <span className="italic font-light text-[#5b7a64]">Lose the admin.</span>
          </h1>
          <p className="text-[15px] opacity-75 mt-4 max-w-2xl leading-relaxed">
            Most MCAT tutors spend more unpaid hours finding students than they&rsquo;d like to admit. We don&rsquo;t
            want a cut of your rate &mdash; we want your students on a platform good enough that you never
            spend a paid hour re-explaining glycolysis.
          </p>
        </section>

        <section className="px-10 py-10 grid sm:grid-cols-3 gap-5 max-w-5xl">
          {TERMS.map(term => (
            <div key={term.label} className="rounded-2xl border-2 border-[#0c1a2e20] p-6">
              <div className="font-sans text-4xl font-medium tracking-tight text-[#5b7a64]">{term.amount}</div>
              <div className="font-sans text-[13px] font-medium mt-1">{term.label}</div>
              <p className="text-[13px] opacity-65 mt-3 leading-relaxed">{term.note}</p>
            </div>
          ))}
        </section>

        <section className="px-10 pb-10 max-w-3xl">
          <h2 className="font-sans text-2xl font-medium mb-4">What you get to work with</h2>
          <ul className="space-y-2.5">
            {[
              "250 lessons, each one reviewed line by line against published sources",
              "1,250 practice questions with a full written explanation on every answer",
              "28 unit cheat sheets your students can print",
              "A dashboard showing exactly which questions each of your students is getting wrong",
            ].map(item => (
              <li key={item} className="flex gap-3 text-[14px] leading-relaxed">
                <span className="text-[#5b7a64] mt-0.5" aria-hidden="true">&#10003;</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
          <p className="text-[14px] opacity-70 mt-5 leading-relaxed">
            We ask for a 515 or better, and that you&rsquo;ve tutored at least a few students before.
          </p>
        </section>

        <section className="px-10 pb-16 max-w-xl">
          {sent ? (
            <div className="rounded-2xl border-2 border-[#5b7a64] bg-[#5b7a6410] p-7">
              <h2 className="font-sans text-xl font-medium mb-2">Got it &mdash; thank you.</h2>
              <p className="text-[14px] opacity-75 leading-relaxed mb-4">
                Pedro reads every application himself and will come back to you within two days. Your referral
                code is reserved:
              </p>
              <div className="font-mono text-2xl font-medium text-[#5b7a64]">{sent}</div>
            </div>
          ) : (
            <form onSubmit={submit} className="space-y-4">
              <h2 className="font-sans text-2xl font-medium">Apply</h2>
              {[
                { name: "name", label: "Your name", type: "text", required: true },
                { name: "email", label: "Email", type: "email", required: true },
                { name: "score", label: "MCAT score", type: "number", required: true },
              ].map(field => (
                <label key={field.name} className="block">
                  <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">{field.label}</div>
                  <input
                    name={field.name}
                    type={field.type}
                    required={field.required}
                    className="w-full px-4 py-3 border-2 border-[#0c1a2e25] rounded-xl bg-transparent outline-none focus:border-[#5b7a64] transition-colors font-sans"
                  />
                </label>
              ))}
              <label className="block">
                <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">
                  Students you could bring with you
                </div>
                <input
                  name="students"
                  placeholder="e.g. 4 current, 2 starting in January"
                  className="w-full px-4 py-3 border-2 border-[#0c1a2e25] rounded-xl bg-transparent outline-none focus:border-[#5b7a64] transition-colors font-sans"
                />
              </label>
              <label className="block">
                <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">
                  How you tutor, briefly
                </div>
                <textarea
                  name="experience"
                  rows={4}
                  className="w-full px-4 py-3 border-2 border-[#0c1a2e25] rounded-xl bg-transparent outline-none focus:border-[#5b7a64] transition-colors font-sans resize-y"
                />
              </label>
              {error && <div className="text-[13px] text-[#a8324a]">{error}</div>}
              <button
                type="submit"
                disabled={busy}
                className="rounded-xl bg-[#5b7a64] text-[#f5f1ea] px-7 py-4 font-sans text-sm font-medium disabled:opacity-50"
              >
                {busy ? "Sending…" : "Send application"}
              </button>
            </form>
          )}
        </section>
      </div>
    </div>
  );
}
