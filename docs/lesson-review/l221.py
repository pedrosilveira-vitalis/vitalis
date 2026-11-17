import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 1010,
      "Four pathways, two symptom classes, one duration ruler",
      "Where the dopamine goes decides whether blocking it helps or hurts",
      "Top: the four dopaminergic pathways. A D2 blocker cannot aim; it hits all four, which is why one drug "
      "produces both the therapeutic effect and the classic side effects. Mesolimbic hyperactivity is the "
      "target, mesocortical hypoactivity is the one that blockade makes worse, and nigrostriatal and "
      "tuberoinfundibular blockade buy the extrapyramidal symptoms and the raised prolactin. Middle: positive "
      "versus negative symptoms, the distinction every vignette turns on — excess versus absence, and which "
      "class the drugs actually treat. Bottom: the duration ruler that separates brief psychotic disorder from "
      "schizophreniform from schizophrenia, with the two diagnoses that are decided by something other than "
      "duration."
      )

# ---------------- Panel A: pathways ----------------
d.rect(40, 180, 840, 318, NAVY, "none", rx=12, width=2)
d.text(460, 208, "The four dopamine pathways, and what D2 blockade does to each",
       color=NAVY, weight="bold", size=15)

rows = [
    ("MESOLIMBIC", "VTA → nucleus accumbens, amygdala, hippocampus",
     "HYPERACTIVE", "blocking it → positive symptoms fall", "THE TARGET", RED),
    ("MESOCORTICAL", "VTA → prefrontal cortex",
     "HYPOACTIVE", "blocking it → negative symptoms, cognition worse", "COLLATERAL", BLUE),
    ("NIGROSTRIATAL", "substantia nigra → striatum",
     "normal", "blocking it → EPS, tardive dyskinesia", "SIDE EFFECT", GOLD),
    ("TUBEROINFUNDIBULAR", "hypothalamus → pituitary",
     "normal", "blocking it → prolactin rises", "SIDE EFFECT", SAGE),
]
y = 228
for name, route, state, effect, tag, col in rows:
    d.rect(66, y, 788, 54, col, FILL[col], rx=8, width=1.8)
    d.text(84, y + 23, name, anchor="start", color=col, weight="bold", size=12)
    d.text(84, y + 40, route, anchor="start", color=GREY, size=10)
    d.text(482, y + 23, "in schizophrenia: " + state, color=NAVY, weight="bold", size=11)
    d.text(482, y + 40, effect, color=NAVY, size=10)
    d.rect(742, y + 14, 98, 26, col, "none", rx=6, width=1.6)
    d.text(791, y + 32, tag, color=col, weight="bold", size=9.5)
    y += 62

d.text(460, 486, "one drug, four pathways — the side effects are the same mechanism as the cure",
       color=NAVY, weight="bold", size=11)

# ---------------- Panel B: positive vs negative ----------------
d.rect(40, 514, 410, 268, RED, "none", rx=12, width=2)
d.text(245, 542, "POSITIVE · something added", color=RED, weight="bold", size=14)
d.text(245, 562, "excess or distortion of normal function", color=GREY, size=10)
items = ["delusions — persecutory, grandiose, referential,",
         "   thought insertion, withdrawal, broadcasting",
         "hallucinations — auditory above all",
         "disorganised speech — loose associations,",
         "   tangentiality, clang, neologisms, word salad",
         "disorganised or catatonic behaviour"]
for i, t in enumerate(items):
    d.text(245, 588 + i * 20, t, color=NAVY, size=10.5)
d.line(80, 718, 410, 718, RED, 1, dash="3,3")
d.text(245, 740, "respond well to antipsychotics", color=RED, weight="bold", size=11.5)
d.text(245, 762, "mesolimbic hyperactivity", color=GREY, size=10)

d.rect(470, 514, 410, 268, BLUE, "none", rx=12, width=2)
d.text(675, 542, "NEGATIVE · something missing", color=BLUE, weight="bold", size=14)
d.text(675, 562, "the five A's — diminution or absence", color=GREY, size=10)
alist = [("Affective flattening", "narrowed expression, monotone"),
         ("Alogia", "poverty of speech"),
         ("Avolition", "cannot start or sustain goals"),
         ("Anhedonia", "no pleasure from what once pleased"),
         ("Asociality", "withdrawal from others")]
for i, (a, b) in enumerate(alist):
    d.text(560, 588 + i * 26, a, anchor="start", color=BLUE, weight="bold", size=11)
    d.text(560, 604 + i * 26, b, anchor="start", color=GREY, size=9.5)
d.line(510, 718, 840, 718, BLUE, 1, dash="3,3")
d.text(675, 740, "poorly treated, and they drive outcome", color=BLUE, weight="bold", size=11.5)
d.text(675, 762, "mesocortical hypoactivity, hypofrontality", color=GREY, size=10)

# ---------------- Panel C: duration ruler ----------------
d.rect(40, 798, 840, 192, SAGE, "none", rx=12, width=2)
d.text(460, 826, "The duration ruler", color=SAGE, weight="bold", size=15)

x0, x1 = 110, 790
yb = 872
d.line(x0, yb, x1, yb, GREY, 2)
marks = [(x0, "1 day"), (x0 + 200, "1 month"), (x0 + 450, "6 months"), (x1, "")]
for mx, lab in marks:
    d.line(mx, yb - 7, mx, yb + 7, GREY, 2)
    if lab:
        d.text(mx, yb + 26, lab, color=NAVY, weight="bold", size=11)

d.rect(x0, yb - 34, 200, 22, GOLD, FILL[GOLD], rx=5, width=1.6)
d.text(x0 + 100, yb - 19, "brief psychotic disorder", color=GOLD, weight="bold", size=10.5)
d.rect(x0 + 200, yb - 34, 250, 22, BLUE, FILL[BLUE], rx=5, width=1.6)
d.text(x0 + 325, yb - 19, "schizophreniform", color=BLUE, weight="bold", size=10.5)
d.rect(x0 + 450, yb - 34, 230, 22, RED, FILL[RED], rx=5, width=1.6)
d.text(x0 + 565, yb - 19, "schizophrenia", color=RED, weight="bold", size=10.5)

d.text(460, 928, "decided by something other than duration:", color=NAVY, weight="bold", size=11)
d.text(250, 952, "DELUSIONAL DISORDER", color=SAGE, weight="bold", size=10.5)
d.text(250, 970, "≥ 1 month of delusions, function otherwise intact", color=GREY, size=10)
d.text(670, 952, "SCHIZOAFFECTIVE", color=SAGE, weight="bold", size=10.5)
d.text(670, 970, "≥ 2 weeks of psychosis with no mood episode", color=GREY, size=10)

d.save("dopamine-pathways-symptom-classes-and-durations")
print("ok")
