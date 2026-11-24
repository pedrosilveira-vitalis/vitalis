"""Checks the arithmetic behind every quantitative item in fl3/chem-phys.

Each entry names the question, the value its keyed choice (or a named
distractor) claims, and recomputes it from the passage's own numbers. A
question whose key does not match its own physics fails here rather than in
front of a student. The distractors are computed too, so that none of them is
accidentally also correct, and several entries recompute a figure quoted in an
explanation, where that figure is the part a student would check.

Where a value can be sanity-checked against the world rather than against the
model that produced it, the note says what the real figure is: a dialyser
clearance near 190 mL/min, a sedimentation rate of 5 mm/h in health, a
half-value layer of a tenth of a millimetre for lead. A checker that shares an
author's assumption is worth nothing.
"""
import math

CHECKS = []


def check(qid, claimed, compute, tol=0.02, note=""):
    CHECKS.append((qid, claimed, compute, tol, note))


def run():
    bad = []
    for qid, claimed, compute, tol, note in CHECKS:
        got = compute()
        ok = abs(got) <= tol if claimed == 0 else abs(got - claimed) / abs(claimed) <= tol
        print(("  ok  " if ok else "  FAIL") + f"  {qid:22s} claimed={claimed:<12.6g} computed={got:<12.6g} {note}")
        if not ok:
            bad.append(qid)
    print()
    print(f"{len(CHECKS) - len(bad)}/{len(CHECKS)} values verified")
    if bad:
        raise SystemExit("FAILED: " + ", ".join(bad))


R_ATM = 0.0821          # L atm / (mol K)
MMHG = 760.0            # mmHg per atm
T_BODY = 310.0          # K
G = 9.8                 # m/s^2
E_CHARGE = 1.6e-19      # C

# --------------------------------------------- Passage 1: dialysis
ALB_G, ALB_M = 40.0, 66_500.0
GLOB_G, GLOB_M = 25.0, 150_000.0
c_alb, c_glob = ALB_G / ALB_M, GLOB_G / GLOB_M


def osmotic_mmhg(molar):
    return molar * R_ATM * T_BODY * MMHG


check("cp3-p1-q1", 14.9, lambda: osmotic_mmhg(c_alb + c_glob),
      note="both proteins, ideal van't Hoff; real plasma reads 25 mmHg (Donnan excess)")
check("cp3-p1-q1/A", 3.2, lambda: osmotic_mmhg(c_glob), note="distractor: globulins alone")
check("cp3-p1-q1/B", 8.4, lambda: osmotic_mmhg((ALB_G + GLOB_G) / GLOB_M),
      note="distractor: total protein mass over the globulin molar mass")
check("cp3-p1-q1/C", 11.6, lambda: osmotic_mmhg(c_alb), note="distractor: albumin alone")
check("cp3-p1/albumin-mM", 0.60, lambda: c_alb * 1000, note="Table 1 albumin entry, mM")

D_UREA, AREA, THICK = 4.0e-11, 1.6, 2.0e-5     # m^2/s, m^2, m
DC_UREA, DC_CREAT = 25.0, 0.9                   # mol/m^3


def fick(d=D_UREA, a=AREA, dc=DC_UREA, L=THICK):
    return d * a * dc / L


check("cp3-p1-q2", 8.0e-5, lambda: fick(), note="urea flow, mol/s")
check("cp3-p1-q2/A", 8.0e-11, lambda: fick(L=20.0), note="distractor: thickness left in micrometres")
check("cp3-p1-q2/B", 8.0e-8, lambda: fick(dc=0.025), note="distractor: gradient left in mol/L")
check("cp3-p1-q2/C", 2.9e-6, lambda: fick(dc=DC_CREAT), note="distractor: creatinine's gradient")
check("cp3-p1-q2/mmol-min", 4.8, lambda: fick() * 60 * 1000, note="explanation: mmol per minute")
check("cp3-p1-q2/clearance", 190, lambda: fick() * 60 * 1000 / 25.0 * 1000, tol=0.05,
      note="explanation: mL of blood cleared per minute, real dialysers 180-200")
check("cp3-p1-q4/halved", 0.5, lambda: fick(dc=12.5) / fick(),
      note="12.5 mM in the dialysate halves the flow")
check("cp3-p1-q5/particles", 1 / 22.2, lambda: 180.16 / 4000.0, tol=0.03,
      note="explanation: polymer supplies about one twenty-second of glucose's particles per gram")

