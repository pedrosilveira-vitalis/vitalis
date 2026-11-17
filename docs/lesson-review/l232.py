import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 884,
      "What Milgram actually varied, and which way it moved",
      "Distance from the victim and distance from the authority push in opposite directions",
      "Top: the obedience rate across Milgram's conditions, drawn against the baseline of 65 per cent that "
      "came from the original study. The two proximity series are the ones to keep straight, because they move "
      "in opposite directions: putting the victim closer lowers obedience, putting the authority further away "
      "also lowers it. Everything else on the chart is a variation on legitimacy or on social support. Bottom "
      "left: the four mechanisms that hold a reluctant person in place. Bottom right: the three words that are "
      "constantly confused, separated by where the pressure comes from and whether anything was actually "
      "asked."
      )

# ---------------- Panel A: the bar chart ----------------
d.rect(40, 180, 840, 400, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Obedience by condition (% reaching 450 volts)", color=NAVY, weight="bold", size=15)

conds = [("BASELINE · Yale, learner unseen", 65.0, GREY),
         ("voice feedback through the wall", 62.5, GREY),
         ("learner in the SAME ROOM", 40.0, BLUE),
         ("hand forced onto the shock plate", 30.0, BLUE),
         ("moved to a run-down office", 47.5, GOLD),
         ("orders given by TELEPHONE", 20.5, RED),
         ("an ordinary man gives the orders", 20.0, RED),
         ("two peers REFUSE and walk out", 10.0, SAGE)]
x0 = 330
scale = 7.4
y = 236
for name, pct, col in conds:
    d.text(316, y + 15, name, anchor="end", color=NAVY, size=10)
    d.rect(x0, y, pct * scale, 22, col, FILL[col], rx=4, width=1.6)
    d.text(x0 + pct * scale + 10, y + 16, "%.1f%%" % pct, anchor="start",
           color=col, weight="bold", size=11)
    y += 30
d.line(x0, 230, x0, y - 4, GREY, 1.4)

d.text(460, 522, "VICTIM closer → obedience falls.  AUTHORITY further away → obedience falls.",
       color=NAVY, weight="bold", size=11.5)
d.text(460, 544, "and all 40 of the original participants went to at least 300 volts before anyone stopped",
       color=GREY, size=10)
d.text(460, 564, "psychiatrists asked beforehand predicted that barely one in a hundred would reach 450",
       color=GREY, size=10)

# ---------------- Panel B: mechanisms ----------------
d.rect(40, 596, 410, 266, RED, "none", rx=12, width=2)
d.text(245, 624, "What holds them in the chair", color=RED, weight="bold", size=14)

mech = [("AGENTIC STATE", "“I am not doing this — I am carrying it out”", RED),
        ("DIFFUSED RESPONSIBILITY", "the scientist is accountable, not me", GOLD),
        ("INCREMENTAL COMMITMENT", "15 volts at a time; stopping now admits\nthe last nineteen were wrong", BLUE),
        ("BINDING FACTORS", "politeness, momentum, and no script\nfor how to walk out", SAGE)]
y = 644
for name, note, col in mech:
    lines = note.split("\n")
    h = 40 if len(lines) == 1 else 52
    d.rect(64, y, 362, h, col, FILL[col], rx=8, width=1.6)
    d.text(245, y + 17, name, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(lines):
        d.text(245, y + 31 + j * 13, ln, color=GREY, size=9)
    y += h + 7

# ---------------- Panel C: three words ----------------
d.rect(470, 596, 410, 266, BLUE, "none", rx=12, width=2)
d.text(675, 624, "Three words, kept apart", color=BLUE, weight="bold", size=14)

words = [("OBEDIENCE", "an ORDER, from someone ABOVE you", "Milgram", RED),
         ("COMPLIANCE", "a REQUEST, from anyone at all", "foot-in-the-door", GOLD),
         ("CONFORMITY", "NO request — just what others are doing", "Asch", SAGE)]
y = 646
for name, note, study, col in words:
    d.rect(494, y, 362, 58, col, FILL[col], rx=8, width=1.8)
    d.text(675, y + 20, name, color=col, weight="bold", size=12)
    d.text(675, y + 36, note, color=NAVY, size=9.5)
    d.text(675, y + 51, study, color=GREY, size=9)
    y += 64

d.text(675, 852, "none of them requires believing it — that would be internalisation",
       color=NAVY, weight="bold", size=9.5)

d.save("milgram-conditions-mechanisms-and-three-words")
print("ok")
