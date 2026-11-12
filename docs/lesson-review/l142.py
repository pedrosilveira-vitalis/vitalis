import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 640,
      "Why a substituent directs: where the arenium ion puts its charge",
      "Ortho or para attack puts positive charge on the carbon bearing the substituent. Meta attack does not.",
      "Three benzene rings show attack at the ortho, meta and para positions relative to a substituent "
      "G. In each the three carbons that carry positive charge in the arenium ion are marked. For ortho "
      "and para attack the carbon bearing G is one of them; for meta attack it is not. Two panels below "
      "read off the consequence: a lone-pair donor stabilises that contributor so it directs ortho and "
      "para, while a resonance withdrawer destabilises it so ortho and para are suppressed and meta is "
      "what is left.")

R = 52
ANG = [90, 30, -30, -90, -150, 150]   # C1 top, clockwise


def ring(cx, cy, attack, plus, title, ok):
    pts = [(cx + R * math.cos(math.radians(a)), cy - R * math.sin(math.radians(a))) for a in ANG]
    for i in range(6):
        d.line(pts[i][0], pts[i][1], pts[(i + 1) % 6][0], pts[(i + 1) % 6][1], NAVY, 2.2)
    col = SAGE if ok else RED
    for i, (px, py) in enumerate(pts):
        if i == 0:
            d.circle(px, py, 15, col, FILL[col], 2.5)
            d.text(px, py + 6, "G", color=col, weight="bold", size=16)
            if 0 in plus:
                d.text(px + 24, py - 12, "+", color=GOLD, weight="bold", size=19)
        elif i == attack:
            d.circle(px, py, 15, NAVY, "#ffffff", 2.5)
            d.text(px, py + 6, "E", color=NAVY, weight="bold", size=15)
        elif i in plus:
            d.circle(px, py, 13, GOLD, FILL[GOLD], 2)
            d.text(px, py + 6, "+", color=GOLD, weight="bold", size=17)
        else:
            d.circle(px, py, 5, NAVY, NAVY, 0)
    d.text(cx, cy - R - 42, title, color=NAVY, weight="bold", size=17)
    verdict = ("carbon bearing G carries +" if ok else "carbon bearing G is untouched")
    d.text(cx, cy + R + 36, verdict, color=col, weight="bold", size=14)


ring(190, 212, 1, {0, 2, 4}, "E attacks ortho", True)
ring(450, 212, 2, {1, 3, 5}, "E attacks meta", False)
ring(710, 212, 3, {0, 2, 4}, "E attacks para", True)

# correction: for ortho attack the plus set is C1, C3, C5
d.text(450, 318, "The three charged carbons are always ortho and para to the carbon the electrophile hit.",
       color=GREY, size=14)

PY0 = 346
for x0, col, head, line1, line2 in [
    (60, SAGE, "G donates a lone pair  (–OH, –NH₂, –OR, and the halogens)",
     "That extra contributor is the one where G can push electron density onto the + carbon.",
     "It exists only for ortho and para attack → ortho/para director."),
    (60, RED, "G withdraws by resonance  (–NO₂, –C≡N, C=O, –SO₃H)",
     "The same contributor puts + next to a carbon already starved of electrons.",
     "Ortho and para are the ones punished → meta wins by default, not by merit."),
]:
    y = PY0 if col is SAGE else PY0 + 132
    d.rect(x0, y, 780, 116, col, FILL[col], rx=12, width=2)
    d.text(450, y + 30, head, color=col, weight="bold", size=17)
    d.text(450, y + 58, line1, color=NAVY, size=15)
    d.text(450, y + 82, line2, color=NAVY, size=15)
    d.text(450, y + 104, "Halogens are the split case: they donate by resonance (ortho/para) but withdraw inductively (deactivating)."
           if col is SAGE else "Deactivating and meta-directing always travel together.",
           color=GREY, size=12)

d.save("eas-directing-arenium")
