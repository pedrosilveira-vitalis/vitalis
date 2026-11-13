import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 800,
      "Classify the collision first, then write only the laws that apply",
      "Momentum is conserved in every one; kinetic energy only when the problem says elastic",
      "Left: before-and-after pictures of three collisions — an elastic collision between equal masses where the "
      "moving ball stops and the struck ball leaves with the same speed, a perfectly inelastic collision where the "
      "two stick together, and an explosion where a resting object splits and the fragments carry equal and opposite "
      "momenta. Right: a decision tree asking whether the objects stick and whether kinetic energy is conserved, "
      "giving the equations available in each case. Bottom: the kinetic energy lost in a perfectly inelastic "
      "collision, the coefficient of restitution scale, and the neutron moderation case.")

# ---------------- Panel A: before / after ----------------
d.rect(40, 112, 430, 400, SAGE, "none", rx=12, width=2)
d.text(255, 142, "Before  →  after", color=SAGE, weight="bold", size=17)
for _y in (196, 300, 404):
    d.line(255, _y - 30, 255, _y + 30, GREY, 1, True)


def ball(x, y, r, col, label=None):
    d.circle(x, y, r, col, FILL[col], width=2)
    if label:
        d.text(x, y + 5, label, color=col, weight="bold", size=13)


def strip(y, title, note, col):
    d.text(255, y - 18, title, color=col, weight="bold", size=15)
    d.text(255, y + 66, note, color=GREY, size=13)


# elastic, equal masses
strip(196, "elastic, equal masses", "the moving one stops dead; speeds swap", BLUE)
ball(96, 216, 17, BLUE, "m")
d.arrow(118, 216, 162, 216, BLUE)
ball(196, 216, 17, GREY, "m")
ball(300, 216, 17, BLUE, "m")
ball(396, 216, 17, GREY, "m")
d.arrow(418, 216, 462, 216, SAGE)
d.text(140, 200, "v", color=BLUE, weight="bold", size=14)
d.text(440, 200, "v", color=SAGE, weight="bold", size=14)

# perfectly inelastic
strip(300, "perfectly inelastic", "one unknown: vᶠ = (m₁v₁ + m₂v₂) / (m₁ + m₂)", RED)
ball(96, 320, 17, RED, "m₁")
d.arrow(118, 320, 160, 320, RED)
ball(196, 320, 21, GREY, "m₂")
d.circle(340, 320, 24, RED, FILL[RED], width=2)
d.text(340, 326, "m₁+m₂", color=RED, weight="bold", size=12)
d.arrow(366, 320, 400, 320, RED)
d.text(383, 304, "vᶠ", color=RED, weight="bold", size=14)

# explosion
strip(404, "explosion from rest", "Σp stays zero; kinetic energy rises", GOLD)
d.circle(150, 424, 24, GOLD, FILL[GOLD], width=2)
d.text(150, 430, "at rest", color=GOLD, weight="bold", size=12)
ball(310, 424, 15, GOLD, "m")
d.arrow(290, 424, 248, 424, GOLD)
ball(410, 424, 21, GOLD, "M")
d.arrow(434, 424, 462, 424, GOLD)
d.text(268, 408, "fast", color=GOLD, weight="bold", size=13)
d.text(448, 408, "slow", color=GOLD, weight="bold", size=13)

# ---------------- Panel B: decision tree ----------------
d.rect(486, 112, 394, 400, BLUE, "none", rx=12, width=2)
d.text(683, 142, "Which equations do you get?", color=BLUE, weight="bold", size=17)

d.rect(566, 162, 234, 44, NAVY, FILL[NAVY], rx=9, width=2)
d.text(683, 190, "Do they stick together?", color=NAVY, weight="bold", size=16)
d.arrow(620, 206, 578, 238, NAVY, label="yes", lx=-18, ly=-2)
d.arrow(746, 206, 786, 238, NAVY, label="no", lx=16, ly=-2)

d.rect(500, 242, 150, 94, RED, FILL[RED], rx=9, width=2)
d.text(575, 268, "perfectly", color=RED, weight="bold", size=15)
d.text(575, 288, "inelastic", color=RED, weight="bold", size=15)
d.text(575, 314, "1 equation,", color=NAVY, size=14)
d.text(575, 332, "1 unknown", color=NAVY, size=14)

d.rect(680, 242, 180, 44, NAVY, FILL[NAVY], rx=9, width=2)
d.text(770, 270, "Is KE conserved?", color=NAVY, weight="bold", size=14)
d.arrow(726, 286, 706, 320, NAVY, label="yes", lx=-18, ly=0)
d.arrow(818, 286, 834, 320, NAVY, label="no", lx=14, ly=0)

d.rect(654, 324, 116, 90, SAGE, FILL[SAGE], rx=9, width=2)
d.text(712, 350, "elastic", color=SAGE, weight="bold", size=15)
d.text(712, 374, "p and KE:", color=NAVY, size=13)
d.text(712, 396, "2 equations", color=NAVY, size=13)

d.rect(784, 324, 94, 90, GOLD, FILL[GOLD], rx=9, width=2)
d.text(831, 350, "inelastic", color=GOLD, weight="bold", size=14)
d.text(831, 374, "p only:", color=NAVY, size=13)
d.text(831, 394, "need more", color=NAVY, size=13)

d.rect(506, 430, 354, 60, BLUE, FILL[BLUE], rx=9, width=2)
d.text(683, 454, "Elastic with the target at rest:", color=BLUE, weight="bold", size=14)
d.text(683, 478, "v₁ᶠ = (m₁−m₂)/(m₁+m₂) · v₁   •   v₂ᶠ = 2m₁/(m₁+m₂) · v₁",
       color=NAVY, weight="bold", size=14)

# ---------------- Bottom ----------------
d.rect(40, 542, 412, 112, RED, FILL[RED], rx=10, width=2)
d.text(246, 570, "How much KE is lost when they stick", color=RED, weight="bold", size=16)
d.text(246, 600, "KE_lost = ½m₁v₁² · m₂/(m₁ + m₂)", color=NAVY, weight="bold", size=16)
d.text(246, 630, "tiny m₁ into huge m₂: almost all of it goes", color=GREY, size=14)

d.rect(468, 542, 412, 112, SAGE, FILL[SAGE], rx=10, width=2)
d.text(674, 570, "Equal masses transfer the most", color=SAGE, weight="bold", size=16)
d.text(674, 600, "a neutron stops dead on hydrogen (A = 1)", color=NAVY, weight="bold", size=15)
d.text(674, 630, "and bounces off lead with its energy intact", color=GREY, size=14)

d.text(460, 692, "e = separation speed / approach speed:  1 elastic  •  0 perfectly inelastic",
       color=NAVY, weight="bold", size=16)
d.text(460, 724, "Same momentum, different energy: 4 kg at 3 m/s and 1 kg at 12 m/s both carry 12 kg·m/s,",
       color=GREY, size=15)
d.text(460, 750, "but 18 J and 72 J — momentum and kinetic energy are not interchangeable",
       color=GREY, size=15)
d.text(460, 780, "Ballistic pendulum: momentum for the collision, energy for the swing — never one across both",
       color=GREY, size=15)

d.save("collision-types-and-decision-tree")
print("ok")
