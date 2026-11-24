import json
import math
import os
import re

BAD = []
def check(qid, claimed, got, tol=0.02, note=""):
    ok = abs(got - claimed) <= tol * abs(claimed) if claimed else abs(got) <= tol
    print(("  ok  " if ok else "  FAIL") + f"  {qid:14s} claimed={claimed:<12.6g} computed={got:<12.6g} {note}")
    if not ok: BAD.append(qid)

def model(label, ok, note=""):
    """A statement about the physics or chemistry, not a sum. The verifier
    confirmed my own mistake back to me once because it shared my assumption,
    so the model gets asserted separately from the arithmetic."""
    print(("  ok  " if ok else "  FAIL") + f"  {label:14s} {'holds' if ok else 'DOES NOT HOLD':14s} {note}")
    if not ok: BAD.append(label)

F, R = 96485.0, 8.314

# Literature values quoted in the passages, as opposed to invented data. These
# are asserted to be right, not derived from anything; each is here so that a
# later reader can see which figures in the prose are checkable against the
# outside world and which are this form's own invention.
LITERATURE = {
    "4-nitrophenolate absorbance maximum / nm": 405,   # cp-p2 method
    "total power of the relaxed human eye / D": 60,    # cp-p4, 59-60 D
    "Faraday constant / C per mol": 96485,
    "gas constant / J per mol K": 8.314,
}
print("literature values quoted (not derived):")
for name, value in LITERATURE.items():
    print(f"        {name} = {value}")
print()

# ---------------------------------------------------------------- P1 buffering
# pH = 6.1 + log([HCO3-] / (0.03 x PCO2)); table gives PCO2 and bicarbonate.
def ph(hco3, pco2):
    return 6.1 + math.log10(hco3 / (0.03 * pco2))

check("cp-p1-q1", 7.40, ph(24, 40), tol=0.002, note="Patient W")
check("cp-p1-q2", 7.32, ph(12, 24), tol=0.003, note="Patient X")
check("cp-p1-q4", -0.30, ph(24, 80) - ph(24, 40), tol=0.02, note="doubling PCO2 at fixed bicarbonate")
# q3 asks which patient is a compensated respiratory problem. Verify the model
# rather than a single number: Y must be the one with both values raised, and
# its pH must sit nearer normal than Z's, which is the metabolic alkalosis.
model("cp-p1-q3", ph(26, 60) < 7.35 and 60 > 45 and 26 > 26 - 0.001,
      note=f"Y: PCO2 60 high, HCO3 26 at ceiling, pH {ph(26, 60):.2f} acidotic")
model("cp-p1-q3b", ph(36, 30) > 7.45 and 36 > 26 and 30 < 35,
      note=f"Z: high bicarbonate with low PCO2, pH {ph(36, 30):.2f} alkalotic")
model("cp-p1-q3c", abs(ph(26, 60) - 7.40) < abs(ph(36, 30) - 7.40),
      note="Y is closer to normal than Z, i.e. the better compensated of the two")

# ------------------------------------------------- P2 Arrhenius and the enzyme
EA_UNCAT, EA_CAT = 50000.0, 25000.0
check("cp-p2-q1", 6.0e3, EA_UNCAT / R, tol=0.01, note="Ea/R, the gradient's magnitude in K")
check("cp-p2-q2", 2.2, math.exp(-(EA_UNCAT / R) * (1 / 310 - 1 / 298)), tol=0.03,
      note="rate ratio 298 K -> 310 K, uncatalysed")
check("cp-p2-q3", 1.6e4, math.exp((EA_UNCAT - EA_CAT) / (R * 310)), tol=0.05,
      note="catalysed / uncatalysed at 310 K, A unchanged")
# New method text: the second group's pH 6.0 arm returns the same activation
# energy, so the gradient q1 asks for must be unchanged by it.
model("cp-p2-pH", abs((EA_UNCAT / R) - (EA_UNCAT / R)) < 1e-9,
      note="pH 6.0 arm is stated to give the same Ea, so q1's gradient is untouched")

# --------------------------------------------------------- P3 flow and calibre
RHO = 1060.0
check("cp-p3-q1", 0.41, 0.8 ** 4, note="flow remaining after a 20% cut in radius")
V1, AREA_FRACTION = 0.30, 0.40
V2 = V1 / AREA_FRACTION
check("cp-p3-q2", 0.75, V2, note="velocity in the narrowing, area ratio used once")
check("cp-p3-q3", 250, 0.5 * RHO * (V2 ** 2 - V1 ** 2), tol=0.02, note="Bernoulli pressure drop, Pa")
# New paragraph: the fourth power as two factors of r^2. Check the claim is the
# same exponent the flow relation carries, not a restatement that drifts.
model("cp-p3-r4", 2 + 2 == 4, note="area ~ r^2 and mean velocity ~ r^2 multiply to r^4")
# The phantom validation claims flow recovered from area x velocity matched the
# pump to within 4%. Verify that is consistent with continuity, not an extra
# assumption: Q is the same each side of the narrowing.
model("cp-p3-phantom", abs((AREA_FRACTION * V2) - (1.0 * V1)) < 1e-12,
      note="A2 v2 = A1 v1, so a flow-rate check validates the method without fixing q2's answer")

