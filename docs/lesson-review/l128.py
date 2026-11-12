import sys; sys.path.insert(0,'/home/claude/dkit')
from dkit import *

d = D(1180, 940, "Why anything dissolves",
      "Pull the lattice apart, then let the solvent wrap the pieces. Solubility is whether the second step pays for the first — or whether entropy covers the shortfall.",
      "An enthalpy ladder for sodium chloride dissolving in water. Starting from solid sodium chloride and water at zero, separating the lattice into gaseous ions costs plus 788 kilojoules per mole, taking the system to the top of the diagram. Hydrating those ions releases 784, bringing the system back down to plus 4. The net enthalpy of solution is therefore plus 4 kilojoules per mole, slightly endothermic, and sodium chloride dissolves anyway because the entropy term carries it. A note records that tabulated hydration enthalpies already include the cost of opening a cavity in the solvent, so the three conceptual steps collapse to two numbers. Beside it, three salts compared: lithium chloride at minus 37 kilojoules per mole is exothermic and very soluble, sodium chloride at plus 4 is nearly thermoneutral and soluble because of entropy, and silver chloride at plus 65 is strongly endothermic, lattice dominated, and insoluble. A panel ranks the intermolecular forces that a solvent can offer a solute, from ion-dipole, the strongest, through hydrogen bonding, dipole-dipole, and finally London dispersion, the weakest, with the rule that like dissolves like meaning the solute-solvent interactions must be comparable in kind and strength to the solute-solute and solvent-solvent interactions they replace. A Henry's law panel gives concentration equals the Henry constant times partial pressure, with constants in water at 25 degrees of 3.4 times ten to the minus two for carbon dioxide, 1.3 times ten to the minus three for oxygen, 6.1 times ten to the minus four for nitrogen and 3.7 times ten to the minus four for helium, and notes that raising the partial pressure raises the dissolved concentration proportionally while raising the temperature lowers it, because dissolving a gas is exothermic. A solubility product panel gives the molar solubility of a one-to-one salt as the square root of the solubility product and of a one-to-two salt as the cube root of the solubility product over four, worked for barium sulfate and magnesium hydroxide, and shows the common ion effect dropping barium ion concentration from about ten to the minus five molar in pure water to about ten to the minus nine molar in 0.10 molar sulfate. A footer states that the hydrophobic effect is entropic, that a nonpolar solute forces water into ordered cages so the cost is paid in solvent entropy, and that ionising a weak acid or base raises its water solubility while its neutral form is the one that crosses membranes.")

F = d.axes(56, 164, 520, 300, "", "ΔH  (kJ/mol)", xr=(0, 3.2), yr=(-80, 880),
           ticks_x=[], ticks_y=[0, 200, 400, 600, 800])
LEV = [(0.15, 0.95, 0.0, "NaCl(s) + H₂O"), (1.25, 2.05, 788.0, "Na⁺(g) + Cl⁻(g)"),
       (2.35, 3.1, 4.0, "Na⁺(aq) + Cl⁻(aq)")]
for x0, x1, y, lab in LEV:
    p0 = F(x0, y); p1 = F(x1, y)
    d.line(p0[0], p0[1], p1[0], p1[1], NAVY, 3)
    d.text((p0[0]+p1[0])/2, p0[1] - 12, lab, color=NAVY, size=11, weight=700)
a0 = F(0.95, 0.0); a1 = F(1.25, 788.0)
d.arrow(a0[0], a0[1], a1[0], a1[1], RED, width=2.5)
d.text(a1[0] - 6, (a0[1]+a1[1])/2, "+788", color=RED, size=13, weight=700, anchor="end")
d.text(a1[0] - 6, (a0[1]+a1[1])/2 + 18, "break the lattice", color=RED, size=10.5, anchor="end")
b0 = F(2.05, 788.0); b1 = F(2.35, 4.0)
d.arrow(b0[0], b0[1], b1[0], b1[1], SAGE, width=2.5)
d.text(b0[0] + 8, (b0[1]+b1[1])/2, "−784", color=SAGE, size=13, weight=700, anchor="start")
d.text(b0[0] + 8, (b0[1]+b1[1])/2 + 18, "hydrate the ions", color=SAGE, size=10.5, anchor="start")
d.text(316, 492, "net ΔH_soln = +4 kJ/mol — slightly ENDOthermic, and NaCl dissolves anyway: TΔS carries it",
       color=NAVY, size=12.5, weight=700)
d.text(316, 516, "Tabulated hydration enthalpies already include the cost of opening a cavity in the solvent — three conceptual steps, two numbers.",
       color=GREY, size=10.5)

d.rect(604, 164, 548, 150, NAVY, FILL[NAVY], 12, 2)
d.text(878, 192, "SAME PICTURE, THREE OUTCOMES", color=NAVY, weight=700, size=13)
SALTS = [("LiCl", "ΔH_soln ≈ −37", SAGE, "hydration beats the lattice — very soluble"),
         ("NaCl", "ΔH_soln ≈ +4", GOLD, "a near tie — soluble on entropy alone"),
         ("AgCl", "ΔH_soln ≈ +65", RED, "lattice wins — entropy cannot cover it")]
