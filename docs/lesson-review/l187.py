import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 858,
      "Unpredictable pays worst and holds hardest",
      "Ratio or interval decides the rate; fixed or variable decides the persistence",
      "Top: the four schedules as cumulative response records. Variable ratio climbs steepest with no breaks; "
      "fixed ratio climbs almost as steeply but stops dead for a moment after each reward; variable interval "
      "rises at a gentle, even slope; fixed interval scallops, flat after each reward and accelerating as the "
      "next one comes due. Middle left: the two orderings to memorise, response rate highest for variable ratio "
      "down to lowest for fixed interval, and resistance to extinction highest for variable ratio down to lowest "
      "for continuous reinforcement. Middle right: why unpredictability persists — on a variable schedule a dry "
      "spell looks exactly like an ordinary gap, so the organism cannot tell that reinforcement has stopped. "
      "Bottom: shaping a lever press by reinforcing successive approximations while each earlier one is allowed "
      "to extinguish.")

# ---------------- Panel A: cumulative records ----------------
d.rect(40, 150, 840, 250, GOLD, "none", rx=12, width=2)
d.text(460, 178, "The four signatures, drawn as cumulative records",
       color=GOLD, weight="bold", size=16)

W, H, Y0 = 180, 120, 200
labels = [("variable ratio", "steepest, no pauses", RED),
          ("fixed ratio", "steep, then a pause", GOLD),
          ("variable interval", "gentle and even", SAGE),
          ("fixed interval", "scalloped", BLUE)]
x = 70
for i, (name, gloss, col) in enumerate(labels):
    d.rect(x, Y0, W, H, GREY, "none", rx=8, width=1.2)
    pts = []
    for k in range(0, 101):
        t = k / 100
        if i == 0:
            v = 0.95 * t
        elif i == 1:
            step = 0.25
            full = int(t // step)
            v = min(0.95, full * 0.23 + max(0.0, (t - full * step - 0.07)) * 0.92)
        elif i == 2:
            v = 0.55 * t
        else:
            seg = 0.25
            full = int(t // seg)
            frac = (t % seg) / seg
            v = min(0.95, full * 0.22 + 0.22 * frac ** 3)
        pts.append((x + 10 + t * (W - 20), Y0 + H - 12 - v * (H - 28)))
    d.path("M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts), col, 2.6)
    d.text(x + W / 2, Y0 + H + 22, name, color=col, weight="bold", size=13)
    d.text(x + W / 2, Y0 + H + 42, gloss, color=GREY, size=12)
    x += 200

d.text(460, 386, "time runs left to right; a steeper line means a faster rate of responding",
       color=GREY, size=12)

# ---------------- Panel B: the two orderings ----------------
d.rect(40, 416, 404, 230, BLUE, "none", rx=12, width=2)
d.text(242, 444, "Two orderings worth memorising", color=BLUE, weight="bold", size=15)

d.text(140, 476, "response rate", color=NAVY, weight="bold", size=13)
for i, (t, col) in enumerate([("VR", RED), ("FR", GOLD), ("VI", SAGE), ("FI", BLUE)]):
    d.rect(76 + i * 44, 490, 36, 30, col, FILL[col], rx=6, width=2)
    d.text(94 + i * 44, 511, t, color=col, weight="bold", size=14)
d.text(242, 540, "highest → lowest", color=GREY, size=12)

d.text(160, 572, "resistance to extinction", color=NAVY, weight="bold", size=13)
for i, (t, col) in enumerate([("VR", RED), ("VI", SAGE), ("FR", GOLD), ("FI", BLUE), ("CRF", GREY)]):
    d.rect(62 + i * 64, 586, 54, 30, col, FILL[col], rx=6, width=2)
    d.text(89 + i * 64, 607, t, color=col, weight="bold", size=13)
d.text(242, 634, "highest → lowest", color=GREY, size=12)

# ---------------- Panel C: why variable persists ----------------
d.rect(466, 416, 414, 230, RED, "none", rx=12, width=2)
d.text(673, 444, "Why unpredictable schedules hold on", color=RED, weight="bold", size=15)

d.text(673, 474, "on a FIXED schedule the gap is known,", color=GREY, size=13)
d.text(673, 494, "so a missed payout is obvious at once", color=NAVY, weight="bold", size=13)
yy = 520
for lab, pattern, col in [("fixed", "● ● ● ● ● ● ●   — — —", BLUE),
                          ("variable", "●●    ●      ●  ●●   — — —", RED)]:
    d.text(566, yy, lab, anchor="end", color=col, weight="bold", size=13)
    d.text(580, yy, pattern, anchor="start", color=col, size=15)
    yy += 30
d.text(673, 596, "after a variable schedule stops, the dry spell is", color=GREY, size=13)
d.text(673, 616, "indistinguishable from an ordinary run of bad luck", color=NAVY, weight="bold", size=13)
d.text(673, 636, "— this is the partial reinforcement extinction effect", color=GREY, size=12)

# ---------------- Panel D: shaping ----------------
d.rect(40, 662, 840, 180, SAGE, "none", rx=12, width=2)
d.text(460, 690, "Shaping: reinforce what is closer, let the rest extinguish",
       color=SAGE, weight="bold", size=16)

steps = ["moves toward\nthat side", "comes within\nan inch", "touches\nthe lever", "presses it\nat all",
         "presses hard\nenough"]
x = 72
for i, s in enumerate(steps):
    col = SAGE if i < 4 else RED
    d.rect(x, 714, 142, 70, col, FILL[col], rx=9, width=2)
    a, b = s.split("\n")
    d.text(x + 71, 742, a, color=NAVY, weight="bold", size=12)
    d.text(x + 71, 762, b, color=NAVY, weight="bold", size=12)
    if i < 4:
        d.arrow(x + 146, 749, x + 166, 749, GREY, width=2)
    x += 170

d.text(460, 812, "at every step the previous approximation stops being reinforced — "
                 "that is what drags the behaviour forward",
       color=GREY, size=13)

d.save("reinforcement-schedules-and-shaping")
print("ok")