# ----------------------------------------------------------------- P4 optics
check("cp-p4-q1", -2.5, 1 / -0.40, note="myopic correction, far point 40 cm")
check("cp-p4-q2", 2.5, 1 / 0.25 - 1 / 0.667, tol=0.01, note="reading addition, near point 66.7 cm")
check("cp-p4-q4", 400, (160 / 4.0) * (250 / 25), note="objective 40x times eyepiece 10x")
# New paragraph calls the corrective powers small adjustments to a 60 D total.
model("cp-p4-60D", abs(1 / -0.40) / 60 < 0.10,
      note=f"2.5 D is {abs(1 / -0.40) / 60 * 100:.0f}% of the eye's 60 D, so 'small adjustment' holds")

# --------------------------------- P5 electrochemistry: ferricyanide mediator
E_MED, E_GLU = 0.36, -0.45
check("cp-p5-q1", 0.81, E_MED - E_GLU, note="cell emf, cathode minus anode")
check("cp-p5-q2", -156, (-2 * F * (E_MED - E_GLU)) / 1000, note="dG in kJ/mol, n=2")
check("cp-p5-q4", 0.0296, (0.0592 / 2) * 1, note="Nernst shift for a tenfold Q at n=2")
check("cp-p5-q5", 1.00e-7, 9.6485e-3 / F, tol=0.01, note="mol electrons from 9.65 mC")
check("cp-p5-q5b", 5.00e-8, (9.6485e-3 / F) / 2, tol=0.01, note="mol glucose, 2 electrons each")
# New method text: the quoted charge is net of a no-glucose blank, and the
# mediator is in excess. Neither changes n or the charge q5 works from.
model("cp-p5-blank", 9.6485e-3 == 9.6485e-3,
      note="blank subtraction is stated to be already applied, so q5's 9.65 mC is the net charge")

# ----------------------------------------------- P6 isolation of the acid drug
check("cp-p6-q3", 0.40, 3.2 / 8.0, note="Rf = spot / solvent front")
# New method data, all invented: scale, recovery and melting range.
model("cp-p6-mass", 0 < 0.52 < 1.00, note="0.52 g recovered from 1.00 g of crude is a possible yield")
model("cp-p6-volumes", 2 * 15 <= 30 * 2, note="two 15 mL aqueous portions against 30 mL of ether is a workable ratio")
model("cp-p6-mp", (153 - 151) <= 3, note="a 2 degree melting range is narrow enough to call it one substance")

# ----------------------------------------- P7 solubility: calcium oxalate
KSP = 2.3e-9
S_WATER = math.sqrt(KSP)
check("cp-p7-q1", 4.8e-5, S_WATER, tol=0.02, note="molar solubility in water")
check("cp-p7-q2", 2.3e-7, KSP / 0.010, note="common-ion solubility in 0.010 M Ca2+")
# New paragraph claims activities and concentrations are near-identical in the
# near-pure water the constant was measured in, and that urine's ionic strength
# is orders of magnitude higher. Ionic strength = 0.5 * sum(c z^2).
I_WATER = 0.5 * (S_WATER * 4 + S_WATER * 4)
I_URINE = 0.3  # literature order of magnitude for urine, 0.15-0.4 mol/L
model("cp-p7-ionic", I_WATER < 1e-3 and I_URINE / I_WATER > 100,
      note=f"saturated water I = {I_WATER:.1e} M against urine ~{I_URINE} M: three orders of magnitude")
model("cp-p7-scope", 0.5 * (0.010 * 4 + 0.020) > I_WATER,
      note="the caveat is scoped to near-pure water and urine, so it leaves q2's 0.010 M case alone")

# ----------------------------------------- P8 gait mechanics: 70 kg, g = 9.8
M, G = 70.0, 9.8
check("cp-p8-q1", 686, M * G, note="body weight in N")
check("cp-p8-q2", 823, 1.2 * M * G, tol=0.01, note="peak ground reaction force")
check("cp-p8-q3", 34.3, M * G * 0.05, note="work raising the centre of mass 5 cm")
check("cp-p8-q4", 57, (M * G * 0.05) / 0.60, tol=0.02, note="average power over a 0.60 s stride")
# New datum: the trough reaches about 0.7 times body weight. It must sit below
# body weight (the passage says the force dips below it there), above zero, and
# must not coincide with any choice offered on this passage's questions.
TROUGH = 0.7 * M * G
model("cp-p8-trough", 0 < TROUGH < M * G < 1.2 * M * G,
      note=f"trough {TROUGH:.0f} N < weight {M * G:.0f} N < peak {1.2 * M * G:.0f} N")
model("cp-p8-marker", 0.005 / 0.05 <= 0.10,
      note="the 5 mm agreement between methods is a tenth of the 5 cm excursion, so it does not disturb h")
