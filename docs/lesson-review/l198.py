import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 916,
      "Five levels of language, and what breaks at each one",
      "The aphasias are a map: fluency, comprehension, repetition — in that order",
      "Top: the hierarchy, from sounds that carry no meaning up to the social use of an utterance, each level "
      "with the disorder that singles it out. Bottom left: the classical language areas on the left hemisphere "
      "and the tract between them. Bottom right: the three questions that sort the aphasias. Is speech fluent? "
      "No points to Broca's area in the inferior frontal gyrus. Is comprehension intact? No points to "
      "Wernicke's area in the posterior superior temporal gyrus. If both are fine but repetition fails, the "
      "lesion is in the arcuate fasciculus between them. The angular gyrus sits apart: damage there gives "
      "alexia together with agraphia, alongside the rest of Gerstmann's syndrome, while alexia with writing "
      "preserved comes from a left occipital and splenial lesion instead."
      )

# ---------------- Panel A: the five levels ----------------
d.rect(40, 164, 840, 270, BLUE, "none", rx=12, width=2)
d.text(460, 192, "From sound to social meaning", color=BLUE, weight="bold", size=16)

levels = [
    ("PRAGMATICS", "context and speaker intent", "\"Can you pass the salt?\" is a request", "autism spectrum: this level alone", GOLD),
    ("SEMANTICS", "meaning of words and sentences", "compositional, so infinitely productive", "semantic dementia; Wernicke's aphasia", RED),
    ("SYNTAX", "how words combine", "surface structure vs deep structure", "agrammatism in Broca's aphasia", SAGE),
    ("MORPHOLOGY", "smallest units of meaning", "un + break + able = three morphemes", "specific language impairment", BLUE),
    ("PHONOLOGY", "smallest units of sound", "~44 phonemes; no meaning on their own", "dyslexia is a phonological deficit", GREY),
]
y = 214
for name, what, ex, dis, col in levels:
    d.rect(70, y, 176, 38, col, FILL[col], rx=7, width=2)
    d.text(158, y + 24, name, color=col, weight="bold", size=12)
    d.text(266, y + 17, what, anchor="start", color=NAVY, weight="bold", size=12)
    d.text(266, y + 33, ex, anchor="start", color=GREY, size=11)
    d.text(600, y + 25, dis, anchor="start", color=col, size=11)
    y += 42

d.arrow(58, 418, 58, 222, GREY, width=2)

# ---------------- Panel B: the brain ----------------
d.rect(40, 450, 404, 440, SAGE, "none", rx=12, width=2)
d.text(242, 478, "Left hemisphere, lateral view", color=SAGE, weight="bold", size=15)

d.rect(82, 498, 320, 172, GREY, "#efe9df", rx=78, width=2.4)
d.path("M118 608 q86 -34 162 -4", GREY, 1.6, "none", dash="5,4")
d.text(242, 690, "frontal at left \u00b7 occipital at right",
       color=GREY, size=10)

d.circle(158, 552, 24, BLUE, FILL[BLUE], width=2)
d.text(158, 557, "B", color=BLUE, weight="bold", size=14)
d.circle(278, 602, 24, RED, FILL[RED], width=2)
d.text(278, 607, "W", color=RED, weight="bold", size=14)
d.path("M177 566 q52 8 82 28", GOLD, 3, "none")
d.circle(358, 566, 19, GOLD, FILL[GOLD], width=2)
d.text(358, 571, "A", color=GOLD, weight="bold", size=12)

d.text(242, 716, "B  Broca's area — inferior frontal gyrus", color=BLUE, weight="bold", size=12)
d.text(242, 734, "speech output and grammar", color=GREY, size=11)
d.text(242, 760, "W  Wernicke's area — posterior superior", color=RED, weight="bold", size=12)
d.text(242, 778, "temporal gyrus; comprehension", color=GREY, size=11)
d.text(242, 804, "—  arcuate fasciculus between them", color=GOLD, weight="bold", size=12)
d.text(242, 822, "carries repetition", color=GREY, size=11)
d.text(242, 850, "A  angular gyrus — reading and writing;", color=GOLD, weight="bold", size=12)
d.text(242, 868, "damage gives alexia WITH agraphia", color=NAVY, size=11)

# ---------------- Panel C: the aphasia decision ----------------
d.rect(460, 450, 420, 440, RED, "none", rx=12, width=2)
d.text(670, 478, "Three questions, in order", color=RED, weight="bold", size=15)

steps = [
    ("Is speech fluent?", "no → BROCA'S", "effortful, telegraphic;\ncomprehension intact; aware of it", BLUE),
    ("Is comprehension intact?", "no → WERNICKE'S", "fluent word salad;\nno insight into the deficit", RED),
    ("Is repetition intact?", "no → CONDUCTION", "fluent and understands,\nbut cannot repeat back", GOLD),
]
y = 500
for q, verdict, note, col in steps:
    d.rect(488, y, 364, 102, col, FILL[col], rx=10, width=2)
    d.text(670, y + 26, q, color=NAVY, weight="bold", size=13)
    d.text(670, y + 50, verdict, color=col, weight="bold", size=14)
    n1, n2 = note.split("\n")
    d.text(670, y + 72, n1, color=GREY, size=11)
    d.text(670, y + 88, n2, color=GREY, size=11)
    if y < 700:
        d.arrow(670, y + 102, 670, y + 116, GREY, width=1.8)
    y += 118

d.text(670, 872, "all three impaired → global aphasia", color=NAVY, weight="bold", size=12)

d.save("language-levels-and-the-aphasias")
print("ok")
