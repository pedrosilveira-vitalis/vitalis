import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 916,
      "Two distributions, one movable line",
      "Every detection question asks the same thing: did sensitivity change, or did the criterion move?",
      "Top: the whole of signal detection theory in one picture. Noise alone produces some internal "
      "activation; a signal adds to it. The two bell curves overlap, and the observer has to place a line "
      "somewhere and say yes above it. The distance between the peaks is d′, the sensitivity, and it is "
      "fixed by the stimulus and the senses. The line is the criterion, and it is set by payoffs, "
      "expectations and base rates. Move the line left and hits and false alarms both rise together; that is "
      "a liberal criterion, not better eyesight. Bottom left: the four outcomes those two things produce, "
      "with their clinical names. Bottom right: Weber's law, where the just noticeable difference is a fixed "
      "proportion of what you started with, so the smaller the Weber fraction the finer the discrimination."
      )

# ---------------- Panel A: the two distributions ----------------
d.rect(40, 176, 840, 318, BLUE, "none", rx=12, width=2)
d.text(460, 204, "Sensitivity is the gap; bias is the line", color=BLUE, weight="bold", size=16)

m = d.axes(110, 232, 700, 170, "", "internal activation",
           (0, 10), (0, 1.12), ticks_x=None, ticks_y=None)


def bell(mu):
    return [(x / 20.0, math.exp(-((x / 20.0 - mu) ** 2) / 2.0)) for x in range(0, 201)]


d.curve(m, bell(3.6), GREY, 2.6)
d.curve(m, bell(6.4), SAGE, 2.8)

px, py = m(3.6, 1.04)
d.text(px, py, "NOISE alone", color=GREY, weight="bold", size=12)
px, py = m(6.4, 1.04)
d.text(px, py, "SIGNAL + NOISE", color=SAGE, weight="bold", size=12)

# d' arrow between the peaks
ax, ay = m(3.6, 0.42)
bx, by = m(6.4, 0.42)
d.arrow(ax, ay, bx, by, BLUE, width=2)
d.text((ax + bx) / 2, ay - 10, "d′ = the distance between the peaks",
       color=BLUE, weight="bold", size=12)

# criterion line
cx, cy0 = m(5.5, 0)
_, cy1 = m(5.5, 1.0)
d.line(cx, cy0, cx, cy1, RED, 2.4)
d.text(cx - 10, cy1 + 16, "criterion \u2192", anchor="end", color=RED, weight="bold", size=12)

d.text(240, 424, "← move it left: LIBERAL", color=GOLD, weight="bold", size=13)
d.text(240, 444, "more hits AND more false alarms", color=GREY, size=11)
d.text(700, 424, "move it right: CONSERVATIVE →", color=BLUE, weight="bold", size=13)
d.text(700, 444, "fewer false alarms AND fewer hits", color=GREY, size=11)

d.text(460, 478, "payoffs, expectations and base rates move the line — they never change d′",
       color=NAVY, weight="bold", size=13)

# ---------------- Panel B: the 2x2 ----------------
d.rect(40, 512, 420, 376, SAGE, "none", rx=12, width=2)
d.text(250, 540, "The four outcomes", color=SAGE, weight="bold", size=15)

d.text(196, 580, "signal PRESENT", color=GREY, weight="bold", size=11)
d.text(346, 580, "signal ABSENT", color=GREY, weight="bold", size=11)
d.text(96, 626, "said", anchor="middle", color=GREY, weight="bold", size=11)
d.text(96, 642, "\"yes\"", anchor="middle", color=GREY, weight="bold", size=11)
d.text(96, 736, "said", anchor="middle", color=GREY, weight="bold", size=11)
d.text(96, 752, "\"no\"", anchor="middle", color=GREY, weight="bold", size=11)

cells = [
    (134, 592, "HIT", "sensitivity, in clinic", SAGE),
    (284, 592, "FALSE ALARM", "costs: the unnecessary biopsy", RED),
    (134, 702, "MISS", "the cancer sent home", RED),
    (284, 702, "CORRECT REJECTION", "specificity, in clinic", SAGE),
]
for x, y, name, note, col in cells:
    d.rect(x, y, 142, 96, col, FILL[col], rx=8, width=2)
    d.text(x + 71, y + 40, name, color=col, weight="bold", size=12)
    d.text(x + 71, y + 62, note.split(",")[0], color=GREY, size=10)
    if "," in note:
        d.text(x + 71, y + 76, note.split(",", 1)[1].strip(), color=GREY, size=10)

d.text(250, 830, "hit rate and false alarm rate are the two numbers", color=NAVY, size=11)
d.text(250, 848, "you need; d′ = z(hit) − z(false alarm)", color=NAVY, weight="bold", size=12)
d.text(250, 872, "high hits AND high false alarms = liberal, not sharp", color=GOLD, weight="bold", size=11)

# ---------------- Panel C: Weber ----------------
d.rect(480, 512, 400, 376, GOLD, "none", rx=12, width=2)
d.text(680, 540, "Weber's law is a proportion", color=GOLD, weight="bold", size=15)

d.rect(512, 560, 336, 72, GOLD, FILL[GOLD], rx=10, width=2)
d.text(680, 594, "ΔI / I = k", color=NAVY, weight="bold", size=22)
d.text(680, 618, "the change you can just detect, over what you started with",
       color=GREY, size=10)

d.text(680, 656, "smaller k = finer discrimination", color=GOLD, weight="bold", size=13)
d.text(680, 674, "(approximate \u2014 published values vary by study)", color=GREY, size=10)

bars = [("heaviness", 0.02), ("pain", 0.07), ("brightness", 0.08),
        ("salt taste", 0.08), ("smell", 0.10), ("loudness", 0.10)]
y = 692
for name, k in bars:
    d.text(596, y + 9, name, anchor="end", color=NAVY, size=11)
    w = k * 1800
    d.rect(608, y, w, 13, GOLD, FILL[GOLD], rx=3, width=1.4)
    d.text(616 + w, y + 9, "%d%%" % round(k * 100), anchor="start", color=GREY, size=10)
    y += 24

d.text(680, 848, "100 g → 2 g JND means 500 g → 10 g JND", color=NAVY, weight="bold", size=12)
d.text(680, 868, "the same proportion, never the same amount", color=GREY, size=11)

d.save("signal-detection-and-webers-law")
print("ok")
