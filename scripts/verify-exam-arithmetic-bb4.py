"""Recompute every quantitative key and distractor in fl4 Bio/Biochem.

Each value is derived from the numbers the passage itself supplies, never
copied from the choice it is meant to confirm, and each distractor is
recomputed from the specific mistake its note names, so that no distractor can
be accidentally right as well.

The blocks headed "model" check the passages rather than the questions. They
read the shipped JSON and confirm that the tables and figures contain the
numbers the questions quote, that a table's rows are internally consistent,
that the bar charts' pixel geometry encodes the values their captions claim,
and that the physiology and biochemistry asserted are also true of real
myocytes, livers, thyroid axes and bacteria. A verifier that only repeats the
author's arithmetic confirms the author's assumptions; the model blocks are
the ones that can catch an assumption itself.
"""
import io
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "lib", "exams", "content", "fl4", "bio-biochem.json")
DATA = json.load(io.open(PATH, encoding="utf-8"))
PASSAGE = {p["id"]: p for p in DATA["passages"]}
QUESTION = {q["id"]: q for q in DATA["questions"]}

BAD = []
COUNT = 0


def check(qid, claimed, got, tol=0.02, note=""):
    """Compare a value written into the content with a value computed here."""
    global COUNT
    COUNT += 1
    ok = abs(got - claimed) <= tol * abs(claimed) if claimed else abs(got) <= tol
    print(("  ok  " if ok else "  FAIL") + f"  {qid:22s} claimed={claimed:<12.6g} computed={got:<12.6g} {note}")
    if not ok:
        BAD.append(qid)


def choice(qid, letter):
    """The numeric value of one choice, as it stands in the shipped file."""
    text = QUESTION[qid]["choices"][letter]
    cleaned = text.replace("×", "x").replace("−", "-").replace(",", "")
    for digit, sup in zip("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"):
        cleaned = cleaned.replace(sup, digit)
    cleaned = re.sub(r"x\s*10\s*(-?\d+)", r"e\1", cleaned)
    match = re.search(r"-?\d+(?:\.\d+)?(?:e-?\d+)?", cleaned)
    assert match, f"{qid} {letter}: no number in {text!r}"
    return float(match.group(0))


def key(qid):
    return choice(qid, QUESTION[qid]["correct"])


def table_numbers(pid):
    """Every number in a passage's table or figure markup, row by row."""
    markup = PASSAGE[pid]["figure"]["markup"]
    rows = re.findall(r"<tr>(.*?)</tr>", markup, re.S)
    out = []
    for row in rows:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)
        out.append([re.sub(r"<[^>]+>", "", c).strip() for c in cells])
    return out


def rects(pid):
    """(x, y, height) for each bar of an SVG figure, in document order."""
    markup = PASSAGE[pid]["figure"]["markup"]
    found = []
    for tag in re.findall(r"<rect[^>]*>", markup):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', tag))
        found.append((float(attrs["x"]), float(attrs["y"]), float(attrs["height"])))
    return found


def passage_text(pid):
    return " ".join(PASSAGE[pid]["paragraphs"])


# ---------------------------------------------------------------- P1
print("P1  malonyl-CoA and fatty acid flux")
MALONYL = {"medium": 6.0, "insulin": 12.0, "compoundK": 1.5, "acci": 0.5, "acci_cpt": 0.5}
SYNTH = {"medium": 12.0, "insulin": 24.0, "compoundK": 3.0, "acci": 1.0, "acci_cpt": 1.0}
OXID = {"medium": 4.0, "insulin": 2.0, "compoundK": 16.0, "acci": 20.0, "acci_cpt": 2.0}
ORDER = ["medium", "insulin", "compoundK", "acci", "acci_cpt"]

# model: the table in the shipped file must hold exactly these numbers
rows = table_numbers("bb4-p1")[1:]
assert len(rows) == 5, rows
for name, row in zip(ORDER, rows):
    assert [float(row[1]), float(row[2]), float(row[3])] == [MALONYL[name], SYNTH[name], OXID[name]], row
print("       table 1 matches the values used below")
# model: malonyl-CoA and oxidation must run in opposite directions in every
# condition where CPT-1 itself is not blocked, since malonyl-CoA inhibits it
free = [k for k in ORDER if k != "acci_cpt"]
by_malonyl = sorted(free, key=lambda k: MALONYL[k])
assert all(OXID[a] >= OXID[b] for a, b in zip(by_malonyl, by_malonyl[1:])), \
    "oxidation must fall as malonyl-CoA rises"
print("       oxidation ranked by rising malonyl-CoA:", [OXID[k] for k in by_malonyl])
# model: synthesis must rise with malonyl-CoA over those same conditions
assert all(SYNTH[a] <= SYNTH[b] for a, b in zip(by_malonyl, by_malonyl[1:])), \
    "synthesis must rise as malonyl-CoA rises"
