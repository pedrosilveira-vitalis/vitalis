import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 860,
      "Learning and performing are two different things",
      "Watch, remember, be able to do it, and want to — all four, or nothing shows",
      "Top: the four processes of observational learning as a chain — attention, retention, reproduction and "
      "motivation — with the thing that breaks each one written underneath, and the note that the chain is only "
      "as strong as its weakest link. Middle left: the 1965 Bobo doll follow-up, where children who saw the model "
      "punished imitated less on their own, but imitated just as much as everyone else once they were offered a "
      "reward — showing that all three groups had learned equally and only motivation differed. Middle right: "
      "the four sources of self-efficacy in order of strength, from doing it yourself through watching someone "
      "like you, being told you can, and how your body feels. Bottom: reciprocal determinism as a triangle of "
      "person, behaviour and environment, each arrow running both ways."
      )

# ---------------- Panel A: four processes ----------------
d.rect(40, 150, 840, 182, BLUE, "none", rx=12, width=2)
d.text(460, 178, "All four, in order", color=BLUE, weight="bold", size=16)

procs = [("ATTENTION", "did you notice it?", "a dull or confusing model"),
         ("RETENTION", "can you still recall it?", "no rehearsal, no coding"),
         ("REPRODUCTION", "can your body do it?", "the sub-skills are missing"),
         ("MOTIVATION", "do you want to?", "you saw the model punished")]
x = 62
for i, (name, q, fail) in enumerate(procs):
    d.rect(x, 198, 180, 86, BLUE, FILL[BLUE], rx=10, width=2)
    d.text(x + 90, 224, name, color=BLUE, weight="bold", size=14)
    d.text(x + 90, 248, q, color=NAVY, size=12)
    d.text(x + 90, 270, fail, color=RED, size=11)
    if i < 3:
        d.arrow(x + 184, 241, x + 202, 241, GREY, width=2)
    x += 206

d.text(460, 312, "break any one link and nothing appears — and only the last one is about wanting to",
       color=GREY, size=13)

# ---------------- Panel B: the 1965 follow-up ----------------
d.rect(40, 348, 440, 266, RED, "none", rx=12, width=2)
d.text(260, 376, "Bobo, 1965: learned or merely performed?", color=RED, weight="bold", size=15)

m = d.axes(118, 392, 300, 112, "", "imitation shown", (0, 3), (0, 1.15), ticks_x=None, ticks_y=None)
groups = [("model\nrewarded", 0.92, 0.95), ("model\npunished", 0.38, 0.93), ("no\nconsequence", 0.74, 0.94)]
bw = 44
for i, (lab, spont, paid) in enumerate(groups):
    cx = 0.5 + i
    px, py0 = m(cx, 0)
    _, py1 = m(cx, spont)
    d.rect(px - bw - 4, py1, bw, py0 - py1, RED, FILL[RED], rx=3, width=2)
    _, py2 = m(cx, paid)
    d.rect(px + 4, py2, bw, py0 - py2, SAGE, FILL[SAGE], rx=3, width=2)
    a, b = lab.split("\n")
    d.text(px, py0 + 18, a, color=NAVY, size=12)
    d.text(px, py0 + 33, b, color=NAVY, size=12)

d.legend(126, 546, [(RED, "left to themselves", False), (SAGE, "offered a reward to copy it", False)])
d.text(260, 606, "once paid, every group performed alike — they had all learned it",
       color=NAVY, weight="bold", size=13)

# ---------------- Panel C: self-efficacy ----------------
d.rect(500, 348, 380, 266, SAGE, "none", rx=12, width=2)
d.text(690, 376, "Where self-efficacy comes from", color=SAGE, weight="bold", size=15)

srcs = [("mastery experience", "you did it yourself", 1.0),
        ("vicarious experience", "someone like you did it", 0.75),
        ("verbal persuasion", "someone credible says you can", 0.5),
        ("bodily state", "calm reads as able; anxiety does not", 0.3)]
y = 404
for name, gloss, strength in srcs:
    w = int(300 * strength)
    d.rect(530, y, w, 22, SAGE, FILL[SAGE], rx=5, width=1.6)
    d.text(536, y + 16, name, anchor="start", color=SAGE, weight="bold", size=13)
    d.text(536, y + 36, gloss, anchor="start", color=GREY, size=12)
    y += 48

d.text(690, 598, "domain-specific: not the same thing as self-esteem", color=NAVY, weight="bold", size=13)

# ---------------- Panel D: reciprocal determinism ----------------
d.rect(40, 630, 840, 200, GOLD, "none", rx=12, width=2)
d.text(460, 658, "Reciprocal determinism: every arrow runs both ways",
       color=GOLD, weight="bold", size=16)

TX, TY = 460, 700
pts = {"PERSON": (TX, TY), "BEHAVIOUR": (TX - 150, TY + 86), "ENVIRONMENT": (TX + 150, TY + 86)}
for name, (px, py) in pts.items():
    d.rect(px - 92, py - 20, 184, 42, GOLD, FILL[GOLD], rx=9, width=2)
    d.text(px, py + 6, name, color=GOLD, weight="bold", size=14)
d.text(TX, TY - 28, "beliefs, expectations, self-efficacy", color=GREY, size=12)
d.text(TX - 150, TY + 128, "what you actually do", color=GREY, size=12)
d.text(TX + 150, TY + 128, "setting, others, contingencies", color=GREY, size=12)

for (ax, ay), (bx, by) in [((TX - 50, TY + 28), (TX - 120, TY + 58)),
                           ((TX + 50, TY + 28), (TX + 120, TY + 58)),
                           ((TX - 58, TY + 86), (TX + 58, TY + 86))]:
    d.arrow(ax, ay, bx, by, NAVY, width=1.8)
    d.arrow(bx, by, ax, ay, NAVY, width=1.8)

d.save("observational-learning-and-self-efficacy")
print("ok")
