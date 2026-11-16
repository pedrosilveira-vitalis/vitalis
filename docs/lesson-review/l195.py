import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 892,
      "A memory is a synapse that was changed",
      "The NMDA receptor only opens when both sides fire — that is the whole trick",
      "Top: the induction of long-term potentiation at a single synapse. Glutamate alone is not enough, because "
      "a magnesium ion plugs the NMDA channel at rest; only when the postsynaptic membrane is already "
      "depolarised does the plug come out, letting calcium in. The calcium activates CaMKII, which "
      "phosphorylates AMPA receptors and brings more of them to the membrane, so the same presynaptic signal now "
      "produces a bigger response. Middle: early against late potentiation — the first lasting one to three "
      "hours on existing proteins, the second lasting days and requiring CREB, new gene expression and new "
      "protein, which is why a protein synthesis blocker spares short-term memory and abolishes long-term "
      "memory. Bottom: the two consolidations, synaptic within hours and systems over months as sleep replays "
      "the trace, with slow-wave sleep favouring declarative material and REM favouring procedural and emotional."
      )

# ---------------- Panel A: LTP induction ----------------
d.rect(40, 156, 840, 268, BLUE, "none", rx=12, width=2)
d.text(460, 184, "Why the NMDA receptor is a coincidence detector",
       color=BLUE, weight="bold", size=16)

# presynaptic terminal
d.path("M90 206 q60 -10 110 10 l0 70 q-60 20 -110 6 z", GREY, 2, "#e9e4da")
d.text(145, 250, "presynaptic", color=GREY, weight="bold", size=12)
for i in range(6):
    d.circle(216 + (i % 3) * 14, 236 + (i // 3) * 18, 4, SAGE, SAGE)
d.text(248, 214, "glutamate", color=SAGE, weight="bold", size=12)

# postsynaptic membrane
d.rect(290, 206, 20, 120, GREY, "#e9e4da", rx=3, width=2)
d.text(300, 344, "postsynaptic", color=GREY, weight="bold", size=12)

# the two receptors
d.rect(282, 222, 36, 34, RED, FILL[RED], rx=5, width=2)
d.text(300, 244, "N", color=RED, weight="bold", size=14)
d.text(344, 232, "NMDA", anchor="start", color=RED, weight="bold", size=13)
d.text(344, 250, "blocked by Mg²⁺ until the", anchor="start", color=GREY, size=11)
d.text(344, 266, "membrane depolarises", anchor="start", color=GREY, size=11)

d.rect(282, 280, 36, 34, SAGE, FILL[SAGE], rx=5, width=2)
d.text(300, 302, "A", color=SAGE, weight="bold", size=14)
d.text(344, 292, "AMPA", anchor="start", color=SAGE, weight="bold", size=13)
d.text(344, 310, "carries the ordinary signal", anchor="start", color=GREY, size=11)

# cascade
steps = [("Ca²⁺ floods in", RED), ("CaMKII activated", GOLD),
         ("AMPA phosphorylated\nand more inserted", SAGE), ("bigger response\nto the same input", BLUE)]
yy = 206
for idx, (name, col) in enumerate(steps):
    lines = name.split("\n")
    d.rect(556, yy, 300, 38, col, FILL[col], rx=8, width=2)
    d.text(706, yy + 24, lines[0] if len(lines) == 1 else lines[0] + " \u2014 " + lines[1], color=col, weight="bold", size=12)
    if idx < 3:
        d.arrow(706, yy + 38, 706, yy + 46, GREY, width=1.8)
    yy += 48
d.text(250, 374, "Hebb in molecules: fire together, wire together",
       color=GREY, size=12)

d.text(460, 398, "both sides must be active at once — that is what makes the synapse selective",
       color=NAVY, weight="bold", size=14)

# ---------------- Panel B: early vs late ----------------
d.rect(40, 440, 840, 198, GOLD, "none", rx=12, width=2)
d.text(460, 468, "Two phases, and only one of them needs the nucleus",
       color=GOLD, weight="bold", size=16)

d.rect(70, 488, 370, 124, SAGE, FILL[SAGE], rx=10, width=2)
d.text(255, 514, "EARLY LTP — 1 to 3 hours", color=SAGE, weight="bold", size=15)
d.text(255, 540, "phosphorylate what is already there;", color=NAVY, size=12)
d.text(255, 558, "traffic existing AMPA receptors in", color=NAVY, size=12)
d.text(255, 584, "no new protein needed", color=GREY, weight="bold", size=12)

d.rect(480, 488, 370, 124, GOLD, FILL[GOLD], rx=10, width=2)
d.text(665, 514, "LATE LTP — hours to days", color=GOLD, weight="bold", size=15)
d.text(665, 540, "PKA → CREB → new gene expression", color=NAVY, size=12)
d.text(665, 558, "new synaptic protein; spines grow", color=NAVY, size=12)
d.text(665, 584, "a protein synthesis blocker stops this one only", color=GREY, weight="bold", size=12)

# ---------------- Panel C: consolidation and sleep ----------------
d.rect(40, 654, 840, 206, SAGE, "none", rx=12, width=2)
d.text(460, 682, "From one synapse to the whole cortex", color=SAGE, weight="bold", size=16)

m = d.axes(110, 702, 350, 108, "time since learning", "hippocampus needed",
           (0, 10), (0, 1.1), ticks_x=None, ticks_y=None)
d.curve(m, [(t / 25, math.exp(-(t / 25) / 3.2)) for t in range(0, 251)], SAGE, 2.8)
px, py = m(0.4, 0.88)
d.text(px + 8, py, "hours: hippocampus holds it", anchor="start", color=NAVY, weight="bold", size=12)
px, py = m(6.2, 0.15)
d.text(px, py - 12, "months: the cortex holds it", anchor="start", color=GREY, size=12)

d.rect(500, 700, 350, 56, BLUE, FILL[BLUE], rx=9, width=2)
d.text(675, 722, "SLOW-WAVE SLEEP", color=BLUE, weight="bold", size=13)
d.text(675, 742, "sharp-wave ripples replay the day; declarative material", color=NAVY, size=12)
d.rect(500, 766, 350, 56, RED, FILL[RED], rx=9, width=2)
d.text(675, 788, "REM SLEEP", color=RED, weight="bold", size=13)
d.text(675, 808, "procedural and emotional material; high acetylcholine", color=NAVY, size=12)
d.text(675, 844, "deprive one stage and you lose that kind of memory", color=GREY, size=12)

d.save("ltp-and-the-biology-of-memory-formation")
print("ok")
