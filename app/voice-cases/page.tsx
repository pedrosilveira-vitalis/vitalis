"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import Script from "next/script";

type Message = { role: "user" | "assistant"; content: string };

type CaseData = {
  patientName: string;
  patientAge: number;
  patientGender: string;
  setting: string;
  openingLine: string;
  hiddenDiagnosis: string;
  mcatConcept: string;
  mcatSection: string;
  keySymptoms: string[];
  redFlags: string[];
  patientPersonality: string;
};

type Phase = "idle" | "loading" | "interview" | "feedback-loading" | "feedback";

type SR = {
  start: () => void;
  stop: () => void;
  onresult: ((e: { results: { 0: { transcript: string } }[] }) => void) | null;
  onerror: ((e: unknown) => void) | null;
  onend: (() => void) | null;
  continuous: boolean;
  interimResults: boolean;
  lang: string;
};

type ChartType = {
  ctx: CanvasRenderingContext2D;
  scales: {
    x: { getPixelForValue: (v: number) => number };
    y: { getPixelForValue: (v: number) => number };
  };
};

type ChartLib = {
  new (canvas: HTMLCanvasElement, config: unknown): unknown;
  getChart: (canvas: HTMLCanvasElement) => ChartType | undefined;
};

declare global {
  interface Window {
    Chart: ChartLib;
    SpeechRecognition: { new (): SR };
    webkitSpeechRecognition: { new (): SR };
  }
}

