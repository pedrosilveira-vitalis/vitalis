"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import MainNav from "@/components/MainNav";

type Scored = {
  status: "scored"; attemptId: string; examId: string; finishedAt: string;
  total: number | null; low: number | null; high: number | null; complete: boolean;
  sections: { short: string; scaled: number }[];
};
type Attempt = Scored | { status: "live"; examId: string; attemptId: string; startedAt: string; sectionIndex: number };
type Exam = { id: string; name: string; number: number };

const isScored = (item: Attempt): item is Scored => item.status === "scored";
/** A sitting of a finished form, so it has a total worth charting. */
type Charted = Scored & { total: number; low: number; high: number };
const isCharted = (item: Scored): item is Charted => item.complete && item.total !== null;

/**
 * Every full-length this student has sat, oldest first.
 *
 * The useful thing about a run of full-lengths is not any single score but the
 * shape of the line, so the trend is what this leads with. Section scores sit
 * underneath because a flat total can hide one section climbing while another
 * slides.
 */
export default function ScoreHistoryPage() {
  const [data, setData] = useState<{ exams: Exam[]; attempts: Attempt[] } | null>(null);

  useEffect(() => {
    let live = true;
    fetch("/api/exams")
      .then(response => response.json())
      .then(payload => { if (live) setData(payload); })
      .catch(() => { if (live) setData({ exams: [], attempts: [] }); });
    return () => { live = false; };
  }, []);

  // A sitting of a form that is not finished has no total to chart.
  const scored = (data?.attempts ?? [])
    .filter(isScored)
    .filter(isCharted)
    .sort((a, b) => new Date(a.finishedAt).getTime() - new Date(b.finishedAt).getTime());

  const best = scored.length ? Math.max(...scored.map(item => item.total)) : null;
  const latest = scored.length ? scored[scored.length - 1] : null;
  const first = scored.length ? scored[0] : null;
  const change = first && latest && scored.length > 1 ? latest.total - first.total : null;
  const nameOf = (examId: string) => data?.exams.find(exam => exam.id === examId)?.name ?? examId;

  return (
    <div className="dashboard-page">
      <MainNav badge="Score history" contentId="scores-content" />
      <main id="scores-content" tabIndex={-1} className="study-dashboard">
        <section className="dashboard-welcome">
          <div>
            <p className="eyebrow">EVERY FULL-LENGTH YOU HAVE SAT</p>
            <h1>
              Score <span>history.</span>
            </h1>
            <p>What the line is doing matters more than any single sitting.</p>
          </div>
        </section>

        {!data ? (
          <p className="report-lede">Loading&hellip;</p>
        ) : !scored.length ? (
          <section className="exam-how">
            <h2>Nothing here yet</h2>
            <p>
              Once you finish a full-length its score lands here, alongside every other one, so you can see
              whether the line is moving. Full-Length 1 is free with your account.
            </p>
            <Link href="/exams" className="button-primary">Go to the full-lengths</Link>
          </section>
        ) : (
          <>
            <section className="report-sections">
              <article className="report-section-card">
                <header><span className="eyebrow">LATEST</span><strong>{latest?.total}</strong></header>
                <p className="report-section-name">{latest ? nameOf(latest.examId) : ""}</p>
                <dl>
                  <div><dt>Range</dt><dd>{latest?.low}&ndash;{latest?.high}</dd></div>
                  <div><dt>Sat</dt><dd>{latest ? new Date(latest.finishedAt).toLocaleDateString() : ""}</dd></div>
                </dl>
              </article>
              <article className="report-section-card">
                <header><span className="eyebrow">BEST</span><strong>{best}</strong></header>
                <p className="report-section-name">Across {scored.length} {scored.length === 1 ? "sitting" : "sittings"}</p>
                <dl>
                  <div>
                    <dt>Change since first</dt>
                    <dd>{change === null ? "—" : change > 0 ? `+${change}` : String(change)}</dd>
                  </div>
                </dl>
              </article>
            </section>

            <section className="report-block">
              <h2>Every sitting</h2>
              <p className="report-lede">
                Section scores are estimates shown to the nearest point. Read the gaps between sections rather than
                the exact figures: a total that has not moved can still hide one section climbing while another slides.
              </p>
              <div className="score-rows">
                {scored.slice().reverse().map(attempt => (
                  <Link key={attempt.attemptId} href={`/exams/${attempt.examId}/score/${attempt.attemptId}`} className="score-row">
                    <span className="score-row-total">{attempt.total}</span>
                    <span className="score-row-meta">
                      <strong>{nameOf(attempt.examId)}</strong>
                      <small>
                        {new Date(attempt.finishedAt).toLocaleDateString()} &middot; estimated {attempt.low}&ndash;{attempt.high}
                      </small>
                    </span>
                    <span className="score-row-sections">
                      {attempt.sections.map(section => (
                        <span key={section.short}>
                          <small>{section.short}</small>
                          <b>{section.scaled}</b>
                        </span>
                      ))}
                    </span>
                    <span className="score-row-open" aria-hidden="true">&rarr;</span>
                  </Link>
                ))}
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
}
