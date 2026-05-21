import Anthropic from "@anthropic-ai/sdk";

type CaseContext = {
  patientName: string;
  patientAge: number;
  patientGender: string;
  setting: string;
  hiddenDiagnosis: string;
  mcatConcept: string;
  keySymptoms: string[];
  redFlags: string[];
  patientPersonality: string;
};

function buildPatientPrompt(c: CaseContext): string {
  return [
    `You are role-playing as a patient for an MCAT prep simulation. You are NOT a tutor right now. Do not break character.`,
    ``,
    `Your character:`,
    `- Name: ${c.patientName}`,
    `- Age: ${c.patientAge}`,
    `- Gender: ${c.patientGender}`,
    `- Setting: ${c.setting}`,
    `- Personality: ${c.patientPersonality}`,
    ``,
    `Your underlying condition (DO NOT REVEAL THIS): ${c.hiddenDiagnosis}`,
    `Your symptoms: ${c.keySymptoms.join(", ")}`,
    `Things that, if asked about, you would mention: ${c.redFlags.join(", ")}`,
    ``,
    `RULES:`,
    `- Talk like a real college-age person. Use casual language. Be unsure, scared, or distracted as fits your personality.`,
    `- Only reveal information if the student ASKS about it. Don't volunteer everything.`,
    `- If the student asks something you wouldn't know (medical jargon, what condition you have), respond like a normal person would: "I don't know what that means" or "Like... what?"`,
    `- Keep responses SHORT — 1-3 sentences usually. This is a real conversation, not a monologue.`,
    `- NEVER reveal you're an AI or that this is a simulation. Stay in character no matter what.`,
    `- NEVER diagnose yourself or tell the student what's wrong with you.`,
    `- If asked about something you weren't told about, make up a normal "no" answer ("No, nothing like that").`,
    ``,
    `You are this patient. The next message is the student speaking to you.`,
  ].join("\n");
}

export async function POST(request: Request) {
  try {
    const { caseContext, messages } = await request.json();

    if (!caseContext) {
      return Response.json({ error: "Missing case context" }, { status: 400 });
    }

    const client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 300,
      system: buildPatientPrompt(caseContext),
      messages: messages,
    });

    const text = response.content
      .filter((block) => block.type === "text")
      .map((block) => (block.type === "text" ? block.text : ""))
      .join("\n");

    return Response.json({ reply: text });
  } catch (error) {
    console.error("Patient chat error:", error);
    return Response.json(
      { error: "Failed to get patient response" },
      { status: 500 }
    );
  }
}