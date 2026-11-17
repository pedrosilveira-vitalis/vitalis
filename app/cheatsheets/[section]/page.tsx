import Link from "next/link";
import { notFound } from "next/navigation";
import MainNav from "@/components/MainNav";
import NoriSubject from "@/components/NoriSubject";
import { sectionMeta, sheetFor, unitsFor } from "@/lib/cheatsheets";

export default async function SectionCheatSheets({
  params,
}: {
  params: Promise<{ section: string }>;
}) {
  const { section: sectionId } = await params;
  const section = sectionMeta(sectionId);
  if (!section) notFound();

  const units = unitsFor(section.id);

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="absolute top-0 right-0 w-[900px] h-[500px] opacity-[0.07] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4"
          style={{ background: section.accent }}
        />
      </div>
      <div className="relative z-10">
        <MainNav badge="Cheat sheets" />

        <section className="px-10 pt-14 pb-8 border-b border-[#0c1a2e15] relative">
          <Link
            href="/cheatsheets"
            className="font-sans text-[11px] tracking-[0.12em] uppercase opacity-55 hover:opacity-100"
          >
            &larr; All subjects
          </Link>
          <div className="mt-5 pr-40">
            <div
              className="font-sans text-[10px] tracking-[0.14em] uppercase mb-3 font-semibold"
              style={{ color: section.accent }}
            >
              {section.short}
            </div>
            <h1 className="font-sans font-normal leading-[0.98] tracking-[-0.03em] text-[clamp(36px,4.5vw,64px)]">
              {section.name}
            </h1>
            <p className="text-[15px] opacity-70 mt-3 max-w-xl leading-relaxed">{section.blurb}</p>
          </div>
          <NoriSubject
            prop={section.prop}
            accent={section.accent}
            className="hidden md:block absolute right-10 bottom-0 w-36 pointer-events-none"
          />
        </section>

        <section className="px-10 py-10 grid sm:grid-cols-2 lg:grid-cols-3 gap-4 max-w-5xl">
          {units.map(unit => {
            const sheet = sheetFor(section.id, unit.id);
            if (!sheet) {
              return (
                <div
                  key={unit.id}
                  className="rounded-2xl border-2 border-dashed border-[#0c1a2e20] p-6 opacity-55"
                >
                  <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-60 mb-2">
                    Unit {unit.number}
                  </div>
                  <h2 className="font-sans text-lg font-medium leading-tight">{unit.title}</h2>
                  <div className="font-sans text-[11px] tracking-[0.1em] uppercase mt-4 opacity-60">
                    Not written yet
                  </div>
                </div>
              );
            }
            return (
              <Link
                key={unit.id}
                href={`/cheatsheets/${section.id}/${unit.id}`}
                className="rounded-2xl border-2 p-6 transition-transform hover:-translate-y-0.5 bg-[#fcfaf6]"
                style={{ borderColor: section.accent }}
              >
                <div
                  className="font-sans text-[10px] tracking-[0.14em] uppercase mb-2 font-semibold"
                  style={{ color: section.accent }}
                >
                  Unit {unit.number}
                </div>
                <h2 className="font-sans text-lg font-medium leading-tight">{unit.title}</h2>
                <p className="text-[12px] opacity-65 mt-3 leading-relaxed line-clamp-3">{sheet.summary}</p>
                <div
                  className="font-sans text-[11px] tracking-[0.1em] uppercase mt-4"
                  style={{ color: section.accent }}
                >
                  Open &rarr;
                </div>
              </Link>
            );
          })}
        </section>
      </div>
    </div>
  );
}
