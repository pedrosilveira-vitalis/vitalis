"use client";

import { useEffect, useState, useRef, useCallback, Suspense } from "react";
import Link from "next/link";
import { useParams, useSearchParams, useRouter } from "next/navigation";
import { useActivity } from "@/components/ActivityProvider";
import Nori from "@/components/Nori";
import MainNav from "@/components/MainNav";

import { flagged,toggleFlag } from "@/lib/flagged";
import type { Question } from "@/lib/practice";
import { fetchJson } from "@/lib/fetch-json";

const historyKey = "vitalis.practice.seen.v1";
let memoryHistory: string[] = [];

function readHistory(): string[] {
  try {
    const saved = JSON.parse(localStorage.getItem(historyKey) || "[]");
    if (Array.isArray(saved)) return [...new Set([...saved.filter(id => typeof id === "string"), ...memoryHistory])].slice(-10000);
  } catch { /* Keep session history when browser storage is unavailable. */ }
  return memoryHistory;
}

type Message = { role: "user" | "assistant"; content: string };

const SECTION_NAMES: Record<string, string> = {
  "bio-biochem": "Bio / Biochem",
  "chem-phys": "Chem / Phys",
  "psych-soc": "Psych / Soc",
  "cars": "CARS",
  "mixed": "Mixed",
};

const SECTION_COLORS: Record<string, string> = {
  "bio-biochem": "#245574",
  "chem-phys": "#245574",
  "psych-soc": "#245574",
  "cars": "#245574",
  "mixed": "#0c1a2e",
};

