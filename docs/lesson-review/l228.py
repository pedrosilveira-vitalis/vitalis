import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 946,
      "Kelley's three dials, and what each setting means",
      "Read the vignette for all three before deciding — one dial alone decides nothing",
      "Top: the three dimensions set out as switches, with the question each one answers and what a HIGH or a "
      "LOW reading contributes. The commonest mistake is misreading distinctiveness: a person who misbehaves "
      "only in one specific setting is HIGH on distinctiveness, which argues for the setting rather than the "
      "person. Middle: the three standard combinations and the attribution each produces. Bottom left: the two "
      "principles for the far more common case of a single observation, where the dials cannot be read at all. "
      "Bottom right: Weiner's three dimensions, which pick up where the attribution leaves off and say what the "
      "person will feel and whether they will try again."
      )

# ---------------- Panel A: the dials ----------------
d.rect(40, 180, 840, 232, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Three dials, three questions", color=NAVY, weight="bold", size=15)

dials = [("CONSENSUS", "do OTHER people do it too?",
          "HIGH — everyone does", "LOW — only this person", BLUE),
         ("DISTINCTIVENESS", "do they do it ONLY here?",
          "HIGH — only this one target", "LOW — they do it everywhere", GOLD),
         ("CONSISTENCY", "do they do it EVERY time?",
          "HIGH — always, over time", "LOW — it varies", SAGE)]
cx = 68
for name, q, hi, lo, col in dials:
    d.rect(cx, 228, 262, 164, col, FILL[col], rx=10, width=2)
    d.text(cx + 131, 254, name, color=col, weight="bold", size=13)
    d.text(cx + 131, 274, q, color=NAVY, weight="bold", size=10)
    d.line(cx + 40, 288, cx + 222, 288, col, 1, dash="3,3")
    d.text(cx + 131, 310, hi, color=NAVY, size=10)
    d.text(cx + 131, 334, lo, color=NAVY, size=10)
    d.text(cx + 131, 368, "watch this one — “only on Mondays”" if name == "DISTINCTIVENESS"
           else "", color=col, weight="bold", size=9)
    d.text(cx + 131, 382, "is HIGH, not low" if name == "DISTINCTIVENESS" else "",
           color=col, weight="bold", size=9)
    cx += 276

# ---------------- Panel B: the three combinations ----------------
d.rect(40, 428, 840, 182, RED, "none", rx=12, width=2)
d.text(460, 456, "The three combinations worth memorising", color=RED, weight="bold", size=15)

combos = [("LOW · LOW · HIGH", "only they do it, they do it everywhere,\nand they always do it",
           "→ THE PERSON", RED),
          ("HIGH · HIGH · HIGH", "everyone does it, only to this target,\nand always",
           "→ THE STIMULUS", SAGE),
          ("LOW · HIGH · LOW", "nobody else does it, only here,\nand not reliably",
           "→ THE CIRCUMSTANCE", GOLD)]
cx = 68
for combo, gloss, out, col in combos:
    d.rect(cx, 474, 262, 120, col, FILL[col], rx=10, width=2)
    d.text(cx + 131, 498, combo, color=col, weight="bold", size=12.5)
    for j, ln in enumerate(gloss.split("\n")):
        d.text(cx + 131, 518 + j * 14, ln, color=GREY, size=9)
    d.text(cx + 131, 570, out, color=NAVY, weight="bold", size=12)
    cx += 276

# ---------------- Panel C: single observation ----------------
d.rect(40, 626, 410, 304, BLUE, "none", rx=12, width=2)
d.text(245, 654, "When you only see it once", color=BLUE, weight="bold", size=15)
d.text(245, 674, "the dials need repeated observations; usually you have one", color=GREY, size=9.5)

d.rect(64, 692, 362, 108, GOLD, FILL[GOLD], rx=9, width=2)
d.text(245, 716, "DISCOUNTING", color=GOLD, weight="bold", size=13)
d.text(245, 736, "another plausible cause is present", color=NAVY, size=10)
d.text(245, 758, "→ trust the dispositional reading LESS", color=GOLD, weight="bold", size=10.5)
d.text(245, 778, "the salesman is enthusiastic — and paid to be", color=GREY, size=9.5)

d.rect(64, 812, 362, 108, SAGE, FILL[SAGE], rx=9, width=2)
d.text(245, 836, "AUGMENTATION", color=SAGE, weight="bold", size=13)
d.text(245, 856, "the behaviour happened DESPITE a cost", color=NAVY, size=10)
d.text(245, 878, "→ trust the dispositional reading MORE", color=SAGE, weight="bold", size=10.5)
d.text(245, 898, "the researcher publishes against their own interest", color=GREY, size=9.5)

# ---------------- Panel D: Weiner ----------------
d.rect(470, 626, 410, 304, SAGE, "none", rx=12, width=2)
d.text(675, 654, "Weiner: what follows from it", color=SAGE, weight="bold", size=15)

wrows = [("ABILITY", "internal · stable · uncontrollable", "shame; stop trying", RED),
         ("EFFORT", "internal · unstable · CONTROLLABLE", "guilt; try again", SAGE),
         ("TASK DIFFICULTY", "external · stable · uncontrollable", "resignation", GOLD),
         ("LUCK", "external · unstable · uncontrollable", "surprise; no lesson", BLUE)]
y = 676
for name, dims, out, col in wrows:
    d.rect(494, y, 362, 48, col, FILL[col], rx=8, width=1.6)
    d.text(560, y + 19, name, color=col, weight="bold", size=10.5)
    d.text(790, y + 19, out, anchor="end", color=NAVY, weight="bold", size=9.5)
    d.text(675, y + 37, dims, color=GREY, size=9)
    y += 56

d.text(675, 912, "blame a failure on effort and motivation survives; blame it on ability and it does not",
       color=NAVY, weight="bold", size=9.5)

d.save("kelley-dials-discounting-and-weiner-dimensions")
print("ok")
