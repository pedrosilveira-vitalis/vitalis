"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";

type Highlight = {
  id: number;
  highlighted_text: string;
  start_offset: number;
  end_offset: number;
  note: string | null;
};

type Question = {
  id: number;
  question_number: number;
  question_text: string;
  choice_a: string;
  choice_b: string;
  choice_c: string;
  choice_d: string;
  correct_answer: string;
  explanation: string;
};

type Lesson = {
  id: number;
  lesson_number: number;
  title: string;
  description: string;
  content: string;
  estimated_minutes: number;
  unitId: number;
  unit_title: string;
  section: string;
  unit_number: number;
};

type LessonData = {
  lesson: Lesson;
  questions: Question[];
  highlights: Highlight[];
  progress: { read_complete: boolean; questions_correct: number; questions_total: number } | null;
  prevLesson: { id: number; lesson_number: number; title: string } | null;
  nextLesson: { id: number; lesson_number: number; title: string } | null;
  isAuthenticated: boolean;
};

const SECTION_NAMES: Record<string, string> = {
  "bio-biochem": "Bio / Biochem",
  "chem-phys": "Chem / Phys",
  "psych-soc": "Psych / Soc",
  "cars": "CARS",
};

const SECTION_COLORS: Record<string, string> = {
  "bio-biochem": "#a8324a",
  "chem-phys": "#2e4a6b",
  "psych-soc": "#8a6b2e",
  "cars": "#4a3b6b",
};

function Logo() {
  return (
    <div className="flex items-center gap-2.5">
      <svg width="32" height="18" viewBox="0 0 60 28" fill="none" className="flex-shrink-0">
        <path d="M2 14 L12 14 L16 6 L22 22 L28 4 L34 18 L38 14 L48 14" stroke="#a8324a" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" fill="none" />
        <circle cx="50" cy="14" r="2.2" fill="#a8324a" />
      </svg>
      <span className="font-serif font-semibold text-xl tracking-tight text-[#0c1a2e]">Vitalis</span>
    </div>
  );
}