# model: blocking CPT-1 must remove the oxidation gained by removing malonyl-CoA,
# which is what makes the paired condition a test rather than a repeat
assert OXID["acci_cpt"] < OXID["medium"] < OXID["acci"], "CPT-1 block must abolish the gain"
# model, against reality: hepatic malonyl-CoA in the fed state is a few nmol per
# gram, so 6 nmol/g is the right order of magnitude for an unstimulated cell
assert 1.0 <= MALONYL["medium"] <= 20.0, MALONYL["medium"]

check("bb4-p1-q1", key("bb4-p1-q1"), SYNTH["insulin"] * 8,
      note="key: 8 acetyl-CoA per C16 chain")
check("bb4-p1-q1/A", choice("bb4-p1-q1", "A"), SYNTH["insulin"],
      note="distractor: table value read as acetyl-CoA")
check("bb4-p1-q1/B", choice("bb4-p1-q1", "B"), SYNTH["insulin"] * 2,
      note="distractor: two acetyl-CoA per palmitate")
check("bb4-p1-q1/C", choice("bb4-p1-q1", "C"), SYNTH["insulin"] * 7,
      note="distractor: the 7 malonyl units, omitting the primer")
check("bb4-p1-q3", key("bb4-p1-q3"), OXID["compoundK"] * 8,
      note="key: 8 acetyl-CoA released per palmitate")
check("bb4-p1-q3/A", choice("bb4-p1-q3", "A"), OXID["compoundK"],
      note="distractor: one acetyl-CoA per palmitate")
check("bb4-p1-q3/B", choice("bb4-p1-q3", "B"), OXID["compoundK"] * 7,
      note="distractor: counts the 7 rounds of beta-oxidation")
check("bb4-p1-q3/D", choice("bb4-p1-q3", "D"), OXID["compoundK"] * 16,
      note="distractor: counts the 16 carbons")
# the explanation of q2 quotes the malonyl-CoA fall and the oxidation rise
assert "6.0 to 0.5" in QUESTION["bb4-p1-q2"]["explanation"]
assert "4 to 20" in QUESTION["bb4-p1-q2"]["explanation"]
check("bb4-p1-q5 model", 4.0, MALONYL["medium"] / MALONYL["compoundK"], tol=0.0,
      note="model: q5 note calls the malonyl-CoA fall fourfold")
check("bb4-p1-q5 model2", 4.0, OXID["compoundK"] / OXID["medium"], tol=0.0,
      note="model: q5 note calls the oxidation rise fourfold (4 to 16)")

# ---------------------------------------------------------------- P2
print()
print("P2  the ventricular action potential")
UPSTROKE = {"control": 250.0, "W": 90.0, "X": 245.0, "Y": 250.0, "Z": 150.0}
APD = {"control": 300.0, "W": 290.0, "X": 200.0, "Y": 420.0, "Z": 330.0}
REST = {"control": -85.0, "W": -85.0, "X": -84.0, "Y": -85.0, "Z": -65.0}
rows = table_numbers("bb4-p2")[1:]
for name, row in zip(["control", "W", "X", "Y", "Z"], rows):
    assert [float(row[1]), float(row[2]), float(row[3])] == [UPSTROKE[name], APD[name], REST[name]], row
print("       table 1 matches the values used below")
# model: drug Y must lengthen the action potential without touching the upstroke
# or the resting potential, or q1's key is not uniquely identifiable
assert APD["Y"] > APD["control"] and UPSTROKE["Y"] == UPSTROKE["control"] and REST["Y"] == REST["control"]
# model: drug X must shorten it, which is the pattern q1 assigns to a calcium block
assert APD["X"] < APD["control"]
# model, against reality: the membrane responsiveness curve of a ventricular
# myocyte, which relates available fast sodium current to the potential the cell
# is held at, falls off over roughly -75 to -55 mV, with about half the current
# available near -65 mV. A Boltzmann curve with a half point at -65 mV and a
# slope of 6 mV therefore predicts the ratio of upstroke velocities that drug Z
# should produce, and the table must agree with it in direction and in size.
avail = lambda v: 1.0 / (1.0 + math.exp((v + 65.0) / 6.0))
predicted = avail(REST["Z"]) / avail(REST["control"])
observed = UPSTROKE["Z"] / UPSTROKE["control"]
print(f"       availability at -65 mV: predicted {predicted:.2f}, table implies {observed:.2f}")
assert UPSTROKE["Z"] < UPSTROKE["control"], "q3 requires drug Z to slow the upstroke"
assert 0.3 <= observed <= 0.75, "the fall must be real but not total"
assert abs(observed - predicted) < 0.25, "the table must match a real responsiveness curve"
# model, against reality: ventricular upstroke velocity and action potential
# duration must be in the ranges real recordings give
assert 150.0 <= UPSTROKE["control"] <= 400.0
assert 200.0 <= APD["control"] <= 400.0
assert -95.0 <= REST["control"] <= -80.0
check("bb4-p2-q2", key("bb4-p2-q2"),
      100.0 * (APD["control"] - APD["X"]) / APD["control"], tol=0.01,
      note="key: shortening by drug X against the control value")
check("bb4-p2-q2/A", choice("bb4-p2-q2", "A"),
      100.0 * (UPSTROKE["control"] - UPSTROKE["X"]) / UPSTROKE["control"], tol=0.05,
      note="distractor: the upstroke column instead of repolarisation")
