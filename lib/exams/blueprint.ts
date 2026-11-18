/**
 * The shape of the real MCAT, and how we turn a raw score into an estimate.
 *
 * Everything in this file is structure, not content: section order, question
 * counts, timing, the break pattern, the AAMC content categories and skills we
 * tag each question with, and the raw-to-scaled estimate used on the report.
 *
 * Section counts, times and the break pattern match the published AAMC exam
 * format (230 questions; 95/90/95/95 minutes; optional 10, 30 and 10 minute
 * breaks). Those are stable year to year and are checked against the AAMC's
 * "What's on the MCAT Exam?" page when it changes.
 */

export type ExamSectionId = "chem-phys" | "cars" | "bio-biochem" | "psych-soc";

export interface SectionBlueprint {
  id: ExamSectionId;
  /** The name as it appears on the real score report. */
  name: string;
  short: string;
  /** How students refer to it. */
  nickname: string;
  questions: number;
  minutes: number;
  /** Questions that hang off a passage. CARS is entirely passage-based. */
  passageQuestions: number;
  /** Standalone questions with no passage. */
  discreteQuestions: number;
  /** The break that follows this section, in minutes. Null after the last. */
  breakAfterMinutes: number | null;
  breakLabel: string | null;
  /** Which of our four study sections this maps to, for recommendations. */
  studySection: "chem-phys" | "cars" | "bio-biochem" | "psych-soc";
}

export const SECTIONS: SectionBlueprint[] = [
  {
    id: "chem-phys",
    name: "Chemical and Physical Foundations of Biological Systems",
    short: "C/P",
    nickname: "Chem/Phys",
    questions: 59,
    minutes: 95,
    passageQuestions: 44,
    discreteQuestions: 15,
    breakAfterMinutes: 10,
    breakLabel: "First break",
    studySection: "chem-phys",
  },
  {
    id: "cars",
    name: "Critical Analysis and Reasoning Skills",
    short: "CARS",
    nickname: "CARS",
    questions: 53,
    minutes: 90,
    passageQuestions: 53,
    discreteQuestions: 0,
    breakAfterMinutes: 30,
    breakLabel: "Mid-exam break",
    studySection: "cars",
  },
  {
    id: "bio-biochem",
    name: "Biological and Biochemical Foundations of Living Systems",
    short: "B/B",
    nickname: "Bio/Biochem",
    questions: 59,
    minutes: 95,
    passageQuestions: 44,
    discreteQuestions: 15,
    breakAfterMinutes: 10,
    breakLabel: "Second break",
    studySection: "bio-biochem",
  },
  {
    id: "psych-soc",
    name: "Psychological, Social, and Biological Foundations of Behavior",
    short: "P/S",
    nickname: "Psych/Soc",
    questions: 59,
    minutes: 95,
    passageQuestions: 44,
    discreteQuestions: 15,
    breakAfterMinutes: null,
    breakLabel: null,
    studySection: "psych-soc",
  },
];

export const TOTAL_QUESTIONS = SECTIONS.reduce((sum, section) => sum + section.questions, 0); // 230
export const TESTING_MINUTES = SECTIONS.reduce((sum, section) => sum + section.minutes, 0); // 375
export const BREAK_MINUTES = SECTIONS.reduce((sum, section) => sum + (section.breakAfterMinutes ?? 0), 0); // 50

export function sectionById(id: string): SectionBlueprint | undefined {
  return SECTIONS.find(section => section.id === id);
}

/**
 * The AAMC's four Scientific Inquiry and Reasoning Skills, and the CARS
 * reasoning skills. Tagging every question lets the report say "you lose
 * points on data interpretation, not on content" — which is a different fix.
 */
export const SKILLS = {
  "skill-1": { name: "Knowledge of scientific concepts and principles", short: "Content recall" },
  "skill-2": { name: "Scientific reasoning and problem solving", short: "Reasoning" },
  "skill-3": { name: "Reasoning about the design and execution of research", short: "Research design" },
  "skill-4": { name: "Data-based and statistical reasoning", short: "Data and stats" },
  "cars-comprehension": { name: "Foundations of comprehension", short: "Comprehension" },
  "cars-reasoning-within": { name: "Reasoning within the text", short: "Reasoning within" },
  "cars-reasoning-beyond": { name: "Reasoning beyond the text", short: "Reasoning beyond" },
} as const;

export type SkillId = keyof typeof SKILLS;

/**
 * AAMC content categories, by their published codes. We tag each science
 * question with one so the report can point at a specific weakness rather
 * than a whole section.
 */
