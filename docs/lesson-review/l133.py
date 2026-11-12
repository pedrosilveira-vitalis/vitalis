import sys, math; sys.path.insert(0,'/home/claude/dkit')
from dkit import *

d = D(1180, 950, "Add the reactions, multiply the constants",
      "Two equilibria that share a species are one equilibrium in disguise. Write the net reaction, multiply the K values, and a salt that “does not dissolve” may dissolve completely.",
      "Three worked couplings are set out as reaction sums. First, calcium carbonate in acid: the dissolution has a solubility product of 3.4 times ten to the minus nine, and protonating carbonate to bicarbonate contributes the reciprocal of the second acid constant of carbonic acid, 1 over 4.7 times ten to the minus eleven, so the net constant is about 71 and the dissolution is product-favoured, which is why antacid tablets dissolve in stomach acid and marble erodes in acid rain. Second, silver chloride in ammonia: the solubility product of 1.8 times ten to the minus ten multiplied by the formation constant of the diamminesilver ion, 1.7 times ten to the seventh, gives 3.1 times ten to the minus three, still below one but enormously larger than the solubility product alone, so concentrated ammonia dissolves the solid. Third, silver chloride in thiosulfate: the same solubility product multiplied by a formation constant of 2.9 times ten to the thirteenth gives 5.2 times ten to the third, far above one and essentially complete dissolution, which is the chemistry of photographic fixing. A plot shows the solubility of magnesium hydroxide against pH on a logarithmic scale in a buffered solution, where the solubility is the solubility product divided by the square of the hydroxide concentration, so the logarithm of the solubility falls by two for every unit of pH. At pH 9 the solubility is 5.6 times ten to the minus two molar, five hundred times its value in unbuffered water, and by pH 12 it has fallen to 5.6 times ten to the minus eight. The point for pure water is marked at a solubility of 1.1 times ten to the minus four molar and a pH of about 10.3, where the hydroxide released by the salt itself sets the pH. A panel works selective precipitation: with 0.10 molar barium and 0.10 molar calcium, sulfate begins to precipitate barium sulfate at 1.1 times ten to the minus nine molar sulfate and calcium sulfate only at 4.9 times ten to the minus four molar, by which point the barium concentration has fallen to 2.2 times ten to the minus seven molar, a removal of 99.9998 per cent. A footer lists which anions make a salt more soluble in acid, namely carbonate, phosphate, hydroxide, sulfide, fluoride and oxalate, all conjugate bases of weak acids, and notes that chloride, nitrate and sulfate are not, and that a formation constant is the reciprocal of a dissociation constant.")

d.rect(24, 160, 1128, 254, NAVY, FILL[NAVY], 12, 2)
d.text(588, 188, "THE MULTIPLICATION RULE, WORKED THREE TIMES", color=NAVY, weight=700, size=13.5)
CASES = [
 ("CaCO₃ in acid", SAGE,
  ["CaCO₃(s) ⇌ Ca²⁺ + CO₃²⁻", "CO₃²⁻ + H⁺ ⇌ HCO₃⁻"],
  ["Kₛₚ = 3.4×10⁻⁹", "1/Kₐ₂ = 2.1×10¹⁰"],
  "K_net ≈ 71", "product-favoured — antacids, acid rain on marble"),
 ("AgCl in ammonia", GOLD,
  ["AgCl(s) ⇌ Ag⁺ + Cl⁻", "Ag⁺ + 2NH₃ ⇌ [Ag(NH₃)₂]⁺"],
  ["Kₛₚ = 1.8×10⁻¹⁰", "K_f = 1.7×10⁷"],
  "K_net = 3.1×10⁻³", "still < 1, but 10⁷× the bare Kₛₚ — dissolves in conc. NH₃"),
 ("AgCl in thiosulfate", RED,
  ["AgCl(s) ⇌ Ag⁺ + Cl⁻", "Ag⁺ + 2S₂O₃²⁻ ⇌ [Ag(S₂O₃)₂]³⁻"],
  ["Kₛₚ = 1.8×10⁻¹⁰", "K_f = 2.9×10¹³"],
  "K_net = 5.2×10³", "≫ 1 — essentially complete: photographic fixing"),
]
x = 48
for name, c, eqs, ks, net, note in CASES:
    d.text(x, 216, name, color=c, size=12.5, weight=700, anchor="start")
    for i, (e, k) in enumerate(zip(eqs, ks)):
        d.text(x, 242 + i*32, e, color=NAVY, size=11, anchor="start")
        d.text(x, 256 + i*32, k, color=GREY, size=10.5, anchor="start")
    d.line(x, 310, x + 320, 310, "#d9d2c4", 1, True)
    d.text(x, 332, net, color=c, size=13.5, weight=700, anchor="start")
    d.lines(x + 160, 356, note, chars=42, lh=13, color=GREY, size=10.5)
    x += 368