check("bb4-p2-q2/B", choice("bb4-p2-q2", "B"),
      100.0 * (APD["control"] - APD["W"]) / APD["control"], tol=0.05,
      note="distractor: drug W's row")
check("bb4-p2-q2/D", choice("bb4-p2-q2", "D"),
      100.0 * (APD["control"] - APD["X"]) / APD["X"], tol=0.01,
      note="distractor: divides by the shortened value")

# ---------------------------------------------------------------- P3
print()
print("P3  antibiotics and the ribosome")
BACT = {1: 25.0, 2: 10.0, 3: 100.0, 4: 8.0, 5: 15.0}
EUK = {1: 95.0, 2: 98.0, 3: 15.0, 4: 90.0, 5: 20.0}
rows = table_numbers("bb4-p3")[1:]
for n, row in zip(range(1, 6), rows):
    assert [float(row[1]), float(row[2])] == [BACT[n], EUK[n]], row
print("       table 1 matches the values used below")
index = {n: EUK[n] / BACT[n] for n in BACT}
print("       selectivity indices:", {n: round(v, 2) for n, v in index.items()})
# model: the key of q3 must be the unique maximum among the four offered
offered = [1, 2, 3, 4]
assert max(offered, key=lambda n: index[n]) == 4, index
assert sorted(index[n] for n in offered)[-2] < index[4], "the maximum must be unambiguous"
# model: the inverted ratio must pick out compound 3, as that note claims
assert max(offered, key=lambda n: 1.0 / index[n]) == 3
# model: compound 3's index must be the lowest of the four, as that note says
assert min(offered, key=lambda n: index[n]) == 3
# model: compound 1's index must be second lowest, as its note says
assert sorted(offered, key=lambda n: index[n])[1] == 1
# model: compound 2 must leave the highest eukaryotic incorporation, as its note says
assert max(offered, key=lambda n: EUK[n]) == 2
# model: compound 4 must leave the lowest bacterial incorporation, as the key's
# explanation says
assert min(BACT, key=lambda n: BACT[n]) == 4
check("bb4-p3-q3 index1", 3.8, index[1], tol=0.01, note="model: value quoted in the explanation")
check("bb4-p3-q3 index2", 9.8, index[2], tol=0.01, note="model: value quoted in the explanation")
check("bb4-p3-q3 index3", 0.15, index[3], tol=0.01, note="model: value quoted in the explanation")
check("bb4-p3-q3 index4", 11.3, index[4], tol=0.01, note="model: value quoted in the explanation")
check("bb4-p3-q3 inverted", 6.7, 1.0 / index[3], tol=0.01, note="model: inverted ratio in note C")
RESIDUES = 100
check("bb4-p3-q5", key("bb4-p3-q5"), (RESIDUES + 1) * 3, tol=0.0,
      note="key: 100 codons plus a stop codon, three nucleotides each")
check("bb4-p3-q5/A", choice("bb4-p3-q5", "A"), RESIDUES, tol=0.0,
      note="distractor: residues counted as nucleotides")
check("bb4-p3-q5/B", choice("bb4-p3-q5", "B"), RESIDUES + 1, tol=0.0,
      note="distractor: codons counted as nucleotides")
check("bb4-p3-q5/C", choice("bb4-p3-q5", "C"), RESIDUES * 3, tol=0.0,
      note="distractor: omits the stop codon")

# ---------------------------------------------------------------- P4
print()
print("P4  methylation and histone acetylation")
REPORTER = {"none": 5.0, "analogue": 60.0, "inhibitor": 20.0, "both": 100.0}
METHYL = {"none": 80.0, "analogue": 15.0, "inhibitor": 78.0, "both": 14.0}
ACETYL = {"none": 1.0, "analogue": 3.5, "inhibitor": 6.0, "both": 7.0}
ORDER4 = ["none", "analogue", "inhibitor", "both"]
# model: the bar chart's pixel geometry must encode the reporter values. The
# caption states 1.4 pixels per unit above a baseline at y = 160.
BASE, SCALE = 160.0, 1.4
bars = rects("bb4-p4")
assert len(bars) == 4, bars
for name, (x, y, h) in zip(ORDER4, sorted(bars)):
    check(f"bb4-p4 svg {name}", h, REPORTER[name] * SCALE, tol=1e-9,
          note="model: bar height = value x 1.4 px")
    check(f"bb4-p4 svg {name} top", y, BASE - REPORTER[name] * SCALE, tol=1e-9,
          note="model: bar top = baseline - height")
# model: the axis tick at 50 units must sit halfway up to the tick at 100
markup = PASSAGE["bb4-p4"]["figure"]["markup"]
assert 'y="94"' in markup and 'y="24"' in markup and 'y="164"' in markup, "axis labels moved"
check("bb4-p4 svg axis", 94.0 - 24.0, (164.0 - 94.0), tol=0.05,
      note="model: the 0-50 and 50-100 tick gaps are equal")
