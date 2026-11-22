"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import MainNav from "@/components/MainNav";
import StudyIcon from "@/components/StudyIcon";

type Progress = { id: string; short: string; written: number; needed: number };
type Exam = { id: string; name: string; number: number; blurb: string; ready: boolean; free: boolean; allowed: boolean; written: number; needed: number; progress: Progress[] };
type LiveAttempt = { status: "live"; examId: string; attemptId: string; startedAt: string; sectionIndex: number };
type ScoredAttempt = { status: "scored"; examId: string; attemptId: string; finishedAt: string; total: number | null; low: number | null; high: number | null; complete: boolean; sections: { short: string; scaled: number }[] };
type Attempt = LiveAttempt | ScoredAttempt;

const isLive = (item: Attempt): item is LiveAttempt => item.status === "live";
const isScored = (item: Attempt): item is ScoredAttempt => item.status === "scored";
type ChartedAttempt = ScoredAttempt & { total: number; low: number; high: number };
const hasTotal = (item: ScoredAttempt): item is ChartedAttempt => item.complete && item.total !== null;

export default function ExamsPage() {
  const [data, setData] = useState<{ signedIn: boolean; allowed: boolean; exams: Exam[]; attempts: Attempt[] } | null>(null);
  const [admin, setAdmin] = useState(false);

  useEffect(() => {
    let live = true;
    fetch("/api/exams")
      .then(response => response.json())
      .then(payload => { if (live) setData(payload); })
      .catch(() => { if (live) setData({ signedIn: false, allowed: false, exams: [], attempts: [] }); });
    return () => { live = false; };
  }, []);

  useEffect(() => {
    let live = true;
    fetch("/api/session")
      .then(response => response.json())
      .then(payload => { if (live) setAdmin(Boolean(payload.isAdmin)); })
      .catch(() => {});
    return () => { live = false; };
  }, []);

  return (
    <div className="dashboard-page">
      <MainNav badge="Full-lengths" contentId="exams-content" />
      <main id="exams-content" tabIndex={-1} className="study-dashboard">
        <section className="dashboard-welcome">
          <div>
            <p className="eyebrow">SEVEN AND A HALF HOURS, LIKE THE REAL ONE</p>
            <h1>
              Full-length <span>practice exams.</span>
            </h1>
            <p>230 questions, four sections, the same timing and the same breaks. Then a report that tells you what to fix.</p>
          </div>
        </section>

        <div className="exam-cards">
          {(data?.exams ?? []).map(exam => {
            const mine = (data?.attempts ?? []).filter(item => item.examId === exam.id);
            const live = mine.filter(isLive)[0];
            const scored = mine.filter(isScored).filter(hasTotal);
            return (
              <article key={exam.id} className="exam-card">
                <div className="exam-card-head">
                  <span className="eyebrow">
                    FULL-LENGTH {exam.number}
                    {exam.free ? <em className="exam-free-tag">Free</em> : null}
                  </span>
                  <h2>{exam.name}</h2>
                  <p>{exam.blurb}</p>
                </div>

                {!exam.ready && (
                  <div className="exam-card-progress">
                    <p>
                      <strong>Being written.</strong> {exam.written} of {exam.needed} questions are finished and reviewed.
                    </p>
                    <ul>
                      {exam.progress.map(row => (
                        <li key={row.id}>
                          <span>{row.short}</span>
                          <progress value={row.written} max={row.needed} />
                          <small>
                            {row.written}/{row.needed}
                          </small>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {scored.length > 0 && (
                  <ul className="exam-card-scores">
                    {scored.map(attempt => (
                      <li key={attempt.attemptId}>
                        <Link href={`/exams/${exam.id}/score/${attempt.attemptId}`}>
                          <strong>{attempt.total}</strong>
                          <span>
                            estimated, {attempt.low}&ndash;{attempt.high}
                          </span>
                          <small>{new Date(attempt.finishedAt).toLocaleDateString()}</small>
                        </Link>
                      </li>
                    ))}
                  </ul>
                )}

                <div className="exam-card-actions">
                  {!data ? (
                    <span className="exam-card-note">Loading&hellip;</span>
                  ) : !data.signedIn ? (
                    <Link href="/sign-in" className="button-primary">
                      Sign in <StudyIcon name="arrow" />
                    </Link>
                  ) : !exam.allowed ? (
                    <>
                      <Link href="/plans" className="button-primary">
                        Unlock with Complete <StudyIcon name="arrow" />
                      </Link>
                      <span className="exam-card-note">
                        Full-Length 1 is free with your account. Complete adds the other four and their score reports.
                      </span>
                    </>
                  ) : live ? (
                    <>
                      <Link href={`/exams/${exam.id}/run`} className="button-primary">
                        Resume where you left off <StudyIcon name="arrow" />
                      </Link>
                      <span className="exam-card-note">
                        Started {new Date(live.startedAt).toLocaleString()}. Section {live.sectionIndex + 1} of 4.
                      </span>
                    </>
                  ) : exam.ready ? (
                    <Link href={`/exams/${exam.id}`} className="button-primary">
                      Read the instructions <StudyIcon name="arrow" />
                    </Link>
                  ) : (
                    <>
                      {admin && (
                        <Link href={`/exams/${exam.id}`} className="button-primary">
                          Preview the interface (admin) <StudyIcon name="arrow" />
                        </Link>
                      )}
                      <span className="exam-card-note">
                        You will get an email the day this one opens. It is included in your plan.
                      </span>
                    </>
                  )}
                </div>
              </article>
            );
          })}
        </div>

        <div className="exam-history-link">
          <Link href="/exams/scores">See every score you have had &rarr;</Link>
        </div>

        <section className="exam-how">
          <h2>How these are built</h2>
          <p>
            Every question is written from scratch to the published AAMC blueprint and tagged with its content
            category, the reasoning skill it tests and the unit it comes from. None of it is copied from an official
            AAMC exam &mdash; that material is theirs, and a prep company that reuses it is one lawsuit from closing.
          </p>
          <p>
            Your scaled score is an <strong>estimate shown as a range</strong>. The AAMC does not publish its
            conversion tables and re-equates every form, so nobody outside the AAMC can hand you an exact number.
            Anyone who tells you otherwise is guessing with more confidence than they have earned.
          </p>
        </section>
      </main>
    </div>
  );
}