export default function VoiceCasesPage() {
  const [phase, setPhase] = useState<Phase>("idle");
  const [caseData, setCaseData] = useState<CaseData | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [feedback, setFeedback] = useState("");
  const [chartReady, setChartReady] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [voiceSupported, setVoiceSupported] = useState(false);
  const [error, setError] = useState("");

  const streamRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<SR | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const SRConstructor = window.SpeechRecognition || window.webkitSpeechRecognition;
      setVoiceSupported(!!SRConstructor && "speechSynthesis" in window);
      window.speechSynthesis?.getVoices();
      if (window.speechSynthesis) {
        window.speechSynthesis.onvoiceschanged = () => {
          window.speechSynthesis.getVoices();
        };
      }
    }
  }, []);

  useEffect(() => {
    if (streamRef.current) streamRef.current.scrollTop = streamRef.current.scrollHeight;
  }, [messages, phase, feedback]);

  useEffect(() => {
    if (!chartReady || phase !== "feedback") return;
    const canvases = document.querySelectorAll<HTMLCanvasElement>(
      "canvas[data-chart]:not([data-rendered])"
    );
    canvases.forEach((canvas) => {
      try {
        const raw = decodeURIComponent(canvas.getAttribute("data-chart") || "");
        const spec = JSON.parse(raw);
        canvas.setAttribute("data-rendered", "1");
        const colors = ["#c54a2a", "#3e5641", "#d9a441", "#161410"];
        const datasets = (spec.datasets || []).map((ds: { label?: string; data: { x: number; y: number }[] }, i: number) => ({
          label: ds.label || "",
          data: ds.data || [],
          borderColor: colors[i % colors.length],
          backgroundColor: colors[i % colors.length] + "22",
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 3,
          fill: false,
        }));
        new window.Chart(canvas, {
          type: spec.type || "line",
          data: { datasets },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              title: spec.title ? { display: true, text: spec.title, font: { family: "Fraunces, serif", size: 15, weight: 500 }, color: "#161410" } : { display: false },
              legend: { display: datasets.length > 1 },
            },
            scales: {
              x: { type: "linear", title: { display: !!spec.xLabel, text: spec.xLabel || "" }, grid: { color: "#1614101a" } },
              y: { title: { display: !!spec.yLabel, text: spec.yLabel || "" }, grid: { color: "#1614101a" } },
            },
          },
        });
        if (spec.annotations?.length) {
          setTimeout(() => {
            const chart = window.Chart.getChart(canvas);
            if (!chart) return;
            const ctx = chart.ctx;
            ctx.save();
            spec.annotations.forEach((a: { x: number; y: number; label: string }) => {
              const px = chart.scales.x.getPixelForValue(a.x);
              const py = chart.scales.y.getPixelForValue(a.y);
              ctx.beginPath();
              ctx.arc(px, py, 5, 0, Math.PI * 2);
              ctx.fillStyle = "#c54a2a";
              ctx.fill();
              ctx.font = "500 11px 'Inter Tight', sans-serif";
              const m = ctx.measureText(a.label);
              const w = m.width + 12;
              let lx = px + 10;
              let ly = py - 22;
              if (lx + w > canvas.width - 8) lx = px - w - 10;
              if (ly < 4) ly = py + 12;
              ctx.fillStyle = "#f3efe7";
              ctx.fillRect(lx, ly, w, 18);
              ctx.strokeStyle = "#16141033";
              ctx.strokeRect(lx, ly, w, 18);
              ctx.fillStyle = "#161410";
              ctx.textBaseline = "middle";
              ctx.fillText(a.label, lx + 6, ly + 9);
            });
            ctx.restore();
          }, 50);
        }
      } catch (e) {
        console.error("Chart error:", e);
      }
    });
  }, [phase, feedback, chartReady]);

  function speak(text: string) {
    if (!voiceEnabled || typeof window === "undefined" || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();

    const utter = new SpeechSynthesisUtterance(text);
    const voices = window.speechSynthesis.getVoices();

    const femaleVoiceNames = ["Samantha", "Karen", "Victoria", "Allison", "Ava", "Susan", "Google US English", "Microsoft Aria"];
    const maleVoiceNames = ["Daniel", "Alex", "Tom", "Fred", "Aaron", "Google UK English Male", "Microsoft Guy"];

    const gender = caseData?.patientGender || "female";
    const preferred = gender === "male" ? maleVoiceNames : femaleVoiceNames;

    let selected = null;
    for (const name of preferred) {
      const match = voices.find((v) => v.name.includes(name));
      if (match) { selected = match; break; }
    }
    if (!selected) selected = voices.find((v) => v.lang.startsWith("en")) || voices[0];

    if (selected) utter.voice = selected;
    utter.rate = 0.95;
    utter.pitch = gender === "male" ? 0.95 : 1.05;
    window.speechSynthesis.speak(utter);
  }async function startNewCase() {
    setPhase("loading");
    setMessages([]);
    setFeedback("");
    setError("");
    try {
      const res = await fetch("/api/case/start", { method: "POST" });
      const data = await res.json();
      if (data.case) {
        setCaseData(data.case);
        const opener: Message = { role: "assistant", content: data.case.openingLine };
        setMessages([opener]);
        setPhase("interview");
        speak(data.case.openingLine);
      } else {
        setError("Couldn't generate a case. Try again?");
        setPhase("idle");
      }
    } catch {
      setError("Connection issue. Try again?");
      setPhase("idle");
    }
  }

  async function sendMessage(text: string) {
    if (!caseData || !text.trim()) return;
    const userMsg: Message = { role: "user", content: text.trim() };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");
    try {
      const res = await fetch("/api/case/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ caseContext: caseData, messages: newMessages }),
      });
      const data = await res.json();
      if (data.reply) {
        setMessages([...newMessages, { role: "assistant", content: data.reply }]);
        speak(data.reply);
      } else {
        setMessages([...newMessages, { role: "assistant", content: "(Patient looks confused.)" }]);
      }
    } catch {
      setMessages([...newMessages, { role: "assistant", content: "(Connection issue.)" }]);
    }
  }

  async function endInterview() {
    if (!caseData) return;
    setPhase("feedback-loading");
    const transcript = messages
      .map((m) => (m.role === "user" ? `Student: ${m.content}` : `${caseData.patientName}: ${m.content}`))
      .join("\n");
    try {
      const res = await fetch("/api/case/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ caseContext: caseData, transcript }),
      });
      const data = await res.json();
      setFeedback(data.feedback || "Feedback unavailable.");
      setPhase("feedback");
    } catch {
      setFeedback("Couldn't generate feedback. Try again?");
      setPhase("feedback");
    }
  }

  function toggleListening() {
    if (!voiceSupported) return;
    if (isListening) {
      recognitionRef.current?.stop();
      return;
    }
    const SRConstructor = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SRConstructor();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";
    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      setInput(transcript);
      setTimeout(() => sendMessage(transcript), 100);
    };
    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);
    recognitionRef.current = recognition;
    recognition.start();
    setIsListening(true);
  }

  function resetCase() {
    window.speechSynthesis?.cancel();
    setPhase("idle");
    setCaseData(null);
    setMessages([]);
    setFeedback("");
    setError("");
  }

  function formatFeedback(text: string): string {
    const chartBlocks: string[] = [];
    text = text.replace(/```chart\s*([\s\S]*?)```/g, (_m, raw) => {
      chartBlocks.push(raw.trim());
      return "\x00CHART" + (chartBlocks.length - 1) + "\x00";
    });
    let html = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*([^*]+)\*/g, "<em>$1</em>")
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/^### (.+)$/gm, "<h3>$1</h3>");
    const lines = html.split("\n");
    let out = "";
    let inList = false;
    for (const line of lines) {
      const li = line.match(/^[-*]\s+(.+)/);
      const cp = line.match(/\x00CHART(\d+)\x00/);
      if (cp) {
        if (inList) { out += "</ul>"; inList = false; }
        const id = "c" + Date.now() + Math.random().toString(36).slice(2, 6);
        out += `<div class="chart-wrap"><canvas id="${id}" data-chart="${encodeURIComponent(chartBlocks[parseInt(cp[1], 10)])}"></canvas></div>`;
      } else if (li) {
        if (!inList) { out += "<ul>"; inList = true; }
        out += "<li>" + li[1] + "</li>";
      } else {
        if (inList) { out += "</ul>"; inList = false; }
        if (line.trim()) {
          if (line.startsWith("<h3>")) out += line;
          else out += "<p>" + line + "</p>";
        }
      }
    }
    if (inList) out += "</ul>";
    return out;
  }return (
    <>
      <Script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js" onLoad={() => setChartReady(true)} />
      <div className="min-h-screen flex flex-col bg-[#f3efe7] text-[#161410]">
        <header className="flex items-center justify-between px-8 py-4 border-b border-[#16141015]">
          <div className="flex items-center gap-3">
            <span className="w-2.5 h-2.5 rounded-full bg-[#c54a2a] shadow-[0_0_0_4px_#c54a2a22]" />
            <span className="font-serif font-semibold text-xl tracking-tight">Vitalis</span>
          </div>
          <div className="hidden md:flex gap-7 text-sm font-medium">
            <Link href="/" className="opacity-60 hover:opacity-100">Home</Link>
            <Link href="/tutor" className="opacity-60 hover:opacity-100">Tutor</Link>
            <Link href="/practice" className="opacity-60 hover:opacity-100">Practice</Link>
            <Link href="/voice-cases" className="opacity-100 border-b border-[#c54a2a] pb-0.5">Voice Cases</Link>
          </div>
          <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">Patient Sim · Beta</div>
        </header>

        {phase === "idle" && (
          <div className="flex-1 flex items-center justify-center px-8 py-12">
            <div className="max-w-xl text-center">
              <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4">Mode 02 · Voice clinical cases</div>
              <h1 className="font-serif text-4xl md:text-5xl font-light italic tracking-tight leading-tight mb-5">
                Talk through a case <span className="text-[#c54a2a] not-italic font-medium">out loud.</span>
              </h1>
              <p className="text-[15px] opacity-70 leading-relaxed mb-8">
                Interview a simulated patient. Ask them about symptoms, history, anything you&apos;d want to know. When you&apos;re done, get feedback on your clinical thinking AND the underlying MCAT science.
              </p>
              {error && <p className="text-[#c54a2a] text-sm mb-4">{error}</p>}
              <button
                onClick={startNewCase}
                className="font-mono text-xs uppercase tracking-[0.08em] bg-[#161410] text-[#f3efe7] px-6 py-3.5 rounded-full hover:bg-[#2a2620] transition-colors"
              >
                Start a new case →
              </button>
              {!voiceSupported && (
                <p className="font-mono text-[10px] uppercase tracking-[0.1em] opacity-50 mt-6">
                  Voice not supported in this browser — text mode only
                </p>
              )}
            </div>
          </div>
        )}

        {phase === "loading" && (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <div className="flex items-center justify-center gap-2 mb-3">
                <span className="w-2 h-2 rounded-full bg-[#161410] animate-bounce" />
                <span className="w-2 h-2 rounded-full bg-[#161410] animate-bounce" style={{ animationDelay: "0.15s" }} />
                <span className="w-2 h-2 rounded-full bg-[#161410] animate-bounce" style={{ animationDelay: "0.3s" }} />
              </div>
              <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Generating case...</div>
            </div>
          </div>
        )}

        {phase === "interview" && caseData && (
          <div className="flex-1 flex flex-col bg-[#ebe5d6] overflow-hidden">
            <div className="px-8 py-3 border-b border-[#16141015] flex items-center justify-between flex-wrap gap-2">
              <div className="flex items-center gap-3">
                <span className="w-2 h-2 rounded-full bg-[#3e5641] animate-pulse" />
                <div>
                  <div className="font-serif text-base font-medium leading-tight">{caseData.patientName}, {caseData.patientAge}</div>
                  <div className="font-mono text-[10px] uppercase tracking-[0.12em] opacity-55">{caseData.setting}</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setVoiceEnabled(!voiceEnabled)}
                  className="font-mono text-[10px] uppercase tracking-[0.1em] opacity-60 hover:opacity-100 transition-opacity px-2 py-1 border border-[#16141025] rounded"
                >
                  {voiceEnabled ? "Voice on" : "Voice off"}
                </button>
                <button
                  onClick={endInterview}
                  className="font-mono text-[10px] uppercase tracking-[0.1em] bg-[#161410] text-[#f3efe7] px-3 py-1.5 rounded-full hover:bg-[#2a2620]"
                >
                  End and Get Feedback
                </button>
              </div>
            </div>

            <div ref={streamRef} className="flex-1 overflow-y-auto px-8 py-7 flex flex-col gap-4">
              {messages.map((msg, i) =>
                msg.role === "user" ? (
                  <div key={i} className="self-end max-w-[78%] bg-[#161410] text-[#f3efe7] px-4 py-3 rounded-2xl rounded-br-md text-[15px] leading-relaxed">
                    {msg.content}
                  </div>
                ) : (
                  <div key={i} className="self-start max-w-[85%]">
                    <div className="flex items-center gap-2 mb-1.5 font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#c54a2a]" />
                      {caseData.patientName}
                    </div>
                    <div className="text-[15px] leading-relaxed italic text-[#161410cc]">&quot;{msg.content}&quot;</div>
                  </div>
                )
              )}
            </div>

            <div className="border-t border-[#16141015] px-8 py-4 flex gap-3 items-center bg-[#ebe5d6]">
              {voiceSupported && (
                <button
                  onClick={toggleListening}
                  className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                    isListening ? "bg-[#c54a2a] text-[#f3efe7] animate-pulse" : "bg-[#1614101a] text-[#161410] hover:bg-[#1614102a]"
                  }`}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                    <line x1="12" y1="19" x2="12" y2="23" />
                  </svg>
                </button>
              )}
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage(input);
                  }
                }}
                placeholder={isListening ? "Listening..." : `Talk to ${caseData.patientName}...`}
                className="flex-1 bg-transparent border-none outline-none text-[15px] placeholder:text-[#16141066]"
              />
              <button
                onClick={() => sendMessage(input)}
                disabled={!input.trim()}
                className="bg-[#161410] text-[#f3efe7] w-10 h-10 rounded-full flex items-center justify-center disabled:opacity-30"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                  <line x1="22" y1="2" x2="11" y2="13" />
                  <polygon points="22 2 15 22 11 13 2 9 22 2" />
                </svg>
              </button>
            </div>
          </div>
        )}

        {phase === "feedback-loading" && (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <div className="flex items-center justify-center gap-2 mb-3">
                <span className="w-2 h-2 rounded-full bg-[#161410] animate-bounce" />
                <span className="w-2 h-2 rounded-full bg-[#161410] animate-bounce" style={{ animationDelay: "0.15s" }} />
                <span className="w-2 h-2 rounded-full bg-[#161410] animate-bounce" style={{ animationDelay: "0.3s" }} />
              </div>
              <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Vitalis is reviewing your interview...</div>
            </div>
          </div>
        )}

        {phase === "feedback" && (
          <div className="flex-1 overflow-y-auto px-8 py-10">
            <div className="max-w-2xl mx-auto">
              <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-3">Session feedback</div>
              <h2 className="font-serif text-3xl font-medium tracking-tight mb-6">Here&apos;s what happened.</h2>
              <div className="feedback-content text-[15px] leading-relaxed" dangerouslySetInnerHTML={{ __html: formatFeedback(feedback) }} />
              <div className="mt-10 flex gap-3">
                <button
                  onClick={startNewCase}
                  className="font-mono text-xs uppercase tracking-[0.08em] bg-[#161410] text-[#f3efe7] px-5 py-3 rounded-full hover:bg-[#2a2620]"
                >
                  New case
                </button>
                <button
                  onClick={resetCase}
                  className="font-mono text-xs uppercase tracking-[0.08em] border border-[#16141025] px-5 py-3 rounded-full hover:bg-[#1614100a]"
                >
                  Back to start
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      <style jsx global>{`
        .feedback-content p { margin-bottom: 12px; }
        .feedback-content strong { font-weight: 600; }
        .feedback-content em { font-style: italic; }
        .feedback-content ul { margin: 12px 0; padding-left: 24px; }
        .feedback-content li { margin-bottom: 6px; }
        .feedback-content code { background: #16141014; padding: 2px 6px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 13px; }
        .feedback-content h3 { font-family: 'Fraunces', serif; font-size: 22px; font-weight: 500; margin: 24px 0 10px; color: #161410; }
        .feedback-content .chart-wrap { margin: 18px 0; padding: 18px; background: #16141008; border: 1px solid #16141015; border-radius: 10px; height: 300px; position: relative; }
      `}</style>
    </>
  );
}