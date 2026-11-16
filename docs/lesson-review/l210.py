import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 906,
      "One injection, two rooms, two emotions",
      "The experiments are the argument — learn what each one rules out",
      "Top: Schachter and Singer's design, which is the whole two-factor theory in one table. Everyone in the "
      "epinephrine rows has the same racing heart. The only thing that differs is whether they have an "
      "explanation for it. Those who do blame the drug and feel little; those who do not borrow an "
      "explanation from whoever is in the room with them, and end up euphoric or furious accordingly. The "
      "saline rows have nothing to label and feel almost nothing. Middle: the same logic in the field — "
      "arousal left over from a frightening bridge gets re-attributed to the person standing on it. Bottom: "
      "Lazarus's two appraisals, which decide not just how strong the emotion is but which emotion it is, and "
      "why the same event lands differently on two different people."
      )

# ---------------- Panel A: the 1962 design ----------------
d.rect(40, 176, 840, 288, GOLD, "none", rx=12, width=2)
d.text(460, 204, "Schachter and Singer, 1962", color=GOLD, weight="bold", size=16)

col_x = [300, 470, 640, 810]
d.text(470, 236, "with a EUPHORIC confederate", color=GREY, weight="bold", size=11)
d.text(740, 236, "with an ANGRY confederate", color=GREY, weight="bold", size=11)
d.line(70, 246, 850, 246, GREY, 1, dash="3,3")

rows = [
    ("EPINEPHRINE,\nuninformed", "feels euphoric", "feels angry",
     "no explanation → borrows one from the room", RED),
    ("EPINEPHRINE,\nmisinformed", "feels euphoric", "feels angry",
     "wrong explanation → same as above", RED),
    ("EPINEPHRINE,\ninformed", "little effect", "little effect",
     "“it's the drug” — arousal already explained", BLUE),
    ("SALINE,\nplacebo", "little effect", "little effect",
     "no arousal to label at all", GREY),
]
y = 258
for label, left, right, note, col in rows:
    l1, l2 = label.split("\n")
    d.rect(70, y, 150, 42, col, FILL[col], rx=7, width=2)
    d.text(145, y + 18, l1, color=col, weight="bold", size=10)
    d.text(145, y + 32, l2, color=col, weight="bold", size=10)
    d.text(470, y + 20, left, color=NAVY, weight="bold", size=12)
    d.text(740, y + 20, right, color=NAVY, weight="bold", size=12)
    d.text(470, y + 38, note, color=GREY, size=10)
    y += 46

d.text(460, 454, "identical arousal · different label · different emotion",
       color=GOLD, weight="bold", size=13)

# ---------------- Panel B: excitation transfer ----------------
d.rect(40, 480, 840, 160, RED, "none", rx=12, width=2)
d.text(460, 508, "Excitation transfer, in the field", color=RED, weight="bold", size=16)

steps = [("the bridge is terrifying", "sympathetic arousal", GREY),
         ("the arousal outlasts it", "no obvious cause left", RED),
         ("someone attractive is there", "the arousal gets re-labelled", SAGE),
         ("“I must be attracted”", "Dutton and Aron, 1974", GOLD)]
x = 66
for a, b, col in steps:
    d.rect(x, 532, 188, 76, col, FILL[col], rx=9, width=2)
    d.text(x + 94, 560, a, color=col, weight="bold", size=11)
    d.text(x + 94, 584, b, color=GREY, size=11)
    if x < 600:
        d.arrow(x + 188, 570, x + 196, 570, GREY, width=1.8)
    x += 196

# ---------------- Panel C: Lazarus ----------------
d.rect(40, 656, 840, 220, SAGE, "none", rx=12, width=2)
d.text(460, 684, "Lazarus: two appraisals, then the emotion", color=SAGE, weight="bold", size=16)

d.rect(70, 704, 340, 150, SAGE, FILL[SAGE], rx=10, width=2)
d.text(240, 728, "PRIMARY — does this matter to me?", color=SAGE, weight="bold", size=12)
for i, (a, b) in enumerate([("irrelevant", "no emotion follows"),
                            ("benign-positive", "pleasant emotions"),
                            ("harm or loss", "grief, anger — damage done"),
                            ("threat", "anxiety — damage ahead"),
                            ("challenge", "excitement — a chance to master")]):
    d.text(228, 754 + i * 20, a, anchor="end", color=NAVY, weight="bold", size=11)
    d.text(240, 754 + i * 20, b, anchor="start", color=GREY, size=11)

d.rect(440, 704, 410, 150, BLUE, FILL[BLUE], rx=10, width=2)
d.text(645, 728, "SECONDARY — what can I do about it?", color=BLUE, weight="bold", size=12)
d.text(645, 756, "what are my options, and will they work?", color=NAVY, size=12)
d.text(645, 780, "controllable threat → focused concern", color=GREY, size=11)
d.text(645, 800, "uncontrollable threat → helplessness", color=GREY, size=11)
d.text(645, 830, "reappraisal changes the emotion later —", color=BLUE, weight="bold", size=11)
d.text(645, 846, "this is the lever cognitive therapy pulls", color=BLUE, weight="bold", size=11)

d.save("schachter-singer-design-and-lazarus-appraisal")
print("ok")
