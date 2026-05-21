import Anthropic from "@anthropic-ai/sdk";

const CONDITION_POOL = [
  "pulmonary embolism", "asthma exacerbation", "pneumothorax", "bronchitis",
  "diabetic ketoacidosis", "hypoglycemia", "hyperthyroidism", "hypothyroidism",
  "iron deficiency anemia", "sickle cell crisis",
  "panic attack", "depression with somatic symptoms", "PTSD flashback", "eating disorder complications",
  "migraine with aura", "concussion", "seizure (post-ictal)", "syncope (vasovagal)",
  "acute gastroenteritis", "appendicitis", "GERD", "lactose intolerance",
  "urinary tract infection", "kidney stone",
  "viral meningitis (mild)", "mononucleosis", "Lyme disease (early)", "strep throat",
  "heat exhaustion", "dehydration from exercise", "rhabdomyolysis from over-exercise",
  "hypertensive crisis", "orthostatic hypotension",
  "allergic reaction / anaphylaxis (mild)", "asthma trigger by exercise",
  "addisonian crisis (mild)", "syndrome of inappropriate ADH",
  "celiac disease", "IBS",
  "alcohol intoxication", "caffeine overdose", "MDMA after-effects",
];

const CASE_GENERATOR_PROMPT = [
  "You are a case generator for an MCAT prep tool. Generate a single patient scenario.",
  "",
  `IMPORTANT: To ensure variety, pick a condition RANDOMLY from this list (do NOT default to common ones like pulmonary embolism unless randomly chosen): ${CONDITION_POOL.join(", ")}.`,
  "",
  "Vary patient demographics each time: gender, ethnicity-suggesting names (Sarah, Marcus, Priya, Diego, Aiyana, Kai, Olivia, Devontae, Mei, Hassan), settings (student health, urgent care, ER, dorm, gym, library), and personality (anxious, stoic, exhausted, sarcastic, embarrassed, friendly, in denial, hostile).",
  "",
  "Connect the condition to ONE specific MCAT-tested science concept (e.g., gas exchange, acid-base buffering, neurotransmitter reuptake, osmotic pressure, action potential, etc.).",
  "",
  "Return ONLY valid JSON with this exact structure (no markdown, no extra text):",
  "{",
  '  "patientName": "first name only",',
  '  "patientAge": number between 18-30,',
  '  "patientGender": "female" or "male" or "nonbinary",',
  '  "setting": "where they are meeting",',
  '  "openingLine": "what the patient says when the student walks in (1-2 sentences, in their voice)",',
  '  "hiddenDiagnosis": "the actual underlying issue",',
  '  "mcatConcept": "the specific MCAT science concept being tested",',
  '  "mcatSection": "Bio/Biochem" or "Chem/Phys" or "Psych/Soc",',
  '  "keySymptoms": ["list", "of", "symptoms (3-6 items)"],',
  '  "redFlags": ["things a sharp student should ask about (2-4 items)"],',
  '  "patientPersonality": "1 sentence describing how this patient speaks"',
  "}",
  "",
  "Make scenarios realistic for college-age students. Vary the setting and presentation. NEVER pick the same condition twice in a row.",
].join("\n");

export async function POST() {
  try {
    const client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });

    // Randomly nudge the model toward a specific category to force variety
    const categories = ["respiratory", "metabolic/endocrine", "psychiatric/neuro", "GI/renal", "musculoskeletal/dermatology", "infectious"];
    const randomCategory = categories[Math.floor(Math.random() * categories.length)];
    const randomSeed = Math.random().toString(36).slice(2, 8);

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 1000,
      system: CASE_GENERATOR_PROMPT,
      messages: [
        {
          role: "user",
          content: `Generate a new MCAT-relevant patient case. Focus area for this case: ${randomCategory}. Variety seed: ${randomSeed} (use this as a hint to pick something different from the most obvious choice).`,
        },
      ],
      temperature: 1.0,
    });

    const text = response.content
      .filter((block) => block.type === "text")
      .map((block) => (block.type === "text" ? block.text : ""))
      .join("\n")
      .trim();

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