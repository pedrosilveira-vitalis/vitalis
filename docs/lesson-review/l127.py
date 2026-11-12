import sys, math; sys.path.insert(0,'/home/claude/dkit')
from dkit import *

A_, B_ = 13.966, 5209.0
def Ppure(t): return math.exp(A_ - B_/(t + 273.15))
CHI = 0.888
def Psol(t): return CHI * Ppure(t)

d = D(1180, 900, "One cause, four properties",
      "A solute lowers the chemical potential of the liquid solvent. Everything on this page follows from that single fact — and from how many particles, never which ones.",
      "A schematic pressure against temperature phase diagram for water, with shifts exaggerated for visibility. The pure solvent's vaporisation curve runs from the triple point up to one atmosphere at 100 degrees. The solution's vaporisation curve lies below it everywhere, because the solute lowers the solvent's vapour pressure, so the curve meets the one atmosphere line further right, at a raised boiling point. The fusion curve is shifted left, so the solid and liquid meet at a lowered freezing point. The sublimation curve is unchanged, because the solid that freezes out is pure solvent. Together the shifted curves show boiling point elevation and freezing point depression as two readings of the same downward shift in the liquid's chemical potential. Panels beside it give the four properties. Vapour pressure lowering: the change in pressure equals the mole fraction of solute times the pure solvent vapour pressure, and the unit required is mole fraction. Boiling point elevation: the change equals the van't Hoff factor times the ebullioscopic constant times molality, which for water is 0.512 degrees per molal. Freezing point depression: the change equals the van't Hoff factor times the cryoscopic constant times molality, which for water is 1.86 degrees per molal, over three times larger, which is why clinical osmometry measures freezing points. Osmotic pressure: pressure equals the van't Hoff factor times molarity times the gas constant times temperature, the only one of the four that uses molarity rather than molality, and by far the largest effect in biological systems. A table gives van't Hoff factors: glucose, urea and sucrose give one; sodium chloride and magnesium sulfate give two; calcium chloride and magnesium chloride give three; and real values fall below these because of ion pairing, with concentrated sodium chloride nearer 1.8 than 2. A final panel distinguishes osmolarity from tonicity: a solute counts towards osmolarity if it is dissolved at all, but towards tonicity only if it cannot cross the membrane, which is why urea raises measured osmolarity without drawing water out of cells.")

F = d.axes(64, 168, 548, 316, "temperature (°C)", "pressure (atm)",
           xr=(-22, 114), yr=(0, 1.35), ticks_x=[25, 50, 75], ticks_y=[])
# one-atm line
x0, y1a = F(-22, 1.0); x1, _ = F(114, 1.0)
d.line(x0, y1a, x1, y1a, "#c9bfae", 1.5, True)
d.text(F(-19, 1.0)[0], y1a - 9, "1 atm", color=GREY, size=10.5, anchor="start")
# vaporisation curves
d.curve(F, [(-11 + i*0.4, min(Ppure(-11 + i*0.4), 1.35)) for i in range(0, 305)], NAVY, 3)
d.curve(F, [(-11 + i*0.4, min(Psol(-11 + i*0.4), 1.35)) for i in range(0, 305)], RED, 2.5, dash=True)
# fusion curves (near-vertical, slight left lean for water)
d.curve(F, [(0.0, 0.006), (-0.5, 0.7), (-0.9, 1.35)], NAVY, 3)
d.curve(F, [(-10.8, 0.0022), (-11.3, 0.7), (-11.7, 1.35)], RED, 2.5, dash=True)
# sublimation curve, shared
d.curve(F, [(-22, 0.0005), (-14, 0.0012), (-7, 0.0027), (0.0, 0.006)], NAVY, 3)

for t, lab, c, anc, off in ((0.0, "Tᶠ°", NAVY, "start", 5), (-10.8, "Tᶠ", RED, "end", -5),
                            (100.0, "Tᵇ°", NAVY, "end", -5), (103.0, "Tᵇ", RED, "start", 5)):
    px, py0 = F(t, 0); _, pyt = F(t, 1.0 if t > 50 else 1.35)
    d.line(px, py0, px, pyt, c, 1, True)
    d.text(px + off, py0 + 18, lab, color=c, size=12, weight=700, anchor=anc)
