"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import Annotated from "./Annotated";
import PeriodicTable from "./PeriodicTable";
import { applyTool, dropSelection, readSelection, type MarkMap } from "./annotations";

/**
 * The exam runner: one section at a time, under test conditions.
 *
 * Deliberately faithful to the real interface, because familiarity with the
 * tools is worth marks on test day: a split passage pane, highlight and
 * strikethrough on any text, flag for review, the navigator, a review screen
 * that appears after the last question, a hideable clock, the periodic table
 * in Chem/Phys, and the three accessibility views the AAMC added in 2025.
 *
 * The clock is the server's. The local countdown exists only so the display
 * ticks between syncs; every save returns the authoritative seconds left, and
 * answers are refused server-side once a section's deadline has passed.
 */

type Choice = "A" | "B" | "C" | "D";
const LETTERS: Choice[] = ["A", "B", "C", "D"];

interface Passage {
  id: string;
  title: string;
  paragraphs: string[];
  figure?: { kind: "svg" | "table"; caption: string; markup: string };
}
interface Question {
  id: string;
  passageId: string | null;
  stem: string;
  choices: Record<Choice, string>;
}
interface SectionInfo {
  id: string;
  name: string;
  short: string;
  nickname: string;
  minutes: number;
  questions: number;
  breakAfterMinutes: number | null;
  breakLabel: string | null;
  index: number;
  count: number;
  periodicTable: boolean;
}
interface View {
  attempt: { id: string; examId: string; sectionIndex: number; secondsRemaining: number; answers: Record<string, Choice>; flagged: string[] };
  onBreak: boolean;
  breakSecondsRemaining: number;
  section: SectionInfo | null;
  content: { id: string; passages: Passage[]; questions: Question[] } | null;
}

type Theme = "light" | "dark" | "salmon";
type Mode = "testing" | "review" | "break";
type ReviewFilter = "all" | "incomplete" | "flagged";

function clock(seconds: number): string {
  const safe = Math.max(0, Math.round(seconds));
  const hours = Math.floor(safe / 3600);
  const minutes = Math.floor((safe % 3600) / 60);
  const rest = safe % 60;
  const pad = (value: number) => String(value).padStart(2, "0");
  return hours > 0 ? `${hours}:${pad(minutes)}:${pad(rest)}` : `${pad(minutes)}:${pad(rest)}`;
}

