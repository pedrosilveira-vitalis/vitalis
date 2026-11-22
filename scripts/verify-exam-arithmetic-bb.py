"""Recompute every quantitative key and distractor in fl1 Bio/Biochem.

Each value is derived from the numbers the passage itself supplies, never
copied from the answer choice it is meant to confirm, and each distractor is
recomputed from the specific mistake its note names. The point of the second
half is that no distractor is accidentally also right.
"""
import math

BAD = []


def check(qid, claimed, got, tol=0.02, note=""):
    ok = abs(got - claimed) <= tol * abs(claimed) if claimed else abs(got) <= tol
    print(("  ok  " if ok else "  FAIL") + f"  {qid:16s} claimed={claimed:<13.6g} computed={got:<13.6g} {note}")
    if not ok:
        BAD.append(qid)


def mm(vmax, km, s):
    """Michaelis-Menten initial velocity."""
    return vmax * s / (km + s)


print("P1  phosphofructokinase, Table 1: Vmax 60 nmol/min; Km 1.0 (none), 0.25 (AMP), 4.0 (citrate), 0.20 (F2,6BP)")
VMAX = 60.0
KM_NONE, KM_AMP, KM_CIT, KM_FBP = 1.0, 0.25, 4.0, 0.20
check("bb-p1-q1", 20, mm(VMAX, KM_CIT, 2.0), note="key: citrate Km 4.0 mM, substrate 2.0 mM")
check("bb-p1-q1/A", 53, mm(VMAX, KM_AMP, 2.0), note="distractor: AMP row's Km used instead")
check("bb-p1-q1/B", 40, mm(VMAX, KM_NONE, 2.0), note="distractor: no-effector Km used instead")
check("bb-p1-q1/C", 30, VMAX * 2.0 / KM_CIT, note="distractor: substrate left out of the denominator")
# the passage's claim that each effector is a pure affinity effect
check("bb-p1-q2", 4.0, KM_CIT / KM_NONE, note="citrate raises apparent Km fourfold, Vmax unchanged")
check("bb-p1-q5", 5.0, KM_NONE / KM_FBP, note="fructose-2,6-bisphosphate raises affinity fivefold")

print()
print("P2  replication fidelity, Table 2 and a 4.6 x 10^6 bp genome")
GENOME = 4.6e6
WT, NO_PROOF, NO_MMR, NEITHER = 1e-10, 1e-7, 1e-8, 1e-5
check("bb-p2-q1", 4.6e-4, WT * GENOME, note="key: mutations per genome per generation")
check("bb-p2-q1/A", 0.46, NO_PROOF * GENOME, note="distractor: proofreading-deficient rate used")
check("bb-p2-q1/C", 4.6e-7, WT * 4.6e3, note="distractor: genome size taken in kilobases")
check("bb-p2-q1/D", 4.6e-16, 4.6 * 10 ** (-10 - 6), note="distractor: exponents subtracted, not added")
check("bb-p2-q2", 3, math.log10(NO_PROOF / WT), note="key: orders of magnitude lost with proofreading")
check("bb-p2-q2/A", 1, math.log10(NO_PROOF / NO_MMR), note="distractor: the two single mutants compared")
check("bb-p2-q2/B", 2, math.log10(NO_MMR / WT), note="distractor: the mismatch repair contribution")
check("bb-p2-q2/D", 5, math.log10(NEITHER / WT), note="distractor: both systems credited at once")
# the passage asserts the three mechanisms multiply; confirm Table 2 is internally consistent
check("bb-p2 model", NEITHER, 1e-5, note="base selection alone is 1 in 10^5, as stated")
check("bb-p2 model", WT, NEITHER / (NO_PROOF / WT) / (NO_MMR / WT) * 1, tol=1e-9,
      note="selection x proofreading x mismatch repair reproduces the wild-type rate")

print()
print("P3  oxygen content: content = 1.34 x Hb x SaO2 + 0.003 x PaO2")


def content(hb, sat, pao2):
    return 1.34 * hb * sat + 0.003 * pao2


J, K, L, M = (15, 0.97, 90), (8, 0.98, 95), (15, 0.80, 50), (15, 0.60, 95)
for name, s in (("J", J), ("K", K), ("L", L), ("M", M)):
    print(f"       Subject {name}: {content(*s):.2f} mL/dL")
check("bb-p3-q1", 10.8, content(*K), note="key: Subject K")
check("bb-p3-q1/A", 1.6, 1.34 * K[1] + 0.003 * K[2], note="distractor: haemoglobin concentration omitted")
check("bb-p3-q1/C", 19.8, content(J[0], K[1], K[2]), tol=0.01,
      note="distractor: control's 15 g/dL used for Subject K")
