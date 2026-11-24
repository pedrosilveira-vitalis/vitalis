"""Recompute every quantitative key and distractor in fl2 Bio/Biochem.

Each value is derived from the numbers the passage itself supplies, never
copied from the choice it is meant to confirm, and each distractor is
recomputed from the specific mistake its note names, so that no distractor is
accidentally also right.

The blocks headed "model" check the passages rather than the questions: that a
table's rows add up, that a figure quoted in prose matches the table it came
from, and that a claim the passage makes about its own data is true. A
verifier that only repeats the author's arithmetic confirms the author's
assumptions; these are the checks that can catch the assumption itself.
"""
import math

BAD = []
COUNT = 0


def check(qid, claimed, got, tol=0.02, note=""):
    global COUNT
    COUNT += 1
    ok = abs(got - claimed) <= tol * abs(claimed) if claimed else abs(got) <= tol
    print(("  ok  " if ok else "  FAIL") + f"  {qid:18s} claimed={claimed:<13.6g} computed={got:<13.6g} {note}")
    if not ok:
        BAD.append(qid)


# ---------------------------------------------------------------- P1
print("P1  isolated mitochondria, Table 1 (nmol O2/min and nmol ATP/min per mg)")
O2 = {"succ": 5.0, "adp": 30.0, "oligo": 4.0, "dnp": 48.0, "dnp_oligo": 46.0, "cn": 0.5}
ATP = {"succ": 0.0, "adp": 90.0, "oligo": 0.0, "dnp": 0.0, "dnp_oligo": 0.0, "cn": 0.0}
# model: the only condition that makes ATP is the one with ADP and no inhibitor
assert [k for k, v in ATP.items() if v > 0] == ["adp"], "only the coupled condition may make ATP"
# model: uncoupled respiration must exceed the ADP-stimulated rate, and must
# survive a block of the synthase, or the passage's argument does not hold
assert O2["dnp"] > O2["adp"] > O2["succ"] > O2["oligo"] > O2["cn"]
check("bb2-p1 model", 0.042, (O2["dnp"] - O2["dnp_oligo"]) / O2["dnp"], tol=0.2,
      note="model: oligomycin changes the uncoupled rate by only a few per cent")
check("bb2-p1-q1", 1.5, ATP["adp"] / (2 * O2["adp"]), note="key: ATP per oxygen ATOM")
check("bb2-p1-q1/A", 9.0, ATP["adp"] / (2 * O2["succ"]), note="distractor: resting rate as the denominator")
check("bb2-p1-q1/B", 3.0, ATP["adp"] / O2["adp"], note="distractor: O2 counted as one atom")
# choice C (2.5) is the textbook NADH-linked P/O, not a figure from the table
check("bb2-p1-q4", 6.0, O2["adp"] / O2["succ"], note="key: respiratory control ratio")
check("bb2-p1-q4/A", 9.6, O2["dnp"] / O2["succ"], note="distractor: uncoupled rate as numerator")
check("bb2-p1-q4/B", 7.5, O2["adp"] / O2["oligo"], note="distractor: oligomycin rate as the resting rate")
check("bb2-p1-q4/D", 5.0, (O2["adp"] - O2["succ"]) / O2["succ"], note="distractor: increment over rate")

# ---------------------------------------------------------------- P2
print()
print("P2  fat absorption, Table 1 (100 g/day intake)")
INTAKE = 100.0
FAECAL = {1: 4.0, 2: 45.0, 3: 30.0, 4: 10.0}
RISE = {1: 80.0, 2: 8.0, 3: 20.0, 4: 2.0}
absorbed = {s: 100 * (INTAKE - f) / INTAKE for s, f in FAECAL.items()}
for s in sorted(absorbed):
    print(f"       Subject {s}: absorbed {absorbed[s]:.0f}%, plasma rise {RISE[s]:.0f} mg/dL")
