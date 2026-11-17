import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 962,
      "Ten personality disorders, and one question that sorts them",
      "Does the trait feel right to the person, or wrong? That is where to start",
      "Top: the three clusters, with the signature feature that identifies each disorder in a vignette, and the "
      "pairs the exam deliberately confuses. Avoidant and schizoid both end up alone; only one of them wants "
      "company. Obsessive-compulsive personality disorder and obsessive-compulsive disorder share a name and "
      "almost nothing else. Bottom left: ego-syntonic against ego-dystonic, the distinction that explains who "
      "walks into a clinic voluntarily and who is brought in. Bottom right: the dissociation continuum, from "
      "ordinary daydreaming to dissociative identity disorder, with the point where reality testing is still "
      "intact marked, because that is what separates these disorders from psychosis."
      )

# ---------------- Panel A: clusters ----------------
d.rect(40, 180, 840, 300, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Three clusters · weird, wild, worried", color=NAVY, weight="bold", size=15)

cols = [
    ("A · ODD", "weird", BLUE,
     [("PARANOID", "reads malice into harmless remarks"),
      ("SCHIZOID", "does not want company at all"),
      ("SCHIZOTYPAL", "magical thinking, odd speech;\nruns in schizophrenia families")]),
    ("B · DRAMATIC", "wild", RED,
     [("ANTISOCIAL", "violates rights; conduct disorder\nbefore 15, diagnosed at 18+"),
      ("BORDERLINE", "splitting, abandonment, self-harm"),
      ("HISTRIONIC", "must be the centre of attention"),
      ("NARCISSISTIC", "grandiose, entitled, no empathy")]),
    ("C · ANXIOUS", "worried", SAGE,
     [("AVOIDANT", "wants company, fears rejection"),
      ("DEPENDENT", "needs others to decide for them"),
      ("OCPD", "perfectionism and control;\nfeels right to them")]),
]
cx = 68
for head, tag, col, items in cols:
    d.rect(cx, 228, 262, 234, col, "none", rx=10, width=2)
    d.text(cx + 131, 252, head, color=col, weight="bold", size=13)
    d.text(cx + 131, 270, tag, color=GREY, size=10)
    y = 282
    for name, note in items:
        lines = note.split("\n")
        h = 38 if len(lines) == 1 else 51
        d.rect(cx + 14, y, 234, h, col, FILL[col], rx=7, width=1.4)
        d.text(cx + 131, y + 16, name, color=col, weight="bold", size=10.5)
        for j, ln in enumerate(lines):
            d.text(cx + 131, y + 30 + j * 12, ln, color=GREY, size=9)
        y += h + 5
    cx += 276

# ---------------- Panel B: syntonic vs dystonic ----------------
d.rect(40, 496, 410, 444, GOLD, "none", rx=12, width=2)
d.text(245, 524, "The question to ask first", color=GOLD, weight="bold", size=15)

d.rect(64, 548, 362, 170, RED, FILL[RED], rx=10, width=2)
d.text(245, 574, "EGO-SYNTONIC", color=RED, weight="bold", size=14)
d.text(245, 594, "“this is simply who I am”", color=NAVY, size=11)
for j, ln in enumerate(["the trait fits the self-image and causes",
                        "the person no distress of its own",
                        "→ all ten personality disorders, and OCPD",
                        "→ brought in by someone else, if at all",
                        "→ low motivation, hard to treat"]):
    d.text(245, 618 + j * 18, ln, color=NAVY if j > 1 else GREY, size=9.5)

d.rect(64, 732, 362, 170, BLUE, FILL[BLUE], rx=10, width=2)
d.text(245, 758, "EGO-DYSTONIC", color=BLUE, weight="bold", size=14)
d.text(245, 778, "“this is not me, and I want it gone”", color=NAVY, size=11)
for j, ln in enumerate(["the symptom feels alien and unwanted,",
                        "and the distress is about the symptom itself",
                        "→ OCD obsessions, depression, panic",
                        "→ walks into the clinic on their own",
                        "→ motivation is already there"]):
    d.text(245, 802 + j * 18, ln, color=NAVY if j > 1 else GREY, size=9.5)

d.text(245, 924, "OCPD and OCD share a name, not a mechanism",
       color=GOLD, weight="bold", size=11)

# ---------------- Panel C: dissociation continuum ----------------
d.rect(470, 496, 410, 444, SAGE, "none", rx=12, width=2)
d.text(675, 524, "The dissociation continuum", color=SAGE, weight="bold", size=15)

steps = [("DAYDREAMING, HIGHWAY HYPNOSIS", "normal; most people, most weeks", GREY),
         ("DEPERSONALIZATION / DEREALIZATION", "detached from self or surroundings;\nreality testing INTACT — not psychosis", BLUE),
         ("DISSOCIATIVE AMNESIA", "cannot recall personal history;\nnew memories still form normally", GOLD),
         ("… with FUGUE", "travel or wandering, sometimes a new\nidentity; a specifier, not its own diagnosis", GOLD),
         ("DISSOCIATIVE IDENTITY DISORDER", "two or more identity states with\namnesia between them", RED)]
y = 548
for name, note, col in steps:
    lines = note.split("\n")
    h = 30 + len(lines) * 14
    d.rect(494, y, 362, h, col, FILL[col], rx=8, width=1.6)
    d.text(675, y + 18, name, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(lines):
        d.text(675, y + 33 + j * 14, ln, color=GREY, size=9)
    y += h + 8

d.text(675, 912, "severity rises; what is lost is integration —", color=NAVY, size=10)
d.text(675, 930, "of memory, identity, perception and sense of self", color=NAVY, size=10)

d.save("personality-clusters-ego-syntony-and-dissociation")
print("ok")
