import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 640,
      "Two alpha positions, two enolates: speed or stability",
      "Which enolate you get is decided by the base and the temperature, not by the ketone.",
      "2-Methylcyclohexanone is drawn in the centre with its two different alpha carbons marked. On the "
      "left, LDA at minus 78 degrees removes the more accessible hydrogen on the unsubstituted side to "
      "give the kinetic enolate with the less substituted double bond. On the right, a weaker base under "
      "equilibrating conditions gives the thermodynamic enolate with the more substituted, more stable "
      "double bond. A lower band lists the pKa values that decide which base is needed.")

R = 44


def ring(cx, cy, col, mark_left, mark_right, label_o=True):
    ang = [90, 30, -30, -90, -150, 150]
    pts = [(cx + R * math.cos(math.radians(a)), cy - R * math.sin(math.radians(a))) for a in ang]
    for i in range(6):
        d.line(pts[i][0], pts[i][1], pts[(i + 1) % 6][0], pts[(i + 1) % 6][1], NAVY, 2.2)
    # carbonyl at top vertex (index 0)
    cxo, cyo = pts[0]
    d.line(cxo - 3, cyo, cxo - 3, cyo - 26, NAVY, 2.2)
    d.line(cxo + 3, cyo, cxo + 3, cyo - 26, NAVY, 2.2)
    d.text(cxo, cyo - 32, "O", color=NAVY, weight="bold", size=15)
    # methyl on index 1 (right of carbonyl)
    mx, my = pts[1]
    d.line(mx, my, mx + 30, my - 10, NAVY, 2.2)
    d.text(mx + 44, my - 8, "CH₃", color=NAVY, size=13)
    if mark_right:
        d.circle(mx, my, 13, col, FILL[col], 2.5)
        d.text(mx, my + 5, "α", color=col, weight="bold", size=14)
    if mark_left:
        lx, ly = pts[5]
        d.circle(lx, ly, 13, col, FILL[col], 2.5)
        d.text(lx, ly + 5, "α", color=col, weight="bold", size=14)


# centre
ring(450, 196, GOLD, True, True)
d.text(450, 268, "2-methylcyclohexanone", color=NAVY, weight="bold", size=16)
d.text(450, 288, "two different α carbons: one CH₂, one CH with a methyl", color=GREY, size=13)

# arrows out
d.arrow(380, 196, 258, 196, BLUE)
d.arrow(520, 196, 642, 196, RED)

# left panel
d.rect(60, 318, 370, 170, BLUE, FILL[BLUE], rx=12, width=2)
d.text(245, 344, "Kinetic enolate", color=BLUE, weight="bold", size=19)
d.text(245, 368, "LDA, −78 °C, THF", color=NAVY, weight="bold", size=15)
d.lines(245, 394,
        "Bulky and non-nucleophilic, and the deprotonation is complete and irreversible, so the "
        "proton removed fastest — on the open CH₂ side — is the one you keep.",
        chars=44, lh=19, size=14, color=NAVY)
d.text(245, 472, "→ less substituted C=C", color=BLUE, weight="bold", size=15)

# right panel
d.rect(470, 318, 370, 170, RED, FILL[RED], rx=12, width=2)
d.text(655, 344, "Thermodynamic enolate", color=RED, weight="bold", size=19)
d.text(655, 368, "NaOEt in EtOH, room temperature", color=NAVY, weight="bold", size=15)
d.lines(655, 394,
        "A weaker base deprotonates reversibly, so the two enolates equilibrate and the more "
        "substituted, more stable one wins.",
        chars=44, lh=19, size=14, color=NAVY)
d.text(655, 472, "→ more substituted C=C", color=RED, weight="bold", size=15)

# pKa band
py = 506
d.rect(60, py, 780, 118, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, py + 26, "Which base can do the job?", color=NAVY, weight="bold", size=17)
items = [("aldehyde α-H", "17"), ("ketone α-H", "20"), ("ester α-H", "25"),
         ("β-ketoester", "11"), ("EtOH", "16"), ("iPr₂NH (LDA)", "36")]
x = 118
for name, pk in items:
    d.text(x, py + 58, name, color=NAVY, size=13)
    d.text(x, py + 80, "pKₐ " + pk, color=GREY, weight="bold", size=14)
    x += 133
d.text(450, py + 104, "A base works only if its conjugate acid is the weaker acid: NaOEt (16) handles a β-ketoester (11) but not a plain ketone (20).",
       color=GREY, size=12)

d.save("kinetic-vs-thermodynamic-enolate")
