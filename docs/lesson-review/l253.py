import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 1004,
      "One constant holds the whole scale together",
      "Kᵥᵥ = [H⁺][OH⁻], and everything else is a logarithm of it",
      "Top: the two scales as mirror images. Fix [H⁺] anywhere on the line and [OH⁻] is determined, because "
      "their product is pinned at 1.0 × 10⁻¹⁴ at 25 °C. That is why pH and pOH must sum to 14 and why one "
      "step along the scale is a tenfold change in concentration, not a small one. Middle: the arithmetic "
      "without a calculator, which comes down to splitting a concentration into a power of ten and a "
      "coefficient you know the log of. Bottom: the two traps — neutrality is not pH 7 except at 25 °C, and a "
      "very dilute acid approaches pH 7 from below without ever crossing it."
      )

# ---------------- Panel A: mirrored scales ----------------
d.rect(40, 180, 840, 262, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Two scales, one constant", color=NAVY, weight="bold", size=15)

x0, x1 = 110, 830
def xp(ph):
    return x0 + (x1 - x0) * ph / 14.0

d.line(x0, 268, x1, 268, GREY, 2)
d.line(x0, 348, x1, 348, GREY, 2)

for ph in range(0, 15, 2):
    px = xp(ph)
    d.line(px, 262, px, 274, GREY, 1.4)
    d.text(px, 256, str(ph), color=NAVY, weight="bold", size=9)
    d.line(px, 342, px, 354, GREY, 1.4)
    d.text(px, 368, str(14 - ph), color=NAVY, weight="bold", size=9)

d.text(x0 - 16, 272, "pH", anchor="end", color=NAVY, weight="bold", size=10)
d.text(x0 - 16, 352, "pOH", anchor="end", color=NAVY, weight="bold", size=10)

d.text(xp(3), 300, "ACIDIC", color=RED, weight="bold", size=11)
d.text(xp(3), 318, "[H⁺] > [OH⁻]", color=GREY, size=9)
d.text(xp(7), 300, "NEUTRAL", color=NAVY, weight="bold", size=11)
d.text(xp(7), 318, "[H⁺] = [OH⁻]", color=GREY, size=9)
d.text(xp(11), 300, "BASIC", color=BLUE, weight="bold", size=11)
d.text(xp(11), 318, "[H⁺] < [OH⁻]", color=GREY, size=9)

d.line(xp(7), 262, xp(7), 288, NAVY, 1.6, dash="4,3")
d.line(xp(7), 326, xp(7), 354, NAVY, 1.6, dash="4,3")

d.text(460, 400, "pH + pOH = pKᵥᵥ = 14.00 at 25 °C · one unit of pH = a TENFOLD change in [H⁺] · 0.30 units = twofold",
       color=NAVY, weight="bold", size=10)
d.text(460, 422, "blood at 7.40 falling to 7.10 doubles [H⁺] — which is why a tenth of a pH unit is a clinical emergency",
       color=GREY, size=9)

# ---------------- Panel B: doing it without a calculator ----------------
d.rect(40, 458, 840, 234, GOLD, "none", rx=12, width=2)
d.text(460, 486, "Doing it without a calculator", color=GOLD, weight="bold", size=14)

d.rect(60, 506, 390, 166, BLUE, FILL[BLUE], rx=9, width=1.8)
d.text(255, 528, "SPLIT, THEN SUBTRACT", color=BLUE, weight="bold", size=11)
steps = ["[H⁺] = A × 10⁻ⁿ, with 1 ≤ A < 10",
         "pH = n − log A",
         "",
         "[H⁺] = 4.0 × 10⁻⁵",
         "pH = 5 − log 4 = 5 − 0.60 = 4.40",
         "",
         "so the answer always lands between",
         "n − 1 and n, nearer n for small A"]
for j, ln in enumerate(steps):
    if not ln:
        continue
    bold = ln.startswith("pH = 5") or ln.startswith("[H⁺] = 4.0")
    d.text(255, 552 + j * 15, ln, color=NAVY if bold else GREY, weight="bold" if bold else "normal", size=8.5)

d.rect(470, 506, 390, 166, SAGE, FILL[SAGE], rx=9, width=1.8)
d.text(665, 528, "THE LOGS TO KNOW", color=SAGE, weight="bold", size=11)
logs = [("2", "0.30"), ("3", "0.48"), ("4", "0.60"), ("5", "0.70"),
        ("6", "0.78"), ("7", "0.85"), ("8", "0.90"), ("9", "0.95")]
cx = 530
cy = 554
for i, (n, v) in enumerate(logs):
    col = cx + (i % 4) * 90
    row = cy + (i // 4) * 30
    d.text(col, row, "log " + n, color=NAVY, weight="bold", size=9)
    d.text(col, row + 14, v, color=GREY, size=9)

d.text(665, 630, "log 2 = 0.30 is the one that earns its keep:", color=NAVY, weight="bold", size=8.5)
d.text(665, 646, "any 0.30 shift in pH is a factor of two in [H⁺],", color=GREY, size=8.5)
d.text(665, 660, "and log 4 = 2 log 2, log 5 = 1 − log 2", color=GREY, size=8.5)

# ---------------- Panel C: the two traps ----------------
d.rect(40, 708, 840, 276, RED, "none", rx=12, width=2)
d.text(460, 736, "The two traps", color=RED, weight="bold", size=14)

d.rect(60, 756, 390, 212, GOLD, FILL[GOLD], rx=9, width=1.8)
d.text(255, 778, "NEUTRAL IS NOT “pH 7”", color=GOLD, weight="bold", size=11)
d.text(255, 796, "neutral means [H⁺] = [OH⁻], i.e. pH = ½ pKᵥᵥ", color=NAVY, size=8.5)
d.text(255, 812, "autoionization is endothermic, so heating", color=GREY, size=8.5)
d.text(255, 826, "raises Kᵥᵥ and lowers neutral pH", color=GREY, size=8.5)

rows = [("0 °C", "0.11 × 10⁻¹⁴", "7.47"),
        ("25 °C", "1.00 × 10⁻¹⁴", "7.00"),
        ("37 °C", "2.42 × 10⁻¹⁴", "6.81"),
        ("100 °C", "51.3 × 10⁻¹⁴", "6.14")]
d.text(120, 850, "T", color=NAVY, weight="bold", size=8.5)
d.text(260, 850, "Kᵥᵥ", color=NAVY, weight="bold", size=8.5)
d.text(390, 850, "neutral pH", color=NAVY, weight="bold", size=8.5)
y = 868
for t, kw, nph in rows:
    d.text(120, y, t, color=GREY, size=8.5)
    d.text(260, y, kw, color=GREY, size=8.5)
    d.text(390, y, nph, color=NAVY if t != "25 °C" else GREY, weight="bold" if t != "25 °C" else "normal", size=8.5)
    y += 17

d.text(255, 952, "at body temperature, neutral is about 6.81", color=GOLD, weight="bold", size=9)

d.rect(470, 756, 390, 212, BLUE, FILL[BLUE], rx=9, width=1.8)
d.text(665, 778, "VERY DILUTE ACID NEVER GOES BASIC", color=BLUE, weight="bold", size=10.5)
d.text(665, 796, "1.0 × 10⁻⁸ M HCl is NOT pH 8", color=NAVY, weight="bold", size=9.5)

d.rect(500, 812, 330, 46, RED, FILL[RED], rx=7, width=1.4)
d.text(665, 830, "naive: [H⁺] = C → pH 8", color=RED, weight="bold", size=9)
d.text(665, 846, "an acid that made the water basic", color=GREY, size=8.5)

d.arrow(665, 860, 665, 878, GREY)

d.rect(500, 882, 330, 62, SAGE, FILL[SAGE], rx=7, width=1.4)
d.text(665, 902, "water still supplies about 10⁻⁷ M", color=SAGE, weight="bold", size=9)
d.text(665, 920, "total [H⁺] sits just above 10⁻⁷, so the pH", color=GREY, size=8.5)
d.text(665, 934, "is just BELOW 7 — acidic, but barely", color=GREY, size=8.5)

d.text(665, 960, "dilution drives any solution toward 7 and never past it", color=BLUE, weight="bold", size=9)

d.save("kw-holds-the-scale-and-two-traps")
print("ok")
