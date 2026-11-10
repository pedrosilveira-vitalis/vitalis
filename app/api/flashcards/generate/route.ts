import Anthropic from "@anthropic-ai/sdk";
import { parseCards, sections, type Section } from "@/lib/practice";
import { coreDeck } from "@/lib/core-flashcards";
import { randomUUID } from "node:crypto";
export const maxDuration = 120;

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
  "- Use plain text; do not include markdown formatting.",
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
  let input: unknown;
  try { input = await request.json(); }
  catch { return Response.json({ error: "Send a valid JSON request." }, { status: 400 }); }
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return Response.json({ error: "Choose a section and card count." }, { status: 400 });
  }
  const { section, count = 8, mode = "ai" } = input as Record<string, unknown>;
  if (typeof section !== "string" || ![...sections, "mixed"].includes(section) ||
      typeof count !== "number" || !Number.isInteger(count) || count < 1 || count > 20 ||
      !["ai", "core"].includes(String(mode))) {
    return Response.json({ error: "Choose a valid section, 1–20 cards, and AI or core mode." }, { status: 400 });
  }
  const requestId = randomUUID();
  const fallback = (unavailable: boolean) => {
    const deck = coreDeck(section as Section | "mixed", count);
    return Response.json({ ...deck, section, source: "core", requestId,
      notice: `${unavailable ? "AI generation is unavailable. " : ""}Showing ${deck.cards.length} core review cards from a fixed starter set.` });
  };
  if (mode === "core") return fallback(false);
  const apiKey = process.env.ANTHROPIC_API_KEY?.trim();
  if (!apiKey || /[\r\n]/.test(apiKey)) {
    console.warn("Flashcard fallback", { requestId, reason: "key_configuration" });
    return fallback(true);
  }
  try {
    const selected = section === "mixed" ? [...sections] : [section as Section];
    const info = selected.map(s => SECTION_TOPICS[s]);
    const topics = info.flatMap(s => s.highYield);
    for (let i = topics.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [topics[i], topics[j]] = [topics[j], topics[i]];
    }
    const system = [PROMPT.replace("deck of 8 flashcards", `deck of ${count} flashcards`),
      `Sections: ${info.map(s => s.name).join("; ")}`,
      `Suggested topics: ${topics.slice(0, 5).join("; ")}`,
      "Every front must be distinct. Do not invent facts. Include only the deck, front and back fields.",
    ].join("\n");
    const client = new Anthropic({ apiKey, timeout: 45000, maxRetries: 0 });
    const response = await client.messages.create({
      model: process.env.ANTHROPIC_FLASHCARD_MODEL?.trim() || "claude-sonnet-4-6",
      max_tokens: 8000, system,
      messages: [{ role: "user", content: `Generate exactly ${count} flashcards.` }],
      temperature: 0.7,
    }, { signal: request.signal });
    const text = response.content.filter(b => b.type === "text").map(b => b.type === "text" ? b.text : "").join("\n").trim();
    if (response.stop_reason === "max_tokens") throw new Error("Incomplete deck");
    const json = text.match(/^```(?:json)?\s*([\s\S]*?)```$/)?.[1] || text;
    const cards = parseCards(JSON.parse(json), count);
    if (new Set(cards.map(c => c.front.toLowerCase().replace(/\s+/g, " "))).size !== cards.length ||
        cards.some(c => c.front.length > 1500 || c.back.length > 4000)) throw new Error("Invalid deck");
    return Response.json({ cards, section, source: "ai", requestId, sources: [] });
  } catch (error) {
    // Never log SDK error bodies or credentials. The local ID correlates fallback reports.
    const status = error instanceof Anthropic.APIError ? error.status : undefined;
    console.warn("Flashcard fallback", { requestId, status, reason: status ? "provider_error" : "generation_failed" });
    return fallback(true);
  }
}
