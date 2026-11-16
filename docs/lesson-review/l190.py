import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 884,
      "The same two conditioning laws, used on purpose",
      "Classical techniques re-pair a stimulus; operant techniques re-arrange consequences",
      "Top: anxiety plotted against time for the two exposure routes. Systematic desensitisation climbs a "
      "hierarchy while the patient stays relaxed, so anxiety stays low throughout; flooding presents the worst "
      "item at once and the patient waits out a single large spike. Both end at the same place, but flooding is "
      "harder to tolerate and more people drop out. Middle left: the three-term contingency with the operant "
      "techniques hung on it — antecedents are handled by prompting and fading, behaviour by shaping and "
      "chaining, consequences by reinforcement, extinction and response cost. Middle right: the extinction burst, "
      "a temporary worsening before the decline, with the warning that giving in during the burst converts the "
      "behaviour to an intermittent schedule and makes it harder to shift. Bottom: the token economy as a "
      "two-step exchange, and the ladder of least restrictive alternatives that ethics requires be climbed from "
      "the bottom.")

# ---------------- Panel A: desensitisation vs flooding ----------------
d.rect(40, 164, 840, 218, BLUE, "none", rx=12, width=2)
d.text(460, 192, "Two routes to the same extinction", color=BLUE, weight="bold", size=16)

m = d.axes(120, 212, 480, 118, "", "anxiety", (0, 10), (0, 1.15), ticks_x=None, ticks_y=None)


def desens(t):
    base = 0.18 + 0.1 * math.sin(t * 3.1)
    return max(0.05, base * math.exp(-t / 14) + 0.06)


def flood(t):
    if t < 0.6:
        return 0.1 + 1.6 * t
    return max(0.06, 1.06 * math.exp(-(t - 0.6) / 2.1))


d.curve(m, [(t / 25, desens(t / 25)) for t in range(0, 251)], SAGE, 2.8)
d.curve(m, [(t / 25, flood(t / 25)) for t in range(0, 251)], RED, 2.8)
px, py = m(1.1, 0.92)
d.text(px + 10, py, "flooding: one big spike", anchor="start", color=RED, weight="bold", size=13)
px, py = m(5.0, 0.46)
d.text(px, py, "systematic desensitisation: relaxed the whole way",
       color=SAGE, weight="bold", size=13)

d.rect(624, 212, 240, 118, GREY, "#e9e4da", rx=9, width=1.6)
d.text(744, 236, "both work by extinction", color=NAVY, weight="bold", size=13)
d.text(744, 260, "desensitisation adds relaxation,", color=GREY, size=12)
d.text(744, 278, "which is incompatible with fear", color=GREY, size=12)
d.text(744, 304, "flooding is faster but", color=NAVY, size=12)
d.text(744, 322, "loses more patients", color=NAVY, size=12)

d.text(460, 364, "imaginal first, then in vivo — real contact generalises better",
       color=GREY, size=13)

# ---------------- Panel B: the ABC spine ----------------
d.rect(40, 398, 440, 230, SAGE, "none", rx=12, width=2)
d.text(260, 426, "Where each operant technique attaches", color=SAGE, weight="bold", size=15)

cols = [("ANTECEDENT", ["prompting", "fading", "discriminative cues"], BLUE),
        ("BEHAVIOUR", ["shaping", "chaining"], SAGE),
        ("CONSEQUENCE", ["reinforcement", "extinction", "response cost"], RED)]
x = 62
for name, items, col in cols:
    d.rect(x, 446, 124, 150, col, FILL[col], rx=9, width=2)
    d.text(x + 62, 470, name, color=col, weight="bold", size=12)
    yy = 498
    for it in items:
        d.text(x + 62, yy, it, color=NAVY, size=12)
        yy += 22
    x += 142
for ax in (190, 332):
    d.arrow(ax, 521, ax + 14, 521, GREY, width=2)

d.text(260, 614, "negative reinforcement is still reinforcement: it raises behaviour",
       color=NAVY, weight="bold", size=13)

# ---------------- Panel C: extinction burst ----------------
d.rect(500, 398, 380, 230, RED, "none", rx=12, width=2)
d.text(690, 426, "Expect it to get worse first", color=RED, weight="bold", size=15)

m2 = d.axes(570, 448, 272, 96, "", "problem behaviour", (0, 10), (0, 1.3),
            ticks_x=None, ticks_y=None)


def eb(t):
    if t < 2.5:
        return 0.6
    if t < 3.4:
        return 0.6 + (t - 2.5) * 0.72
    return max(0.05, 1.25 * math.exp(-(t - 3.4) / 1.7))


d.curve(m2, [(t / 25, eb(t / 25)) for t in range(0, 251)], RED, 2.8)
px, py = m2(2.5, 0.6)
d.line(px, py + 10, px, py - 76, GREY, 1.4, True)
d.text(px - 8, py - 34, "reinforcement withheld", anchor="end", color=GREY, size=11)
px, py = m2(3.4, 1.25)
d.text(px + 8, py + 2, "the burst", anchor="start", color=RED, weight="bold", size=13)

d.text(690, 578, "give in here and you have just taught", color=NAVY, weight="bold", size=13)
d.text(690, 598, "an intermittent schedule — the hardest kind to undo", color=GREY, size=12)
d.text(690, 618, "", color=GREY, size=12)

# ---------------- Panel D: token economy ----------------
d.rect(40, 644, 404, 212, GOLD, "none", rx=12, width=2)
d.text(242, 672, "Token economy: a two-step exchange", color=GOLD, weight="bold", size=15)

boxes = [("target behaviour", "specific and observable", 694),
         ("token", "a conditioned reinforcer,\ndelivered immediately", 746),
         ("backup reinforcer", "what the person actually wants", 812)]
for name, gloss, y in boxes:
    d.rect(64, y, 356, 44 if "\n" not in gloss else 56, GOLD, FILL[GOLD], rx=9, width=2)
    d.text(242, y + 20, name, color=GOLD, weight="bold", size=13)
    if "\n" in gloss:
        a, b = gloss.split("\n")
        d.text(242, y + 38, a, color=NAVY, size=11)
        d.text(242, y + 52, b, color=NAVY, size=11)
    else:
        d.text(242, y + 38, gloss, color=NAVY, size=11)
for ay in (740, 806):
    d.arrow(242, ay, 242, ay + 6, GREY, width=2)

# ---------------- Panel E: least restrictive ladder ----------------
d.rect(466, 644, 414, 212, NAVY, "none", rx=12, width=2)
d.text(673, 672, "Climb from the bottom, and only if you must",
       color=NAVY, weight="bold", size=15)

rungs = [("aversive procedures", RED, 690),
         ("response cost, time-out", GOLD, 728),
         ("extinction of the problem behaviour", BLUE, 766),
         ("reinforce an alternative that works", SAGE, 804)]
for name, col, y in rungs:
    d.rect(498, y, 352, 30, col, FILL[col], rx=7, width=2)
    d.text(674, y + 21, name, color=col, weight="bold", size=13)
d.arrow(482, 828, 482, 696, GREY, width=2)
d.text(673, 846, "consent, assent, and review before anything aversive",
       color=GREY, size=12)

d.save("behaviour-modification-techniques-and-ethics")
print("ok")
