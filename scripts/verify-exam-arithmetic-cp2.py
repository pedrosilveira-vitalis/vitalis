"""Checks the arithmetic behind every quantitative item in fl2/chem-phys.

Each entry names the question, the value its keyed choice (or a named
distractor) claims, and recomputes it from the passage's own numbers. A
question whose key does not match its own physics fails here rather than in
front of a student. Distractors are computed too, so none is accidentally
also correct.
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
        print(("  ok  " if ok else "  FAIL") + f"  {qid:16s} claimed={claimed:<12.6g} computed={got:<12.6g} {note}")
        if not ok:
            bad.append(qid)
    print()
    print(f"{len(CHECKS) - len(bad)}/{len(CHECKS)} values verified")
    if bad:
        raise SystemExit("FAILED: " + ", ".join(bad))


# ------------------------------------------------- Passage 1: bomb calorimetry
# Calibration: 1.000 g benzoic acid, 26.4 kJ/g, raises the bomb 2.64 degC.
BENZOIC, DT_CAL = 26.4, 2.64
C_CAL = BENZOIC / DT_CAL                       # kJ per degC
check("cp2-p1-q1", 10.0, lambda: C_CAL, note="calorimeter constant 26.4 kJ / 2.64 degC")
check("cp2-p1-q1/A", 0.010, lambda: (BENZOIC / 1000) / DT_CAL, note="distractor: 26.4 read as J/g")
check("cp2-p1-q1/B", 0.10, lambda: DT_CAL / BENZOIC, note="distractor: division inverted")

# Table of 1.00 g samples and their temperature rises.
RISE = {"glucose": 1.56, "casein": 1.72, "ethanol": 2.97, "palmitic": 3.90}
for name, dt in RISE.items():
    check(f"cp2-p1/table-{name}", round(dt * 10.0, 1), lambda dt=dt: dt * C_CAL, note=f"{name}: kJ per gram")
check("cp2-p1-q2", 39.0, lambda: RISE["palmitic"] * C_CAL, note="palmitic acid, kJ/g")

M_GLUCOSE, M_PALMITIC = 180.16, 256.43
check("cp2-p1-q3", 2810, lambda: RISE["glucose"] * C_CAL * M_GLUCOSE, note="glucose, kJ/mol (sign negative)")
check("cp2-p1-q3/B", 281, lambda: RISE["glucose"] * M_GLUCOSE, note="distractor: calorimeter constant omitted")
check("cp2-p1-q3/D", 4000, lambda: RISE["glucose"] * C_CAL * M_PALMITIC,
      note="distractor: molar mass of palmitic acid used")

# ------------------------------------------------- Passage 2: gas laws, altitude
PATM, PH2O, FIO2 = 760.0, 47.0, 0.21
PALT, RQ = 460.0, 0.8
check("cp2-p2-q1", 150, lambda: FIO2 * (PATM - PH2O), note="humidified inspired PO2, sea level")
check("cp2-p2-q1/C", 160, lambda: FIO2 * PATM, note="distractor: water vapour ignored")
check("cp2-p2-q1/D", 713, lambda: PATM - PH2O, note="distractor: oxygen fraction omitted")
check("cp2-p2/table-alt", 87, lambda: FIO2 * (PALT - PH2O), note="humidified inspired PO2 at 460 mmHg")
check("cp2-p2-q2", 49, lambda: FIO2 * (PALT - PH2O) - 30 / RQ, note="alveolar PO2 at altitude, PaCO2 30")
check("cp2-p2-q2/A", 12, lambda: FIO2 * (PALT - PH2O) - 2 * 30 / RQ, tol=0.03,
      note="distractor: correction applied twice (11.7, shown rounded to 12)")
check("cp2-p2-q2/B", 37, lambda: FIO2 * (PALT - PH2O) - 40 / RQ, note="distractor: sea-level PaCO2 of 40 used")
check("cp2-p2-q2/D", 57, lambda: FIO2 * (PALT - PH2O) - 30, note="distractor: PaCO2 not divided by 0.8")
V0 = 20.0
check("cp2-p2-q3", 33, lambda: V0 * PATM / PALT, note="Boyle: 20 mL gas pocket at 460 mmHg")
check("cp2-p2-q3/A", 12, lambda: V0 * PALT / PATM, note="distractor: ratio inverted")
check("cp2-p2-q3/D", 55, lambda: V0 * (PATM / PALT) ** 2, note="distractor: ratio applied twice")

# ------------------------------------------------- Passage 3: histidine titration
PK1, PK2, PK3 = 1.8, 6.0, 9.2
check("cp2-p3-q1", 1.8, lambda: PK1, tol=0.0, note="pH at the first half-equivalence")
check("cp2-p3-q1/A", 0.9, lambda: PK1 / 2, note="distractor: pKa halved")
check("cp2-p3-q2", 9.2, lambda: PK3, tol=0.0, note="pH at 62.5 mL = third half-equivalence")
check("cp2-p3-q3", 7.6, lambda: (PK2 + PK3) / 2, note="isoelectric point")
check("cp2-p3-q3/A", 3.9, lambda: (PK1 + PK2) / 2, note="distractor: first two pKa values averaged")
check("cp2-p3-q3/B", 5.7, lambda: (PK1 + PK2 + PK3) / 3, note="distractor: all three averaged")
CONC, VOL = 0.100, 0.0250
check("cp2-p3/equivalence", 25.0, lambda: 1000 * CONC * VOL / 0.100, note="mL of 0.100 M NaOH per equivalence")

# ------------------------------------------------- Passage 4: iodometric vitamin C
C_I2, V_I2 = 0.0100, 0.01420
M_ASC = 176.12
mol_asc = C_I2 * V_I2                           # 1:1 with iodine
check("cp2-p4/mean-titre", 14.20, lambda: (14.25 + 14.20 + 14.15) / 3, note="mean of the three trials, mL")
check("cp2-p4-q2", 1.42e-4, lambda: mol_asc, note="mol ascorbic acid in the 25.00 mL aliquot")
check("cp2-p4-q2/A", 7.10e-5, lambda: mol_asc / 2, note="distractor: 2 mol iodine per ascorbic acid assumed")
check("cp2-p4-q2/C", 2.84e-4, lambda: mol_asc * 2, note="distractor: multiplied by two instead")
check("cp2-p4-q2/D", 1.42e-3, lambda: mol_asc * 10, note="distractor: decade slip in the burette volume")
check("cp2-p4-q3", 100.0, lambda: mol_asc * 4 * M_ASC * 1000, note="mg ascorbic acid per tablet")
check("cp2-p4-q3/A", 25.0, lambda: mol_asc * M_ASC * 1000, note="distractor: aliquot factor of 4 omitted")
check("cp2-p4-q3/B", 50.0, lambda: (mol_asc / 2) * 4 * M_ASC * 1000, note="distractor: 2:1 stoichiometry assumed")
check("cp2-p4-q3/D", 400.0, lambda: mol_asc * 16 * M_ASC * 1000, note="distractor: factor of 4 applied twice")

# ------------------------------------------------- Passage 5: centrifugation
G = 9.8


def rcf(radius_m, rpm):
    omega = 2 * math.pi * rpm / 60
    return omega ** 2 * radius_m / G


check("cp2-p5/protocol-1", 168, lambda: rcf(0.15, 1000), note="0.15 m, 1000 rpm")
check("cp2-p5/protocol-2", 755, lambda: rcf(0.075, 3000), note="0.075 m, 3000 rpm")
check("cp2-p5/protocol-3", 755, lambda: rcf(0.30, 1500), note="0.30 m, 1500 rpm")
check("cp2-p5-q2", 1.5e3, lambda: rcf(0.15, 3000), note="protocol 4: 0.15 m, 3000 rpm")
check("cp2-p5-q2/B", 1.5e4, lambda: rcf(0.15, 3000) * G, note="distractor: not divided by g")
check("cp2-p5-q2/C", 1.5e5, lambda: rcf(15.0, 3000), note="distractor: radius left in centimetres")
check("cp2-p5-q2/D", 5.4e6, lambda: (2 * math.pi * 3000) ** 2 * 0.15 / G,
      note="distractor: rpm used as rev/s")

# ------------------------------------------------- Passage 6: Doppler ultrasound
C_SOUND, F0, COS60 = 1540.0, 5.0e6, 0.5


def doppler_v(df, factor=2, angle=COS60):
    return df * C_SOUND / (factor * F0 * angle)


for df, v in ((650, 0.20), (1300, 0.40), (3250, 1.00), (6500, 2.00)):
    check(f"cp2-p6/table-{df}", v, lambda df=df: doppler_v(df), note=f"{df} Hz shift, m/s")
check("cp2-p6-q1", 1.00, lambda: doppler_v(3250), note="3250 Hz at 60 degrees")
check("cp2-p6-q1/B", 0.58, lambda: doppler_v(3250, angle=math.sin(math.radians(60))),
      note="distractor: sin 60 used for cos 60")
check("cp2-p6-q1/C", 0.50, lambda: doppler_v(3250, angle=1.0), note="distractor: cosine omitted")
check("cp2-p6-q2", 3.08e-4, lambda: C_SOUND / F0, note="wavelength of 5.0 MHz in tissue, m")
check("cp2-p6-q2/B", 1.54e-4, lambda: C_SOUND / (2 * F0), note="distractor: round-trip factor applied to lambda")

# ------------------------------------------------- Passage 7: radiopharmaceuticals
check("cp2-p7-q1", 0.125, lambda: 0.5 ** (18 / 6.0), note="Tc-99m, 18 h / 6.0 h half-life")
check("cp2-p7-q2", 100, lambda: 400 * 0.5 ** (220 / 110), note="F-18, 400 MBq after 220 min")
check("cp2-p7-q2/A", 283, lambda: 400 * 0.5 ** 0.5, note="distractor: half a half-life")
check("cp2-p7-q2/C", 141, lambda: 400 * 0.5 ** 1.5, note="distractor: one and a half half-lives")
check("cp2-p7-q3", 1.0e-2, lambda: math.log(2) / 68, note="Ga-68 decay constant, per minute")
check("cp2-p7-q3/B", 1.5e-2, lambda: 1 / 68, note="distractor: ln 2 omitted")
check("cp2-p7-q3/C", 6.1e-1, lambda: 60 * math.log(2) / 68, note="distractor: per hour labelled per minute")
check("cp2-p7-q3/D", 4.7e1, lambda: math.log(2) * 68, note="distractor: multiplied by the half-life")

# ------------------------------------------------- Passage 8: surfactant, Laplace
def laplace(gamma, r):
    return 2 * gamma / r


check("cp2-p8-q1", 2000, lambda: laplace(0.050, 50e-6), note="bare saline film, r = 50 um")
check("cp2-p8-q1/B", 1000, lambda: laplace(0.050, 50e-6) / 2, note="distractor: factor of 2 omitted")
check("cp2-p8/inflated", 500, lambda: laplace(0.025, 100e-6), note="inflated alveolus row")
check("cp2-p8-q2", 400, lambda: laplace(0.010, 50e-6), note="surfactant-lined, r = 50 um")
check("cp2-p8-q2/B", 1000, lambda: laplace(0.025, 50e-6), note="distractor: inflation tension with resting radius")
check("cp2-p8-q2/mmHg", 3.0, lambda: laplace(0.010, 50e-6) / 133.3, note="the same pressure in mmHg")

# ------------------------------------------------- Passage 9: defibrillator
C1, R_TH, V_SET = 100e-6, 50.0, 2000.0
check("cp2-p9-q1", 200, lambda: 0.5 * C1 * V_SET ** 2, note="energy stored at 2.0 kV")
check("cp2-p9-q1/A", 0.10, lambda: 0.5 * C1 * V_SET, note="distractor: voltage not squared")
check("cp2-p9-q1/B", 0.20, lambda: C1 * V_SET, note="distractor: charge in coulombs reported as joules")
check("cp2-p9/v-100J", 1414, lambda: math.sqrt(2 * 100 / C1), note="volts for the 100 J setting")
check("cp2-p9/v-360J", 2683, lambda: math.sqrt(2 * 360 / C1), note="volts for the 360 J setting")
check("cp2-p9-q2", 0.20, lambda: C1 * V_SET, note="charge on the capacitor at 2.0 kV")
check("cp2-p9-q2/C", 0.27, lambda: C1 * 2683, note="distractor: the 360 J setting's voltage")
check("cp2-p9-q2/D", 2.0e5, lambda: 100 * V_SET, note="distractor: microfarads read as farads")
check("cp2-p9-q3", 5.0e-3, lambda: R_TH * C1, note="time constant, adult 100 uF through 50 ohm")
check("cp2-p9-q3/A", 2.5e-3, lambda: R_TH * 50e-6, note="distractor: paediatric 50 uF used")
check("cp2-p9-q3/C", 1.0e-2, lambda: R_TH * 200e-6, note="distractor: the parallel pair used")
check("cp2-p9-q4", 400, lambda: 0.5 * (2 * C1) * V_SET ** 2, note="two 100 uF in parallel at 2.0 kV")
check("cp2-p9-q4/A", 100, lambda: 0.5 * (C1 / 2) * V_SET ** 2, note="distractor: series combination")
check("cp2-p9-q4/D", 800, lambda: 2 * 0.5 * (2 * C1) * V_SET ** 2, note="distractor: doubled a second time")

# ------------------------------------------------- Passage 10: rate law
RATE1 = 2.0e-4
check("cp2-p10/trial-2", 4.0e-4, lambda: RATE1 * 2, note="[RBr] doubled, first order")
check("cp2-p10/trial-3", 4.0e-4, lambda: RATE1 * 2, note="[thiol] doubled, first order")
check("cp2-p10/trial-4", 8.0e-4, lambda: RATE1 * 4, note="both doubled")
check("cp2-p10-q2", 2.0e-2, lambda: RATE1 / (0.10 * 0.10), note="second-order rate constant")
check("cp2-p10-q2/B", 5.0e-3, lambda: RATE1 / (0.20 * 0.20), note="distractor: trial 1 rate with trial 4 concentrations")
check("cp2-p10-q2/C", 2.0e-3, lambda: RATE1 / 0.10, note="distractor: divided by one concentration only")
check("cp2-p10-q5", 8.0e-4, lambda: RATE1 * 2 * 2, note="both concentrations doubled")
check("cp2-p10-q5/B", 2.83e-4, lambda: RATE1 * math.sqrt(2), note="distractor: half order in each")
check("cp2-p10-q5/C", 4.0e-4, lambda: RATE1 * 2, note="distractor: first order overall")

# ------------------------------------------------- Discretes
R_ATM, T_BODY = 0.08206, 310.0
check("cp2-d1", 7.8, lambda: 2 * 0.154 * R_ATM * T_BODY, note="osmotic pressure of 0.154 M NaCl, atm")
check("cp2-d1/A", 0.94, lambda: 2 * 0.154 * R_ATM * 37, note="distractor: 37 used for T")
check("cp2-d1/B", 3.9, lambda: 0.154 * R_ATM * T_BODY, note="distractor: van't Hoff factor of 1")
check("cp2-d1/D", 794, lambda: 2 * 0.154 * 8.314 * T_BODY, note="distractor: kPa value labelled atm")
GAMMA = 42.58
check("cp2-d5", 63.9, lambda: GAMMA * 1.5, note="proton resonance at 1.5 T, MHz")
check("cp2-d5/C", 85.2, lambda: GAMMA * 2.0, note="distractor: 2.0 T used")
check("cp2-d5/D", 95.8, lambda: GAMMA * 1.5 * 1.5, note="distractor: field applied twice")
check("cp2-d6", 75.2, lambda: math.degrees(math.asin(1.45 / 1.50)), note="critical angle, core 1.50 / clad 1.45")
check("cp2-d6/A", 14.8, lambda: 90 - math.degrees(math.asin(1.45 / 1.50)), note="distractor: complement taken")
check("cp2-d6/B", 41.8, lambda: math.degrees(math.asin(1 / 1.50)), note="distractor: core-to-air interface")
check("cp2-d6/C", 69.1, lambda: math.degrees(math.asin((1.45 / 1.50) ** 2)), note="distractor: index ratio squared")
check("cp2-d7", 368, lambda: 5.0 * 9.8 * 0.30 / 0.040, note="biceps force, N")
check("cp2-d7/A", 6.5, lambda: 5.0 * 9.8 * 0.040 / 0.30, note="distractor: lever arms interchanged")
check("cp2-d7/B", 49, lambda: 5.0 * 9.8, note="distractor: weight of the load alone")
check("cp2-d7/D", 3675, lambda: 5.0 * 9.8 * 0.30 / 0.0040, note="distractor: decade slip in the insertion distance")
check("cp2-d8", 20, lambda: 10 * math.log10(100), note="dB rise for a hundredfold intensity")
check("cp2-d8/D", 40, lambda: 20 * math.log10(100), note="distractor: amplitude formula used")
PKA_AC = 4.76
check("cp2-d10", 4.46, lambda: PKA_AC + math.log10(0.050 / 0.10), note="buffer pH")
check("cp2-d10/A", 4.16, lambda: PKA_AC + 2 * math.log10(0.050 / 0.10), note="distractor: log term doubled")
check("cp2-d10/D", 5.06, lambda: PKA_AC + math.log10(0.10 / 0.050), note="distractor: ratio inverted")
check("cp2-d11", 8, lambda: 2 ** 3, note="stereoisomers from three stereocentres")
check("cp2-d11/B", 6, lambda: 3 * 2, note="distractor: centres multiplied by two")
check("cp2-d11/D", 9, lambda: 3 ** 2, note="distractor: centres squared")
check("cp2-d13", 0.05, lambda: math.exp(-0.050 * 60), tol=0.01, note="fraction left, k = 0.050 /s, 60 s")
check("cp2-d13/B", 0.25, lambda: 0.5 ** 2, note="distractor: two half-lives")
check("cp2-d13/C", 0.50, lambda: 0.5 ** 1, note="distractor: one half-life")
check("cp2-d13/D", 0.95, lambda: 1 - math.exp(-0.050 * 60), tol=0.01, note="distractor: fraction reacted")
check("cp2-d13/half-life", 13.9, lambda: math.log(2) / 0.050, note="for the explanation: half-life in s")

# ------------------------------------------------- values quoted in explanations
check("cp2-p3-q4/ratio", 6.3e-4, lambda: 10 ** (6.0 - 9.2),
      note="deprotonated:protonated amino at pH 6.0, about 1 in 1600")
check("cp2-p5-q4/disadvantage", 7.5, lambda: 0.30 / 0.040, note="lever-arm ratio quoted in cp2-d7")
check("cp2-p6-q3/cos75", 0.26, lambda: math.cos(math.radians(75)), note="cosine at 75 degrees")
check("cp2-p6-q4", 0.32, lambda: 1 - math.cos(math.radians(70)) / math.cos(math.radians(60)),
      note="shortfall when 70 degrees is recorded as 60")
check("cp2-p6-q4/D", 0.14, lambda: 1 - 60 / 70, tol=0.05, note="distractor: shortfall if angles were proportional")
check("cp2-p8-q2/15", 15.0, lambda: laplace(0.050, 50e-6) / 133, note="saline film in mmHg")
check("cp2-p8-q2/7.5", 7.5, lambda: laplace(0.025, 50e-6) / 133, note="inflation tension at resting radius, mmHg")
check("cp2-p8-q2/3.8", 3.8, lambda: laplace(0.025, 100e-6) / 133, note="fully inflated alveolus, mmHg")
check("cp2-p9-q3/four-tau", 2.0e-2, lambda: 4 * R_TH * C1, note="four time constants, the quoted 20 ms")
check("cp2-p10-q5-new", 4.0e-4, lambda: 2.0e-2 * 0.40 * 0.050, note="0.40 M bromide with 0.050 M thiol")
check("cp2-p10-q5-new/A", 1.6e-4, lambda: 2.0e-2 * 0.40 ** 2 * 0.050, note="distractor: second order in the bromide")
check("cp2-p10-q5-new/D", 1.0e-3, lambda: 2.0e-2 * 0.050, note="distractor: bromide term dropped")
check("cp2-p7-q4/fortnight", 0.30, lambda: 0.5 ** (14 / 8.0), note="iodine-131 activity left after a fortnight")
check("cp2-d2/CaCl2", 0.30, lambda: 3 * 0.10, note="particle concentration of 0.10 M calcium chloride")
check("cp2-d13/four-half-lives", 4.3, lambda: 60 / (math.log(2) / 0.050), tol=0.05,
      note="60 s expressed in half-lives, more than four")

run()