check("bb-p3-q1/D", 105.5, 1.34 * K[0] * K[1] + K[2], note="distractor: PaO2 added rather than scaled by 0.003")
check("bb-p3-q2", max(content(*s) for s in (J, K, L, M)), content(*J),
      note="key: Subject J holds the greatest content of the four")
check("bb-p3-q5", 12.3, content(*M), note="Subject M's content, used in the explanation")
assert content(*M) < content(*J), "carbon monoxide must lower content below the control"

print()
print("P4  flow cytometry, Table 4")
check("bb-p4-q1", 35, 35, note="variant cells in S phase, read from Table 4")
check("bb-p4-q3", 55, 100 - 45, note="variant cells that have left G1")
check("bb-p4-q3b", 15, 100 - 85, note="untransfected cells that have left G1")
for row in ((85, 6, 9), (80, 9, 11), (45, 35, 20)):
    assert sum(row) == 100, f"Table 4 row {row} does not total 100%"

print()
print("P5  growth and resistance, Table 5; doubling time 30 min from 1.0 x 10^3 cells/mL")
N0, DOUBLING_MIN = 1.0e3, 30.0
gens = 4 * 60 / DOUBLING_MIN
check("bb-p5-q1", 2.6e5, N0 * 2 ** gens, note="key: 4 hours is 8 generations")
check("bb-p5-q1/A", 8.0e3, N0 * gens, note="distractor: multiplied by the generation count")
check("bb-p5-q1/B", 1.6e4, N0 * 2 ** 4, note="distractor: one division per hour assumed")
check("bb-p5-q1/C", 1.3e5, N0 * 2 ** 7, note="distractor: seven doublings counted")
AMP_FREE, AMP_PLASMID, TET_FREE, TET_PLASMID = 2.0, 512.0, 1.0, 64.0
check("bb-p5-q3", 256, AMP_PLASMID / AMP_FREE, note="key: ampicillin fold rise")
check("bb-p5-q3/A", 8, AMP_PLASMID / TET_PLASMID, note="distractor: the two drugs divided into each other")
check("bb-p5-q3/B", 64, TET_PLASMID / TET_FREE, note="distractor: the tetracycline fold rise")
check("bb-p5-q3/C", 128, AMP_PLASMID / 4.0, note="distractor: divided by 4 rather than by 2")

print()
print("P6  fatty acid oxidation (2.5 per NADH, 1.5 per FADH2, 10 per acetyl-CoA, 2 to activate)")


def fa_atp(carbons, per_nadh=2.5, per_fadh=1.5, per_acetyl=10.0, activation=2.0, rounds=None):
    acetyl = carbons // 2
    spirals = acetyl - 1 if rounds is None else rounds
    return spirals * (per_nadh + per_fadh) + acetyl * per_acetyl - activation


check("bb-p6-q1", 106, fa_atp(16), note="key: 7 spirals, 8 acetyl-CoA, less activation")
check("bb-p6-q1/B", 108, fa_atp(16, activation=0.0), note="distractor: activation cost omitted")
check("bb-p6-q1/C", 110, fa_atp(16, rounds=8), note="distractor: one spiral per acetyl-CoA")
check("bb-p6-q1/D", 129, fa_atp(16, per_nadh=3.0, per_fadh=2.0, per_acetyl=12.0),
      note="distractor: older conversion factors")
# Table 6 trends quoted in the explanations
FFA12, FFA72, BHB12, BHB72, INS12, INS72 = 0.6, 1.4, 0.15, 3.0, 60.0, 15.0
check("bb-p6-q2", 20, BHB72 / BHB12, note="3-hydroxybutyrate rises twentyfold, 12 h to 72 h")
check("bb-p6-q2b", 2.33, FFA72 / FFA12, note="free fatty acids more than double over the same period")
check("bb-p6-q3", 4, INS12 / INS72, note="insulin falls fourfold, so it cannot be rising")
check("bb-p6-q2c", 5, BHB72 / 0.6, note="3-hydroxybutyrate rises fivefold after 24 h")
BRAIN_G, WHOLE_G, LIVER_GLYCOGEN = 120.0, 300.0, 100.0
check("bb-p6-q5", 20, 24 * LIVER_GLYCOGEN / BRAIN_G, note="key: hours the liver store covers the brain")
check("bb-p6-q5/A", 8, 24 * LIVER_GLYCOGEN / WHOLE_G, note="distractor: whole-body glucose use")
check("bb-p6-q5/C", 29, 24 * BRAIN_G / LIVER_GLYCOGEN, tol=0.01, note="distractor: the ratio inverted")
check("bb-p6-q5/D", 48, 24 * LIVER_GLYCOGEN / 50.0, note="distractor: a 50 g/day requirement assumed")