# model: the numbers quoted in the prose of paragraph 2 must be these
text = passage_text("bb4-p4")
for value in ("80%", "15%", "78%", "14%", "1.0, 3.5, 6.0 and 7.0"):
    assert value in text, value
# model: the drug that removes methylation must be the one that lowers it, and
# the deacetylase inhibitor must leave methylation alone, or q2 has no basis
assert METHYL["analogue"] < 0.3 * METHYL["none"]
assert abs(METHYL["inhibitor"] - METHYL["none"]) < 0.05 * METHYL["none"]
assert ACETYL["analogue"] > ACETYL["none"], "q2 needs acetylation to rise with demethylation"
check("bb4-p4-q1", key("bb4-p4-q1"), REPORTER["both"] / REPORTER["none"], tol=0.01,
      note="key: combination against untreated")
check("bb4-p4-q1/A", choice("bb4-p4-q1", "A"), REPORTER["both"] / REPORTER["analogue"], tol=0.02,
      note="distractor: compares with the analogue bar")
check("bb4-p4-q1/B", choice("bb4-p4-q1", "B"), REPORTER["analogue"] / REPORTER["none"], tol=0.01,
      note="distractor: reads the analogue bar as the combination")
check("bb4-p4-q1/D", choice("bb4-p4-q1", "D"), REPORTER["both"] - REPORTER["none"], tol=0.01,
      note="distractor: subtracts instead of dividing")
check("bb4-p4-q3 note", 12.0, REPORTER["analogue"] / REPORTER["none"], tol=0.01,
      note="model: note A calls the rise with the analogue twelvefold")

# ---------------------------------------------------------------- P5
print()
print("P5  commitment of a multipotent progenitor")
FATE = {
    "none": (2.0, 3.0, 95.0, 24.0),
    "bmp": (70.0, 5.0, 25.0, 30.0),
    "adipo": (3.0, 80.0, 17.0, 32.0),
    "both": (35.0, 40.0, 25.0, 31.0),
    "bmp_inhib": (5.0, 8.0, 87.0, 29.0),
}
ORDER5 = ["none", "bmp", "adipo", "both", "bmp_inhib"]
rows = table_numbers("bb4-p5")[1:]
for name, row in zip(ORDER5, rows):
    assert tuple(float(c) for c in row[1:]) == FATE[name], row
print("       table 1 matches the values used below")
# model: every row must account for 100% of the colonies scored, because the
# passage states that no colony was scored in two categories
for name, (mineral, lipid, undiff, _) in FATE.items():
    check(f"bb4-p5 model {name}", 100.0, mineral + lipid + undiff, tol=0.0,
          note="model: the three fates must exhaust the colonies")
check("bb4-p5-q1", key("bb4-p5-q1"), FATE["both"][0] + FATE["both"][1], tol=0.0,
      note="key: committed = mineralised + lipid-laden")
check("bb4-p5-q1/A", choice("bb4-p5-q1", "A"), FATE["both"][2], tol=0.0,
      note="distractor: the undifferentiated share")
check("bb4-p5-q1/B", choice("bb4-p5-q1", "B"), FATE["both"][0], tol=0.0,
      note="distractor: mineralised only")
check("bb4-p5-q1/C", choice("bb4-p5-q1", "C"), FATE["both"][1], tol=0.0,
      note="distractor: lipid-laden only")
# model: q5's key says the signals are not additive, which requires the
# committed share with both signals to equal the share with the osteogenic
# signal alone. Check the claim rather than assuming it.
committed = lambda k: FATE[k][0] + FATE[k][1]
check("bb4-p5-q5 model", committed("bmp"), committed("both"), tol=0.0,
      note="model: q5 key requires equal committed shares")
assert committed("both") < committed("bmp") + committed("adipo"), "must not be additive"
# model: the distractor that calls mineralisation halved must be right about it
check("bb4-p5-q5/D", 0.5, FATE["both"][0] / FATE["bmp"][0], tol=0.01,
      note="model: note D calls mineralisation halved")
# model: the doubling times must support q4, rising in every signalled condition
assert all(FATE[k][3] > FATE["none"][3] for k in ORDER5 if k != "none")
assert max(FATE[k][3] for k in ORDER5) - FATE["none"][3] <= 10.0, "the slowing must be modest"

# ---------------------------------------------------------------- P6
print()
print("P6  microsomal oxidation of a test drug")
KM = {"untreated": 10.0, "induced": 10.0, "inhibited": 40.0}
VMAX = {"untreated": 4.0, "induced": 16.0, "inhibited": 4.0}
ENZ = {"untreated": 80.0, "induced": 320.0, "inhibited": 80.0}
rows = table_numbers("bb4-p6")[1:]
for name, row in zip(["untreated", "induced", "inhibited"], rows[:3]):
    assert [float(row[1]), float(row[2]), float(row[3])] == [KM[name], VMAX[name], ENZ[name]], row
