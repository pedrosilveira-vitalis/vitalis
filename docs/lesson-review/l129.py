import sys, math; sys.path.insert(0,'/home/claude/dkit')
from dkit import *

d = D(1180, 900, "Kₛₚ is not solubility",
      "The exponent pattern changes with the formula, so two salts can rank one way by Kₛₚ and the opposite way by how much actually dissolves. Convert first, then compare.",
      "A table converts the solubility product to molar solubility for four formula types. For a one-to-one salt such as silver chloride, the solubility product equals s squared and s is its square root, giving 1.3 times ten to the minus five molar from a solubility product of 1.8 times ten to the minus ten. For a one-to-two salt such as calcium fluoride, and equally for a two-to-one salt such as silver chromate, the solubility product equals four s cubed and s is the cube root of the solubility product over four: calcium fluoride at 3.9 times ten to the minus eleven gives 2.1 times ten to the minus four, and silver chromate at 1.1 times ten to the minus twelve gives 6.5 times ten to the minus five. For a three-to-two salt such as calcium phosphate, the solubility product equals 108 s to the fifth and s is the fifth root of the solubility product over 108, giving about 1.1 times ten to the minus seven from 2.1 times ten to the minus thirty-three. A panel drives the point home: silver chromate has a solubility product about 160 times smaller than silver chloride, yet dissolves about five times more, because its formula releases three ions instead of two. A second panel shows selective precipitation on a logarithmic chloride axis: starting from 0.10 molar silver and lead ions, silver chloride begins to precipitate once chloride reaches 1.8 times ten to the minus nine molar, while lead chloride does not begin until chloride reaches about 0.013 molar, leaving roughly seven orders of magnitude of chloride concentration in which silver is removed and lead is untouched. A footer gives the comparison of the ion product with the solubility product: below it the solution is unsaturated and more solid dissolves, equal to it the solution is saturated, above it the solution is supersaturated and solid precipitates until they match; and warns that when two solutions are mixed every concentration must first be recomputed for the combined volume, since forgetting the dilution is the commonest way these questions are lost.")

d.rect(24, 150, 1128, 246, NAVY, FILL[NAVY], 12, 2)
d.text(588, 178, "Kₛₚ → MOLAR SOLUBILITY, BY FORMULA TYPE", color=NAVY, weight=700, size=13.5)
HEAD = [(70, "type"), (250, "dissolution"), (560, "Kₛₚ in terms of s"), (790, "s from Kₛₚ"), (1120, "worked")]
for x, h in HEAD:
    d.text(x, 204, h.upper(), color=GREY, size=9.5,
           anchor="end" if x in (560, 1120) else "start")
ROWS = [
 ("MX", "MX ⇌ M⁺ + X⁻", "K = s²", "s = √K", "AgCl  1.8×10⁻¹⁰  →  1.3×10⁻⁵ M", NAVY),
 ("MX₂", "MX₂ ⇌ M²⁺ + 2X⁻", "K = s(2s)² = 4s³", "s = ∛(K/4)", "CaF₂  3.9×10⁻¹¹  →  2.1×10⁻⁴ M", BLUE),
 ("M₂X", "M₂X ⇌ 2M⁺ + X²⁻", "K = (2s)²s = 4s³", "s = ∛(K/4)", "Ag₂CrO₄  1.1×10⁻¹²  →  6.5×10⁻⁵ M", BLUE),
 ("M₃X₂", "M₃X₂ ⇌ 3M²⁺ + 2X³⁻", "K = (3s)³(2s)² = 108s⁵", "s = ⁵√(K/108)", "Ca₃(PO₄)₂  2.1×10⁻³³  →  1.1×10⁻⁷ M", RED),
]
yy = 234
for t, eq, kexp, sexp, worked, c in ROWS:
    d.text(70, yy, t, color=c, size=13, weight=700, anchor="start")
    d.text(250, yy, eq, color=NAVY, size=11.5, anchor="start")
    d.text(560, yy, kexp, color=NAVY, size=11.5, weight=700, anchor="end")
    d.text(790, yy, sexp, color=c, size=12, weight=700, anchor="end")
    d.text(1120, yy, worked, color=GREY, size=11, anchor="end")
    yy += 34
d.text(588, 378, "MX₂ and M₂X give the SAME formula — what matters is how many ions, not which one is doubled",
       color=NAVY, size=11.5, weight=700)

