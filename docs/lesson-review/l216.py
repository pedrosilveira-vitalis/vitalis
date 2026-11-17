import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 906,
      "Four men, four answers to “how many traits are there?”",
      "The question that separates them is how they counted, and whether they asked why",
      "Top: the lineage. Allport opened a dictionary and sorted words by how much of a life they explained; "
      "Cattell put the same words through factor analysis and got sixteen; Eysenck said sixteen was too many "
      "and factored again to three, which he tried to tie to the nervous system; the Big Five landed in "
      "between and has stayed there because it keeps replicating. Bottom left: OCEAN, with what each "
      "dimension actually predicts — which is what vignette questions test, not the definitions. Bottom "
      "right: the two biological claims Eysenck made that the exam still asks about, drawn the right way "
      "round. Introverts start from higher cortical arousal, which is why the quiet room suits them and why "
      "reversing this is the commonest error on the topic."
      )

# ---------------- Panel A: the lineage ----------------
d.rect(40, 178, 840, 212, BLUE, "none", rx=12, width=2)
d.text(460, 206, "From 18,000 words to five dimensions", color=BLUE, weight="bold", size=16)

men = [
    ("ALLPORT", "~4,500 trait words", "cardinal · central · secondary", "sorted by how much of a life\neach one explains", GREY),
    ("CATTELL", "16 source traits", "factor analysis of the words", "surface traits are what you see;\nsource traits cause them", GOLD),
    ("EYSENCK", "3 supertraits", "P · E · N", "factored again, and asked\nwhat the brain was doing", RED),
    ("BIG FIVE", "5 factors", "O · C · E · A · N", "replicates across languages;\nstrong at predicting", SAGE),
]
x = 62
for name, count, mid, note, col in men:
    d.rect(x, 226, 198, 144, col, FILL[col], rx=10, width=2)
    d.text(x + 99, 252, name, color=col, weight="bold", size=13)
    d.text(x + 99, 274, count, color=NAVY, weight="bold", size=13)
    d.text(x + 99, 296, mid, color=NAVY, size=11)
    n1, n2 = note.split("\n")
    d.text(x + 99, 326, n1, color=GREY, size=10)
    d.text(x + 99, 342, n2, color=GREY, size=10)
    if x < 650:
        d.arrow(x + 198, 298, x + 206, 298, GREY, width=1.8)
    x += 206

# ---------------- Panel B: OCEAN ----------------
d.rect(40, 410, 470, 466, SAGE, "none", rx=12, width=2)
d.text(275, 438, "OCEAN, and what each one predicts", color=SAGE, weight="bold", size=15)

ocean = [
    ("O", "OPENNESS", "curious, imaginative, likes the new", "creative achievement", GOLD),
    ("C", "CONSCIENTIOUSNESS", "organised, dependable, deliberate", "job performance · adherence · longevity", SAGE),
    ("E", "EXTRAVERSION", "sociable, assertive, seeks stimulation", "positive affect and well-being", BLUE),
    ("A", "AGREEABLENESS", "cooperative, trusting, harmony-seeking", "relationship satisfaction", GOLD),
    ("N", "NEUROTICISM", "reactive, anxious, slow to settle", "depression, anxiety, poorer health", RED),
]
y = 460
for letter, name, what, predicts, col in ocean:
    d.rect(66, y, 418, 72, col, FILL[col], rx=9, width=2)
    d.circle(100, y + 36, 19, col, "#ffffff", width=2)
    d.text(100, y + 42, letter, color=col, weight="bold", size=17)
    d.text(300, y + 22, name, color=col, weight="bold", size=12)
    d.text(300, y + 42, what, color=NAVY, size=11)
    d.text(300, y + 60, "predicts: " + predicts, color=GREY, size=10)
    y += 78

d.text(275, 862, "heritability runs about 40–60% for every one of them", color=NAVY, size=11)

# ---------------- Panel C: Eysenck's biology ----------------
d.rect(530, 410, 350, 466, RED, "none", rx=12, width=2)
d.text(705, 438, "Eysenck's two claims", color=RED, weight="bold", size=15)

d.rect(556, 458, 298, 190, BLUE, FILL[BLUE], rx=10, width=2)
d.text(705, 482, "EXTRAVERSION ← cortical arousal", color=BLUE, weight="bold", size=12)
d.text(705, 508, "INTROVERT", color=NAVY, weight="bold", size=13)
d.text(705, 528, "starts HIGH on the dial", color=NAVY, size=11)
d.text(705, 546, "so added noise overshoots", color=GREY, size=11)
d.text(705, 564, "→ prefers the quiet room", color=BLUE, weight="bold", size=11)
d.line(596, 580, 814, 580, GREY, 1, dash="3,3")
d.text(705, 600, "EXTRAVERT", color=NAVY, weight="bold", size=13)
d.text(705, 618, "starts LOW — goes looking for input", color=NAVY, size=11)
d.text(705, 636, "→ bored by the quiet room", color=BLUE, weight="bold", size=11)

d.rect(556, 666, 298, 118, RED, FILL[RED], rx=10, width=2)
d.text(705, 690, "NEUROTICISM ← limbic reactivity", color=RED, weight="bold", size=12)
d.text(705, 716, "the alarm trips more easily", color=NAVY, size=11)
d.text(705, 734, "and takes longer to switch off", color=NAVY, size=11)
d.text(705, 762, "the modern version: HPA reactivity", color=GREY, size=11)

d.text(705, 812, "P · E · N is only three because he", color=GREY, size=11)
d.text(705, 830, "factor-analysed Cattell's sixteen again", color=GREY, size=11)
d.text(705, 858, "reversing the arousal claim is the classic slip",
       color=RED, weight="bold", size=11)

d.save("trait-models-ocean-and-eysenck-arousal")
print("ok")