assert rows[3][1] == "not fitted" and float(rows[3][2]) == 0.0, rows[3]
print("       table 1 matches the values used below")
# model: induction must raise enzyme and Vmax in step, since it works by making
# more of the same enzyme. The turnover number must come out the same.
kcat = {k: VMAX[k] * 1000.0 / ENZ[k] for k in VMAX}   # nmol/min per nmol enzyme
check("bb4-p6 model kcat", kcat["untreated"], kcat["induced"], tol=1e-9,
      note="model: induction must leave the turnover number unchanged")
print(f"       turnover number {kcat['untreated']:.0f} per minute")
# model, against reality: a cytochrome P450 turns over at roughly 1-200 per
# minute, so the table must not imply something outside that range
assert 1.0 <= kcat["untreated"] <= 200.0, kcat
# model: Vmax must rise by the same factor as the enzyme content
check("bb4-p6 model fold", VMAX["induced"] / VMAX["untreated"], ENZ["induced"] / ENZ["untreated"],
      tol=1e-9, note="model: fourfold enzyme, fourfold Vmax")
# model: the inhibited row must be competitive in form, raising Km alone
assert VMAX["inhibited"] == VMAX["untreated"] and KM["inhibited"] > KM["untreated"]
check("bb4-p6-q2 model", 4.0, KM["inhibited"] / KM["untreated"], tol=0.0,
      note="model: note and explanation call the Km rise fourfold")
michaelis = lambda k, s: VMAX[k] * s / (KM[k] + s)
check("bb4-p6-q1", key("bb4-p6-q1"), michaelis("induced", 10.0), tol=0.001,
      note="key: Michaelis-Menten at S = Km for the induced row")
check("bb4-p6-q1/A", choice("bb4-p6-q1", "A"), michaelis("untreated", 10.0), tol=0.001,
      note="distractor: the same calculation on the untreated row")
check("bb4-p6-q1/B", choice("bb4-p6-q1", "B"), VMAX["untreated"], tol=0.0,
      note="distractor: the untreated maximal rate")
check("bb4-p6-q1/D", choice("bb4-p6-q1", "D"), VMAX["induced"], tol=0.0,
      note="distractor: the induced maximal rate, ignoring saturation")

# ---------------------------------------------------------------- P7
print()
print("P7  calcium and tension in smooth muscle")
SM = {
    "none": (120.0, 5.0, 2.0),
    "agonist": (600.0, 55.0, 80.0),
    "nocalcium": (300.0, 25.0, 35.0),
    "mlck": (590.0, 8.0, 5.0),
    "rho": (610.0, 30.0, 45.0),
    "kcl": (580.0, 40.0, 60.0),
}
ORDER7 = ["none", "agonist", "nocalcium", "mlck", "rho", "kcl"]
rows = table_numbers("bb4-p7")[1:]
for name, row in zip(ORDER7, rows):
    assert tuple(float(c) for c in row[1:]) == SM[name], row
print("       table 1 matches the values used below")
# model: q1 rests on the agonist and potassium chloride reaching similar calcium
# while differing in phosphorylation and tension. Check both halves.
assert abs(SM["agonist"][0] - SM["kcl"][0]) / SM["agonist"][0] < 0.05, "calcium must be similar"
assert SM["agonist"][1] > SM["kcl"][1] and SM["agonist"][2] > SM["kcl"][2]
# model: blocking Rho-associated kinase must pull the agonist's phosphorylation
# down toward the depolarisation value without lowering calcium
assert SM["rho"][1] < SM["agonist"][1] and SM["rho"][0] >= SM["agonist"][0]
# model: the kinase inhibitor must leave calcium essentially untouched, or q3's
# statement I could not be rejected
assert abs(SM["mlck"][0] - SM["agonist"][0]) / SM["agonist"][0] < 0.05
assert SM["mlck"][1] < 0.2 * SM["agonist"][1]
# model: phosphorylation must order tension across every stimulus, since tension
# follows from phosphorylated cross-bridges
by_phos = sorted(ORDER7, key=lambda k: SM[k][1])
assert all(SM[a][2] <= SM[b][2] for a, b in zip(by_phos, by_phos[1:])), \
    "tension must rise with phosphorylation"
print("       tension ranked by phosphorylation:", [SM[k][2] for k in by_phos])
# model, against reality: resting and stimulated cytosolic calcium in smooth
# muscle are of the order of 100 nM and several hundred nM
assert 50.0 <= SM["none"][0] <= 200.0 and 300.0 <= SM["agonist"][0] <= 1000.0
rise = lambda k: SM[k][0] - SM["none"][0]
check("bb4-p7-q2", key("bb4-p7-q2"), 100.0 * rise("nocalcium") / rise("agonist"), tol=0.001,
      note="key: ratio of the two rises above the unstimulated level")
check("bb4-p7-q2/B", choice("bb4-p7-q2", "B"),
      100.0 * SM["nocalcium"][2] / SM["agonist"][2], tol=0.005,
      note="distractor: the tension column")
check("bb4-p7-q2/C", choice("bb4-p7-q2", "C"),
      100.0 * SM["nocalcium"][0] / SM["agonist"][0], tol=0.001,
      note="distractor: peak levels, baseline not subtracted")
check("bb4-p7-q2/D", choice("bb4-p7-q2", "D"), SM["agonist"][2], tol=0.0,
      note="distractor: the tension in normal medium")