F = d.axes(64, 452, 480, 250, "pH (buffered)", "log₁₀ solubility  (M)",
           xr=(8.4, 12.2), yr=(-8.5, 0.5), ticks_x=[9, 10, 11, 12],
           ticks_y=[-8, -6, -4, -2, 0])
pts = [(p/10.0, 16.748 - 2*(p/10.0)) for p in range(85, 123)]
d.curve(F, [(a, b) for a, b in pts if b <= 0.5], NAVY, 3)
px, py = F(10.34, -3.96)
d.circle(px, py, 5, RED, RED, 0)
d.text(px + 10, py + 4, "pure water: 1.1×10⁻⁴ M", color=RED, size=11, weight=700, anchor="start")
qx, qy = F(9.0, -1.25)
d.circle(qx, qy, 5, SAGE, SAGE, 0)
d.text(qx + 10, qy + 4, "pH 9: 5.6×10⁻² M — 500× more", color=SAGE, size=11, weight=700, anchor="start")
d.text(304, 768, "Mg(OH)₂,  Kₛₚ = 5.6×10⁻¹².  Buffered, s = Kₛₚ/[OH⁻]², so log s falls by 2 per pH unit.",
       color=NAVY, size=11.5, weight=700)
d.text(304, 786, "This is milk of magnesia: insoluble in the gut, freely soluble in stomach acid.", color=GREY, size=11)

d.rect(584, 452, 568, 254, BLUE, FILL[BLUE], 12, 2)
d.text(868, 484, "SELECTIVE PRECIPITATION — 0.10 M Ba²⁺ AND 0.10 M Ca²⁺", color=BLUE, weight=700, size=12.5)
d.text(868, 506, "adding sulfate slowly", color=GREY, size=10.5)
ROWS = [("BaSO₄ begins", "Kₛₚ = 1.1×10⁻¹⁰", "[SO₄²⁻] = 1.1×10⁻⁹ M", NAVY),
        ("CaSO₄ begins", "Kₛₚ = 4.9×10⁻⁵", "[SO₄²⁻] = 4.9×10⁻⁴ M", BLUE)]
yy = 540
for a, b, c3, col in ROWS:
    d.text(608, yy, a, color=col, size=12, weight=700, anchor="start")
    d.text(860, yy, b, color=GREY, size=10.5, anchor="end")
    d.text(1128, yy, c3, color=NAVY, size=11.5, weight=700, anchor="end")
    yy += 30
d.line(608, 608, 1128, 608, "#d9d2c4", 1, True)
d.text(868, 634, "when CaSO₄ just starts, [Ba²⁺] = 1.1×10⁻¹⁰ / 4.9×10⁻⁴ = 2.2×10⁻⁷ M",
       color=NAVY, size=11.5, weight=700)
d.text(868, 654, "99.9998% of the barium is already out before any calcium follows", color=BLUE, size=11.5, weight=700)
d.text(868, 676, "The ion needing the LOWER added-ion concentration goes first —", color=GREY, size=10.5)
d.text(868, 692, "which depends on its starting concentration as well as its Kₛₚ", color=GREY, size=10.5)

d.box(24, 806, 1128, 118, "Which salts care about pH, and which do not",
      "MORE SOLUBLE IN ACID — the anion is the conjugate base of a WEAK acid, so H⁺ removes it: CO₃²⁻, PO₄³⁻, OH⁻, S²⁻, F⁻, C₂O₄²⁻.   INDIFFERENT — the anion is the conjugate base of a STRONG acid and is never protonated in water: Cl⁻, Br⁻, I⁻, NO₃⁻. SO₄²⁻ is the near-miss: its parent HSO₄⁻ has pKₐ ≈ 1.9, so sulfates are pH-indifferent above about pH 4 but not in strong acid.   AND NOTE: K_f = 1/K_d. A huge formation constant is a tiny dissociation constant — the same statement twice.",
      NAVY, chars=148, size=12, head_size=13.5)
print(d.save("coupled-equilibria"))
