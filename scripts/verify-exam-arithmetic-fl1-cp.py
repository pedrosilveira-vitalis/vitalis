import math
BAD = []
def check(qid, claimed, got, tol=0.02, note=""):
    ok = abs(got - claimed) <= tol * abs(claimed) if claimed else abs(got) <= tol
    print(("  ok  " if ok else "  FAIL") + f"  {qid:14s} claimed={claimed:<12.6g} computed={got:<12.6g} {note}")
    if not ok: BAD.append(qid)

F, R = 96485.0, 8.314

# P5 electrochemistry: ferricyanide mediator vs glucose/gluconolactone
E_MED, E_GLU = 0.36, -0.45
check("cp-p5-q1", 0.81, E_MED - E_GLU, note="cell emf, cathode minus anode")
check("cp-p5-q2", -156, (-2 * F * (E_MED - E_GLU)) / 1000, note="dG in kJ/mol, n=2")
check("cp-p5-q4", 0.0296, (0.0592 / 2) * 1, note="Nernst shift for a tenfold Q at n=2")
check("cp-p5-q5", 1.00e-7, 9.6485e-3 / F, tol=0.01, note="mol electrons from 9.65 mC")
check("cp-p5-q5b", 5.00e-8, (9.6485e-3 / F) / 2, tol=0.01, note="mol glucose, 2 electrons each")

# P6 organic: TLC retention factor
check("cp-p6-q3", 0.40, 3.2 / 8.0, note="Rf = spot / solvent front")

# P7 solubility: calcium oxalate, Ksp = 2.3e-9
KSP = 2.3e-9
check("cp-p7-q1", 4.8e-5, math.sqrt(KSP), tol=0.02, note="molar solubility in water")
check("cp-p7-q2", 2.3e-7, KSP / 0.010, note="common-ion solubility in 0.010 M Ca2+")

# P8 gait mechanics: 70 kg, g = 9.8
M, G = 70.0, 9.8
check("cp-p8-q1", 686, M * G, note="body weight in N")
check("cp-p8-q2", 823, 1.2 * M * G, tol=0.01, note="peak ground reaction force")
check("cp-p8-q3", 34.3, M * G * 0.05, note="work raising the centre of mass 5 cm")
check("cp-p8-q4", 57, (M * G * 0.05) / 0.60, tol=0.02, note="average power over a 0.60 s stride")

# P9 protein folding: dH = -120 kJ/mol, dS = -350 J/(mol K)
DH, DS = -120000.0, -350.0
check("cp-p9-q1", -11.5, (DH - 310 * DS) / 1000, tol=0.03, note="dG at 310 K, kJ/mol")
check("cp-p9-q2", 343, DH / DS, tol=0.01, note="melting temperature in K")
check("cp-p9-q2b", 69.8, DH / DS - 273.15, tol=0.02, note="the same in Celsius")

# P10 membrane cable: R = 10 kohm cm2, C = 1 uF/cm2
check("cp-p10-q1", 0.010, 1.0e4 * 1.0e-6, note="membrane time constant in s")

print()
print(f"{15 - len(BAD)}/15 verified")
if BAD: raise SystemExit("FAILED: " + ", ".join(BAD))
