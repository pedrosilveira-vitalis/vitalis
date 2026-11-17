import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 900,
      "Who is teaching you, and what kind of lesson is it?",
      "The agent changes with age; the type of socialization changes with the role",
      "Top: the agents ranked by when they dominate. Family first and deepest, because primary socialization "
      "happens while the child has no alternative frame of reference; peers at their peak in adolescence, when "
      "identity is the developmental task; school, media, work and religion overlapping throughout. Middle: "
      "Mead's three stages, which are tested as a sequence and are easy to confuse — imitation before "
      "role-taking, role-taking before grasping that all the roles interlock. Bottom: the four types of "
      "socialization named in the exam's vocabulary, separated by one question — are you learning a role you "
      "do not yet hold, adding one, replacing your identity, or leaving a role behind."
      )

# ---------------- Panel A: agents by life stage ----------------
d.rect(40, 180, 840, 212, NAVY, "none", rx=12, width=2)
d.text(460, 208, "When each agent dominates", color=NAVY, weight="bold", size=15)

x0, x1 = 150, 850
d.line(x0, 362, x1, 362, GREY, 1.6)
for px, lab in [(x0, "birth"), (x0 + 160, "school age"), (x0 + 330, "adolescence"),
                (x0 + 510, "adulthood"), (x1, "later life")]:
    d.line(px, 356, px, 368, GREY, 1.4)
    d.text(px, 384, lab, color=NAVY, weight="bold", size=9)

bars = [("FAMILY", 0, 700, 232, RED, "primary socialization — language, values, class, attachment"),
        ("PEERS", 120, 460, 258, GOLD, "peaks in adolescence; identity is negotiated here"),
        ("SCHOOL", 150, 420, 284, BLUE, "and its hidden curriculum: authority, time, competition"),
        ("MEDIA", 60, 700, 310, SAGE, "representation, modelling, cultivation"),
        ("WORK", 480, 700, 336, GREY, "occupational socialization")]
for name, start, end, y, col, note in bars:
    d.rect(x0 + start, y, end - start, 20, col, FILL[col], rx=4, width=1.4)
    d.text(x0 + start + 8, y + 15, name, anchor="start", color=col, weight="bold", size=9)
    d.text(142, y + 15, "", anchor="end", color=GREY, size=8)
    d.text(x0 + end - 8, y + 15, note, anchor="end", color=GREY, size=8)

# ---------------- Panel B: Mead's stages ----------------
d.rect(40, 408, 840, 166, GOLD, "none", rx=12, width=2)
d.text(460, 436, "Mead's three stages, in order", color=GOLD, weight="bold", size=15)

stages = [("PREPARATORY", "under about 2", "imitation without understanding —\ncopying the act, not the role", GREY),
          ("PLAY", "about 2 to 6", "takes ONE role at a time:\nplaying doctor, playing parent", GOLD),
          ("GAME", "about 7 and up", "holds SEVERAL roles at once and\nsees how they interlock — the\ngeneralized other", SAGE)]
cx = 68
for name, age, note, col in stages:
    d.rect(cx, 456, 262, 100, col, FILL[col], rx=9, width=1.8)
    d.text(cx + 131, 478, name, color=col, weight="bold", size=12)
    d.text(cx + 131, 494, age, color=NAVY, size=9)
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 131, 512 + j * 13, ln, color=GREY, size=8.5)
    cx += 276
for ax in (336, 612):
    d.arrow(ax, 506, ax + 18, 506, GREY)

# ---------------- Panel C: four types ----------------
d.rect(40, 590, 840, 290, SAGE, "none", rx=12, width=2)
d.text(460, 618, "Four types, told apart by one question", color=SAGE, weight="bold", size=15)
d.text(460, 640, "what is happening to the role you hold?", color=GREY, size=10)

types_ = [("ANTICIPATORY", "rehearsing a role you do NOT yet hold", BLUE,
           ["the pre-med who already talks like",
            "a clinician; reading about parenthood",
            "before the child arrives",
            "",
            "it SMOOTHS the transition"]),
          ("DEVELOPMENTAL", "ADDING a role as life moves on", SAGE,
           ["student, then worker, then spouse,",
            "then parent, then retiree",
            "",
            "each brings new expectations and",
            "a new reference group"]),
          ("RESOCIALIZATION", "REPLACING the identity you had", RED,
           ["boot camp, prison, a religious order",
            "— Goffman's total institutions",
            "",
            "mortification of the self first,",
            "then a new identity built"]),
          ("ROLE EXIT", "LEAVING a role that defined you", GOLD,
           ["retirement, widowhood, leaving a",
            "profession or a faith (Ebaugh)",
            "",
            "the hard part is rebuilding identity",
            "once the role is gone"])]
cx = 56
for name, tag, col, lines in types_:
    d.rect(cx, 660, 200, 194, col, FILL[col], rx=10, width=2)
    d.text(cx + 100, 684, name, color=col, weight="bold", size=11)
    d.text(cx + 100, 704, tag, color=NAVY, weight="bold", size=8.5)
    d.line(cx + 24, 716, cx + 176, 716, col, 1, dash="3,3")
    for j, ln in enumerate(lines):
        if not ln:
            continue
        d.text(cx + 100, 738 + j * 17, ln, color=NAVY if j == 4 else GREY,
               weight="bold" if j == 4 else "normal", size=8.5)
    cx += 205

d.save("socialization-agents-mead-stages-and-four-types")
print("ok")