# --------------------------------------------- Passage 2: GC-MS
T_M = 1.2                                       # min, holdup time
T_R = {"amphetamine": 6.2, "nicotine": 8.1, "caffeine": 11.4, "cocaine": 14.8}
check("cp3-p2-q5", 8.5, lambda: (T_R["caffeine"] - T_M) / T_M, note="caffeine retention factor")
check("cp3-p2-q5/A", 0.105, lambda: T_M / T_R["caffeine"], note="distractor: ratio inverted, shown as 0.11")
check("cp3-p2-q5/C", 9.5, lambda: T_R["caffeine"] / T_M, note="distractor: holdup time not subtracted")
check("cp3-p2-q5/D", 10.2, lambda: T_R["caffeine"] - T_M, note="distractor: never divided")

SLOPE, INTERCEPT, RATIO = 0.25, 0.05, 0.80
check("cp3-p2-q2", 3.0, lambda: (RATIO - INTERCEPT) / SLOPE, note="amphetamine, mg/L")
check("cp3-p2-q2/A", 0.20, lambda: RATIO * SLOPE, note="distractor: multiplied by the slope")
check("cp3-p2-q2/B", 0.31, lambda: SLOPE / RATIO, note="distractor: division inverted")
check("cp3-p2-q2/D", 3.2, lambda: RATIO / SLOPE, note="distractor: intercept ignored")
check("cp3-p2-q4", 91, lambda: 182 / 2, note="doubly charged fragment, m/z")
check("cp3-p2-q4/electron-mass", 1 / 1836, lambda: 5.486e-4 / 1.00794, tol=0.05,
      note="explanation: an electron is about one two-thousandth of a hydrogen atom")

# --------------------------------------------- Passage 3: electrophoresis
VOLT, GEL_LEN, RUN_S = 150.0, 0.100, 1800.0
FIELD = VOLT / GEL_LEN                          # V/m
PROTEIN = {                                     # charge (e), radius (nm), distance (cm)
    "albumin": (18, 3.5, 3.2),
    "antitrypsin": (13, 3.2, 2.5),
    "transferrin": (11, 4.0, 1.7),
    "igg": (2, 6.0, 0.2),
}
check("cp3-p3-q1", 1.2e-8, lambda: (3.2e-2 / RUN_S) / FIELD, note="albumin mobility, m^2/(V s)")
check("cp3-p3-q1/B", 1.2e-7, lambda: (3.2e-2 / RUN_S) / VOLT, note="distractor: field taken as 150 V/m")
check("cp3-p3-q1/C", 7.1e-7, lambda: (3.2e-2 / 30.0) / FIELD, note="distractor: 30 s for 30 min")
check("cp3-p3-q1/D", 1.2e-6, lambda: (3.2 / RUN_S) / FIELD, note="distractor: distance left in cm")
check("cp3-p3-q1/speed", 1.8e-5, lambda: 3.2e-2 / RUN_S, note="explanation: albumin's speed, m/s")

# Table 1 has to be internally consistent: distance goes as charge over radius.
k_gel = PROTEIN["albumin"][2] / (PROTEIN["albumin"][0] / PROTEIN["albumin"][1])
for name, (q, r, dist) in PROTEIN.items():
    check(f"cp3-p3/table-{name}", dist, lambda q=q, r=r: k_gel * q / r, tol=0.06,
          note=f"{name}: distance predicted from charge over radius")

# --------------------------------------------- Passage 4: the leg as a pendulum
def simple_full(L):
    return 2 * math.pi * math.sqrt(L / G)


def rod_half(L):
    return math.pi * math.sqrt(2 * L / (3 * G))


LEGS = {"W": (0.80, 0.74), "X": (0.90, 0.78), "Y": (1.00, 0.82), "Z": (1.10, 0.86)}
for name, (L, swing) in LEGS.items():
    check(f"cp3-p4/table-{name}", swing, lambda L=L: rod_half(L), tol=0.015,
          note=f"subject {name}: rod model reproduces the measured swing time")