function PracticeSessionContent() {
  const activity = useActivity();
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const requestRef = useRef<AbortController | null>(null);
  const [generation, setGeneration] = useState(0);
  const sectionId = (params.section as string) || "mixed";
  const requestedCount = Number(searchParams.get("n") || "10");
  const numQuestions = Number.isInteger(requestedCount) && requestedCount >= 1 && requestedCount <= 20 ? requestedCount : 10;
  const format = searchParams.get("f") || "standalone";
  const difficulty = (searchParams.get("d") as "mixed" | "easy" | "medium" | "hard") || "mixed";

  const [exhausted, setExhausted] = useState(false);
  const [blend, setBlend] = useState(false);
  const [isFlagged,setIsFlagged]=useState(false);
  const [flagMessage,setFlagMessage]=useState("");
  const [starter, setStarter] = useState(false);
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

  const loadQuestions = useCallback(async (review = false, custom = false) => {
    requestRef.current?.abort();
    const controller = new AbortController();
    requestRef.current = controller;
    setLoading(true);
    setError("");
    setExhausted(false);
    setQuestions([]);
    setCurrentIdx(0); setResults([]); setSessionComplete(false); setSelectedAnswer(null); setShowExplanation(false); setShowTutor(false); setTutorMessages([]);
    try {
      const data = await fetchJson("/api/practice/generate", {
        signal: controller.signal,
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ section: sectionId, count: numQuestions, difficulty, format, custom, seen: review ? [] : readHistory() }),
      });
      if (controller.signal.aborted) return;
      if (data.exhausted) { setExhausted(true); setLoading(false); return; }
      if (!data.questions || data.questions.length === 0) {
        setError("Couldn't load questions. Try again.");
        setLoading(false);
        return;
      }
      setBlend(data.source === "blend" || (data.source === "generated" && data.questions.length < numQuestions));
      setStarter(data.source === "bank");
      memoryHistory = [...new Set([...readHistory(), ...data.questions.map((q: Question)=>q.id)])].slice(-10000);
      try {localStorage.setItem(historyKey,JSON.stringify(memoryHistory));} catch { /* Keep this tab’s history. */ }
      setQuestions(data.questions);
      setLoading(false);
    } catch (error) {
      if (controller.signal.aborted) return;
      setError(error instanceof Error ? error.message : "Couldn't load questions. Try again.");
      setLoading(false);
    }
  }, [sectionId, numQuestions, difficulty, format]);

  useEffect(() => {
    loadQuestions();
    return () => requestRef.current?.abort();
  }, [loadQuestions, generation]);

  useEffect(() => {
    if (tutorRef.current) {
      tutorRef.current.scrollTop = tutorRef.current.scrollHeight;
    }
  }, [tutorMessages, tutorLoading]);

  const currentQ = questions[currentIdx];

  useEffect(() => {
    if (loading || !currentQ) return;
    setFlagMessage("");
    try { setIsFlagged(flagged(currentQ.id)); } catch { setIsFlagged(false); }
  }, [loading, currentQ]);

  function handleSubmit() {
    if (!selectedAnswer || !currentQ || showExplanation) return;
    const isCorrect = selectedAnswer === currentQ.correct_answer;
    activity.record(currentQ.activityToken, selectedAnswer);
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
    if (!currentQ || !results.length) return;
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
    const initialUserMsg = `Help me understand the reasoning behind this question.

Question: ${currentQ.question_text}

I picked: ${lastResult.selected}. ${wrongAnswerText}
Correct: ${currentQ.correct_answer}. ${correctText}

The explanation says: ${currentQ.explanation}

Can you explain this more deeply and help me build the right intuition so I get questions like this right next time?`;

    setTutorMessages([{ role: "user", content: initialUserMsg }]);
    setTutorLoading(true);
    fetchJson("/api/practice/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: currentQ, studentAnswer: lastResult.selected, messages: [{ role: "user", content: initialUserMsg }] }),
    })
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
      const data = await fetchJson("/api/practice/explain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: currentQ, studentAnswer: selectedAnswer, messages: newMessages }),
      });
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
          <div className="font-sans text-[11px] uppercase tracking-[0.12em] opacity-60">Preparing {numQuestions} {sectionName} questions...</div>
          <p className="mt-4 text-sm opacity-70">Preparing your questions and explanations. This may take up to 90 seconds.</p>
          <Link href="/practice" className="inline-block mt-5 underline">Cancel and go back</Link>
        </div>
      </div>
    );
  }

  if (exhausted) return (
    <main className="min-h-screen bg-[#f5f1ea] flex flex-col items-center justify-center gap-5 p-8 text-center">
      <h1 className="font-sans text-3xl">You’ve seen every question currently available for these settings.</h1>
      <Link href="/practice" className="underline">Choose another section or difficulty</Link>
      {!["guide","drills"].includes(format) && <button onClick={()=>loadQuestions(false,true)} className="underline">Try generating new questions with the AI tutor</button>}
      <button onClick={() => loadQuestions(true)} className="rounded-full bg-[#0c1a2e] text-white px-5 py-3">Start a review session</button>
    </main>
  );

  if (error) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] flex items-center justify-center p-10">
        <div className="text-center max-w-md">
          <div className="font-sans text-[11px] tracking-[0.18em] uppercase opacity-50 mb-4">Error</div>
          <h1 className="font-sans text-3xl font-medium mb-4">{error}</h1>
          <div className="flex gap-3 justify-center">
            <button onClick={() => loadQuestions()} className="font-sans text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full">
              Try again
            </button>
            <Link href="/practice" className="font-sans text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full">
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
          <div className="session-achievement"><Nori/><span aria-hidden="true">✦</span></div>
          <div className="font-sans text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4">Session complete</div>
          <h2 className="text-2xl font-semibold mb-3">You made time to learn.</h2>
          <p className="text-sm mb-6 opacity-75">Review what surprised you, or take a well-earned break.</p>
          <h1 className="font-sans text-[clamp(48px,6vw,88px)] font-medium tracking-tight mb-2">
            <span style={{ color: accent }}>{correctCount}</span> / {results.length}
          </h1>
          <p className="font-sans text-[14px] tracking-[0.1em] uppercase opacity-65 mb-10">{pct}% correct</p>
          <div className="flex gap-3 justify-center flex-wrap">
            <button onClick={() => setGeneration(generation + 1)} className="font-sans text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]">
              New session →
            </button>
            <Link href="/practice" className="font-sans text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a]">
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
        <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-60 mb-3 flex items-center gap-2">
          <Link href="/practice" className="hover:opacity-100 opacity-70">Practice</Link>
          <span className="opacity-40">/</span>
          <span style={{ color: accent }}>{sectionName}</span>
          <span className="opacity-40">·</span>
          <span>{currentQ.topic}</span>
        </div>

        {blend && <p className="mb-4 text-sm">Practice set · {questions.length} of {numQuestions} requested.</p>}
        {starter && <p role="status" className="mb-4 text-sm">Question bank · {questions.length} of {numQuestions} requested.</p>}
        <div className="mb-7 flex items-center gap-3">
          <div className="practice-progress flex-1" role="progressbar" aria-label="Questions answered" aria-valuemin={0} aria-valuemax={questions.length} aria-valuenow={currentIdx + (showExplanation ? 1 : 0)}>
            <div className="h-full transition-all" style={{ width: `${((currentIdx + (showExplanation ? 1 : 0)) / questions.length) * 100}%`, backgroundColor: accent }} />
          </div>
          <div className="font-sans text-[10px] tracking-[0.1em] uppercase opacity-55 flex-shrink-0">
            {currentIdx + 1} / {questions.length}
          </div>
        </div>

        <div className="mb-5 flex items-center gap-4"><button className="border rounded-full px-4 py-2 text-sm" aria-pressed={isFlagged} onClick={()=>{try{setIsFlagged(toggleFlag(currentQ));}catch{setFlagMessage("Could not save. Check browser storage permissions or space.");}}}>{isFlagged ? "Flagged ✓" : "Flag for later"}</button><Link href="/flagged" className="text-sm underline">View flagged questions</Link><span role="status">{flagMessage}</span></div>
        {currentQ.passage && <article className="mb-8 rounded-2xl border border-[#0c1a2e20] bg-white/60 p-6" aria-label="Passage"><p className="text-xs uppercase tracking-widest text-[#245574] mb-3">Read the passage</p><h2 className="font-sans text-2xl mb-4">{currentQ.passage.title}</h2><div className="whitespace-pre-wrap text-base leading-8">{currentQ.passage.content}</div></article>}
        <h1 className="font-sans text-[clamp(22px,2.6vw,30px)] font-medium leading-snug mb-7">
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
              else if (isSel && !isAns) { cls = "border-[#245574]"; bg = "bg-[#24557415]"; }
            } else if (isSel) { cls = "border-[#0c1a2e]"; bg = "bg-[#0c1a2e0a]"; }
            return (
              <button
                key={letter}
                onClick={() => !showExplanation && setSelectedAnswer(letter)}
                disabled={showExplanation}
                className={`w-full text-left p-4 rounded-xl border-2 transition-all ${cls} ${bg} ${!showExplanation ? "hover:border-[#0c1a2e] hover:bg-[#0c1a2e0a] cursor-pointer" : "cursor-default"}`}
              >
                <div className="flex gap-3">
                  <span className="font-sans font-semibold w-6 flex-shrink-0">{letter}</span>
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
              className="font-sans text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a] disabled:opacity-30 disabled:cursor-not-allowed"
            >
              Submit →
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {activity.error && <p className="portal-error" role="alert">{activity.error} <button onClick={activity.retry}>Retry saving streak</button></p>}
            {activity.data?.streak.completedToday && <p className="portal-success" role="status">Today’s practice is saved. Your streak is {activity.data.streak.current} day{activity.data.streak.current===1?"":"s"}.</p>}
            <div className={`answer-feedback p-5 rounded-xl border ${isCorrect ? "border-[#3e6b4a] bg-[#3e6b4a08]" : "border-[#245574] bg-[#24557408]"}`}>
              <div className="font-sans text-[10px] tracking-[0.14em] uppercase opacity-60 mb-2">
                {isCorrect ? "✓ Correct — nicely reasoned" : "Not quite — let’s work through it"}
              </div>
              <div className="text-[14px] leading-relaxed">{currentQ.explanation}</div>
              {selectedAnswer && !isCorrect && currentQ.wrongAnswerExplanations[selectedAnswer] && <p className="mt-3 text-sm leading-relaxed"><strong>Why your choice was incorrect: </strong>{currentQ.wrongAnswerExplanations[selectedAnswer]}</p>}
            </div>

            <div className="flex justify-between items-center flex-wrap gap-3">
              {!showTutor && (
                <button
                  onClick={openTutor}
                  className="font-sans text-xs uppercase tracking-[0.08em] border-2 border-[#245574] text-[#245574] px-5 py-3 rounded-full hover:bg-[#245574] hover:text-[#f5f1ea] transition-all"
                >
                  Ask the tutor →
                </button>
              )}
              <div className="ml-auto">
                <button
                  onClick={handleNext}
                  className="font-sans text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]"
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
                <span className="w-2 h-2 rounded-full bg-[#245574] animate-pulse" />
                <div className="font-sans text-lg font-medium">Tutor · helping you</div>
              </div>
              <button onClick={() => setShowTutor(false)} className="opacity-50 hover:opacity-100 font-sans text-sm">✕</button>
            </div>

            <div ref={tutorRef} className="flex-1 overflow-y-auto px-6 py-5 space-y-4">
              {tutorMessages.map((msg, i) =>
                msg.role === "user" && i === 0 ? null : msg.role === "user" ? (
                  <div key={i} className="self-end ml-auto max-w-[78%] bg-[#0c1a2e] text-[#f5f1ea] px-4 py-3 rounded-2xl rounded-br-md text-[14px] leading-relaxed">
                    {msg.content}
                  </div>
                ) : (
                  <div key={i} className="max-w-[85%]">
                    <div className="flex items-center gap-2 mb-1.5 font-sans text-[10px] tracking-[0.14em] uppercase opacity-55">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#245574]" />
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