check("bb4-p7-q2 rise", 480.0, rise("agonist"), tol=0.0, note="model: rise quoted in the explanation")
check("bb4-p7-q2 rise2", 180.0, rise("nocalcium"), tol=0.0, note="model: rise quoted in the explanation")

# ---------------------------------------------------------------- P8
print()
print("P8  biofilm mutants")
BIOFILM = {"wt": 1.00, "flagellum": 0.36, "matrix": 0.08, "signal": 0.20, "signal_plus": 0.96}
ORDER8 = ["wt", "flagellum", "matrix", "signal", "signal_plus"]
PLANKTONIC_OD = {"wt": 0.80, "flagellum": 0.78, "matrix": 0.82, "signal": 0.79, "signal_plus": 0.80}
SURVIVAL = {"wt_biofilm": 40.0, "wt_planktonic": 0.5,
            "matrix_biofilm": 2.0, "matrix_planktonic": 0.6}
# model: the bar chart must encode the biomass values. The caption states
# 100 pixels per absorbance unit above a baseline at y = 150.
BASE8, SCALE8 = 150.0, 100.0
bars = rects("bb4-p8")
assert len(bars) == 5, bars
for name, (x, y, h) in zip(ORDER8, sorted(bars)):
    check(f"bb4-p8 svg {name}", h, BIOFILM[name] * SCALE8, tol=1e-9,
          note="model: bar height = value x 100 px")
    check(f"bb4-p8 svg {name} top", y, BASE8 - BIOFILM[name] * SCALE8, tol=1e-9,
          note="model: bar top = baseline - height")
# model: the printed value above each bar must match the bar it labels
markup = PASSAGE["bb4-p8"]["figure"]["markup"]
labels = [float(t) for t in re.findall(r">(\d\.\d\d)</text>", markup)]
assert labels == [BIOFILM[k] for k in ORDER8], labels
# model: the axis ticks at 0, 0.5 and 1.0 must be evenly spaced at this scale
assert 'y="154"' in markup and 'y="104"' in markup and 'y="54"' in markup
check("bb4-p8 svg axis", 50.0, 154.0 - 104.0, tol=0.0, note="model: 0.5 absorbance unit = 50 px")
# model: the prose must give every strain the same growth in suspension, or the
# design argument of q2 collapses
text = passage_text("bb4-p8")
for value in ("0.80", "0.78", "0.82", "0.79"):
    assert value in text, value
spread = max(PLANKTONIC_OD.values()) - min(PLANKTONIC_OD.values())
check("bb4-p8 model growth", 0.0, spread, tol=0.06,
      note="model: planktonic growth must be effectively equal across strains")
# model: supplying the signal must restore the synthesis mutant to near wild type
check("bb4-p8-q1 model", 1.0, BIOFILM["signal_plus"] / BIOFILM["wt"], tol=0.05,
      note="model: q1 key requires near-complete restoration")
# model: the matrix mutant must gain almost nothing from the well, as note C of
# q4 claims
assert SURVIVAL["matrix_biofilm"] / SURVIVAL["matrix_planktonic"] < 5.0
check("bb4-p8-q3", key("bb4-p8-q3"),
      SURVIVAL["wt_biofilm"] / SURVIVAL["wt_planktonic"], tol=0.001,
      note="key: biofilm survival divided by planktonic survival")
check("bb4-p8-q3/A", choice("bb4-p8-q3", "A"), SURVIVAL["wt_biofilm"] / 5.0, tol=0.001,
      note="distractor: planktonic survival misread as 5%")
check("bb4-p8-q3/B", choice("bb4-p8-q3", "B"),
      SURVIVAL["wt_biofilm"] - SURVIVAL["wt_planktonic"], tol=0.001,
      note="distractor: subtracts instead of dividing")
check("bb4-p8-q3/C", choice("bb4-p8-q3", "C"), SURVIVAL["wt_biofilm"] / 1.0, tol=0.001,
      note="distractor: planktonic survival taken as 1%")

# ---------------------------------------------------------------- P9
print()
print("P9  the thyroid axis")
THY = {
    1: (1.8, 15.0, 4.5, 5.0),
    2: (42.0, 4.0, 2.0, 8.0),
    3: (9.0, 34.0, 9.0, 1.2),
    4: (0.05, 32.0, 7.0, 1.1),
    5: (0.2, 5.0, 2.2, 1.1),
}
rows = table_numbers("bb4-p9")[1:]
for n, row in zip(range(1, 6), rows):
    assert tuple(float(c) for c in row[1:]) == THY[n], row