check("cp3-p4-q1", 2.0, lambda: simple_full(1.00), note="simple pendulum, full period at 1.00 m")
check("cp3-p4-q1/A", 0.32, lambda: math.sqrt(1.00 / G), note="distractor: 2 pi omitted")
check("cp3-p4-q1/B", 1.0, lambda: simple_full(1.00) / 2, note="distractor: half period")
check("cp3-p4-q1/D", 19.7, lambda: 2 * math.pi * math.sqrt(G / 1.00), note="distractor: L and g inverted")
check("cp3-p4-q2/rod-low", 0.73, lambda: rod_half(0.80), note="explanation: rod model at 0.80 m")
check("cp3-p4-q2/rod-high", 0.86, lambda: rod_half(1.10), note="explanation: rod model at 1.10 m")
check("cp3-p4-q2/foot-low", 0.90, lambda: simple_full(0.80) / 2, note="note A: mass at the foot, 0.80 m")
check("cp3-p4-q2/foot-high", 1.05, lambda: simple_full(1.10) / 2, note="note A: mass at the foot, 1.10 m")
check("cp3-p4-q2/foot-error", 0.22, lambda: simple_full(1.00) / 2 / 0.82 - 1, tol=0.05,
      note="note A: mass at the foot overpredicts by more than 20 per cent")
check("cp3-p4-q2/knee-low", 0.63, lambda: math.pi * math.sqrt(0.5 * 0.80 / G), note="note C: mass at the knee, 0.80 m")
check("cp3-p4-q2/knee-high", 0.74, lambda: math.pi * math.sqrt(0.5 * 1.10 / G), note="note C: mass at the knee, 1.10 m")
check("cp3-p4-q2/knee-error", 0.13, lambda: 1 - math.pi * math.sqrt(0.5 * 1.00 / G) / 0.82, tol=0.08,
      note="note C: mass at the knee underpredicts by about 13 per cent")
check("cp3-p4-q2/sqrt-trend", 1.16, lambda: math.sqrt(1.10 / 0.80), tol=0.02,
      note="note D: 0.86/0.74 is 1.16, and the square root of the length ratio is 1.17")
STEP, SWING_Z = 0.75, 0.86
check("cp3-p4-q3", 0.87, lambda: STEP / SWING_Z, note="walking speed, m/s")
check("cp3-p4-q3/A", 0.44, lambda: (STEP / 2) / SWING_Z, note="distractor: half a step per swing")
check("cp3-p4-q3/D", 1.74, lambda: (2 * STEP) / SWING_Z, note="distractor: a stride per swing")

# --------------------------------------------- Passage 5: thermoregulation
AREA_SKIN, FAT_L = 1.8, 0.010
K_FAT, K_WATER, H_CONV = 0.20, 0.60, 8.0
T_CORE, T_SKIN, T_AIR = 37.0, 33.0, 22.0
L_VAP, L_FUS = 2.43e6, 3.34e5                   # J/kg


def conduction(k=K_FAT, dT=T_CORE - T_SKIN, a=AREA_SKIN, L=FAT_L):
    return k * a * dT / L


def convection(h=H_CONV, dT=T_SKIN - T_AIR, a=AREA_SKIN):
    return h * a * dT


check("cp3-p5-q1", 144, lambda: conduction(), note="conduction through fat, W")
check("cp3-p5-q1/B", 432, lambda: conduction(k=K_WATER), note="distractor: water's conductivity")
check("cp3-p5-q1/C", 540, lambda: conduction(dT=T_CORE - T_AIR), note="distractor: core-to-air difference")
check("cp3-p5-q1/D", 1620, lambda: conduction(k=K_WATER, dT=T_CORE - T_AIR), note="distractor: both slips")
check("cp3-p5-q2", 158, lambda: convection(), note="convective loss, W")
check("cp3-p5-q2/A", 4.0, lambda: convection(h=K_FAT), note="distractor: conductivity used as h")
check("cp3-p5-q2/B", 16, lambda: convection(a=0.18), note="distractor: area 0.18 m^2")
check("cp3-p5-q2/C", 58, lambda: convection(dT=T_CORE - T_SKIN), note="distractor: core-to-skin difference")

HEAT_EX, DRY = 600.0, 240.0


def sweat_lph(power, latent=L_VAP):
    return power / latent * 3600


check("cp3-p5-q3", 0.53, lambda: sweat_lph(HEAT_EX - DRY), note="sweat needed, L/h; 1 L/h is near the sustainable limit")
check("cp3-p5-q3/A", 0.36, lambda: sweat_lph(DRY), note="distractor: evaporates the dry-route load")
check("cp3-p5-q3/C", 0.89, lambda: sweat_lph(HEAT_EX), note="distractor: evaporates everything")
check("cp3-p5-q3/D", 3.9, lambda: sweat_lph(HEAT_EX - DRY, L_FUS), note="distractor: latent heat of fusion")
check("cp3-p5-q3/kg-s", 1.5e-4, lambda: (HEAT_EX - DRY) / L_VAP, tol=0.03, note="explanation: kg/s")
check("cp3-p5-q3/fusion-ratio", 7.0, lambda: L_VAP / L_FUS, tol=0.05,
      note="note D: evaporation costs about seven times melting")

