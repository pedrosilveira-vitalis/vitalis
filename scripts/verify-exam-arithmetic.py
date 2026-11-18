"""Checks the arithmetic behind every quantitative exam question.

Each entry names the question, the value the keyed choice claims, and a lambda
that recomputes it from the passage's own numbers. A question whose key does
not match its own physics fails here rather than in front of a student.
"""
import math

CHECKS = []

def check(qid, claimed, compute, tol=0.02, note=""):
    CHECKS.append((qid, claimed, compute, tol, note))

def run():
    bad = []
    for qid, claimed, compute, tol, note in CHECKS:
        got = compute()
        if claimed == 0:
            ok = abs(got) <= tol
        else:
            ok = abs(got - claimed) / abs(claimed) <= tol
        print(("  ok  " if ok else "  FAIL") + f"  {qid:12s} claimed={claimed:<12.6g} computed={got:<12.6g} {note}")
        if not ok:
            bad.append(qid)
    print()
    print(f"{len(CHECKS) - len(bad)}/{len(CHECKS)} numeric keys verified")
    if bad:
        raise SystemExit("FAILED: " + ", ".join(bad))

# ---------------------------------------------------------------- Passage 1
# Bicarbonate buffer: pH = 6.1 + log([HCO3-] / (0.03 * PCO2))
def hh(bicarb, pco2):
    return 6.1 + math.log10(bicarb / (0.03 * pco2))

check("cp-p1-q1", 7.40, lambda: hh(24, 40), note="normal plasma, stated in passage")
check("cp-p1-q2", 7.32, lambda: hh(12, 24), note="compensated metabolic acidosis")
check("cp-p1-q4", 7.10, lambda: hh(24, 80), note="PCO2 doubled, bicarb held")
check("cp-p1-q4b", -0.30, lambda: hh(24, 80) - hh(24, 40), tol=0.05, note="the shift itself")

# ---------------------------------------------------------------- Passage 2
# Arrhenius: k = A exp(-Ea/RT); ratio of rates at two temperatures
R = 8.314
def arrhenius_ratio(ea_kj, t1, t2):
    ea = ea_kj * 1000
    return math.exp(-ea / R * (1 / t2 - 1 / t1))

# Ea = 50 kJ/mol, 298 K -> 310 K
check("cp-p2-q2", 2.19, lambda: arrhenius_ratio(50, 298, 310), tol=0.05,
      note="rate ratio 310K/298K at Ea=50kJ")
# Catalysed Ea 25 kJ/mol: rate enhancement at 310 K vs uncatalysed 50 kJ/mol
check("cp-p2-q3", 16300, lambda: math.exp((50000 - 25000) / (R * 310)), tol=0.1,
      note="halving Ea at body temperature")

# ---------------------------------------------------------------- Passage 3
# Poiseuille: Q goes as r^4 at fixed pressure gradient.
check("cp-p3-q1", 0.41, lambda: 0.8 ** 4, tol=0.02, note="20% radius loss -> flow fraction")

# Continuity acts on AREA: v2 = v1 * (A1/A2). The area is given directly as
# 40% of healthy, so the factor is 1/0.40 = 2.5 and nothing is squared.
RHO, V1, AREA_FRACTION = 1060.0, 0.30, 0.40
def v_narrow():
    return V1 / AREA_FRACTION
def bernoulli_drop():
    return 0.5 * RHO * (v_narrow() ** 2 - V1 ** 2)

check("cp-p3-q2", 0.75, v_narrow, note="continuity on area, not radius")
check("cp-p3-q3", 250, bernoulli_drop, tol=0.02, note="dynamic pressure drop in Pa")

# Each distractor must be the arithmetic of a named error, so no distractor is
# accidentally also correct.
check("cp-p3-q2-dA", 0.12, lambda: V1 * AREA_FRACTION, note="distractor: multiplied by 0.40")
check("cp-p3-q2-dC", 1.875, lambda: V1 * (1 / AREA_FRACTION) ** 2, tol=0.02, note="distractor: squared the area ratio")
check("cp-p3-q3-dA", 47.7, lambda: 0.5 * RHO * V1 ** 2, tol=0.02, note="distractor: healthy segment only")
check("cp-p3-q3-dC", 1816, lambda: 0.5 * RHO * ((V1 * (1 / AREA_FRACTION) ** 2) ** 2 - V1 ** 2), tol=0.02,
      note="distractor: squared area ratio then Bernoulli")

# ---------------------------------------------------------------- Passage 4
# Thin lens / corrective optics: P = 1/f, in dioptres, distances in metres
check("cp-p4-q1", -2.5, lambda: 1 / (-0.40), note="far point 40 cm -> lens power")
check("cp-p4-q2", 2.5, lambda: 1 / 0.25 - 1 / 0.667, tol=0.03,
      note="reading add for 25 cm with 66.7 cm near point")
# Magnification of a two-lens microscope: m = (L/f_o)(25/f_e) style estimate
check("cp-p4-q4", 400, lambda: (160 / 4) * (250 / 25), tol=0.02,
      note="objective x eyepiece, mm units")

run()