export default function ExamRunner({ examId }: { examId: string }) {
  const router = useRouter();
  const [view, setView] = useState<View | null>(null);
  const [error, setError] = useState("");
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, Choice>>({});
  const [flagged, setFlagged] = useState<Set<string>>(new Set());
  const [seen, setSeen] = useState<Set<string>>(new Set());
  const [marks, setMarks] = useState<MarkMap>({});
  const [seconds, setSeconds] = useState(0);
  const [breakSeconds, setBreakSeconds] = useState(0);
  const [mode, setMode] = useState<Mode>("testing");
  const [filter, setFilter] = useState<ReviewFilter>("all");
  const [navOpen, setNavOpen] = useState(false);
  const [tableOpen, setTableOpen] = useState(false);
  const [timerHidden, setTimerHidden] = useState(false);
  const [theme, setTheme] = useState<Theme>("light");
  const [confirmEnd, setConfirmEnd] = useState(false);
  const [busy, setBusy] = useState(false);

  // Seconds spent per question, flushed with the periodic save.
  const timing = useRef<Record<string, number>>({});
  const pendingTiming = useRef<Record<string, number>>({});
  const dirty = useRef(false);
  const landed = useRef<number>(Date.now());
  const passagePane = useRef<HTMLElement | null>(null);

  const questions = view?.content?.questions ?? [];
  const question = questions[index];
  const passage = useMemo(
    () => (question?.passageId ? view?.content?.passages.find(item => item.id === question.passageId) ?? null : null),
    [question, view],
  );

  /* ---------------- loading and section changes ---------------- */

  const adopt = useCallback((next: View) => {
    setView(next);
    setAnswers(next.attempt.answers ?? {});
    setFlagged(new Set(next.attempt.flagged ?? []));
    setSeconds(next.attempt.secondsRemaining);
    setBreakSeconds(next.breakSecondsRemaining);
    setMode(next.onBreak ? "break" : "testing");
    setIndex(0);
    setSeen(new Set());
    setMarks({});
    setConfirmEnd(false);
    setFilter("all");
    setNavOpen(false);
    setTableOpen(false);
    timing.current = {};
    pendingTiming.current = {};
    landed.current = Date.now();
  }, []);

  useEffect(() => {
    let live = true;
    (async () => {
      try {
        const response = await fetch(`/api/exams/attempt?exam=${encodeURIComponent(examId)}`);
        const data = await response.json();
        if (!live) return;
        if (!response.ok) { setError(data.error ?? "Could not load the exam."); return; }
        if (!data.attempt) { router.replace(`/exams/${examId}`); return; }
        adopt(data as View);
      } catch {
        if (live) setError("Could not reach the exam server. Check your connection; your answers are saved.");
      }
    })();
    return () => { live = false; };
  }, [examId, router, adopt]);

  /* ---------------- the clocks ---------------- */

  useEffect(() => {
    if (mode === "break") return;
    const timer = setInterval(() => setSeconds(current => Math.max(0, current - 1)), 1000);
    return () => clearInterval(timer);
  }, [mode]);

  useEffect(() => {
    if (mode !== "break") return;
    const timer = setInterval(() => setBreakSeconds(current => Math.max(0, current - 1)), 1000);
    return () => clearInterval(timer);
  }, [mode]);

  /* ---------------- saving ---------------- */

  const save = useCallback(async () => {
    const attempt = view?.attempt;
    if (!attempt) return;
    const timings = pendingTiming.current;
    pendingTiming.current = {};
    const payload = {
      action: "save",
      exam: examId,
      attempt: attempt.id,
      answers,
      flagged: [...flagged],
      timing: timings,
    };
    dirty.current = false;
    try {
      const response = await fetch("/api/exams/attempt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (typeof data.secondsRemaining === "number") setSeconds(data.secondsRemaining);
    } catch {
      // Keep the answers in state and try again on the next tick.
      dirty.current = true;
      Object.assign(pendingTiming.current, timings);
    }
  }, [view, examId, answers, flagged]);

  useEffect(() => {
    if (mode === "break") return;
    const timer = setInterval(() => { void save(); }, 15000);
    return () => clearInterval(timer);
  }, [save, mode]);

  // Record the time spent on the question being left.
  const stamp = useCallback(() => {
    if (!question) return;
    const spent = Math.round((Date.now() - landed.current) / 1000);
    landed.current = Date.now();
    if (spent <= 0) return;
    timing.current[question.id] = (timing.current[question.id] ?? 0) + spent;
    pendingTiming.current[question.id] = timing.current[question.id];
  }, [question]);

  const go = useCallback((next: number) => {
    stamp();
    setIndex(Math.max(0, Math.min(next, questions.length - 1)));
    dropSelection();
  }, [stamp, questions.length]);

  useEffect(() => {
    if (question) setSeen(current => (current.has(question.id) ? current : new Set(current).add(question.id)));
  }, [question]);

  // On the real exam a passage you have scrolled through returns to the top
  // when you move to the next question. It is a small thing that costs
  // students time on test day if they have only practised somewhere kinder.
  useEffect(() => {
    if (passagePane.current) passagePane.current.scrollTop = 0;
  }, [index]);

  /* ---------------- answering ---------------- */

  const choose = useCallback((letter: Choice) => {
    if (!question) return;
    setAnswers(current => ({ ...current, [question.id]: letter }));
    dirty.current = true;
  }, [question]);

  const toggleFlag = useCallback(() => {
    if (!question) return;
    setFlagged(current => {
      const next = new Set(current);
      if (next.has(question.id)) next.delete(question.id); else next.add(question.id);
      return next;
    });
    dirty.current = true;
  }, [question]);

  const tool = useCallback((kind: "highlight" | "strike") => {
    const hits = readSelection();
    if (!hits.length) return;
    setMarks(current => applyTool(current, kind, hits));
    dropSelection();
  }, []);

  /* ---------------- section flow ---------------- */

  const post = useCallback(async (body: Record<string, unknown>) => {
    setBusy(true);
    try {
      const response = await fetch("/api/exams/attempt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ exam: examId, attempt: view?.attempt.id, ...body }),
      });
      const data = await response.json();
      if (data.finished) { router.replace(`/exams/${examId}/score/${data.attemptId ?? view?.attempt.id}`); return null; }
      if (!response.ok) { setError(data.error ?? "Something went wrong."); return null; }
      return data as View;
    } catch {
      setError("Could not reach the exam server. Your answers are saved; try again.");
      return null;
    } finally {
      setBusy(false);
    }
  }, [examId, view, router]);

  const endSection = useCallback(async (takeBreak: boolean) => {
    stamp();
    await save();
    const next = await post({ action: "submit-section", takeBreak });
    if (next) adopt(next);
  }, [stamp, save, post, adopt]);

  const resume = useCallback(async () => {
    const next = await post({ action: "end-break" });
    if (next) adopt(next);
  }, [post, adopt]);

  // A break that runs out resumes on its own, as the real exam does.
  useEffect(() => {
    if (mode === "break" && breakSeconds === 0 && view?.onBreak) void resume();
  }, [mode, breakSeconds, view, resume]);

  // Time called: the section is handed in whether or not anyone is watching.
  const expired = useRef(false);
  useEffect(() => {
    if (mode === "break" || seconds > 0 || !view?.attempt || expired.current) return;
    expired.current = true;
    void endSection(true);
  }, [seconds, mode, view, endSection]);
  useEffect(() => { expired.current = false; }, [view?.attempt.sectionIndex]);

  /* ---------------- keyboard ---------------- */

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") { setNavOpen(false); setTableOpen(false); return; }
      const key = event.key.toLowerCase();
      if (event.altKey) {
        const handled = () => { event.preventDefault(); };
        if (mode === "review") {
          if (key === "a") { setFilter("all"); handled(); }
          if (key === "i") { setFilter("incomplete"); handled(); }
          if (key === "r") { setFilter("flagged"); handled(); }
          if (key === "e") { setConfirmEnd(true); handled(); }
          return;
        }
        if (key === "n") { if (index === questions.length - 1) setMode("review"); else go(index + 1); handled(); }
        if (key === "p") { go(index - 1); handled(); }
        if (key === "v") { setNavOpen(true); handled(); }
        if (key === "c") { setNavOpen(false); setTableOpen(false); handled(); }
        if (key === "f") { toggleFlag(); handled(); }
        if (key === "h") { tool("highlight"); handled(); }
        if (key === "s") { tool("strike"); handled(); }
        if (key === "t" && view?.section?.periodicTable) { setTableOpen(true); handled(); }
        if (key === "w") { setMode("review"); handled(); }
        return;
      }
      if (mode === "testing" && !navOpen && !tableOpen && LETTERS.some(letter => letter.toLowerCase() === key)) {
        choose(key.toUpperCase() as Choice);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [mode, index, questions.length, go, toggleFlag, tool, choose, navOpen, tableOpen, view]);

  /* ---------------- leaving the page ---------------- */

  useEffect(() => {
    const warn = (event: BeforeUnloadEvent) => {
      if (mode === "break") return;
      event.preventDefault();
      event.returnValue = "";
    };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [mode]);

  /* ---------------- rendering ---------------- */

  if (error) {
    return (
      <div className="exam-shell exam-light">
        <div className="exam-notice">
          <h1>We hit a problem</h1>
          <p>{error}</p>
          <button type="button" onClick={() => window.location.reload()} className="exam-primary">Try again</button>
        </div>
      </div>
    );
  }

  if (!view || !view.section) {
    return (
      <div className="exam-shell exam-light">
        <div className="exam-notice"><h1>Loading your exam&hellip;</h1></div>
      </div>
    );
  }

  const section = view.section;
  const answeredCount = questions.filter(item => answers[item.id]).length;
  const low = seconds <= 300 && mode !== "break";

  if (mode === "break") {
    return (
      <div className={`exam-shell exam-${theme}`}>
        <div className="exam-notice exam-break">
          <span className="exam-eyebrow">{section.breakLabel ?? "Break"}</span>
          <h1>{clock(breakSeconds)}</h1>
          <p>
            Your break is running. The clock for {section.nickname} starts the moment the break ends, or as soon as
            you choose to go back in &mdash; whichever comes first.
          </p>
          <p className="exam-fine">
            On test day this is when you leave the room, eat something and use the bathroom. Practise it the same
            way: a full-length taken straight through does not tell you how you will hold up at hour six.
          </p>
          <button type="button" onClick={resume} disabled={busy} className="exam-primary">
            {busy ? "Starting…" : `Start ${section.nickname} now`}
          </button>
        </div>
      </div>
    );
  }

  if (mode === "review") {
    const shown = questions
      .map((item, position) => ({ item, position }))
      .filter(({ item }) =>
        filter === "all" ? true : filter === "incomplete" ? !answers[item.id] : flagged.has(item.id),
      );
    const incomplete = questions.length - answeredCount;
    return (
      <div className={`exam-shell exam-${theme}`}>
        <header className="exam-bar">
          <div className="exam-bar-left">
            <strong>{section.name}</strong>
            <span>Section review</span>
          </div>
          <div className="exam-bar-right">
            <button type="button" className="exam-chip" onClick={() => setTimerHidden(value => !value)}>
              {timerHidden ? "Show time" : clock(seconds)}
            </button>
          </div>
        </header>

        <div className="exam-review">
          <h1>You have reached the end of {section.nickname}.</h1>
          <p>
            {incomplete === 0
              ? "Every question is answered."
              : `${incomplete} ${incomplete === 1 ? "question is" : "questions are"} still unanswered. There is no penalty for a wrong answer, so leave nothing blank.`}
          </p>

          <div className="exam-review-tabs">
            {([["all", "Review all", "Alt+A"], ["incomplete", "Review incomplete", "Alt+I"], ["flagged", "Review flagged", "Alt+R"]] as const).map(
              ([value, label, hint]) => (
                <button
                  key={value}
                  type="button"
                  className={filter === value ? "exam-tab is-on" : "exam-tab"}
                  onClick={() => setFilter(value)}
                >
                  {label} <span className="exam-key">{hint}</span>
                </button>
              ),
            )}
          </div>

          <table className="exam-review-table">
            <thead>
              <tr><th>Question</th><th>Status</th><th>Flagged</th><th /></tr>
            </thead>
            <tbody>
              {shown.map(({ item, position }) => (
                <tr key={item.id}>
                  <td>{position + 1}</td>
                  <td>{answers[item.id] ? `Answered (${answers[item.id]})` : seen.has(item.id) ? "Incomplete" : "Unseen"}</td>
                  <td>{flagged.has(item.id) ? "Flagged" : ""}</td>
                  <td>
                    <button type="button" className="exam-link" onClick={() => { setMode("testing"); setIndex(position); }}>
                      Go to question
                    </button>
                  </td>
                </tr>
              ))}
              {!shown.length && (
                <tr><td colSpan={4} className="exam-empty">Nothing to review here.</td></tr>
              )}
            </tbody>
          </table>

          <div className="exam-review-actions">
            <button type="button" className="exam-secondary" onClick={() => { setMode("testing"); setIndex(questions.length - 1); }}>
              Back to the section
            </button>
            <button type="button" className="exam-primary" onClick={() => setConfirmEnd(true)}>
              End this section <span className="exam-key">Alt+E</span>
            </button>
          </div>
        </div>

        {confirmEnd && (
          <div className="exam-window exam-window-small" role="dialog" aria-modal="true" aria-label="End the section">
            <div className="exam-window-head"><h2>End {section.nickname}?</h2></div>
            <div className="exam-window-body">
              <p>
                You cannot come back to this section once it is handed in, exactly as on test day.
                {incomplete > 0 ? ` ${incomplete} ${incomplete === 1 ? "question" : "questions"} will be scored as incorrect.` : ""}
              </p>
              {section.breakAfterMinutes ? (
                <p className="exam-fine">
                  A {section.breakAfterMinutes}-minute break follows. A break you decline is forfeited, as it is on
                  the real exam.
                </p>
              ) : (
                <p className="exam-fine">This is the last section. Ending it finishes the exam and produces your report.</p>
              )}
              <div className="exam-window-actions">
                <button type="button" className="exam-secondary" onClick={() => setConfirmEnd(false)}>Keep working</button>
                {section.breakAfterMinutes ? (
                  <>
                    <button type="button" className="exam-secondary" disabled={busy} onClick={() => void endSection(false)}>
                      Skip the break
                    </button>
                    <button type="button" className="exam-primary" disabled={busy} onClick={() => void endSection(true)}>
                      {busy ? "Handing in…" : `Take the ${section.breakAfterMinutes}-minute break`}
                    </button>
                  </>
                ) : (
                  <button type="button" className="exam-primary" disabled={busy} onClick={() => void endSection(false)}>
                    {busy ? "Scoring…" : "Finish the exam"}
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className={`exam-shell exam-${theme}`}>
      <header className="exam-bar">
        <div className="exam-bar-left">
          <strong>{section.name}</strong>
          <span>
            Question {index + 1} of {questions.length}
          </span>
        </div>

        {/* Upper-left, always visible, as on the real exam. */}
        <div className="exam-tools">
          <button type="button" className="exam-chip" onClick={() => tool("highlight")} title="Select text first">
            Highlight <span className="exam-key">Alt+H</span>
          </button>
          <button type="button" className="exam-chip" onClick={() => tool("strike")} title="Select text first">
            Strikethrough <span className="exam-key">Alt+S</span>
          </button>
        </div>

        <div className="exam-bar-right">
          {section.periodicTable && (
            <button type="button" className="exam-chip" onClick={() => setTableOpen(true)}>
              Periodic table <span className="exam-key">Alt+T</span>
            </button>
          )}
          <select
            className="exam-chip exam-select"
            value={theme}
            onChange={event => setTheme(event.target.value as Theme)}
            aria-label="Screen colours"
          >
            <option value="light">White background</option>
            <option value="dark">Black background</option>
            <option value="salmon">Salmon background</option>
          </select>
          <button
            type="button"
            className={low ? "exam-chip exam-clock is-low" : "exam-chip exam-clock"}
            onClick={() => setTimerHidden(value => !value)}
          >
            {timerHidden ? "Show time" : clock(seconds)}
          </button>
        </div>
      </header>

      <main className={passage ? "exam-body has-passage" : "exam-body"}>
        {passage && (
          <section className="exam-passage" aria-label="Passage" ref={passagePane}>
            <h2>{passage.title}</h2>
            {passage.paragraphs.map((paragraph, position) => (
              <Annotated
                key={position}
                text={paragraph}
                marks={marks[`${passage.id}-p${position}`]}
                annotateKey={`${passage.id}-p${position}`}
              />
            ))}
            {passage.figure && (
              <figure className="exam-figure">
                <div dangerouslySetInnerHTML={{ __html: passage.figure.markup }} />
                <figcaption>{passage.figure.caption}</figcaption>
              </figure>
            )}
          </section>
        )}

        <section className="exam-question" aria-label="Question">
          {question && (
            <>
              <Annotated text={question.stem} marks={marks[`${question.id}-stem`]} annotateKey={`${question.id}-stem`} className="exam-stem" />
              <ul className="exam-choices">
                {LETTERS.map(letter => {
                  const chosen = answers[question.id] === letter;
                  return (
                    <li key={letter}>
                      <button
                        type="button"
                        className={chosen ? "exam-choice is-chosen" : "exam-choice"}
                        onClick={() => choose(letter)}
                        aria-pressed={chosen}
                      >
                        <span className="exam-letter">{letter}</span>
                        <Annotated
                          as="span"
                          text={question.choices[letter]}
                          marks={marks[`${question.id}-${letter}`]}
                          annotateKey={`${question.id}-${letter}`}
                        />
                      </button>
                    </li>
                  );
                })}
              </ul>
            </>
          )}
        </section>
      </main>

      <footer className="exam-foot">
        <div className="exam-foot-left">
          <button type="button" className="exam-chip" onClick={() => setNavOpen(true)}>
            Navigator <span className="exam-key">Alt+V</span>
          </button>
          <button type="button" className={question && flagged.has(question.id) ? "exam-chip is-flagged" : "exam-chip"} onClick={toggleFlag}>
            {question && flagged.has(question.id) ? "Unflag" : "Flag for review"} <span className="exam-key">Alt+F</span>
          </button>
          <span className="exam-progress">
            {answeredCount} of {questions.length} answered
          </span>
        </div>
        <div className="exam-foot-right">
          <button type="button" className="exam-secondary" onClick={() => go(index - 1)} disabled={index === 0}>
            Previous <span className="exam-key">Alt+P</span>
          </button>
          <button
            type="button"
            className="exam-primary"
            onClick={() => {
              if (index === questions.length - 1) { stamp(); setMode("review"); } else { go(index + 1); }
            }}
          >
            {index === questions.length - 1 ? "Review the section" : "Next"} <span className="exam-key">Alt+N</span>
          </button>
        </div>
      </footer>

      {navOpen && (
        <div className="exam-window exam-window-small" role="dialog" aria-modal="true" aria-label="Navigator">
          <div className="exam-window-head">
            <h2>Navigator</h2>
            <button type="button" className="exam-window-close" onClick={() => setNavOpen(false)}>
              Close <span className="exam-key">Alt+C</span>
            </button>
          </div>
          <div className="exam-window-body">
            <table className="exam-review-table">
              <thead><tr><th>Question</th><th>Status</th><th>Flagged</th></tr></thead>
              <tbody>
                {questions.map((item, position) => (
                  <tr key={item.id} className={position === index ? "is-current" : undefined}>
                    <td>
                      <button type="button" className="exam-link" onClick={() => { setNavOpen(false); go(position); }}>
                        {position + 1}
                      </button>
                    </td>
                    <td>{answers[item.id] ? "Answered" : seen.has(item.id) ? "Incomplete" : "Unseen"}</td>
                    <td>{flagged.has(item.id) ? "Flagged" : ""}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {tableOpen && <PeriodicTable onClose={() => setTableOpen(false)} />}
    </div>
  );
}