yy = 222
for name, dh, c, note in SALTS:
    d.text(628, yy, name, color=NAVY, size=13, weight=700, anchor="start")
    d.text(800, yy, dh, color=c, size=12, weight=700, anchor="end")
    d.text(1128, yy, note, color=GREY, size=11, anchor="end")
    yy += 30

d.rect(604, 330, 548, 134, BLUE, FILL[BLUE], 12, 2)
d.text(878, 358, "WHAT THE SOLVENT CAN OFFER — STRONGEST FIRST", color=BLUE, weight=700, size=12.5)
IMF = [("ion–dipole", "Na⁺ with water — the strongest solvent–solute interaction"),
       ("hydrogen bond", "ethanol, glucose, ammonia in water"),
       ("dipole–dipole", "polar but no O–H or N–H; weaker"),
       ("London dispersion", "hexane in benzene — weak, but all that nonpolar pairs need")]
yy = 384
for name, eg in IMF:
    d.text(628, yy, name, color=BLUE, size=11.5, weight=700, anchor="start")
    d.text(1128, yy, eg, color=GREY, size=10.5, anchor="end")
    yy += 20

d.rect(24, 530, 560, 206, GOLD, FILL[GOLD], 12, 2)
d.text(304, 558, "GASES — HENRY'S LAW   C = kₕ × P", color=GOLD, weight=700, size=13)
GAS = [("CO₂", "3.4 × 10⁻²"), ("O₂", "1.3 × 10⁻³"),
       ("N₂", "6.1 × 10⁻⁴"), ("He", "3.7 × 10⁻⁴")]
yy = 590
for g, k in GAS:
    d.text(60, yy, g, color=NAVY, size=12, weight=700, anchor="start")
    d.text(250, yy, k, color=NAVY, size=12, anchor="end")
    yy += 24
d.text(155, 690, "kₕ in water at 25 °C, mol/(L·atm)", color=GREY, size=10.5)
d.line(290, 578, 290, 700, "#d9d2c4", 1, True)
for i, (a, b) in enumerate([("\u2191 partial pressure", "\u2191 dissolved, proportionally"),
                            ("\u2191 temperature", "\u2193 dissolved \u2014 dissolving a gas is exothermic"),
                            ("the bends", "ascend fast \u2192 P falls \u2192 N\u2082 leaves solution as bubbles"),
                            ("hyperbaric O\u2082", "3 atm of O\u2082 \u2192 3\u00d7 the dissolved fraction")]):
    d.text(312, 586 + i*34, a, color=GOLD, size=11.5, weight=700, anchor="start")
    d.text(312, 602 + i*34, b, color=GREY, size=10.5, anchor="start")

d.rect(604, 530, 548, 206, SAGE, FILL[SAGE], 12, 2)
d.text(878, 558, "SPARINGLY SOLUBLE SALTS — Kₛₚ", color=SAGE, weight=700, size=13)
for i, (a, b, c3) in enumerate([
        ("MA  \u21cc  M\u207a + A\u207b", "K\u209b\u209a = s\u00b2", "s = \u221aK\u209b\u209a"),
        ("MA\u2082 \u21cc M\u00b2\u207a + 2A\u207b", "K\u209b\u209a = 4s\u00b3", "s = \u221b(K\u209b\u209a/4)")]):
    d.text(628, 590 + i*26, a, color=NAVY, size=11.5, anchor="start")
    d.text(950, 590 + i*26, b, color=NAVY, size=11.5, weight=700, anchor="end")
    d.text(1128, 590 + i*26, c3, color=NAVY, size=11.5, weight=700, anchor="end")
d.line(628, 632, 1128, 632, "#d9d2c4", 1, True)
d.text(628, 654, "BaSO₄, Kₛₚ = 1.1×10⁻¹⁰", color=SAGE, size=11.5, weight=700, anchor="start")
d.text(1128, 654, "s = 1.05×10⁻⁵ M in pure water", color=NAVY, size=11.5, anchor="end")
d.text(628, 678, "… in 0.10 M SO₄²⁻", color=SAGE, size=11.5, weight=700, anchor="start")
d.text(1128, 678, "[Ba²⁺] = 1.1×10⁻⁹ M — 10,000× lower", color=NAVY, size=11.5, anchor="end")
d.text(878, 712, "Q < Kₛₚ unsaturated  ·  Q = Kₛₚ saturated  ·  Q > Kₛₚ precipitates",
       color=SAGE, size=11, weight=700)

d.box(24, 756, 1128, 104, "Two things the exam asks about that are not in the numbers above",
      "THE HYDROPHOBIC EFFECT IS ENTROPIC. A nonpolar solute does not repel water; it forces water into ordered cages around itself, and the cost is paid in solvent entropy. · pH CHANGES SOLUBILITY, AND PERMEABILITY THE OTHER WAY. Ionising a weak acid or base makes it far more water-soluble — but the NEUTRAL form is the one that crosses membranes.",
      NAVY, chars=150, size=12, head_size=13.5)
print(d.save("dissolution-energetics"))
