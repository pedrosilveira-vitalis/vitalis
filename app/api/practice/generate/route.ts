import { withQuestionTokens } from "@/lib/question-token";
import Anthropic from "@anthropic-ai/sdk";
import { sessionSettings, sections, allocateSections, parseQuestions } from "@/lib/practice";
import { fresh, reserveQuestions } from "./rotation";
export const maxDuration = 120;

const SECTION_CONTEXT: Record<string, { name: string; topics: string[]; style: string }> = {
  "bio-biochem": {
    name: "Biological and Biochemical Foundations of Living Systems",
    topics: [
      "amino acid structure and function", "protein structure and folding", "enzyme kinetics (Michaelis-Menten)",
      "cellular respiration and ATP yield", "glycolysis and gluconeogenesis", "Krebs cycle and ETC",
      "DNA replication, transcription, translation", "Mendelian and non-Mendelian genetics",
      "cell membrane transport (osmosis, active transport)", "signal transduction cascades",
      "endocrine system (hormones, feedback loops)", "nervous system (action potentials, synaptic transmission)",
      "cardiovascular physiology (Starling forces, cardiac output)", "renal physiology (filtration, secretion)",
      "respiratory physiology (gas exchange, oxygen-hemoglobin curve)", "immune system (innate vs adaptive)",
      "microbial classification and reproduction", "lipid metabolism and fatty acid synthesis",
    ],
    style: "Tests integration of biology and biochemistry. Often involves experimental data interpretation.",
  },
  "chem-phys": {
    name: "Chemical and Physical Foundations of Biological Systems",
    topics: [
      "acid-base chemistry (pKa, buffers, Henderson-Hasselbalch)", "thermodynamics (Gibbs free energy)",
      "kinetics and equilibrium", "electrochemistry and redox", "stereochemistry and chirality",
      "functional groups and IR/NMR spectroscopy", "nucleophilic substitution (SN1/SN2) and elimination",
      "translational mechanics (forces, energy, momentum)", "fluids (Bernoulli, Poiseuille, surface tension)",
      "electrostatics and circuits", "optics (lenses, mirrors, refraction)", "waves and sound (Doppler)",
      "atomic structure and periodic trends", "intermolecular forces and phase changes",
      "solutions and colligative properties", "gas laws and kinetic molecular theory",
    ],
    style: "Heavy on quantitative reasoning, dimensional analysis, and applying physics/chem to biological systems.",
  },
  "psych-soc": {
    name: "Psychological, Social, and Biological Foundations of Behavior",
    topics: [
      "classical and operant conditioning", "cognitive development (Piaget, Vygotsky)",
      "memory (encoding, storage, retrieval, types)", "sensation and perception (signal detection theory)",
      "emotion theories (James-Lange, Cannon-Bard, Schachter-Singer)", "motivation (drive reduction, Maslow)",
      "personality theories (Big Five, Freud, humanistic)", "psychological disorders and DSM",
      "social cognition (attribution theory, cognitive dissonance)", "group dynamics (conformity, obedience)",
      "demographic structures and stratification", "socialization and culture",
      "research methods (validity, reliability, experimental design)", "statistics (mean, median, SD, p-values, correlation vs causation)",
      "biological bases of behavior (neurotransmitters, brain regions)", "sleep stages and circadian rhythms",
    ],
    style: "Heavily tests research methodology, statistical reasoning, and applying theories to scenarios.",
  },
  "cars": {
    name: "Critical Analysis and Reasoning Skills",
    topics: [
      "humanities passage (philosophy, ethics, literary criticism, history)",
      "social science passage (sociology, anthropology, psychology, political theory, economics)",
    ],
    style: "Passages are dense, argument-driven, and require inference. NO outside knowledge — only the passage. Questions test: main idea, author's purpose, inference, application of ideas to new contexts, evaluation of arguments.",
  },
};

const PROMPT_INTRO = [
  "You are an expert MCAT question writer trained on AAMC question style. Generate practice questions that closely mirror the format, difficulty, and reasoning style of real AAMC MCAT questions.",
  "",
  "CRITICAL STYLE NOTES — make your questions AAMC-realistic:",
  "- Average MCAT question difficulty (not too easy, not impossibly hard).",
  "- Distractors (wrong answers) should be plausible — common misconceptions, partially correct, or right-idea-wrong-detail. NOT obviously absurd.",
  "- For science sections: questions should require TWO-STEP reasoning (understand a concept + apply it to a scenario or interpret data).",
  "- Use specific scientific values when relevant (e.g., 'an enzyme with Km = 5 mM' not 'an enzyme').",
  "- Avoid trivia. AAMC tests understanding, not memorization.",
  "- For CARS: questions test reading the passage. No outside knowledge required. Wrong answers often state things that are TRUE but not supported by the passage.",
  "",
  "OUTPUT FORMAT — return ONLY valid JSON, no markdown, no extra text:",
].join("\n");

