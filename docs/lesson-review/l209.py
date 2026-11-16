import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 906,
      "Two roads to the amygdala, two timescales of stress",
      "Fear is fast because it is allowed to be wrong",
      "Top: LeDoux's two routes. The low road runs thalamus straight to amygdala and fires before you know "
      "what you are looking at — it is crude, and it is supposed to be, because a stick mistaken for a "
      "snake costs nothing while the reverse costs everything. The high road goes through sensory cortex "
      "first, arrives later, and can call the alarm off. Middle: the stress response on its two clocks. "
      "Sympathetic nerves and adrenal catecholamines act in seconds; the HPA axis takes minutes and keeps "
      "going for hours, which is the arm that does the damage when it never shuts off. Bottom: the four "
      "theories of emotion, which differ only in where they put the arrow between body, appraisal and "
      "feeling — and a question stem naming an experiment is usually asking which arrow it supports."
      )

# ---------------- Panel A: two roads ----------------
d.rect(40, 170, 840, 216, RED, "none", rx=12, width=2)
d.text(460, 198, "The low road and the high road", color=RED, weight="bold", size=16)

d.rect(70, 226, 134, 54, GREY, "#e9e4da", rx=9, width=2)
d.text(137, 258, "stimulus", color=GREY, weight="bold", size=13)

d.rect(250, 226, 134, 54, BLUE, FILL[BLUE], rx=9, width=2)
d.text(317, 258, "thalamus", color=BLUE, weight="bold", size=13)

d.rect(452, 300, 160, 54, SAGE, FILL[SAGE], rx=9, width=2)
d.text(532, 332, "sensory cortex", color=SAGE, weight="bold", size=13)

d.rect(700, 226, 150, 54, RED, FILL[RED], rx=9, width=2)
d.text(775, 258, "amygdala", color=RED, weight="bold", size=14)

d.arrow(206, 253, 246, 253, GREY, width=2)
d.arrow(386, 248, 696, 248, RED, width=3)
d.text(540, 276, "LOW ROAD — about 12 ms, crude, pre-conscious",
       color=RED, weight="bold", size=12)

d.path("M330 282 q0 22 44 30 q40 6 76 6", SAGE, 2.4, "none")
d.path("M612 322 q70 -4 112 -32", SAGE, 2.4, "none")
d.text(532, 368, "HIGH ROAD — slower, accurate, can cancel the alarm",
       color=SAGE, weight="bold", size=12)

# ---------------- Panel B: two timescales ----------------
d.rect(40, 402, 840, 232, GOLD, "none", rx=12, width=2)
d.text(460, 430, "Two clocks on the same threat", color=GOLD, weight="bold", size=16)

d.rect(70, 450, 380, 164, RED, FILL[RED], rx=10, width=2)
d.text(260, 474, "SECONDS — sympathetic", color=RED, weight="bold", size=13)
d.text(260, 498, "nerves release norepinephrine", color=NAVY, size=12)
d.text(260, 516, "adrenal MEDULLA adds epinephrine", color=NAVY, size=12)
d.text(260, 534, "(about 80% epi, 20% norepi)", color=GREY, size=11)
d.text(260, 562, "heart up · airways open · pupils wide", color=GREY, size=11)
d.text(260, 580, "gut down · glucose up · palms wet", color=GREY, size=11)
d.text(260, 602, "this is the arm you feel", color=RED, weight="bold", size=11)

d.rect(470, 450, 380, 164, BLUE, FILL[BLUE], rx=10, width=2)
d.text(660, 474, "MINUTES TO HOURS — HPA axis", color=BLUE, weight="bold", size=13)
d.text(660, 500, "hypothalamus: CRH", color=NAVY, weight="bold", size=12)
d.text(660, 520, "↓  anterior pituitary: ACTH", color=NAVY, weight="bold", size=12)
d.text(660, 540, "↓  adrenal CORTEX: cortisol", color=NAVY, weight="bold", size=12)
d.text(660, 566, "mobilises fuel · damps immunity", color=GREY, size=11)
d.text(660, 584, "negative feedback shuts it down", color=GREY, size=11)
d.text(660, 606, "chronic elevation injures the hippocampus", color=BLUE, weight="bold", size=11)

# ---------------- Panel C: four theories ----------------
d.rect(40, 650, 840, 232, SAGE, "none", rx=12, width=2)
d.text(460, 678, "Four theories, four arrangements of the same three things",
       color=SAGE, weight="bold", size=16)

theories = [
    ("JAMES–LANGE", "stimulus → body → feeling", "you are afraid because you tremble", SAGE),
    ("CANNON–BARD", "stimulus → body AND feeling", "at the same time, neither causing the other", BLUE),
    ("SCHACHTER–SINGER", "arousal + label → feeling", "same adrenaline, different emotion by context", GOLD),
    ("LAZARUS", "appraisal → feeling and body", "what it means to me comes first", RED),
]
y = 700
for name, chain, note, col in theories:
    d.rect(70, y, 230, 38, col, FILL[col], rx=8, width=2)
    d.text(185, y + 24, name, color=col, weight="bold", size=12)
    d.text(320, y + 17, chain, anchor="start", color=NAVY, weight="bold", size=12)
    d.text(320, y + 33, note, anchor="start", color=GREY, size=11)
    y += 42

d.text(460, 876, "block the body's arousal and James-Lange predicts the feeling fades; Cannon-Bard predicts "
                 "it does not",
       color=NAVY, weight="bold", size=11)

d.save("two-roads-to-the-amygdala-and-the-stress-axes")
print("ok")
