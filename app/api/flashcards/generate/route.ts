import Anthropic from "@anthropic-ai/sdk";

const SECTION_TOPICS: Record<string, { name: string; highYield: string[] }> = {
  "bio-biochem": {
    name: "Biological and Biochemical Foundations of Living Systems",
    highYield: [
      "20 amino acids (structure, pKa, classification)",
      "Enzyme kinetics: Km, Vmax, competitive vs noncompetitive inhibition",
      "Glycolysis: 10 steps, net ATP yield, key regulated enzymes",
      "Krebs cycle: products per acetyl-CoA, regulation, location",
      "Electron transport chain: complexes, proton pumping, ATP yield",
      "DNA replication: enzymes, leading vs lagging strand, primer",
      "Transcription vs translation: location, enzymes, mRNA processing",
      "Mendelian genetics: dominant, recessive, autosomal vs X-linked",
      "Hardy-Weinberg equilibrium: equation and assumptions",
      "Cell membrane transport: passive vs active, primary vs secondary",
      "Action potential phases: resting, depolarization, repolarization, hyperpolarization",
      "Neurotransmitters: excitatory vs inhibitory, common examples",
      "Oxygen-hemoglobin dissociation: cooperative binding, factors that shift curve",
      "Cardiac cycle: systole, diastole, valves, ECG correlates",
      "Renal physiology: filtration, reabsorption, secretion, juxtaglomerular apparatus",
      "Endocrine hormones: source, target, feedback loops",
      "Immune system: innate vs adaptive, antibody classes, T cell types",
      "Cell cycle: phases, checkpoints, regulators (cyclins, CDKs)",
    ],
  },
  "chem-phys": {
    name: "Chemical and Physical Foundations of Biological Systems",
    highYield: [
      "pKa and buffer systems: Henderson-Hasselbalch equation",
      "Strong vs weak acids: dissociation, conjugate base strength",
      "Gibbs free energy: ΔG = ΔH - TΔS, spontaneity",
      "Reaction equilibrium: Keq, Le Chatelier's principle",
      "Reaction rate laws: zero, first, and second order",
      "Stereochemistry: R/S, E/Z, enantiomers vs diastereomers",
      "SN1 vs SN2: rate-determining step, stereochemistry, substrate preference",
      "E1 vs E2 elimination: conditions, Zaitsev's rule",
      "IR spectroscopy: key functional group absorptions",
      "NMR spectroscopy: chemical shift, splitting (n+1 rule)",
      "Newton's laws: F=ma, action-reaction",
      "Kinematic equations: constant acceleration",
      "Conservation of energy: KE, PE, work-energy theorem",
      "Bernoulli's equation: fluid flow, pressure-velocity relationship",
      "Poiseuille's law: laminar flow through a tube",
      "Coulomb's law and electric field",
      "Circuits: resistors in series vs parallel, Kirchhoff's laws",
      "Doppler effect: equation, frequency change",
      "Lenses and mirrors: thin lens equation, magnification",
    ],
  },
  "psych-soc": {
    name: "Psychological, Social, and Biological Foundations of Behavior",
    highYield: [
      "Classical conditioning: UCS, UCR, CS, CR, extinction, spontaneous recovery",
      "Operant conditioning: positive/negative reinforcement vs punishment",
      "Piaget's stages of cognitive development",
      "Memory: sensory, short-term, working, long-term; encoding, retrieval",
      "Sleep stages: NREM (1-3) and REM, EEG patterns",
      "Signal detection theory: hits, misses, false alarms, correct rejections",
      "Emotion theories: James-Lange, Cannon-Bard, Schachter-Singer",
      "Maslow's hierarchy of needs",
      "Big Five personality traits (OCEAN)",
      "Major DSM categories of psychological disorders",
      "Cognitive dissonance: definition, examples, resolution",
      "Conformity: Asch experiment; Obedience: Milgram experiment",
      "Demographic transition model",
      "Stratification systems: class, caste, slavery, meritocracy",
      "Research methods: validity (internal vs external), reliability",
      "Statistical concepts: p-value, Type I vs II error, effect size",
      "Correlation vs causation: confounding variables",
      "Neurotransmitters: dopamine, serotonin, GABA, glutamate (functions)",
      "Brain regions: prefrontal cortex, hippocampus, amygdala, hypothalamus (functions)",
    ],
  },
  "cars": {
    name: "Critical Analysis and Reasoning Skills",
    highYield: [
      "Foundations of Comprehension: main idea and supporting details",
      "Reasoning Within the Text: integrating information from different parts of a passage",
      "Reasoning Beyond the Text: applying passage to a new context",
      "Identifying the author's main argument",
      "Distinguishing facts vs opinions in passages",
      "Recognizing tone and perspective shifts",
      "Spotting answer traps: wrong-but-true, out-of-scope, extreme statements",
      "Time management: aiming for ~9-10 minutes per passage",
      "Process of elimination strategies",
    ],
  },
};