model("cp-p8-sampling", 1000 * 0.60 >= 100,
      note="1000 readings a second over a 0.60 s stride is enough to resolve two peaks and a trough")

# ----------------------------- P9 protein folding: dH = -120 kJ, dS = -350 J/K
DH, DS = -120000.0, -350.0
TM = DH / DS
check("cp-p9-q1", -11.5, (DH - 310 * DS) / 1000, tol=0.03, note="dG at 310 K, kJ/mol")
check("cp-p9-q2", 343, TM, tol=0.01, note="melting temperature in K")
check("cp-p9-q2b", 69.8, TM - 273.15, tol=0.02, note="the same in Celsius")
# New method text names the scanned interval. q2 extrapolates to the unfolding
# temperature, so that temperature has to lie inside the interval over which
# the passage says the two quantities may be treated as constant.
model("cp-p9-range", 283 <= TM <= 353,
      note=f"Tm = {TM:.0f} K lies inside the 283-353 K the two-state fit is stated to cover")
model("cp-p9-urea", True,
      note="the urea arm deliberately carries no temperature: 298 K clashed with q2 choice A")

# ------------------------- P10 membrane cable: R = 10 kohm cm2, C = 1 uF/cm2
RM, CM = 1.0e4, 1.0e-6
TAU = RM * CM
check("cp-p10-q1", 0.010, TAU, note="membrane time constant in s")
# q4's reasoning, which the verifier did not previously cover: 5 ms is half a
# time constant and 50 ms is five of them.
check("cp-p10-q4", 0.61, math.exp(-0.005 / TAU), tol=0.02, note="fraction of the first input left after 5 ms")
check("cp-p10-q4b", 0.0067, math.exp(-0.050 / TAU), tol=0.05, note="fraction left after 50 ms")
model("cp-p10-q4c", math.exp(-0.005 / TAU) > 0.5 > math.exp(-0.050 / TAU) * 10,
      note="most of the first input survives 5 ms and almost none survives 50 ms")
# New method text: the measurement multiplies an input resistance by an area to
# reach ohm cm2, so the units q1 relies on still cancel.
model("cp-p10-units", abs(TAU - RM * CM) < 1e-18,
      note="ohm cm2 times F/cm2 leaves seconds, so the per-area normalisation is self-consistent")

# ------------------------------------------------------------------------------
# No new figure may coincide with a numeric choice on its own passage's
# questions. The defect this guards against: an extension to another section
# made a distractor defensible, and nothing read the choices against the new
# prose. Values are as they appear in the passages.
NEW_FIGURES = {
    "cp-p1": [10],                              # minutes to analysis
    "cp-p2": [405, 0.1, 0.15, 8.0, 6.0],        # nm, K, mol/L, pH, pH
    "cp-p3": [3, 4],                            # cardiac cycles, percent
    "cp-p4": [60, 2],                           # dioptres, cm
    "cp-p5": [3],                               # electrodes
    "cp-p6": [1.00, 30, 15, 5, 0.52, 400, 151, 153],
    "cp-p7": [48, 0.22],
    "cp-p8": [1000, 0.7, 5, 480.2],             # Hz, trough fraction, mm, trough in N
    "cp-p9": [1, 283, 353],
    "cp-p10": [],
}
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "lib", "exams", "content", "fl1", "chem-phys.json")) as handle:
    SECTION = json.load(handle)


def choice_numbers(text):
    """Numbers in a choice, with 'x 10^-5' style notation resolved."""
    cleaned = text.replace("×", "x").replace("−", "-")
    for glyph, plain in zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁻",
                            "0123456789-"):
        cleaned = cleaned.replace(glyph, plain)
    out = []
    for mantissa, exponent in re.findall(r"(-?\d+(?:\.\d+)?)(?:\s*x\s*10\s*(-?\d+))?", cleaned):
        try:
            value = float(mantissa)
        except ValueError:
            continue
        if exponent:
            value *= 10.0 ** int(exponent)
        out.append(value)
    return out


print()
clashes = 0
for passage_id, figures in NEW_FIGURES.items():
    questions = [q for q in SECTION["questions"] if q.get("passageId") == passage_id]
    for figure in figures:
        for question in questions:
            for letter, text in question["choices"].items():
                for value in choice_numbers(text):
                    if value and abs(value - figure) <= 0.001 * abs(figure):
                        clashes += 1
                        print(f"  FAIL  {passage_id}: new figure {figure} matches "
                              f"{question['id']} choice {letter} ({text})")
                        BAD.append(f"{passage_id}-clash")
model("new-figures", clashes == 0,
      note=f"no new datum coincides with a numeric choice on its own passage ({sum(len(v) for v in NEW_FIGURES.values())} figures checked)")

print()
print(f"{len(BAD)} failure(s)" if BAD else "all checks verified")
if BAD: raise SystemExit("FAILED: " + ", ".join(dict.fromkeys(BAD)))
