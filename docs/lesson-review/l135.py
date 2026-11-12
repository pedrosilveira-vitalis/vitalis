import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 720,
      "Boiling point at matched molecular weight (all MW 58-60)",
      "Hold molecular weight fixed and the order falls out of hydrogen bonding, not of polarity alone.",
      "A horizontal bar chart of normal boiling points for nine compounds of molecular weight 58 to 60, "
      "from acetamide at 221 degrees Celsius down to butane at minus 0.5. A right-hand column states, "
      "for each, whether the molecule can donate and accept hydrogen bonds, only accept them, or "
      "neither.")

rows = [
    ("Acetamide (amide)",        221.0, "donates + accepts (2 N-H)", RED),
    ("Acetic acid (carb. acid)", 118.0, "donates + accepts, dimerises", RED),
    ("1-Propanol (alcohol)",      97.0, "donates + accepts (O-H)", RED),
    ("Acetone (ketone)",          56.0, "accepts only", BLUE),
    ("Propanal (aldehyde)",       48.0, "accepts only", BLUE),
    ("Propylamine (1° amine)",    48.0, "donates + accepts (weak N-H)", RED),
    ("Methyl formate (ester)",    32.0, "accepts only", BLUE),
    ("Methoxyethane (ether)",      7.4, "accepts only", BLUE),
    ("Butane (alkane)",           -0.5, "neither", GREY),
]

X0, XW = 268, 352          # bar origin and full width
LO, HI = -10.0, 230.0
y = 108
BH = 32
GAP = 44


def bx(v):
    return X0 + XW * (v - LO) / (HI - LO)


# zero gridline
d.line(bx(0), 96, bx(0), 96 + GAP * len(rows) - 6, GREY, 1, dash=True)
d.text(bx(0), 90, "0 °C", color=GREY, size=13)

for label, bp, hb, col in rows:
    cy = y + BH / 2
    d.text(258, cy + 5, label, anchor="end", color=NAVY, size=16)
    w = max(bx(bp) - bx(0), 3)
    d.rect(bx(0) if bp >= 0 else bx(bp), y, w, BH, col, FILL[col], rx=5, width=2)
    d.text(bx(bp) + 10, cy + 5, (("%.1f" % bp).rstrip("0").rstrip(".")) + "°C",
           anchor="start", color=col, weight="bold", size=15)
    d.text(700, cy + 5, hb, anchor="start", color=GREY, size=13)
    y += GAP

d.text(700, 92, "hydrogen bonding", anchor="start", color=NAVY, weight="bold", size=14)

d.rect(60, 536, 780, 76, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, 560, "Order at matched molecular weight", color=NAVY, weight="bold", size=18)
d.text(450, 586, "amide > carboxylic acid > alcohol > aldehyde/ketone ≈ 1°/2° amine > ester > ether ≈ alkane",
       color=NAVY, size=16)
d.text(450, 604, "Two N-H donors plus a strongly polarised C=O put amides at the top, above the acid dimer.",
       color=GREY, size=13)

d.legend(60, 640, [(RED, "Red: donates and accepts hydrogen bonds", False),
                   (BLUE, "Blue: accepts only", False),
                   (GREY, "Grey: neither", False)])

d.save("boiling-point-ladder")