const PASSAGE_SCHEMA = `{
  "format": "passage",
  "passage": {
    "title": "short title for the passage",
    "content": "300-450 word passage in MCAT style. For science: describe a research study with methods, results, sometimes a figure description. For CARS: a dense argument-driven excerpt with a clear thesis. NO LISTS — write it as flowing prose."
  },
  "questions": [
    {
      "id": "q1",
      "stem": "the question itself — clear, specific, testing one thing",
      "choices": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "correctAnswer": "A" | "B" | "C" | "D",
      "explanation": "2-3 sentence explanation of why the correct answer is right and the key concept being tested",
      "wrongAnswerExplanations": {
        "A": "why A is wrong (skip if A is correct)",
        "B": "why B is wrong (skip if B is correct)",
        "C": "why C is wrong (skip if C is correct)",
        "D": "why D is wrong (skip if D is correct)"
      },
      "concept": "the specific concept tested",
      "difficulty": "easy" | "medium" | "hard"
    }
  ]
}`;

const STANDALONE_SCHEMA = `{
  "format": "standalone",
  "questions": [
    {
      "id": "q1",
      "stem": "self-contained question. May include a brief scenario (2-3 sentences) or be discrete.",
      "choices": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "correctAnswer": "A" | "B" | "C" | "D",
      "explanation": "2-3 sentences",
      "wrongAnswerExplanations": {
        "A": "...", "B": "...", "C": "...", "D": "..."
      },
      "concept": "the specific concept tested",
      "difficulty": "easy" | "medium" | "hard"
    }
  ]
}`;

export async function POST(request: Request) {
  let settings: ReturnType<typeof sessionSettings>;
  let custom = false;
  let seen: Set<string>;
  try {
    const input = await request.json();
    settings = sessionSettings(input);
    custom = input.custom === true;
    seen = new Set(Array.isArray(input.seen) ? input.seen.slice(-10000).filter((id: unknown) => typeof id === "string" && /^[a-f0-9]{24}$/.test(id)) : []);
  }
  catch (error) { return Response.json({ error: error instanceof Error ? error.message : "Invalid settings" }, { status: 400 }); }
  const groups = allocateSections(settings.section, settings.count);
  const saved = await Promise.all(groups.map(g => reserveQuestions(settings, seen, g.count, g.section)));
  const bank = saved.flat();
  if (settings.section==="mixed" && bank.length < settings.count) {
    for (const section of sections) {
      const needed=settings.count-bank.length;
      if (!needed) break;
      bank.push(...await reserveQuestions(settings,seen,needed,section));
    }
  }
  const deficits = groups.map((g,i)=>({...g,count:g.count-saved[i].length})).filter(g=>g.count>0);
  function bankResponse() {
    return Response.json({questions:withQuestionTokens(bank),section:settings.section,source:"bank",exhausted:!bank.length});
  }
  if (!custom || bank.length >= settings.count || !deficits.length || ["guide","drills"].includes(settings.format)) return bankResponse();
  const apiKey = process.env.ANTHROPIC_API_KEY?.trim();
  if (!apiKey || /\s/.test(apiKey) || apiKey.startsWith("apikey_")) return bankResponse();
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 85000);
  try {
    const client = new Anthropic({ apiKey, timeout: 85000, maxRetries: 0 });
    const batches = await Promise.all(deficits.map(async ({ section, count }) => {
      const info = SECTION_CONTEXT[section];
      const passage = section === "cars" || settings.format === "passage";
      const response = await client.messages.create({
        model: "claude-sonnet-4-6", max_tokens: Math.min(16000, 1500 + count * 650), temperature: 0.8,
        system: [PROMPT_INTRO, passage ? PASSAGE_SCHEMA : STANDALONE_SCHEMA,
          `Section: ${info.name}. ${info.style}`,
          `Generate EXACTLY ${count} questions. Difficulty: ${settings.difficulty}.`,
          "For mixed difficulty, vary easy, medium, and hard. Include explanations for every incorrect choice.",
          `Topics to draw from: ${info.topics.join(", ")}`,
          passage ? "Include one coherent passage supporting ALL questions." : "Each question must be self-contained. Vary topics across the set."
        ].join("\n"),
        messages: [{ role: "user", content: `Create a fresh set of exactly ${count} questions. Return valid JSON only. Variety: ${crypto.randomUUID()}` }],
      }, { signal: controller.signal });
      if (response.stop_reason === "max_tokens") throw new Error("Truncated response");
      const raw = response.content.filter(b => b.type === "text").map(b => b.type === "text" ? b.text : "").join("\n").trim();
      const match = raw.match(/```(?:json)?\s*([\s\S]*?)```/);
      return parseQuestions(JSON.parse(match ? match[1] : raw), section, count, passage, settings.difficulty);
    }));
    const generated = batches.flatMap((batch,i)=>fresh(batch,seen,deficits[i].count));
    const selected=[...bank,...generated].slice(0,settings.count);
    return Response.json({questions:withQuestionTokens(selected),section:settings.section,source:bank.length ? "blend" : "generated",exhausted:!selected.length});
  } catch (error) {
    controller.abort();
    console.error("Practice generation failed", error instanceof Error ? error.name : "Unknown error");
    return bankResponse();
  } finally { clearTimeout(timer); }
}