# model: the control must be the best absorber and give the largest rise
assert absorbed[1] == max(absorbed.values()) and RISE[1] == max(RISE.values())
# model: the micelle defect must sit between the lipase defect and the control
# on both measures, or the pattern asked for in q2 is not discriminating
assert absorbed[2] < absorbed[3] < absorbed[4] < absorbed[1]
assert RISE[2] < RISE[3] < RISE[1] and RISE[4] < RISE[3]
check("bb2-p2-q1", 70, absorbed[3], note="key: Subject 3's coefficient of fat absorption")
check("bb2-p2-q1/A", 96, absorbed[1], note="distractor: Subject 1's value")
check("bb2-p2-q1/C", 55, absorbed[2], note="distractor: Subject 2's value")
check("bb2-p2-q1/D", 30, 100 * FAECAL[3] / INTAKE, note="distractor: the fraction NOT absorbed")
check("bb2-p2-q3", 90, absorbed[4], tol=0.001,
      note="model: Subject 4 absorbs nearly normally, as a post-uptake block requires")

# ---------------------------------------------------------------- P3
print()
print("P3  mtl operon, Table 1 (reporter activity, arbitrary units)")
R = {
    "wt": {"none": 5.0, "mtl": 500.0, "mtl_glc": 50.0},
    "dR": {"none": 480.0, "mtl": 500.0, "mtl_glc": 50.0},
    "oc": {"none": 460.0, "mtl": 470.0, "mtl_glc": 48.0},
    "sR": {"none": 4.0, "mtl": 6.0, "mtl_glc": 4.0},
}
# model: the glucose effect must be about tenfold in every strain that
# expresses the reporter, since q4 rests on exactly that
for name in ("wt", "dR", "oc"):
    ratio = R[name]["mtl"] / R[name]["mtl_glc"]
    check(f"bb2-p3 model/{name}", 10.0, ratio, tol=0.05, note="model: glucose lowers expression tenfold")
# model: the super-repressor strain must be repressed in every medium
assert max(R["sR"].values()) < 0.02 * R["wt"]["mtl"], "the fourth strain must stay off"
check("bb2-p3-q1", 100, R["wt"]["mtl"] / R["wt"]["none"], note="key: wild-type induction ratio")
check("bb2-p3-q1/A", 125, R["wt"]["mtl"] / R["sR"]["none"], note="distractor: basal from another strain")
check("bb2-p3-q1/C", 10, R["wt"]["mtl"] / R["wt"]["mtl_glc"], note="distractor: the glucose effect")
check("bb2-p3-q1/D", 1.0, R["dR"]["mtl"] / R["dR"]["none"], tol=0.05,
      note="distractor: the ratio in the mtlR deletion strain")

# ---------------------------------------------------------------- P4
print()
print("P4  alternative splicing; exon 5 = 108 nt, exon 6 = 144 nt")
EX5, EX6 = 108, 144
assert EX6 % 3 == 0 and EX5 % 3 == 0, "skipping the exon must preserve the reading frame"
check("bb2-p4-q1", 48, EX6 / 3, note="key: residues encoded by the skipped exon")
check("bb2-p4-q1/A", 144, EX6, note="distractor: nucleotides counted as residues")
check("bb2-p4-q1/B", 84, (EX6 + EX5) / 3, note="distractor: exon 5 counted as missing too")
check("bb2-p4-q1/D", 36, EX5 / 3, note="distractor: the wrong exon divided by three")
FORM_A = {"none": 85.0, "cyto": 40.0, "kd": 20.0, "oe": 95.0}
# model: form B is the complement of form A, and the factor's two manipulations
# must move inclusion in opposite directions for q2 to be answerable
assert all(0 < v < 100 for v in FORM_A.values())
assert FORM_A["kd"] < FORM_A["none"] < FORM_A["oe"]

# ---------------------------------------------------------------- P5
print()
print("P5  three viruses, Table 1 (log10 PFU/mL)")
Y = {
    "none": {"P": 8.0, "Q": 7.0, "R": 8.0},
    "nuc": {"P": 8.0, "Q": 3.0, "R": 8.0},
    "act": {"P": 7.9, "Q": 4.0, "R": 5.0},
    "chx": {"P": 5.0, "Q": 4.0, "R": 5.0},
    "pro": {"P": 4.0, "Q": 7.0, "R": 8.0},
}
check("bb2-p5-q2", 10000, 10 ** (Y["none"]["Q"] - Y["nuc"]["Q"]), note="key: fold reduction by the analogue")
check("bb2-p5-q2/B", 1000, 10 ** (Y["none"]["Q"] - Y["chx"]["Q"]), note="distractor: cycloheximide row used")
check("bb2-p5-q2/C", 100, 10 ** math.floor(Y["none"]["Q"] / Y["nuc"]["Q"]),
      note="distractor: logarithms divided, 7.0/3.0 read as two orders of magnitude")