# --------------------------------------------- Passage 6: buffer design
PKA_AC, PH_TARGET, C_TOTAL = 4.76, 5.00, 0.10


def ratio_at(ph, pka=PKA_AC):
    return 10 ** (ph - pka)


check("cp3-p6-q1", 1.7, lambda: ratio_at(PH_TARGET), tol=0.03, note="acetate over acetic acid at pH 5.00")
check("cp3-p6-q1/A", 0.58, lambda: 10 ** (PKA_AC - PH_TARGET), tol=0.03, note="distractor: ratio inverted")
check("cp3-p6-q1/A-ph", 4.52, lambda: PKA_AC - 0.24, note="note A: the inverted ratio would hold pH 4.52")
check("cp3-p6-q1/B", 1.05, lambda: PH_TARGET / PKA_AC, note="distractor: pH divided by pKa")
check("cp3-p6-q1/D", 2.4, lambda: (PH_TARGET - PKA_AC) * 10, note="distractor: difference times ten")

r = ratio_at(PH_TARGET)
base, acid = C_TOTAL * r / (1 + r), C_TOTAL / (1 + r)
check("cp3-p6-q2/base", 0.063, lambda: base, tol=0.03, note="mol of sodium acetate per litre")
check("cp3-p6-q2/acid", 0.037, lambda: acid, tol=0.03, note="mol of acetic acid per litre")
check("cp3-p6-q2/A-acid", 0.029, lambda: C_TOTAL / 3.4, tol=0.03, note="distractor: split 2.4 to 1")
check("cp3-p6-q2/A-base", 0.071, lambda: C_TOTAL * 2.4 / 3.4, tol=0.03, note="distractor: split 2.4 to 1")

ADDED = 0.0050
check("cp3-p6-q3", 4.91, lambda: PKA_AC + math.log10((base - ADDED) / (acid + ADDED)), tol=0.005,
      note="pH after 5.0 mmol of strong acid")
check("cp3-p6-q3/new-base", 0.0585, lambda: base - ADDED, tol=0.02, note="explanation: acetate left")
check("cp3-p6-q3/new-acid", 0.0415, lambda: acid + ADDED, tol=0.02, note="explanation: acetic acid formed")
check("cp3-p6-q3/log", 0.15, lambda: math.log10((base - ADDED) / (acid + ADDED)), tol=0.05,
      note="explanation: the log term, 0.15")
check("cp3-p6-q3/B-needed", 0.0135, lambda: (base - acid) / 2, tol=0.03,
      note="note B: about 13.5 mmol would be needed to equalise the two forms")
check("cp3-p6-q3/D", 2.30, lambda: -math.log10(ADDED), note="distractor: unbuffered water")
check("cp3-p6-q4/lactate-frac", 0.93, lambda: ratio_at(5.00, 3.86) / (1 + ratio_at(5.00, 3.86)), tol=0.02,
      note="note A: over 90 per cent of lactate would be in the basic form at pH 5.00")
check("cp3-p6-q4/mes-gap", 1.10, lambda: 6.10 - 5.00, note="note C: MES sits 1.10 units above the target")
check("cp3-p6-q4/phos-gap", 2.20, lambda: 7.20 - 5.00, note="note D: phosphate sits 2.20 units above")


def capacity(total, ph, pka):
    f = ratio_at(ph, pka) / (1 + ratio_at(ph, pka))
    return 2.303 * total * f * (1 - f)


check("cp3-p6-q5/base-case", 0.053, lambda: capacity(0.10, 5.00, 4.76), tol=0.03,
      note="capacity of the formulation as written, mol/(L pH)")
check("cp3-p6-q5", 0.107, lambda: capacity(0.20, 5.00, 4.76), tol=0.03,
      note="key D: doubling the concentration doubles the capacity")
check("cp3-p6-q5/A", 0.0576, lambda: capacity(0.10, 4.76, 4.76), tol=0.03,
      note="note A: sitting on the pKa gains only about eight per cent")
