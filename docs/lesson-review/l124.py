import sys; sys.path.insert(0,'/home/claude/dkit')
from dkit import *

d = D(1180, 880, "From a mechanism to a rate law",
      "Stoichiometry gives you the rate law for an elementary step — and for nothing else. Everything below is how to get from the steps you are given to the law you can measure.",
      "A procedure chart. A top strip states the rule that the exponents in a rate law come from the stoichiometry of an elementary step only, never from an overall balanced equation, where they must be measured. Three columns follow. Column one, the slow step is first: read the rate law straight off it. The worked case is the unimolecular ionisation of tert-butyl bromide to a carbocation, slow, followed by fast capture by the nucleophile, giving rate equals k times the concentration of the substrate, with no dependence on nucleophile concentration, which is the experimental signature of an SN1 reaction. Column two, the slow step comes later behind a fast equilibrium: write the rate law for the slow step, then substitute the intermediate out. The worked case is two molecules of nitric oxide in fast equilibrium with the dimer, followed by the slow reaction of the dimer with oxygen; the equilibrium constant equals the dimer concentration over the square of the nitric oxide concentration, so the dimer concentration is the equilibrium constant times the square of the nitric oxide concentration, and the rate becomes the observed constant times nitric oxide squared times oxygen, third order overall and matching experiment. Column three, the intermediate is not at equilibrium: apply the steady state approximation, setting the rate of change of the intermediate to zero. The worked case is enzyme plus substrate in reversible equilibrium with the enzyme substrate complex, which turns over to enzyme plus product; setting the rate of change of the complex to zero gives the complex concentration as the forward rate constant times enzyme times substrate over the sum of the reverse and catalytic rate constants, and since the velocity is the catalytic constant times the complex concentration, this is the Michaelis Menten equation with the Michaelis constant equal to the sum of the reverse and catalytic constants over the forward constant. A footer gives the three tests a proposed mechanism must pass: the steps must sum to the overall balanced equation with every intermediate cancelling, the derived rate law must match the measured one, and every step must be chemically reasonable, with termolecular steps almost never acceptable. Passing all three shows only that a mechanism is consistent with the data, never that it is correct, since more than one mechanism can give the same rate law. A second footer explains how to read the energy diagram: a mechanism with n elementary steps has n peaks, which are transition states and cannot be isolated, and n minus one valleys, which are intermediates and are real species; the rate determining step is the one with the largest climb, measured from the lowest point before it to the highest peak after it.")

d.box(24, 128, 1128, 88, "The rule everything else depends on",
      "Exponents come from the stoichiometry of an ELEMENTARY STEP — and from nothing else. For an overall balanced equation they must be measured. Writing Rate = k[A][B]² off the equation A + 2B → C is the single most common error in this topic.",
      NAVY, chars=146, size=12, head_size=13.5)

COLS = [
  (24, SAGE, "1 · THE SLOW STEP IS FIRST", "read it straight off",
   [("mechanism", None),
    ("(CH₃)₃CBr → (CH₃)₃C⁺ + Br⁻", "slow"),
    ("(CH₃)₃C⁺ + Nu⁻ → (CH₃)₃CNu", "fast"),
    ("", None),
    ("rate law", None),
    ("Rate = k[(CH₃)₃CBr]", None),
    ("", None),
    ("every species in it is a reactant,", None),
    ("so there is nothing to substitute", None)],
   "[Nu⁻] is absent — the experimental signature of Sₙ1. Doubling the nucleophile does nothing to the rate."),
  (402, BLUE, "2 · THE SLOW STEP COMES LATER", "substitute the intermediate out",
   [("mechanism", None),
    ("NO + NO ⇌ N₂O₂", "fast, K₁"),
    ("N₂O₂ + O₂ → 2 NO₂", "slow"),
    ("", None),
    ("rate law of the slow step", None),
    ("Rate = k₂[N₂O₂][O₂]", None),
    ("N₂O₂ is an intermediate — it cannot stay", None),
    ("K₁ = [N₂O₂]/[NO]²  →  [N₂O₂] = K₁[NO]²", None),
    ("Rate = k₂K₁[NO]²[O₂] = kₒᵇₛ[NO]²[O₂]", None)],
   "Third order, and it matches experiment — which is why the termolecular one-step version is not needed."),
  (780, GOLD, "3 · NO EQUILIBRIUM TO USE", "set d[intermediate]/dt = 0",
   [("mechanism", None),
    ("E + S ⇌ ES", "k₁, k₋₁"),
    ("ES → E + P", "k₂ = k_cat"),
    ("", None),
    ("steady state on ES", None),
    ("k₁[E][S] = (k₋₁ + k₂)[ES]", None),
    ("[ES] = k₁[E][S] / (k₋₁ + k₂)", None),
    ("v = k₂[ES]  →  v = Vₘₐₓ[S]/(Kₘ + [S])", None),
    ("Kₘ = (k₋₁ + k₂) / k₁", None)],
   "Use this when the intermediate is consumed about as fast as it forms, so a pre-equilibrium cannot be assumed."),
]
for x, c, head, sub, rows, foot in COLS:
    d.rect(x, 212, 376, 384, c, FILL.get(c), 12, 2)
    d.text(x+188, 240, head, color=c, weight=700, size=13)
    d.text(x+188, 260, sub, color=GREY, size=11.5)
    yy = 292
    for txt, tag in rows:
        if not txt:
            yy += 10; continue
        if txt in ("mechanism", "rate law", "rate law of the slow step", "steady state on ES"):
            d.text(x+22, yy, txt.upper(), color=GREY, size=9.5, anchor="start")
        else:
            d.text(x+22, yy, txt, color=NAVY, size=11.5, weight=700 if "Rate" in txt or "v =" in txt or "Kₘ =" in txt else 400, anchor="start")
            if tag:
                d.text(x+354, yy, tag, color=c, size=10.5, anchor="end")
        yy += 24
    d.line(x+22, 536, x+354, 536, "#d9d2c4", 1, True)
    d.lines(x+188, 556, foot, chars=46, lh=15, color=GREY, size=11)

d.rect(24, 624, 556, 112, NAVY, FILL[NAVY], 12, 2)
d.text(302, 650, "Three tests a proposed mechanism must pass", color=NAVY, weight=700, size=13)
for i, t in enumerate([
        "1 \u00b7 The steps must sum to the overall equation, every intermediate cancelling.",
        "2 \u00b7 The derived rate law must match the measured one.",
        "3 \u00b7 Every step must be chemically reasonable \u2014 a termolecular step almost never is."]):
    d.text(46, 676 + i*21, t, color=NAVY, size=11.5, anchor="start")
d.box(600, 624, 552, 112, "Reading the energy diagram",
      "n elementary steps → n peaks (transition states, not isolable) and n−1 valleys (intermediates, real species). The rate-determining step is the biggest climb: from the LOWEST point before it to the HIGHEST peak after it.",
      NAVY, chars=72, size=12, head_size=13)
d.box(24, 756, 1128, 80, "What passing all three tests does NOT mean",
      "It shows the mechanism is *consistent* with the data — never that it is correct. More than one mechanism can give the same rate law, and kinetics alone cannot choose between them; that is what isotope labelling, trapping experiments and spectroscopy are for.",
      RED, chars=142, size=12, head_size=13.5)
print(d.save("mechanism-to-rate-law"))
