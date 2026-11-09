import Anthropic from "@anthropic-ai/sdk";
import { randomUUID } from "node:crypto";
export const maxDuration = 60;

const SYSTEM_PROMPT = [
  "You are Nori, the friendly neuron mascot and MCAT tutor at Vitalis. Your students are pre-med college students preparing for the MCAT.",
  "",
  "Your style:",
  "- Conversational and direct, like a strong scorer mentoring a friend.",
  "- Concrete examples and analogies over abstract definitions.",
  "- When a concept has a visual component (titration curves, free body diagrams, biochem pathways, Michaelis-Menten plots, neural circuits, etc.), generate one. Use SVG for diagrams, Chart.js JSON for graphs.",
  "- Stay focused on MCAT-relevant content. If asked about something off-topic, briefly redirect.",
  "- Use markdown formatting: **bold** for key terms, *italics* for emphasis, `code` for short technical terms, ### for major section headers.",
  "- Bullets (- ) and numbered lists (1. ) work in standard markdown.",
  "",
  "When the student sends an image:",
  "- Read it carefully. It could be a homework problem, a textbook diagram, a question from a practice book, lecture notes, or something else.",
  "- If it's a problem, walk them through it. Don't just give the answer.",
  "- If it's a diagram/figure, explain what it shows and what's important to understand.",
  "- If you can't tell what something is or the image is unclear, ask.",
  "",
  "DIAGRAMS — when needed, emit SVG inside ```svg fenced code blocks. Use viewBox, no scripts.",
  "",
  "GRAPHS / CHARTS — when needed, emit a JSON spec inside ```chart fenced code blocks. Format:",
  "```chart",
  '{"type": "line", "title": "Optional title", "xLabel": "x axis label", "yLabel": "y axis label",',
  ' "datasets": [{"label": "Series name", "data": [{"x": 0, "y": 0}, {"x": 1, "y": 2}]}],',
  ' "annotations": [{"x": 1.5, "y": 1.8, "label": "Equivalence point"}]}',
  "```",
  "Supported types: line, scatter, bar. Annotations render as labeled red dots on top of the chart.",
].join("\n");

type ImagePart = {
  type: "image";
  source: {
    type: "base64";
    media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp";
    data: string;
  };
};

type TextPart = { type: "text"; text: string };

type Message = { role: "user" | "assistant"; content: string | Array<TextPart | ImagePart> };
function validMessages(value: unknown): value is Message[] {
  if (!Array.isArray(value) || value.length === 0 || value.length > 100) return false;
  let textLength = 0;
  let imageLength = 0;
  for (const item of value) {
    if (!item || typeof item !== "object" || !["user", "assistant"].includes(item.role)) return false;
    if (typeof item.content === "string") {
      if (!item.content.trim() || item.content.length > 20000) return false;
      textLength += item.content.length;
    } else {
      if (!Array.isArray(item.content) || item.content.length === 0 || item.content.length > 8) return false;
      for (const part of item.content) {
        if (!part || typeof part !== "object") return false;
        if (part.type === "text" && typeof part.text === "string" && part.text.trim() && part.text.length <= 20000) {
          textLength += part.text.length;
        } else if (part.type === "image" && item.role === "user" && part.source?.type === "base64" &&
          ["image/jpeg", "image/png", "image/gif", "image/webp"].includes(part.source.media_type) &&
          typeof part.source.data === "string" && part.source.data.length > 0 &&
          /^[A-Za-z0-9+/]+={0,2}$/.test(part.source.data)) {
          imageLength += part.source.data.length;
        } else return false;
      }
    }
  }
  return textLength <= 120000 && imageLength <= 20000000 && value.at(-1).role === "user";
}

export async function POST(request: Request) {
  const requestId = randomUUID();
  let input: unknown;
  try { input = await request.json(); }
  catch { return Response.json({ error: "Send a valid JSON request.", requestId }, { status: 400 }); }
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return Response.json({ error: "Send a question for Nori.", requestId }, { status: 400 });
  }
  const { messages, mode } = input as Record<string, unknown>;
  if (!validMessages(messages) || (mode !== undefined && mode !== "companion")) {
    return Response.json({ error: "Send a valid question, or start a new chat if this conversation is too long.", requestId }, { status: 400 });
  }
  const apiKey = process.env.ANTHROPIC_API_KEY?.trim();
  if (!apiKey || /[\r\n]/.test(apiKey)) {
    console.warn("Nori unavailable", { requestId, reason: "key_configuration" });
    return Response.json({ error: "Nori is temporarily unavailable. Please try again later.", requestId }, { status: 503 });
  }
  // Retain only supported fields; never forward arbitrary client-supplied roles or options.
  const normalized: Message[] = messages.map(m => ({ role: m.role, content: typeof m.content === "string" ? m.content : m.content.map(p =>
    p.type === "text" ? { type: "text", text: p.text } : { type: "image", source: { type: "base64", media_type: p.source.media_type, data: p.source.data } }) }));
  try {
    const client = new Anthropic({ apiKey, timeout: 45000, maxRetries: 0 });
    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 4096,
      system: mode === "companion" ? SYSTEM_PROMPT + "\nThis is a compact on-page chat. Reply in concise plain text with short paragraphs. Do not output markdown, SVG, HTML, chart JSON, or code fences. Explain visual concepts in words." : SYSTEM_PROMPT,
      messages: normalized,
    }, { signal: request.signal });

    const reply = response.content
      .filter((b) => b.type === "text")
      .map((b) => (b.type === "text" ? b.text : ""))
      .join("\n")
      .trim();

    if (!reply || response.stop_reason === "max_tokens") throw new Error("Incomplete reply");
    return Response.json({ reply, requestId });
  } catch (error) {
    const status = error instanceof Anthropic.APIError ? error.status : undefined;
    console.warn("Nori unavailable", { requestId, status, reason: status ? "provider_error" : "generation_failed" });
    return Response.json({ error: "Nori couldn’t respond. Please try again.", requestId }, { status: 503 });
  }
}