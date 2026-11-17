/**
 * One-page cheat sheets, one per unit.
 *
 * Content lives here rather than in the database because these are editorial
 * documents, not user data: they are reviewed, versioned and diffed like the
 * lessons are. A unit with no sheet yet simply has no entry, and the UI says so
 * rather than rendering an empty page.
 */
export type Block =
  | { kind: "list"; heading: string; items: string[] }
  | { kind: "formulas"; heading: string; items: { label: string; formula: string; note?: string }[] }
  | { kind: "table"; heading: string; columns: string[]; rows: string[][] }
  | { kind: "trap"; heading: string; items: string[] };

export interface CheatSheet {
  unitId: number;
  section: SectionId;
  unit: string;
  summary: string;
  blocks: Block[];
}

export type SectionId = "bio-biochem" | "chem-phys" | "psych-soc" | "cars";

export interface SectionMeta {
  id: SectionId;
  name: string;
  short: string;
  blurb: string;
  accent: string;
  tint: string;
  prop: "flask" | "cell" | "brain" | "book";
}

export const SECTIONS: SectionMeta[] = [
  {
    id: "bio-biochem",
    name: "Biology & Biochemistry",
    short: "Bio / Biochem",
    blurb: "Nine units, from amino acids to microbes.",
    accent: "#5b7a64",
    tint: "#e5ece3",
    prop: "cell",
  },
  {
    id: "chem-phys",
    name: "Chemistry & Physics",
    short: "Chem / Phys",
    blurb: "Eight units, from pKa to circuits.",
    accent: "#245574",
    tint: "#e6edf1",
    prop: "flask",
  },
  {
    id: "psych-soc",
    name: "Psychology & Sociology",
    short: "Psych / Soc",
    blurb: "Eight units, from conditioning to statistics.",
    accent: "#a8324a",
    tint: "#f2e4e4",
    prop: "brain",
  },
  {
    id: "cars",
    name: "Critical Analysis & Reasoning",
    short: "CARS",
    blurb: "Three units. No content to memorise, only method.",
    accent: "#987740",
    tint: "#f1eadc",
    prop: "book",
  },
];

export function sectionMeta(id: string): SectionMeta | undefined {
  return SECTIONS.find(section => section.id === id);
}

