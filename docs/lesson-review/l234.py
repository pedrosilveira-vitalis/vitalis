import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 960,
      "Three words, four levels, one set of defences",
      "Thought, feeling, action — and the machinery that keeps all three in place",
      "Top: the tripartite structure the exam insists on. A stereotype is the belief, prejudice is the feeling, "
      "discrimination is the act, and the links between them are loose in both directions: someone can be "
      "prejudiced without discriminating, and an institution can discriminate with nobody in it prejudiced. "
      "Middle: the four levels at which an explanation can sit. A question is usually asking you to pick the "
      "level, not just the term — cognitive shortcuts, the need for a good group to belong to, personality and "
      "ideology, or structure and policy. Bottom: why counter-evidence so rarely lands. Subtyping files the "
      "exception away, the ultimate attribution error explains it away, and contact only works under Allport's "
      "four conditions."
      )

# ---------------- Panel A: three words ----------------
d.rect(40, 180, 840, 182, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Belief, feeling, act", color=NAVY, weight="bold", size=15)

trio = [("STEREOTYPE", "COGNITIVE", "a belief about what\nmembers of a group are like", BLUE),
        ("PREJUDICE", "AFFECTIVE", "an attitude — how you feel\nabout them, before meeting one", GOLD),
        ("DISCRIMINATION", "BEHAVIOURAL", "treating someone differently\nbecause of their group", RED)]
cx = 70
for name, kind, note, col in trio:
    d.rect(cx, 228, 230, 100, col, FILL[col], rx=10, width=2)
    d.text(cx + 115, 252, name, color=col, weight="bold", size=12.5)
    d.text(cx + 115, 270, kind, color=NAVY, weight="bold", size=10)
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 115, 292 + j * 14, ln, color=GREY, size=9.5)
    cx += 260
for ax in (306, 566):
    d.arrow(ax, 278, 326 if ax == 306 else 586, 278, GREY)

d.text(460, 350, "the arrows are weak both ways: prejudice without discrimination, and discrimination without prejudice",
       color=NAVY, weight="bold", size=10)

# ---------------- Panel B: four levels ----------------
d.rect(40, 378, 840, 288, GOLD, "none", rx=12, width=2)
d.text(460, 406, "Four levels an explanation can sit at", color=GOLD, weight="bold", size=15)

levels = [("COGNITIVE", "the mind takes shortcuts", BLUE,
           ["social categorisation", "accentuation and out-group",
            "homogeneity", "illusory correlation",
            "schemas, availability"]),
          ("MOTIVATIONAL", "the group props up the self", GOLD,
           ["social identity theory", "minimal group paradigm",
            "realistic group conflict", "terror management",
            "scapegoating under frustration"]),
          ("PERSONALITY", "some people more than others", SAGE,
           ["right-wing authoritarianism", "social dominance orientation",
            "legitimising myths", "just-world belief",
            "and the victim-blaming it brings"]),
          ("STRUCTURAL", "nobody has to be a bigot", RED,
           ["institutional discrimination", "neutral policy, disparate impact",
            "sentencing, school funding,", "algorithms trained on old data",
            "intersectional compounding"])]
cx = 60
for name, tag, col, items in levels:
    d.rect(cx, 426, 200, 220, col, FILL[col], rx=9, width=1.8)
    d.text(cx + 100, 450, name, color=col, weight="bold", size=11.5)
    d.text(cx + 100, 468, tag, color=NAVY, size=9)
    d.line(cx + 22, 480, cx + 178, 480, col, 1, dash="3,3")
    for j, ln in enumerate(items):
        d.text(cx + 100, 502 + j * 18, ln, color=GREY, size=9)
    cx += 205

# ---------------- Panel C: why it persists ----------------
d.rect(40, 682, 410, 258, RED, "none", rx=12, width=2)
d.text(245, 710, "Why counter-evidence bounces off", color=RED, weight="bold", size=14)

why = [("SUBTYPING", "the exception gets its own box — “she's not\nlike the others” — and the rule survives", RED),
       ("ULTIMATE ATTRIBUTION ERROR", "out-group success is luck, out-group failure\nis character; reversed for the in-group", GOLD),
       ("CONFIRMATION BIAS", "the fitting case is noticed and remembered,\nthe misfitting one is not", BLUE)]
y = 730
for name, note, col in why:
    d.rect(64, y, 362, 62, col, FILL[col], rx=8, width=1.6)
    d.text(245, y + 21, name, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(note.split("\n")):
        d.text(245, y + 38 + j * 13, ln, color=GREY, size=9)
    y += 68

# ---------------- Panel D: contact ----------------
d.rect(470, 682, 410, 258, SAGE, "none", rx=12, width=2)
d.text(675, 710, "Contact, but only on four conditions", color=SAGE, weight="bold", size=14)

conds = ["EQUAL STATUS inside the contact situation",
         "COMMON GOALS that neither group reaches alone",
         "COOPERATION, not competition",
         "INSTITUTIONAL SUPPORT from those in charge"]
y = 732
for i, c in enumerate(conds):
    d.rect(494, y, 362, 36, SAGE, FILL[SAGE], rx=7, width=1.5)
    d.text(675, y + 23, c, color=NAVY, weight="bold", size=10)
    y += 42

d.text(675, 906, "without them, contact can entrench the stereotype instead",
       color=RED, weight="bold", size=10)
d.text(675, 926, "superordinate goals work by recategorising: one group, not two", color=GREY, size=9.5)

d.save("prejudice-structure-levels-and-persistence")
print("ok")