d.rect(24, 418, 448, 206, RED, FILL[RED], 12, 2)
d.text(248, 446, "THE TRAP THIS LESSON IS BUILT AROUND", color=RED, weight=700, size=12.5)
BARS = [("AgCl", 1.34, "Kₛₚ 1.8×10⁻¹⁰", NAVY),
        ("Ag₂CrO₄", 6.50, "Kₛₚ 1.1×10⁻¹²", RED)]
for i, (name, val, k, c) in enumerate(BARS):
    y = 486 + i*52
    d.text(48, y, name, color=NAVY, size=12, weight=700, anchor="start")
    d.text(48, y + 18, k, color=GREY, size=10.5, anchor="start")
    w = val / 6.5 * 180
    d.rect(170, y - 12, w, 20, c, c, 4, 0)
    d.text(170 + w + 8, y + 2, f"{val:.2f}×10⁻⁵ M", color=c, size=11.5, weight=700, anchor="start")
d.text(248, 596, "160× the smaller Kₛₚ — and 5× the solubility", color=RED, size=11.5, weight=700)

d.rect(492, 418, 660, 206, SAGE, FILL[SAGE], 12, 2)
d.text(822, 446, "SELECTIVE PRECIPITATION — THE WINDOW", color=SAGE, weight=700, size=12.5)
d.text(822, 466, "starting from 0.10 M Ag⁺ and 0.10 M Pb²⁺, adding Cl⁻ slowly", color=GREY, size=10.5)
ax0, ax1, axy = 540, 1110, 540
d.line(ax0, axy, ax1, axy, NAVY, 2)
def LX(logc): return ax0 + (logc + 10.0) / 10.0 * (ax1 - ax0)
for lc, lab in ((-10, "10⁻¹⁰"), (-8, "10⁻⁸"), (-6, "10⁻⁶"), (-4, "10⁻⁴"), (-2, "10⁻²"), (0, "1 M")):
    x = LX(lc)
    d.line(x, axy, x, axy + 5, NAVY, 1)
    d.text(x, axy + 18, lab, color=GREY, size=10)
for lc, lab, c, dy in ((math.log10(1.8e-9), "AgCl starts\n1.8×10⁻⁹ M", NAVY, -1),
                       (math.log10(0.013), "PbCl₂ starts\n0.013 M", RED, -1)):
    x = LX(lc)
    d.line(x, axy - 36, x, axy, c, 2, True)
    for j, part in enumerate(lab.split("\n")):
        d.text(x, axy - 60 + j*14, part, color=c, size=10.5, weight=700)
d.line(LX(math.log10(1.8e-9)), axy - 8, LX(math.log10(0.013)), axy - 8, SAGE, 7)
d.text(822, 600, "≈ 7 orders of magnitude of [Cl⁻] in which Ag⁺ is gone and Pb²⁺ is untouched",
       color=SAGE, size=11, weight=700)

d.rect(24, 648, 1128, 110, BLUE, FILL[BLUE], 12, 2)
d.text(588, 676, "COMPARE THE ION PRODUCT WITH Kₛₚ — SAME LOGIC AS Q vs K ANYWHERE ELSE", color=BLUE, weight=700, size=12.5)
QS = [("Q < Kₛₚ", "unsaturated", "more solid dissolves"),
      ("Q = Kₛₚ", "saturated", "no net change"),
      ("Q > Kₛₚ", "supersaturated", "precipitates until Q = Kₛₚ")]
for i, (q, state, what) in enumerate(QS):
    x = 100 + i * 376
    d.text(x, 708, q, color=BLUE, size=13, weight=700, anchor="start")
    d.text(x + 102, 708, state, color=NAVY, size=12, weight=700, anchor="start")
    d.text(x, 730, what, color=GREY, size=11, anchor="start")

d.box(24, 778, 1128, 92, "Before you compute Q, dilute",
      "Mixing two solutions dilutes BOTH: C_final = C_initial × V_initial / V_total. Mixing equal volumes halves every concentration, and for an MX₂ salt that drops Q eightfold — enough to turn a predicted precipitate into a clear solution. Also: only ions that appear in the Kₛₚ expression exert a common ion effect. Adding NaNO₃ to AgCl does nothing.",
      NAVY, chars=150, size=12, head_size=13.5)
print(d.save("ksp-to-solubility"))
