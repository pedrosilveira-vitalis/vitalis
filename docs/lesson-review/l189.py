import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 880,
      "Not every association is equally learnable",
      "Cognition fills in what reinforcement cannot explain; evolution decides what is easy to learn",
      "Top left: Tolman's three groups of rats plotted as errors against days. The always-rewarded group improves "
      "steadily, the never-rewarded group barely improves, and the group switched to reward on day eleven drops "
      "almost at once to the level of the rewarded group — the map had been built all along and only the reason "
      "to use it was missing. Top right: Garcia and Koelling's result, in which a compound of taste plus light "
      "and noise is followed either by illness or by shock; illness attaches to the taste and shock attaches to "
      "the light and noise, and not the other way round. Middle: the four ways taste aversion breaks the ordinary "
      "rules of conditioning, with the adaptive reason for each. Bottom: instinctive drift against extinction, "
      "and a list of which researcher goes with which phenomenon."
      )

# ---------------- Panel A: latent learning ----------------
d.rect(40, 156, 420, 288, BLUE, "none", rx=12, width=2)
d.text(250, 184, "Tolman: learning you cannot see", color=BLUE, weight="bold", size=15)

m = d.axes(110, 196, 296, 120, "days in the maze", "errors", (1, 17), (0, 10),
           ticks_x=[1, 5, 11, 17], ticks_y=None)


def rewarded(x):
    return 1.6 + 7.4 * math.exp(-(x - 1) / 3.4)


def never(x):
    return 5.6 + 3.4 * math.exp(-(x - 1) / 6.0)


def switched(x):
    if x <= 11:
        return never(x)
    return 1.7 + (never(11) - 1.7) * math.exp(-(x - 11) / 0.9)


for f, col in [(rewarded, SAGE), (never, GREY), (switched, RED)]:
    d.curve(m, [(1 + k / 10, f(1 + k / 10)) for k in range(0, 161)], col, 2.6)
px, py = m(11, switched(11))
d.line(px, py - 8, px, m(11, 0)[1], NAVY, 1.4, True)
d.text(px + 6, 222, "reward starts", anchor="start", color=NAVY, weight="bold", size=12)

for k, (col, lab) in enumerate([(SAGE, "rewarded every day"), (GREY, "never rewarded"), (RED, "reward from day 11")]):
    d.line(96, 380 + k * 22, 130, 380 + k * 22, col, 3)
    d.text(140, 385 + k * 22, lab, anchor="start", color=NAVY, size=13)

# ---------------- Panel B: Garcia and Koelling ----------------
d.rect(480, 156, 400, 288, RED, "none", rx=12, width=2)
d.text(680, 184, "Garcia: what goes with what", color=RED, weight="bold", size=15)

d.rect(510, 206, 340, 44, GREY, "#e9e4da", rx=8, width=2)
d.text(680, 234, "taste  +  light and noise  (both present)", color=NAVY, weight="bold", size=14)

d.arrow(600, 254, 570, 288, GOLD, width=2.2)
d.arrow(760, 254, 790, 288, BLUE, width=2.2)
d.rect(492, 292, 178, 62, GOLD, FILL[GOLD], rx=9, width=2)
d.text(581, 316, "then: illness", color=GOLD, weight="bold", size=14)
d.text(581, 340, "⇒ avoids the TASTE", color=NAVY, weight="bold", size=13)
d.rect(690, 292, 178, 62, BLUE, FILL[BLUE], rx=9, width=2)
d.text(779, 316, "then: shock", color=BLUE, weight="bold", size=14)
d.text(779, 340, "⇒ avoids the LIGHT", color=NAVY, weight="bold", size=13)

d.text(680, 386, "illness comes from what you ate;", color=GREY, size=13)
d.text(680, 406, "pain comes from what is around you", color=GREY, size=13)
d.text(680, 430, "equipotentiality is simply false", color=RED, weight="bold", size=14)

# ---------------- Panel C: four broken rules ----------------
d.rect(40, 460, 840, 172, GOLD, "none", rx=12, width=2)
d.text(460, 488, "Taste aversion breaks four rules of conditioning — and each break pays off",
       color=GOLD, weight="bold", size=16)

rules = [("one trial", "normally many pairings", "one bad meal is all you get"),
         ("hours of delay", "normally seconds", "poison acts slowly"),
         ("taste only", "normally everything present", "food is the likely culprit"),
         ("barely extinguishes", "normally fades", "a second test could kill you")]
x = 62
for a, b, c in rules:
    d.rect(x, 506, 196, 96, GOLD, FILL[GOLD], rx=10, width=2)
    d.text(x + 98, 532, a, color=GOLD, weight="bold", size=14)
    d.text(x + 98, 556, b, color=GREY, size=12)
    d.text(x + 98, 582, c, color=NAVY, weight="bold", size=12)
    x += 206

# ---------------- Panel D: drift vs extinction ----------------
d.rect(40, 648, 404, 200, SAGE, "none", rx=12, width=2)
d.text(242, 676, "Two different ways a trained act dies", color=SAGE, weight="bold", size=15)

d.rect(62, 696, 360, 64, RED, FILL[RED], rx=9, width=2)
d.text(242, 718, "INSTINCTIVE DRIFT", color=RED, weight="bold", size=14)
d.text(242, 742, "reward keeps coming, but the instinct wins", color=NAVY, size=12)
d.rect(62, 770, 360, 64, BLUE, FILL[BLUE], rx=9, width=2)
d.text(242, 792, "EXTINCTION", color=BLUE, weight="bold", size=14)
d.text(242, 816, "the reward stopped, so the act fades", color=NAVY, size=12)

# ---------------- Panel E: who is who ----------------
d.rect(466, 648, 414, 200, NAVY, "none", rx=12, width=2)
d.text(673, 676, "Name to phenomenon", color=NAVY, weight="bold", size=15)

names = [("Tolman", "latent learning, cognitive maps"),
         ("Köhler", "insight in chimpanzees"),
         ("Bandura", "observational learning"),
         ("Seligman", "biological preparedness"),
         ("Garcia & Koelling", "taste aversion"),
         ("Breland & Breland", "instinctive drift")]
y = 702
for who, what in names:
    d.text(672, y, who, anchor="end", color=NAVY, weight="bold", size=13)
    d.text(684, y, what, anchor="start", color=GREY, size=13)
    y += 24

d.save("cognitive-and-biological-constraints-on-learning")
print("ok")
