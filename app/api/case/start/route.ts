import Anthropic from "@anthropic-ai/sdk";

const CASE_GENERATOR_PROMPT = [
  "You are a case generator for an MCAT prep tool. Generate a single patient scenario that connects to a real MCAT-tested science concept (from Bio/Biochem, Chem/Phys, or Psych/Soc).",
  "",
  "Return ONLY valid JSON with this exact structure (no markdown, no extra text):",
  "{",
  '  "patientName": "first name only",',
  '  "patientAge": number between 18-30,',
  '  "patientGender": "female" or "male" or "nonbinary",',
  '  "setting": "where they are meeting (e.g., student health clinic, ER, dorm)",',
  '  "openingLine": "what the patient says when the student walks in (1-2 sentences, in their voice, scared or confused or normal)",',
  '  "hiddenDiagnosis": "the actual underlying issue (e.g., pulmonary embolism, DKA, panic attack)",',
  '  "mcatConcept": "the specific MCAT science concept being tested (e.g., oxygen-hemoglobin dissociation, acid-base buffering)",',
  '  "mcatSection": "Bio/Biochem" or "Chem/Phys" or "Psych/Soc",',
  '  "keySymptoms": ["list", "of", "symptoms the patient has (3-6 items)"],',
  '  "redFlags": ["things a sharp student should ask about (e.g., recent travel, family history) (2-4 items)"],',
  '  "patientPersonality": "1 sentence describing how this patient speaks (e.g., anxious teenager, stoic athlete, embarrassed)"',
  "}",
  "",
  "Vary the cases — don't always do pulmonary embolism. Rotate across systems: respiratory, metabolic, cardiac, neuro, endocrine, GI, psychiatric.",
  "Make scenarios realistic for the age range. College students don't usually have heart attacks.",
  "Each case should map cleanly to ONE primary MCAT concept.",
].join("\n");

export async function POST() {
  try {
    const client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 1000,
      system: CASE_GENERATOR_PROMPT,
      messages: [{ role: "user", content: "Generate a new MCAT-relevant patient case." }],
    });

    const text = response.content
      .filter((block) => block.type === "text")
      .map((block) => (block.type === "text" ? block.text : ""))
      .join("\n")
      .trim();

    // Try to extract JSON if wrapped in code fences
    let jsonStr = text;
    const fenceMatch = text.match(/```(?:json)?\s*([\s\S]*?)```/);
    if (fenceMatch) jsonStr = fenceMatch[1].trim();

    const caseData = JSON.parse(jsonStr);
    return Response.json({ case: caseData });
  } catch (error) {
    console.error("Case generation error:", error);
    return Response.json(
      { error: "Failed to generate case" },
      { status: 500 }
    );
  }
}