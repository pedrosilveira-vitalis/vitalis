"""Checks the arithmetic behind every quantitative item in fl4/chem-phys.

Each entry names the question, the value its keyed choice (or a named
distractor) claims, and recomputes it from the passage's own numbers. A
question whose key does not match its own physics fails here rather than in
front of a student. Distractors are computed too, so none is accidentally
also correct, and the printed values are meant to be read against reality -
a checker that only shares the author's assumption is worth nothing.
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


R = 8.314            # J mol^-1 K^-1
F = 96485.0          # C per mol

# ------------------------------------------------- Passage 1: Raoult, distillation
# At 50 degC: hexane 400 torr, toluene 92 torr. Liquid is 0.60 hexane.
P_HEX, P_TOL = 400.0, 92.0
X_HEX, X_TOL = 0.60, 0.40
P_TOTAL = X_HEX * P_HEX + X_TOL * P_TOL
check("cp4-p1-q1", 277, lambda: P_TOTAL, note="total vapour pressure above the 0.60 mixture")
check("cp4-p1-q1/A", 215, lambda: X_TOL * P_HEX + X_HEX * P_TOL, note="distractor: mole fractions swapped")
check("cp4-p1-q1/B", 240, lambda: X_HEX * P_HEX, note="distractor: hexane term only")
check("cp4-p1-q1/C", 246, lambda: (P_HEX + P_TOL) / 2, note="distractor: unweighted average")
check("cp4-p1-q2", 0.87, lambda: X_HEX * P_HEX / P_TOTAL, note="hexane mole fraction in the vapour")
check("cp4-p1-q2/A", 0.13, lambda: X_TOL * P_TOL / P_TOTAL, tol=0.03, note="distractor: the toluene fraction")
check("cp4-p1-q2/C", 0.81, lambda: P_HEX / (P_HEX + P_TOL), note="distractor: ratio of the pure pressures")
check("cp4-p1-q4/excess", 300, lambda: 300.0, tol=0.0001, note="measured pressure stated in the passage")
check("cp4-p1-q4/gap", 23, lambda: 300.0 - P_TOTAL, tol=0.05, note="positive deviation, torr above Raoult")

# ------------------------------------------------- Passage 3: Beer-Lambert, fluorescence
EPS494, EPS450 = 7.3e4, 1.5e4      # M^-1 cm^-1
A494, PATH, DIL = 0.44, 1.00, 50.0
C_CUVETTE = A494 / (EPS494 * PATH)
check("cp4-p3-q2/cuvette", 6.0e-6, lambda: C_CUVETTE, note="concentration in the cuvette")
check("cp4-p3-q2", 3.0e-4, lambda: C_CUVETTE * DIL, note="stock concentration, 50-fold dilution undone")
check("cp4-p3-q2/A", 6.0e-6, lambda: C_CUVETTE, note="distractor: dilution ignored")
check("cp4-p3-q2/C", 1.5e-3, lambda: A494 / (EPS450 * PATH) * DIL, tol=0.03, note="distractor: the 450 nm absorptivity used")
check("cp4-p3-q2/D", 3.0e-3, lambda: A494 / (EPS494 * 0.100) * DIL, note="distractor: path read as 1.0 mm")
check("cp4-p3-q3/1nM", 7.3e-5, lambda: EPS494 * 1.0e-9 * 1.00, note="absorbance of a 1 nM solution, 1 cm")
check("cp4-p3-q3/10cm", 7.3e-4, lambda: EPS494 * 1.0e-9 * 10.0, note="distractor B: same in a 10 cm cell")
check("cp4-p3-q4", 0.64, lambda: 1 - 10 ** (-A494), note="fraction absorbed at A = 0.44")
check("cp4-p3-q4/A", 0.36, lambda: 10 ** (-A494), note="distractor: the transmitted fraction")
check("cp4-p3-q4/C", 0.56, lambda: 1 - A494, note="distractor: one minus the absorbance")
# Stokes shift: 494 nm absorbed, 519 nm emitted.
check("cp4-p3-q1/eV494", 2.51, lambda: 1240.0 / 494, note="photon energy at 494 nm, eV")
check("cp4-p3-q1/eV519", 2.39, lambda: 1240.0 / 519, note="photon energy at 519 nm, eV")

# ------------------------------------------------- Passage 4: torque at the jaw
F_MASSETER, D_MUSCLE = 700.0, 4.0            # N, cm from the joint
D_MOLAR, D_PRE, D_INCISOR = 7.0, 9.0, 12.0   # cm from the joint
bite = lambda d: F_MASSETER * D_MUSCLE / d
check("cp4-p4/table-molar", 400, lambda: bite(D_MOLAR), note="molar bite force, N")
check("cp4-p4/table-premolar", 311, lambda: bite(D_PRE), note="premolar bite force, N")
check("cp4-p4/table-incisor", 233, lambda: bite(D_INCISOR), note="incisor bite force, N")
check("cp4-p4-q1", 400, lambda: bite(D_MOLAR), note="key: molar bite force from a 700 N muscle force")
check("cp4-p4-q1/A", 233, lambda: bite(D_INCISOR), note="distractor: incisor arm used")
check("cp4-p4-q1/D", 1225, lambda: F_MASSETER * D_MOLAR / D_MUSCLE, note="distractor: lever arms inverted")
check("cp4-p4-q2/product", 2800, lambda: bite(D_MOLAR) * D_MOLAR, note="bite force x distance, constant")
check("cp4-p4-q2/product2", 2800, lambda: bite(D_INCISOR) * D_INCISOR, note="same product at the incisor")
check("cp4-p4-q3/advantage", 0.571, lambda: D_MUSCLE / D_MOLAR, note="mechanical advantage at the molar, below one")
check("cp4-p4-q4/B", 0.985, lambda: math.cos(math.radians(10)), note="key B: 10 deg tilt costs 1.5 percent")
check("cp4-p4-q4/A", 1.10, lambda: 1.10, tol=0.0001, note="distractor A: 10 percent more muscle force")
check("cp4-p4-q4/C", 1.167, lambda: D_MOLAR / 6.0, note="distractor C: biting 1 cm nearer the joint")
check("cp4-p4-q4/D", 1.10, lambda: 4.4 / D_MUSCLE, note="distractor D: insertion moved to 4.4 cm")

# ------------------------------------------------- Passage 5: glass electrode, Nernst
NERNST_25 = 2.303 * R * 298.15 / F * 1000     # mV per pH unit at 25 degC
NERNST_37 = 2.303 * R * 310.15 / F * 1000     # mV per pH unit at 37 degC
check("cp4-p5/nernst25", 59.2, lambda: NERNST_25, note="theoretical slope at 25 degC, mV per pH")
check("cp4-p5/nernst37", 61.5, lambda: NERNST_37, note="theoretical slope at 37 degC, mV per pH")
E4, E7, E10 = 177.0, 0.0, -177.0
SLOPE = (E4 - E10) / (10.00 - 4.00)
check("cp4-p5-q2", 59.0, lambda: SLOPE, note="key: measured slope from the three buffers")
check("cp4-p5-q2/B", 61.5, lambda: NERNST_37, note="distractor: theory at body temperature")
check("cp4-p5-q2/C", 118, lambda: (E4 - E10) / 3.0, note="distractor: the 354 mV range over 3 pH units")
check("cp4-p5-q2/D", 177, lambda: E4, note="distractor: the pH 4 reading quoted as a slope")
check("cp4-p5/RTF", 25.7, lambda: R * 298.15 / F * 1000, note="RT/F alone, the natural-log slip")
E_SAMPLE = 47.0
check("cp4-p5-q1", 6.20, lambda: 7.00 - E_SAMPLE / SLOPE, note="key: pH of a sample reading +47 mV")
check("cp4-p5-q1/A", 7.80, lambda: 7.00 + E_SAMPLE / SLOPE, note="distractor: sign of the offset reversed")
check("cp4-p5-q1/B", 6.60, lambda: 7.00 - E_SAMPLE / 118.0, note="distractor: 118 mV per pH used")
check("cp4-p5-q1/D", 5.41, lambda: 7.00 - E_SAMPLE / (SLOPE / 2), note="distractor: slope halved for two electrons")
# Blood at 37 degC read on an electrode calibrated at 25 degC, isopotential at pH 7.
E_BLOOD = -(7.40 - 7.00) * NERNST_37
check("cp4-p5-q4/mV", -24.6, lambda: E_BLOOD, note="potential of pH 7.40 blood at 37 degC, mV")
check("cp4-p5-q4", 0.017, lambda: (7.00 - E_BLOOD / SLOPE) - 7.40, note="key: reported pH too high by about 0.02")
check("cp4-p5-q4/C", 0.32, lambda: 7.40 * NERNST_37 / SLOPE - 7.40, note="distractor: whole pH value rescaled, 0.3")

# ------------------------------------------------- Passage 7: diffraction limit
abbe = lambda lam, na: lam / (2 * na)
check("cp4-p7/table-025", 1100, lambda: abbe(550, 0.25), note="Abbe limit, NA 0.25, nm")
check("cp4-p7/table-065", 423, lambda: abbe(550, 0.65), note="Abbe limit, NA 0.65, nm")
check("cp4-p7/table-125", 220, lambda: abbe(550, 1.25), note="Abbe limit, NA 1.25, nm")
check("cp4-p7/table-140", 196, lambda: abbe(550, 1.40), note="Abbe limit, NA 1.40, nm")
check("cp4-p7-q1", 196, lambda: abbe(550, 1.40), note="key: finest spacing, NA 1.40 at 550 nm")
check("cp4-p7-q1/B", 220, lambda: abbe(550, 1.25), note="distractor: the 1.25 oil row")
check("cp4-p7-q1/C", 393, lambda: 550 / 1.40, note="distractor: factor of two omitted")
check("cp4-p7-q1/D", 423, lambda: abbe(550, 0.65), note="distractor: the dry 0.65 row")
check("cp4-p7-q2", 161, lambda: abbe(450, 1.40), note="key: same objective at 450 nm")
check("cp4-p7-q2/A", 131, lambda: abbe(550, 1.40) * (450 / 550) ** 2, note="distractor: wavelength ratio squared")
check("cp4-p7-q2/D", 241, lambda: abbe(550, 1.40) * (550 / 450), note="distractor: ratio applied the wrong way")
check("cp4-p7-q4/blue", 0.18, lambda: 1 - abbe(450, 0.65) / abbe(550, 0.65), note="450 nm improves the dry lens 18 percent")
check("cp4-p7-q4/NA095", 0.32, lambda: 1 - abbe(550, 0.95) / abbe(550, 0.65), note="NA 0.95 improves it 32 percent")
check("cp4-p7-q5/gap", 196, lambda: abbe(550, 1.40), note="beads 150 nm apart sit below this limit")

# ------------------------------------------------- Passage 8: clearance and filtration
V_URINE = 1.2                                   # mL/min
clearance = lambda u, p: u * V_URINE / p
check("cp4-p8/table-inulin", 125, lambda: clearance(104.0, 1.0), note="inulin clearance, mL/min")
check("cp4-p8/table-creatinine", 140, lambda: clearance(117.0, 1.0), note="creatinine clearance, mL/min")
check("cp4-p8/table-urea", 65, lambda: clearance(1625.0, 30.0), note="urea clearance, mL/min")
check("cp4-p8/table-pah", 600, lambda: clearance(10.0, 0.020), note="PAH clearance, mL/min")
check("cp4-p8-q3", 65, lambda: clearance(1625.0, 30.0), note="key: urea clearance")
check("cp4-p8-q3/A", 0.022, lambda: 30.0 * V_URINE / 1625.0, note="distractor: ratio inverted")
check("cp4-p8-q3/B", 54, lambda: 1625.0 / 30.0, note="distractor: urine flow left out")
check("cp4-p8-q3/D", 1950, lambda: 1625.0 * V_URINE, note="distractor: plasma division left out")
P_GLOM, P_BOWMAN, PI_GLOM = 55.0, 15.0, 28.0
NFP = P_GLOM - P_BOWMAN - PI_GLOM
check("cp4-p8-q2", 12, lambda: NFP, note="key: net filtration pressure, mmHg")
check("cp4-p8-q2/A", 68, lambda: P_GLOM - P_BOWMAN + PI_GLOM, note="distractor: oncotic sign reversed")
check("cp4-p8-q2/B", 40, lambda: P_GLOM - P_BOWMAN, note="distractor: oncotic term dropped")
check("cp4-p8-q2/C", 27, lambda: P_GLOM - PI_GLOM, note="distractor: Bowman pressure dropped")
check("cp4-p8/Kf", 10.4, lambda: 125.0 / NFP, note="filtration coefficient implied, mL/min per mmHg")

# ------------------------------------------------- Passage 9: transition state theory
EA_UNCAT, EA_CAT, DH_RXN = 80.0, 50.0, -30.0    # kJ/mol
T_BODY = 310.0
check("cp4-p9-q1", 50, lambda: EA_CAT, tol=0.0001, note="key: catalysed forward barrier, kJ/mol")
check("cp4-p9-q1/reverse-uncat", 110, lambda: EA_UNCAT - DH_RXN, note="reverse barrier, uncatalysed")
check("cp4-p9-q1/reverse-cat", 80, lambda: EA_CAT - DH_RXN, note="reverse barrier, catalysed")
factor = lambda de, t: math.exp(de * 1000 / (R * t))
check("cp4-p9-q3", 1.1e5, lambda: factor(EA_UNCAT - EA_CAT, T_BODY), tol=0.05,
      note="key: rate enhancement from a 30 kJ/mol drop at 310 K")
check("cp4-p9-q3/A", 8.8e-6, lambda: 1 / factor(EA_UNCAT - EA_CAT, T_BODY), tol=0.05,
      note="distractor: exponent sign reversed")
check("cp4-p9-q3/B", 1.6, lambda: EA_UNCAT / EA_CAT, note="distractor: ratio of the two barriers")
check("cp4-p9-q3/D", 1.4e21, lambda: factor((EA_UNCAT - EA_CAT) * 4.184, T_BODY), tol=0.10,
      note="distractor: 30 read as kcal/mol")

# ------------------------------------------------- Passage 10: Hess cycles
HC_GLUCOSE, HC_LACTIC, HC_ETHANOL, HC_ACETIC = -2808.0, -1344.0, -1367.0, -874.0
check("cp4-p10-q1", -120, lambda: HC_GLUCOSE - 2 * HC_LACTIC, note="key: glucose to two lactic acid, kJ/mol")
check("cp4-p10-q1/B", -1464, lambda: HC_GLUCOSE - HC_LACTIC, note="distractor: factor of two omitted")
check("cp4-p10-q1/C", -2808, lambda: HC_GLUCOSE, tol=0.0001, note="distractor: glucose combustion quoted")
check("cp4-p10-q1/D", -5496, lambda: HC_GLUCOSE + 2 * HC_LACTIC, note="distractor: enthalpies added")
check("cp4-p10-q3", -74, lambda: HC_GLUCOSE - 2 * HC_ETHANOL, note="key: fermentation to two ethanol, kJ/mol")
check("cp4-p10-q3/B", -120, lambda: HC_GLUCOSE - 2 * HC_LACTIC, note="distractor: the lactic acid row used")
check("cp4-p10-q3/C", -148, lambda: 2 * (HC_GLUCOSE - 2 * HC_ETHANOL), note="distractor: the two applied twice")
check("cp4-p10-q3/D", -1441, lambda: HC_GLUCOSE - HC_ETHANOL, note="distractor: factor of two omitted")
check("cp4-p10-q4/retained", 0.97, lambda: 2 * HC_ETHANOL / HC_GLUCOSE,
      note="ethanol still holds 97 percent of glucose's combustion enthalpy")

# ------------------------------------------------- Discretes
# d1 Raoult: 1.00 mol glucose in 9.00 mol water, water 23.8 torr at 25 degC.
PW = 23.8
check("cp4-d1", 21.4, lambda: PW * 9.0 / 10.0, note="key: vapour pressure above the solution, torr")
check("cp4-d1/A", 2.38, lambda: PW * 1.0 / 10.0, note="distractor: solute mole fraction used")
check("cp4-d1/B", 19.5, lambda: PW * 9.0 / 11.0, note="distractor: glucose treated as dissociating")
check("cp4-d1/D", 26.4, lambda: PW / 0.900, note="distractor: divided by the mole fraction")
# d3 Beer-Lambert: 10.0 percent transmitted, concentration tripled.
check("cp4-d3/A0", 1.00, lambda: -math.log10(0.100), note="absorbance at 10 percent transmission")
check("cp4-d3", 3.00, lambda: 3 * -math.log10(0.100), note="key: absorbance when the concentration triples")
check("cp4-d3/A", 0.333, lambda: -math.log10(0.100) / 3, note="distractor: absorbance divided by three")
check("cp4-d3/B", 0.52, lambda: -math.log10(0.300), note="distractor: transmittance tripled instead")
# d4 deltoid: arm weight 35 N at 30 cm, insertion 5.0 cm.
check("cp4-d4", 210, lambda: 35.0 * 30.0 / 5.0, note="key: deltoid force, N")
check("cp4-d4/A", 5.8, lambda: 35.0 * 5.0 / 30.0, note="distractor: lever arms inverted")
check("cp4-d4/D", 1050, lambda: 35.0 * 30.0, note="distractor: a torque quoted as a force")
# d5 concentration cell, Cu/Cu2+ 0.0010 M against 0.10 M, n = 2.
check("cp4-d5", 0.059, lambda: (NERNST_25 / 1000 / 2) * math.log10(0.10 / 0.0010), tol=0.01,
      note="key: cell potential, V")
check("cp4-d5/C", 0.118, lambda: (NERNST_25 / 1000) * math.log10(0.10 / 0.0010), tol=0.01,
      note="distractor: electron count omitted")
check("cp4-d5/D", 2.96, lambda: (NERNST_25 / 1000 / 2) * (0.10 / 0.0010), tol=0.01,
      note="distractor: ratio used in place of its logarithm")
# d7 eye: pupil 3.0 mm, 550 nm, Rayleigh.
check("cp4-d7", 2.2e-4, lambda: 1.22 * 550e-9 / 3.0e-3, note="key: angular resolution, rad")
check("cp4-d7/arcmin", 0.77, lambda: (1.22 * 550e-9 / 3.0e-3) * 180 / math.pi * 60,
      note="sanity: about one arcminute")
check("cp4-d7/A", 9.2e-5, lambda: 0.5 * 550e-9 / 3.0e-3, note="distractor: Abbe one-half in place of 1.22")
check("cp4-d7/B", 1.8e-4, lambda: 550e-9 / 3.0e-3, note="distractor: the 1.22 omitted")
check("cp4-d7/D", 2.2e-3, lambda: 1.22 * 550e-9 / 3.0e-4, note="distractor: pupil taken as 0.30 mm")
# d8 nephrotic filtration: oncotic halved to 14 mmHg.
check("cp4-d8", 26, lambda: P_GLOM - P_BOWMAN - 14.0, note="key: new net filtration pressure, mmHg")
check("cp4-d8/A", 6, lambda: NFP / 2, note="distractor: the net pressure halved instead")
check("cp4-d8/B", 12, lambda: NFP, tol=0.0001, note="distractor: unchanged value")
check("cp4-d8/D", 40, lambda: P_GLOM - P_BOWMAN, note="distractor: oncotic term dropped entirely")
# d9 catalyst: 75 to 50 kJ/mol at 300 K.
check("cp4-d9", 2.2e4, lambda: factor(25.0, 300.0), tol=0.05, note="key: rate enhancement")
check("cp4-d9/A", 1.5, lambda: 75.0 / 50.0, note="distractor: ratio of the barriers")
check("cp4-d9/C", 5.1e8, lambda: factor(50.0, 300.0), tol=0.05, note="distractor: the drop counted twice")
check("cp4-d9/D", 1.6e18, lambda: factor(25.0 * 4.184, 300.0), tol=0.10, note="distractor: 25 read as kcal/mol")
# d11 Hess: ethanol oxidised to acetic acid.
check("cp4-d11", -493, lambda: HC_ETHANOL - HC_ACETIC, note="key: ethanol to acetic acid, kJ/mol")
check("cp4-d11/B", -874, lambda: HC_ACETIC, tol=0.0001, note="distractor: acetic acid combustion quoted")
check("cp4-d11/C", -1367, lambda: HC_ETHANOL, tol=0.0001, note="distractor: ethanol combustion quoted")
check("cp4-d11/D", -2241, lambda: HC_ETHANOL + HC_ACETIC, note="distractor: enthalpies added")

run()