export const CHEAT_SHEETS: CheatSheet[] = [
  {
    unitId: 10,
    section: "chem-phys",
    unit: "Acid-Base Chemistry",
    summary:
      "One constant holds the whole topic together: Kw = [H⁺][OH⁻] = 1.0 × 10⁻¹⁴ at 25 °C. Everything else is a logarithm of it.",
    blocks: [
      {
        kind: "formulas",
        heading: "The equations",
        items: [
          { label: "pH", formula: "pH = −log[H⁺]", note: "and [H⁺] = 10⁻ᵖᴴ" },
          { label: "Water", formula: "pH + pOH = 14.00", note: "at 25 °C only" },
          { label: "Henderson–Hasselbalch", formula: "pH = pKₐ + log([A⁻]/[HA])", note: "buffer is strongest when pH = pKₐ" },
          { label: "Weak acid", formula: "[H⁺] ≈ √(Kₐ · C)", note: "only when dissociation is small" },
          { label: "Percent dissociation", formula: "([H⁺] / C) × 100", note: "rises as you dilute" },
        ],
      },
      {
        kind: "list",
        heading: "Logs without a calculator",
        items: [
          "log 2 = 0.30 · log 3 = 0.48 · log 5 = 0.70 · log 7 = 0.85",
          "Split the concentration: [H⁺] = A × 10⁻ⁿ gives pH = n − log A",
          "So 4.0 × 10⁻⁵ → pH = 5 − 0.60 = 4.40",
          "A 0.30 shift in pH is always a factor of two in [H⁺]",
          "log 4 = 2 log 2, and log 5 = 1 − log 2",
        ],
      },
      {
        kind: "table",
        heading: "Strong acids and bases — know them on sight",
        columns: ["Strong acids", "Strong bases"],
        rows: [
          ["HCl, HBr, HI", "NaOH, KOH, LiOH"],
          ["HNO₃, HClO₄, HClO₃", "Ca(OH)₂, Ba(OH)₂, Sr(OH)₂"],
          ["H₂SO₄ (first proton only)", "Group II hydroxides give TWO OH⁻"],
        ],
      },
      {
        kind: "list",
        heading: "Buffers",
        items: [
          "A buffer is a weak acid and its conjugate base in comparable amounts",
          "Capacity is greatest when [A⁻] = [HA], which is where pH = pKₐ",
          "Useful range is roughly pKₐ ± 1",
          "Blood: carbonic acid / bicarbonate, pKₐ 6.1, held at pH 7.40",
          "Adding strong acid converts A⁻ → HA; strong base does the reverse",
        ],
      },
      {
        kind: "list",
        heading: "Titration landmarks",
        items: [
          "Half-equivalence: pH = pKₐ. This is how a titration curve hands you the pKₐ for free",
          "Equivalence of a WEAK acid with strong base: pH > 7, because the conjugate base is left over",
          "Equivalence of a strong acid with strong base: pH = 7",
          "Equivalence of a weak base with strong acid: pH < 7",
          "Polyprotic acids show one buffer region and one equivalence point per proton",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Neutral means [H⁺] = [OH⁻], which is pH 7 only at 25 °C. At body temperature it is about 6.81",
          "Low pH does not mean strong acid — a concentrated weak acid beats a dilute strong one",
          "A 10⁻⁸ M strong acid is not pH 8. Water still supplies ~10⁻⁷, so the pH sits just below 7",
          "Ba(OH)₂ releases two OH⁻ per formula unit; forgetting the 2 costs the whole question",
          "pH can be negative or above 14 in concentrated solutions",
        ],
      },
    ],
  },
  {
    unitId: 2,
    section: "bio-biochem",
    unit: "Enzymes",
    summary:
      "Enzymes lower activation energy and change nothing else. They do not shift equilibrium, and they are not consumed.",
    blocks: [
      {
        kind: "formulas",
        heading: "Kinetics",
        items: [
          { label: "Michaelis–Menten", formula: "v = (Vₘₐₓ · [S]) / (Kₘ + [S])" },
          { label: "At v = ½Vₘₐₓ", formula: "[S] = Kₘ", note: "this is the definition of Kₘ" },
          { label: "Lineweaver–Burk", formula: "1/v = (Kₘ/Vₘₐₓ)(1/[S]) + 1/Vₘₐₓ", note: "y-intercept 1/Vₘₐₓ, x-intercept −1/Kₘ" },
          { label: "Catalytic efficiency", formula: "kₑₐₜ / Kₘ" },
        ],
      },
      {
        kind: "table",
        heading: "Inhibition — the table that answers the question",
        columns: ["Type", "Binds", "Vₘₐₓ", "Kₘ"],
        rows: [
          ["Competitive", "active site, free enzyme", "unchanged", "increases"],
          ["Noncompetitive", "allosteric, E or ES", "decreases", "unchanged"],
          ["Uncompetitive", "ES complex only", "decreases", "decreases"],
          ["Mixed", "allosteric, either", "decreases", "either way"],
        ],
      },
      {
        kind: "list",
        heading: "Reading the graphs",
        items: [
          "Competitive inhibition is outcompeted by more substrate, so Vₘₐₓ is reachable",
          "On Lineweaver–Burk, lines crossing on the y-axis means competitive",
          "Lines crossing on the x-axis means noncompetitive",
          "Parallel lines means uncompetitive",
          "A low Kₘ means high affinity. The number is a concentration, so smaller is tighter",
        ],
      },
      {
        kind: "list",
        heading: "Regulation",
        items: [
          "Allosteric regulators bind away from the active site and change its shape",
          "Cooperativity gives a sigmoidal curve, not hyperbolic — haemoglobin, not myoglobin",
          "Feedback inhibition: the end product shuts off an upstream enzyme",
          "Covalent modification: phosphorylation by kinases, removal by phosphatases",
          "Zymogens are inactive precursors activated by cleavage — pepsinogen, trypsinogen, the clotting cascade",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Enzymes do not change ΔG or Kₑq. They change only how fast equilibrium is reached",
          "Saturation is about occupied active sites, not about running out of substrate",
          "Denaturation is loss of structure, not of the peptide bonds",
          "Optimal pH is enzyme-specific: pepsin works at pH 2, most cytosolic enzymes near 7.4",
        ],
      },
    ],
  },
  {
    unitId: 8,
    section: "bio-biochem",
    unit: "Immunology",
    summary:
      "Two systems: innate responds fast and the same way every time; adaptive is slow the first time and fast forever after.",
    blocks: [
      {
        kind: "table",
        heading: "Innate against adaptive",
        columns: ["", "Innate", "Adaptive"],
        rows: [
          ["Speed", "minutes to hours", "days on first exposure"],
          ["Specificity", "pattern recognition", "one antigen"],
          ["Memory", "none", "yes — the basis of vaccination"],
          ["Cells", "macrophage, neutrophil, NK, dendritic", "B and T lymphocytes"],
          ["Molecules", "complement, cytokines, lysozyme", "antibodies, T-cell receptors"],
        ],
      },
      {
        kind: "list",
        heading: "The cells you must be able to name",
        items: [
          "Macrophage — phagocytoses, then presents antigen on MHC II",
          "Dendritic cell — the bridge: innate sensor, best antigen presenter",
          "Helper T (CD4) — reads MHC II, coordinates everything else",
          "Cytotoxic T (CD8) — reads MHC I, kills infected and tumour cells",
          "B cell — makes antibody; becomes a plasma cell or a memory cell",
          "NK cell — kills cells showing too LITTLE MHC I, which is how viruses hide",
        ],
      },
      {
        kind: "list",
        heading: "MHC, the part people reverse",
        items: [
          "MHC I is on every nucleated cell and presents from INSIDE the cell — read by CD8",
          "MHC II is only on antigen-presenting cells and presents from OUTSIDE — read by CD4",
          "Mnemonic: CD8 × MHC I = 8, CD4 × MHC II = 8",
        ],
      },
      {
        kind: "list",
        heading: "Antibodies",
        items: [
          "IgM — first to appear, pentamer, best complement activator",
          "IgG — most abundant, crosses the placenta, drives the secondary response",
          "IgA — mucosal surfaces, breast milk, dimer",
          "IgE — allergy and parasites, binds mast cells",
          "IgD — B-cell receptor, function still poorly understood",
          "Variable region binds antigen; constant region decides what happens next",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Active immunity means your own cells responded; passive means antibodies were handed to you and there is no memory",
          "The secondary response is faster AND larger, and it is mostly IgG",
          "Autoimmunity is failed self-tolerance; allergy is an IgE response to something harmless",
          "HIV destroys CD4 cells, which is why infections that need coordination run unchecked",
        ],
      },
    ],
  },
  {
    unitId: 25,
    section: "psych-soc",
    unit: "Research Methods & Statistics",
    summary:
      "Almost every passage question reduces to two things: what design is this, and what does that design let you claim?",
    blocks: [
      {
        kind: "table",
        heading: "Name the design",
        columns: ["Design", "Starts at", "Yields", "Signature weakness"],
        rows: [
          ["Experiment", "random assignment", "causation", "artificial setting"],
          ["Quasi-experiment", "assigned, not randomly", "strong association", "pre-existing group differences"],
          ["Cohort", "the exposure", "relative risk, incidence", "loss to follow-up"],
          ["Case-control", "the outcome", "odds ratio only", "recall bias"],
          ["Cross-sectional", "one moment", "prevalence", "no temporal order"],
        ],
      },
      {
        kind: "list",
        heading: "The distinctions that get tested",
        items: [
          "Random SAMPLING buys external validity. Random ASSIGNMENT buys internal validity. Only the second licenses a causal claim",
          "A confound must affect the outcome AND vary with the groups. Held constant, it is merely extraneous",
          "A variable on the causal path is a mediator, not a confound — adjusting for it erases the real effect",
          "Reliability is consistency; validity is accuracy. Reliable and wrong is entirely possible",
        ],
      },
      {
        kind: "formulas",
        heading: "The numbers",
        items: [
          { label: "Empirical rule", formula: "68% · 95% · 99.7%", note: "within 1, 2 and 3 SD" },
          { label: "Standard error", formula: "SEM = SD / √N", note: "precision of the mean, not spread of people" },
          { label: "Type I error", formula: "probability = α", note: "false positive, “I cried wolf”" },
          { label: "Type II error", formula: "probability = β", note: "power = 1 − β, conventionally 0.80" },
        ],
      },
      {
        kind: "list",
        heading: "Skew in one line",
        items: [
          "The mean is always dragged toward the long tail; the mode sits at the peak",
          "Right skew: mean > median > mode. Left skew: mean < median < mode",
          "A mean well above a median is the signature of a right tail — which is why income is quoted as a median",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "A p-value is the probability of the data given the null, NOT the probability the null is true",
          "Failing to reject the null does not prove it",
          "Only a larger sample reduces both error types; tightening α just trades one for the other",
          "A 99% confidence interval is WIDER than a 95% one — more confidence means casting a wider net",
          "Overlapping SEM bars do mean p is well above 0.05, but bars that merely fail to overlap are not yet significant",
        ],
      },
    ],
  },
  {
    unitId: 26,
    section: "cars",
    unit: "Reading Strategy",
    summary:
      "CARS tests nothing you can revise. Every answer is in the passage, and the winning skill is reading for structure rather than for facts.",
    blocks: [
      {
        kind: "list",
        heading: "What to track while reading",
        items: [
          "The author's OPINION, and where it changes. Most questions hang off this",
          "Tone words: however, admittedly, yet, surprisingly — these mark the turns",
          "The function of each paragraph, not its content. “Concedes a point” beats memorising the example",
          "Who is speaking: the author, or a view the author is describing in order to attack it",
        ],
      },
      {
        kind: "list",
        heading: "Pacing",
        items: [
          "90 minutes, 9 passages, 53 questions — about 10 minutes a passage including its questions",
          "Set checkpoints: passage 3 done by minute 30, passage 6 by minute 60",
          "Never leave a blank. There is no penalty for a wrong answer",
          "A passage you hate is worth the same as one you enjoy. Do not spend double on it out of pride",
        ],
      },
      {
        kind: "trap",
        heading: "Why strong readers still lose points",
        items: [
          "Bringing outside knowledge. If it is true in the world but not in the passage, it is wrong",
          "Choosing the answer that is true but does not answer the question asked",
          "Extreme language — always, never, proves — is usually wrong, though not automatically",
          "Re-reading the whole passage instead of the lines the question points to",
        ],
      },
    ],
  },
  {
    unitId: 27,
    section: "cars",
    unit: "Question Types & Approach",
    summary:
      "Three families. Naming the family tells you how much of the passage you are allowed to use.",
    blocks: [
      {
        kind: "table",
        heading: "The three families",
        columns: ["Family", "Asks", "How to answer"],
        rows: [
          ["Foundations of comprehension", "what it says", "stay inside the text"],
          ["Reasoning within the text", "why it says it", "use structure and tone"],
          ["Reasoning beyond the text", "what if", "apply the author's logic to something new"],
        ],
      },
      {
        kind: "list",
        heading: "Method",
        items: [
          "Answer in your head before reading the options. This is the single highest-yield habit",
          "Eliminate rather than select — three wrong answers are easier to spot than one right one",
          "For “the author would most likely agree”, find the sentence that licenses it",
          "For strengthen and weaken, ask what the author's argument NEEDS to be true",
          "For analogy questions, strip the content and keep the relationship",
        ],
      },
      {
        kind: "trap",
        heading: "The four wrong-answer shapes",
        items: [
          "Too extreme — right idea, overstated",
          "Half right — the first clause is true, the second is not. Read to the end of every option",
          "Out of scope — plausible, never mentioned",
          "Opposite — reverses the author's stance, and catches tired readers",
        ],
      },
    ],
  },
  {
    unitId: 28,
    section: "cars",
    unit: "Passage Genres & Practice",
    summary:
      "The genre changes the texture, not the method. Humanities passages argue; social science passages describe and then interpret.",
    blocks: [
      {
        kind: "list",
        heading: "What each genre does",
        items: [
          "Philosophy — dense, abstract, built on definitions. Slow down on the definitions and the rest follows",
          "Literary criticism — an argument about a work, with heavy tone. Track who is being praised and who is being dismissed",
          "History — a thesis about causes, usually against an older thesis. Find the author's opponent",
          "Social science — study, finding, interpretation. The author's view is usually in the last paragraph",
          "Art and music criticism — reads like opinion because it is. Separate description from judgement",
        ],
      },
      {
        kind: "list",
        heading: "Practising so it counts",
        items: [
          "Review wrong answers longer than you spend doing the passage",
          "For every miss, name the wrong-answer shape you fell for — patterns show up within a week",
          "Timed from the start. Untimed CARS practice builds a habit you cannot use on test day",
          "One or two passages daily beats nine passages on a Sunday",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Deciding a passage is “about” its subject matter rather than its argument",
          "Letting a familiar topic make you careless — your knowledge is not the author's claim",
          "Letting an unfamiliar topic rush you. Difficulty of vocabulary is not difficulty of reasoning",
        ],
      },
    ],
  },
];

