import type { CheatSheet } from "./types";

export const PSYCH_SOC: CheatSheet[] = [
  {
    unitId: 18,
    section: "psych-soc",
    unit: "Learning & Conditioning",
    summary:
      "Classical conditioning is about what a stimulus predicts. Operant conditioning is about what a behaviour produces. Decide which one first and the vocabulary falls into place.",
    blocks: [
      {
        kind: "table",
        heading: "Classical against operant",
        columns: ["", "Classical", "Operant"],
        rows: [
          ["Who", "Pavlov, Watson", "Skinner, Thorndike"],
          ["Behaviour", "involuntary, reflexive", "voluntary"],
          ["Learning", "stimulus predicts stimulus", "behaviour produces consequence"],
          ["Order", "stimulus comes first", "behaviour comes first"],
        ],
      },
      {
        kind: "table",
        heading: "The operant four-box",
        columns: ["", "Add something", "Remove something"],
        rows: [
          ["Increase behaviour", "positive reinforcement", "negative reinforcement"],
          ["Decrease behaviour", "positive punishment", "negative punishment"],
        ],
      },
      {
        kind: "list",
        heading: "Schedules of reinforcement",
        items: [
          "Fixed ratio — after a set number of responses. Fast, with a pause after each reward",
          "Variable ratio — after an unpredictable number. Highest and steadiest rate; this is gambling",
          "Fixed interval — after a set time. A scalloped pattern, slow then rushed",
          "Variable interval — unpredictable time. Slow and very steady",
          "Variable schedules resist extinction best, because the absence of a reward means nothing new",
        ],
      },
      {
        kind: "list",
        heading: "The other terms",
        items: [
          "Acquisition, extinction, spontaneous recovery — extinction suppresses, it does not erase",
          "Generalisation responds to similar stimuli; discrimination tells them apart",
          "Shaping rewards successive approximations",
          "Observational learning — Bandura's Bobo doll; learning without doing",
          "Latent learning is learned but not shown until there is a reason to show it",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Negative reinforcement is not punishment. It REMOVES something unpleasant and INCREASES the behaviour — taking a painkiller is the classic case",
          "Positive and negative mean add and remove, not good and bad",
          "In classical conditioning the learner is passive; if the subject is doing something to get an outcome, it is operant",
          "A reinforcer is defined by its effect, not by whether it sounds pleasant",
        ],
      },
    ],
  },
  {
    unitId: 19,
    section: "psych-soc",
    unit: "Cognition & Memory",
    summary:
      "Memory is three stages — encoding, storage, retrieval — and almost every memory question is really asking which stage failed.",
    blocks: [
      {
        kind: "list",
        heading: "The stores",
        items: [
          "Sensory memory — under a second; iconic for sight, echoic for sound",
          "Short-term / working memory — about 7 ± 2 items, 15 to 30 seconds without rehearsal",
          "Long-term — effectively unlimited",
          "Working memory has parts: phonological loop, visuospatial sketchpad, central executive",
          "Chunking beats the 7 ± 2 limit by making each item bigger",
        ],
      },
      {
        kind: "table",
        heading: "Long-term memory types",
        columns: ["Type", "Also called", "Example"],
        rows: [
          ["Explicit", "declarative", "facts and events"],
          ["— Semantic", "", "the capital of France"],
          ["— Episodic", "", "your last birthday"],
          ["Implicit", "non-declarative", "skills and conditioning"],
          ["— Procedural", "", "riding a bike"],
        ],
      },
      {
        kind: "list",
        heading: "What helps and what hurts",
        items: [
          "Deeper processing remembers better: meaning beats sound beats appearance",
          "Spacing beats cramming; the testing effect beats re-reading",
          "Context and state dependence — recall is better in the same place and mood",
          "Serial position: the first items survive by rehearsal, the last by recency",
          "Proactive interference is old blocking new; retroactive is new blocking old",
        ],
      },
      {
        kind: "list",
        heading: "Biology and failure",
        items: [
          "Hippocampus forms new explicit memories; patient H.M. could not after its removal",
          "Amygdala attaches emotion; cerebellum holds procedural memory",
          "Anterograde amnesia cannot form new memories; retrograde has lost old ones",
          "Alzheimer's begins with the hippocampus, which is why recent memory goes first",
          "Memory is reconstructive, so it can be distorted by suggestion — Loftus's work on misinformation",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Recognition is easier than recall — which is why re-reading feels like learning and is not",
          "A flashbulb memory is vivid and confidently held, and no more accurate than any other",
          "Retrieval failure is not the same as the memory being gone",
          "Procedural memory usually survives damage that destroys explicit memory",
        ],
      },
    ],
  },
  {
    unitId: 20,
    section: "psych-soc",
    unit: "Sensation & Perception",
    summary:
      "Sensation is detection, perception is interpretation. The exam tests where one becomes the other.",
    blocks: [
      {
        kind: "formulas",
        heading: "Thresholds",
        items: [
          { label: "Absolute threshold", formula: "detected 50% of the time" },
          { label: "Weber's law", formula: "ΔI / I = constant", note: "the just-noticeable difference is a proportion, not an amount" },
          { label: "Signal detection", formula: "hit · miss · false alarm · correct rejection", note: "separates sensitivity from willingness to say yes" },
        ],
      },
      {
        kind: "list",
        heading: "Vision",
        items: [
          "Path: cornea → pupil → lens → retina → optic nerve → thalamus (LGN) → occipital lobe",
          "Rods see in dim light, no colour, mostly peripheral. Cones need light, see colour, concentrated in the fovea",
          "Trichromatic theory explains the receptors; opponent-process explains afterimages. Both are right, at different stages",
          "Feature detectors in the visual cortex respond to edges and movement — Hubel and Wiesel",
        ],
      },
      {
        kind: "list",
        heading: "Hearing and the others",
        items: [
          "Path: pinna → eardrum → ossicles → oval window → cochlea → hair cells → auditory nerve → temporal lobe",
          "Place theory explains high frequencies, frequency theory low ones",
          "Vestibular system is balance: semicircular canals for rotation, otoliths for linear motion",
          "Only smell reaches the cortex without passing through the thalamus first",
        ],
      },
      {
        kind: "list",
        heading: "Perceptual organisation",
        items: [
          "Gestalt principles: proximity, similarity, continuity, closure, figure-ground",
          "Bottom-up starts with the data; top-down starts with expectation",
          "Binocular depth cues: retinal disparity, convergence. Monocular: relative size, interposition, texture gradient",
          "Constancies keep size, shape and colour stable as the image on the retina changes",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Weber's law is about proportion: adding 1 kg is obvious at 2 kg and imperceptible at 100 kg",
          "Dark adaptation is mostly rods, and takes far longer than light adaptation",
          "Sensory adaptation is the receptor responding less; habituation is the brain attending less",
          "Signal detection theory exists because a 'miss' and a 'false alarm' are different errors with different costs",
        ],
      },
    ],
  },
  {
    unitId: 21,
    section: "psych-soc",
    unit: "Emotion, Motivation, Personality",
    summary:
      "Three theory-heavy topics. The exam wants you to name the theory from a description, so learn the distinguishing feature of each rather than the whole model.",
    blocks: [
      {
        kind: "table",
        heading: "Theories of emotion — the order of events",
        columns: ["Theory", "Sequence"],
        rows: [
          ["James–Lange", "stimulus → body → emotion (I am afraid because I tremble)"],
          ["Cannon–Bard", "stimulus → body and emotion at once"],
          ["Schachter–Singer", "body + a label for it → emotion"],
          ["Lazarus", "appraisal comes first, then emotion"],
        ],
      },
      {
        kind: "list",
        heading: "Motivation",
        items: [
          "Drive reduction — a need creates tension, behaviour reduces it; built around homeostasis",
          "Arousal theory — we seek an optimal level. Yerkes–Dodson: moderate arousal is best, and simpler tasks tolerate more",
          "Maslow's hierarchy — physiological, safety, love, esteem, self-actualisation",
          "Self-determination theory — autonomy, competence, relatedness",
          "Intrinsic motivation can be damaged by paying for something already enjoyed: the overjustification effect",
        ],
      },
      {
        kind: "list",
        heading: "Personality",
        items: [
          "Psychoanalytic — Freud: id, ego, superego, and defence mechanisms",
          "Humanistic — Rogers and Maslow: unconditional positive regard, self-concept",
          "Trait — the Big Five, OCEAN: openness, conscientiousness, extraversion, agreeableness, neuroticism",
          "Social-cognitive — Bandura: reciprocal determinism between person, behaviour and environment",
          "Biological — temperament and heritability",
        ],
      },
      {
        kind: "list",
        heading: "Defence mechanisms worth recognising",
        items: [
          "Repression — pushing it out of awareness",
          "Projection — attributing your own feeling to someone else",
          "Displacement — redirecting at a safer target",
          "Rationalisation — inventing an acceptable reason",
          "Reaction formation — behaving as the opposite of what you feel",
          "Sublimation — channelling into something productive; the only one considered healthy",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "James–Lange is body FIRST. If the description has the physical response causing the feeling, that is the one",
          "Conscientiousness, not intelligence, is the Big Five trait that best predicts job performance",
          "Displacement redirects at a substitute target; projection puts your feeling into another person. They are often confused",
          "Self-actualisation in Maslow is the top of the hierarchy, not a synonym for happiness",
        ],
      },
    ],
  },
  {
    unitId: 22,
    section: "psych-soc",
    unit: "Psychological Disorders",
    summary:
      "Know the category, the hallmark symptom, and the duration criterion. The exam distinguishes disorders mostly by time course.",
    blocks: [
      {
        kind: "table",
        heading: "Duration is the usual tiebreaker",
        columns: ["Disorder", "Hallmark", "Duration"],
        rows: [
          ["Major depressive episode", "low mood or anhedonia", "2 weeks"],
          ["Manic episode", "elevated mood, reduced sleep need", "1 week"],
          ["Hypomanic episode", "same but milder, no impairment", "4 days"],
          ["Schizophrenia", "psychosis", "6 months"],
          ["PTSD", "re-experiencing after trauma", "over 1 month"],
          ["Generalised anxiety", "uncontrollable worry", "6 months"],
        ],
      },
      {
        kind: "list",
        heading: "Schizophrenia",
        items: [
          "Positive symptoms are additions: hallucinations, delusions, disorganised speech",
          "Negative symptoms are absences: flat affect, avolition, alogia",
          "Dopamine hypothesis: too much dopamine in the mesolimbic pathway",
          "Antipsychotics block D₂ receptors; they help positive symptoms far more than negative ones",
        ],
      },
      {
        kind: "list",
        heading: "The main categories",
        items: [
          "Depressive — major depressive disorder, persistent depressive disorder",
          "Bipolar — I requires a manic episode, II requires hypomania plus depression",
          "Anxiety — generalised, panic, phobias, social anxiety",
          "Obsessive-compulsive — obsessions are thoughts, compulsions are the acts that relieve them",
          "Personality — Cluster A odd, Cluster B dramatic, Cluster C anxious",
        ],
      },
      {
        kind: "list",
        heading: "Biology and treatment",
        items: [
          "Depression: low serotonin, norepinephrine, dopamine. SSRIs take weeks to work despite raising serotonin in hours",
          "Anxiety: GABA is the main inhibitory transmitter; benzodiazepines enhance it",
          "Alzheimer's: acetylcholine loss, plaques and tangles",
          "Parkinson's: dopamine loss in the substantia nigra",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Bipolar I needs only a manic episode — depression is not required for the diagnosis",
          "Schizophrenia is not split personality. That is dissociative identity disorder",
          "Obsessive-compulsive personality disorder is not OCD; the personality disorder lacks the true obsessions",
          "The antidepressant delay is strong evidence that low serotonin alone cannot be the whole story",
        ],
      },
    ],
  },
  {
    unitId: 23,
    section: "psych-soc",
    unit: "Social Psychology",
    summary:
      "The recurring lesson of this unit: situations drive behaviour far more than observers assume, and our explanations are systematically biased toward blaming the person.",
    blocks: [
      {
        kind: "list",
        heading: "Attribution",
        items: [
          "Dispositional attributes to the person; situational to the circumstances",
          "Fundamental attribution error — overweighting disposition when explaining OTHERS",
          "Actor-observer bias — situational for yourself, dispositional for everyone else",
          "Self-serving bias — success is mine, failure is the world's",
          "Kelley's covariation: high consensus, high distinctiveness and low consistency point to the situation",
        ],
      },
      {
        kind: "table",
        heading: "The classic studies",
        columns: ["Study", "Showed"],
        rows: [
          ["Asch", "conformity to a visibly wrong majority"],
          ["Milgram", "obedience to authority, 65% to the maximum shock"],
          ["Zimbardo", "role adoption — though methodologically contested"],
          ["Darley & Latané", "bystander effect, diffusion of responsibility"],
          ["Sherif, Robbers Cave", "conflict from competition, resolved by shared goals"],
        ],
      },
      {
        kind: "list",
        heading: "Influence and groups",
        items: [
          "Normative influence is to be liked; informational influence is to be right",
          "Foot-in-the-door starts small; door-in-the-face starts unreasonable",
          "Social facilitation: an audience helps easy tasks and hurts hard ones",
          "Social loafing is reduced effort when individual contributions are hidden",
          "Groupthink suppresses dissent; group polarisation makes the average view more extreme",
        ],
      },
      {
        kind: "list",
        heading: "Attitudes",
        items: [
          "Cognitive dissonance — discomfort from acting against a belief, resolved by changing the belief",
          "Elaboration likelihood: central route is the argument, peripheral route is the packaging",
          "Attitudes predict behaviour best when they are specific, strongly held and personally relevant",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "The fundamental attribution error applies to how we judge OTHERS. Applied to ourselves it reverses",
          "Milgram and Stanford are taught as settled and are both methodologically contested — know the finding and the caveat",
          "Prejudice is the attitude, discrimination is the behaviour, stereotype is the belief",
          "Bystander intervention falls as the group grows, and the key variable is responsibility, not apathy",
        ],
      },
    ],
  },
  {
    unitId: 24,
    section: "psych-soc",
    unit: "Sociology & Demographics",
    summary:
      "Three lenses on every social question: functionalism asks what it does for society, conflict theory asks who benefits, symbolic interactionism asks what it means to the people in it.",
    blocks: [
      {
        kind: "table",
        heading: "The three frameworks",
        columns: ["Lens", "Asks", "Scale"],
        rows: [
          ["Functionalism", "what purpose does this serve?", "macro"],
          ["Conflict theory", "who has power, who benefits?", "macro"],
          ["Symbolic interactionism", "what does it mean to those involved?", "micro"],
          ["Social constructionism", "how did we agree this is real?", "either"],
        ],
      },
      {
        kind: "list",
        heading: "Demography — the measures",
        items: [
          "Crude birth and death rates are per 1,000 people per year",
          "Rate of natural increase = (CBR − CDR) ÷ 10, as a percentage. Divide by ten or you will report 2% as 20%",
          "Total fertility rate: children per woman. Replacement is about 2.1",
          "Infant mortality is per 1,000 LIVE BIRTHS, not per population",
          "Dependency ratio = [(under 15) + (65 and over)] ÷ (15–64) × 100",
        ],
      },
      {
        kind: "list",
        heading: "The demographic transition",
        items: [
          "Stage 1 — births and deaths both high, population flat",
          "Stage 2 — deaths fall first, population explodes. Sanitation needs no behaviour change; fertility does",
          "Stage 3 — births begin to fall as cities, schooling and contraception spread",
          "Stage 4 — both low, population stable",
          "Population momentum: growth continues for decades after fertility reaches replacement, because the large young cohorts have not reproduced yet",
        ],
      },
      {
        kind: "list",
        heading: "Stratification and institutions",
        items: [
          "Weber's three dimensions: class, status, power",
          "Cultural capital is tastes and knowledge; social capital is who you know",
          "Meritocracy is the belief that position reflects merit; social reproduction is the tendency for position to be inherited",
          "Globalisation, urbanisation and the social determinants of health run through every passage in this unit",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Prevalence ≈ incidence × duration. A long illness can be highly prevalent and rarely new",
          "Absolute mobility is movement from your parents; relative mobility is your rank among peers. A society can have lots of the first and none of the second",
          "Race is a social construct with biological consequences, because of how people are treated, not what their genes are",
          "Functionalism is not approval — describing what something does for a system is not endorsing it",
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
];
