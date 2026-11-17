import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 960,
      "Three institutions, one question asked three ways",
      "What does it do for society, whose interests does it serve, and how is it lived?",
      "Top: family, education and religion read through each of the three frameworks. The grid is the point — "
      "a passage is almost never asking which institution is involved, it is asking which reading of it the "
      "author has adopted. Functionalism names the need the institution meets. Conflict theory asks who the "
      "arrangement benefits and finds that advantage is handed down. Symbolic interactionism drops to the "
      "level of the classroom, the dinner table and the ritual. Bottom left: the religious organisation types, "
      "ordered by how much tension each has with the surrounding society. Bottom right: the health "
      "associations, which is where this material usually enters a question."
      )

# ---------------- Panel A: the grid ----------------
d.rect(40, 180, 840, 420, NAVY, "none", rx=12, width=2)
d.text(460, 208, "The grid the exam is really testing", color=NAVY, weight="bold", size=15)

heads = [("FUNCTIONALIST", "what need does it meet?", SAGE),
         ("CONFLICT", "who does it serve?", RED),
         ("INTERACTIONIST", "how is it lived?", BLUE)]
cx = 262
for name, q, col in heads:
    d.rect(cx, 226, 200, 38, col, FILL[col], rx=7, width=1.6)
    d.text(cx + 100, 244, name, color=col, weight="bold", size=10.5)
    d.text(cx + 100, 258, q, color=GREY, size=8.5)
    cx += 205

rows = [("FAMILY", GOLD,
         "reproduction, primary\nsocialization, status;\nParsons's instrumental\nand expressive roles",
         "hands down economic,\ncultural and social\ncapital; Engels on\ninheritance",
         "the looking-glass self;\nfamily labels become\nself-concept"),
        ("EDUCATION", BLUE,
         "integration, placement,\ninnovation; Durkheim on\nshared values",
         "social reproduction;\nBourdieu — schools reward\nthe capital the privileged\nalready arrive with",
         "teacher expectations;\nPygmalion and the\nself-fulfilling prophecy"),
        ("RELIGION", RED,
         "cohesion, meaning,\ncontrol, support;\nDurkheim's sacred\nand profane",
         "Marx: the opium of the\npeople — though liberation\ntheology cuts the other\nway",
         "ritual makes shared\nsymbols; conversion\nremakes identity")]
y = 274
for name, col, f, c, s in rows:
    d.rect(60, y, 190, 94, col, FILL[col], rx=8, width=1.8)
    d.text(155, y + 53, name, color=col, weight="bold", size=13)
    cx = 262
    for text, hcol in ((f, SAGE), (c, RED), (s, BLUE)):
        d.rect(cx, y, 200, 94, hcol, FILL[hcol], rx=8, width=1.4)
        for j, ln in enumerate(text.split("\n")):
            d.text(cx + 100, y + 22 + j * 14, ln, color=NAVY, size=8.5)
        cx += 205
    y += 102

d.text(460, 590, "and Bellah's CIVIL RELIGION applies the religious reading to secular ritual — flags, anthems, founding stories",
       color=NAVY, weight="bold", size=9.5)

# ---------------- Panel B: organisation types ----------------
d.rect(40, 616, 410, 326, SAGE, "none", rx=12, width=2)
d.text(245, 644, "Ordered by tension with society", color=SAGE, weight="bold", size=14)

orgs = [("ECCLESIA", "a state church; membership by birth", SAGE),
        ("DENOMINATION", "one church among several, accepted\nand accommodated", SAGE),
        ("SECT", "broke away from a church; stricter,\nconversion-based, keeps its distance", GOLD),
        ("NEW RELIGIOUS MOVEMENT", "novel beliefs, often a charismatic\nfounder, high tension — the word “cult”\ncarries judgement, so sociologists avoid it", RED)]
y = 666
for name, note, col in orgs:
    lines = note.split("\n")
    h = 30 + len(lines) * 13
    d.rect(64, y, 362, h, col, FILL[col], rx=8, width=1.6)
    d.text(245, y + 18, name, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(lines):
        d.text(245, y + 33 + j * 13, ln, color=GREY, size=8.5)
    y += h + 8

d.text(245, 928, "low tension at the top, high tension at the bottom", color=NAVY, weight="bold", size=9.5)

# ---------------- Panel C: health links ----------------
d.rect(470, 616, 410, 326, BLUE, "none", rx=12, width=2)
d.text(675, 644, "Where this enters a health question", color=BLUE, weight="bold", size=14)

links = [("EDUCATION", "the strongest single social predictor of\nhealth — via income, literacy and control", BLUE),
         ("MARRIAGE AND FAMILY", "lower mortality and depression; support\nblunts the cortisol response — but quality\nmatters, and the effect is larger for men", GOLD),
         ("RELIGIOUS ATTENDANCE", "lower all-cause mortality, partly through\ndense social support and health norms;\nAdventists are the natural experiment", SAGE),
         ("AND THE OTHER DIRECTION", "prayer substituted for care, shame around\nillness, refusal of specific treatments — take\na spiritual history rather than assuming", RED)]
y = 666
for name, note, col in links:
    lines = note.split("\n")
    h = 28 + len(lines) * 13
    d.rect(494, y, 362, h, col, FILL[col], rx=8, width=1.6)
    d.text(675, y + 17, name, color=col, weight="bold", size=10)
    for j, ln in enumerate(lines):
        d.text(675, y + 31 + j * 13, ln, color=GREY, size=8.5)
    y += h + 8

d.save("three-institutions-three-frameworks-and-health")
print("ok")
