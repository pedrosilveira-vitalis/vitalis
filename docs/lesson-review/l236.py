import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 972,
      "Five gates between an emergency and a helping hand",
      "Each one can close on its own, and two of them close because other people are there",
      "Top: Latané and Darley's decision model as five gates in series. Help happens only if all five open; a "
      "failure at any one ends the sequence. The two gates the exam cares about are the second and the third, "
      "because they fail for different reasons and get confused with one another. At gate two the bystander "
      "does not know an emergency is happening, because everyone else looks calm — pluralistic ignorance. At "
      "gate three the bystander knows perfectly well and still does not move, because somebody else will — "
      "diffusion of responsibility. Bottom left: the numbers from the two studies that established the effect. "
      "Bottom right: what reopens the gates, and the aggression counterpart where the same situational logic "
      "runs the other way."
      )

# ---------------- Panel A: five gates ----------------
d.rect(40, 180, 840, 322, NAVY, "none", rx=12, width=2)
d.text(460, 208, "All five, in order", color=NAVY, weight="bold", size=15)

gates = [("1", "NOTICE IT", "attention; a crowded, hurried\nstreet can end it right here", GREY,
          "distraction, time pressure"),
         ("2", "READ IT AS\nAN EMERGENCY", "everyone else looks calm, so\nit must be nothing", GOLD,
          "PLURALISTIC IGNORANCE"),
         ("3", "FEEL\nRESPONSIBLE", "it is an emergency — and\nsomeone else will handle it", RED,
          "DIFFUSION OF RESPONSIBILITY"),
         ("4", "KNOW HOW\nTO HELP", "no competence, or fear of\nlooking incompetent", BLUE,
          "audience inhibition"),
         ("5", "ACTUALLY\nDO IT", "decided to help, then hesitated\nunder the watching eyes", SAGE,
          "evaluation apprehension")]
cx = 56
for num, name, note, col, failure in gates:
    d.rect(cx, 228, 162, 200, col, FILL[col], rx=9, width=1.8)
    d.text(cx + 81, 252, num, color=col, weight="bold", size=16)
    lines = name.split("\n")
    for j, ln in enumerate(lines):
        d.text(cx + 81, 274 + j * 14, ln, color=NAVY, weight="bold", size=10.5)
    d.line(cx + 20, 308, cx + 142, 308, col, 1, dash="3,3")
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 81, 328 + j * 13, ln, color=GREY, size=8.5)
    d.rect(cx + 8, 368, 146, 46, col, "none", rx=6, width=1.5)
    for j, ln in enumerate(failure.split(" ", 1) if len(failure) > 24 else [failure]):
        d.text(cx + 81, 386 + j * 13, ln, color=col, weight="bold", size=8.5)
    cx += 170
for ax in (222, 392, 562, 732):
    d.arrow(ax, 328, ax + 10, 328, GREY, width=1.6)

d.text(460, 450, "gate 2 fails because the bystander does not KNOW; gate 3 fails although they do",
       color=NAVY, weight="bold", size=11.5)
d.text(460, 472, "both are caused by other people being present — that is why they get confused",
       color=GREY, size=10)

# ---------------- Panel B: the numbers ----------------
d.rect(40, 518, 410, 436, RED, "none", rx=12, width=2)
d.text(245, 546, "The two founding studies", color=RED, weight="bold", size=14)

d.text(245, 572, "SEIZURE OVER THE INTERCOM", color=RED, weight="bold", size=11)
d.text(245, 588, "Darley and Latané, 1968 · helping by group size", color=GREY, size=9)
bars = [("alone", 85, 52, SAGE), ("one other", 62, 93, GOLD), ("four others", 31, 166, RED)]
y = 604
for lab, pct, secs, col in bars:
    d.text(130, y + 15, lab, anchor="end", color=NAVY, size=9.5)
    d.rect(140, y, pct * 2.6, 22, col, FILL[col], rx=4, width=1.5)
    d.text(146 + pct * 2.6, y + 16, "%d%%  ·  %ds" % (pct, secs), anchor="start",
           color=col, weight="bold", size=9.5)
    y += 30

d.line(80, 702, 410, 702, GREY, 1, dash="3,3")

d.text(245, 724, "THE SMOKE-FILLED ROOM", color=BLUE, weight="bold", size=11)
d.text(245, 740, "Latané and Darley, 1968 · reporting the smoke", color=GREY, size=9)
bars2 = [("alone", 75, SAGE), ("with two calm others", 10, RED)]
y = 756
for lab, pct, col in bars2:
    d.text(190, y + 15, lab, anchor="end", color=NAVY, size=9.5)
    d.rect(200, y, pct * 1.9, 22, col, FILL[col], rx=4, width=1.5)
    d.text(206 + pct * 1.9, y + 16, "%d%%" % pct, anchor="start", color=col, weight="bold", size=10)
    y += 30

d.rect(64, 826, 362, 110, NAVY, FILL[NAVY], rx=9, width=2)
d.text(245, 848, "AND THEY DID CARE", color=NAVY, weight="bold", size=11)
for j, ln in enumerate(["the bystanders who never helped were not",
                        "indifferent — they were visibly agitated,",
                        "asking whether the victim was all right.",
                        "The block was responsibility, not empathy."]):
    d.text(245, 868 + j * 16, ln, color=NAVY if j == 3 else GREY,
           weight="bold" if j == 3 else "normal", size=9)

# ---------------- Panel C: reopening the gates ----------------
d.rect(470, 518, 410, 436, SAGE, "none", rx=12, width=2)
d.text(675, 546, "What reopens them", color=SAGE, weight="bold", size=14)

fixes = [("MAKE IT UNAMBIGUOUS", "shout what is wrong; gate 2 opens", SAGE),
         ("NAME ONE PERSON", "“you, in the red jacket, call 911” —\ndiffusion cannot survive being named", SAGE),
         ("SMALLER GROUP", "fewer people, more felt responsibility", SAGE),
         ("COMPETENCE", "training removes gate 4", SAGE)]
y = 568
for name, note, col in fixes:
    lines = note.split("\n")
    h = 28 + len(lines) * 13
    d.rect(494, y, 362, h, col, FILL[col], rx=8, width=1.6)
    d.text(675, y + 18, name, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(lines):
        d.text(675, y + 33 + j * 13, ln, color=GREY, size=9)
    y += h + 7

d.line(510, 778, 840, 778, GREY, 1, dash="3,3")
d.text(675, 798, "THE SAME LOGIC, RUN THE OTHER WAY", color=RED, weight="bold", size=11)
agg = [("FRUSTRATION", "makes aggression possible, not certain"),
       ("AGGRESSIVE CUES", "a weapon in the room raises the odds"),
       ("MODELS", "Bobo doll \u2014 watched, learned, repeated"),
       ("REWARD OR PUNISHMENT", "changes PERFORMANCE, not LEARNING")]
y = 812
for name, note in agg:
    d.rect(494, y, 362, 30, RED, FILL[RED], rx=7, width=1.4)
    d.text(510, y + 19, name, anchor="start", color=RED, weight="bold", size=9)
    d.text(840, y + 19, note, anchor="end", color=GREY, size=8.5)
    y += 34

d.save("bystander-five-gates-numbers-and-remedies")
print("ok")
