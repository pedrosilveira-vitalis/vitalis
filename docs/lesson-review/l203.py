import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 906,
      "Where the lesion is, and what the patient loses",
      "Field defects are read backwards: the pattern names the site",
      "The visual pathway, drawn from above, with the five lesion sites the exam uses and the field defect "
      "each one produces. Before the chiasm a lesion takes one eye. At the chiasm it takes the crossing nasal "
      "fibres, which carry the two outer fields, so both temporal fields go — bitemporal hemianopia, "
      "classically from a pituitary adenoma pressing up on the chiasm from below. Behind the chiasm every "
      "lesion is homonymous and contralateral, because from there on each side carries the opposite half of "
      "the world. Meyer's loop swings through the temporal lobe carrying the lower radiation, so a temporal "
      "lesion costs the upper quadrant; the parietal radiation costs the lower one. At the occipital pole the "
      "macula is often spared, since it sits on a watershed between two arterial supplies."
      )

# ---------------- the pathway ----------------
d.rect(40, 164, 840, 420, BLUE, "none", rx=12, width=2)
d.text(460, 192, "The pathway from above, left eye on the left", color=BLUE, weight="bold", size=16)

# eyes
for cx, lab in [(150, "LEFT eye"), (150, None)]:
    pass
d.circle(150, 268, 34, GREY, "#efe9df", width=2.4)
d.text(150, 218, "LEFT eye", color=GREY, weight="bold", size=12)
d.circle(150, 420, 34, GREY, "#efe9df", width=2.4)
d.text(150, 476, "RIGHT eye", color=GREY, weight="bold", size=12)

# nerves to chiasm
d.line(184, 268, 300, 320, SAGE, 2.6)
d.line(184, 268, 300, 368, RED, 2.6)
d.line(184, 420, 300, 368, SAGE, 2.6)
d.line(184, 420, 300, 320, RED, 2.6)

d.circle(318, 344, 22, NAVY, FILL[NAVY] if NAVY in FILL else "#dde4ea", width=2)
d.text(318, 349, "X", color=NAVY, weight="bold", size=14)
d.text(318, 392, "chiasm", color=NAVY, weight="bold", size=12)

# tracts
d.line(340, 326, 470, 300, BLUE, 2.8)
d.line(340, 362, 470, 390, BLUE, 2.8)
d.text(404, 286, "tract", color=BLUE, weight="bold", size=11)

# LGN
d.rect(470, 278, 92, 44, GOLD, FILL[GOLD], rx=8, width=2)
d.text(516, 306, "LGN", color=GOLD, weight="bold", size=13)
d.rect(470, 368, 92, 44, GOLD, FILL[GOLD], rx=8, width=2)
d.text(516, 396, "LGN", color=GOLD, weight="bold", size=13)

# radiations
d.path("M562 292 q70 -40 130 -8", SAGE, 2.6, "none")
d.text(636, 262, "parietal radiation", color=SAGE, weight="bold", size=11)
d.path("M562 404 q70 44 130 10", RED, 2.6, "none")
d.text(628, 470, "Meyer's loop (temporal)", color=RED, weight="bold", size=11)

# V1
d.rect(692, 300, 104, 100, NAVY, "#dde4ea", rx=10, width=2)
d.text(744, 344, "V1", color=NAVY, weight="bold", size=16)
d.text(744, 366, "occipital", color=GREY, size=11)
d.text(744, 420, "macula at the pole", color=GREY, size=11)

# lesion markers
marks = [(214, 292, "1"), (318, 344, "2"), (452, 300, "3"), (676, 428, "4"), (744, 288, "5")]
for x, y, n in marks:
    d.circle(x, y, 13, RED, "#ffffff", width=2.4)
    d.text(x, y + 5, n, color=RED, weight="bold", size=12)

d.text(460, 540, "crossing fibres are nasal · nasal retina sees the TEMPORAL field · so the chiasm "
                 "lesion costs both outer fields",
       color=NAVY, weight="bold", size=12)
d.text(460, 562, "everything behind the chiasm is homonymous and on the opposite side",
       color=GREY, size=12)

# ---------------- the table ----------------
d.rect(40, 600, 840, 282, RED, "none", rx=12, width=2)
d.text(460, 628, "The five defects", color=RED, weight="bold", size=16)

rows = [
    ("1", "optic nerve", "monocular blindness — that eye only", "optic neuritis in MS", GREY),
    ("2", "optic chiasm", "bitemporal hemianopia — both outer fields", "pituitary adenoma", GOLD),
    ("3", "optic tract or LGN", "contralateral homonymous hemianopia", "same half lost in both eyes", BLUE),
    ("4", "Meyer's loop, temporal", "contralateral superior quadrantanopia", "\"pie in the sky\"", RED),
    ("5", "occipital cortex", "homonymous hemianopia, macula spared", "PCA stroke", SAGE),
]
y = 646
for n, site, defect, note, col in rows:
    d.circle(92, y + 18, 13, col, FILL[col], width=2)
    d.text(92, y + 23, n, color=col, weight="bold", size=12)
    d.text(122, y + 14, site, anchor="start", color=col, weight="bold", size=12)
    d.text(122, y + 30, note, anchor="start", color=GREY, size=11)
    d.text(420, y + 22, defect, anchor="start", color=NAVY, weight="bold", size=12)
    y += 42

d.text(460, 872, "tunnel vision is something else entirely — a concentric loss from glaucoma or "
                 "retinitis pigmentosa, not a chiasmal lesion",
       color=RED, weight="bold", size=11)

d.save("visual-pathway-and-field-defects")
print("ok")
