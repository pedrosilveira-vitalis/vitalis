"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import MainNav from "@/components/MainNav";

type Progress = { id: string; short: string; written: number; needed: number };
type Exam = { id: string; name: string; number: number; blurb: string; ready: boolean; free: boolean; allowed: boolean; written: number; needed: number; progress: Progress[] };

/**
 * The screen before the clock starts. It does the job the test-day tutorial
 * does: says what is coming, what the tools are, and what the rules are — and
 * makes the student commit before anything is timed.
 */
export default function ExamStartPage() {
  const params = useParams();
  const router = useRouter();
  const examId = (params.exam as string) || "";
  const [data, setData] = useState<{ signedIn: boolean; allowed: boolean; exams: Exam[] } | null>(null);
  const [admin, setAdmin] = useState(false);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let live = true;
    fetch("/api/exams")
      .then(response => response.json())
      .then(payload => { if (live) setData(payload); })
      .catch(() => { if (live) setError("Could not load the exam."); });
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

  const exam = data?.exams.find(item => item.id === examId);

  async function begin() {
    setStarting(true);
    setError("");
    try {
      const response = await fetch("/api/exams/attempt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "start", exam: examId }),
      });
      const payload = await response.json();
      if (!response.ok) { setError(payload.error ?? "Could not start the exam."); setStarting(false); return; }
      router.push(`/exams/${examId}/run`);
    } catch {
      setError("Could not reach the exam server.");
      setStarting(false);
    }
  }

  return (
    <div className="dashboard-page">
      <MainNav badge="Full-lengths" contentId="start-content" />
      <main id="start-content" tabIndex={-1} className="study-dashboard">
        <section className="exam-brief">
          <p className="eyebrow">BEFORE YOU START</p>
          <h1>{exam?.name ?? "Full-length exam"}</h1>

          <div className="exam-brief-grid">
            <div>
              <h2>What is coming</h2>
              <table className="exam-brief-table">
                <tbody>
                  <tr><td>Chemical and Physical Foundations</td><td>59 questions</td><td>95 min</td></tr>
                  <tr><td className="is-break" colSpan={3}>Optional break &mdash; 10 minutes</td></tr>
                  <tr><td>Critical Analysis and Reasoning Skills</td><td>53 questions</td><td>90 min</td></tr>
                  <tr><td className="is-break" colSpan={3}>Optional mid-exam break &mdash; 30 minutes</td></tr>
                  <tr><td>Biological and Biochemical Foundations</td><td>59 questions</td><td>95 min</td></tr>
                  <tr><td className="is-break" colSpan={3}>Optional break &mdash; 10 minutes</td></tr>
                  <tr><td>Psychological, Social, and Biological Foundations</td><td>59 questions</td><td>95 min</td></tr>
                  <tr className="is-total"><td>Total</td><td>230 questions</td><td>6 h 15 min of testing</td></tr>
                </tbody>
              </table>
              <p className="exam-brief-fine">
                With the breaks taken in full that is a seven-hour sitting. Take it in one go, at the time of day your
                real exam starts. A full-length split across two evenings tells you about your content and nothing
                about your stamina, and stamina is what the back half of the exam measures.
              </p>
            </div>

            <div>
              <h2>Your tools</h2>
              <ul className="exam-brief-list">
                <li><strong>Highlight</strong> &mdash; select text, then Alt+H. Works on the passage, the question and the answers.</li>
                <li><strong>Strikethrough</strong> &mdash; select text, then Alt+S. For eliminating choices.</li>
                <li><strong>Flag for review</strong> &mdash; Alt+F. Flagged questions are listed on the review screen.</li>
                <li><strong>Navigator</strong> &mdash; Alt+V. Every question with its status: answered, incomplete or unseen.</li>
                <li><strong>Periodic table</strong> &mdash; Alt+T, in Chem/Phys only, as on the real exam.</li>
                <li><strong>a, b, c, d</strong> &mdash; select an answer without the mouse.</li>
                <li><strong>Alt+N / Alt+P</strong> &mdash; next and previous question.</li>
                <li><strong>Screen colours</strong> &mdash; white, black or salmon, the three the AAMC offers.</li>
              </ul>

              <h2>The rules</h2>
              <ul className="exam-brief-list">
                <li><strong>No calculator.</strong> There is none on the real exam. Keep paper and a pencil beside you.</li>
                <li><strong>The clock runs on our server.</strong> Closing the tab does not pause it; it carries on without you.</li>
                <li><strong>A section you hand in is closed.</strong> You cannot go back to it, exactly as on test day.</li>
                <li><strong>A break you decline is forfeited.</strong> It does not roll into the next section.</li>
                <li><strong>Nothing is penalised for guessing.</strong> Never leave a question blank.</li>
              </ul>
            </div>
          </div>

          {error && <p className="exam-brief-error">{error}</p>}

          <div className="exam-brief-actions">
            {!data ? (
              <span className="exam-card-note">Loading&hellip;</span>
            ) : !exam?.allowed ? (
              <Link href="/plans" className="button-primary">Unlock this form with Complete</Link>
            ) : !exam?.ready ? (
              <>
                <span className="exam-card-note">
                  This form is still being written &mdash; {exam?.written ?? 0} of {exam?.needed ?? 230} questions are
                  finished. We will email you the day it opens.
                </span>
                {admin && (
                  <button type="button" className="button-primary" onClick={begin} disabled={starting}>
                    {starting ? "Opening\u2026" : "Preview the interface (admin)"}
                  </button>
                )}
                <Link href="/exams" className="button-outline">Back to full-lengths</Link>
              </>
            ) : (
              <>
                <button type="button" className="button-primary" onClick={begin} disabled={starting}>
                  {starting ? "Starting…" : "Start the exam — the clock begins now"}
                </button>
                <Link href="/exams" className="button-outline">Not yet</Link>
              </>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