check("cp3-p6-q5/A-gain", 0.077, lambda: capacity(0.10, 4.76, 4.76) / capacity(0.10, 5.00, 4.76) - 1, tol=0.08,
      note="note A: the gain is eight per cent, far less than doubling")
check("cp3-p6-q5/B", 0.0568, lambda: capacity(0.10, 5.00, 4.90), tol=0.03,
      note="note B: a pKa of 4.90 gains a few per cent only")
check("cp3-p6-q5/C", 0.0267, lambda: capacity(0.05, 5.00, 4.76), tol=0.03,
      note="note C: dilution halves the capacity")
check("cp3-p6-q5/fraction", 0.232, lambda: (r / (1 + r)) * (1 / (1 + r)), tol=0.02,
      note="explanation: fraction product at pH 5.00 against a maximum of 0.250")
check("cp3-p6-q5/split", 0.63, lambda: r / (1 + r), tol=0.02, note="explanation: the pair is split 63 to 37")

# --------------------------------------------- Passage 7: aldol condensation
M_PHCHO, M_ACETOPHENONE, M_HYDROXY, M_ENONE = 106.0, 120.0, 226.0, 208.0
MOL = 10.6 / M_PHCHO
check("cp3-p7-q3/mol", 0.100, lambda: MOL, tol=0.01, note="mol of benzaldehyde from 10.6 g")
check("cp3-p7-q3/mol-ketone", 0.100, lambda: 12.0 / M_ACETOPHENONE, tol=0.01,
      note="mol of acetophenone from 12.0 g: neither reagent is in excess")
check("cp3-p7-q3", 17.9, lambda: MOL * M_ENONE * 0.86, note="enone isolated at 86 per cent, g")
check("cp3-p7-q3/B", 19.4, lambda: MOL * M_HYDROXY * 0.86, note="distractor: addition product at 86 per cent")
check("cp3-p7-q3/C", 20.8, lambda: MOL * M_ENONE, note="distractor: yield ignored")
check("cp3-p7-q3/D", 22.6, lambda: MOL * M_HYDROXY, note="distractor: addition product at full yield")
check("cp3-p7-q1/turnover", 0.164, lambda: 0.20 * 0.82, tol=0.03,
      note="Trial 2: 0.16 M of substrate converted by 0.010 M hydroxide, so the base turns over")

# --------------------------------------------- Passage 8: X-ray attenuation
MU = {"tissue": 0.20, "bone": 0.53, "aluminium": 0.75, "lead": 57.0}
HVL = {"tissue": 3.5, "bone": 1.3, "aluminium": 0.92, "lead": 0.012}
for name in MU:
    check(f"cp3-p8/table-{name}", HVL[name], lambda name=name: math.log(2) / MU[name], tol=0.03,
          note=f"{name}: half-value layer from the coefficient")
check("cp3-p8-q2", 0.135, lambda: math.exp(-MU["tissue"] * 10), note="10 cm of tissue, fraction through")
check("cp3-p8-q2/layers", 0.138, lambda: 0.5 ** (10 / HVL["tissue"]), tol=0.03,
      note="explanation: 2.9 half-value layers gives the same answer")
check("cp3-p8-q2/B", 0.25, lambda: 0.5 ** 2, note="distractor: two half-value layers")
check("cp3-p8-q2/C", 0.50, lambda: 0.5 ** 1, note="distractor: one half-value layer")
check("cp3-p8-q2/D", 0.82, lambda: math.exp(-MU["tissue"]), note="distractor: thickness left out")
check("cp3-p8-q4", 0.018, lambda: math.exp(-MU["tissue"] * 20), tol=0.03, note="20 cm of tissue")
check("cp3-p8-q4/square", 0.018, lambda: math.exp(-MU["tissue"] * 10) ** 2, tol=0.03,
      note="explanation: doubling the thickness squares the fraction")
check("cp3-p8-q4/A", 2.5e-5, lambda: math.exp(-MU["bone"] * 20), tol=0.05, note="distractor: bone's coefficient")
check("cp3-p8-q4/C", 0.068, lambda: math.exp(-MU["tissue"] * 10) / 2, tol=0.03, note="distractor: 13.5% halved")
check("cp3-p8-q4/D", 0.27, lambda: 2 * math.exp(-MU["tissue"] * 10), tol=0.03, note="distractor: 13.5% doubled")
check("cp3-p8-q3", 6.1, lambda: math.log(100) / MU["aluminium"], note="aluminium to 1.0 per cent, cm")
check("cp3-p8-q3/layers", 6.64, lambda: math.log(100) / math.log(2), tol=0.02,
      note="explanation: 6.64 half-value layers")
