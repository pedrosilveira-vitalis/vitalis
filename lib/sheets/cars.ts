import type { CheatSheet } from "./types";

export const CARS: CheatSheet[] = [
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
    summary: "Three families. Naming the family tells you how much of the passage you are allowed to use.",
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
