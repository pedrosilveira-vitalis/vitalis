import sys; sys.path.insert(0,'/home/claude/dkit')
from dkit import *

d = D(1180, 940, "One basis, every concentration unit",
      "Pick 100 g of solution or 1 L of solution, fill in six numbers, and read any unit straight off. Density bridges mass to volume; molar mass bridges mass to moles.",
      "A conversion chart. Across the top, five concentration units as cards. Molarity: moles of solute over litres of solution, units molar, temperature dependent because volume expands, and the unit required by equilibrium constants, Beer-Lambert and osmotic pressure. Molality: moles of solute over kilograms of solvent, units molal, temperature independent, and the unit required by boiling point elevation and freezing point depression. Mole fraction: moles of one component over total moles, dimensionless, temperature independent, and the unit required by Raoult's law and Dalton's law. Mass percent: mass of solute over mass of solution times one hundred, temperature independent, and how concentrated laboratory acids are labelled. Parts per million: for aqueous solutions one part per million is one milligram per litre, used for trace contaminants. In the middle, the master strategy: choose a basis, either one hundred grams of solution when a mass percent is given, or one litre of solution when a molarity is given, then fill in six quantities — mass of solution, mass of solute, mass of solvent, moles of solute, moles of solvent and volume of solution — using density to move between mass and volume and molar mass to move between mass and moles. Every unit is then a ratio of two of those six numbers. A worked example takes twenty per cent by mass ethanol of density 0.968 grams per millilitre on a basis of one hundred grams: twenty grams of ethanol is 0.434 moles, eighty grams of water is 4.44 moles, the volume is 103.3 millilitres, so the molarity is 4.20, the molality is 5.43 and the mole fraction of ethanol is 0.0891. The molarity and the molality differ by nearly thirty per cent, and the reason is that the solute carries 194 grams of every litre, not that the density differs from one. A final panel matches each formula to the unit it requires.")

UNITS = [
 (24, NAVY, "MOLARITY  M", "mol solute", "L SOLUTION", "mol/L",
  "changes with T", "Kₑq · Beer-Lambert · π = iMRT · M₁V₁ = M₂V₂"),
 (254, BLUE, "MOLALITY  m", "mol solute", "kg SOLVENT", "mol/kg",
  "T-independent", "ΔTᵇ = iKᵇm · ΔTᶠ = iKᶠm"),
 (484, SAGE, "MOLE FRACTION  χ", "mol of one part", "mol TOTAL", "none",
  "T-independent", "Raoult · Dalton · sums to 1"),
 (714, GOLD, "MASS PERCENT  % w/w", "mass solute", "mass SOLUTION", "× 100",
  "T-independent", "how bottled acids are labelled"),
 (944, GREY, "ppm / ppb", "mass solute", "mass SOLUTION", "×10⁶ / ×10⁹",
  "T-independent", "aqueous: 1 ppm = 1 mg/L"),
]
for x, c, name, num, den, units, temp, use in UNITS:
    d.rect(x, 142, 212, 180, c, FILL.get(c), 12, 2)
    d.text(x+106, 168, name, color=c, weight=700, size=12.5)
    d.text(x+106, 200, num, color=NAVY, size=12)
    d.line(x+36, 208, x+176, 208, NAVY, 1.5)
    d.text(x+106, 226, den, color=NAVY, size=12, weight=700)
    d.text(x+106, 250, units, color=GREY, size=10.5)
    d.text(x+106, 272, temp, color=c, size=11, weight=700)
    d.lines(x+106, 292, use, chars=30, lh=13, color=GREY, size=10)

d.rect(24, 346, 1128, 196, NAVY, FILL[NAVY], 12, 2)
d.text(588, 374, "THE MASTER STRATEGY — PICK A BASIS, FILL IN SIX NUMBERS", color=NAVY, weight=700, size=13.5)
d.text(588, 396, "given a mass percent → take 100 g of SOLUTION    ·    given a molarity → take 1 L of SOLUTION", color=GREY, size=11.5)
BASIS = [("mass of solution", "basis, or d × V"), ("mass of solute", "from % w/w"),
         ("mass of solvent", "solution − solute"), ("moles of solute", "÷ molar mass"),
         ("moles of solvent", "÷ molar mass"), ("volume of solution", "mass ÷ density")]
