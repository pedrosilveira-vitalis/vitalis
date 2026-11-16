import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 898,
      "Attention decides, the senses vote, experience tunes",
      "Three filters sit between the world and the percept",
      "Top: where attention does its selecting. Broadbent put the gate early, before meaning; Treisman turned "
      "the gate into a dimmer, which is how your own name still gets through from the ignored ear; Deutsch "
      "and Deutsch put it late, after everything has been understood. Lavie's load theory settles the "
      "argument by making the gate's position depend on how hard the attended task is. Middle: the McGurk "
      "effect, in the right order — the ears get ba, the eyes get ga, and what reaches awareness is da, a "
      "syllable nobody presented. Knowing about it does not switch it off, which is the point: integration "
      "happens before consciousness. Bottom: the rules that govern when two senses combine at all, and the "
      "windows in development when experience prunes perception to fit the world the infant actually lives in."
      )

# ---------------- Panel A: models of selection ----------------
d.rect(40, 168, 840, 206, BLUE, "none", rx=12, width=2)
d.text(460, 196, "Where is the bottleneck?", color=BLUE, weight="bold", size=16)

models = [
    ("BROADBENT", "a hard filter, EARLY", "selects on physical features;\nmeaning never extracted", GREY),
    ("TREISMAN", "a dimmer, not a gate", "unattended is attenuated;\nyour name still breaks through", SAGE),
    ("DEUTSCH × 2", "selection is LATE", "everything is understood;\nattention picks what reaches awareness", GOLD),
    ("LAVIE", "it depends on load", "hard task → early selection;\neasy task → late", BLUE),
]
x = 62
for name, sub, note, col in models:
    d.rect(x, 216, 198, 134, col, FILL[col], rx=10, width=2)
    d.text(x + 99, 242, name, color=col, weight="bold", size=13)
    d.text(x + 99, 264, sub, color=NAVY, weight="bold", size=11)
    n1, n2 = note.split("\n")
    d.text(x + 99, 296, n1, color=GREY, size=11)
    d.text(x + 99, 314, n2, color=GREY, size=11)
    x += 204
d.text(460, 364, "no attention, no conscious percept — the invisible gorilla and change blindness make "
                 "the same point",
       color=NAVY, weight="bold", size=12)

# ---------------- Panel B: McGurk ----------------
d.rect(40, 390, 840, 196, RED, "none", rx=12, width=2)
d.text(460, 418, "The McGurk effect, in the right order", color=RED, weight="bold", size=16)

d.rect(90, 440, 210, 96, SAGE, FILL[SAGE], rx=10, width=2)
d.text(195, 466, "EARS HEAR", color=SAGE, weight="bold", size=12)
d.text(195, 500, "“ba”", color=NAVY, weight="bold", size=24)

d.rect(340, 440, 210, 96, BLUE, FILL[BLUE], rx=10, width=2)
d.text(445, 466, "EYES SEE THE LIPS SAY", color=BLUE, weight="bold", size=12)
d.text(445, 500, "“ga”", color=NAVY, weight="bold", size=24)

d.rect(620, 440, 210, 96, RED, FILL[RED], rx=10, width=2)
d.text(725, 466, "WHAT YOU PERCEIVE", color=RED, weight="bold", size=12)
d.text(725, 500, "“da”", color=NAVY, weight="bold", size=24)

d.arrow(306, 488, 332, 488, GREY, width=2)
d.arrow(558, 488, 612, 488, GREY, width=2)
d.text(460, 562, "neither input, and it does not go away once you know — integration finishes before "
                 "awareness begins",
       color=GREY, size=12)

# ---------------- Panel C: rules + development ----------------
d.rect(40, 602, 420, 266, GOLD, "none", rx=12, width=2)
d.text(250, 630, "When do two senses combine?", color=GOLD, weight="bold", size=15)

rules = [
    ("same place", "spatial correspondence"),
    ("same time", "within about ±200 ms for speech"),
    ("both weak", "inverse effectiveness: the boost is biggest"),
    ("weight by reliability", "vision wins for space, ears for time"),
]
y = 656
for a, b in rules:
    d.rect(66, y, 368, 42, GOLD, FILL[GOLD], rx=8, width=1.8)
    d.text(250, y + 18, a, color=GOLD, weight="bold", size=12)
    d.text(250, y + 34, b, color=GREY, size=11)
    y += 48

d.text(250, 858, "lose one sense early and its cortex is recruited by the others",
       color=NAVY, size=11)

d.rect(480, 602, 400, 266, SAGE, "none", rx=12, width=2)
d.text(680, 630, "Experience prunes perception", color=SAGE, weight="bold", size=15)

dev = [
    ("newborn acuity", "about 20/400 → adult by 6–12 months"),
    ("stereopsis", "appears at 3–5 months"),
    ("visual cliff", "depth before the fear of heights"),
    ("phonemes", "all contrasts at 6 months, native only by 12"),
    ("faces", "other-race effect by about 9 months"),
    ("ageing", "presbycusis from above 4 kHz; wider binding window"),
]
y = 658
for a, b in dev:
    d.text(500, y, a, anchor="start", color=SAGE, weight="bold", size=12)
    d.text(500, y + 16, b, anchor="start", color=GREY, size=11)
    y += 34

d.save("attention-models-mcgurk-and-perceptual-narrowing")
print("ok")