const PROMPT = [
  "You are an expert MCAT content writer creating flashcards for high-yield exam topics.",
  "",
  "Generate a deck of 8 flashcards. Each card has:",
  "- A clear, focused front (a prompt, term, or short question)",
  "- A precise back (the answer or explanation)",
  "",
  "STYLE NOTES:",
  "- Focus on AAMC-tested concepts.",
  "- Front side should be specific (not 'what is metabolism?' but 'what is the net ATP yield of glycolysis?').",
  "- Back side should be concise (2-3 sentences max) but complete.",
  "- Mix definition cards (term → definition), application cards (scenario → concept), and quantitative cards (numbers, equations).",
  "- Use **bold** for key terms in the back side.",
  "- Avoid trivia. Test understanding, not memorization of obscure facts.",
  "",
  "OUTPUT — return ONLY valid JSON with this structure (no markdown, no extra text):",
  "{",
  '  "deck": [',
  "    {",
  '      "id": "c1",',
  '      "front": "the question or prompt",',
  '      "back": "the answer or explanation (2-3 sentences)",',
  '      "concept": "the specific concept being tested",',
  '      "difficulty": "easy" | "medium" | "hard"',
  "    }",
  "  ]",
  "}",
].join("\n");

export async function POST(request: Request) {
  try {
    const { section } = await request.json();

    let actualSection = section;
    if (section === "mixed") {
      const sections = ["bio-biochem", "chem-phys", "psych-soc", "cars"];
      actualSection = sections[Math.floor(Math.random() * sections.length)];
    }

    const info = SECTION_TOPICS[actualSection];
    if (!info) {
      return Response.json({ error: "Invalid section" }, { status: 400 });
    }

    // Pick 2-3 random high-yield topics for variety
    const shuffled = [...info.highYield].sort(() => Math.random() - 0.5);
    const focusTopics = shuffled.slice(0, 3);
    const randomSeed = Math.random().toString(36).slice(2, 8);

    const systemPrompt = [
      PROMPT,
      "",
      `Section: ${info.name}`,
      `Focus this deck on these high-yield topics (mix them across the 8 cards): ${focusTopics.join("; ")}`,
      `Variety seed: ${randomSeed}`,
    ].join("\n");

    const client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 2000,
      system: systemPrompt,
      messages: [
        { role: "user", content: `Generate a deck of 8 high-yield MCAT flashcards for ${info.name}.` },
      ],
      temperature: 0.9,
    });

    const text = response.content
      .filter((b) => b.type === "text")
      .map((b) => (b.type === "text" ? b.text : ""))
      .join("\n")
      .trim();

    let jsonStr = text;
    const fenceMatch = text.match(/```(?:json)?\s*([\s\S]*?)```/);
    if (fenceMatch) jsonStr = fenceMatch[1].trim();

    const data = JSON.parse(jsonStr);
    return Response.json({ ...data, section: actualSection });
  } catch (error) {
    console.error("Flashcard generation error:", error);
    return Response.json({ error: "Failed to generate flashcards" }, { status: 500 });
  }
}