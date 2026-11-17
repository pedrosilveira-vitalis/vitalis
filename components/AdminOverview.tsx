"use client";

import { Fragment, useEffect, useState } from "react";
import Link from "next/link";

type Person = {
  email: string;
  name: string | null;
  plan: string | null;
  windowDays: number | null;
  paid: string | null;
  referral: string | null;
  expiresAt: string | null;
};

type Detail = {
  email: string;
  lessonsRead: number;
  attempted: number;
  correct: number;
  accuracy: number | null;
  lastSeen: string | null;
  daysActive: number;
  missed: { questionId: number; lesson: string | null; lessonId: number; question: string | null; chose: string; answer: string | null }[];
  purchases: { plan: string; windowDays: number; amountCents: number; expiresAt: string; referral: string | null }[];
};

type Overview = {
  people: Person[];
  totals: { signups: number; purchases: number; active: number; referred: number; gross: string; tutorOwed: string };
  referrals: { code: string; sales: number }[];
  error?: string;
};

function daysLeft(expiresAt: string | null): number | null {
  if (!expiresAt) return null;
  return Math.max(0, Math.ceil((new Date(expiresAt).getTime() - Date.now()) / 86400000));
}

export default function AdminOverview() {
  const [data, setData] = useState<Overview | null>(null);
  const [error, setError] = useState("");
  const [open, setOpen] = useState<string | null>(null);
  const [detail, setDetail] = useState<Detail | null>(null);

  function inspect(email: string) {
    if (open === email) { setOpen(null); setDetail(null); return; }
    setOpen(email);
    setDetail(null);
    fetch(`/api/admin/student?email=${encodeURIComponent(email)}`)
      .then(response => response.json())
      .then(payload => (payload.error ? setError(payload.error) : setDetail(payload)))
      .catch(() => setError("Could not load this student."));
  }

  useEffect(() => {
    fetch("/api/admin/overview")
      .then(response => response.json())
      .then(payload => (payload.error ? setError(payload.error) : setData(payload)))
      .catch(() => setError("Could not load the overview."));
  }, []);

  if (error) {
    return <section className="px-10 py-12"><p className="text-[15px] opacity-70">{error}</p></section>;
  }
  if (!data) {
    return <section className="px-10 py-12"><p className="text-[15px] opacity-50">Loading&hellip;</p></section>;
  }

  const tiles: { label: string; value: string | number; note?: string }[] = [
    { label: "Signed up", value: data.totals.signups },
    { label: "Paying now", value: data.totals.active, note: `${data.totals.purchases} purchases all time` },
    { label: "Gross", value: data.totals.gross, note: "before Stripe fees" },
    { label: "Owed to tutors", value: data.totals.tutorOwed, note: `${data.totals.referred} referred sales` },
  ];

  return (
    <>
      <section className="px-10 py-10 grid sm:grid-cols-2 lg:grid-cols-4 gap-4 max-w-6xl">
        {tiles.map(tile => (
          <div key={tile.label} className="rounded-2xl border-2 border-[#0c1a2e25] p-6">
            <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">{tile.label}</div>
            <div className="font-sans text-4xl font-medium tracking-tight leading-none">{tile.value}</div>
            {tile.note && <div className="font-sans text-[11px] opacity-50 mt-2">{tile.note}</div>}
          </div>
        ))}
      </section>

      <section className="px-10 pb-6 max-w-6xl">
        <Link
          href="/admin/calls"
          className="inline-flex items-center gap-2 rounded-xl bg-[#245574] text-[#f5f1ea] px-6 py-4 font-sans text-sm font-medium"
        >
          Schedule a session &rarr;
        </Link>
        <p className="text-[13px] opacity-60 mt-3 max-w-xl leading-relaxed">
          Complete includes a live group review before every MCAT date in a student&rsquo;s window. Schedule
          those here; each one shows up on the student&rsquo;s calls page.
        </p>
      </section>

      <section className="px-10 pb-14 max-w-6xl">
        <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-55 mb-3">
          People ({data.people.length}) &mdash; click a row for detail
        </div>
        {data.people.length === 0 ? (
          <div className="rounded-2xl border-2 border-dashed border-[#0c1a2e25] p-10 text-center">
            <div className="font-sans text-xl font-light opacity-60">Nobody has signed up yet.</div>
          </div>
        ) : (
          <div className="rounded-2xl border-2 border-[#0c1a2e25] overflow-hidden">
            <table className="w-full text-[13px]">
              <thead>
                <tr className="bg-[#0c1a2e08] font-sans text-[10px] tracking-[0.12em] uppercase opacity-60">
                  <th className="text-left px-5 py-3 font-medium">Student</th>
                  <th className="text-left px-5 py-3 font-medium">Plan</th>
                  <th className="text-left px-5 py-3 font-medium">Paid</th>
                  <th className="text-left px-5 py-3 font-medium">Days left</th>
                  <th className="text-left px-5 py-3 font-medium">Referral</th>
                </tr>
              </thead>
              <tbody>
                {data.people.map(person => {
                  const left = daysLeft(person.expiresAt);
                  return (
                    <Fragment key={person.email}>
                    <tr
                      onClick={() => inspect(person.email)}
                      className="border-t border-[#0c1a2e12] cursor-pointer hover:bg-[#0c1a2e06]"
                    >
                      <td className="px-5 py-3">
                        <div className="font-medium">{person.name || person.email}</div>
                        {person.name && <div className="opacity-55 text-[12px]">{person.email}</div>}
                      </td>
                      <td className="px-5 py-3">
                        {person.plan ? (
                          <span className="inline-block rounded-full bg-[#5b7a6418] text-[#5b7a64] px-3 py-1 text-[11px] font-medium">
                            {person.plan}
                          </span>
                        ) : (
                          <span className="opacity-45">&mdash;</span>
                        )}
                      </td>
                      <td className="px-5 py-3">{person.paid ?? <span className="opacity-45">&mdash;</span>}</td>
                      <td className="px-5 py-3">
                        {left === null ? (
                          <span className="opacity-45">&mdash;</span>
                        ) : (
                          <span className={left <= 14 ? "text-[#a8324a] font-medium" : ""}>
                            {left}
                            {left <= 14 && " \u00b7 renewing soon"}
                          </span>
                        )}
                      </td>
                      <td className="px-5 py-3">
                        {person.referral ?? <span className="opacity-45">&mdash;</span>}
                      </td>
                    </tr>
                    {open === person.email && (
                      <tr className="border-t border-[#0c1a2e12] bg-[#0c1a2e05]">
                        <td colSpan={5} className="px-5 py-5">
                          {!detail ? (
                            <span className="opacity-50">Loading&hellip;</span>
                          ) : (
                            <div className="space-y-5">
                              <div className="flex flex-wrap gap-8">
                                {[
                                  ["Lessons read", String(detail.lessonsRead)],
                                  ["Questions answered", String(detail.attempted)],
                                  ["Accuracy", detail.accuracy === null ? "\u2014" : `${detail.accuracy}%`],
                                  ["Days practised", String(detail.daysActive)],
                                  ["Last seen", detail.lastSeen ? new Date(detail.lastSeen).toLocaleDateString() : "\u2014"],
                                ].map(([label, value]) => (
                                  <div key={label}>
                                    <div className="font-sans text-[10px] tracking-[0.12em] uppercase opacity-50 mb-1">{label}</div>
                                    <div className="font-sans text-xl font-medium">{value}</div>
                                  </div>
                                ))}
                              </div>

                              <div>
                                <div className="font-sans text-[10px] tracking-[0.12em] uppercase opacity-50 mb-2">
                                  Getting wrong ({detail.missed.length})
                                </div>
                                {detail.missed.length === 0 ? (
                                  <p className="opacity-55 text-[13px]">
                                    Nothing recorded yet. Missed questions appear here once they work through a
                                    lesson&rsquo;s questions.
                                  </p>
                                ) : (
                                  <ul className="space-y-2">
                                    {detail.missed.map(item => (
                                      <li key={item.questionId} className="rounded-xl border border-[#0c1a2e18] px-4 py-3">
                                        <div className="text-[13px] leading-relaxed">{item.question}</div>
                                        <div className="font-sans text-[11px] opacity-60 mt-1.5">
                                          {item.lesson} &middot; chose {item.chose}, answer was {item.answer}
                                        </div>
                                      </li>
                                    ))}
                                  </ul>
                                )}
                              </div>

                              {detail.purchases.length > 0 && (
                                <div>
                                  <div className="font-sans text-[10px] tracking-[0.12em] uppercase opacity-50 mb-2">
                                    Purchases
                                  </div>
                                  <ul className="space-y-1 text-[13px]">
                                    {detail.purchases.map(buy => (
                                      <li key={buy.expiresAt}>
                                        {buy.plan} &middot; {buy.windowDays} days &middot; $
                                        {(buy.amountCents / 100).toFixed(2)} &middot; until{" "}
                                        {new Date(buy.expiresAt).toLocaleDateString()}
                                        {buy.referral && ` \u00b7 ${buy.referral}`}
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                            </div>
                          )}
                        </td>
                      </tr>
                    )}
                    </Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {data.referrals.length > 0 && (
        <section className="px-10 pb-16 max-w-6xl">
          <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-55 mb-3">
            Referral codes &mdash; $100 owed per sale
          </div>
          <div className="rounded-2xl border-2 border-[#0c1a2e25] divide-y divide-[#0c1a2e12]">
            {data.referrals.map(entry => (
              <div key={entry.code} className="flex items-center justify-between px-5 py-3">
                <span className="font-sans font-medium">{entry.code}</span>
                <span className="text-[13px] opacity-70">
                  {entry.sales} {entry.sales === 1 ? "sale" : "sales"} &middot; ${entry.sales * 100} owed
                </span>
              </div>
            ))}
          </div>
        </section>
      )}
    </>
  );
}