check("bb2-p5-q2/D", 10, 10 ** (Y["chx"]["Q"] - Y["nuc"]["Q"]), note="distractor: two treatments compared")
# model: q3 quotes "three orders of magnitude" for R and "about one-fifth" for P
check("bb2-p5 model/R", 1000, 10 ** (Y["none"]["R"] - Y["act"]["R"]),
      note="model: actinomycin D costs Virus R three logs")
check("bb2-p5 model/P", 0.20, 1 - 10 ** (Y["act"]["P"] - Y["none"]["P"]), tol=0.05,
      note="model: the same drug costs Virus P about one fifth of its yield")
# model: the protease inhibitor must hit only the virus whose protease it targets
assert Y["pro"]["Q"] == Y["none"]["Q"] and Y["pro"]["R"] == Y["none"]["R"] < 8.1
assert Y["pro"]["P"] < Y["none"]["P"]
# model: cycloheximide must lower all three, since no virus carries a ribosome
assert all(Y["chx"][v] < Y["none"][v] for v in "PQR")
# model: the serum-withdrawal experiment described in paragraph 4. Virus R, a
# nuclear DNA virus, must lose yield in a culture held out of the cycle while
# the cytoplasmic RNA virus does not, and the infected cells must then show a
# clear rise in the proportion that have replicated their DNA, or q4 has
# nothing to rest on.
R_SERUM_LOGS = 2.0
check("bb2-p5 model/serum", 100, 10 ** R_SERUM_LOGS,
      note="model: two logarithms is a 100-fold loss of Virus R yield")
S_PHASE_BEFORE, S_PHASE_AFTER = 3.0, 45.0
check("bb2-p5 model/S-phase", 15, S_PHASE_AFTER / S_PHASE_BEFORE,
      note="model: replicated-DNA fraction rises 15-fold after Virus R infection")
assert S_PHASE_AFTER < 100 and S_PHASE_BEFORE > 0
# model: the nucleoside analogue must spare both viruses that make no DNA from RNA
assert Y["nuc"]["P"] == Y["none"]["P"] and Y["nuc"]["R"] == Y["none"]["R"]

# ---------------------------------------------------------------- P6
print()
print("P6  ventricular volumes, Table 1")
V = {
    "base": (120.0, 50.0, 70.0),
    "saline": (150.0, 55.0, 70.0),
    "inotrope": (120.0, 30.0, 80.0),
    "blocker": (130.0, 70.0, 50.0),
}
for name, (edv, esv, hr) in V.items():
    sv = edv - esv
    print(f"       {name:9s} SV {sv:5.1f} mL   CO {sv * hr / 1000:5.2f} L/min   EF {100 * sv / edv:4.1f}%")
# model: raising filling volume with nothing else changed must raise stroke
# volume, or the passage's Frank-Starling argument in q2 has no support
assert V["saline"][0] - V["saline"][1] > V["base"][0] - V["base"][1]
assert V["saline"][2] == V["base"][2], "heart rate must be unchanged by the saline infusion"
# model: the inotrope must lower end-systolic volume at unchanged filling volume
assert V["inotrope"][0] == V["base"][0] and V["inotrope"][1] < V["base"][1]


def co(name, edv=None, esv=None, hr=None):
    e, s, h = V[name]
    return ((edv or e) - (esv if esv is not None else s)) * (hr or h) / 1000.0


