import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 660,
      "E2 needs the beta-H and the leaving group antiperiplanar",
      "A 180 degree H-C-C-LG dihedral lets the breaking C-H bond overlap with the back lobe of the C-LG bond. Nothing else works.",
      "Two Newman projections compare a 180 degree dihedral between the beta hydrogen and the leaving "
      "group, which reacts, with a 60 degree gauche arrangement, which does not. A cyclohexane chair "
      "below shows that the same requirement forces both the leaving group and the beta hydrogen onto "
      "adjacent axial positions, so an equatorial leaving group must ring-flip before E2 can occur.")


def newman(cx, cy, r, front, back, ok):
    hot = SAGE if ok else RED
    d.circle(cx, cy, r, NAVY, "#ffffff", 2.5)
    for a, lab in back:
        rad = math.radians(a)
        xe, ye = cx + r * math.cos(rad), cy - r * math.sin(rad)
        x2, y2 = cx + (r + 30) * math.cos(rad), cy - (r + 30) * math.sin(rad)
        c = hot if lab in ("H", "LG") else GREY
        d.line(xe, ye, x2, y2, c, 2.5)
        d.text(x2 + 15 * math.cos(rad), y2 - 15 * math.sin(rad) + 5, lab, color=c,
               weight=("bold" if c is hot else None), size=15)
    for a, lab in front:
        rad = math.radians(a)
        x2, y2 = cx + (r + 30) * math.cos(rad), cy - (r + 30) * math.sin(rad)
        c = hot if lab in ("H", "LG") else NAVY
        d.line(cx, cy, x2, y2, c, 2.5)
        d.text(x2 + 15 * math.cos(rad), y2 - 15 * math.sin(rad) + 5, lab, color=c,
               weight=("bold" if c is hot else None), size=15)
    d.circle(cx, cy, 4, NAVY, NAVY, 0)


# left: H front at 90, LG back at 270  ->  180 degrees apart
newman(210, 240, 46,
       [(90, "H"), (210, "R"), (330, "R")],
       [(30, "R"), (150, "R"), (270, "LG")], True)
d.text(210, 114, "180° — antiperiplanar", color=SAGE, weight="bold", size=19)
d.text(210, 360, "E2 proceeds", color=SAGE, weight="bold", size=17)
d.text(210, 382, "C–H breaks into the back lobe of C–LG", color=GREY, size=13)

# right: H front at 90, LG back at 30  ->  60 degrees apart
newman(660, 240, 46,
       [(90, "H"), (210, "R"), (330, "R")],
       [(30, "LG"), (150, "R"), (270, "R")], False)
d.text(660, 114, "60° — gauche", color=RED, weight="bold", size=19)
d.text(660, 360, "no E2 from this rotamer", color=RED, weight="bold", size=17)
d.text(660, 382, "orbitals cannot align; rotate first", color=GREY, size=13)

d.text(435, 240, "vs", color=GREY, weight="bold", size=20)

# chair consequence panel
py = 404
d.rect(60, py, 780, 206, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, py + 28, "In a cyclohexane the only 180° pairs are adjacent axial bonds",
       color=NAVY, weight="bold", size=18)

raw = [(10, 40), (50, 60), (110, 50), (150, 30), (110, 10), (50, 20)]
P = [(190 + x * 1.0, 449 + y * 1.4) for x, y in raw]
for i in range(6):
    d.line(P[i][0], P[i][1], P[(i + 1) % 6][0], P[(i + 1) % 6][1], NAVY, 2.5)

# LG axial down on the lowest carbon
d.line(P[1][0], P[1][1], P[1][0], P[1][1] + 34, SAGE, 2.5)
d.text(P[1][0], P[1][1] + 52, "LG, axial", color=SAGE, weight="bold", size=14)
# beta-H axial up on the adjacent carbon
d.line(P[0][0], P[0][1], P[0][0], P[0][1] - 34, SAGE, 2.5)
d.text(P[0][0], P[0][1] - 42, "\u03b2-H, axial", color=SAGE, weight="bold", size=14)

d.lines(646, py + 68,
        "Adjacent axial bonds point in opposite directions, so they are the only 180° pair on the ring. "
        "An equatorial leaving group must ring-flip to axial first, and if the flipped chair offers no "
        "adjacent axial β-H, E2 is shut down altogether.",
        chars=40, lh=21, size=15, color=NAVY, anchor="middle")

d.save("e2-antiperiplanar")
