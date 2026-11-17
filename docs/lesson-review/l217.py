import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 916,
      "Three answers to what a person is made of",
      "Freud says conflict, Rogers says conditions, Bandura says a loop",
      "Top: the three frameworks set against each other on the questions that separate them — what drives "
      "behaviour, how good human nature is taken to be, and whether the theory can actually be tested. Middle: "
      "Rogers in detail, because his machinery is the most often muddled. A child meets conditional regard, "
      "takes on conditions of worth, and starts editing the self-concept to fit them; the edited self-concept "
      "then drifts away both from the ideal self and from what the child actually experiences and values, and "
      "that gap is the distress. Bottom left: the defence mechanisms that vignettes test, grouped so the "
      "confusable pairs sit together. Bottom right: Bandura's loop and the four sources of self-efficacy, in "
      "order of strength."
      )

# ---------------- Panel A: comparison ----------------
d.rect(40, 180, 840, 170, BLUE, "none", rx=12, width=2)
d.text(460, 208, "The three frameworks, on what divides them", color=BLUE, weight="bold", size=16)

cols = [
    ("PSYCHODYNAMIC", "Freud", "unconscious conflict", "human nature: conflicted", "testability: low", GREY),
    ("HUMANISTIC", "Rogers, Maslow", "an innate push to grow", "human nature: good", "testability: low", SAGE),
    ("SOCIAL-COGNITIVE", "Bandura", "beliefs and observation", "human nature: neutral", "testability: high", BLUE),
]
x = 66
for name, who, driver, nature, test, col in cols:
    d.rect(x, 226, 258, 108, col, FILL[col], rx=10, width=2)
    d.text(x + 129, 250, name, color=col, weight="bold", size=13)
    d.text(x + 129, 270, who, color=GREY, size=11)
    d.text(x + 129, 292, driver, color=NAVY, weight="bold", size=12)
    d.text(x + 129, 312, nature, color=GREY, size=10)
    d.text(x + 129, 326, test, color=GREY, size=10)
    x += 274

# ---------------- Panel B: Rogers chain ----------------
d.rect(40, 370, 840, 196, GOLD, "none", rx=12, width=2)
d.text(460, 398, "Rogers, in the order it actually happens", color=GOLD, weight="bold", size=16)

chain = [
    ("conditional regard", "loved IF you perform", GOLD),
    ("conditions of worth", "“only valuable if…”", GOLD),
    ("self-concept distorts", "to fit the conditions", RED),
    ("INCONGRUENCE", "with the ideal self, and\nwith what you really value", RED),
]
x = 66
for name, note, col in chain:
    d.rect(x, 418, 188, 86, col, FILL[col], rx=9, width=2)
    d.text(x + 94, 446, name, color=col, weight="bold", size=12)
    lines = note.split("\n")
    if len(lines) == 1:
        d.text(x + 94, 472, lines[0], color=GREY, size=11)
    else:
        d.text(x + 94, 466, lines[0], color=GREY, size=10)
        d.text(x + 94, 482, lines[1], color=GREY, size=10)
    if x < 600:
        d.arrow(x + 188, 461, x + 196, 461, GREY, width=1.8)
    x += 196

d.text(460, 530, "the cure runs backwards: unconditional positive regard · empathy · genuineness",
       color=SAGE, weight="bold", size=13)
d.text(460, 550, "remove the conditions and the actualising tendency does the rest",
       color=GREY, size=11)

# ---------------- Panel C: defences ----------------
d.rect(40, 586, 470, 304, RED, "none", rx=12, width=2)
d.text(275, 614, "The pairs that get confused", color=RED, weight="bold", size=15)

pairs = [
    ("REPRESSION", "pushed out, unconsciously", "SUPPRESSION", "pushed out, on purpose"),
    ("PROJECTION", "my feeling, attributed to you", "REACTION FORMATION", "my feeling, flipped in me"),
    ("DISPLACEMENT", "same feeling, safer target", "SUBLIMATION", "redirected into something useful"),
    ("REGRESSION", "retreat to an earlier age", "INTELLECTUALISATION", "all facts, no feeling"),
]
y = 636
for a, ad, b, bd in pairs:
    d.rect(66, y, 200, 52, RED, FILL[RED], rx=8, width=1.8)
    d.text(166, y + 21, a, color=RED, weight="bold", size=11)
    d.text(166, y + 38, ad, color=GREY, size=10)
    d.rect(284, y, 200, 52, BLUE, FILL[BLUE], rx=8, width=1.8)
    d.text(384, y + 21, b, color=BLUE, weight="bold", size=11)
    d.text(384, y + 38, bd, color=GREY, size=10)
    y += 58

d.text(275, 880, "sublimation is the mature one", color=NAVY, weight="bold", size=11)

# ---------------- Panel D: Bandura ----------------
d.rect(530, 586, 350, 304, SAGE, "none", rx=12, width=2)
d.text(705, 614, "Bandura's loop", color=SAGE, weight="bold", size=15)

d.circle(705, 668, 24, NAVY, "#dde4ea", width=2)
d.text(705, 673, "P", color=NAVY, weight="bold", size=16)
d.text(705, 636, "person · beliefs", color=NAVY, size=10)
d.circle(620, 726, 24, SAGE, FILL[SAGE], width=2)
d.text(620, 731, "B", color=SAGE, weight="bold", size=16)
d.text(600, 760, "behaviour", anchor="middle", color=SAGE, size=10)
d.circle(790, 726, 24, GOLD, FILL[GOLD], width=2)
d.text(790, 731, "E", color=GOLD, weight="bold", size=16)
d.text(810, 760, "environment", anchor="middle", color=GOLD, size=10)

d.path("M686 684 q-34 14 -46 24", GREY, 2, "none")
d.path("M644 718 q40 -34 40 -34", GREY, 2, "none")
d.line(644, 726, 766, 726, GREY, 2)
d.path("M724 684 q34 14 46 24", GREY, 2, "none")
d.text(705, 790, "each one changes the other two", color=NAVY, weight="bold", size=11)

d.text(705, 820, "self-efficacy, strongest source first:", color=GREY, weight="bold", size=11)
d.text(705, 840, "mastery → vicarious → persuasion → arousal", color=NAVY, weight="bold", size=11)
d.text(705, 862, "domain-specific — not the same as self-esteem", color=GREY, size=10)

d.save("three-personality-frameworks-rogers-and-bandura")
print("ok")
