import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 1000,
      "One behaviour, four different explanations",
      "Who is judging whom decides which way the attribution falls",
      "Top: the same lateness, explained four ways. The fundamental attribution error, the actor-observer "
      "asymmetry and the self-serving bias are not separate facts to memorise — they are the same tilt seen from "
      "different seats. Watching someone else, the person is what you see, so the cause lands on their "
      "character. Being the person, the situation is what you see, so the cause lands on circumstance. Add the "
      "motive to protect self-esteem and the actor's own successes come back inside while their failures stay "
      "outside. Bottom left: Kelley's three dials, with the combinations that point each way. Bottom right: the "
      "inference biases that all run on one principle — what arrives first, or comes to mind easiest, counts "
      "for too much."
      )

# ---------------- Panel A: four attributions ----------------
d.rect(40, 180, 840, 318, NAVY, "none", rx=12, width=2)
d.text(460, 208, "“They arrived late.” Now explain it.", color=NAVY, weight="bold", size=15)

d.rect(70, 228, 780, 44, GREY, FILL[GREY], rx=8, width=1.6)
d.text(460, 256, "THE BEHAVIOUR: someone shows up twenty minutes late to a meeting",
       color=NAVY, weight="bold", size=12)

quad = [("YOU, watching THEM", "“they are disorganised”", "DISPOSITIONAL",
         "fundamental attribution error", RED),
        ("YOU, explaining YOU", "“the train was delayed”", "SITUATIONAL",
         "the actor half of actor-observer", BLUE),
        ("YOU, after SUCCEEDING", "“I prepared well”", "DISPOSITIONAL",
         "self-serving bias, esteem up", SAGE),
        ("YOU, after FAILING", "“the test was unfair”", "SITUATIONAL",
         "self-serving bias, esteem defended", GOLD)]
x = 70
for who, quote, kind, name, col in quad:
    d.rect(x, 286, 186, 150, col, FILL[col], rx=9, width=1.8)
    d.text(x + 93, 310, who, color=col, weight="bold", size=10)
    d.text(x + 93, 336, quote, color=NAVY, weight="bold", size=10.5)
    d.rect(x + 28, 350, 130, 24, col, "none", rx=5, width=1.4)
    d.text(x + 93, 366, kind, color=col, weight="bold", size=9.5)
    for j, ln in enumerate(name.split(", ")):
        d.text(x + 93, 394 + j * 14, ln, color=GREY, size=9)
    x += 198

d.text(460, 466, "the person is salient when you watch; the situation is salient when you live it",
       color=NAVY, weight="bold", size=11.5)
d.text(460, 486, "collectivist cultures show the tilt more weakly, and sometimes reverse the self-serving half",
       color=GREY, size=10)

# ---------------- Panel B: Kelley ----------------
d.rect(40, 514, 410, 464, BLUE, "none", rx=12, width=2)
d.text(245, 542, "Kelley's three dials", color=BLUE, weight="bold", size=15)

dials = [("CONSENSUS", "do OTHERS do it too?"),
         ("DISTINCTIVENESS", "do they do it ONLY here?"),
         ("CONSISTENCY", "do they do it EVERY time?")]
y = 566
for name, q in dials:
    d.rect(64, y, 362, 44, BLUE, FILL[BLUE], rx=7, width=1.5)
    d.text(245, y + 20, name, color=BLUE, weight="bold", size=11)
    d.text(245, y + 36, q, color=GREY, size=9.5)
    y += 50

d.rect(64, 724, 362, 108, SAGE, FILL[SAGE], rx=9, width=2)
d.text(245, 748, "HIGH · HIGH · HIGH", color=SAGE, weight="bold", size=13)
d.text(245, 768, "everyone does it, only here, every time", color=NAVY, size=10)
d.text(245, 794, "→ SITUATIONAL", color=SAGE, weight="bold", size=13)
d.text(245, 814, "the cause is the thing, not the person", color=GREY, size=9.5)

d.rect(64, 844, 362, 108, RED, FILL[RED], rx=9, width=2)
d.text(245, 868, "LOW · LOW · HIGH", color=RED, weight="bold", size=13)
d.text(245, 888, "only they do it, everywhere, every time", color=NAVY, size=10)
d.text(245, 914, "→ DISPOSITIONAL", color=RED, weight="bold", size=13)
d.text(245, 934, "the cause is the person", color=GREY, size=9.5)

# ---------------- Panel C: inference biases ----------------
d.rect(470, 514, 410, 464, GOLD, "none", rx=12, width=2)
d.text(675, 542, "What counts for too much", color=GOLD, weight="bold", size=15)

bias = [("PRIMACY", "what came FIRST", "early traits set the lens the rest is read through", GOLD),
        ("ANCHORING", "the FIRST number or impression",
         "later information adjusts it, never enough — which is\nwhy a first impression survives contrary evidence", GOLD),
        ("AVAILABILITY", "what comes to MIND easiest",
         "vivid and recent feels frequent", BLUE),
        ("REPRESENTATIVENESS", "what RESEMBLES the prototype",
         "fits the picture, so base rates get ignored", BLUE),
        ("HALO", "one GOOD thing, globally",
         "a positive evaluation spills into unrelated domains", SAGE),
        ("IMPLICIT PERSONALITY THEORY", "which traits you think TRAVEL together",
         "the lay belief that warm people are also generous", SAGE),
        ("CONFIRMATION", "what AGREES with you already",
         "and acting on it makes others confirm it", RED)]
y = 566
for name, tag, note, col in bias:
    lines = note.split("\n")
    h = 36 + len(lines) * 13
    d.rect(494, y, 362, h, col, FILL[col], rx=7, width=1.5)
    d.text(675, y + 17, name, color=col, weight="bold", size=10.5)
    d.text(675, y + 32, tag, color=NAVY, size=9.5)
    for j, ln in enumerate(lines):
        d.text(675, y + 46 + j * 13, ln, color=GREY, size=9)
    y += h + 7

d.save("attribution-seats-kelley-dials-and-inference-biases")
print("ok")
