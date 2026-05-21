"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";

type Choice = "A" | "B" | "C" | "D";

type Question = {
  id: string;
  stem: string;
  choices: { A: string; B: string; C: string; D: string };
  correctAnswer: Choice;
  explanation: string;
  wrongAnswerExplanations: { A?: string; B?: string; C?: string; D?: string };
  concept: string;
  difficulty: string;
};

type PassageData = {
  title: string;
  content: string;
};

type QuestionSet = {
  format: "passage" | "standalone";
  passage?: PassageData;
  questions: Question[];
  section: string;
};

type TutorMessage = { role: "user" | "assistant"; content: string };

const SECTION_NAMES: Record<string, string> = {
  "bio-biochem": "Bio / Biochem",
  "chem-phys": "Chem / Phys",
  "psych-soc": "Psych / Soc",
  "cars": "CARS",
  "mixed": "Mixed Practice",
};

export default function PracticeSessionPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const section = (params.section as string) || "mixed";
  const format = (searchParams.get("format") as "standalone" | "passage") || "standalone";

  const [questionSet, setQuestionSet] = useState<QuestionSet | null>(null);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [selected, setSelected] = useState<Choice | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Stats
  const [totalAnswered, setTotalAnswered] = useState(0);
  const [totalCorrect, setTotalCorrect] = useState(0);

  // Timer
  const [timerOn, setTimerOn] = useState(false);
  const [secondsElapsed, setSecondsElapsed] = useState(0);

  // Pop-up tutor
  const [showTutor, setShowTutor] = useState(false);
  const [tutorMessages, setTutorMessages] = useState<TutorMessage[]>([]);
  const [tutorInput, setTutorInput] = useState("");
  const [tutorLoading, setTutorLoading] = useState(false);

  // Load first question on mount
  useEffect(() => {
    loadNewQuestion();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Timer tick
  useEffect(() => {
    if (!timerOn || submitted) return;
    const id = setInterval(() => setSecondsElapsed((s) => s + 1), 1000);
    return () => clearInterval(id);
  }, [timerOn, submitted, currentIdx]);

  async function loadNewQuestion() {
    setLoading(true);
    setError("");
    setSelected(null);
    setSubmitted(false);
    setSecondsElapsed(0);
    setShowTutor(false);
    setTutorMessages([]);
    try {
      const res = await fetch("/api/practice/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ section, format }),
      });
      const data = await res.json();
      if (data.questions && data.questions.length > 0) {
        setQuestionSet(data);
        setCurrentIdx(0);
      } else {
        setError("Couldn't generate a question. Try again?");
      }
    } catch {
      setError("Connection issue. Try again?");
    }
    setLoading(false);
  }

  function submitAnswer() {
    if (!selected || !questionSet) return;
    setSubmitted(true);
    setTotalAnswered((n) => n + 1);
    const correct = selected === questionSet.questions[currentIdx].correctAnswer;
    if (correct) setTotalCorrect((n) => n + 1);
    else {
      // Auto-open tutor on wrong answer
      const q = questionSet.questions[currentIdx];
      const wrongExp = q.wrongAnswerExplanations[selected] || "";
      const seedMessage =
        `**The correct answer is ${q.correctAnswer}.**\n\n${q.explanation}\n\n**Why ${selected} is wrong:** ${wrongExp}\n\nWant me to dig deeper? Ask anything — I'll walk you through it.`;
      setTutorMessages([{ role: "assistant", content: seedMessage }]);
      setTimeout(() => setShowTutor(true), 400);
    }
  }

  function nextQuestion() {
    if (!questionSet) return;
    // If passage format and more questions remain, advance within the set
    if (questionSet.format === "passage" && currentIdx < questionSet.questions.length - 1) {
      setCurrentIdx(currentIdx + 1);
      setSelected(null);
      setSubmitted(false);
      setSecondsElapsed(0);
      setShowTutor(false);
      setTutorMessages([]);
    } else {
      loadNewQuestion();
    }
  }async function askTutor() {
    if (!tutorInput.trim() || tutorLoading || !questionSet) return;
    const q = questionSet.questions[currentIdx];
    const userMsg: TutorMessage = { role: "user", content: tutorInput.trim() };
    const newMessages = [...tutorMessages, userMsg];
    setTutorMessages(newMessages);
    setTutorInput("");
    setTutorLoading(true);

    try {
      const res = await fetch("/api/practice/explain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: q,
          studentAnswer: selected,
          messages: newMessages,
        }),
      });
      const data = await res.json();
      if (data.reply) {
        setTutorMessages([...newMessages, { role: "assistant", content: data.reply }]);
      } else {
        setTutorMessages([
          ...newMessages,
          { role: "assistant", content: "Sorry — I had trouble responding. Try again?" },
        ]);
      }
    } catch {
      setTutorMessages([
        ...newMessages,
        { role: "assistant", content: "Connection issue. Try again?" },
      ]);
    }
    setTutorLoading(false);
  }

  function formatMessage(text: string): string {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*([^*]+)\*/g, "<em>$1</em>")
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\n\n/g, "</p><p>")
      .replace(/\n/g, "<br/>");
  }

  function formatTime(s: number): string {
    const min = Math.floor(s / 60);
    const sec = s % 60;
    return `${min}:${sec.toString().padStart(2, "0")}`;
  }

  const currentQ = questionSet?.questions[currentIdx];
  const isCorrect = submitted && selected === currentQ?.correctAnswer;
  const accuracy = totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0;return (
    <div className="min-h-screen bg-[#f3efe7] text-[#161410] font-sans flex flex-col">
      {/* Nav */}
      <header className="flex items-center justify-between px-8 py-4 border-b border-[#16141015] sticky top-0 bg-[#f3efe7] z-30">
        <div className="flex items-center gap-3">
          <span className="w-2.5 h-2.5 rounded-full bg-[#c54a2a] shadow-[0_0_0_4px_#c54a2a22]" />
          <span className="font-serif font-semibold text-xl tracking-tight">Vitalis</span>
        </div>
        <div className="hidden md:flex gap-7 text-sm font-medium">
          <Link href="/" className="opacity-60 hover:opacity-100">Home</Link>
          <Link href="/tutor" className="opacity-60 hover:opacity-100">Tutor</Link>
          <Link href="/practice" className="opacity-100 border-b border-[#c54a2a] pb-0.5">Practice</Link>
          <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
        </div>
        <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">
          {SECTION_NAMES[section] || section}
        </div>
      </header>

      {/* Stats bar */}
      <div className="px-8 py-3 border-b border-[#16141015] flex items-center justify-between text-[12px] font-mono tracking-[0.08em] uppercase">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="opacity-50">Answered:</span>
            <span className="font-serif text-base font-medium">{totalAnswered}</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="opacity-50">Accuracy:</span>
            <span className="font-serif text-base font-medium">{totalAnswered > 0 ? `${accuracy}%` : "—"}</span>
          </div>
          {timerOn && (
            <div className="flex items-center gap-2">
              <span className="opacity-50">Time:</span>
              <span className="font-serif text-base font-medium">{formatTime(secondsElapsed)}</span>
            </div>
          )}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setTimerOn(!timerOn)}
            className="text-[10px] tracking-[0.1em] uppercase opacity-60 hover:opacity-100 px-2 py-1 border border-[#16141025] rounded"
          >
            {timerOn ? "Timer on" : "Timer off"}
          </button>
          <Link
            href="/practice"
            className="text-[10px] tracking-[0.1em] uppercase opacity-60 hover:opacity-100 px-2 py-1 border border-[#16141025] rounded"
          >
            ← Sections
          </Link>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-3">
              <span className="w-2 h-2 rounded-full bg-[#161410] animate-bounce" />
              <span className="w-2 h-2 rounded-full bg-[#161410] animate-bounce" style={{ animationDelay: "0.15s" }} />
              <span className="w-2 h-2 rounded-full bg-[#161410] animate-bounce" style={{ animationDelay: "0.3s" }} />
            </div>
            <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Generating question...</div>
          </div>
        </div>
      )}

      {/* Error */}
      {!loading && error && (
        <div className="flex-1 flex items-center justify-center px-8">
          <div className="text-center max-w-md">
            <div className="text-[#c54a2a] text-sm mb-4">{error}</div>
            <button
              onClick={loadNewQuestion}
              className="font-mono text-xs uppercase tracking-[0.08em] bg-[#161410] text-[#f3efe7] px-5 py-3 rounded-full hover:bg-[#2a2620]"
            >
              Try again
            </button>
          </div>
        </div>
      )}{/* Question */}
      {!loading && !error && currentQ && (
        <div className="flex-1 overflow-y-auto px-8 py-8 grid lg:grid-cols-2 gap-10 max-w-7xl mx-auto w-full">
          {/* Left: passage if exists */}
          {questionSet?.passage && (
            <div className="bg-[#ebe5d6] rounded-2xl p-7 max-h-[70vh] overflow-y-auto">
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Passage</div>
              <h2 className="font-serif text-xl font-medium mb-4 leading-tight">{questionSet.passage.title}</h2>
              <div className="text-[14px] leading-relaxed whitespace-pre-wrap">{questionSet.passage.content}</div>
            </div>
          )}

          {/* Right: question */}
          <div className={questionSet?.passage ? "" : "lg:col-span-2 max-w-3xl mx-auto w-full"}>
            <div className="flex items-center justify-between mb-4">
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">
                Question {currentIdx + 1}{questionSet && questionSet.questions.length > 1 ? ` of ${questionSet.questions.length}` : ""}
              </div>
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-40">
                {currentQ.difficulty}
              </div>
            </div>

            <div className="text-[16px] leading-relaxed mb-6 whitespace-pre-wrap">{currentQ.stem}</div>

            <div className="space-y-2.5">
              {(["A", "B", "C", "D"] as Choice[]).map((letter) => {
                const isSelected = selected === letter;
                const isCorrectChoice = letter === currentQ.correctAnswer;
                let borderClass = "border-[#16141025]";
                let bgClass = "bg-transparent";
                if (submitted) {
                  if (isCorrectChoice) {
                    borderClass = "border-[#3e5641]";
                    bgClass = "bg-[#3e564115]";
                  } else if (isSelected && !isCorrectChoice) {
                    borderClass = "border-[#c54a2a]";
                    bgClass = "bg-[#c54a2a15]";
                  }
                } else if (isSelected) {
                  borderClass = "border-[#161410]";
                  bgClass = "bg-[#1614100a]";
                }

                return (
                  <button
                    key={letter}
                    onClick={() => !submitted && setSelected(letter)}
                    disabled={submitted}
                    className={`w-full text-left p-4 rounded-xl border-2 transition-all ${borderClass} ${bgClass} ${
                      !submitted ? "hover:border-[#161410] hover:bg-[#1614100a] cursor-pointer" : "cursor-default"
                    }`}
                  >
                    <div className="flex gap-3">
                      <span className="font-serif font-semibold w-6 flex-shrink-0">{letter}</span>
                      <span className="text-[14px] leading-relaxed">{currentQ.choices[letter]}</span>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Submit or result */}
            {!submitted ? (
              <button
                onClick={submitAnswer}
                disabled={!selected}
                className="mt-7 font-mono text-xs uppercase tracking-[0.08em] bg-[#161410] text-[#f3efe7] px-6 py-3.5 rounded-full hover:bg-[#2a2620] disabled:opacity-30 disabled:cursor-not-allowed"
              >
                Submit answer →
              </button>
            ) : (
              <div className="mt-7">
                <div className={`p-5 rounded-xl mb-5 ${isCorrect ? "bg-[#3e564115] border border-[#3e564140]" : "bg-[#c54a2a15] border border-[#c54a2a40]"}`}>
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-70 mb-2">
                    {isCorrect ? "✓ Correct" : "✗ Incorrect"}
                  </div>
                  <div className="text-[14px] leading-relaxed">
                    {isCorrect ? (
                      <span><strong>Answer: {currentQ.correctAnswer}.</strong> {currentQ.explanation}</span>
                    ) : (
                      <span>The correct answer is <strong>{currentQ.correctAnswer}</strong>. Vitalis is breaking it down for you →</span>
                    )}
                  </div>
                  {isCorrect && (
                    <button
                      onClick={() => {
                        setTutorMessages([
                          { role: "assistant", content: `Nice work! The concept here is **${currentQ.concept}**. Want me to go deeper on this — variations, related topics, or what to watch out for on the MCAT?` },
                        ]);
                        setShowTutor(true);
                      }}
                      className="mt-3 font-mono text-[10px] tracking-[0.1em] uppercase opacity-60 hover:opacity-100"
                    >
                      Ask Vitalis →
                    </button>
                  )}
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={nextQuestion}
                    className="font-mono text-xs uppercase tracking-[0.08em] bg-[#161410] text-[#f3efe7] px-6 py-3.5 rounded-full hover:bg-[#2a2620]"
                  >
                    Next question →
                  </button>
                  <Link
                    href="/practice"
                    className="font-mono text-xs uppercase tracking-[0.08em] border border-[#16141025] px-6 py-3.5 rounded-full hover:bg-[#1614100a]"
                  >
                    Stop session
                  </Link>
                </div>
              </div>
            )}
          </div>
        </div>
      )}{/* Tutor pop-up */}
      {showTutor && currentQ && (
        <div className="fixed inset-0 bg-[#16141066] z-50 flex items-end md:items-center justify-center p-0 md:p-6">
          <div className="bg-[#f3efe7] w-full md:max-w-2xl md:rounded-2xl shadow-2xl flex flex-col max-h-[90vh] md:max-h-[80vh] rounded-t-2xl">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#16141015]">
              <div className="flex items-center gap-2.5">
                <span className="w-2 h-2 rounded-full bg-[#c54a2a]" />
                <div>
                  <div className="font-serif font-medium">Vitalis explains</div>
                  <div className="font-mono text-[10px] uppercase tracking-[0.12em] opacity-50">{currentQ.concept}</div>
                </div>
              </div>
              <button
                onClick={() => setShowTutor(false)}
                className="font-mono text-[10px] uppercase tracking-[0.1em] opacity-60 hover:opacity-100 px-2 py-1"
              >
                Close ×
              </button>
            </div>

            <div className="flex-1 overflow-y-auto px-6 py-5 flex flex-col gap-4">
              {tutorMessages.map((msg, i) =>
                msg.role === "user" ? (
                  <div key={i} className="self-end max-w-[80%] bg-[#161410] text-[#f3efe7] px-4 py-2.5 rounded-2xl rounded-br-md text-[14px] leading-relaxed">
                    {msg.content}
                  </div>
                ) : (
                  <div
                    key={i}
                    className="self-start max-w-[90%] text-[14px] leading-relaxed tutor-content"
                    dangerouslySetInnerHTML={{ __html: `<p>${formatMessage(msg.content)}</p>` }}
                  />
                )
              )}
              {tutorLoading && (
                <div className="self-start flex items-center gap-1.5 opacity-60 py-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#161410] animate-bounce" />
                  <span className="w-1.5 h-1.5 rounded-full bg-[#161410] animate-bounce" style={{ animationDelay: "0.15s" }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-[#161410] animate-bounce" style={{ animationDelay: "0.3s" }} />
                </div>
              )}
            </div>

            <div className="border-t border-[#16141015] px-6 py-4 flex gap-3 items-center">
              <input
                value={tutorInput}
                onChange={(e) => setTutorInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    askTutor();
                  }
                }}
                placeholder="Ask a follow-up..."
                className="flex-1 bg-transparent border-none outline-none text-[14px] placeholder:text-[#16141066]"
              />
              <button
                onClick={askTutor}
                disabled={!tutorInput.trim() || tutorLoading}
                className="bg-[#161410] text-[#f3efe7] w-9 h-9 rounded-full flex items-center justify-center disabled:opacity-30"
              >
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                  <line x1="22" y1="2" x2="11" y2="13" />
                  <polygon points="22 2 15 22 11 13 2 9 22 2" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}

      <style jsx global>{`
        .tutor-content p { margin-bottom: 8px; }
        .tutor-content p:last-child { margin-bottom: 0; }
        .tutor-content strong { font-weight: 600; }
        .tutor-content em { font-style: italic; }
        .tutor-content code { background: #16141014; padding: 1px 5px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 12px; }
      `}</style>
    </div>
  );
}