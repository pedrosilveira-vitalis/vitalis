import Link from "next/link";
import MainNav from "@/components/MainNav";
import NoriSubject from "@/components/NoriSubject";
import { CHEAT_SHEETS, SECTIONS, sheetsFor, unitsFor } from "@/lib/cheatsheets";

export const metadata = { title: "Cheat sheets | Vitalis" };

export default function CheatSheetsPage() {
  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[900px] h-[500px] bg-[#245574] opacity-[0.05] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
      </div>
      <div className="relative z-10">
        <MainNav badge="Cheat sheets" />

        <section className="px-10 pt-14 pb-8 border-b border-[#0c1a2e15]">
          <div className="font-sans text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Cheat sheets
          </div>
          <h1 className="font-sans font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(44px,5.5vw,80px)] max-w-4xl">
            One page. <span className="italic font-light text-[#245574]">One unit.</span>
          </h1>
          <p className="text-[15px] opacity-70 mt-4 max-w-xl leading-relaxed">
            Everything a unit is actually tested on, condensed to a single sheet you can read the night before
            &mdash; including the places students reliably lose points.
          </p>
          <p className="font-sans text-[11px] tracking-[0.12em] uppercase opacity-50 mt-5">
            {CHEAT_SHEETS.length} of 28 published
          </p>
        </section>

        <section className="px-10 py-12 grid sm:grid-cols-2 gap-6 max-w-5xl">
          {SECTIONS.map(section => {
            const published = sheetsFor(section.id).length;
            const total = unitsFor(section.id).length;
            return (
              <Link
                key={section.id}
                href={`/cheatsheets/${section.id}`}
                className="group relative overflow-hidden rounded-2xl p-7 pb-6 border-2 transition-transform hover:-translate-y-1"
                style={{ borderColor: section.accent, background: section.tint }}
              >
                <div className="relative z-10 pr-28">
                  <div
                    className="font-sans text-[10px] tracking-[0.14em] uppercase mb-2 font-semibold"
                    style={{ color: section.accent }}
                  >
                    {section.short}
                  </div>
                  <h2 className="font-sans text-2xl font-medium tracking-tight leading-tight mb-2">
                    {section.name}
                  </h2>
                  <p className="text-[13px] opacity-70 leading-relaxed">{section.blurb}</p>
                  <div className="mt-5 font-sans text-[11px] tracking-[0.1em] uppercase" style={{ color: section.accent }}>
                    {`${published} of ${total} ready`} &nbsp;&rarr;
                  </div>
                </div>
                <NoriSubject
                  prop={section.prop}
                  accent={section.accent}
                  className="absolute -right-3 -bottom-3 w-32 opacity-90 pointer-events-none"
                />
              </Link>
            );
          })}
        </section>
      </div>
    </div>
  );
}
