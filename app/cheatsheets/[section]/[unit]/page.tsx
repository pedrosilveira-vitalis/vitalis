import Link from "next/link";
import { notFound } from "next/navigation";
import { auth } from "@/auth";
import MainNav from "@/components/MainNav";
import NoriSubject from "@/components/NoriSubject";
import { capabilitiesFor } from "@/lib/billing";
import { portalDb } from "@/lib/portal-db";
import { sectionMeta, sheetFor, type Block } from "@/lib/cheatsheets";

function BlockView({ block, accent }: { block: Block; accent: string }) {
  const heading = (
    <h2
      className="font-sans text-[10px] tracking-[0.14em] uppercase font-semibold mb-3"
      style={{ color: block.kind === "trap" ? "#a8324a" : accent }}
    >
      {block.heading}
    </h2>
  );

  if (block.kind === "formulas") {
    return (
      <section className="break-inside-avoid mb-7">
        {heading}
        <div className="space-y-2.5">
          {block.items.map(item => (
            <div key={item.label} className="rounded-xl border border-[#0c1a2e18] px-4 py-3 bg-[#fcfaf6]">
              <div className="font-sans text-[11px] uppercase tracking-[0.1em] opacity-55 mb-1">{item.label}</div>
              <div className="font-mono text-[15px]">{item.formula}</div>
              {item.note && <div className="text-[12px] opacity-60 mt-1">{item.note}</div>}
            </div>
          ))}
        </div>
      </section>
    );
  }

  if (block.kind === "table") {
    return (
      <section className="break-inside-avoid mb-7">
        {heading}
        <div className="rounded-xl border border-[#0c1a2e18] overflow-hidden">
          <table className="w-full text-[13px]">
            <thead>
              <tr className="bg-[#0c1a2e08]">
                {block.columns.map(column => (
                  <th key={column} className="text-left px-3 py-2 font-sans text-[10px] tracking-[0.1em] uppercase opacity-60 font-medium">
                    {column}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {block.rows.map(row => (
                <tr key={row.join("|")} className="border-t border-[#0c1a2e12]">
                  {row.map((cell, index) => (
                    <td key={index} className={`px-3 py-2 align-top ${index === 0 ? "font-medium" : "opacity-80"}`}>
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    );
  }

  const isTrap = block.kind === "trap";
  return (
    <section className="break-inside-avoid mb-7">
      {heading}
      <ul className={`space-y-2 ${isTrap ? "rounded-xl border-2 border-[#a8324a35] bg-[#a8324a08] px-4 py-3.5" : ""}`}>
        {block.items.map(item => (
          <li key={item} className="flex gap-2.5 text-[13.5px] leading-relaxed">
            <span className="mt-[7px] w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: isTrap ? "#a8324a" : accent }} />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default async function CheatSheetPage({
  params,
}: {
  params: Promise<{ section: string; unit: string }>;
}) {
  const { section: sectionId, unit } = await params;
  const section = sectionMeta(sectionId);
  const sheet = section ? sheetFor(section.id, Number(unit)) : undefined;
  if (!section || !sheet) notFound();

  const email = (await auth())?.user?.email;
  const capabilities = await capabilitiesFor(await portalDb(), email);

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans">
      <div className="print:hidden">
        <MainNav badge="Cheat sheets" />
      </div>

      <article className="px-10 py-10 max-w-4xl mx-auto">
        <Link
          href={`/cheatsheets/${section.id}`}
          className="print:hidden font-sans text-[11px] tracking-[0.12em] uppercase opacity-55 hover:opacity-100"
        >
          &larr; {section.name}
        </Link>

        <header
          className="mt-5 pb-6 mb-8 border-b-2 flex items-start justify-between gap-6"
          style={{ borderColor: section.accent }}
        >
          <div className="min-w-0">
            <div
              className="font-sans text-[10px] tracking-[0.14em] uppercase font-semibold mb-2"
              style={{ color: section.accent }}
            >
              {section.short} &middot; Unit cheat sheet
            </div>
            <h1 className="font-sans text-[clamp(30px,4vw,48px)] font-medium tracking-tight leading-[1.05]">
              {sheet.unit}
            </h1>
            <p className="text-[14px] opacity-75 mt-3 leading-relaxed max-w-2xl">{sheet.summary}</p>
          </div>
          <NoriSubject
            prop={section.prop}
            accent={section.accent}
            className="hidden sm:block w-24 flex-shrink-0 pointer-events-none print:hidden"
          />
        </header>

        {capabilities.lessons ? (
          <>
            <div className="md:columns-2 md:gap-10">
              {sheet.blocks.map(block => (
                <BlockView key={block.heading} block={block} accent={section.accent} />
              ))}
            </div>
            <footer className="print:hidden mt-6 pt-6 border-t border-[#0c1a2e15] flex flex-wrap gap-3 items-center">
              <Link
                href={`/study/${section.id}`}
                className="rounded-xl px-5 py-3 font-sans text-sm font-medium text-[#f5f1ea]"
                style={{ background: section.accent }}
              >
                Study this unit in full &rarr;
              </Link>
              <span className="text-[12px] opacity-55">Print this page for a paper copy.</span>
            </footer>
          </>
        ) : (
          <>
            <div className="relative">
              <div className="md:columns-2 md:gap-10 max-h-[260px] overflow-hidden" aria-hidden="true">
                {sheet.blocks.map(block => (
                  <BlockView key={block.heading} block={block} accent={section.accent} />
                ))}
              </div>
              <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-b from-transparent to-[#f5f1ea]" />
            </div>
            <div className="rounded-2xl border-2 p-7 mt-2" style={{ borderColor: section.accent }}>
              <h2 className="font-sans text-xl font-medium mb-2">The rest of this sheet is part of Complete.</h2>
              <p className="text-[14px] opacity-70 leading-relaxed mb-5 max-w-xl">
                Cheat sheets come with the written lessons. Complete includes all 250 lessons, all 1,250
                questions, and a live review before every test date in your window.
              </p>
              <Link
                href="/plans"
                className="inline-block rounded-xl px-6 py-3.5 font-sans text-sm font-medium text-[#f5f1ea]"
                style={{ background: section.accent }}
              >
                See plans &rarr;
              </Link>
            </div>
          </>
        )}
      </article>
    </div>
  );
}
