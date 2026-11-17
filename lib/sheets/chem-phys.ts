import type { CheatSheet } from "./types";

export const CHEM_PHYS: CheatSheet[] = [
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
    unitId: 11,
    section: "chem-phys",
    unit: "Thermodynamics & Kinetics",
    summary:
      "Thermodynamics says whether a reaction can happen. Kinetics says whether it will happen in your lifetime. They answer different questions and are tested on the difference.",
    blocks: [
      {
        kind: "formulas",
        heading: "The equations",
        items: [
          { label: "Gibbs free energy", formula: "ΔG = ΔH − TΔS", note: "negative means spontaneous" },
          { label: "At equilibrium", formula: "ΔG° = −RT ln K", note: "K > 1 means ΔG° is negative" },
          { label: "First law", formula: "ΔU = q − w" },
          { label: "Arrhenius", formula: "k = Ae^(−Eₐ/RT)", note: "raising T raises k steeply" },
          { label: "Hess's law", formula: "ΔH is path independent", note: "add the steps" },
        ],
      },
      {
        kind: "table",
        heading: "Spontaneity by sign",
        columns: ["ΔH", "ΔS", "Spontaneous?"],
        rows: [
          ["negative", "positive", "always"],
          ["positive", "negative", "never"],
          ["negative", "negative", "only at low temperature"],
          ["positive", "positive", "only at high temperature"],
        ],
      },
      {
        kind: "list",
        heading: "Kinetics",
        items: [
          "Rate depends on the slowest step, the rate-determining step",
          "Rate law comes from experiment, not from the balanced equation",
          "A catalyst lowers Eₐ for forward and reverse equally, so K is unchanged",
          "Raising temperature speeds everything up by giving more molecules enough energy",
          "Zero order: rate is constant. First order: rate ∝ [A], and the half-life is constant",
        ],
      },
      {
        kind: "list",
        heading: "Reading an energy diagram",
        items: [
          "The hump is the activation energy; the top of it is the transition state",
          "Difference between start and end heights is ΔH",
          "A transition state cannot be isolated; an intermediate sits in a dip and can be",
          "Exothermic diagrams end lower than they start",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Spontaneous does not mean fast. Diamond turning to graphite is spontaneous and will not happen today",
          "A catalyst changes the rate, never the equilibrium position or ΔG",
          "ΔG° is at standard conditions; ΔG is where the reaction actually is. Only ΔG decides direction right now",
          "Entropy is not disorder in the tidy-room sense — it is the number of ways the energy can be arranged",
        ],
      },
    ],
  },
  {
    unitId: 12,
    section: "chem-phys",
    unit: "Solutions & Equilibrium",
    summary:
      "Le Châtelier answers most equilibrium questions in one sentence: push the system and it shifts to undo what you did.",
    blocks: [
      {
        kind: "formulas",
        heading: "The equations",
        items: [
          { label: "Equilibrium constant", formula: "K = [products]/[reactants]", note: "each raised to its coefficient" },
          { label: "Reaction quotient", formula: "Q vs K", note: "Q < K shifts right, Q > K shifts left" },
          { label: "Solubility product", formula: "Kₛₚ = [A⁺]ᵐ[B⁻]ⁿ" },
          { label: "Molarity", formula: "M = mol solute / L solution" },
          { label: "Dilution", formula: "M₁V₁ = M₂V₂" },
        ],
      },
      {
        kind: "table",
        heading: "Le Châtelier, applied",
        columns: ["Change", "Shift"],
        rows: [
          ["add reactant", "toward products"],
          ["remove product", "toward products"],
          ["increase pressure", "toward fewer moles of gas"],
          ["raise temperature", "toward the endothermic side"],
          ["add a catalyst", "no shift at all"],
          ["add inert gas at constant volume", "no shift"],
        ],
      },
      {
        kind: "list",
        heading: "Solubility",
        items: [
          "Common ion effect: adding a shared ion pushes the salt out of solution",
          "Most salts dissolve better hot; gases dissolve better cold and under pressure",
          "All nitrates, all group I salts and all ammonium salts are soluble — worth memorising",
          "A larger Kₛₚ means more soluble, but only compare directly when the formulas have the same ion ratio",
        ],
      },
      {
        kind: "list",
        heading: "Colligative properties — count particles, not identity",
        items: [
          "Boiling point rises, freezing point falls, osmotic pressure rises, vapour pressure falls",
          "NaCl gives two particles per formula unit, CaCl₂ gives three. That factor is everything",
          "This is why salt melts ice and why IV fluids must match blood osmolarity",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Pure solids and pure liquids never appear in K. Their concentration does not change",
          "Temperature is the only thing that changes the value of K. Everything else just shifts the position",
          "Adding inert gas at constant VOLUME changes nothing; at constant PRESSURE it behaves like expansion",
          "Equilibrium means the rates are equal, not the concentrations",
        ],
      },
    ],
  },
  {
    unitId: 13,
    section: "chem-phys",
    unit: "Organic Chemistry",
    summary:
      "The MCAT tests organic chemistry as pattern recognition, not synthesis. Know the functional groups, the few mechanisms, and how to read a spectrum.",
    blocks: [
      {
        kind: "table",
        heading: "Functional groups by reactivity",
        columns: ["Group", "Looks like", "Note"],
        rows: [
          ["Carboxylic acid", "–COOH", "most oxidised; acidic"],
          ["Ester", "–COOR", "from acid + alcohol"],
          ["Amide", "–CONH₂", "least reactive; the peptide bond"],
          ["Aldehyde", "–CHO", "oxidises easily to acid"],
          ["Ketone", "R–CO–R", "cannot oxidise further"],
          ["Alcohol", "–OH", "hydrogen bonds; high boiling point"],
        ],
      },
      {
        kind: "table",
        heading: "SN1, SN2, E1, E2",
        columns: ["", "SN1", "SN2"],
        rows: [
          ["Steps", "two, carbocation", "one, concerted"],
          ["Substrate", "tertiary", "methyl or primary"],
          ["Stereochemistry", "racemises", "inverts — Walden inversion"],
          ["Rate", "depends on substrate only", "depends on both"],
          ["Solvent", "polar protic", "polar aprotic"],
        ],
      },
      {
        kind: "list",
        heading: "Stereochemistry",
        items: [
          "A chiral centre has four different groups attached",
          "Enantiomers are non-superimposable mirror images; identical physical properties except optical rotation",
          "Diastereomers differ at some but not all centres, and have different physical properties",
          "Maximum stereoisomers = 2ⁿ for n chiral centres",
          "A meso compound has chiral centres and an internal mirror plane, so it is achiral overall",
        ],
      },
      {
        kind: "list",
        heading: "Spectroscopy, the fast version",
        items: [
          "IR: broad peak at 3300 is an O–H; sharp strong peak at 1700 is a C=O. Those two answer most IR questions",
          "NMR: number of signals is the number of distinct hydrogen environments",
          "Integration gives how many hydrogens; splitting is n+1 for n neighbours",
          "Downfield means deshielded — next to electronegative atoms",
          "Mass spec: the molecular ion is the whole molecule; an M+2 peak of similar height means bromine",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "SN2 is blocked by bulk. Tertiary carbons do not do SN2, no matter how good the nucleophile",
          "A racemic mixture shows no optical rotation — the two rotations cancel",
          "Aldehydes oxidise, ketones do not. That is the whole basis of Tollens and Benedict's tests",
          "Resonance structures are not real alternating forms; the real molecule is the average of all of them",
        ],
      },
    ],
  },
  {
    unitId: 14,
    section: "chem-phys",
    unit: "Electrochemistry",
    summary:
      "Oxidation is loss, reduction is gain. Get the signs of the cell right and the rest follows mechanically.",
    blocks: [
      {
        kind: "formulas",
        heading: "The equations",
        items: [
          { label: "Cell potential", formula: "E°cell = E°cathode − E°anode" },
          { label: "Free energy", formula: "ΔG° = −nFE°", note: "positive E means spontaneous" },
          { label: "Nernst", formula: "E = E° − (RT/nF) ln Q", note: "potential falls as the cell discharges" },
          { label: "Faraday's constant", formula: "F ≈ 96,485 C/mol e⁻" },
        ],
      },
      {
        kind: "table",
        heading: "The two cell types",
        columns: ["", "Galvanic (voltaic)", "Electrolytic"],
        rows: [
          ["Spontaneous?", "yes", "no, needs a power supply"],
          ["E°cell", "positive", "negative"],
          ["ΔG", "negative", "positive"],
          ["Anode charge", "negative", "positive"],
          ["Example", "a battery", "electroplating"],
        ],
      },
      {
        kind: "list",
        heading: "Rules that never change",
        items: [
          "Oxidation always happens at the anode, reduction always at the cathode. In both cell types",
          "An Ox, Red Cat — anode oxidation, cathode reduction",
          "Electrons flow from anode to cathode through the wire, in both cell types",
          "Only the CHARGE of the electrodes flips between cell types, not the chemistry",
          "The salt bridge keeps charge balanced so the cell does not stall",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Reduction potentials do not get multiplied when you scale the half-reaction. Potential is intensive",
          "A dead battery is a cell at equilibrium, where E = 0 and Q = K",
          "The strongest oxidising agent is the one with the most POSITIVE reduction potential — it is the one being reduced",
          "n in both ΔG and Nernst is moles of electrons, not moles of reactant",
        ],
      },
    ],
  },
  {
    unitId: 15,
    section: "chem-phys",
    unit: "Mechanics",
    summary:
      "Draw the free-body diagram. Nearly every mechanics question that goes wrong goes wrong because a force was missed or pointed the wrong way.",
    blocks: [
      {
        kind: "formulas",
        heading: "The equations",
        items: [
          { label: "Newton's second law", formula: "F = ma" },
          { label: "Kinematics", formula: "v = v₀ + at", note: "and x = v₀t + ½at²" },
          { label: "No-time kinematic", formula: "v² = v₀² + 2ax", note: "the one to reach for when t is unknown" },
          { label: "Work", formula: "W = Fd cosθ" },
          { label: "Kinetic energy", formula: "KE = ½mv²", note: "PE = mgh" },
          { label: "Momentum", formula: "p = mv", note: "impulse = FΔt = Δp" },
        ],
      },
      {
        kind: "list",
        heading: "Conservation, and when it applies",
        items: [
          "Momentum is conserved in every collision, elastic or not",
          "Kinetic energy is conserved only in elastic collisions",
          "Perfectly inelastic means they stick together and lose the most kinetic energy possible",
          "Mechanical energy is conserved when only conservative forces act. Friction breaks it",
        ],
      },
      {
        kind: "list",
        heading: "Circular motion and torque",
        items: [
          "Centripetal acceleration = v²/r, always pointing toward the centre",
          "There is no outward force. What feels like one is inertia",
          "Torque = rF sinθ. Longer lever arm, more torque",
          "Static equilibrium means both net force and net torque are zero",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Normal force does not always equal mg — not on an incline, not in a lift, not with an extra push",
          "Work done by a force perpendicular to motion is zero, which is why centripetal force does no work",
          "Mass does not change with location; weight does",
          "At the top of projectile motion the vertical velocity is zero but the acceleration is still g",
        ],
      },
    ],
  },
  {
    unitId: 16,
    section: "chem-phys",
    unit: "Fluids, Waves & Optics",
    summary:
      "Fluids conserve volume and energy. Waves carry energy, not matter. Optics is two equations and a strict sign convention.",
    blocks: [
      {
        kind: "formulas",
        heading: "Fluids",
        items: [
          { label: "Pressure with depth", formula: "P = P₀ + ρgh" },
          { label: "Buoyant force", formula: "Fᵇ = ρ_fluid · V_displaced · g" },
          { label: "Continuity", formula: "A₁v₁ = A₂v₂", note: "narrower means faster" },
          { label: "Bernoulli", formula: "P + ½ρv² + ρgh = constant", note: "faster flow means lower pressure" },
        ],
      },
      {
        kind: "formulas",
        heading: "Waves and optics",
        items: [
          { label: "Wave speed", formula: "v = fλ" },
          { label: "Thin lens / mirror", formula: "1/f = 1/dₒ + 1/dᵢ" },
          { label: "Magnification", formula: "m = −dᵢ/dₒ", note: "negative m means inverted and real" },
          { label: "Snell's law", formula: "n₁sinθ₁ = n₂sinθ₂" },
        ],
      },
      {
        kind: "table",
        heading: "The sign convention that decides the answer",
        columns: ["Quantity", "Positive means"],
        rows: [
          ["f", "converging: convex lens, concave mirror"],
          ["f negative", "diverging: concave lens, convex mirror"],
          ["dᵢ positive", "real image, inverted"],
          ["dᵢ negative", "virtual image, upright"],
          ["|m| > 1", "enlarged"],
        ],
      },
      {
        kind: "list",
        heading: "Sound and the Doppler effect",
        items: [
          "Approaching source means higher observed frequency; receding means lower",
          "Sound travels fastest in solids and slowest in gases — the opposite of light",
          "Intensity falls with the square of distance",
          "Decibels are logarithmic: every 10 dB is ten times the intensity",
          "Beats occur at the difference of two frequencies",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "A floating object displaces its own WEIGHT; a submerged one displaces its own VOLUME",
          "Bernoulli says fast flow is low pressure, which feels backwards and is heavily tested",
          "Total internal reflection only happens going from higher n to lower n",
          "A diverging lens always gives a virtual, upright, reduced image. No exceptions worth worrying about",
        ],
      },
    ],
  },
  {
    unitId: 17,
    section: "chem-phys",
    unit: "Electricity & Magnetism",
    summary:
      "Charges make fields, fields push charges, and moving charges make magnetism. Circuits are bookkeeping once you know series from parallel.",
    blocks: [
      {
        kind: "formulas",
        heading: "The equations",
        items: [
          { label: "Coulomb's law", formula: "F = kq₁q₂/r²", note: "inverse square, like gravity" },
          { label: "Electric field", formula: "E = F/q = kQ/r²" },
          { label: "Ohm's law", formula: "V = IR" },
          { label: "Power", formula: "P = IV = I²R = V²/R" },
          { label: "Capacitance", formula: "C = Q/V", note: "energy = ½CV²" },
        ],
      },
      {
        kind: "table",
        heading: "Series against parallel",
        columns: ["", "Series", "Parallel"],
        rows: [
          ["Current", "same through each", "splits"],
          ["Voltage", "divides", "same across each"],
          ["Resistors", "Rₜ = R₁ + R₂", "1/Rₜ = 1/R₁ + 1/R₂"],
          ["Capacitors", "1/Cₜ = 1/C₁ + 1/C₂", "Cₜ = C₁ + C₂"],
        ],
      },
      {
        kind: "list",
        heading: "Fields and potential",
        items: [
          "Field lines leave positive charges and enter negative ones",
          "Potential is a scalar, so add the numbers; field is a vector, so add the arrows",
          "Equipotential lines are perpendicular to field lines, and no work is done moving along them",
          "Inside a conductor at equilibrium the field is zero — this is why a car is safe in lightning",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Resistors and capacitors combine by OPPOSITE rules. Mixing them up is the most common error in this unit",
          "Adding a resistor in parallel LOWERS total resistance, because you have added another path",
          "A magnetic force on a moving charge is always perpendicular to its velocity, so it does no work and only changes direction",
          "Conventional current flows opposite to the electrons",
        ],
      },
    ],
  },
];
