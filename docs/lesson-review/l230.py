import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 978,
      "Two routes in, and the one that sticks",
      "Whether a message is thought about decides how long its effect lasts",
      "Top: the elaboration likelihood model as a gate. Motivation and ability both have to be present for the "
      "central route; either one missing sends the message down the peripheral route. The two routes do not "
      "differ only in how persuasion happens but in what it produces: central-route change is durable, "
      "resistant and predicts behaviour, peripheral-route change is none of those. Note the counter-intuitive "
      "consequence in the middle — distracting an audience that would otherwise argue back can raise "
      "persuasion, because the distraction knocks out the counterarguing rather than the comprehension. Bottom "
      "left: dissonance and the three ways out of it, with the paradigms. Bottom right: what makes an attitude "
      "actually predict a behaviour."
      )

# ---------------- Panel A: the two routes ----------------
d.rect(40, 180, 840, 332, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Which route does the message take?", color=NAVY, weight="bold", size=15)

d.rect(360, 228, 200, 46, GREY, FILL[GREY], rx=8, width=1.6)
d.text(460, 248, "A PERSUASIVE MESSAGE", color=NAVY, weight="bold", size=11)
d.text(460, 265, "arrives", color=GREY, size=9.5)

d.rect(300, 290, 320, 42, NAVY, FILL[NAVY], rx=8, width=1.8)
d.text(460, 310, "MOTIVATED to think about it?", color=NAVY, weight="bold", size=10.5)
d.text(460, 326, "AND ABLE to — time, quiet, expertise?", color=GREY, size=9)

d.arrow(390, 338, 250, 362, SAGE, label="both yes", lx=-30, ly=-8, label_size=9.5)
d.arrow(530, 338, 670, 362, GOLD, label="either no", lx=30, ly=-8, label_size=9.5)

d.rect(70, 370, 350, 128, SAGE, FILL[SAGE], rx=10, width=2)
d.text(245, 394, "CENTRAL ROUTE", color=SAGE, weight="bold", size=13)
d.text(245, 414, "the argument itself is weighed", color=NAVY, size=10)
d.line(110, 426, 380, 426, SAGE, 1, dash="3,3")
for j, ln in enumerate(["change is DURABLE", "resists later counter-persuasion",
                        "and it predicts behaviour"]):
    d.text(245, 446 + j * 18, ln, color=NAVY if j == 0 else GREY, weight="bold" if j == 0 else "normal", size=10)

d.rect(500, 370, 350, 128, GOLD, FILL[GOLD], rx=10, width=2)
d.text(675, 394, "PERIPHERAL ROUTE", color=GOLD, weight="bold", size=13)
d.text(675, 414, "cues stand in for the argument", color=NAVY, size=10)
d.line(540, 426, 810, 426, GOLD, 1, dash="3,3")
for j, ln in enumerate(["change is FRAGILE", "source looks good, crowd agrees,",
                        "the message simply felt nice"]):
    d.text(675, 446 + j * 18, ln, color=NAVY if j == 0 else GREY, weight="bold" if j == 0 else "normal", size=10)

# ---------------- Panel B: dissonance ----------------
d.rect(40, 528, 410, 426, RED, "none", rx=12, width=2)
d.text(245, 556, "Dissonance, and the ways out", color=RED, weight="bold", size=15)

d.rect(64, 578, 362, 56, RED, FILL[RED], rx=9, width=2)
d.text(245, 600, "“I smoke”  +  “smoking kills”", color=RED, weight="bold", size=12)
d.text(245, 620, "an aversive state, like hunger — it demands action", color=GREY, size=9)

outs = [("CHANGE A COGNITION", "quit, or decide the risk is overstated", BLUE),
        ("ADD A COGNITION", "“but I run every morning” — rationalisation", GOLD),
        ("DEMOTE A COGNITION", "“life is short anyway” — trivialisation", SAGE)]
y = 646
for name, note, col in outs:
    d.rect(64, y, 362, 48, col, FILL[col], rx=8, width=1.6)
    d.text(245, y + 20, name, color=col, weight="bold", size=11)
    d.text(245, y + 37, note, color=GREY, size=9)
    y += 54

d.rect(64, 810, 362, 134, NAVY, FILL[NAVY], rx=10, width=2.2)
d.text(245, 834, "THE THREE PARADIGMS", color=NAVY, weight="bold", size=11)
for j, ln in enumerate(["INSUFFICIENT JUSTIFICATION — $1 beats $20,",
                        "because the big payment explains the lie away",
                        "POST-DECISION — after choosing, the chosen",
                        "option looks better and the rejected one worse",
                        "EFFORT JUSTIFICATION — a harsh initiation",
                        "makes a dull group seem worth joining"]):
    d.text(245, 854 + j * 15, ln, color=NAVY if j % 2 == 0 else GREY,
           weight="bold" if j % 2 == 0 else "normal", size=9)

# ---------------- Panel C: when attitudes predict ----------------
d.rect(470, 528, 410, 426, SAGE, "none", rx=12, width=2)
d.text(675, 556, "When an attitude predicts behaviour", color=SAGE, weight="bold", size=14)

cond = [("SPECIFICITY", "measure the attitude at the same grain as\nthe behaviour — “recycling”, not “the environment”", SAGE),
        ("STRENGTH AND ACCESS", "held with certainty, and it comes to mind fast", SAGE),
        ("DIRECT EXPERIENCE", "lived, not heard about", SAGE),
        ("WEAK SITUATION", "no social pressure pulling the other way", GOLD)]
y = 578
for name, note, col in cond:
    lines = note.split("\n")
    h = 34 + len(lines) * 13
    d.rect(494, y, 362, h, col, FILL[col], rx=8, width=1.6)
    d.text(675, y + 19, name, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(lines):
        d.text(675, y + 34 + j * 13, ln, color=GREY, size=9)
    y += h + 8

d.rect(494, y + 6, 362, 150, BLUE, FILL[BLUE], rx=10, width=2.2)
d.text(675, y + 30, "AND WHAT THE MODEL ADDS", color=BLUE, weight="bold", size=11)
d.text(675, y + 48, "theory of planned behaviour", color=NAVY, size=9.5)
for j, ln in enumerate(["ATTITUDE toward the behaviour",
                        "SUBJECTIVE NORMS — what others expect",
                        "PERCEIVED BEHAVIOURAL CONTROL — can I?"]):
    d.text(675, y + 70 + j * 17, ln, color=NAVY, weight="bold", size=9.5)
d.text(675, y + 128, "all three feed INTENTION, and intention predicts the act",
       color=GREY, size=9)

d.save("elaboration-routes-dissonance-and-attitude-behaviour")
print("ok")
