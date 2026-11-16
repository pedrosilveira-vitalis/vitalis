import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 860,
      "The CS borrows its power from what it predicts",
      "Name the US first, then the UR — the other two labels follow without guessing",
      "Top: the four labels laid on a timeline. Before conditioning the food produces salivation with no learning, "
      "so food is the unconditioned stimulus and that salivation the unconditioned response, while the bell does "
      "nothing. During conditioning the bell comes just before the food, about half a second ahead. After "
      "conditioning the bell alone produces salivation, so the bell is now the conditioned stimulus and that "
      "salivation the conditioned response, usually a little weaker than the original. Middle: the strength of "
      "the conditioned response over time, rising through acquisition, falling through extinction, then "
      "reappearing by itself after a rest, which shows extinction suppresses the association rather than erasing "
      "it. Bottom left: generalisation as a gradient falling away from the trained stimulus, against "
      "discrimination, which is trained by reinforcing one stimulus and not its neighbours. Bottom right: taste "
      "aversion as the exception that proves biology constrains learning, and the amygdala and cerebellum as the "
      "two separate seats of conditioning.")

# ---------------- Panel A: the four labels ----------------
d.rect(40, 150, 840, 196, BLUE, "none", rx=12, width=2)
d.text(460, 178, "Before, during, after", color=BLUE, weight="bold", size=16)

cols = [("BEFORE", [("food → salivation", NAVY), ("US → UR", RED), ("bell → nothing", GREY)]),
        ("DURING", [("bell, then food", NAVY), ("CS before US,", GREY), ("by about 0.5 s", GREY)]),
        ("AFTER", [("bell → salivation", NAVY), ("CS → CR", RED), ("usually weaker than the UR", GREY)])]
x = 70
for title, lines in cols:
    d.rect(x, 198, 256, 124, BLUE, FILL[BLUE], rx=10, width=2)
    d.text(x + 128, 224, title, color=BLUE, weight="bold", size=15)
    y = 254
    for t, col in lines:
        d.text(x + 128, y, t, color=col, weight="bold" if col is RED else "normal", size=13)
        y += 24
    x += 270
for ax in (326, 596):
    d.arrow(ax, 260, ax + 12, 260, GREY, width=2)

# ---------------- Panel B: acquisition / extinction / recovery ----------------
d.rect(40, 362, 840, 236, RED, "none", rx=12, width=2)
d.text(460, 390, "Extinction suppresses; it does not erase", color=RED, weight="bold", size=16)

m = d.axes(120, 412, 556, 120, "", "strength of the CR", (0, 30), (0, 1.1),
           ticks_x=None, ticks_y=None)


def strength(t):
    if t <= 10:
        return 1 - math.exp(-t / 3.2)
    if t <= 18:
        return (1 - math.exp(-10 / 3.2)) * math.exp(-(t - 10) / 2.4)
    if t <= 22:
        return 0.03
    return min(0.55, 0.03 + (t - 22) * 0.16) * math.exp(-(max(0, t - 24)) / 5)


d.curve(m, [(t / 10, strength(t / 10)) for t in range(0, 301)], RED, 2.8)
for x0, x1, lab, col in [(0, 10, "acquisition", SAGE), (10, 18, "extinction", NAVY),
                         (18, 22, "rest", GREY), (22, 30, "spontaneous recovery", GOLD)]:
    pa, _ = m(x0, 0)
    pb, _ = m(x1, 0)
    d.line(pa, 556, pb, 556, col, 4)
    d.text((pa + pb) / 2, 576, lab, color=col, weight="bold", size=12)

d.text(700, 440, "the CR comes back", anchor="start", color=GOLD, weight="bold", size=12)
d.text(700, 460, "on its own, weaker —", anchor="start", color=GREY, size=12)
d.text(700, 480, "so the old association", anchor="start", color=GREY, size=12)
d.text(700, 500, "was only inhibited", anchor="start", color=NAVY, weight="bold", size=12)
d.text(700, 528, "(same reason phobia", anchor="start", color=GREY, size=12)
d.text(700, 546, "relapse is common)", anchor="start", color=GREY, size=12)

# ---------------- Panel C: generalisation vs discrimination ----------------
d.rect(40, 614, 404, 216, SAGE, "none", rx=12, width=2)
d.text(242, 642, "Spread out, or narrow down", color=SAGE, weight="bold", size=15)

m2 = d.axes(110, 660, 250, 78, "similarity to the CS", "CR", (-3, 3), (0, 1.1),
            ticks_x=None, ticks_y=None)
d.curve(m2, [(x / 10, math.exp(-(x / 10) ** 2 / 1.6)) for x in range(-30, 31)], SAGE, 2.6)
px, py = m2(0, 1)
d.circle(px, py, 4, NAVY, NAVY)
d.text(px, py - 12, "the trained CS", color=NAVY, weight="bold", size=12)
d.text(242, 806, "generalisation is this gradient; discrimination is", color=GREY, size=12)
d.text(242, 824, "trained by reinforcing one point and not its neighbours", color=GREY, size=12)

# ---------------- Panel D: constraints and circuits ----------------
d.rect(466, 614, 414, 216, GOLD, "none", rx=12, width=2)
d.text(673, 642, "Biology sets the rules", color=GOLD, weight="bold", size=15)

d.rect(490, 660, 366, 66, GOLD, FILL[GOLD], rx=9, width=2)
d.text(673, 682, "taste aversion breaks every rule", color=GOLD, weight="bold", size=14)
d.text(673, 704, "one trial • hours between CS and US • hard to extinguish", color=NAVY, size=12)
d.text(673, 718, "and only for tastes — not for sounds or sights", color=NAVY, size=12)

d.rect(490, 738, 176, 72, RED, FILL[RED], rx=9, width=2)
d.text(578, 760, "amygdala", color=RED, weight="bold", size=14)
d.text(578, 782, "fear conditioning", color=NAVY, size=12)
d.text(578, 800, "(vmPFC extinguishes it)", color=GREY, size=11)
d.rect(680, 738, 176, 72, BLUE, FILL[BLUE], rx=9, width=2)
d.text(768, 760, "cerebellum", color=BLUE, weight="bold", size=14)
d.text(768, 782, "eyeblink conditioning", color=NAVY, size=12)
d.text(768, 800, "(hippocampus: context)", color=GREY, size=11)

d.save("classical-conditioning-terms-and-curves")
print("ok")
