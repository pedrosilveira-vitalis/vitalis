import Anthropic from "@anthropic-ai/sdk";

type Question = {
  stem: string;
  choices: { A: string; B: string; C: string; D: string };
  correctAnswer: string;
  explanation: string;
  concept: string;
};

function buildSystemPrompt(question: Question, studentAnswer: string | null): string {
  return [
    "You are Vitalis, an MCAT tutor helping a student understand a practice question they just got wrong (or want to learn more about).",
    "",
    "The student just saw this question:",
    `Q: ${question.stem}`,
    `Choices: A) ${question.choices.A} | B) ${question.choices.B} | C) ${question.choices.C} | D) ${question.choices.D}`,
    `Correct answer: ${question.correctAnswer}`,
    `The student picked: ${studentAnswer || "(no answer)"}`,
    `Concept being tested: ${question.concept}`,
    `Explanation: ${question.explanation}`,
    "",
    "Your job: be a patient, focused tutor. Answer the student's follow-up questions about THIS specific question or the underlying concept.",
    "",
    "Style:",
    "- Short, conversational responses (2-4 sentences usually).",
    "- Use **bold** for key terms, *italics* for emphasis.",
    "- Don't give monologues — invite the student to ask more if needed.",
    "- Connect explanations back to what the MCAT actually tests.",
    "- If they ask about an unrelated topic, gently redirect to this question's concept.",
    "- Never reveal a different correct answer than what's already given.",
  ].join("\n");
}

export async function POST(request: Request) {
  try {
    const { question, studentAnswer, messages } = await request.json();

    if (!question || !messages) {
      return Response.json({ error: "Missing data" }, { status: 400 });
    }

    const client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 800,
      system: buildSystemPrompt(question, studentAnswer),
      messages: messages.filter((m: { role: string }) => m.role === "user" || m.role === "assistant"),
    });

    const text = response.content
      .filter((b) => b.type === "text")
      .map((b) => (b.type === "text" ? b.text : ""))
      .join("\n");

    return Response.json({ reply: text });
  } catch (error) {
    console.error("Practice explain error:", error);
    return Response.json(
      { error: "Failed to explain" },
      { status: 500 }
    );
  }
}