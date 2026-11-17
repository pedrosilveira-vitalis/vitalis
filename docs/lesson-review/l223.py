import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 934,
      "Three ways a fear comes back after extinction",
      "Extinction writes a second memory; it never erases the first",
      "Top: the fear-learning arc that sits under phobias and PTSD alike. Acquisition pairs a neutral cue with "
      "something aversive; extinction lays down a competing inhibitory memory rather than deleting the first, "
      "which is why the fear can return by three distinct routes that the exam keeps apart. Time brings it back "
      "as spontaneous recovery. A new place brings it back as renewal. Meeting the aversive event again brings "
      "it back as reinstatement. Bottom left: the circuit that decides whether extinction holds — amygdala up, "
      "ventromedial prefrontal cortex down, hippocampus shrunken and no longer tagging which context is safe. "
      "Bottom right: the three-question triage for telling these diagnoses apart."
      )

# ---------------- Panel A: the three returns ----------------
d.rect(40, 180, 840, 330, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Acquisition → extinction → and then what?", color=NAVY, weight="bold", size=15)

d.rect(70, 228, 230, 62, RED, FILL[RED], rx=8, width=1.8)
d.text(185, 252, "ACQUISITION", color=RED, weight="bold", size=12)
d.text(185, 272, "cue (CS) + aversive event (US)", color=GREY, size=10)
d.arrow(306, 259, 350, 259, GREY)
d.rect(356, 228, 230, 62, SAGE, FILL[SAGE], rx=8, width=1.8)
d.text(471, 252, "EXTINCTION", color=SAGE, weight="bold", size=12)
d.text(471, 272, "cue alone, again and again", color=GREY, size=10)
d.arrow(592, 259, 636, 259, GREY)
d.rect(642, 228, 208, 62, GOLD, FILL[GOLD], rx=8, width=1.8)
d.text(746, 252, "TWO MEMORIES NOW", color=GOLD, weight="bold", size=11)
d.text(746, 272, "the fear one is still there", color=GREY, size=10)

d.text(460, 318, "so the fear can come back three ways — keep the names apart",
       color=NAVY, weight="bold", size=12)

ways = [("SPONTANEOUS RECOVERY", "TIME passes", "nothing new happens; the fear simply\nreturns after a delay", BLUE),
        ("RENEWAL", "the PLACE changes", "extinguished at home, met again\nin the street — fear returns", GOLD),
        ("REINSTATEMENT", "the AVERSIVE EVENT recurs", "another bite, or a stressor — the\noriginal memory is re-energised", RED)]
cx = 68
for name, trigger, note, col in ways:
    d.rect(cx, 336, 262, 134, col, FILL[col], rx=10, width=2)
    d.text(cx + 131, 362, name, color=col, weight="bold", size=12)
    d.rect(cx + 36, 376, 190, 26, col, "none", rx=6, width=1.6)
    d.text(cx + 131, 394, trigger, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 131, 424 + j * 16, ln, color=NAVY, size=10)
    cx += 276
d.text(460, 492, "none of them means the extinction training failed — all three are expected",
       color=GREY, size=10)

# ---------------- Panel B: circuit ----------------
d.rect(40, 526, 410, 384, RED, "none", rx=12, width=2)
d.text(245, 554, "Why extinction fails in PTSD", color=RED, weight="bold", size=15)

d.rect(96, 578, 300, 60, RED, FILL[RED], rx=8, width=2)
d.text(246, 602, "AMYGDALA — overreactive", color=RED, weight="bold", size=12)
d.text(246, 622, "threshold for threat drops; fear generalises", color=GREY, size=9.5)

d.arrow(246, 644, 246, 674, BLUE, label="too weak", lx=46, ly=0, label_size=9.5)

d.rect(96, 680, 300, 60, BLUE, FILL[BLUE], rx=8, width=2)
d.text(246, 704, "vmPFC — underactive", color=BLUE, weight="bold", size=12)
d.text(246, 724, "cannot deliver the “it is safe now” signal", color=GREY, size=9.5)

d.rect(96, 756, 300, 60, GOLD, FILL[GOLD], rx=8, width=2)
d.text(246, 780, "HIPPOCAMPUS — reduced volume", color=GOLD, weight="bold", size=11.5)
d.text(246, 800, "no context tag, so no safe places", color=GREY, size=9.5)

d.rect(96, 832, 300, 62, GREY, FILL[GREY], rx=8, width=1.8)
d.text(246, 856, "AND THE CORTISOL GOES THE OTHER WAY", color=GREY, weight="bold", size=10)
d.text(246, 876, "PTSD runs LOW cortisol; depression runs high", color=NAVY, weight="bold", size=10)

# ---------------- Panel C: triage ----------------
d.rect(470, 526, 410, 384, SAGE, "none", rx=12, width=2)
d.text(675, 554, "Three questions, in order", color=SAGE, weight="bold", size=15)

qs = [("1 · Was there a stressor?",
       "none → anxiety disorder or OCD\nstressor, not DSM-traumatic → adjustment disorder\ntraumatic, under 1 month → acute stress disorder\ntraumatic, over 1 month → PTSD", BLUE),
      ("2 · Obsessions with rituals?",
       "intrusive thought neutralised by an act → OCD\nappearance → body dysmorphic disorder\ndiscarding → hoarding; pulling, picking → the rest", GOLD),
      ("3 · How wide is the fear?",
       "one object or situation → specific phobia\nbeing judged → social anxiety disorder\nunexpected attacks → panic disorder\nworry about everything → GAD", RED)]
y = 578
for name, body, col in qs:
    lines = body.split("\n")
    h = 36 + len(lines) * 16
    d.rect(494, y, 362, h, col, FILL[col], rx=8, width=1.8)
    d.text(675, y + 22, name, color=col, weight="bold", size=11.5)
    for j, ln in enumerate(lines):
        d.text(675, y + 42 + j * 16, ln, color=NAVY, size=9.5)
    y += h + 10

d.save("fear-return-after-extinction-and-anxiety-triage")
print("ok")