/** Every unit, so the index can show what exists and what is still to come. */
export const UNITS: { id: number; section: SectionId; number: number; title: string }[] = [
  { id: 1, section: "bio-biochem", number: 1, title: "Biochemistry Foundations" },
  { id: 2, section: "bio-biochem", number: 2, title: "Enzymes" },
  { id: 3, section: "bio-biochem", number: 3, title: "Cellular Metabolism" },
  { id: 4, section: "bio-biochem", number: 4, title: "Molecular Biology" },
  { id: 5, section: "bio-biochem", number: 5, title: "Genetics" },
  { id: 6, section: "bio-biochem", number: 6, title: "Cell Biology" },
  { id: 7, section: "bio-biochem", number: 7, title: "Physiology" },
  { id: 8, section: "bio-biochem", number: 8, title: "Immunology" },
  { id: 9, section: "bio-biochem", number: 9, title: "Microbiology" },
  { id: 10, section: "chem-phys", number: 1, title: "Acid-Base Chemistry" },
  { id: 11, section: "chem-phys", number: 2, title: "Thermodynamics & Kinetics" },
  { id: 12, section: "chem-phys", number: 3, title: "Solutions & Equilibrium" },
  { id: 13, section: "chem-phys", number: 4, title: "Organic Chemistry" },
  { id: 14, section: "chem-phys", number: 5, title: "Electrochemistry" },
  { id: 15, section: "chem-phys", number: 6, title: "Mechanics" },
  { id: 16, section: "chem-phys", number: 7, title: "Fluids, Waves & Optics" },
  { id: 17, section: "chem-phys", number: 8, title: "Electricity & Magnetism" },
  { id: 18, section: "psych-soc", number: 1, title: "Learning & Conditioning" },
  { id: 19, section: "psych-soc", number: 2, title: "Cognition & Memory" },
  { id: 20, section: "psych-soc", number: 3, title: "Sensation & Perception" },
  { id: 21, section: "psych-soc", number: 4, title: "Emotion, Motivation, Personality" },
  { id: 22, section: "psych-soc", number: 5, title: "Psychological Disorders" },
  { id: 23, section: "psych-soc", number: 6, title: "Social Psychology" },
  { id: 24, section: "psych-soc", number: 7, title: "Sociology & Demographics" },
  { id: 25, section: "psych-soc", number: 8, title: "Research Methods & Statistics" },
  { id: 26, section: "cars", number: 1, title: "Reading Strategy" },
  { id: 27, section: "cars", number: 2, title: "Question Types & Approach" },
  { id: 28, section: "cars", number: 3, title: "Passage Genres & Practice" },
];

export function unitsFor(section: string) {
  return UNITS.filter(unit => unit.section === section).sort((a, b) => a.number - b.number);
}

export function sheetsFor(section: string): CheatSheet[] {
  return CHEAT_SHEETS.filter(sheet => sheet.section === section);
}

export function sheetFor(section: string, unitId: number): CheatSheet | undefined {
  return CHEAT_SHEETS.find(sheet => sheet.section === section && sheet.unitId === unitId);
}
