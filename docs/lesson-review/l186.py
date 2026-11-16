import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 880,
      "Ask two questions: added or taken away, and did the behaviour go up?",
      "Positive and negative mean add and subtract — nothing about good or bad",
      "Top: the two-by-two table of operant contingencies. Adding something and the behaviour rising is positive "
      "reinforcement; taking something away and the behaviour rising is negative reinforcement, which covers both "
      "escape and avoidance; adding something and the behaviour falling is positive punishment; taking something "
      "away and the behaviour falling is negative punishment. Middle: the four reinforcement schedules drawn as "
      "cumulative response curves — variable ratio steepest with no pauses, fixed ratio steep with a pause after "
      "each reward, variable interval steady and moderate, fixed interval scalloped. Bottom: the shape of operant "
      "extinction, with the burst of harder responding that comes first, and a reminder that the three-term "
      "contingency runs antecedent, behaviour, consequence.")

# ---------------- Panel A: the 2x2 ----------------
d.rect(40, 150, 840, 262, BLUE, "none", rx=12, width=2)
d.text(460, 178, "The whole system is one table", color=BLUE, weight="bold", size=16)

CX, CY, W, H = 240, 200, 300, 92
d.text(CX + W / 2, 216, "behaviour GOES UP", color=SAGE, weight="bold", size=14)
d.text(CX + W + 20 + W / 2, 216, "behaviour GOES DOWN", color=RED, weight="bold", size=14)
d.text(228, 272, "something", anchor="end", color=NAVY, weight="bold", size=14)
d.text(228, 292, "is ADDED", anchor="end", color=NAVY, weight="bold", size=14)
d.text(228, 364, "something", anchor="end", color=NAVY, weight="bold", size=14)
d.text(228, 384, "is TAKEN AWAY", anchor="end", color=NAVY, weight="bold", size=14)

cells = [(CX, 228, "positive reinforcement", "praise for studying", SAGE),
         (CX + W + 20, 228, "positive punishment", "a speeding ticket", RED),
         (CX, 324, "negative reinforcement", "lever press stops the shock", SAGE),
         (CX + W + 20, 324, "negative punishment", "phone taken for a week", RED)]
for x, y, name, ex, col in cells:
    d.rect(x, y, W, 80, col, FILL[col], rx=10, width=2)
    d.text(x + W / 2, y + 32, name, color=col, weight="bold", size=15)
    d.text(x + W / 2, y + 58, ex, color=NAVY, size=12)

# ---------------- Panel B: schedules ----------------
d.rect(40, 428, 840, 268, GOLD, "none", rx=12, width=2)
d.text(460, 456, "Cumulative responses: each schedule has its own signature",
       color=GOLD, weight="bold", size=16)

m = d.axes(120, 476, 470, 128, "time", "total responses", (0, 10), (0, 10),
           ticks_x=None, ticks_y=None)


def vr(t):
    return 0.95 * t


def fr(t):
    out = 0.0
    step = 1.6
    full = int(t // step)
    out = full * 1.35 + max(0.0, (t - full * step - 0.35)) * 0.95
    return min(out, 9.6)


def vi(t):
    return 0.42 * t


def fi(t):
    out = 0.0
    for k in range(int(t // 2.5)):
        out += 1.1
    frac = (t % 2.5) / 2.5
    return min(9.6, out + 1.1 * frac ** 3)


for f, col, lab, dy in [(vr, RED, "variable ratio", -2), (fr, GOLD, "fixed ratio", 6),
                        (vi, SAGE, "variable interval", 18), (fi, BLUE, "fixed interval", 0)]:
    d.curve(m, [(t / 25, min(9.7, f(t / 25))) for t in range(0, 251)], col, 2.6)
    px, py = m(10, min(9.7, f(10)))
    d.text(px + 8, py + dy, lab, anchor="start", color=col, weight="bold", size=12)

d.text(460, 666, "ratio schedules pay per response, so they drive the rate up; "
                 "interval schedules pay per clock tick",
       color=GREY, size=13)
d.text(460, 686, "variable ratio is both the fastest and the hardest to extinguish — "
                 "which is what a slot machine runs on",
       color=NAVY, weight="bold", size=13)

# ---------------- Panel C: extinction ----------------
d.rect(40, 712, 404, 150, RED, "none", rx=12, width=2)
d.text(242, 740, "Stop reinforcing and it gets worse first", color=RED, weight="bold", size=15)

m2 = d.axes(96, 760, 290, 64, "", "rate", (0, 10), (0, 1.25), ticks_x=None, ticks_y=None)


def burst(t):
    if t < 3:
        return 0.72
    return max(0.03, 1.15 * math.exp(-(t - 3.4) / 1.9)) if t > 3.4 else 1.15


d.curve(m2, [(t / 25, burst(t / 25)) for t in range(0, 251)], RED, 2.6)
px, py = m2(3.1, 1.15)
d.text(px + 6, py - 8, "extinction burst", anchor="start", color=RED, weight="bold", size=12)
px, py = m2(3, 0.72)
d.line(px, py + 12, px, py - 52, GREY, 1.4, True)
d.text(px + 6, py + 28, "reinforcement stops", anchor="start", color=GREY, size=11)

# ---------------- Panel D: three-term ----------------
d.rect(466, 712, 414, 150, SAGE, "none", rx=12, width=2)
d.text(673, 740, "Everything sits in a three-term contingency", color=SAGE, weight="bold", size=15)

terms = [("antecedent", "the Sᴰ that says reward is available", 768),
         ("behaviour", "what the organism emits", 798),
         ("consequence", "what changes its future odds", 828)]
for name, gloss, y in terms:
    d.text(620, y, name, anchor="end", color=SAGE, weight="bold", size=14)
    d.text(634, y, gloss, anchor="start", color=NAVY, size=12)
    if y < 820:
        d.arrow(600, y + 8, 600, y + 20, GREY, width=1.6)

d.save("operant-contingencies-and-schedules")
print("ok")
