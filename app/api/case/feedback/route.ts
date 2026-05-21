import Anthropic from "@anthropic-ai/sdk";

function buildFeedbackPrompt(caseContext: {
  patientName: string;
  hiddenDiagnosis: string;
  mcatConcept: string;
  mcatSection: string;
  keySymptoms: string[];
  redFlags: string[];
}): string {
  return [
    "You are Vitalis, an MCAT tutor. You just finished observing a student conduct a simulated patient interview.",
    "",
    "THE CASE (what the patient really had):",
    "- Diagnosis: " + caseContext.hiddenDiagnosis,
    "- MCAT concept being tested: " + caseContext.mcatConcept,
    "- MCAT section: " + caseContext.mcatSection,
    "- Key symptoms: " + caseContext.keySymptoms.join(", "),
    "- Red flags a sharp student would ask about: " + caseContext.redFlags.join(", "),
    "",
    "The full transcript of the student's interview with the patient (" + caseContext.patientName + ") follows in the next message.",
    "",
    "Your feedback should have THREE sections, in this order:",
    "",
    "### 1. The diagnosis",
    "Reveal what the patient actually had. One short paragraph.",
    "",
    "### 2. What you did well / what you missed",
    "Briefly note questions the student asked that were good clinical thinking. Then list 2-4 things they missed asking about (especially red flags). Be honest but encouraging.",
    "",
    "### 3. The MCAT science",
    "THIS IS THE MOST IMPORTANT SECTION. Connect the case to the MCAT concept (" + caseContext.mcatConcept + "). Explain the underlying science the MCAT actually tests. Use **bold** for key terms. If a diagram would help (curves, energy graphs, etc.), include one using the chart format below.",
    "",
    "For graphs, use a code block starting with three backticks and the word 'chart', containing valid JSON like this example:",
    "{",
    '  "type": "line",',
    '  "title": "Oxygen-Hemoglobin Dissociation Curve",',
    '  "xLabel": "PO2 (mmHg)",',
    '  "yLabel": "Hb saturation (%)",',
    '  "datasets": [{"label": "Normal", "data": [{"x":10,"y":12},{"x":20,"y":35},{"x":40,"y":75},{"x":60,"y":89},{"x":80,"y":95},{"x":100,"y":98}]}],',
    '  "annotations": [{"x": 40, "y": 75, "label": "P50"}]',
    "}",
    "End the block with three backticks.",
    "",
    "End with one practice question the student should be able to answer after this case.",
    "",
    "Tone: warm, focused, like a good tutor. Don't over-praise. Don't be harsh.",
  ].join("\n");
}

export async function POST(request: Request) {
  try {
    const { caseContext, transcript } = await request.json();

    if (!caseContext || !transcript) {
      return Response.json({ error: "Missing case context or transcript" }, { status: 400 });
    }

    const client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });

    const userContent =
      "Here is the full transcript of my interview with " +
      caseContext.patientName +
      ":\n\n" +
      transcript +
      "\n\nPlease give me feedback.";

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 2000,
      system: buildFeedbackPrompt(caseContext),
      messages: [
        {
          role: "user",
          content: userContent,
        },
      ],
    });

    const text = response.content
      .filter((b) => b.type === "text")
      .map((b) => (b.type === "text" ? b.text : ""))
      .join("\n");

    return Response.json({ feedback: text });
  } catch (error) {
    console.error("Feedback generation error:", error);
    return Response.json(
      { error: "Failed to generate feedback" },
      { status: 500 }
    );
  }
}