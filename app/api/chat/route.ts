import Anthropic from "@anthropic-ai/sdk";

const SYSTEM_PROMPT = [
  "You are Vitalis, an expert MCAT tutor. Your students are pre-med college students preparing for the MCAT.",
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

type IncomingMessage = {
  role: "user" | "assistant";
  content:
    | string
    | Array<TextPart | { type: "image"; source: { type: "base64"; media_type: string; data: string } }>;
};

export async function POST(request: Request) {
  try {
    const { messages } = (await request.json()) as { messages: IncomingMessage[] };

    if (!Array.isArray(messages) || messages.length === 0) {
      return Response.json({ error: "No messages provided" }, { status: 400 });
    }

    // Normalize messages for the Anthropic SDK
    const normalized = messages.map((m) => {
      if (typeof m.content === "string") {
        return { role: m.role, content: m.content };
      }
      // Already array form (e.g., with images)
      const parts: Array<TextPart | ImagePart> = m.content.map((part) => {
        if (part.type === "image") {
          const mt = part.source.media_type;
          const validMt =
            mt === "image/jpeg" || mt === "image/png" || mt === "image/gif" || mt === "image/webp"
              ? mt
              : "image/jpeg";
          return {
            type: "image" as const,
            source: {
              type: "base64" as const,
              media_type: validMt,
              data: part.source.data,
            },
          };
        }
        return part as TextPart;
      });
      return { role: m.role, content: parts };
    });

    const client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 4096,
      system: SYSTEM_PROMPT,
      messages: normalized,
    });

    const reply = response.content
      .filter((b) => b.type === "text")
      .map((b) => (b.type === "text" ? b.text : ""))
      .join("\n")
      .trim();

    return Response.json({ reply });
  } catch (error) {
    console.error("Chat API error:", error);
    return Response.json({ error: "Failed to get response" }, { status: 500 });
  }
}