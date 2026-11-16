import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 902,
      "Air to bone to fluid, and then to a nerve",
      "The cochlea is a frequency analyser: where it moves is which note you hear",
      "Top: the journey, and the problem the middle ear exists to solve. Sound crossing straight from air into "
      "fluid would lose about 99.9 per cent of its energy, roughly 30 decibels. The ossicles recover almost all "
      "of it by collecting force over the wide eardrum and delivering it to the much smaller oval window, with "
      "a small extra lever advantage — together about a twenty-two-fold pressure gain. Middle: the basilar "
      "membrane unrolled. It is narrow and stiff at the base and wide and floppy at the apex, so high notes "
      "peak near the oval window and low notes near the helicotrema. That map is tonotopy, and it is kept all "
      "the way to the cortex. Bottom: what a hair cell does, and why a lesion before the cochlea is a different "
      "diagnosis from one inside it."
      )

# ---------------- Panel A: the chain ----------------
d.rect(40, 166, 840, 182, BLUE, "none", rx=12, width=2)
d.text(460, 194, "Three divisions, one impedance problem", color=BLUE, weight="bold", size=16)

parts = [
    ("OUTER", "pinna · canal", "collects; the canal\nresonates at 3–4 kHz", GREY),
    ("MIDDLE", "malleus · incus · stapes", "air → fluid:\nthe gain happens here", GOLD),
    ("INNER", "cochlea", "transduction on the\nbasilar membrane", SAGE),
]
x = 66
for name, sub, note, col in parts:
    d.rect(x, 214, 170, 104, col, FILL[col], rx=10, width=2)
    d.text(x + 85, 240, name, color=col, weight="bold", size=13)
    d.text(x + 85, 262, sub, color=NAVY, weight="bold", size=11)
    n1, n2 = note.split("\n")
    d.text(x + 85, 288, n1, color=GREY, size=10)
    d.text(x + 85, 304, n2, color=GREY, size=10)
    x += 180
d.arrow(240, 266, 262, 266, GREY, width=2)
d.arrow(420, 266, 442, 266, GREY, width=2)

d.rect(616, 214, 234, 104, BLUE, FILL[BLUE], rx=10, width=2)
d.text(733, 238, "WHY IT WORKS", color=BLUE, weight="bold", size=13)
d.text(733, 260, "eardrum 55 mm² → oval window 3.2 mm²", color=NAVY, size=11)
d.text(733, 278, "≈ 17–20×, plus a 1.3× lever", color=NAVY, size=11)
d.text(733, 302, "≈ 22× pressure · about 25–30 dB back", color=GREY, weight="bold", size=11)

# ---------------- Panel B: tonotopy ----------------
d.rect(40, 364, 840, 236, GOLD, "none", rx=12, width=2)
d.text(460, 392, "The basilar membrane, unrolled", color=GOLD, weight="bold", size=16)

# wedge
d.path("M110 436 L810 418 L810 500 L110 466 z", GOLD, 2, FILL[GOLD])
d.text(110, 420, "BASE", anchor="start", color=NAVY, weight="bold", size=12)
d.text(110, 528, "oval window", anchor="start", color=GREY, size=11)
d.text(110, 544, "narrow · stiff", anchor="start", color=GREY, size=11)
d.text(810, 404, "APEX", anchor="end", color=NAVY, weight="bold", size=12)
d.text(810, 528, "helicotrema", anchor="end", color=GREY, size=11)
d.text(810, 544, "wide · floppy", anchor="end", color=GREY, size=11)

for frac, lab in [(0.04, "20 kHz"), (0.30, "4 kHz"), (0.56, "1 kHz"), (0.82, "100 Hz"), (0.96, "20 Hz")]:
    x = 110 + frac * 700
    d.line(x, 430 - frac * 10, x, 470 + frac * 24, NAVY, 1.4, dash="3,3")
    d.text(x, 506, lab, color=NAVY, weight="bold", size=11)

d.text(460, 572, "high notes at the base, low notes at the apex — and this map is preserved "
                 "right through to the auditory cortex",
       color=GREY, size=12)

# ---------------- Panel C: hair cell + hearing loss ----------------
d.rect(40, 616, 470, 256, SAGE, "none", rx=12, width=2)
d.text(275, 644, "What a hair cell does", color=SAGE, weight="bold", size=15)

steps = [
    "shear bends the stereocilia toward the tallest",
    "tip links pull open K⁺ channels",
    "K⁺ flows IN — endolymph is K⁺-rich, +80 mV",
    "depolarisation opens Ca²⁺ channels",
    "glutamate released onto the cochlear nerve",
]
y = 670
for i, t in enumerate(steps):
    d.circle(82, y + 8, 11, SAGE, FILL[SAGE], width=1.8)
    d.text(82, y + 12, str(i + 1), color=SAGE, weight="bold", size=11)
    d.text(104, y + 12, t, anchor="start", color=NAVY, size=11)
    y += 30

d.text(275, 848, "inner hair cells report · outer hair cells amplify, by changing length",
       color=GREY, weight="bold", size=11)

d.rect(530, 616, 350, 256, RED, "none", rx=12, width=2)
d.text(705, 644, "Two kinds of deafness", color=RED, weight="bold", size=15)

d.rect(556, 662, 298, 92, GOLD, FILL[GOLD], rx=9, width=2)
d.text(705, 686, "CONDUCTIVE", color=GOLD, weight="bold", size=13)
d.text(705, 708, "outer or middle ear: wax, effusion,", color=NAVY, size=11)
d.text(705, 724, "perforation, otosclerosis", color=NAVY, size=11)
d.text(705, 744, "bone conduction still works", color=GREY, weight="bold", size=11)

d.rect(556, 766, 298, 92, RED, FILL[RED], rx=9, width=2)
d.text(705, 790, "SENSORINEURAL", color=RED, weight="bold", size=13)
d.text(705, 812, "cochlea or nerve: noise, ageing,", color=NAVY, size=11)
d.text(705, 828, "aminoglycosides, acoustic neuroma", color=NAVY, size=11)
d.text(705, 848, "air AND bone both impaired", color=GREY, weight="bold", size=11)

d.save("ear-impedance-tonotopy-and-hair-cells")
print("ok")
