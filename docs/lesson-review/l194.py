import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 884,
      "Memory is several systems wearing one name",
      "Which structure is damaged tells you exactly which kind of remembering fails",
      "Top: the branching of long-term memory. Explicit memory, which needs conscious access, splits into "
      "episodic memory for personal events, run by the hippocampus, and semantic memory for plain facts, hubbed "
      "in the anterior temporal lobes. Implicit memory, which shows without conscious recall, splits into "
      "procedural skills in the basal ganglia and cerebellum, priming in the neocortex, classical conditioning "
      "with the amygdala for fear and the cerebellum for eyeblink, and non-associative habituation and "
      "sensitisation. Middle: the clinical dissociations, with each disease matched to the structure it attacks "
      "and the memory it spares. Bottom: consolidation, from synaptic changes within hours through long-term "
      "potentiation to systems consolidation over months, as sleep replays the trace and the cortex gradually "
      "takes over from the hippocampus."
      )

# ---------------- Panel A: the tree ----------------
d.rect(40, 156, 840, 288, BLUE, "none", rx=12, width=2)
d.text(460, 184, "One name, two families", color=BLUE, weight="bold", size=16)

d.rect(390, 198, 140, 34, NAVY, FILL[NAVY], rx=8, width=2)
d.text(460, 221, "LONG-TERM", color=NAVY, weight="bold", size=14)
d.arrow(424, 234, 262, 258, GREY, width=1.8)
d.arrow(496, 234, 658, 258, GREY, width=1.8)

d.rect(140, 260, 244, 34, BLUE, FILL[BLUE], rx=8, width=2)
d.text(262, 283, "EXPLICIT — you can state it", color=BLUE, weight="bold", size=13)
d.rect(536, 260, 244, 34, RED, FILL[RED], rx=8, width=2)
d.text(658, 283, "IMPLICIT — it shows in behaviour", color=RED, weight="bold", size=13)

ex = [("episodic", "your own events,\nplaced in time", "hippocampus", 76),
      ("semantic", "facts with no\npersonal context", "anterior temporal", 258)]
for name, gloss, where, x in ex:
    d.rect(x, 312, 170, 92, BLUE, "none", rx=9, width=2)
    d.text(x + 85, 336, name, color=BLUE, weight="bold", size=14)
    a, b = gloss.split("\n")
    d.text(x + 85, 358, a, color=NAVY, size=11)
    d.text(x + 85, 374, b, color=NAVY, size=11)
    d.text(x + 85, 396, where, color=GREY, weight="bold", size=11)

im = [("procedural", "skills and habits", "basal ganglia,\ncerebellum", 460),
      ("priming", "prior exposure\nspeeds processing", "neocortex", 606),
      ("conditioning", "fear → amygdala;\neyeblink → cerebellum", "", 752)]
for name, gloss, where, x in im:
    d.rect(x, 312, 136, 92, RED, "none", rx=9, width=2)
    d.text(x + 68, 336, name, color=RED, weight="bold", size=13)
    lines = gloss.split("\n")
    d.text(x + 68, 358, lines[0], color=NAVY, size=11)
    if len(lines) > 1:
        d.text(x + 68, 374, lines[1], color=NAVY, size=11)
    if where:
        for i, w in enumerate(where.split("\n")):
            d.text(x + 68, 382 + i * 13, w, color=GREY, weight="bold", size=10)

d.text(460, 426, "H.M. lost the left family entirely and kept the right one intact",
       color=GREY, size=13)

# ---------------- Panel B: dissociations ----------------
d.rect(40, 460, 840, 206, SAGE, "none", rx=12, width=2)
d.text(460, 488, "Which structure, which failure", color=SAGE, weight="bold", size=16)

rows = [("medial temporal lobe", "H.M., hypoxia", "no new episodes; skills and priming fine", BLUE),
        ("diencephalon", "Korsakoff: mammillary bodies,\nmediodorsal thalamus", "amnesia plus confabulation", GOLD),
        ("anterior temporal", "semantic dementia", "concepts go; recent episodes hold up", RED),
        ("striatum", "Parkinson's, Huntington's", "habits and skills go; facts hold up", SAGE)]
y = 510
for where, disease, effect, col in rows:
    d.text(224, y, where, anchor="end", color=col, weight="bold", size=13)
    parts = disease.split("\n")
    d.text(240, y, parts[0], anchor="start", color=NAVY, size=12)
    if len(parts) > 1:
        d.text(240, y + 15, parts[1], anchor="start", color=NAVY, size=12)
    d.text(858, y, effect, anchor="end", color=GREY, size=12)
    y += 38 if len(parts) == 1 else 44

d.text(460, 652, "a double dissociation: hippocampal damage spares concepts, "
                 "temporal-pole damage spares episodes",
       color=NAVY, weight="bold", size=13)

# ---------------- Panel C: consolidation ----------------
d.rect(40, 682, 840, 178, GOLD, "none", rx=12, width=2)
d.text(460, 710, "Consolidation runs on two clocks", color=GOLD, weight="bold", size=16)

d.rect(70, 730, 370, 104, BLUE, FILL[BLUE], rx=10, width=2)
d.text(255, 756, "SYNAPTIC — minutes to hours", color=BLUE, weight="bold", size=14)
d.text(255, 780, "LTP: NMDA receptors, calcium in,", color=NAVY, size=12)
d.text(255, 798, "AMPA receptors inserted, protein made", color=NAVY, size=12)
d.text(255, 820, "the synapse itself gets stronger", color=GREY, size=11)

d.rect(480, 730, 370, 104, GOLD, FILL[GOLD], rx=10, width=2)
d.text(665, 756, "SYSTEMS — weeks to years", color=GOLD, weight="bold", size=14)
d.text(665, 780, "sleep replays the trace; the cortex", color=NAVY, size=12)
d.text(665, 798, "gradually takes over from the hippocampus", color=NAVY, size=12)
d.text(665, 820, "which is why old memories survive the lesion", color=GREY, size=11)

d.save("long-term-memory-systems-and-their-lesions")
print("ok")