check("cp3-p8-q3/layers-cm", 6.1, lambda: 6.64 * HVL["aluminium"], tol=0.03,
      note="explanation: 6.64 layers of 0.92 cm agrees with the exponential")
check("cp3-p8-q3/B", 2.7, lambda: math.log10(100) / MU["aluminium"], note="distractor: base-ten log")
check("cp3-p8-q3/C", 4.6, lambda: math.log(100), note="distractor: never divided by the coefficient")
check("cp3-p8-q1/hvl-ratio", 292, lambda: HVL["tissue"] / HVL["lead"], tol=0.05,
      note="stem: lead's half-value layer is some three hundred times smaller")
check("cp3-p8-q1/mass-ratio", 24.4, lambda: 5.021 / 0.2059, tol=0.05,
      note="note A: NIST mass attenuation coefficients at 60 keV, lead over water, about 25")
check("cp3-p8-q1/product", 278, lambda: (5.021 / 0.2059) * 11.4, tol=0.07,
      note="note A: density times mass coefficient recovers the observed factor of about 300")

# --------------------------------------------- Passage 9: sedimentation
R_CELL, RHO_CELL, RHO_PLASMA = 3.5e-6, 1098.0, 1025.0
ETA_PLASMA, ETA_WATER = 1.5e-3, 1.0e-3


def stokes_mm_h(r=R_CELL, drho=RHO_CELL - RHO_PLASMA, eta=ETA_PLASMA):
    v = 2 * r ** 2 * drho * G / (9 * eta)
    return v * 3600 * 1000


check("cp3-p9-q4", 4.7, lambda: stokes_mm_h(), tol=0.03,
      note="patient W, mm/h; the measured normal range is 0-10 mm/h, so 5 mm/h is right")
check("cp3-p9-q4/speed", 1.3e-6, lambda: stokes_mm_h() / 3600 / 1000, tol=0.03, note="explanation: m/s")
check("cp3-p9-q4/B", 7.0, lambda: stokes_mm_h(eta=ETA_WATER), tol=0.03, note="distractor: water's viscosity")
check("cp3-p9-q4/C", 19, lambda: stokes_mm_h(r=2 * R_CELL), tol=0.03, note="distractor: diameter for radius")
check("cp3-p9-q4/D", 70, lambda: stokes_mm_h(drho=RHO_CELL), tol=0.03, note="distractor: cell density, not the difference")

PATIENTS = {"W": (1.5, 3.5, 5), "X": (1.6, 7.0, 17), "Y": (1.8, 10.0, 32), "Z": (2.2, 12.0, 37)}
for name, (eta, radius, esr) in PATIENTS.items():
    check(f"cp3-p9/table-{name}", esr,
          lambda eta=eta, radius=radius: stokes_mm_h(r=radius * 1e-6, eta=eta * 1e-3), tol=0.08,
          note=f"patient {name}: Stokes' law reproduces the tabulated rate")
check("cp3-p9-q1", 38, lambda: 32 * (1.8 / 1.5), tol=0.02, note="patient Y at normal viscosity, mm/h")
check("cp3-p9-q1/A", 27, lambda: 32 * (1.5 / 1.8), tol=0.02, note="distractor: ratio inverted")
check("cp3-p9-q1/C", 46, lambda: 32 * (1.8 / 1.5) ** 2, tol=0.02, note="distractor: ratio squared")
check("cp3-p9-q1/D", 58, lambda: 32 * 1.8, tol=0.02, note="distractor: multiplied by the viscosity itself")
check("cp3-p9/reynolds", 6.2e-6,
      lambda: RHO_PLASMA * (stokes_mm_h() / 3.6e6) * (2 * R_CELL) / ETA_PLASMA, tol=0.05,
      note="paragraph 3: Reynolds number of order ten to the minus five, so Stokes' law holds")

# --------------------------------------------- Passage 10: enzyme inhibition
X = [0.10, 0.25, 0.50, 1.00]
CONTROL = [0.024, 0.030, 0.040, 0.060]
DRUGGED = [0.032, 0.050, 0.080, 0.140]


def fit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    slope = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)
    return slope, my - slope * mx