function formatMarkdown(text: string): string {
  let html = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/^# (.+)$/gm, "<h1>$1</h1>")
    .replace(/^## (.+)$/gm, "<h2>$1</h2>")
    .replace(/^### (.+)$/gm, "<h3>$1</h3>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");

  const lines = html.split("\n");
  let out = "";
  let inList = false;
  for (const line of lines) {
    const li = line.match(/^[-*]\s+(.+)/);
    if (li) {
      if (!inList) { out += "<ul>"; inList = true; }
      out += "<li>" + li[1] + "</li>";
    } else {
      if (inList) { out += "</ul>"; inList = false; }
      if (line.trim()) {
        if (line.match(/^<h[1-6]>/)) out += line;
        else out += "<p>" + line + "</p>";
      }
    }
  }
  if (inList) out += "</ul>";
  return out;
}

export default function StudyLessonPage() {
  const params = useParams();
  const router = useRouter();
  const lessonId = parseInt(params.id as string, 10);

  const [data, setData] = useState<LessonData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [highlights, setHighlights] = useState<Highlight[]>([]);
  const [selection, setSelection] = useState<{ text: string; start: number; end: number; x: number; y: number } | null>(null);
  const [activeHighlight, setActiveHighlight] = useState<Highlight | null>(null);
  const [noteDraft, setNoteDraft] = useState("");

  const [showQuestions, setShowQuestions] = useState(false);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [submitted, setSubmitted] = useState(false);

  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isNaN(lessonId)) {
      setError("Invalid lesson");
      setLoading(false);
      return;
    }
    fetch(`/api/study/lessons/${lessonId}`)
      .then((r) => r.json())
      .then((d) => {
        if (d.error) setError(d.error);
        else {
          setData(d);
          setHighlights(d.highlights || []);
        }
        setLoading(false);
      })
      .catch(() => {
        setError("Couldn't load this lesson.");
        setLoading(false);
      });
  }, [lessonId]);

  // Render highlights into the content
  const renderedContent = useCallback(() => {
    if (!data) return "";
    const formatted = formatMarkdown(data.lesson.content);
    if (highlights.length === 0) return formatted;

    // We highlight by wrapping text matches. Since offsets are character-based on raw text,
    // we'll use the highlighted_text string directly to find and wrap in the rendered HTML.
    // This is robust enough for our use case.
    let result = formatted;
    const sorted = [...highlights].sort((a, b) => b.highlighted_text.length - a.highlighted_text.length);
    for (const h of sorted) {
      const escapedText = h.highlighted_text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const regex = new RegExp(escapedText, "g");
      const hasNote = h.note && h.note.trim().length > 0;
      result = result.replace(regex, (match) =>
        `<mark class="study-highlight" data-hid="${h.id}" data-hasnote="${hasNote ? "1" : "0"}">${match}${hasNote ? '<span class="note-indicator">●</span>' : ""}</mark>`
      );
    }
    return result;
  }, [data, highlights]);

  // Handle text selection within the content area
  function handleMouseUp() {
    if (!data?.isAuthenticated) return;
    const sel = window.getSelection();
    if (!sel || sel.isCollapsed || sel.toString().trim().length === 0) {
      setSelection(null);
      return;
    }
    if (!contentRef.current || !contentRef.current.contains(sel.anchorNode)) return;

    const range = sel.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    setSelection({
      text: sel.toString(),
      start: 0,
      end: 0,
      x: rect.left + rect.width / 2,
      y: rect.top - 10,
    });
  }

  // Click on existing highlight opens the note
  function handleContentClick(e: React.MouseEvent) {
    const target = e.target as HTMLElement;
    const mark = target.closest("mark.study-highlight") as HTMLElement | null;
    if (mark) {
      const hid = parseInt(mark.getAttribute("data-hid") || "", 10);
      const h = highlights.find((x) => x.id === hid);
      if (h) {
        setActiveHighlight(h);
        setNoteDraft(h.note || "");
        setSelection(null);
      }
    }
  }

  async function saveHighlight(withNote: boolean) {
    if (!selection || !data) return;
    try {
      const res = await fetch(`/api/study/lessons/${lessonId}/highlights`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          highlighted_text: selection.text,
          start_offset: 0,
          end_offset: 0,
          note: null,
        }),
      });
      if (res.ok) {
        const result = await res.json();
        const newHighlight: Highlight = result.highlight;
        setHighlights([...highlights, newHighlight]);
        setSelection(null);
        window.getSelection()?.removeAllRanges();
        if (withNote) {
          setActiveHighlight(newHighlight);
          setNoteDraft("");
        }
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function updateNote() {
    if (!activeHighlight) return;
    try {
      const res = await fetch(`/api/study/highlights/${activeHighlight.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note: noteDraft.trim() || null }),
      });
      if (res.ok) {
        setHighlights(highlights.map((h) =>
          h.id === activeHighlight.id ? { ...h, note: noteDraft.trim() || null } : h
        ));
        setActiveHighlight(null);
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function deleteHighlight() {
    if (!activeHighlight) return;
    try {
      const res = await fetch(`/api/study/highlights/${activeHighlight.id}`, {
        method: "DELETE",
      });
      if (res.ok) {
        setHighlights(highlights.filter((h) => h.id !== activeHighlight.id));
        setActiveHighlight(null);
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function markComplete() {
    if (!data?.isAuthenticated) return;
    try {
      await fetch(`/api/study/lessons/${lessonId}/progress`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ read_complete: true }),
      });
      if (data.nextLesson) {
        router.push(`/study/lessons/${data.nextLesson.id}`);
      } else {
        router.push(`/study/${data.lesson.section}`);
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function submitQuestions() {
    if (!data) return;
    let correct = 0;
    for (const q of data.questions) {
      if (answers[q.id] === q.correct_answer) correct++;
    }
    setSubmitted(true);
    if (data.isAuthenticated) {
      try {
        await fetch(`/api/study/lessons/${lessonId}/progress`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            questions_correct: correct,
            questions_total: data.questions.length,
            read_complete: true,
          }),
        });
      } catch (e) {
        console.error(e);
      }
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] flex items-center justify-center">
        <div className="text-center">
          <div className="flex items-center justify-center gap-2 mb-3">
            <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" />
            <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.15s" }} />
            <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.3s" }} />
          </div>
          <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Loading lesson...</div>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] flex items-center justify-center p-10">
        <div className="text-center max-w-md">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-50 mb-4">Error</div>
          <h1 className="font-serif text-3xl font-medium mb-4">{error || "Lesson not found"}</h1>
          <Link href="/study" className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]">
            ← Back to Study
          </Link>
        </div>
      </div>
    );
  }

  const accent = SECTION_COLORS[data.lesson.section] || "#0c1a2e";
  const answeredCount = Object.keys(answers).length;
  const correctCount = submitted ? data.questions.filter((q) => answers[q.id] === q.correct_answer).length : 0;

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans">
      <nav className="flex items-center justify-between px-8 py-4 border-b border-[#0c1a2e15] sticky top-0 bg-[#f5f1ea] z-30">
        <Logo />
        <div className="hidden md:flex gap-6 text-sm font-medium">
          <Link href="/" className="opacity-60 hover:opacity-100">Home</Link>
          <Link href="/tutor" className="opacity-60 hover:opacity-100">Tutor</Link>
          <Link href="/practice" className="opacity-60 hover:opacity-100">Practice</Link>
          <Link href="/flashcards" className="opacity-60 hover:opacity-100">Flashcards</Link>
          <Link href="/study" className="opacity-100 border-b border-[#a8324a] pb-0.5">Study</Link>
          <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
        </div>
        <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">Reading</div>
      </nav>

      <header className="px-10 pt-10 pb-6 border-b border-[#0c1a2e15] max-w-4xl mx-auto">
        <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-3 flex items-center gap-2 flex-wrap">
          <Link href="/study" className="hover:opacity-100 opacity-70">Study</Link>
          <span className="opacity-40">/</span>
          <Link href={`/study/${data.lesson.section}`} className="hover:opacity-100 opacity-70">{SECTION_NAMES[data.lesson.section]}</Link>
          <span className="opacity-40">/</span>
          <span>Unit {data.lesson.unit_number} · {data.lesson.unit_title}</span>
        </div>
        <h1 className="font-serif text-[clamp(32px,4vw,52px)] font-medium tracking-tight leading-tight mb-3">
          {data.lesson.title}
        </h1>
        <div className="flex items-center gap-4 font-mono text-[10px] tracking-[0.12em] uppercase opacity-55">
          <span>Lesson {data.lesson.lesson_number}</span>
          <span>·</span>
          <span>{data.lesson.estimated_minutes} min read</span>
          {data.progress?.read_complete && (
            <>
              <span>·</span>
              <span className="text-[#3e6b4a]">✓ Read</span>
            </>
          )}
        </div>
        {!data.isAuthenticated && (
          <div className="mt-4 p-3 bg-[#a8324a08] border border-[#a8324a25] rounded-lg text-[12px] opacity-80 max-w-2xl">
            <Link href="/sign-in" className="text-[#a8324a] font-medium hover:underline">Sign in</Link> to highlight, take notes, and save progress.
          </div>
        )}
      </header>

      <main className="max-w-3xl mx-auto px-10 py-10">
        <article
          ref={contentRef}
          className="study-content"
          onMouseUp={handleMouseUp}
          onClick={handleContentClick}
          dangerouslySetInnerHTML={{ __html: renderedContent() }}
        />

        {/* End-of-lesson questions */}
        <div className="mt-16 pt-10 border-t border-[#0c1a2e15]">
          {!showQuestions ? (
            <div className="text-center">
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-3">Check your understanding</div>
              <h2 className="font-serif text-2xl font-medium mb-3">5 questions on this lesson</h2>
              <p className="text-[14px] opacity-70 mb-5 max-w-md mx-auto">
                Optional, but recommended. Test what you remember before moving on.
              </p>
              <div className="flex gap-3 justify-center flex-wrap">
                <button
                  onClick={() => setShowQuestions(true)}
                  className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]"
                >
                  Start questions →
                </button>
                {data.isAuthenticated && (
                  <button
                    onClick={markComplete}
                    className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a]"
                  >
                    Skip · mark complete
                  </button>
                )}
              </div>
            </div>
          ) : (
            <div>
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-3 flex items-center justify-between">
                <span>Check your understanding</span>
                {submitted && (
                  <span className="text-[#0c1a2e]">{correctCount} / {data.questions.length} correct</span>
                )}
                {!submitted && (
                  <span>{answeredCount} / {data.questions.length} answered</span>
                )}
              </div>
              <div className="space-y-7">
                {data.questions.map((q) => {
                  const userAns = answers[q.id];
                  return (
                    <div key={q.id} className="border border-[#0c1a2e15] rounded-2xl p-6">
                      <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Q{q.question_number}</div>
                      <p className="text-[15px] leading-relaxed mb-4 font-medium">{q.question_text}</p>
                      <div className="space-y-2">
                        {(["A","B","C","D"] as const).map((letter) => {
                          const text = letter === "A" ? q.choice_a : letter === "B" ? q.choice_b : letter === "C" ? q.choice_c : q.choice_d;
                          const isSelected = userAns === letter;
                          const isCorrect = letter === q.correct_answer;
                          let cls = "border-[#0c1a2e25]";
                          let bg = "bg-transparent";
                          if (submitted) {
                            if (isCorrect) { cls = "border-[#3e6b4a]"; bg = "bg-[#3e6b4a15]"; }
                            else if (isSelected && !isCorrect) { cls = "border-[#a8324a]"; bg = "bg-[#a8324a15]"; }
                          } else if (isSelected) { cls = "border-[#0c1a2e]"; bg = "bg-[#0c1a2e0a]"; }
                          return (
                            <button
                              key={letter}
                              onClick={() => !submitted && setAnswers({...answers, [q.id]: letter})}
                              disabled={submitted}
                              className={`w-full text-left p-3 rounded-xl border-2 transition-all ${cls} ${bg} ${!submitted ? "hover:border-[#0c1a2e] hover:bg-[#0c1a2e0a] cursor-pointer" : "cursor-default"}`}
                            >
                              <div className="flex gap-3">
                                <span className="font-serif font-semibold w-5 flex-shrink-0">{letter}</span>
                                <span className="text-[13.5px] leading-relaxed">{text}</span>
                              </div>
                            </button>
                          );
                        })}
                      </div>
                      {submitted && (
                        <div className="mt-4 p-4 bg-[#0c1a2e0a] rounded-xl text-[13px] leading-relaxed">
                          <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-1">Explanation</div>
                          {q.explanation}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {!submitted ? (
                <div className="mt-7 flex gap-3 justify-center">
                  <button
                    onClick={submitQuestions}
                    disabled={answeredCount < data.questions.length}
                    className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a] disabled:opacity-30 disabled:cursor-not-allowed"
                  >
                    Submit answers →
                  </button>
                </div>
              ) : (
                <div className="mt-7 flex gap-3 justify-center flex-wrap">
                  {data.nextLesson ? (
                    <Link
                      href={`/study/lessons/${data.nextLesson.id}`}
                      className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]"
                    >
                      Next lesson →
                    </Link>
                  ) : (
                    <Link
                      href={`/study/${data.lesson.section}`}
                      className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]"
                    >
                      Back to unit
                    </Link>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Nav at bottom */}
        <div className="mt-12 pt-6 border-t border-[#0c1a2e15] flex justify-between gap-4 flex-wrap">
          {data.prevLesson ? (
            <Link href={`/study/lessons/${data.prevLesson.id}`} className="font-mono text-[11px] tracking-[0.1em] uppercase opacity-60 hover:opacity-100">
              ← Previous: {data.prevLesson.title}
            </Link>
          ) : <div />}
          {data.nextLesson ? (
            <Link href={`/study/lessons/${data.nextLesson.id}`} className="font-mono text-[11px] tracking-[0.1em] uppercase opacity-60 hover:opacity-100 text-right">
              Next: {data.nextLesson.title} →
            </Link>
          ) : (
            <Link href={`/study/${data.lesson.section}`} className="font-mono text-[11px] tracking-[0.1em] uppercase opacity-60 hover:opacity-100 text-right">
              Back to {SECTION_NAMES[data.lesson.section]} →
            </Link>
          )}
        </div>
      </main>

      {/* Selection toolbar (appears when user highlights text) */}
      {selection && (
        <div
          className="fixed z-40 bg-[#0c1a2e] text-[#f5f1ea] rounded-full shadow-lg flex items-center gap-1 px-1 py-1"
          style={{
            top: selection.y,
            left: selection.x,
            transform: "translate(-50%, -100%)",
          }}
        >
          <button
            onClick={() => saveHighlight(false)}
            className="px-3 py-1.5 text-[11px] font-mono uppercase tracking-[0.08em] hover:bg-[#1a2c4a] rounded-full"
          >
            Highlight
          </button>
          <button
            onClick={() => saveHighlight(true)}
            className="px-3 py-1.5 text-[11px] font-mono uppercase tracking-[0.08em] hover:bg-[#1a2c4a] rounded-full"
          >
            + Note
          </button>
        </div>
      )}

      {/* Note popup (appears when user clicks a highlight) */}
      {activeHighlight && (
        <div
          className="fixed inset-0 bg-[#0c1a2e66] z-50 flex items-center justify-center p-6"
          onClick={() => setActiveHighlight(null)}
        >
          <div
            className="bg-[#f5f1ea] rounded-2xl max-w-lg w-full p-7 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-3">Note</div>
            <div className="bg-[#fef3a3] rounded-lg p-3 mb-4 text-[13px] leading-relaxed italic">
              &quot;{activeHighlight.highlighted_text}&quot;
            </div>
            <textarea
              value={noteDraft}
              onChange={(e) => setNoteDraft(e.target.value)}
              placeholder="Add a note about this passage..."
              rows={4}
              className="w-full px-3 py-2.5 border border-[#0c1a2e25] rounded-xl bg-[#f5f1ea] outline-none text-[14px] focus:border-[#0c1a2e] resize-none"
            />
            <div className="mt-5 flex gap-3 justify-between">
              <button
                onClick={deleteHighlight}
                className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-50 hover:opacity-100 hover:text-[#a8324a]"
              >
                Delete highlight
              </button>
              <div className="flex gap-3">
                <button
                  onClick={() => setActiveHighlight(null)}
                  className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-4 py-2.5 rounded-full hover:bg-[#0c1a2e0a]"
                >
                  Cancel
                </button>
                <button
                  onClick={updateNote}
                  className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-4 py-2.5 rounded-full hover:bg-[#1a2c4a]"
                >
                  Save note
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <style jsx global>{`
        .study-content p { font-size: 16px; line-height: 1.75; margin-bottom: 18px; color: #0c1a2ed8; }
        .study-content h1 { font-family: 'Fraunces', serif; font-size: 28px; font-weight: 500; margin: 32px 0 14px; color: #0c1a2e; }
        .study-content h2 { font-family: 'Fraunces', serif; font-size: 22px; font-weight: 500; margin: 28px 0 12px; color: #0c1a2e; }
        .study-content h3 { font-family: 'Fraunces', serif; font-size: 19px; font-weight: 600; margin: 22px 0 10px; color: ${accent}; }
        .study-content strong { font-weight: 600; color: #0c1a2e; }
        .study-content em { font-style: italic; }
        .study-content code { background: #0c1a2e14; padding: 2px 6px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 14px; }
        .study-content ul { margin: 14px 0 18px; padding-left: 28px; }
        .study-content li { font-size: 16px; line-height: 1.7; margin-bottom: 8px; color: #0c1a2ed8; }
        .study-content mark.study-highlight {
          background: #fef3a3;
          padding: 1px 0;
          border-radius: 2px;
          cursor: pointer;
          position: relative;
          transition: background 0.15s;
        }
        .study-content mark.study-highlight:hover {
          background: #fde672;
        }
        .study-content mark.study-highlight .note-indicator {
          color: #a8324a;
          font-size: 10px;
          margin-left: 2px;
          vertical-align: super;
          line-height: 0;
        }
      `}</style>
    </div>
  );
}