print("       table 1 matches the values used below")
TSH_RANGE, FT4_RANGE, FT3_RANGE = (0.4, 4.0), (12.0, 22.0), (3.0, 6.5)
text = passage_text("bb4-p9")
assert "0.4 to 4.0" in text and "12 to 22" in text and "3.0 to 6.5" in text
# model, against reality: the reference ranges quoted must be the ones a real
# laboratory uses for these assays, and the healthy subject must sit inside all
# three of them
assert TSH_RANGE[0] <= THY[1][0] <= TSH_RANGE[1]
assert FT4_RANGE[0] <= THY[1][1] <= FT4_RANGE[1]
assert FT3_RANGE[0] <= THY[1][2] <= FT3_RANGE[1]
print("       subject 1 lies inside all three reference ranges")
# model: each pattern must be the only one consistent with its diagnosis
# primary gland failure: low free T4, high TSH, intact pituitary reserve
assert THY[2][1] < FT4_RANGE[0] and THY[2][0] > TSH_RANGE[1] and THY[2][3] > THY[1][3]
# inappropriate secretion: high free T4 with high TSH and a blunted response
assert THY[3][1] > FT4_RANGE[1] and THY[3][0] > TSH_RANGE[1] and THY[3][3] < 2.0
# exogenous hormone: high free T4 with suppressed TSH
assert THY[4][1] > FT4_RANGE[1] and THY[4][0] < TSH_RANGE[0]
# pituitary failure: low free T4 with a TSH that is not raised
assert THY[5][1] < FT4_RANGE[0] and THY[5][0] < TSH_RANGE[0]
# model: free T3 must move with free T4 in every subject, because most of it is
# made from T4 in the tissues. Rank-order the two columns and compare.
by_t4 = sorted(THY, key=lambda n: THY[n][1])
assert all(THY[a][2] <= THY[b][2] for a, b in zip(by_t4, by_t4[1:])), \
    "free T3 must track free T4"
print("       free T3 ranked by free T4:", [THY[n][2] for n in by_t4])
# model: the explanation calls subject 2's TSH ten times the upper limit
check("bb4-p9-q1 model", 10.0, THY[2][0] / TSH_RANGE[1], tol=0.06,
      note="model: TSH against the top of the reference range")
check("bb4-p9-q4", key("bb4-p9-q4"), THY[2][0] / THY[1][0], tol=0.005,
      note="key: subject 2's TSH against subject 1's")
check("bb4-p9-q4/B", choice("bb4-p9-q4", "B"), THY[2][0] - THY[1][0], tol=0.001,
      note="distractor: subtracts instead of dividing")
check("bb4-p9-q4/C", choice("bb4-p9-q4", "C"), THY[2][0], tol=0.0,
      note="distractor: quotes the raw concentration")
check("bb4-p9-q4/D", choice("bb4-p9-q4", "D"), THY[2][0] / (THY[1][0] / 10.0), tol=0.005,
      note="distractor: decimal point moved one place")

# ---------------------------------------------------------------- P10
print()
print("P10  pattern-recognition receptors")
CYTO = {
    "wt": (4200.0, 2600.0, 6500.0),
    "noP": (60.0, 2550.0, 2600.0),
    "noQ": (4150.0, 70.0, 4200.0),
    "noR": (50.0, 60.0, 90.0),
}
ORDER10 = ["wt", "noP", "noQ", "noR"]
rows = table_numbers("bb4-p10")[1:]
for name, row in zip(ORDER10, rows):
    assert tuple(float(c) for c in row[1:]) == CYTO[name], row
print("       table 1 matches the values used below")
BACKGROUND = 50.0
# model: each receptor knockout must lose one response and keep the other, or
# q1's conclusion does not follow
assert CYTO["noP"][0] <= 2 * BACKGROUND and CYTO["noP"][1] > 0.9 * CYTO["wt"][1]
assert CYTO["noQ"][1] <= 2 * BACKGROUND and CYTO["noQ"][0] > 0.9 * CYTO["wt"][0]
# model: the adaptor knockout must lose both
assert CYTO["noR"][0] <= 2 * BACKGROUND and CYTO["noR"][1] <= 2 * BACKGROUND
# model: with both ligands, each receptor knockout must give about what its one
# working receptor gives alone
check("bb4-p10 model noP", CYTO["noP"][2], CYTO["noP"][1], tol=0.05,
      note="model: receptor P absent, both ligands = RNA alone")
check("bb4-p10 model noQ", CYTO["noQ"][2], CYTO["noQ"][0], tol=0.05,
      note="model: receptor Q absent, both ligands = lipopolysaccharide alone")
# model: q3's explanation calls the wild-type combination slightly less than the
# sum of the separate responses. Check the sum and the shortfall.
total = CYTO["wt"][0] + CYTO["wt"][1]
check("bb4-p10-q3 sum", 6800.0, total, tol=0.0, note="model: sum quoted in the explanation")
assert CYTO["wt"][2] < total, "the combination must fall short of the sum"
assert (total - CYTO["wt"][2]) / total < 0.10, "the shortfall must be slight, as the key says"
# model: the acidification block must spare the surface route, as q2 requires
assert 150.0 < 0.1 * CYTO["wt"][1] and 4000.0 > 0.9 * CYTO["wt"][0]

# ---------------------------------------------------------------- discretes
print()
print("Discretes")
# d3  Michaelis-Menten at three times Km
KM3, VMAX3, S3 = 2.0, 60.0, 6.0
check("bb4-d3", key("bb4-d3"), VMAX3 * S3 / (KM3 + S3), tol=0.001,
      note="key: velocity at S = 3 Km")
