import type { CheatSheet } from "./types";

export const BIO_BIOCHEM: CheatSheet[] = [
  {
    unitId: 1,
    section: "bio-biochem",
    unit: "Biochemistry Foundations",
    summary:
      "Twenty amino acids, four macromolecules, and one idea underneath all of it: structure decides function, and structure is decided by what the side chains want to do around water.",
    blocks: [
      {
        kind: "table",
        heading: "Amino acids worth knowing by name",
        columns: ["Group", "Members", "Why they get asked"],
        rows: [
          ["Nonpolar", "Gly, Ala, Val, Leu, Ile, Pro, Phe, Met, Trp", "bury in the protein core"],
          ["Polar", "Ser, Thr, Cys, Asn, Gln, Tyr", "hydrogen bond; Ser/Thr/Tyr get phosphorylated"],
          ["Acidic", "Asp, Glu", "negative at pH 7"],
          ["Basic", "Lys, Arg, His", "positive at pH 7; His buffers near 6"],
          ["Special", "Gly, Pro, Cys", "flexible hinge, rigid kink, disulfide bridge"],
        ],
      },
      {
        kind: "list",
        heading: "The four levels of structure",
        items: [
          "Primary — the sequence, held by peptide (covalent) bonds",
          "Secondary — alpha helix and beta sheet, held by backbone hydrogen bonds",
          "Tertiary — the 3D fold, driven by the hydrophobic effect; also disulfides, salt bridges, hydrogen bonds",
          "Quaternary — more than one chain together, like haemoglobin's four",
          "Denaturation destroys everything above primary. The sequence survives",
        ],
      },
      {
        kind: "formulas",
        heading: "Titration and charge",
        items: [
          { label: "Isoelectric point", formula: "pI = ½(pKₐ₁ + pKₐ₂)", note: "for a neutral side chain; average the two pKa values flanking the neutral species" },
          { label: "Charge rule", formula: "pH < pI → positive", note: "pH > pI → negative. At pI, net zero" },
          { label: "Henderson–Hasselbalch", formula: "pH = pKₐ + log([A⁻]/[HA])" },
        ],
      },
      {
        kind: "list",
        heading: "The other three macromolecules",
        items: [
          "Carbohydrates — (CH₂O)ₙ. Glycosidic bonds. Glycogen is the animal store, starch the plant one, cellulose the one we cannot digest",
          "Lipids — not polymers. Triglycerides store energy, phospholipids build membranes, steroids signal",
          "Nucleic acids — phosphodiester backbone, 5' to 3'. DNA is deoxy and double-stranded, RNA has 2'-OH and uracil",
          "Saturated fats pack tightly and are solid; one cis double bond kinks the chain and drops the melting point",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Hydrophobic collapse is driven by ENTROPY of water, not by attraction between the nonpolar groups",
          "Proline cannot sit inside an alpha helix — its ring removes the backbone NH that would donate the hydrogen bond",
          "A peptide bond has partial double-bond character, so it is planar and does not rotate freely",
          "Only Ser, Thr and Tyr carry the hydroxyl that kinases phosphorylate",
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
    unitId: 3,
    section: "bio-biochem",
    unit: "Cellular Metabolism",
    summary:
      "Follow the carbon and follow the electrons. Glucose is taken apart in stages, and almost all the ATP comes at the very end from a proton gradient.",
    blocks: [
      {
        kind: "table",
        heading: "The stages, in order",
        columns: ["Stage", "Where", "Per glucose", "Needs O₂?"],
        rows: [
          ["Glycolysis", "cytosol", "2 ATP, 2 NADH, 2 pyruvate", "no"],
          ["Pyruvate → acetyl-CoA", "mitochondrial matrix", "2 NADH, 2 CO₂", "yes"],
          ["Krebs cycle", "matrix", "6 NADH, 2 FADH₂, 2 GTP, 4 CO₂", "yes"],
          ["Electron transport + ATP synthase", "inner membrane", "about 26–28 ATP", "yes"],
        ],
      },
      {
        kind: "list",
        heading: "Control points — where questions live",
        items: [
          "Phosphofructokinase-1 is the rate-limiting step of glycolysis. Inhibited by ATP and citrate, activated by AMP and fructose-2,6-bisphosphate",
          "Pyruvate dehydrogenase is inhibited by its own products, acetyl-CoA and NADH",
          "Isocitrate dehydrogenase is the rate-limiting step of the Krebs cycle",
          "High energy charge shuts pathways down; high AMP turns them on",
        ],
      },
      {
        kind: "list",
        heading: "Oxidative phosphorylation",
        items: [
          "NADH enters at Complex I, FADH₂ at Complex II — which is why FADH₂ yields less ATP, it pumps at fewer sites",
          "Oxygen is the FINAL electron acceptor, reduced to water. It does not participate before that",
          "Complexes I, III and IV pump protons into the intermembrane space",
          "ATP synthase lets protons back in; the gradient, not the electrons, makes the ATP — chemiosmosis",
          "Uncouplers let protons leak back without passing through ATP synthase: the gradient collapses, electron transport speeds up, and the energy leaves as heat",
        ],
      },
      {
        kind: "list",
        heading: "Fed and fasted",
        items: [
          "Insulin is the fed signal: glycogenesis, lipogenesis, glucose uptake",
          "Glucagon and epinephrine are the fasted signals: glycogenolysis, gluconeogenesis, lipolysis",
          "Gluconeogenesis is not reverse glycolysis — it bypasses the three irreversible steps, and it costs ATP",
          "Beta-oxidation yields far more ATP per carbon than glucose, because fat is more reduced",
          "The brain cannot use fatty acids; in prolonged fasting it switches to ketone bodies",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Fermentation does not make ATP. It regenerates NAD⁺ so glycolysis can keep going",
          "The Krebs cycle does not use oxygen directly, but it stops without it because NADH has nowhere to go",
          "Substrate-level phosphorylation happens in glycolysis and Krebs; oxidative phosphorylation is separate",
          "Acetyl-CoA cannot be converted back to glucose in humans — fat does not become sugar",
        ],
      },
    ],
  },
  {
    unitId: 4,
    section: "bio-biochem",
    unit: "Molecular Biology",
    summary:
      "DNA to RNA to protein, and the ways cells decide how much of each. Direction matters everywhere: synthesis is always 5' to 3'.",
    blocks: [
      {
        kind: "list",
        heading: "Replication",
        items: [
          "Semi-conservative: each daughter keeps one old strand",
          "Helicase unwinds, primase lays an RNA primer, DNA polymerase III extends 5' to 3'",
          "Leading strand is continuous; lagging strand is Okazaki fragments, because polymerase cannot run 3' to 5'",
          "DNA polymerase I removes the primers, ligase seals the nicks",
          "Topoisomerase relieves the supercoiling ahead of the fork",
          "Telomeres shorten each round; telomerase replaces them in germ and stem cells, and in most cancers",
        ],
      },
      {
        kind: "table",
        heading: "Transcription against translation",
        columns: ["", "Transcription", "Translation"],
        rows: [
          ["Where (eukaryote)", "nucleus", "cytoplasm / rough ER"],
          ["Machine", "RNA polymerase II", "ribosome, 80S"],
          ["Template", "antisense DNA strand", "mRNA codons"],
          ["Product", "pre-mRNA", "polypeptide"],
          ["Start signal", "promoter, TATA box", "AUG, methionine"],
        ],
      },
      {
        kind: "list",
        heading: "RNA processing — eukaryotes only",
        items: [
          "5' cap, for ribosome binding and stability",
          "3' poly-A tail, for stability and export",
          "Splicing removes introns and keeps exons, done by the spliceosome",
          "Alternative splicing lets one gene make several proteins — the main reason we have far more proteins than genes",
        ],
      },
      {
        kind: "list",
        heading: "Mutations",
        items: [
          "Silent — the codon changes, the amino acid does not. Thank the degenerate third base",
          "Missense — a different amino acid. Sickle cell is one, Glu to Val",
          "Nonsense — a premature stop. Usually severe",
          "Frameshift — insertion or deletion not divisible by three. Usually catastrophic",
          "A mutation in a promoter or splice site changes nothing in the coding sequence and can still be devastating",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "The lac operon is INDUCIBLE and turns on with lactose; the trp operon is REPRESSIBLE and turns off with tryptophan",
          "mRNA is read 5' to 3', and the protein is built N-terminus to C-terminus",
          "The template strand is the antisense strand, but the mRNA matches the CODING strand with U for T",
          "Prokaryotes transcribe and translate at once; eukaryotes cannot, the nuclear membrane is in the way",
        ],
      },
    ],
  },
  {
    unitId: 5,
    section: "bio-biochem",
    unit: "Genetics",
    summary:
      "Most of this unit is one skill: set up the cross correctly, then count. The rest is knowing which inheritance pattern a pedigree is showing.",
    blocks: [
      {
        kind: "formulas",
        heading: "The maths",
        items: [
          { label: "Monohybrid cross", formula: "Aa × Aa → 3:1", note: "genotypes 1:2:1" },
          { label: "Dihybrid cross", formula: "AaBb × AaBb → 9:3:3:1", note: "only if the genes are unlinked" },
          { label: "Hardy–Weinberg", formula: "p + q = 1 and p² + 2pq + q² = 1", note: "2pq is the carrier frequency" },
          { label: "Recombination", formula: "1% recombinants = 1 map unit", note: "more crossing over means further apart" },
        ],
      },
      {
        kind: "table",
        heading: "Reading a pedigree",
        columns: ["Pattern", "Tell-tale sign"],
        rows: [
          ["Autosomal dominant", "every affected child has an affected parent; no skipping"],
          ["Autosomal recessive", "skips generations; unaffected parents have affected children"],
          ["X-linked recessive", "mostly males; never father to son; affected males come from carrier mothers"],
          ["X-linked dominant", "affected fathers pass it to ALL daughters and no sons"],
          ["Mitochondrial", "mother passes it to every child; fathers pass it to none"],
        ],
      },
      {
        kind: "list",
        heading: "Beyond simple dominance",
        items: [
          "Incomplete dominance — the heterozygote is a blend, red and white give pink",
          "Codominance — both show fully, as in AB blood type",
          "Epistasis — one gene masks another entirely",
          "Pleiotropy — one gene affects many traits",
          "Penetrance is whether the phenotype appears at all; expressivity is how strongly",
        ],
      },
      {
        kind: "list",
        heading: "Meiosis, and where variation comes from",
        items: [
          "Crossing over in prophase I",
          "Independent assortment in metaphase I",
          "Random fertilisation",
          "Nondisjunction gives aneuploidy — trisomy 21 is the usual example",
          "Meiosis I separates homologues; meiosis II separates sister chromatids",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Hardy–Weinberg q² is the frequency of the recessive PHENOTYPE; q is the allele frequency. Take the square root first",
          "“Carrier frequency” is 2pq, not q",
          "Dominant does not mean common or advantageous. It only describes which allele is expressed",
          "A 9:3:3:1 ratio collapses if the genes are linked — check before you use it",
        ],
      },
    ],
  },
  {
    unitId: 6,
    section: "bio-biochem",
    unit: "Cell Biology",
    summary:
      "Organelles are compartments with jobs, the membrane is a selective barrier, and the cytoskeleton is what moves everything around.",
    blocks: [
      {
        kind: "table",
        heading: "Organelles, one line each",
        columns: ["Organelle", "Job"],
        rows: [
          ["Rough ER", "protein synthesis for export and membranes"],
          ["Smooth ER", "lipid synthesis, detoxification, calcium store"],
          ["Golgi", "modifies, sorts and ships; adds sugars"],
          ["Lysosome", "acid hydrolases, pH about 4.8, digests waste"],
          ["Peroxisome", "breaks down very long fatty acids and H₂O₂"],
          ["Mitochondrion", "ATP; own circular DNA, maternally inherited"],
        ],
      },
      {
        kind: "list",
        heading: "Membrane transport",
        items: [
          "Simple diffusion — small and nonpolar, down the gradient, no protein, no ATP",
          "Facilitated diffusion — down the gradient, through a protein, still no ATP",
          "Primary active transport — against the gradient, ATP directly. The Na⁺/K⁺ pump moves 3 Na⁺ out for 2 K⁺ in",
          "Secondary active transport — against the gradient, powered by someone else's gradient",
          "Osmosis is water moving toward the higher solute concentration",
        ],
      },
      {
        kind: "list",
        heading: "Cytoskeleton and junctions",
        items: [
          "Microfilaments (actin) — thinnest, muscle contraction, cytokinesis cleavage furrow",
          "Intermediate filaments — structural, keratin, the most stable",
          "Microtubules (tubulin) — thickest, the mitotic spindle, cilia and flagella in a 9+2 arrangement",
          "Tight junctions seal, desmosomes rivet, gap junctions let small molecules pass",
        ],
      },
      {
        kind: "list",
        heading: "The cell cycle",
        items: [
          "G₁ → S (DNA copied) → G₂ → M. G₀ is a resting exit",
          "Checkpoints at G₁/S, G₂/M and the spindle checkpoint",
          "p53 halts the cycle for repair; lose it and damaged cells divide. It is the most commonly mutated gene in cancer",
          "Apoptosis is programmed and tidy; necrosis is damage, and it inflames",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Hypertonic means the SOLUTION has more solute, so the cell shrinks. Hypotonic makes it swell",
          "The Na⁺/K⁺ pump is electrogenic — unequal charge movement is why it contributes to the membrane potential",
          "Cholesterol does not simply make membranes more fluid; it buffers them, resisting change in both directions",
          "Prokaryotic ribosomes are 70S and eukaryotic 80S — which is exactly why some antibiotics are safe for us",
        ],
      },
    ],
  },
  {
    unitId: 7,
    section: "bio-biochem",
    unit: "Physiology",
    summary:
      "Every system here is a loop holding something steady. Find the sensor, the set point and the effector, and most questions answer themselves.",
    blocks: [
      {
        kind: "list",
        heading: "Cardiovascular",
        items: [
          "Path: body → vena cava → right atrium → right ventricle → lungs → left atrium → left ventricle → aorta",
          "Cardiac output = heart rate × stroke volume",
          "SA node sets the pace; AV node delays so the atria finish first",
          "Starling's law: more filling stretches the ventricle and it contracts harder",
          "Arteries have the highest pressure, capillaries the greatest total cross-sectional area and the slowest flow",
        ],
      },
      {
        kind: "list",
        heading: "Respiratory",
        items: [
          "Inhalation is active: the diaphragm contracts and flattens, lowering thoracic pressure. Quiet exhalation is passive",
          "The main drive to breathe is rising CO₂, detected as falling pH, not falling O₂",
          "Haemoglobin is cooperative, giving the sigmoid curve",
          "Right shift means less affinity and more unloading: higher CO₂, lower pH, higher temperature, more 2,3-BPG — all the signs of hard-working tissue",
        ],
      },
      {
        kind: "list",
        heading: "Renal",
        items: [
          "Filter at the glomerulus, reabsorb what you want, secrete what you do not, excrete the rest",
          "Proximal tubule reabsorbs the bulk: glucose, amino acids, most sodium and water",
          "Descending loop is permeable to water only; ascending limb to salt only. That is what builds the medullary gradient",
          "Aldosterone retains sodium and water; ADH retains water alone",
          "Renin–angiotensin–aldosterone raises blood pressure; ANP from a stretched atrium lowers it",
        ],
      },
      {
        kind: "table",
        heading: "Hormones that keep coming up",
        columns: ["Hormone", "From", "Does"],
        rows: [
          ["Insulin / glucagon", "pancreas", "lowers / raises blood glucose"],
          ["Cortisol", "adrenal cortex", "stress, raises glucose, suppresses immunity"],
          ["Epinephrine", "adrenal medulla", "fight or flight, fast"],
          ["Thyroid hormone", "thyroid", "sets metabolic rate"],
          ["ADH", "posterior pituitary", "water retention"],
          ["Parathyroid hormone", "parathyroid", "raises blood calcium"],
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Negative feedback is the default. Positive feedback is rare and worth memorising: oxytocin in labour, the clotting cascade, the action potential upstroke",
          "Steroid hormones are lipid-soluble and bind receptors inside the cell, changing transcription — slow but lasting. Peptide hormones act at the surface through second messengers — fast and brief",
          "The posterior pituitary does not make its hormones; it stores what the hypothalamus made",
          "A right shift on the oxygen curve helps tissues, it does not harm them",
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
    unitId: 9,
    section: "bio-biochem",
    unit: "Microbiology",
    summary:
      "Bacteria are cells and can be killed selectively. Viruses are not cells, which is exactly why they are hard to treat.",
    blocks: [
      {
        kind: "table",
        heading: "Gram positive against gram negative",
        columns: ["", "Gram positive", "Gram negative"],
        rows: [
          ["Stain", "purple", "pink"],
          ["Peptidoglycan", "thick", "thin"],
          ["Outer membrane", "none", "yes, with LPS"],
          ["Toxin", "exotoxin, secreted protein", "endotoxin is Lipid A, released on lysis"],
          ["Drug access", "easier", "outer membrane blocks vancomycin"],
        ],
      },
      {
        kind: "list",
        heading: "Bacterial genetics",
        items: [
          "Binary fission — asexual, so variation has to come from elsewhere",
          "Transformation — picking up naked DNA from the environment",
          "Transduction — a bacteriophage carries DNA between cells",
          "Conjugation — the sex pilus and a plasmid. This is how resistance spreads fastest",
          "Transposons jump within a genome",
        ],
      },
      {
        kind: "list",
        heading: "Viruses",
        items: [
          "Not alive by most definitions: no metabolism, no ribosomes, cannot replicate alone",
          "Lytic cycle bursts the cell; lysogenic integrates and waits",
          "Retroviruses carry reverse transcriptase, turning RNA into DNA — the reverse of the usual flow",
          "Enveloped viruses steal host membrane on the way out and are easier to kill with soap",
          "Prions are protein alone and cause disease by making normal proteins misfold",
        ],
      },
      {
        kind: "list",
        heading: "How antibiotics choose their target",
        items: [
          "Cell wall — beta-lactams and vancomycin. We have no peptidoglycan, so this is the safest target",
          "70S ribosome — aminoglycosides and tetracyclines at 30S, macrolides at 50S. Ours is 80S",
          "DNA gyrase — fluoroquinolones",
          "Folate synthesis — sulfonamides and trimethoprim. Bacteria make folate; we eat it",
        ],
      },
      {
        kind: "trap",
        heading: "Where points are lost",
        items: [
          "Antibiotics do nothing to viruses. There is no peptidoglycan, no 70S ribosome and no folate pathway to attack",
          "Endotoxin is released when the bacterium dies, which is why killing a lot of gram-negatives at once can make a patient briefly worse",
          "Resistance is selected for, not caused by the drug. The mutants were already there",
          "Gram-negative does not mean less dangerous — it means a different set of defences",
        ],
      },
    ],
  },
];
