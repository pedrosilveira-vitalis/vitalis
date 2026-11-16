import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 910,
      "Every sense does the same four things",
      "Different front ends, one common path: open or close a channel, grade a potential, code a rate",
      "Top: the universal chain. Whatever the stimulus, it ends up changing the permeability of a membrane; "
      "the resulting receptor potential is graded and local, and only the action potentials it triggers are "
      "all-or-none. Intensity is carried by how often those spikes come, not by how big they are. Middle: the "
      "front end differs by modality — directly gated channels for touch and hearing, a G protein cascade "
      "for vision and smell, mixed mechanisms for taste, TRP channels for temperature and pain. The one that "
      "catches people out is vision, where light closes channels and the cell hyperpolarises. Bottom: "
      "adaptation, and the receptors that refuse to do it.")

# ---------------- Panel A: the common chain ----------------
d.rect(40, 170, 840, 136, BLUE, "none", rx=12, width=2)
d.text(460, 198, "The chain every modality shares", color=BLUE, weight="bold", size=16)

steps = [("stimulus", GREY), ("channel opens\nor closes", SAGE),
         ("RECEPTOR POTENTIAL\ngraded · local", BLUE),
         ("ACTION POTENTIALS\nall-or-none", RED),
         ("rate codes\nintensity", GOLD)]
x = 62
for name, col in steps:
    d.rect(x, 218, 148, 62, col, FILL[col], rx=9, width=2)
    parts = name.split("\n")
    if len(parts) == 1:
        d.text(x + 74, 255, parts[0], color=col, weight="bold", size=12)
    else:
        d.text(x + 74, 245, parts[0], color=col, weight="bold", size=11)
        d.text(x + 74, 263, parts[1], color=GREY, size=11)
    if x < 650:
        d.arrow(x + 148, 249, x + 168, 249, GREY, width=1.8)
    x += 168

# ---------------- Panel B: front ends ----------------
d.rect(40, 322, 840, 300, SAGE, "none", rx=12, width=2)
d.text(460, 350, "Five front ends", color=SAGE, weight="bold", size=16)

rows = [
    ("TOUCH", "mechanically gated channels (PIEZO)", "deformation → Na⁺ and Ca²⁺ in → depolarise", SAGE),
    ("HEARING", "tip links pull open MET channels", "endolymph is K⁺-rich, so K⁺ flows IN", SAGE),
    ("VISION", "rhodopsin → transducin → PDE → cGMP falls", "channels CLOSE → HYPERpolarise · the exception", RED),
    ("SMELL", "GPCR → G-olf → cAMP → CNG channels", "Ca²⁺ then opens Cl⁻ channels, amplifying", GOLD),
    ("TASTE", "salt: ENaC · sour: H⁺ · rest: T1R/T2R", "sweet, bitter, umami go through gustducin", GOLD),
    ("HEAT · PAIN", "TRP channels on free nerve endings", "TRPV1 >43 °C and capsaicin; TRPM8 cold, menthol", BLUE),
]
y = 372
for name, mech, note, col in rows:
    d.rect(70, y, 150, 34, col, FILL[col], rx=7, width=2)
    d.text(145, y + 22, name, color=col, weight="bold", size=12)
    d.text(240, y + 15, mech, anchor="start", color=NAVY, weight="bold", size=11)
    d.text(240, y + 30, note, anchor="start", color=GREY, size=11)
    y += 38

d.text(460, 612, "in the dark the photoreceptor sits depolarised and leaks glutamate; light is what switches it off",
       color=RED, size=11)

# ---------------- Panel C: adaptation ----------------
d.rect(40, 638, 840, 246, GOLD, "none", rx=12, width=2)
d.text(460, 666, "Adaptation — and the receptors that will not",
       color=GOLD, weight="bold", size=16)

d.rect(70, 686, 250, 174, SAGE, FILL[SAGE], rx=10, width=2)
d.text(195, 712, "RAPIDLY ADAPTING", color=SAGE, weight="bold", size=13)
d.text(195, 734, "fires at onset and offset", color=NAVY, size=12)
d.text(195, 752, "then falls silent", color=NAVY, size=12)
d.text(195, 782, "Meissner · Pacinian", color=SAGE, weight="bold", size=12)
d.text(195, 804, "reports CHANGE:", color=GREY, size=11)
d.text(195, 820, "vibration, movement,", color=GREY, size=11)
d.text(195, 836, "the moment of contact", color=GREY, size=11)

d.rect(336, 686, 250, 174, BLUE, FILL[BLUE], rx=10, width=2)
d.text(461, 712, "SLOWLY ADAPTING", color=BLUE, weight="bold", size=13)
d.text(461, 734, "keeps firing throughout", color=NAVY, size=12)
d.text(461, 752, "at a reduced rate", color=NAVY, size=12)
d.text(461, 782, "Merkel · Ruffini", color=BLUE, weight="bold", size=12)
d.text(461, 804, "reports STATE:", color=GREY, size=11)
d.text(461, 820, "steady pressure, shape,", color=GREY, size=11)
d.text(461, 836, "skin stretch, position", color=GREY, size=11)

d.rect(602, 686, 250, 174, RED, FILL[RED], rx=10, width=2)
d.text(727, 712, "BARELY ADAPTS", color=RED, weight="bold", size=13)
d.text(727, 734, "nociceptors SENSITISE", color=NAVY, size=12)
d.text(727, 752, "instead of fading", color=NAVY, size=12)
d.text(727, 782, "also proprioception", color=RED, weight="bold", size=12)
d.text(727, 804, "inflammation lowers the", color=GREY, size=11)
d.text(727, 820, "TRPV1 threshold — hence", color=GREY, size=11)
d.text(727, 836, "allodynia and hyperalgesia", color=GREY, size=11)

d.save("transduction-by-modality-and-adaptation")
print("ok")