export const CONTENT_CATEGORIES: Record<string, string> = {
  "1A": "Structure and function of proteins and their constituents",
  "1B": "Transmission of genetic information",
  "1C": "Transmission of heritable information and processes that increase genetic diversity",
  "1D": "Principles of bioenergetics and fuel molecule metabolism",
  "2A": "Assemblies of molecules, cells and groups of cells",
  "2B": "The structure, growth, physiology and genetics of prokaryotes and viruses",
  "2C": "Processes of cell division, differentiation and specialization",
  "3A": "Structure and functions of the nervous and endocrine systems",
  "3B": "Structure and integrative functions of the main organ systems",
  "4A": "Translational motion, forces, work, energy, and equilibrium",
  "4B": "Importance of fluids for the circulation of blood, gas movement, and gas exchange",
  "4C": "Electrochemistry and electrical circuits and their elements",
  "4D": "How light and sound interact with matter",
  "4E": "Atoms, nuclear decay, electronic structure, and atomic chemical behavior",
  "5A": "Unique nature of water and its solutions",
  "5B": "Nature of molecules and intermolecular interactions",
  "5C": "Separation and purification methods",
  "5D": "Structure, function, and reactivity of biologically relevant molecules",
  "5E": "Principles of chemical thermodynamics and kinetics",
  "6A": "Sensing the environment",
  "6B": "Making sense of the environment",
  "6C": "Responding to the world",
  "7A": "Individual influences on behavior",
  "7B": "Social processes that influence human behavior",
  "7C": "Attitude and behavior change",
  "8A": "Self-identity",
  "8B": "Social thinking",
  "8C": "Social interactions",
  "9A": "Understanding social structure",
  "9B": "Demographic characteristics and processes",
  "10A": "Social inequality",
};

/**
 * Raw correct count to estimated scaled score.
 *
 * The AAMC does not publish its conversion tables, and the real conversion is
 * re-equated for every test form, so no honest product can claim an exact
 * scaled score from a third-party exam. What follows is an estimate built by
 * anchoring percent-correct to the scaled scores and percentiles the AAMC does
 * publish, with CARS set slightly harsher because its raw-to-scaled curve runs
 * tighter than the science sections.
 *
 * It is labelled as an estimate everywhere a student sees it, with a range
 * rather than a bare number, because a precise-looking fake number is worse
 * than an honest band: students make test-date decisions on these.
 */
export const SCALE_MIN = 118;
export const SCALE_MAX = 132;
export const TOTAL_MIN = SCALE_MIN * 4; // 472
export const TOTAL_MAX = SCALE_MAX * 4; // 528

/** Percent-correct thresholds, lowest first, paired with the scaled score. */
type Curve = [percent: number, scaled: number][];

const SCIENCE_CURVE: Curve = [
  [0, 118], [18, 119], [25, 120], [31, 121], [37, 122], [42, 123], [47, 124],
  [52, 125], [57, 126], [62, 127], [68, 128], [73, 129], [79, 130], [86, 131], [93, 132],
];

const CARS_CURVE: Curve = [
  [0, 118], [20, 119], [27, 120], [33, 121], [39, 122], [45, 123], [50, 124],
  [55, 125], [60, 126], [66, 127], [71, 128], [77, 129], [83, 130], [89, 131], [95, 132],
];

function curveFor(section: ExamSectionId): Curve {
  return section === "cars" ? CARS_CURVE : SCIENCE_CURVE;
}

/**
 * The estimated scaled score for a section, plus the honest band around it.
 * The band is ±1 because that is roughly the standard error the AAMC reports
 * for a single section; claiming tighter than that would be invented precision.
 */
export function scaledFor(section: ExamSectionId, correct: number, total: number) {
  if (total <= 0) return { scaled: SCALE_MIN, low: SCALE_MIN, high: SCALE_MIN, percent: 0 };
  const percent = (correct / total) * 100;
  const curve = curveFor(section);
  let scaled = SCALE_MIN;
  for (const [threshold, value] of curve) if (percent >= threshold) scaled = value;
  return {
    scaled,
    low: Math.max(SCALE_MIN, scaled - 1),
    high: Math.min(SCALE_MAX, scaled + 1),
    percent: Math.round(percent),
  };
}

/** Published AAMC total-score percentiles, used only to place a total score. */
const TOTAL_PERCENTILES: [score: number, percentile: number][] = [
  [472, 1], [478, 1], [482, 3], [486, 7], [490, 14], [494, 25], [498, 38],
  [500, 45], [502, 53], [506, 69], [510, 81], [514, 90], [518, 96], [522, 99], [526, 100],
];

/** The percentile band a total score falls in, or null when out of range. */
export function percentileFor(total: number): number | null {
  if (!Number.isFinite(total) || total < TOTAL_MIN || total > TOTAL_MAX) return null;
  let percentile: number | null = null;
  for (const [score, value] of TOTAL_PERCENTILES) if (total >= score) percentile = value;
  return percentile;
}