for i, (lab, how) in enumerate(BASIS):
    bx = 56 + (i % 3) * 368
    by = 432 + (i // 3) * 54
    d.text(bx, by, "□  " + lab, color=NAVY, size=12.5, weight=700, anchor="start")
    d.text(bx+22, by+20, how, color=GREY, size=11, anchor="start")
d.text(588, 528, "every unit above is a ratio of two of these six — nothing else is needed",
       color=NAVY, size=12, weight=700)

d.rect(24, 566, 660, 244, GOLD, FILL[GOLD], 12, 2)
d.text(354, 594, "WORKED — 20.0% w/w ETHANOL, d = 0.968 g/mL, basis 100 g", color=GOLD, weight=700, size=12.5)
LINES = [("ethanol", "20.0 g", "÷ 46.07", "0.434 mol"),
         ("water", "80.0 g", "÷ 18.02", "4.440 mol"),
         ("solution", "100 g", "÷ 0.968", "103.3 mL")]
yy = 626
for a, b, c2, e in LINES:
    d.text(50, yy, a, color=GREY, size=11.5, anchor="start")
    d.text(210, yy, b, color=NAVY, size=12, weight=700, anchor="end")
    d.text(330, yy, c2, color=GREY, size=11, anchor="end")
    d.text(470, yy, e, color=NAVY, size=12, weight=700, anchor="end")
    yy += 26
d.line(50, 712, 658, 712, "#d9d2c4", 1, True)
for i, (lab, val) in enumerate([("M", "0.434 / 0.1033 L  =  4.20 M"),
                                ("m", "0.434 / 0.0800 kg  =  5.43 m"),
                                ("χ", "0.434 / 4.874  =  0.0891")]):
    d.text(50, 730 + i*21, lab, color=GOLD, size=12, weight=700, anchor="start")
    d.text(86, 730 + i*21, val, color=NAVY, size=12, weight=700, anchor="start")
d.text(354, 796, "M and m differ by 29% because the solute is 194 g of every litre — not because d ≠ 1",
       color=GOLD, size=11, weight=700)

d.rect(708, 566, 444, 244, BLUE, FILL[BLUE], 12, 2)
d.text(930, 594, "WHICH FORMULA WANTS WHICH UNIT", color=BLUE, weight=700, size=12.5)
PAIRS = [("ΔTᵇ, ΔTᶠ  (bp, fp)", "molality"), ("π = iMRT", "molarity"),
         ("Raoult, Dalton", "mole fraction"), ("A = εlc", "molarity"),
         ("Kₐ, Kᵇ, Kₛₚ, Kᴄ", "molarity"), ("M₁V₁ = M₂V₂", "molarity"),
         ("Henderson–Hasselbalch", "a MOLE ratio")]
yy = 622
for f, u in PAIRS:
    d.text(732, yy, f, color=NAVY, size=11.5, anchor="start")
    d.text(1128, yy, u, color=BLUE if u != "a MOLE ratio" else RED, size=11.5, weight=700, anchor="end")
    yy += 24
d.text(930, 796, "volume cancels in H–H, so moles work — masses do not", color=RED, size=10.5, weight=700)

d.box(24, 832, 1128, 92, "The two bridges, and the one that gets forgotten",
      "DENSITY moves mass ↔ volume (g/mL = kg/L). MOLAR MASS moves mass ↔ moles. Everything else is bookkeeping. The forgotten one: molality is per kilogram of SOLVENT, molarity per litre of SOLUTION — in a concentrated solution those are very different denominators.",
      NAVY, chars=150, size=12, head_size=13.5)
print(d.save("concentration-unit-map"))
