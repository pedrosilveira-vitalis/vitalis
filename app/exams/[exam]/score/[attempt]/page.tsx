"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import MainNav from "@/components/MainNav";

type Breakdown = { key: string; name: string; correct: number; total: number; percent: number };
type SectionScore = {
  id: string; name: string; short: string; nickname: string;
  correct: number; total: number; answered: number; blank: number;
  percent: number; scaled: number; low: number; high: number; secondsRemaining: number;
  categories: Breakdown[]; skills: Breakdown[];
};
type Miss = {
  id: string; section: string; position: number; stem: string;
  chosen: "A" | "B" | "C" | "D" | null; correct: "A" | "B" | "C" | "D";
  category: string; categoryName: string; skillName: string; difficulty: string;
  unit: string | null; unitName: string | null; unitHref: string | null; seconds: number | null;
  choices: Record<"A" | "B" | "C" | "D", string> | null;
  explanation: string; whyWrong: string; passageTitle: string | null;
};
type Report = {
  examName: string; startedAt: string; finishedAt: string | null;
  total: number; totalLow: number; totalHigh: number; percentile: number | null;
  correct: number; questions: number;
  sections: SectionScore[]; missed: Miss[];
  recommendations: {
    unit: string; section: string; missed: number; total: number; categories: string[];
    unitName: string; lessonHref: string | null; sheetHref: string | null; drillHref: string | null;
  }[];
  weakestSkills: Breakdown[]; weakestCategories: Breakdown[];
};

function minutes(seconds: number) {
  const whole = Math.round(seconds / 60);
  return whole <= 0 ? "none" : `${whole} min`;
}