d.text(F(50, 0.62)[0], F(50, 0.62)[1], "LIQUID", color=GREY, size=12, weight=700)
d.text(F(92, 0.18)[0], F(92, 0.18)[1], "VAPOUR", color=GREY, size=12, weight=700)
d.text(F(-17, 0.75)[0], F(-17, 0.75)[1], "SOLID", color=GREY, size=12, weight=700)
d.legend(300, 212, [(NAVY, "pure solvent", False), (RED, "solution", True)])
d.text(338, 536, "Schematic — shifts exaggerated. The sublimation curve does not move: the solid that freezes out is pure solvent.",
       color=GREY, size=11)

PROPS = [
 (NAVY, "VAPOUR PRESSURE LOWERING", "ΔP = χ_solute × P°", "mole fraction",
  "the parent effect — the other three are this shift read on different axes"),
 (BLUE, "BOILING POINT ELEVATION", "ΔTᵇ = i·Kᵇ·m", "molality",
  "Kᵇ(water) = 0.512 °C·kg/mol"),
 (SAGE, "FREEZING POINT DEPRESSION", "ΔTᶠ = i·Kᶠ·m", "molality",
  "Kᶠ(water) = 1.86 — 3.6× larger, so osmometry reads freezing points"),
 (GOLD, "OSMOTIC PRESSURE", "π = i·M·R·T", "MOLARITY",
  "the only one using molarity — and the largest effect in cells"),
]
yy = 160
for c, name, formula, unit, note in PROPS:
    d.rect(640, yy, 512, 88, c, FILL.get(c), 11, 2)
    d.text(662, yy + 26, name, color=c, weight=700, size=12, anchor="start")
    d.text(1130, yy + 26, formula, color=NAVY, weight=700, size=12.5, anchor="end")
    d.text(662, yy + 48, "needs " + unit, color=c, size=11, weight=700, anchor="start")
    d.lines(896, yy + 68, note, chars=66, lh=13, color=GREY, size=10.5)
    yy += 98

d.rect(24, 556, 560, 184, BLUE, FILL[BLUE], 12, 2)
d.text(304, 584, "VAN'T HOFF FACTOR — COUNT THE PARTICLES", color=BLUE, weight=700, size=13)
VH = [("glucose · urea · sucrose", "i = 1", "do not dissociate"),
      ("NaCl · MgSO₄", "i = 2", "two ions per formula unit"),
      ("CaCl₂ · MgCl₂ · Na₂SO₄", "i = 3", "three ions per formula unit")]
yy = 616
for a, b, why in VH:
    d.text(50, yy, a, color=NAVY, size=12, weight=700, anchor="start")
    d.text(400, yy, b, color=BLUE, size=12.5, weight=700, anchor="end")
    d.text(558, yy, why, color=GREY, size=10.5, anchor="end")
    yy += 30
d.line(50, 700, 558, 700, "#d9d2c4", 1, True)
d.text(304, 722, "Real i falls BELOW these — ion pairing puts concentrated NaCl nearer 1.8 than 2.0",
       color=BLUE, size=11, weight=700)

d.rect(608, 556, 544, 184, RED, FILL[RED], 12, 2)
d.text(880, 584, "OSMOLARITY IS NOT TONICITY", color=RED, weight=700, size=13)
for i, t in enumerate([
    "OSMOLARITY counts every dissolved particle.",
    "TONICITY counts only the ones that CANNOT cross the membrane.",
    "",
    "Urea crosses freely: it raises measured osmolarity and moves no water.",
    "A urea solution can be hyperosmotic and still isotonic."]):
    if t:
        d.text(632, 612 + i*22, t, color=NAVY, size=11.5,
               weight=700 if t.startswith(("OSMOLARITY", "TONICITY")) else 400, anchor="start")
d.text(880, 730, "hypotonic → cell swells, may lyse   ·   hypertonic → cell shrinks (crenation)",
       color=RED, size=11, weight=700)

d.box(24, 762, 1128, 92, "The two questions that settle every colligative problem",
      "1 · HOW MANY PARTICLES? Multiply molality (or molarity) by i. The identity of the solute never enters beyond the particle count.   2 · WHICH CONCENTRATION UNIT? Molality for ΔTᵇ and ΔTᶠ, mole fraction for Raoult, molarity for π. Using the wrong one is the commonest way to lose these points.",
      NAVY, chars=150, size=12, head_size=13.5)
print(d.save("colligative-phase-diagram"))