check("bb2-p6-q1", 7.2, co("inotrope"), note="key: cardiac output under the inotrope")
check("bb2-p6-q1/A", 2.4, V["inotrope"][1] * V["inotrope"][2] / 1000, note="distractor: ESV times rate")
check("bb2-p6-q1/B", 6.3, co("inotrope", hr=V["base"][2]), note="distractor: baseline heart rate used")
check("bb2-p6-q1/D", 9.6, V["inotrope"][0] * V["inotrope"][2] / 1000, note="distractor: EDV times rate")
check("bb2-p6-q2", 95, V["saline"][0] - V["saline"][1], note="stem: stroke volume after saline, quoted in prose")
check("bb2-p6-q3", 46, 100 * (V["blocker"][0] - V["blocker"][1]) / V["blocker"][0],
      tol=0.01, note="key: ejection fraction after the antagonist")
check("bb2-p6-q3/B", 54, 100 * V["blocker"][1] / V["blocker"][0], tol=0.01,
      note="distractor: fraction retained, not ejected")
check("bb2-p6-q3/C", 58, 100 * (V["base"][0] - V["base"][1]) / V["base"][0], tol=0.01,
      note="distractor: the baseline ejection fraction")
check("bb2-p6-q3/D", 86, 100 * (V["blocker"][0] - V["blocker"][1]) / V["blocker"][1], tol=0.01,
      note="distractor: divided by end-systolic volume")
check("bb2-p6-q4", 4.9, co("base"), note="explanation: baseline cardiac output")
check("bb2-p6-q4b", 6.65, co("saline"), note="explanation: cardiac output after saline")

# ---------------------------------------------------------------- P7
print()
print("P7  three-point cross, Table 1")
CLASS = {"+ + +": 410, "b a c": 390, "b + +": 54, "+ a c": 50,
         "+ + c": 45, "b a +": 43, "+ a +": 4, "b + c": 4}
TOTAL = sum(CLASS.values())
check("bb2-p7 model", 1000, TOTAL, tol=0.0, note="model: the eight classes sum to the 1000 scored")
# model: with order b-a-c and parental arrangements +++ and bac, work out which
# class each exchange produces rather than asserting it
PARENTS = ({"b": "+", "a": "+", "c": "+"}, {"b": "b", "a": "a", "c": "c"})


def label(g):
    return " ".join(g[k] for k in ("b", "a", "c"))


def swap(parent, genes):
    out = dict(parent)
    other = PARENTS[0] if parent is PARENTS[1] else PARENTS[1]
    for g in genes:
        out[g] = other[g]
    return out


# an exchange in the b-a interval moves b (the outer gene of that interval)
sco1 = {label(swap(p, ["b"])) for p in PARENTS}
# an exchange in the a-c interval moves c
sco2 = {label(swap(p, ["c"])) for p in PARENTS}
# an exchange in both moves only the middle gene a
dco = {label(swap(p, ["b", "c"])) for p in PARENTS}
print("       derived classes: b-a single", sorted(sco1), "a-c single", sorted(sco2), "double", sorted(dco))
assert sco1 == {"b + +", "+ a c"}, sco1
assert sco2 == {"+ + c", "b a +"}, sco2
assert dco == {"+ a +", "b + c"}, dco
n_dco = sum(CLASS[k] for k in dco)
n_sco1 = sum(CLASS[k] for k in sco1)
n_sco2 = sum(CLASS[k] for k in sco2)
# model: the derived double-crossover classes must be the rarest, which is the
# whole basis of the gene-order question
assert max(CLASS[k] for k in dco) < min(CLASS[k] for k in list(sco1) + list(sco2))
d_ba = 100 * (n_sco1 + n_dco) / TOTAL
d_ac = 100 * (n_sco2 + n_dco) / TOTAL
check("bb2-p7-q2", 20.8, d_ba + d_ac, note="key: b to c as the sum of the two intervals")
check("bb2-p7-q2/B", 19.2, 100 * (n_sco1 + n_sco2) / TOTAL, note="distractor: outer markers scored directly")
check("bb2-p7-q2/C", 11.2, d_ba, note="distractor: the b to a interval alone")
check("bb2-p7-q2/D", 9.6, d_ac, note="distractor: the a to c interval alone")
check("bb2-p7-q3", 9.6, d_ac, note="key: the a to c interval")
check("bb2-p7-q3/A", 8.8, 100 * n_sco2 / TOTAL, note="distractor: double crossovers omitted")
check("bb2-p7-q5", 11, (d_ba / 100) * (d_ac / 100) * TOTAL, tol=0.03,
      note="key: double crossovers expected under independence")
