import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 640,
      "Reading an IR spectrum: five places to look, in order",
      "Wavenumber runs high to low, left to right, the way a spectrum is printed. Everything below 1500 is the fingerprint region.",
      "An infrared wavenumber axis from 4000 down to 400 inverse centimetres, divided into labelled "
      "bands: O-H and N-H stretches from 3200 to 3600, the carboxylic acid O-H smear from 2500 to 3300, "
      "C-H stretches around 3000 with sp3 below and sp2 above, the triple-bond window from 2100 to 2260 "
      "for alkynes and nitriles, the carbonyl window from 1650 to 1850, and the fingerprint region below "
      "1500. A second strip orders the carbonyl types inside that window, from acid chloride highest to "
      "amide lowest.")

X0, X1 = 70, 846
HI, LO = 4000.0, 400.0


def px(v):
    return X0 + (X1 - X0) * (HI - v) / (HI - LO)


AX = 300
d.line(X0, AX, X1, AX, NAVY, 2.5)
for v in [4000, 3500, 3000, 2500, 2000, 1500, 1000, 400]:
    d.line(px(v), AX - 6, px(v), AX + 6, NAVY, 1.5)
    d.text(px(v), AX + 24, str(v), color=GREY, size=12)


bands = [
    (3200, 3600, "O–H  /  N–H", "alcohol broad; amine sharper", BLUE, 1, 0),
    (2500, 3300, "COOH O–H", "very broad, smeared across C–H", RED, 1, 96),
    (2850, 3100, "C–H", "sp³ below 3000, sp² above", SAGE, -1, 0),
    (2100, 2260, "C≡C  /  C≡N", "sharp; nitrile stronger", GOLD, 1, 0),
    (1650, 1850, "C=O", "the single most useful band", RED, -1, 0),
    (400, 1500, "fingerprint", "C–O at 1000–1300; aromatic C=C 1450–1600", GREY, -1, 0),
]

for lo, hi, name, note, col, side, lift in bands:
    x1, x2 = px(hi), px(lo)
    y = AX - 26 - lift if side > 0 else AX + 74
    d.rect(x1, y - 20, x2 - x1, 40, col, FILL[col], rx=6, width=2)
    d.text((x1 + x2) / 2, y + 1, name, color=col, weight="bold", size=15)
    ny = y - 30 if side > 0 else y + 36
    d.lines((x1 + x2) / 2, ny, note, chars=30, lh=15, size=12, color=GREY)

# carbonyl zoom strip
zy = 436
d.rect(60, zy, 780, 186, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, zy + 28, "Inside the carbonyl window: the more the substituent donates, the lower the band",
       color=NAVY, weight="bold", size=17)

rows = [("acid chloride", "1800–1850", RED), ("anhydride", "1800–1850 + 1750", RED),
        ("ester", "1735–1750", GOLD), ("aldehyde", "1720–1740", GOLD),
        ("ketone", "1705–1725", BLUE), ("carboxylic acid", "1700–1725", BLUE),
        ("amide", "1630–1690", SAGE)]
x = 112
for name, rng, col in rows:
    d.text(x, zy + 70, name, color=col, weight="bold", size=13)
    d.text(x, zy + 92, rng, color=GREY, size=12)
    x += 110
d.arrow(100, zy + 112, 806, zy + 112, NAVY, width=2)
d.text(450, zy + 136, "Conjugation lowers the band another 20–40 cm⁻¹; a strained ring raises it.",
       color=GREY, size=13)
d.text(450, zy + 162, "Mass spec partners: m/z 77 phenyl · 91 tropylium · 105 benzoyl · 43 acetyl · M:M+2 of 3:1 means Cl, 1:1 means Br",
       color=NAVY, size=13)

d.save("ir-band-map")
