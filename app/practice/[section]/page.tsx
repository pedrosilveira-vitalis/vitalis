"use client";

import { useEffect, useState, useRef, useCallback, Suspense } from "react";
import Link from "next/link";
import { useParams, useSearchParams, useRouter } from "next/navigation";
import MainNav from "@/components/MainNav";

type Question = {
  id: string;
  question_text: string;
  choice_a: string;
  choice_b: string;
  choice_c: string;
  choice_d: string;
  correct_answer: string;
  explanation: string;
  topic: string;
};

type Message = { role: "user" | "assistant"; content: string };

const SECTION_NAMES: Record<string, string> = {
  "bio-biochem": "Bio / Biochem",
  "chem-phys": "Chem / Phys",
  "psych-soc": "Psych / Soc",
  "cars": "CARS",
  "mixed": "Mixed",
};

const SECTION_COLORS: Record<string, string> = {
  "bio-biochem": "#a8324a",
  "chem-phys": "#2e4a6b",
  "psych-soc": "#8a6b2e",
  "cars": "#4a3b6b",
  "mixed": "#0c1a2e",
};

function PracticeSessionContent() {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const sectionId = (params.section as string) || "mixed";
  const numQuestions = parseInt(searchParams.get("n") || "10", 10);
  const difficulty = (searchParams.get("d") as "mixed" | "easy" | "medium" | "hard") || "mixed";

  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [results, setResults] = useState<{ qId: string; correct: boolean; selected: string }[]>([]);
  const [sessionComplete, setSessionComplete] = useState(false);

  // Tutor pop-up state
  const [showTutor, setShowTutor] = useState(false);
  const [tutorMessages, setTutorMessages] = useState<Message[]>([]);
  const [tutorInput, setTutorInput] = useState("");
  const [tutorLoading, setTutorLoading] = useState(false);
  const tutorRef = useRef<HTMLDivElement>(null);

  const accent = SECTION_COLORS[sectionId] || "#0c1a2e";
  const sectionName = SECTION_NAMES[sectionId] || sectionId;

  const loadQuestions = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/practice/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ section: sectionId, count: numQuestions, difficulty }),
      });
      const data = await res.json();
      if (!data.questions || data.questions.length === 0) {
        setError("Couldn't load questions. Try again.");
        setLoading(false);
        return;
      }
      setQuestions(data.questions);
      setLoading(false);
    } catch {
      setError("Couldn't load questions. Try again.");
      setLoading(false);
    }
  }, [sectionId, numQuestions, difficulty]);

  useEffect(() => {
    loadQuestions();
  }, [loadQuestions]);

  useEffect(() => {
    if (tutorRef.current) {
      tutorRef.current.scrollTop = tutorRef.current.scrollHeight;
    }
  }, [tutorMessages, tutorLoading]);

  const currentQ = questions[currentIdx];

  function handleSubmit() {
    if (!selectedAnswer || !currentQ) return;
    const isCorrect = selectedAnswer === currentQ.correct_answer;
    setResults([...results, { qId: currentQ.id, correct: isCorrect, selected: selectedAnswer }]);
    setShowExplanation(true);
  }

  function handleNext() {
    if (currentIdx + 1 >= questions.length) {
      setSessionComplete(true);
      return;
    }
    setCurrentIdx(currentIdx + 1);
    setSelectedAnswer(null);
    setShowExplanation(false);
    setShowTutor(false);
    setTutorMessages([]);
  }

  function openTutor() {
    if (!currentQ) return;
    setShowTutor(true);
    const lastResult = results[results.length - 1];
    const wrongAnswerText =
      lastResult.selected === "A" ? currentQ.choice_a :
      lastResult.selected === "B" ? currentQ.choice_b :
      lastResult.selected === "C" ? currentQ.choice_c :
      currentQ.choice_d;
    const correctText =
      currentQ.correct_answer === "A" ? currentQ.choice_a :
      currentQ.correct_answer === "B" ? currentQ.choice_b :
      currentQ.correct_answer === "C" ? currentQ.choice_c :
      currentQ.choice_d;
    const initialUserMsg = `I got this question wrong. Help me understand why.

Question: ${currentQ.question_text}

I picked: ${lastResult.selected}. ${wrongAnswerText}
Correct: ${currentQ.correct_answer}. ${correctText}

The explanation says: ${currentQ.explanation}

Can you explain this more deeply and help me build the right intuition so I get questions like this right next time?`;

    setTutorMessages([{ role: "user", content: initialUserMsg }]);
    setTutorLoading(true);
    fetch("/api/practice/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: [{ role: "user", content: initialUserMsg }] }),
    })
      .then((r) => r.json())
      .then((d) => {
        setTutorMessages([
          { role: "user", content: initialUserMsg },
          { role: "assistant", content: d.reply || "Sorry — connection issue. Try again?" },
        ]);
        setTutorLoading(false);
      })
      .catch(() => {
        setTutorMessages([
          { role: "user", content: initialUserMsg },
          { role: "assistant", content: "Sorry — connection issue. Try again?" },
        ]);
        setTutorLoading(false);
      });
  }

  async function sendTutorMessage() {
    if (!tutorInput.trim() || tutorLoading) return;
    const newMessages: Message[] = [...tutorMessages, { role: "user" as const, content: tutorInput.trim() }];
    setTutorMessages(newMessages);
    setTutorInput("");
    setTutorLoading(true);
    try {
      const res = await fetch("/api/practice/explain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: newMessages }),
      });
      const data = await res.json();
      setTutorMessages([...newMessages, { role: "assistant" as const, content: data.reply || "Sorry — connection issue." }]);
    } catch {
      setTutorMessages([...newMessages, { role: "assistant" as const, content: "Sorry — connection issue." }]);
    }
    setTutorLoading(false);
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
          <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Generating {numQuestions} {sectionName} questions...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] flex items-center justify-center p-10">
        <div className="text-center max-w-md">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-50 mb-4">Error</div>
          <h1 className="font-serif text-3xl font-medium mb-4">{error}</h1>
          <div className="flex gap-3 justify-center">
            <button onClick={loadQuestions} className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full">
              Try again
            </button>
            <Link href="/practice" className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full">
              Back
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (sessionComplete) {
    const correctCount = results.filter((r) => r.correct).length;
    const pct = Math.round((correctCount / results.length) * 100);
    return (
      <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e]">
        <MainNav active="practice" badge="Session complete" />
        <div className="max-w-2xl mx-auto px-10 py-20 text-center">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4">Session complete</div>
          <h1 className="font-serif text-[clamp(48px,6vw,88px)] font-medium tracking-tight mb-2">
            <span style={{ color: accent }}>{correctCount}</span> / {results.length}
          </h1>
          <p className="font-mono text-[14px] tracking-[0.1em] uppercase opacity-65 mb-10">{pct}% correct</p>
          <div className="flex gap-3 justify-center flex-wrap">
            <Link href={`/practice/${sectionId}?n=${numQuestions}&d=${difficulty}`} className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]">
              New session →
            </Link>
            <Link href="/practice" className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a]">
              Pick another section
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (!currentQ) return null;

  const isCorrect = selectedAnswer === currentQ.correct_answer;

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e]">
      <MainNav active="practice" badge={`${currentIdx + 1} / ${questions.length}`} />

      <div className="max-w-4xl mx-auto px-10 py-10">
        <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-3 flex items-center gap-2">
          <Link href="/practice" className="hover:opacity-100 opacity-70">Practice</Link>
          <span className="opacity-40">/</span>
          <span style={{ color: accent }}>{sectionName}</span>
          <span className="opacity-40">·</span>
          <span>{currentQ.topic}</span>
        </div>

        <div className="mb-7 flex items-center gap-3">
          <div className="flex-1 h-1.5 bg-[#0c1a2e15] rounded-full overflow-hidden">
            <div className="h-full transition-all" style={{ width: `${((currentIdx + (showExplanation ? 1 : 0)) / questions.length) * 100}%`, backgroundColor: accent }} />
          </div>
          <div className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-55 flex-shrink-0">
            {currentIdx + 1} / {questions.length}
          </div>
        </div>

        <h1 className="font-serif text-[clamp(22px,2.6vw,30px)] font-medium leading-snug mb-7">
          {currentQ.question_text}
        </h1>

        <div className="space-y-3 mb-6">
          {(["A", "B", "C", "D"] as const).map((letter) => {
            const text = letter === "A" ? currentQ.choice_a : letter === "B" ? currentQ.choice_b : letter === "C" ? currentQ.choice_c : currentQ.choice_d;
            const isSel = selectedAnswer === letter;
            const isAns = letter === currentQ.correct_answer;
            let cls = "border-[#0c1a2e25]";
            let bg = "bg-transparent";
            if (showExplanation) {
              if (isAns) { cls = "border-[#3e6b4a]"; bg = "bg-[#3e6b4a15]"; }
              else if (isSel && !isAns) { cls = "border-[#a8324a]"; bg = "bg-[#a8324a15]"; }
            } else if (isSel) { cls = "border-[#0c1a2e]"; bg = "bg-[#0c1a2e0a]"; }
            return (
              <button
                key={letter}
                onClick={() => !showExplanation && setSelectedAnswer(letter)}
                disabled={showExplanation}
                className={`w-full text-left p-4 rounded-xl border-2 transition-all ${cls} ${bg} ${!showExplanation ? "hover:border-[#0c1a2e] hover:bg-[#0c1a2e0a] cursor-pointer" : "cursor-default"}`}
              >
                <div className="flex gap-3">
                  <span className="font-serif font-semibold w-6 flex-shrink-0">{letter}</span>
                  <span className="text-[15px] leading-relaxed">{text}</span>
                </div>
              </button>
            );
          })}
        </div>

        {!showExplanation ? (
          <div className="flex justify-end">
            <button
              onClick={handleSubmit}
              disabled={!selectedAnswer}
              className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a] disabled:opacity-30 disabled:cursor-not-allowed"
            >
              Submit →
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className={`p-5 rounded-xl border ${isCorrect ? "border-[#3e6b4a] bg-[#3e6b4a08]" : "border-[#a8324a] bg-[#a8324a08]"}`}>
              <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-2">
                {isCorrect ? "✓ Correct" : "✗ Incorrect"}
              </div>
              <div className="text-[14px] leading-relaxed">{currentQ.explanation}</div>
            </div>

            <div className="flex justify-between items-center flex-wrap gap-3">
              {!isCorrect && !showTutor && (
                <button
                  onClick={openTutor}
                  className="font-mono text-xs uppercase tracking-[0.08em] border-2 border-[#a8324a] text-[#a8324a] px-5 py-3 rounded-full hover:bg-[#a8324a] hover:text-[#f5f1ea] transition-all"
                >
                  Ask the tutor →
                </button>
              )}
              <div className="ml-auto">
                <button
                  onClick={handleNext}
                  className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]"
                >
                  {currentIdx + 1 >= questions.length ? "Finish session →" : "Next question →"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Tutor pop-up */}
      {showTutor && (
        <div className="fixed inset-0 bg-[#0c1a2e88] z-50 flex items-end md:items-center justify-center p-0 md:p-6" onClick={() => setShowTutor(false)}>
          <div className="bg-[#f5f1ea] rounded-t-2xl md:rounded-2xl max-w-3xl w-full max-h-[85vh] flex flex-col shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="px-6 py-4 border-b border-[#0c1a2e15] flex items-center justify-between flex-shrink-0">
              <div className="flex items-center gap-3">
                <span className="w-2 h-2 rounded-full bg-[#a8324a] animate-pulse" />
                <div className="font-serif text-lg font-medium">Tutor · helping you</div>
              </div>
              <button onClick={() => setShowTutor(false)} className="opacity-50 hover:opacity-100 font-mono text-sm">✕</button>
            </div>

            <div ref={tutorRef} className="flex-1 overflow-y-auto px-6 py-5 space-y-4">
              {tutorMessages.map((msg, i) =>
                msg.role === "user" && i === 0 ? null : msg.role === "user" ? (
                  <div key={i} className="self-end ml-auto max-w-[78%] bg-[#0c1a2e] text-[#f5f1ea] px-4 py-3 rounded-2xl rounded-br-md text-[14px] leading-relaxed">
                    {msg.content}
                  </div>
                ) : (
                  <div key={i} className="max-w-[85%]">
                    <div className="flex items-center gap-2 mb-1.5 font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#a8324a]" />
                      Vitalis
                    </div>
                    <div className="text-[14px] leading-relaxed whitespace-pre-wrap">{msg.content}</div>
                  </div>
                )
              )}
              {tutorLoading && (
                <div className="flex items-center gap-1.5 opacity-60">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0s" }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.15s" }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.3s" }} />
                </div>
              )}
            </div>

            <div className="border-t border-[#0c1a2e15] px-6 py-4 flex gap-3 items-center flex-shrink-0">
              <input
                value={tutorInput}
                onChange={(e) => setTutorInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendTutorMessage(); } }}
                placeholder="Ask a follow-up..."
                className="flex-1 bg-transparent border-none outline-none text-[14px] placeholder:text-[#0c1a2e66]"
              />
              <button onClick={sendTutorMessage} disabled={tutorLoading || !tutorInput.trim()} className="bg-[#0c1a2e] text-[#f5f1ea] w-9 h-9 rounded-full flex items-center justify-center disabled:opacity-30">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                  <line x1="22" y1="2" x2="11" y2="13" />
                  <polygon points="22 2 15 22 11 13 2 9 22 2" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function PracticeSessionPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#f5f1ea]" />}>
      <PracticeSessionContent />
    </Suspense>
  );
}