check("bb2-p7-q5/A", 208, (d_ba + d_ac) / 100 * TOTAL, note="distractor: frequencies added")
check("bb2-p7-q5/B", 192, n_sco1 + n_sco2, note="distractor: the direct b to c recombinants")
check("bb2-p7-q5/C", 108, d_ba * d_ac, tol=0.01, note="distractor: percentages multiplied as percentages")
check("bb2-p7 model", 8, n_dco, tol=0.0, note="model: observed double crossovers, fewer than expected")

# ---------------------------------------------------------------- P8
print()
print("P8  steroid and peptide hormone, Table 1 (fold change)")
FOLD = {
    "S": {"0.5": 1.2, "2": 6.0, "8": 24.0},
    "S_act": {"0.5": 1.0, "2": 1.1, "8": 1.0},
    "S_nls": {"0.5": 1.0, "2": 1.1, "8": 1.2},
    "S_poly": {"0.5": 1.1, "2": 1.2, "8": 1.1},
    "P": {"0.5": 3.0, "2": 4.0, "8": 2.0},
}
BASE = 400.0
# model: the peptide must be ahead at 30 min and the steroid ahead at 8 h, or
# the comparison q1 asks about does not exist in the data
assert FOLD["P"]["0.5"] > FOLD["S"]["0.5"] and FOLD["S"]["8"] > FOLD["P"]["8"]
# model: each of the three blocked conditions must stay within noise of 1.0
for name in ("S_act", "S_nls", "S_poly"):
    assert max(FOLD[name].values()) <= 1.2, name
check("bb2-p8-q2", 9600, FOLD["S"]["8"] * BASE, note="key: copies per cell at eight hours")
check("bb2-p8-q2/B", 2400, FOLD["S"]["2"] * BASE, note="distractor: the two-hour fold change")
check("bb2-p8-q2/C", 480, FOLD["S"]["0.5"] * BASE, note="distractor: the 30-minute fold change")
check("bb2-p8-q2/D", 17, BASE / FOLD["S"]["8"], tol=0.03, note="distractor: divided instead of multiplied")

# ---------------------------------------------------------------- P9
print()
print("P9  secreted enzyme, Table 1 (kDa)")
PRIMARY, SIGNAL, SITES, CORE = 54.5, 2.5, 2, 2.0
MASS = {"wt": 60.0, "nosig": 52.0, "tunica": 52.0, "asn": 52.0, "bfa": 56.0}
# model: the cleaved chain must be the primary product less the signal sequence,
# and the three unglycosylated preparations must all run at that mass
check("bb2-p9 model", 52.0, PRIMARY - SIGNAL, note="model: chain mass after signal cleavage")
for name in ("nosig", "tunica", "asn"):
    assert MASS[name] == PRIMARY - SIGNAL, name
# model: the ER form must carry two cores and nothing more
check("bb2-p9 model/ER", MASS["bfa"], (PRIMARY - SIGNAL) + SITES * CORE,
      note="model: brefeldin A sample is the cleaved chain plus two cores")
check("bb2-p9-q1", 4.0, (MASS["wt"] - MASS["tunica"]) / SITES, note="key: mass per mature oligosaccharide")
check("bb2-p9-q1/A", 8.0, MASS["wt"] - MASS["tunica"], note="distractor: whole difference at one site")
check("bb2-p9-q1/C", 2.5, SIGNAL, note="distractor: the signal sequence, which is removed")
check("bb2-p9-q1/D", 2.0, (MASS["bfa"] - MASS["tunica"]) / SITES, note="distractor: the core, before extension")
SECRETED = {"wt": 85.0, "nosig": 2.0, "tunica": 40.0, "asn": 55.0, "bfa": 3.0}
# model: removing the sugars two different ways must reduce secretion without
# abolishing it, which is exactly the claim q3 keys on
assert SECRETED["nosig"] < 5 and SECRETED["bfa"] < 5
assert 20 < SECRETED["tunica"] < SECRETED["asn"] < SECRETED["wt"]

