import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 872,
      "Conditioning is about prediction, not mere pairing",
      "If the CS tells you nothing you did not already know, nothing is learned",
      "Top left: blocking shown in two phases — a tone is first trained to predict the shock, then a light is "
      "added alongside it, and because the tone already predicts the shock perfectly the light is learned "
      "hardly at all. Beneath it the Rescorla-Wagner rule, in which the change in associative strength is "
      "proportional to how surprising the outcome still is. Top right: the four ways an extinguished response "
      "comes back — spontaneous recovery after a rest, renewal in a different context, reinstatement after the "
      "US alone, and rapid reacquisition on re-pairing — all of them evidence that extinction added new "
      "inhibitory learning rather than deleting the old association. Bottom left: discrimination training "
      "narrowing the generalisation gradient around the reinforced stimulus and shifting its peak away from the "
      "unreinforced one. Bottom right: the effects that change how readily something is learned — latent "
      "inhibition, overshadowing, preparedness and second-order conditioning.")

# ---------------- Panel A: blocking ----------------
d.rect(40, 150, 420, 300, BLUE, "none", rx=12, width=2)
d.text(250, 178, "Blocking: no surprise, no learning", color=BLUE, weight="bold", size=15)

d.rect(70, 198, 360, 72, SAGE, FILL[SAGE], rx=9, width=2)
d.text(250, 220, "Phase 1", color=SAGE, weight="bold", size=13)
d.text(250, 244, "tone → shock, many times", color=NAVY, weight="bold", size=14)
d.text(250, 262, "the tone now predicts the shock fully", color=GREY, size=12)

d.rect(70, 282, 360, 90, RED, FILL[RED], rx=9, width=2)
d.text(250, 304, "Phase 2", color=RED, weight="bold", size=13)
d.text(250, 328, "tone + light → shock", color=NAVY, weight="bold", size=14)
d.text(250, 350, "test the light alone: almost no fear", color=RED, weight="bold", size=13)
d.text(250, 366, "nothing was left to explain", color=GREY, size=12)

d.text(250, 400, "ΔV = αβ(λ − ΣV)", color=NAVY, weight="bold", size=19)
d.text(250, 426, "learning stops as ΣV approaches λ", color=GREY, size=13)

# ---------------- Panel B: return of the CR ----------------
d.rect(480, 150, 400, 300, GOLD, "none", rx=12, width=2)
d.text(680, 178, "Four ways the response comes back", color=GOLD, weight="bold", size=15)

items = [("spontaneous recovery", "just let time pass", SAGE),
         ("renewal", "test it somewhere else", BLUE),
         ("reinstatement", "give the US on its own", RED),
         ("rapid reacquisition", "re-pair once or twice", GOLD)]
y = 202
for name, how, col in items:
    d.rect(506, y, 348, 48, col, FILL[col], rx=9, width=2)
    d.text(560, y + 30, name, anchor="start", color=col, weight="bold", size=14)
    d.text(840, y + 30, how, anchor="end", color=GREY, size=12)
    y += 54

d.text(680, 438, "so extinction wrote something new; it erased nothing",
       color=NAVY, weight="bold", size=14)

# ---------------- Panel C: gradient and peak shift ----------------
d.rect(40, 466, 420, 250, SAGE, "none", rx=12, width=2)
d.text(250, 494, "Training discrimination narrows the gradient", color=SAGE, weight="bold", size=15)

m = d.axes(110, 516, 300, 120, "stimulus along the dimension", "CR", (-3.2, 3.2), (0, 1.15),
           ticks_x=None, ticks_y=None)
d.curve(m, [(x / 10, 0.95 * math.exp(-(x / 10) ** 2 / 2.2)) for x in range(-32, 33)], GREY, 2.2, dash=True)
d.curve(m, [(x / 10, math.exp(-((x / 10 - 0.55) ** 2) / 0.5)) for x in range(-32, 33)], SAGE, 2.8)
px, py = m(0, 0)
d.line(px, py, px, py - 12, NAVY, 2)
d.text(px, py + 20, "CS+", color=NAVY, weight="bold", size=13)
px2, py2 = m(-1.4, 0)
d.line(px2, py2, px2, py2 - 12, RED, 2)
d.text(px2, py2 + 20, "CS−", color=RED, weight="bold", size=13)
px3, py3 = m(0.55, 1)
d.circle(px3, py3, 4, SAGE, SAGE)
d.text(px3 + 8, py3 - 8, "peak shift", anchor="start", color=SAGE, weight="bold", size=12)
d.text(250, 700, "before training (dashed) the gradient is broad and centred on the CS+",
       color=GREY, size=12)

# ---------------- Panel D: what changes learnability ----------------
d.rect(480, 466, 400, 250, RED, "none", rx=12, width=2)
d.text(680, 494, "What makes a CS easy or hard to learn", color=RED, weight="bold", size=15)

rows = [("latent inhibition", "seen it before with no US ⇒ slower"),
        ("overshadowing", "a louder partner CS takes the strength"),
        ("preparedness", "taste–nausea is learned in one trial;"),
        ("", "tone–nausea hardly at all"),
        ("second-order", "CS1 can train CS2 — weaker, and CS1"),
        ("", "extinguishes while you do it")]
y = 524
for a, b in rows:
    if a:
        d.text(690, y, a, anchor="end", color=RED, weight="bold", size=13)
    d.text(700, y, b, anchor="start", color=NAVY, size=12)
    y += 28

d.text(680, 700, "partial reinforcement during training slows extinction later",
       color=NAVY, weight="bold", size=13)

d.text(460, 760, "Contiguity is not enough — the CS must raise the odds of the US",
       color=NAVY, weight="bold", size=17)
d.text(460, 792, "A US that occurs just as often without the CS teaches nothing (Rescorla)",
       color=GREY, size=14)
d.text(460, 822, "Clinically: relapse after exposure therapy is the same four effects,",
       color=GREY, size=14)
d.text(460, 846, "which is why extinction is practised in many contexts",
       color=GREY, size=14)

d.save("prediction-blocking-and-the-return-of-the-cr")
print("ok")