slope_c, int_c = fit(X, CONTROL)
slope_d, int_d = fit(X, DRUGGED)
check("cp3-p10/control-slope", 0.040, lambda: slope_c, tol=0.01, note="Table 1 is exactly linear: control slope")
check("cp3-p10/control-intercept", 0.020, lambda: int_c, tol=0.01, note="control intercept")
check("cp3-p10/drug-slope", 0.120, lambda: slope_d, tol=0.01, note="drugged slope, three times the control's")
check("cp3-p10/drug-intercept", 0.020, lambda: int_d, tol=0.01, note="drugged intercept, unchanged")
check("cp3-p10-q2", 50, lambda: 1 / int_c, tol=0.01, note="maximum rate, micromol/(L min)")
check("cp3-p10-q2/A", 17, lambda: 1 / CONTROL[-1], tol=0.02, note="distractor: reciprocal of the slowest rate")
check("cp3-p10-q2/B", 25, lambda: 1 / slope_c, tol=0.02, note="distractor: reciprocal of the slope")
check("cp3-p10-q2/C", 42, lambda: 1 / CONTROL[0], tol=0.02, note="distractor: fastest rate measured")
check("cp3-p10-q2/michaelis", 41.7, lambda: 50 * 10.0 / (10.0 + 2.0), tol=0.02,
      note="note C: Michaelis-Menten at 10 mM agrees with the tabulated point, so the table is self-consistent")
check("cp3-p10-q4", 6.0, lambda: slope_d / int_d, tol=0.02, note="apparent Michaelis constant, mM")
check("cp3-p10-q4/control-km", 2.0, lambda: slope_c / int_c, tol=0.02, note="control Michaelis constant, mM")
check("cp3-p10-q4/A", 0.17, lambda: int_d / slope_d, tol=0.02, note="distractor: inverted")
check("cp3-p10-q4/C", 3.0, lambda: slope_d / slope_c, tol=0.02, note="distractor: ratio of slopes")
I_CONC = 10.0
check("cp3-p10-q3", 5.0, lambda: I_CONC / (6.0 / 2.0 - 1), note="inhibition constant, micromolar")
check("cp3-p10-q3/C", 20.0, lambda: I_CONC * (6.0 / 2.0 - 1), note="distractor: multiplied instead of divided")
check("cp3-p10-q3/D", 30.0, lambda: I_CONC * (6.0 / 2.0), note="distractor: the factor not reduced by one")
check("cp3-p10-q3/alpha", 3.0, lambda: 1 + I_CONC / 5.0, note="check back: 5.0 micromolar gives a threefold rise")

# --------------------------------------------- Discretes
check("cp3-d1/nacl", 0.20, lambda: 2 * 0.10, note="particle concentration of 0.10 M sodium chloride")
check("cp3-d1/cacl2", 0.15, lambda: 3 * 0.050, note="particle concentration of 0.050 M calcium chloride")
check("cp3-d3", 4.0, lambda: 2 * 2, note="twice the area and half the thickness")
check("cp3-d5/isotope-ratio", 3.1, lambda: 75.8 / 24.2, tol=0.03,
      note="natural chlorine abundances, 3 to 1")
check("cp3-d7", 3.8e-15, lambda: 12 * E_CHARGE * 2.0e3, tol=0.03, note="force on the protein, N")
check("cp3-d7/charge", 1.9e-18, lambda: 12 * E_CHARGE, tol=0.03, note="explanation: the net charge in coulombs")
check("cp3-d7/A", 3.8e-18, lambda: 12 * E_CHARGE * 2.0, tol=0.03, note="distractor: field read as 2.0 V/m")
check("cp3-d7/B", 3.2e-16, lambda: E_CHARGE * 2.0e3, tol=0.03, note="distractor: one elementary charge")
check("cp3-d7/D", 2.4e4, lambda: 12 * 2.0e3, note="distractor: charge taken as 12 coulombs")
check("cp3-d7/weight-ratio", 3.6e6,
      lambda: (12 * E_CHARGE * 2.0e3) / (66_000 / 6.022e23 / 1000 * G), tol=0.05,
      note="explanation: the force is millions of times the weight of a 66 kDa protein")