export default function ScoreReportPage() {
  const params = useParams();
  const attemptId = (params.attempt as string) || "";
  const [data, setData] = useState<{ report: Report; verdict: string } | null>(null);
  const [error, setError] = useState("");
  const [openSection, setOpenSection] = useState<string>("all");

  useEffect(() => {
    let live = true;
    fetch(`/api/exams/report?attempt=${encodeURIComponent(attemptId)}`)
      .then(async response => {
        const payload = await response.json();
        if (!live) return;
        if (!response.ok) { setError(payload.error ?? "Could not load your report."); return; }
        setData(payload);
      })
      .catch(() => { if (live) setError("Could not load your report."); });
    return () => { live = false; };
  }, [attemptId]);

  if (error) {
    return (
      <div className="dashboard-page">
        <MainNav badge="Score report" />
        <main className="study-dashboard">
          <section className="exam-brief">
            <h1>We could not open that report</h1>
            <p className="exam-brief-fine">{error}</p>
            <Link href="/exams" className="button-outline">Back to full-lengths</Link>
          </section>
        </main>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="dashboard-page">
        <MainNav badge="Score report" />
        <main className="study-dashboard">
          <section className="exam-brief"><h1>Scoring your exam&hellip;</h1></section>
        </main>
      </div>
    );
  }

  const { report, verdict } = data;
  const misses = openSection === "all" ? report.missed : report.missed.filter(miss => miss.section === openSection);

  return (
    <div className="dashboard-page">
      <MainNav badge="Score report" contentId="report-content" />
      <main id="report-content" tabIndex={-1} className="study-dashboard">
        <section className="report-hero">
          <div>
            <p className="eyebrow">{report.examName.toUpperCase()}</p>
            <h1>
              <span className="report-total">{report.total}</span>
              <small>
                estimated &mdash; likely {report.totalLow} to {report.totalHigh}
              </small>
            </h1>
            <p className="report-verdict">{verdict}</p>
            <p className="report-meta">
              {report.correct} of {report.questions} correct
              {report.percentile !== null ? ` · around the ${report.percentile}th percentile` : ""}
              {report.finishedAt ? ` · finished ${new Date(report.finishedAt).toLocaleDateString()}` : ""}
            </p>
          </div>
        </section>

        <section className="report-sections">
          {report.sections.map(section => (
            <article key={section.id} className="report-section-card">
              <header>
                <span className="eyebrow">{section.short}</span>
                <strong>{section.scaled}</strong>
                <small>
                  {section.low}&ndash;{section.high}
                </small>
              </header>
              <p className="report-section-name">{section.nickname}</p>
              <dl>
                <div>
                  <dt>Correct</dt>
                  <dd>
                    {section.correct}/{section.total} ({section.percent}%)
                  </dd>
                </div>
                <div>
                  <dt>Left blank</dt>
                  <dd className={section.blank > 0 ? "is-warning" : undefined}>{section.blank}</dd>
                </div>
                <div>
                  <dt>Time unused</dt>
                  <dd>{minutes(section.secondsRemaining)}</dd>
                </div>
              </dl>
            </article>
          ))}
        </section>

        <section className="report-block">
          <h2>Where the points went</h2>
          <p className="report-lede">
            A section score tells you how much. These tell you what. A content category you are losing marks in means
            go and read; a reasoning skill you are losing marks in means the content is fine and the approach is not.
          </p>

          <div className="report-two">
            <div>
              <h3>By reasoning skill</h3>
              {report.weakestSkills.length ? (
                <ul className="report-bars">
                  {report.weakestSkills.map(row => (
                    <li key={row.key}>
                      <span>{row.name}</span>
                      <progress value={row.correct} max={row.total} />
                      <small>
                        {row.correct}/{row.total}
                      </small>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="report-lede">Not enough questions in any one skill to say anything useful.</p>
              )}
            </div>
            <div>
              <h3>Weakest content categories</h3>
              {report.weakestCategories.length ? (
                <ul className="report-bars">
                  {report.weakestCategories.slice(0, 8).map(row => (
                    <li key={row.key}>
                      <span>
                        <code>{row.key}</code> {row.name}
                      </span>
                      <progress value={row.correct} max={row.total} />
                      <small>
                        {row.correct}/{row.total}
                      </small>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="report-lede">Nothing stands out.</p>
              )}
            </div>
          </div>
        </section>

        {report.recommendations.length > 0 && (
          <section className="report-block">
            <h2>What to do next</h2>
            <p className="report-lede">
              Ranked by how many marks each unit cost you, not by percentage &mdash; a unit that cost you six is worth
              more of tonight than one that cost you one.
            </p>
            <ol className="report-plan">
              {report.recommendations.slice(0, 8).map((row, position) => (
                <li key={row.unit}>
                  <span className="report-rank">{position + 1}</span>
                  <div>
                    <h3>{row.unitName}</h3>
                    <p>
                      Cost you {row.missed} {row.missed === 1 ? "mark" : "marks"} out of {row.total} on this form
                      {row.categories.length ? ` · ${row.categories.join(", ")}` : ""}
                    </p>
                    <div className="report-plan-links">
                      {row.lessonHref && <Link href={row.lessonHref}>Read the unit</Link>}
                      {row.sheetHref && <Link href={row.sheetHref}>Cheat sheet</Link>}
                      {row.drillHref && <Link href={row.drillHref}>Drill 10 questions</Link>}
                    </div>
                  </div>
                </li>
              ))}
            </ol>
          </section>
        )}

        <section className="report-block">
          <h2>Every question you missed</h2>
          <div className="report-filters">
            <button type="button" className={openSection === "all" ? "exam-tab is-on" : "exam-tab"} onClick={() => setOpenSection("all")}>
              All {report.missed.length}
            </button>
            {report.sections.map(section => {
              const count = report.missed.filter(miss => miss.section === section.id).length;
              return (
                <button
                  key={section.id}
                  type="button"
                  className={openSection === section.id ? "exam-tab is-on" : "exam-tab"}
                  onClick={() => setOpenSection(section.id)}
                >
                  {section.short} {count}
                </button>
              );
            })}
          </div>

          <div className="report-misses">
            {misses.map(miss => (
              <details key={miss.id} className="report-miss">
                <summary>
                  <span className="report-miss-no">Q{miss.position}</span>
                  <span className="report-miss-stem">{miss.stem}</span>
                  <span className="report-miss-tags">
                    {miss.chosen ? `You: ${miss.chosen}` : "Blank"} <b>Answer: {miss.correct}</b>
                  </span>
                </summary>
                <div className="report-miss-body">
                  {miss.passageTitle && <p className="report-miss-passage">From the passage: {miss.passageTitle}</p>}
                  {miss.choices && (
                    <ul className="report-miss-choices">
                      {(["A", "B", "C", "D"] as const).map(letter => (
                        <li
                          key={letter}
                          className={
                            letter === miss.correct ? "is-right" : letter === miss.chosen ? "is-yours" : undefined
                          }
                        >
                          <span>{letter}</span>
                          {miss.choices?.[letter]}
                        </li>
                      ))}
                    </ul>
                  )}
                  {miss.whyWrong && (
                    <p className="report-miss-wrong">
                      <strong>Why {miss.chosen} is wrong.</strong> {miss.whyWrong}
                    </p>
                  )}
                  <p className="report-miss-right">
                    <strong>Why {miss.correct} is right.</strong> {miss.explanation}
                  </p>
                  <p className="report-miss-foot">
                    {miss.categoryName}
                    {miss.category ? ` (${miss.category})` : ""} · {miss.skillName} · {miss.difficulty}
                    {miss.seconds !== null ? ` · you spent ${miss.seconds}s on it` : ""}
                    {miss.unitName && miss.unitHref ? (
                      <>
                        {" · "}
                        <Link href={miss.unitHref}>{miss.unitName}</Link>
                      </>
                    ) : null}
                  </p>
                </div>
              </details>
            ))}
            {!misses.length && <p className="report-lede">Nothing missed in this section.</p>}
          </div>
        </section>

        <section className="exam-how">
          <h2>About this score</h2>
          <p>
            Your scaled score is an estimate, which is why it is shown as a range. The AAMC does not publish its
            raw-to-scaled conversion tables, and re-equates every form it writes, so no third party can give you an
            exact number &mdash; ours included. Use the range to decide whether you are ready, and use the breakdown
            above to decide what to do tomorrow.
          </p>
          <p>
            Where this exam is most reliable is in the ranking: the sections and units it says are weakest are the ones
            that are weakest. That is the part you can act on.
          </p>
          <Link href="/exams" className="button-outline">Back to full-lengths</Link>
        </section>
      </main>
    </div>
  );
}
