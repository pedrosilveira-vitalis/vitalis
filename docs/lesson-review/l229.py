import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 930,
      "Four biases, two axes, one grid",
      "Whose behaviour, and whether it went well — that is all that separates them",
      "Top: the four attribution biases laid out on the two axes that actually distinguish them. Across the "
      "top, whose behaviour is being explained; down the side, how it turned out. The fundamental attribution "
      "error lives in the “other person” column and does not care about the outcome. The actor-observer bias is "
      "the contrast between the two columns. The self-serving bias is the contrast between the two rows within "
      "the self column. The ultimate attribution error is the same grid re-drawn with in-group and out-group in "
      "place of self and other, which is what makes it the socially dangerous one. Bottom: the single question "
      "that identifies which bias a vignette is testing, and what reliably weakens each."
      )

# ---------------- Panel A: the grid ----------------
d.rect(40, 180, 840, 372, NAVY, "none", rx=12, width=2)
d.text(460, 208, "The grid that separates them", color=NAVY, weight="bold", size=15)

d.rect(300, 228, 270, 34, GREY, FILL[GREY], rx=7, width=1.5)
d.text(435, 250, "MY OWN behaviour", color=NAVY, weight="bold", size=11.5)
d.rect(580, 228, 270, 34, GREY, FILL[GREY], rx=7, width=1.5)
d.text(715, 250, "SOMEONE ELSE'S", color=NAVY, weight="bold", size=11.5)

cells = [("IT WENT WELL", SAGE,
          ("“I am skilled”", "DISPOSITIONAL", SAGE),
          ("“they got lucky”", "SITUATIONAL", GOLD)),
         ("IT WENT BADLY", RED,
          ("“the situation was against me”", "SITUATIONAL", BLUE),
          ("“that is who they are”", "DISPOSITIONAL", RED))]
y = 272
for rowname, rowcol, left, right in cells:
    d.rect(70, y, 220, 108, rowcol, FILL[rowcol], rx=8, width=1.8)
    d.text(180, y + 60, rowname, color=rowcol, weight="bold", size=12.5)
    for (quote, kind, col), x in ((left, 300), (right, 580)):
        d.rect(x, y, 270, 108, col, FILL[col], rx=8, width=1.8)
        d.text(x + 135, y + 42, quote, color=NAVY, weight="bold", size=11)
        d.rect(x + 70, y + 58, 130, 26, col, "none", rx=5, width=1.5)
        d.text(x + 135, y + 76, kind, color=col, weight="bold", size=10)
    y += 118

d.text(460, 518, "left column vs right column = ACTOR-OBSERVER · top row vs bottom row on the left = SELF-SERVING",
       color=NAVY, weight="bold", size=10.5)
d.text(460, 538, "the right column on its own = FUNDAMENTAL ATTRIBUTION ERROR · swap self and other for in-group and out-group = ULTIMATE",
       color=GREY, size=9.5)

# ---------------- Panel B: identify it ----------------
d.rect(40, 568, 410, 346, GOLD, "none", rx=12, width=2)
d.text(245, 596, "Which one is the vignette testing?", color=GOLD, weight="bold", size=14)

qs = [("Is a GROUP named,\nand treated as a group?", "YES → ULTIMATE ATTRIBUTION ERROR", RED),
      ("Is the SAME person's success\nand failure both described?", "YES → SELF-SERVING BIAS", SAGE),
      ("Are self and other\nexplained SIDE BY SIDE?", "YES → ACTOR-OBSERVER BIAS", BLUE),
      ("Only one person judged,\nsituation ignored?", "YES → FUNDAMENTAL ATTRIBUTION ERROR", GOLD)]
y = 618
for q, ans, col in qs:
    d.rect(64, y, 362, 68, col, FILL[col], rx=8, width=1.6)
    for j, ln in enumerate(q.split("\n")):
        d.text(245, y + 20 + j * 14, ln, color=NAVY, weight="bold", size=10)
    d.text(245, y + 58, ans, color=col, weight="bold", size=10)
    y += 74

# ---------------- Panel C: what weakens them ----------------
d.rect(470, 568, 410, 346, SAGE, "none", rx=12, width=2)
d.text(675, 596, "What actually weakens them", color=SAGE, weight="bold", size=14)

fixes = [("PERSPECTIVE-TAKING", "deliberately occupying the other person's\nposition; Storms reversed the bias with a camera", BLUE),
         ("ACCOUNTABILITY · TIME", "the correction step is effortful, so it fails\nunder load and returns when resources allow", GOLD),
         ("INDIVIDUATING INFORMATION", "specific facts about the person crowd out\nthe category-based reading", SAGE),
         ("INTERGROUP CONTACT", "Allport's conditions: equal status, common\ngoals, cooperation, institutional support", RED)]
y = 618
for name, note, col in fixes:
    d.rect(494, y, 362, 60, col, FILL[col], rx=8, width=1.6)
    d.text(675, y + 20, name, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(note.split("\n")):
        d.text(675, y + 36 + j * 13, ln, color=GREY, size=9)
    y += 66

d.text(675, 892, "knowing about a bias does not remove it — that is the bias blind spot",
       color=NAVY, weight="bold", size=10)

d.save("attribution-bias-grid-identification-and-remedies")
print("ok")