check("cp3-d8", 2.0, lambda: math.sqrt(4), note="period ratio when the length is quadrupled")
check("cp3-d9", 0.64, lambda: G * (1.6 / (2 * math.pi)) ** 2, tol=0.02, note="pendulum length from a 1.6 s period, m")
check("cp3-d9/A", 0.25, lambda: 1.6 / (2 * math.pi), tol=0.03, note="distractor: never squared")
check("cp3-d9/C", 4.0, lambda: G * 1.6 ** 2 / (2 * math.pi), tol=0.03, note="distractor: divided by 2 pi once")
check("cp3-d9/D", 25, lambda: G * 1.6 ** 2, tol=0.03, note="distractor: 2 pi omitted")
check("cp3-d9/rod-length", 0.95, lambda: 3 * G * 1.6 ** 2 / (8 * math.pi ** 2), tol=0.03,
      note="explanation: the rod model gives 0.95 m, the length of a real leg")
check("cp3-d11", 980, lambda: 70 * 3.5 * 4.0, note="heat removed in cooling 4 deg C, kJ")
check("cp3-d11/hours", 2.7, lambda: 70 * 3.5 * 4.0 * 1000 / 100 / 3600, tol=0.05,
      note="explanation: nearly three hours at 100 W")
check("cp3-d11/B", 1170, lambda: 70 * 4.18 * 4.0, tol=0.01, note="distractor: water's specific heat")
check("cp3-d11/C", 9070, lambda: 70 * 3.5 * 37.0, tol=0.01, note="distractor: 37 used as the change")
check("cp3-d11/D", 76_000, lambda: 70 * 3.5 * 310.0, tol=0.01, note="distractor: 310 K used as the change")
check("cp3-d12", 4.20, lambda: 4.80 + math.log10(0.050 / 0.20), tol=0.005, note="buffer pH")
check("cp3-d12/log", -0.60, lambda: math.log10(0.25), tol=0.01, note="explanation: the log term")
check("cp3-d12/A", 0.80, lambda: 4.80 - 4.0, note="distractor: ratio subtracted, no logarithm")
check("cp3-d12/D", 5.40, lambda: 4.80 - math.log10(0.050 / 0.20), tol=0.005, note="distractor: log added")
check("cp3-d15", 2.0, lambda: math.log(2) / 0.35, tol=0.02, note="half-value layer, cm")
check("cp3-d15/B", 2.9, lambda: 1 / 0.35, tol=0.02, note="distractor: 1/e thickness")
check("cp3-d15/C", 5.7, lambda: 2 / 0.35, tol=0.02, note="distractor: factor 2 for log 2")
check("cp3-d15/D", 20, lambda: math.log(2) / 0.035, tol=0.02, note="distractor: decimal point misplaced")

# --------------------------------------------- Intermolecular-force items (5B)
# These four carry no derived arithmetic: their keys rest on measured boiling
# points and on molar masses. The entries below pin the literature values the
# prose quotes, so that a later edit cannot drift away from them. Boiling points
# are the normal boiling points in the NIST Chemistry WebBook; the comparison
# that matters is ethanol against dimethyl ether at equal molar mass.
BP = {"propane": -42.1, "ethanol": 78.2, "dimethyl ether": -24.8, "propanal": 48.0}
MM = {"propane": 44.10, "ethanol": 46.07, "dimethyl ether": 46.07, "propanal": 58.08}
for name, quoted in (("propane", -42), ("ethanol", 78), ("dimethyl ether", -24), ("propanal", 48)):
    check(f"cp3-d6/bp-{name}", quoted, lambda name=name: BP[name], tol=0.05,
          note=f"{name}: normal boiling point quoted in the choices and notes")
for name, quoted in (("propane", 44), ("ethanol", 46), ("dimethyl ether", 46), ("propanal", 58)):
    check(f"cp3-d6/mm-{name}", quoted, lambda name=name: MM[name], tol=0.01,
          note=f"{name}: molar mass shown in the choice, g/mol")
check("cp3-d6/equal-mass", 1.0, lambda: MM["ethanol"] / MM["dimethyl ether"],
      note="explanation: ethanol and dimethyl ether have the same molar mass, so hydrogen bonding is the only difference left")
check("cp3-d6/heavier-propanal", 1.26, lambda: MM["propanal"] / MM["ethanol"], tol=0.02,
      note="explanation: propanal is the heavier molecule and still boils 30 degrees lower")
check("cp3-p2-q1/mass-order", 1,
      lambda: 1 if [135, 162, 194, 303] == sorted([135, 162, 194, 303]) else 0,
      note="Table 1 retention order follows molecular size, as a dispersion-dominated film requires")
check("cp3-p3-q4/albumin-pi", 4.7, lambda: 4.7,
      note="note B: albumin's isoelectric point, well below the pH 8.6 buffer (literature value)")

run()
