import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 946,
      "One fact, three explanations",
      "The frameworks differ in what they look at, not only in what they conclude",
      "Top: the same observation — surgeons are paid far more than nurses — run through all three lenses. "
      "Functionalism asks what the arrangement does for the system and answers that unequal rewards staff the "
      "demanding posts. Conflict theory asks who set the rates and answers that those with power write the "
      "rules that keep them on top. Symbolic interactionism does not explain the origin at all; it asks how "
      "the difference is lived, in titles, deference and who gets interrupted on a ward round. Bottom left: "
      "the three-question triage that identifies which lens a passage is using. Bottom right: the vocabulary "
      "that belongs to each, which is how most questions are actually marked."
      )

# ---------------- Panel A: three lenses ----------------
d.rect(40, 180, 840, 330, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Why does the surgeon earn more than the nurse?", color=NAVY, weight="bold", size=15)

lenses = [("FUNCTIONALISM", "MACRO · stability", SAGE,
           "“the post is harder to fill”",
           ["unequal rewards draw talent into",
            "the demanding positions",
            "Davis and Moore, 1945",
            "",
            "CRITIQUE: who decides which",
            "posts are important? It reads",
            "today's pay as proof of worth,",
            "and ignores inherited advantage"]),
          ("CONFLICT THEORY", "MACRO · power", RED,
           "“the powerful set the rates”",
           ["inequality is an outcome of",
            "domination, not a solution",
            "Marx, Weber, Mills, Gramsci",
            "",
            "CRITIQUE: not every arrangement",
            "is exploitation, and if conflict",
            "runs that deep it is hard to",
            "explain why societies hold together"]),
          ("SYMBOLIC INTERACTIONISM", "MICRO · meaning", BLUE,
           "“watch the ward round”",
           ["who is addressed by title, who is",
            "interrupted, who is believed",
            "Mead, Cooley, Blumer, Goffman",
            "",
            "CRITIQUE: explains how it is",
            "lived, not where it came from;",
            "cannot by itself account for a",
            "population-wide disparity"])]
cx = 68
for name, level, col, quote, body in lenses:
    d.rect(cx, 228, 262, 266, col, FILL[col], rx=10, width=2)
    d.text(cx + 131, 252, name, color=col, weight="bold", size=11.5)
    d.text(cx + 131, 270, level, color=NAVY, weight="bold", size=9.5)
    d.text(cx + 131, 292, quote, color=col, weight="bold", size=10.5)
    d.line(cx + 30, 302, cx + 232, 302, col, 1, dash="3,3")
    for j, ln in enumerate(body):
        if not ln:
            continue
        d.text(cx + 131, 322 + j * 19, ln, color=NAVY if j > 3 else GREY,
               weight="bold" if j == 4 else "normal", size=9)
    cx += 276

# ---------------- Panel B: triage ----------------
d.rect(40, 526, 410, 398, GOLD, "none", rx=12, width=2)
d.text(245, 554, "Which lens is the passage using?", color=GOLD, weight="bold", size=14)

qs = [("Does it say the arrangement\nSERVES a need or keeps order?", "FUNCTIONALISM", SAGE),
      ("Does it name POWER, interests,\nexploitation or who benefits?", "CONFLICT THEORY", RED),
      ("Is it about MEANING, labels,\nidentity, or two people talking?", "SYMBOLIC INTERACTIONISM", BLUE)]
y = 578
for q, ans, col in qs:
    d.rect(64, y, 362, 86, col, FILL[col], rx=9, width=1.8)
    for j, ln in enumerate(q.split("\n")):
        d.text(245, y + 24 + j * 16, ln, color=NAVY, weight="bold", size=10)
    d.text(245, y + 70, "→ " + ans, color=col, weight="bold", size=11)
    y += 94

d.rect(64, 858, 362, 58, NAVY, FILL[NAVY], rx=9, width=2)
d.text(245, 879, "AND THE LEVEL GIVES IT AWAY", color=NAVY, weight="bold", size=10)
d.text(245, 899, "institutions and populations = macro · a conversation = micro", color=GREY, size=9)

# ---------------- Panel C: vocabulary ----------------
d.rect(470, 526, 410, 398, BLUE, "none", rx=12, width=2)
d.text(675, 554, "The words that mark each one", color=BLUE, weight="bold", size=14)

vocab = [("FUNCTIONALISM", SAGE,
          ["manifest and latent function", "dysfunction", "mechanical and organic solidarity",
           "anomie", "the sick role"]),
         ("CONFLICT THEORY", RED,
          ["bourgeoisie and proletariat", "surplus value", "false consciousness, hegemony",
           "power elite", "structural racism, intersectionality"]),
         ("SYMBOLIC INTERACTIONISM", BLUE,
          ["looking-glass self", "generalized other", "master status, labelling",
           "stigma: passing and covering", "dramaturgy, medicalization"])]
y = 576
for name, col, words in vocab:
    h = 30 + len(words) * 15
    d.rect(494, y, 362, h, col, FILL[col], rx=8, width=1.6)
    d.text(675, y + 19, name, color=col, weight="bold", size=10.5)
    for j, w in enumerate(words):
        d.text(675, y + 36 + j * 15, w, color=GREY, size=9)
    y += h + 8

d.save("three-lenses-on-inequality-triage-and-vocabulary")
print("ok")