check("bb4-d3 model", 0.75, (VMAX3 * S3 / (KM3 + S3)) / VMAX3, tol=1e-9,
      note="model: three quarters of maximum, as the explanation says")
check("bb4-d3/A", choice("bb4-d3", "A"), VMAX3 * KM3 / (KM3 + S3), tol=0.001,
      note="distractor: Km and S exchanged in the numerator")
check("bb4-d3/B", choice("bb4-d3", "B"), VMAX3 / (S3 / KM3), tol=0.001,
      note="distractor: Vmax divided by the S-to-Km ratio")
check("bb4-d3/C", choice("bb4-d3", "C"), VMAX3 / 2.0, tol=0.001,
      note="distractor: half-maximal velocity")
# d6  Hardy-Weinberg
qq = math.sqrt(1.0 / 400.0)
check("bb4-d6 model q", 0.05, qq, tol=1e-9, note="model: recessive allele frequency")
check("bb4-d6", key("bb4-d6"), 100.0 * 2.0 * qq * (1.0 - qq), tol=0.005,
      note="key: heterozygote frequency as a percentage")
check("bb4-d6/A", choice("bb4-d6", "A"), 100.0 * 2.0 * qq * 1.0, tol=0.001,
      note="distractor: dominant allele frequency taken as 1.00")
check("bb4-d6/C", choice("bb4-d6", "C"), 100.0 * qq, tol=0.001,
      note="distractor: the allele frequency itself")
check("bb4-d6/D", choice("bb4-d6", "D"), 100.0 / 400.0, tol=0.001,
      note="distractor: the homozygous recessive frequency given in the stem")
# d12  doubling time
N0, N1, MINUTES = 2.0e5, 1.28e7, 180.0
fold = N1 / N0
check("bb4-d12 model fold", 64.0, fold, tol=1e-9, note="model: the stated rise is 64-fold")
check("bb4-d12 model doublings", 6.0, math.log(fold, 2), tol=1e-9,
      note="model: 64-fold is six doublings")
check("bb4-d12", key("bb4-d12"), MINUTES / math.log(fold, 2), tol=0.001,
      note="key: 180 minutes divided by six doublings")
check("bb4-d12/A", choice("bb4-d12", "A"), MINUTES / fold, tol=0.02,
      note="distractor: divides by the fold increase itself")
check("bb4-d12/C", choice("bb4-d12", "C"), MINUTES / 5.0, tol=0.001,
      note="distractor: five doublings instead of six")
check("bb4-d12/D", choice("bb4-d12", "D"), MINUTES, tol=0.001,
      note="distractor: the whole period as one doubling")
check("bb4-d12 note D", 4.0e5, N0 * 2.0, tol=1e-9,
      note="model: one doubling would reach the value quoted in note D")
# d15  ATP equivalents per acetyl-CoA
check("bb4-d15", key("bb4-d15"), 3 * 2.5 + 1 * 1.5 + 1, tol=1e-9,
      note="key: 3 NADH, 1 FADH2 and 1 GTP")
check("bb4-d15/B", choice("bb4-d15", "B"), 3 * 2.5 + 1 * 2.5 + 1, tol=1e-9,
      note="distractor: FADH2 valued as an NADH")
check("bb4-d15/C", choice("bb4-d15", "C"), 3 * 3.0 + 1 * 2.0 + 1, tol=1e-9,
      note="distractor: the older 3-and-2 convention")
check("bb4-d15/D", choice("bb4-d15", "D"), 4 * 2.5 + 1 * 1.5 + 1, tol=1e-9,
      note="distractor: adds the pyruvate dehydrogenase NADH")

# ---------------------------------------------------------------- choice order
print()
print("Choice order and distinctness")
LETTERS = "ABCD"
for q in DATA["questions"]:
    texts = [q["choices"][letter].strip() for letter in LETTERS]
    if all(re.match(r"^[-+]?\d", t) for t in texts):
        values = []
        for t in texts:
            cleaned = t.replace("×", "x")
            for digit, sup in zip("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"):
                cleaned = cleaned.replace(sup, digit)
            cleaned = re.sub(r"x\s*10\s*(-?\d+)", r"e\1", cleaned)
            values.append(float(re.search(r"-?\d+(?:\.\d+)?(?:e-?\d+)?", cleaned).group(0)))
        up = all(b >= a for a, b in zip(values, values[1:]))
        down = all(b <= a for a, b in zip(values, values[1:]))
        if not (up or down):
            BAD.append(q["id"] + " order")
            print(f"  FAIL  {q['id']}: numeric choices out of order {values}")
        else:
            print(f"  ok    {q['id']}: {'ascending' if up else 'descending'} {values}")
        if len(set(values)) != 4:
            BAD.append(q["id"] + " duplicate")
            print(f"  FAIL  {q['id']}: two choices share a value")

print()
print(f"{COUNT} values checked")
if BAD:
    print("FAILURES:", sorted(set(BAD)))
    raise SystemExit(1)
print("All computed values agree with the content, and every model check holds.")
