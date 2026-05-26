"use client";

import { useState, useRef, useEffect, useCallback, Suspense } from "react";
import Link from "next/link";
import Script from "next/script";
import { useSearchParams, useRouter } from "next/navigation";

type ImagePart = {
  type: "image";
  source: { type: "base64"; media_type: string; data: string };
};
type TextPart = { type: "text"; text: string };

type DisplayMessage = {
  role: "user" | "assistant";
  text: string;
  images?: string[];
};

type ApiMessage = {
  role: "user" | "assistant";
  content: string | Array<TextPart | ImagePart>;
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
  }
}

function Logo() {
  return (
    <div className="flex items-center gap-2.5">
      <svg width="32" height="18" viewBox="0 0 60 28" fill="none" className="flex-shrink-0">
        <path
          d="M2 14 L12 14 L16 6 L22 22 L28 4 L34 18 L38 14 L48 14"
          stroke="#a8324a"
          strokeWidth="2.4"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        <circle cx="50" cy="14" r="2.2" fill="#a8324a" />
      </svg>
      <span className="font-serif font-semibold text-xl tracking-tight text-[#0c1a2e]">Vitalis</span>
    </div>
  );
}

function TutorPageContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const conversationIdParam = searchParams.get("c");

  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [input, setInput] = useState("");
  const [pendingImages, setPendingImages] = useState<{ dataUrl: string; mediaType: string; base64: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [chartReady, setChartReady] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [conversationLoading, setConversationLoading] = useState(false);
  const streamRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch("/api/conversations", { method: "GET" })
      .then((r) => setIsAuthenticated(r.status !== 401))
      .catch(() => setIsAuthenticated(false));
  }, []);

  const loadConversation = useCallback(async (id: number) => {
    setConversationLoading(true);
    try {
      const res = await fetch(`/api/conversations/${id}`);
      if (res.ok) {
        const data = await res.json();
        const loaded: DisplayMessage[] = (data.messages || []).map(
          (m: { role: string; content: string }) => ({
            role: m.role as "user" | "assistant",
            text: m.content,
          })
        );
        setMessages(loaded);
        setConversationId(id);
      } else {
        setMessages([]);
        setConversationId(null);
      }
    } catch (e) {
      console.error("Failed to load conversation:", e);
    }
    setConversationLoading(false);
  }, []);

  useEffect(() => {
    if (conversationIdParam) {
      const id = parseInt(conversationIdParam, 10);
      if (!isNaN(id)) loadConversation(id);
    }
  }, [conversationIdParam, loadConversation]);

  useEffect(() => {
    if (streamRef.current) {
      streamRef.current.scrollTop = streamRef.current.scrollHeight;
    }
  }, [messages, loading]);

  useEffect(() => {
    if (!chartReady || !streamRef.current) return;
    const canvases = streamRef.current.querySelectorAll<HTMLCanvasElement>(
      "canvas[data-chart]:not([data-rendered])"
    );
    canvases.forEach((canvas) => {
      try {
        const raw = decodeURIComponent(canvas.getAttribute("data-chart") || "");
        const spec = JSON.parse(raw);
        canvas.setAttribute("data-rendered", "1");
        const colors = ["#a8324a", "#0c1a2e", "#8a6b2e", "#4a3b6b"];
        const datasets = (spec.datasets || []).map((ds: { label?: string; data: { x: number; y: number }[] }, i: number) => ({
          label: ds.label || "",
          data: ds.data || [],
          borderColor: colors[i % colors.length],
          backgroundColor: colors[i % colors.length] + "22",
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 3,
          pointHoverRadius: 5,
          fill: false,
        }));
        new window.Chart(canvas, {
          type: spec.type || "line",
          data: { datasets },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              title: spec.title ? { display: true, text: spec.title, font: { family: "Fraunces, serif", size: 15, weight: 500 }, color: "#0c1a2e", padding: { bottom: 12 } } : { display: false },
              legend: { display: datasets.length > 1, labels: { font: { family: "Inter Tight, sans-serif", size: 12 }, color: "#0c1a2e" } },
            },
            scales: {
              x: { type: "linear", title: { display: !!spec.xLabel, text: spec.xLabel || "", font: { family: "Inter Tight, sans-serif", size: 12, weight: 500 }, color: "#0c1a2eaa" }, grid: { color: "#0c1a2e1a" }, ticks: { color: "#0c1a2eaa", font: { family: "Inter Tight, sans-serif", size: 11 } } },
              y: { title: { display: !!spec.yLabel, text: spec.yLabel || "", font: { family: "Inter Tight, sans-serif", size: 12, weight: 500 }, color: "#0c1a2eaa" }, grid: { color: "#0c1a2e1a" }, ticks: { color: "#0c1a2eaa", font: { family: "Inter Tight, sans-serif", size: 11 } } },
            },
          },
        });
        if (spec.annotations && spec.annotations.length) {
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
              ctx.fillStyle = "#a8324a";
              ctx.fill();
              ctx.lineWidth = 2;
              ctx.strokeStyle = "#f5f1ea";
              ctx.stroke();
              ctx.font = "500 11px 'Inter Tight', sans-serif";
              const m = ctx.measureText(a.label);
              const boxW = m.width + 12;
              let lx = px + 10;
              let ly = py - 22;
              if (lx + boxW > canvas.width - 8) lx = px - boxW - 10;
              if (ly < 4) ly = py + 12;
              ctx.fillStyle = "#f5f1ea";
              ctx.fillRect(lx, ly, boxW, 18);
              ctx.strokeStyle = "#0c1a2e33";
              ctx.strokeRect(lx, ly, boxW, 18);
              ctx.fillStyle = "#0c1a2e";
              ctx.textBaseline = "middle";
              ctx.fillText(a.label, lx + 6, ly + 9);
            });
            ctx.restore();
          }, 50);
        }
      } catch (e) {
        console.error("Chart render error:", e);
      }
    });
  }, [messages, chartReady]);

  function handleFileSelect(e: React.ChangeEvent<HTMLInputElement>) {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    Array.from(files).forEach((file) => {
      if (file.size > 5 * 1024 * 1024) {
        alert(`${file.name} is larger than 5MB. Try a smaller image.`);
        return;
      }
      if (!file.type.startsWith("image/")) {
        alert(`${file.name} is not an image.`);
        return;
      }
      const reader = new FileReader();
      reader.onload = (ev) => {
        const dataUrl = ev.target?.result as string;
        if (!dataUrl) return;
        const base64 = dataUrl.split(",")[1] || "";
        setPendingImages((prev) => [...prev, { dataUrl, mediaType: file.type, base64 }]);
      };
      reader.readAsDataURL(file);
    });

    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  function removePendingImage(index: number) {
    setPendingImages((prev) => prev.filter((_, i) => i !== index));
  }

  async function ensureConversation(): Promise<number | null> {
    if (conversationId) return conversationId;
    if (!isAuthenticated) return null;
    try {
      const res = await fetch("/api/conversations", { method: "POST" });
      if (res.ok) {
        const data = await res.json();
        const newId = data.conversation.id;
        setConversationId(newId);
        router.replace(`/tutor?c=${newId}`);
        return newId;
      }
    } catch (e) {
      console.error("Failed to create conversation:", e);
    }
    return null;
  }

  async function saveMessage(convId: number, role: "user" | "assistant", content: string) {
    try {
      await fetch(`/api/conversations/${convId}/messages`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role, content }),
      });
    } catch (e) {
      console.error("Failed to save message:", e);
    }
  }

  async function send() {
    if (loading) return;
    const hasText = input.trim().length > 0;
    const hasImages = pendingImages.length > 0;
    if (!hasText && !hasImages) return;

    const textContent = input.trim();
    const imagesForDisplay = pendingImages.map((p) => p.dataUrl);
    const imagesForApi: ImagePart[] = pendingImages.map((p) => ({
      type: "image",
      source: { type: "base64", media_type: p.mediaType, data: p.base64 },
    }));

    const displayMsg: DisplayMessage = {
      role: "user",
      text: textContent,
      images: imagesForDisplay.length > 0 ? imagesForDisplay : undefined,
    };
    const newDisplayMessages = [...messages, displayMsg];
    setMessages(newDisplayMessages);
    setInput("");
    setPendingImages([]);
    setLoading(true);

    const apiMessages: ApiMessage[] = newDisplayMessages.map((m) => ({
      role: m.role,
      content: m.text,
    }));

    if (imagesForApi.length > 0) {
      const lastIdx = apiMessages.length - 1;
      const parts: Array<TextPart | ImagePart> = [...imagesForApi];
      if (textContent) parts.push({ type: "text", text: textContent });
      else parts.push({ type: "text", text: "What's in this image?" });
      apiMessages[lastIdx] = { role: "user", content: parts };
    }

    const convId = await ensureConversation();
    if (convId) {
      const saved = textContent || (hasImages ? "[Sent image]" : "");
      if (saved) await saveMessage(convId, "user", saved);
    }

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: apiMessages }),
      });
      const data = await res.json();
      const reply = data.reply || "Sorry — I had trouble responding. Try again?";
      setMessages([...newDisplayMessages, { role: "assistant", text: reply }]);
      if (convId) await saveMessage(convId, "assistant", reply);
    } catch {
      setMessages([...newDisplayMessages, { role: "assistant", text: "Sorry — connection issue. Try again?" }]);
    }
    setLoading(false);
  }

  async function askExample(text: string) {
    if (loading) return;
    const displayMsg: DisplayMessage = { role: "user", text };
    const newMessages = [...messages, displayMsg];
    setMessages(newMessages);
    setLoading(true);

    const convId = await ensureConversation();
    if (convId) await saveMessage(convId, "user", text);

    const apiMessages: ApiMessage[] = newMessages.map((m) => ({
      role: m.role,
      content: m.text,
    }));

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: apiMessages }),
      });
      const data = await res.json();
      const reply = data.reply || "Sorry — I had trouble responding. Try again?";
      setMessages([...newMessages, { role: "assistant", text: reply }]);
      if (convId) await saveMessage(convId, "assistant", reply);
    } catch {
      setMessages([...newMessages, { role: "assistant", text: "Sorry — connection issue. Try again?" }]);
    }
    setLoading(false);
  }

  function startFresh() {
    setMessages([]);
    setConversationId(null);
    setPendingImages([]);
    router.replace("/tutor");
  }

  function sanitizeSVG(svg: string): string {
    if (typeof window === "undefined") return "";
    const tmp = document.createElement("div");
    tmp.innerHTML = svg;
    const svgEl = tmp.querySelector("svg");
    if (!svgEl) return "";
    const allowed = new Set(["svg","g","path","rect","circle","ellipse","line","polyline","polygon","text","tspan","defs","marker","linearGradient","radialGradient","stop","title","desc"]);
    const walk = (node: Element) => {
      if (!allowed.has(node.tagName.toLowerCase())) { node.remove(); return; }
      Array.from(node.attributes).forEach((attr) => {
        if (/^on/i.test(attr.name)) node.removeAttribute(attr.name);
        if (/script/i.test(attr.value)) node.removeAttribute(attr.name);
      });
      Array.from(node.children).forEach(walk);
    };
    walk(svgEl);
    return svgEl.outerHTML;
  }

  function formatBody(text: string): string {
    const chartBlocks: string[] = [];
    text = text.replace(/```chart\s*([\s\S]*?)```/g, (_m, raw) => {
      chartBlocks.push(raw.trim());
      return "\x00CHART" + (chartBlocks.length - 1) + "\x00";
    });
    const svgBlocks: string[] = [];
    text = text.replace(/```svg\s*([\s\S]*?)```/g, (_m, svg) => {
      svgBlocks.push(sanitizeSVG(svg.trim()));
      return "\x00SVG" + (svgBlocks.length - 1) + "\x00";
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
    let listType = "";
    for (const line of lines) {
      const ulMatch = line.match(/^[-*]\s+(.+)/);
      const olMatch = line.match(/^\d+\.\s+(.+)/);
      const svgPlaceholder = line.match(/\x00SVG(\d+)\x00/);
      const chartPlaceholder = line.match(/\x00CHART(\d+)\x00/);
      if (chartPlaceholder) {
        if (inList) { out += "</" + listType + ">"; inList = false; }
        const id = "chart-" + Date.now() + "-" + Math.random().toString(36).slice(2, 8);
        const dataAttr = encodeURIComponent(chartBlocks[parseInt(chartPlaceholder[1], 10)]);
        out += `<div class="chart-wrap"><canvas id="${id}" data-chart="${dataAttr}"></canvas></div>`;
      } else if (svgPlaceholder) {
        if (inList) { out += "</" + listType + ">"; inList = false; }
        out += `<div class="diagram">${svgBlocks[parseInt(svgPlaceholder[1], 10)]}</div>`;
      } else if (ulMatch) {
        if (!inList || listType !== "ul") { if (inList) out += "</" + listType + ">"; out += "<ul>"; inList = true; listType = "ul"; }
        out += "<li>" + ulMatch[1] + "</li>";
      } else if (olMatch) {
        if (!inList || listType !== "ol") { if (inList) out += "</" + listType + ">"; out += "<ol>"; inList = true; listType = "ol"; }
        out += "<li>" + olMatch[1] + "</li>";
      } else {
        if (inList) { out += "</" + listType + ">"; inList = false; }
        if (line.trim()) {
          if (line.startsWith("<h3>")) out += line;
          else out += "<p>" + line + "</p>";
        }
      }
    }
    if (inList) out += "</" + listType + ">";
    return out;
  }

  return (
    <>
      <Script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js" onLoad={() => setChartReady(true)} />
      <div className="h-screen flex flex-col bg-[#f5f1ea] text-[#0c1a2e]">
        <header className="flex items-center justify-between px-8 py-4 border-b border-[#0c1a2e15]">
          <Logo />
          <div className="hidden md:flex gap-6 text-sm font-medium">
            <Link href="/" className="opacity-60 hover:opacity-100">Home</Link>
            <Link href="/tutor" className="opacity-100 border-b border-[#a8324a] pb-0.5">Tutor</Link>
            <Link href="/practice" className="opacity-60 hover:opacity-100">Practice</Link>
            <Link href="/flashcards" className="opacity-60 hover:opacity-100">Flashcards</Link>
            <Link href="/voice-cases" className="opacity-60 hover:opacity-100">Voice Cases</Link>
            <Link href="/score-calculator" className="opacity-60 hover:opacity-100">Score Calc</Link>
          </div>
          <div className="flex items-center gap-3">
            {isAuthenticated && (
              <Link
                href="/tutor/conversations"
                className="font-mono text-[10px] uppercase tracking-[0.1em] opacity-60 hover:opacity-100 px-3 py-1.5 border border-[#0c1a2e25] rounded-full"
              >
                Past chats
              </Link>
            )}
            <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">MCAT Tutor · Beta</div>
          </div>
        </header>
        <div className="flex-1 flex flex-col bg-[#ebe5d6] overflow-hidden">
          <div className="px-8 py-3 border-b border-[#0c1a2e15] flex items-center justify-between">
            <div className="flex items-center gap-2.5 font-serif text-base font-medium">
              <span className="w-2 h-2 rounded-full bg-[#a8324a] animate-pulse" />
              {conversationId ? "Continuing conversation" : "New tutor session"}
            </div>
            <div className="flex items-center gap-3">
              {messages.length > 0 && (
                <button
                  onClick={startFresh}
                  className="font-mono text-[10px] uppercase tracking-[0.1em] opacity-60 hover:opacity-100 px-2 py-1 border border-[#0c1a2e25] rounded"
                >
                  + New chat
                </button>
              )}
              <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">{messages.length} messages</div>
            </div>
          </div>
          <div ref={streamRef} className="flex-1 overflow-y-auto px-8 py-7 flex flex-col gap-5">
            {conversationLoading ? (
              <div className="m-auto text-center">
                <div className="flex items-center justify-center gap-2 mb-3">
                  <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" />
                  <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.15s" }} />
                  <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.3s" }} />
                </div>
                <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Loading conversation...</div>
              </div>
            ) : messages.length === 0 ? (
              <div className="m-auto max-w-xl text-center px-5 py-10">
                <h2 className="font-serif text-3xl font-medium tracking-tight mb-3 leading-tight">Built to bring out the physician in you.</h2>
                <p className="text-sm opacity-65 leading-relaxed mb-6">Ask anything about the MCAT — concepts, study strategy, practice problems. Upload a photo of your homework or a textbook diagram, and I&apos;ll walk you through it.</p>
                {isAuthenticated === false && (
                  <div className="mb-6 p-3 bg-[#a8324a08] border border-[#a8324a25] rounded-lg text-[12px] opacity-75">
                    <Link href="/sign-in" className="text-[#a8324a] font-medium hover:underline">Sign in</Link> to save your conversations and pick up where you left off.
                  </div>
                )}
                <div className="grid sm:grid-cols-2 gap-2.5 text-left">
                  <button onClick={() => askExample("Draw a titration curve for a weak acid and walk me through what each region means.")} className="p-4 bg-[#0c1a2e0a] border border-[#0c1a2e15] rounded-xl text-[13px] leading-snug hover:bg-[#0c1a2e1a] transition-all hover:-translate-y-0.5">
                    <span className="block font-mono text-[9px] tracking-[0.12em] opacity-55 uppercase mb-1">Biochem · diagram</span>
                    Draw a titration curve and explain each region.
                  </button>
                  <button onClick={() => askExample("Show me a free body diagram for a block sliding down a frictionless incline.")} className="p-4 bg-[#0c1a2e0a] border border-[#0c1a2e15] rounded-xl text-[13px] leading-snug hover:bg-[#0c1a2e1a] transition-all hover:-translate-y-0.5">
                    <span className="block font-mono text-[9px] tracking-[0.12em] opacity-55 uppercase mb-1">Physics · diagram</span>
                    Show me a free body diagram for a block on an incline.
                  </button>
                  <button onClick={() => askExample("Explain competitive vs non-competitive inhibition with a Michaelis-Menten diagram.")} className="p-4 bg-[#0c1a2e0a] border border-[#0c1a2e15] rounded-xl text-[13px] leading-snug hover:bg-[#0c1a2e1a] transition-all hover:-translate-y-0.5">
                    <span className="block font-mono text-[9px] tracking-[0.12em] opacity-55 uppercase mb-1">Biochem</span>
                    Competitive vs non-competitive inhibition, with a chart.
                  </button>
                  <button onClick={() => askExample("I have 3 months until my MCAT. How should I structure my studying?")} className="p-4 bg-[#0c1a2e0a] border border-[#0c1a2e15] rounded-xl text-[13px] leading-snug hover:bg-[#0c1a2e1a] transition-all hover:-translate-y-0.5">
                    <span className="block font-mono text-[9px] tracking-[0.12em] opacity-55 uppercase mb-1">Strategy</span>
                    How should I structure 3 months of MCAT prep?
                  </button>
                </div>
              </div>
            ) : (
              messages.map((msg, i) =>
                msg.role === "user" ? (
                  <div key={i} className="self-end max-w-[78%] flex flex-col items-end gap-2">
                    {msg.images && msg.images.length > 0 && (
                      <div className="flex flex-wrap gap-2 justify-end">
                        {msg.images.map((src, idx) => (
                          // eslint-disable-next-line @next/next/no-img-element
                          <img
                            key={idx}
                            src={src}
                            alt="Attached"
                            className="max-w-[200px] max-h-[200px] rounded-xl object-contain border border-[#0c1a2e25]"
                          />
                        ))}
                      </div>
                    )}
                    {msg.text && (
                      <div className="bg-[#0c1a2e] text-[#f5f1ea] px-4 py-3 rounded-2xl rounded-br-md text-[15px] leading-relaxed">
                        {msg.text}
                      </div>
                    )}
                  </div>
                ) : (
                  <div key={i} className="self-start max-w-[85%] tutor-msg">
                    <div className="flex items-center gap-2 mb-2 font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#a8324a]" />
                      Vitalis
                    </div>
                    <div className="text-[15px] leading-relaxed" dangerouslySetInnerHTML={{ __html: formatBody(msg.text) }} />
                  </div>
                )
              )
            )}
            {loading && (
              <div className="self-start">
                <div className="flex items-center gap-2 mb-2 font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#a8324a]" />
                  Vitalis
                </div>
                <div className="flex items-center gap-1.5 opacity-60">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0s" }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.15s" }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.3s" }} />
                </div>
              </div>
            )}
          </div>

          {pendingImages.length > 0 && (
            <div className="border-t border-[#0c1a2e15] px-8 py-3 bg-[#ebe5d6] flex gap-2 flex-wrap">
              {pendingImages.map((img, i) => (
                <div key={i} className="relative">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={img.dataUrl} alt="Pending" className="w-16 h-16 rounded-lg object-cover border border-[#0c1a2e25]" />
                  <button onClick={() => removePendingImage(i)} className="absolute -top-2 -right-2 w-5 h-5 bg-[#0c1a2e] text-[#f5f1ea] rounded-full flex items-center justify-center text-[10px] hover:bg-[#a8324a]">×</button>
                </div>
              ))}
            </div>
          )}

          <div className="border-t border-[#0c1a2e15] px-8 py-4 flex gap-3 items-center bg-[#ebe5d6]">
            <input ref={fileInputRef} type="file" accept="image/*" multiple onChange={handleFileSelect} className="hidden" />
            <button onClick={() => fileInputRef.current?.click()} disabled={loading} className="w-10 h-10 rounded-full bg-[#0c1a2e1a] text-[#0c1a2e] hover:bg-[#0c1a2e2a] flex items-center justify-center disabled:opacity-30 flex-shrink-0" title="Upload image">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
              </svg>
            </button>
            <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }} placeholder={pendingImages.length > 0 ? "Add a question about the image..." : "Ask anything — Bio, Chem, Phys, Psych, CARS..."} className="flex-1 bg-transparent border-none outline-none text-[15px] placeholder:text-[#0c1a2e66]" />
            <button onClick={send} disabled={loading || (!input.trim() && pendingImages.length === 0)} className="bg-[#0c1a2e] text-[#f5f1ea] w-10 h-10 rounded-full flex items-center justify-center disabled:opacity-30 transition-transform hover:scale-105">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          </div>
          <div className="px-8 py-2.5 font-mono text-[10px] tracking-[0.08em] opacity-40 text-center border-t border-[#0c1a2e15]">
            Vitalis is a study aid. Verify critical content with official AAMC materials. {isAuthenticated && conversationId ? "Your conversation is being saved." : ""}
          </div>
        </div>
      </div>
      <style jsx global>{`
        .tutor-msg p { margin-bottom: 10px; }
        .tutor-msg p:last-child { margin-bottom: 0; }
        .tutor-msg strong { font-weight: 600; }
        .tutor-msg em { font-style: italic; }
        .tutor-msg ul, .tutor-msg ol { margin: 10px 0; padding-left: 22px; }
        .tutor-msg li { margin-bottom: 5px; }
        .tutor-msg code { background: #0c1a2e14; padding: 2px 6px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 13px; }
        .tutor-msg h3 { font-family: 'Fraunces', serif; font-size: 18px; font-weight: 600; margin: 14px 0 8px; }
        .tutor-msg .diagram { margin: 14px 0; padding: 14px; background: #0c1a2e08; border: 1px solid #0c1a2e15; border-radius: 10px; display: flex; justify-content: center; }
        .tutor-msg .diagram svg { max-width: 100%; height: auto; }
        .tutor-msg .chart-wrap { margin: 14px 0; padding: 18px; background: #0c1a2e08; border: 1px solid #0c1a2e15; border-radius: 10px; height: 300px; position: relative; }
      `}</style>
    </>
  );
}

export default function TutorPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#f5f1ea]" />}>
      <TutorPageContent />
    </Suspense>
  );
}