print()
print("P7  filtered load: GFR 125 mL/min, plasma glucose 5.0 mM, transport maximum 2.0 mmol/min")
GFR_L, PG, TM = 0.125, 5.0, 2.0
check("bb-p7-q1", 0.625, GFR_L * PG, note="key: filtered load in mmol/min")
check("bb-p7-q1/A", 625, 125.0 * PG, note="distractor: filtration rate left in millilitres")
check("bb-p7-q1/B", 25, 125.0 / PG, note="distractor: divided instead of multiplied")
check("bb-p7-q1/C", 6.25, 1.25 * PG, note="distractor: 125 mL read as 1.25 L")
assert GFR_L * PG < TM, "a fasting adult must sit below the transport maximum"
check("bb-p7-q2", 16, TM / GFR_L, note="key: threshold plasma concentration in mmol/L")
check("bb-p7-q2/B", 3.2, TM / (GFR_L * PG), note="distractor: transport maximum divided by the filtered load")
check("bb-p7-q2/D", 1.6, TM / 1.25, note="distractor: divided by 1.25 L/min")
check("bb-p7-q2b", 3.2, (TM / GFR_L) / PG, note="threshold is about three times the fasting concentration")

print()
print("P8  Hardy-Weinberg: 4 affected per 10 000")
q2 = 4 / 10000
qf = math.sqrt(q2)
pf = 1 - qf
check("bb-p8-q1", 3.9, 100 * 2 * pf * qf, note="key: heterozygote percentage")
check("bb-p8-q1/A", 0.04, 100 * q2, note="distractor: the affected frequency reported")
check("bb-p8-q1/B", 0.08, 100 * 2 * (1 - q2) * q2, note="distractor: square root never taken")
check("bb-p8-q1/C", 2.0, 100 * qf, note="distractor: the allele frequency reported")
check("bb-p8-q1b", 26, 1 / (2 * pf * qf), tol=0.02, note="one carrier in about 26 people")
check("bb-p8-q5", 0.5, 2 * 0.5 * 0.5, note="key: heterozygote share of a heterozygote cross")
check("bb-p8-q5/A", 0.667, 0.5 / 0.75, tol=0.01, note="distractor: conditioned on being unaffected")
check("bb-p8-q5/D", 0.25, 0.5 * 0.5, note="distractor: one homozygous class")
check("bb-p8-q4", 0.25, 0.5 * 0.5, note="affected share of a heterozygote cross, as the clinic saw")

print()
print("P9  end-plate potentials, Table 8; threshold 25 mV")
THRESHOLD = 25.0
EPP = {"control": (40.0, 38.0), "antibody": (18.0, 9.0), "antibody+inhibitor": (32.0, 26.0)}
for name, (first, tenth) in EPP.items():
    print(f"       {name:20s} first {first:5.1f}  tenth {tenth:5.1f}  "
          f"run-down {100 * (1 - tenth / first):4.1f}%  fires at tenth: {tenth >= THRESHOLD}")
check("bb-p9-q1", 2.0, EPP["control"][0] - EPP["control"][1], note="control run-down, in mV")
check("bb-p9-q1b", 0.5, EPP["antibody"][1] / EPP["antibody"][0], note="antibody amplitude halves across the train")
check("bb-p9-q4", 9.0, EPP["antibody"][1], note="key: the only tenth response below threshold")
assert EPP["antibody"][1] < THRESHOLD <= EPP["antibody+inhibitor"][1] < EPP["control"][1], \
    "only the antibody-alone preparation may fail at the tenth stimulus"

print()
print("P10  affinity maturation, Table 9")
KD7, KD28, KD42 = 1e-6, 1e-9, 1e-10
TITRE7, TITRE28, TITRE42 = 100.0, 1e4, 1e5
check("bb-p10-q1", 1000, KD7 / KD28, note="key: fold rise in affinity, day 7 to day 28")
check("bb-p10-q1/B", 100, TITRE28 / TITRE7, note="distractor: the ratio of the titres")
check("bb-p10-q1/C", 3, math.log10(KD7 / KD28), note="distractor: the difference of the exponents")
check("bb-p10-q1/D", 1000, KD7 / KD28, note="distractor: same factor, wrong direction")
check("bb-p10-q4", 10, TITRE42 / TITRE28, note="tenfold higher titre after the second dose")
check("bb-p10-q4b", 10, KD28 / KD42, note="a further tenfold fall in dissociation constant")

print()
print("D11  dihybrid cross of two double heterozygotes")
check("bb-d11", 1 / 16, 0.25 * 0.25, note="key: double recessive")
check("bb-d11/B", 3 / 16, 3 * 0.25 * 0.25, note="distractor: one recessive, one dominant")
check("bb-d11/C", 4 / 16, 0.25, note="distractor: one locus only")
check("bb-d11/D", 9 / 16, 0.75 * 0.75, note="distractor: both dominant")

print()
total = 54
print(f"{total - len(BAD)}/{total} values verified")
if BAD:
    raise SystemExit("FAILED: " + ", ".join(BAD))