# ---------------------------------------------------------------- P10
print()
print("P10  complement, Table 1 (% lysis and serum C3)")
S = {
    "donor": (100.0, 100.0, 130.0),
    "p1": (2.0, 98.0, 125.0),
    "p2": (3.0, 4.0, 8.0),
    "p3": (5.0, 6.0, 135.0),
    "p4": (96.0, 3.0, 128.0),
}
LO, HI = 100.0, 180.0
for name, (ab, alt, c3) in S.items():
    print(f"       {name:6s} antibody-dependent {ab:5.1f}%  antibody-independent {alt:5.1f}%  C3 {c3:5.1f} mg/dL"
          f"  {'C3 low' if c3 < LO else 'C3 normal'}")
# model: exactly one patient may have a low C3, and only that patient's
# deficiency may be of the shared component
assert [n for n, v in S.items() if v[2] < LO] == ["p2"]
# model: each of the four patterns the questions name must be unique
assert S["p1"][0] < 10 and S["p1"][1] > 90        # classical-only defect
assert S["p4"][1] < 10 and S["p4"][0] > 90        # alternative-only defect
assert S["p3"][0] < 10 and S["p3"][1] < 10 and S["p3"][2] >= LO   # late defect, normal C3
assert S["p2"][0] < 10 and S["p2"][1] < 10 and S["p2"][2] < LO    # shared defect, low C3
assert LO <= S["p4"][2] <= HI, "q4 asserts Patient 4's C3 lies inside the reference interval"

# ---------------------------------------------------------------- discretes
print()
print("Discretes")
KCAT, KM_UM = 300.0, 50.0
check("bb2-d3", 6.0e6, KCAT / (KM_UM * 1e-6), note="key: kcat/Km in M^-1 s^-1")
check("bb2-d3/A", 1.7e-7, (KM_UM * 1e-6) / KCAT, tol=0.03, note="distractor: ratio inverted")
check("bb2-d3/B", 6.0e3, KCAT / (KM_UM * 1e-3), note="distractor: Km left in millimolar")
check("bb2-d3/C", 1.5e4, KCAT * KM_UM, note="distractor: multiplied by 50 instead of divided")
# d7: an affected father makes the daughter an obligate carrier
check("bb2-d7", 50, 100 * 1.0 * 0.5, note="key: half of the sons of a carrier mother")
check("bb2-d7/B", 25, 100 * 0.5 * 0.5, note="distractor: probability of an affected son among all children")
CARBONS = 16
check("bb2-d8", 7, CARBONS / 2 - 1, note="key: rounds of beta-oxidation for a 16-carbon chain")
check("bb2-d8/B", 8, CARBONS / 2, note="distractor: the number of acetyl-CoA")
check("bb2-d8/D", 6, CARBONS / 2 - 2, note="distractor: two fewer than the acetyl-CoA count")
# d13: phase durations from the DNA-content shares of an asynchronous culture
CYCLE_H = 20.0
SHARE = {"G1": 0.60, "S": 0.25, "G2M": 0.15}
# model: the three measured compartments must account for the whole population,
# or the stem's assumption cannot be applied to any of them
check("bb2-d13 model", 1.0, sum(SHARE.values()), tol=0.0,
      note="model: the three DNA-content classes are the whole culture")
check("bb2-d13", 12, SHARE["G1"] * CYCLE_H, note="key: G1 is 60% of a 20 h cycle")
check("bb2-d13/B", 6.7, CYCLE_H / 3, tol=0.01,
      note="distractor: cycle split equally between the three compartments")
check("bb2-d13/C", 5.0, SHARE["S"] * CYCLE_H, note="distractor: the S-phase share used for G1")
check("bb2-d13/D", 3.0, SHARE["G2M"] * CYCLE_H, note="distractor: the G2/M share used for G1")
# model: the phase lengths must sum back to the cycle time quoted in the stem
check("bb2-d13 model/sum", CYCLE_H, sum(v * CYCLE_H for v in SHARE.values()), tol=0.0,
      note="model: G1 + S + G2/M returns the 20 h cycle")

print()
print(f"{COUNT - len(BAD)}/{COUNT} values verified")
if BAD:
    raise SystemExit("FAILED: " + ", ".join(sorted(set(BAD))))
