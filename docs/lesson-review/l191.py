import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 892,
      "Three stores, three failures",
      "Encoding, storage, retrieval — name which one broke and the answer follows",
      "Top: the flow from the world through sensory memory, which holds a great deal for well under a second, "
      "into working memory, which holds about seven chunks for fifteen to thirty seconds, and on into long-term "
      "memory, which has no known limit; attention gates the first transfer and encoding the second, and "
      "retrieval brings things back. Middle left: the branching of long-term memory into explicit memory, which "
      "splits into episodic and semantic, and implicit memory, which splits into procedural, priming and "
      "conditioning, with the structure each depends on. Middle right: Baddeley's working memory, a central "
      "executive over a phonological loop, a visuospatial sketchpad and an episodic buffer. Bottom left: levels "
      "of processing, from structural through phonemic to semantic, with memory strength rising as processing "
      "deepens. Bottom right: the two kinds of interference, old disrupting new and new disrupting old."
      )

# ---------------- Panel A: the pipeline ----------------
d.rect(40, 150, 840, 182, BLUE, "none", rx=12, width=2)
d.text(460, 178, "The pipeline, and what gates each step", color=BLUE, weight="bold", size=16)

stores = [("SENSORY", "everything, < 1 s", "iconic ≈ 250–500 ms\necho ≈ 3–4 s", GOLD),
          ("WORKING", "≈ 7 chunks, 15–30 s", "rehearsal keeps it\nalive, nothing more", SAGE),
          ("LONG-TERM", "no known limit", "minutes to\na lifetime", BLUE)]
x = 96
for name, cap, note, col in stores:
    d.rect(x, 198, 214, 96, col, FILL[col], rx=10, width=2)
    d.text(x + 107, 224, name, color=col, weight="bold", size=15)
    d.text(x + 107, 248, cap, color=NAVY, weight="bold", size=13)
    a, b = note.split("\n")
    d.text(x + 107, 270, a, color=GREY, size=11)
    d.text(x + 107, 286, b, color=GREY, size=11)
    x += 270

d.arrow(314, 246, 362, 246, NAVY, width=2.4)
d.text(338, 232, "attention", color=NAVY, weight="bold", size=12)
d.arrow(584, 246, 632, 246, NAVY, width=2.4)
d.text(608, 232, "encoding", color=NAVY, weight="bold", size=12)
d.arrow(632, 274, 584, 274, RED, width=2.4)
d.text(608, 296, "retrieval", color=RED, weight="bold", size=12)

d.text(460, 320, "lose it at step one and it was never encoded — that is not a retrieval problem",
       color=GREY, size=13)

# ---------------- Panel B: LTM tree ----------------
d.rect(40, 348, 440, 268, SAGE, "none", rx=12, width=2)
d.text(260, 376, "Long-term memory is not one thing", color=SAGE, weight="bold", size=15)

d.rect(190, 392, 140, 32, SAGE, FILL[SAGE], rx=8, width=2)
d.text(260, 414, "LONG-TERM", color=SAGE, weight="bold", size=13)
d.arrow(224, 426, 150, 448, GREY, width=1.8)
d.arrow(296, 426, 370, 448, GREY, width=1.8)

d.rect(70, 450, 160, 30, BLUE, FILL[BLUE], rx=7, width=2)
d.text(150, 471, "EXPLICIT", color=BLUE, weight="bold", size=13)
d.text(150, 496, "you can say it", color=GREY, size=11)
d.rect(290, 450, 160, 30, RED, FILL[RED], rx=7, width=2)
d.text(370, 471, "IMPLICIT", color=RED, weight="bold", size=13)
d.text(370, 496, "it just shows", color=GREY, size=11)

d.text(150, 522, "episodic — your own events", color=NAVY, size=12)
d.text(150, 542, "semantic — plain facts", color=NAVY, size=12)
d.text(150, 566, "hippocampus", color=BLUE, weight="bold", size=12)
d.text(370, 522, "procedural — how to", color=NAVY, size=12)
d.text(370, 542, "priming, conditioning", color=NAVY, size=12)
d.text(370, 566, "basal ganglia, cerebellum", color=RED, weight="bold", size=11)

d.text(260, 596, "H.M. lost the left branch and kept the right", color=GREY, size=12)

# ---------------- Panel C: working memory ----------------
d.rect(500, 348, 380, 268, GOLD, "none", rx=12, width=2)
d.text(690, 376, "Inside working memory", color=GOLD, weight="bold", size=15)

d.rect(560, 394, 260, 40, GOLD, FILL[GOLD], rx=9, width=2)
d.text(690, 420, "CENTRAL EXECUTIVE", color=GOLD, weight="bold", size=14)
d.text(690, 450, "allocates attention, switches tasks", color=GREY, size=12)

subs = [("phonological loop", "the inner voice;\nholds speech ≈ 2 s", 466),
        ("visuospatial sketchpad", "the inner eye;\nimages and layout", 466),
        ("episodic buffer", "binds the two to long-term memory", 556)]
d.rect(528, 466, 160, 76, BLUE, FILL[BLUE], rx=8, width=2)
d.text(608, 488, "phonological loop", color=BLUE, weight="bold", size=12)
d.text(608, 508, "the inner voice;", color=NAVY, size=11)
d.text(608, 524, "holds speech ≈ 2 s", color=NAVY, size=11)
d.rect(700, 466, 160, 76, SAGE, FILL[SAGE], rx=8, width=2)
d.text(780, 488, "visuospatial sketchpad", color=SAGE, weight="bold", size=12)
d.text(780, 508, "the inner eye;", color=NAVY, size=11)
d.text(780, 524, "images and layout", color=NAVY, size=11)
d.rect(528, 554, 332, 34, RED, FILL[RED], rx=8, width=2)
d.text(694, 576, "episodic buffer: binds them to long-term memory", color=RED, weight="bold", size=12)

# ---------------- Panel D: levels of processing ----------------
d.rect(40, 632, 440, 232, NAVY, "none", rx=12, width=2)
d.text(260, 660, "Deeper processing, stronger trace", color=NAVY, weight="bold", size=15)

levels = [("structural", "is it in capitals?", 0.22, GREY),
          ("phonemic", "does it rhyme?", 0.48, BLUE),
          ("semantic", "what does it mean?", 1.0, SAGE)]
y = 684
for name, q, strength, col in levels:
    d.text(162, y + 22, name, anchor="end", color=col, weight="bold", size=13)
    d.rect(172, y + 6, int(150 * strength), 22, col, FILL[col], rx=5, width=2)
    d.text(336, y + 22, q, anchor="start", color=GREY, size=12)
    y += 48

d.text(260, 836, "repetition alone is shallow; connecting to meaning is what lasts",
       color=GREY, size=12)

# ---------------- Panel E: interference ----------------
d.rect(500, 632, 380, 232, RED, "none", rx=12, width=2)
d.text(690, 660, "Which way does the interference run?", color=RED, weight="bold", size=15)

d.rect(530, 682, 320, 70, BLUE, FILL[BLUE], rx=9, width=2)
d.text(690, 706, "PROACTIVE: old blocks new", color=BLUE, weight="bold", size=14)
d.text(690, 730, "old Spanish gets in the way of new Italian", color=NAVY, size=12)
d.rect(530, 766, 320, 70, RED, FILL[RED], rx=9, width=2)
d.text(690, 790, "RETROACTIVE: new blocks old", color=RED, weight="bold", size=14)
d.text(690, 814, "new Italian crowds out the old Spanish", color=NAVY, size=12)

d.save("information-processing-memory-stores-and-failures")
print("ok")
