import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 1070,
      "Reading a distribution from three numbers",
      "Where the mean sits relative to the median tells you the shape",
      "Top: the three shapes and the ordering of mean, median and mode in each. The mode is always at the "
      "peak and the mean is always dragged toward the long tail, so the median ends up between them — which "
      "is why a mean far above a median is the signature of a right tail, and why the median is what you "
      "quote for income. Middle: the empirical rule, the one piece of arithmetic on this topic the exam "
      "expects you to do in your head. Bottom: standard deviation against standard error, and what error "
      "bars do and do not let you conclude — a question that depends entirely on which of the two is drawn."
      )

# ---------------- Panel A: three shapes ----------------
d.rect(40, 180, 840, 290, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Mean, median and mode in three shapes", color=NAVY, weight="bold", size=15)

import math

def curve_pts(f, x0, x1, n=120):
    return [(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]

def panel(x0, title, sub, kind, col):
    m = d.axes(x0, 236, 240, 120, "", "", (0, 10), (0, 1.05), ticks_x=0, ticks_y=0)
    if kind == "normal":
        f = lambda x: math.exp(-((x - 5) ** 2) / 4.0)
        peak, med, mean = 5.0, 5.0, 5.0
    elif kind == "right":
        f = lambda x: (math.exp(-((x - 3.1) ** 2) / 2.2) + 0.42 * math.exp(-((x - 5.6) ** 2) / 7.5))
        peak, med, mean = 3.1, 3.9, 4.7
    else:
        f = lambda x: (math.exp(-((x - 6.9) ** 2) / 2.2) + 0.42 * math.exp(-((x - 4.4) ** 2) / 7.5))
        peak, med, mean = 6.9, 6.1, 5.3
    pts = curve_pts(f, 0.2, 9.8)
    mx = max(p[1] for p in pts)
    pts = [(a, b / mx) for a, b in pts]
    d.curve(m, pts, col, 2.6)
    for val, lab, c in ((peak, "mode", GOLD), (med, "median", SAGE), (mean, "mean", RED)):
        px, py = m(val, 0)
        _, top = m(val, f(val) / mx * 0.92)
        d.line(px, py, px, top, c, 1.6, dash="3,2")
    d.text(x0 + 120, 378, title, color=col, weight="bold", size=11)
    d.text(x0 + 120, 396, sub, color=NAVY, weight="bold", size=10)
    d.text(x0 + 120, 414, "the tail is where the mean goes" if kind != "normal" else "all three coincide",
           color=GREY, size=8.5)

panel(70, "NORMAL", "mean = median = mode", "normal", BLUE)
panel(340, "POSITIVE / RIGHT SKEW", "mean > median > mode", "right", RED)
panel(610, "NEGATIVE / LEFT SKEW", "mean < median < mode", "left", SAGE)

d.text(285, 440, "mode", color=GOLD, weight="bold", size=9)
d.text(400, 440, "median", color=SAGE, weight="bold", size=9)
d.text(520, 440, "mean", color=RED, weight="bold", size=9)
d.text(460, 458, "a mean of $85k against a median of $52k is a right tail, which is why incomes are quoted as medians", color=GREY, size=9)

# ---------------- Panel B: empirical rule ----------------
d.rect(40, 486, 840, 214, GOLD, "none", rx=12, width=2)
d.text(460, 514, "The 68–95–99.7 rule", color=GOLD, weight="bold", size=14)

m = d.axes(170, 534, 580, 110, "", "", (-4, 4), (0, 1.05), ticks_x=0, ticks_y=0)
f = lambda x: math.exp(-(x ** 2) / 2.0)
d.curve(m, curve_pts(f, -4, 4), NAVY, 2.6)
for sd, col in ((1, SAGE), (2, GOLD), (3, RED)):
    for s in (-sd, sd):
        px, _ = m(s, 0)
        _, top = m(s, f(s))
        _, base = m(s, 0)
        d.line(px, base, px, top, col, 1.5, dash="3,2")

for s, lab in ((-3, "−3"), (-2, "−2"), (-1, "−1"), (0, "mean"), (1, "+1"), (2, "+2"), (3, "+3")):
    px, _ = m(s, 0)
    d.text(px, 662, lab, color=GREY, size=8.5)

d.text(460, 684, "±1 SD ≈ 68% · ±2 SD ≈ 95% · ±3 SD ≈ 99.7%", color=NAVY, weight="bold", size=11)

# ---------------- Panel C: SD vs SEM and error bars ----------------
d.rect(40, 716, 840, 330, BLUE, "none", rx=12, width=2)
d.text(460, 744, "SD, SEM, and what error bars let you say", color=BLUE, weight="bold", size=14)

d.rect(60, 764, 390, 92, SAGE, FILL[SAGE], rx=9, width=1.8)
d.text(255, 786, "STANDARD DEVIATION", color=SAGE, weight="bold", size=11)
d.text(255, 806, "how spread out the INDIVIDUALS are", color=NAVY, size=9)
d.text(255, 824, "does not shrink as you collect more data —", color=GREY, size=8.5)
d.text(255, 840, "it is a fact about the population", color=GREY, size=8.5)

d.rect(470, 764, 390, 92, RED, FILL[RED], rx=9, width=1.8)
d.text(665, 786, "STANDARD ERROR  =  SD ÷ √N", color=RED, weight="bold", size=11)
d.text(665, 806, "how precisely you know the MEAN", color=NAVY, size=9)
d.text(665, 824, "shrinks as N grows — it is a fact about", color=GREY, size=8.5)
d.text(665, 840, "your estimate, not about the people", color=GREY, size=8.5)

d.text(460, 882, "SO ERROR BARS MEAN DIFFERENT THINGS DEPENDING ON WHICH ONE IS DRAWN", color=NAVY, weight="bold", size=10)

bars = [("SD bars", "overlap or gap tells you almost nothing about significance", RED),
        ("SEM bars", "if they OVERLAP (and N is similar), p is well above 0.05;\na gap of about one SEM is where p reaches 0.05", GOLD),
        ("95% CI bars", "may overlap by up to about half an arm and still be significant;\nif they merely touch, the difference is already highly significant", SAGE)]
y = 898
for name, note, col in bars:
    lines = note.split("\n")
    h = 26 if len(lines) == 1 else 36
    d.rect(60, y, 800, h, col, FILL[col], rx=6, width=1.3)
    d.text(140, y + (17 if len(lines) == 1 else 22), name, color=col, weight="bold", size=9.5)
    for j, ln in enumerate(lines):
        d.text(560, y + (17 if len(lines) == 1 else 15 + j * 14), ln, color=GREY, size=8.5)
    y += h + 6

d.save("shape-from-three-numbers-and-error-bars")
print("ok")
