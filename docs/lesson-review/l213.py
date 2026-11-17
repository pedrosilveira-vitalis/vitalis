import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 890,
      "Three answers to “why did it do that?”",
      "Drive says reduce the tension; arousal says find the right amount of it",
      "Top: the Yerkes and Dodson result, drawn as the two curves it actually is. Both peak in the middle, "
      "but the peak sits further right for a simple, well-practised task and further left for a complex or "
      "novel one — which is why high arousal helps a sprinter and ruins a chess player, and why exam "
      "anxiety hurts most on the questions that need the most working memory. Bottom left: Hull's equation, "
      "whose point is that it multiplies. Drive without a learned habit produces nothing, and a perfectly "
      "learned habit with no drive produces nothing either. Bottom right: the three traditions and what "
      "finished each of them — instinct theory died of circular reasoning, drive theory of curiosity."
      )

# ---------------- Panel A: Yerkes-Dodson ----------------
d.rect(40, 170, 840, 300, BLUE, "none", rx=12, width=2)
d.text(460, 198, "Two curves, not one", color=BLUE, weight="bold", size=16)

m = d.axes(130, 224, 660, 170, "arousal  →", "performance",
           (0, 10), (0, 1.15), ticks_x=None, ticks_y=None)


def bump(peak, width, height):
    return [(x / 20.0, height * math.exp(-((x / 20.0 - peak) ** 2) / (2 * width ** 2)))
            for x in range(0, 201)]


d.curve(m, bump(3.4, 1.7, 1.0), RED, 3)
d.curve(m, bump(6.6, 2.0, 1.0), SAGE, 3)

px, py = m(1.3, 0.95)
d.text(px, py, "COMPLEX or NEW task", anchor="start", color=RED, weight="bold", size=12)
d.text(px, py + 16, "peaks early — needs calm", anchor="start", color=RED, size=11)
px, py = m(9.4, 0.95)
d.text(px, py, "SIMPLE or PRACTISED task", anchor="end", color=SAGE, weight="bold", size=12)
d.text(px, py + 16, "peaks late — tolerates pressure", anchor="end", color=SAGE, size=11)

for cx, col in [(3.4, RED), (6.6, SAGE)]:
    ax, ay0 = m(cx, 0)
    _, ay1 = m(cx, 1.0)
    d.line(ax, ay0, ax, ay1, col, 1.2, dash="4,4")

px, py = m(0.6, 0.12)
d.text(px, py, "asleep", anchor="start", color=GREY, size=11)
px, py = m(9.4, 0.12)
d.text(px, py, "panic", anchor="end", color=GREY, size=11)

d.text(460, 452, "the law has two halves: the inverted U, and the fact that its peak moves with difficulty",
       color=NAVY, weight="bold", size=12)

# ---------------- Panel B: Hull ----------------
d.rect(40, 488, 400, 372, GOLD, "none", rx=12, width=2)
d.text(240, 516, "Hull's equation multiplies", color=GOLD, weight="bold", size=15)

d.rect(70, 536, 340, 66, GOLD, FILL[GOLD], rx=10, width=2)
d.text(240, 578, "E = D × H × K", color=NAVY, weight="bold", size=24)

terms = [
    ("D  drive", "how energised — and it is GENERAL,", "any need energises the strongest habit", RED),
    ("H  habit strength", "how well learned — built by", "reinforced practice, with diminishing returns", BLUE),
    ("K  incentive", "how good the reward looks — added later,", "and it is where cognition sneaks in", SAGE),
]
y = 620
for name, l1, l2, col in terms:
    d.text(240, y, name, color=col, weight="bold", size=13)
    d.text(240, y + 18, l1, color=NAVY, size=11)
    d.text(240, y + 34, l2, color=GREY, size=11)
    y += 62

d.rect(70, 806, 340, 40, RED, FILL[RED], rx=8, width=2)
d.text(240, 831, "any term at zero → no behaviour at all", color=RED, weight="bold", size=12)

# ---------------- Panel C: three traditions ----------------
d.rect(460, 488, 420, 372, SAGE, "none", rx=12, width=2)
d.text(670, 516, "What killed each one", color=SAGE, weight="bold", size=15)

trads = [
    ("INSTINCT", "James, McDougall", "behaviour is innate and species-wide",
     "named 10,000 instincts and explained\nnothing — pure circular reasoning", GREY),
    ("DRIVE REDUCTION", "Hull, after Cannon", "a need makes a tension; behaviour cuts it",
     "cannot explain curiosity, play or\nanything that RAISES arousal", BLUE),
    ("AROUSAL", "Yerkes and Dodson", "organisms seek an optimum, not a minimum",
     "still standing — and it absorbed the\nproblem that sank drive theory", SAGE),
]
y = 540
for name, who, claim, note, col in trads:
    d.rect(486, y, 368, 100, col, FILL[col], rx=9, width=2)
    d.text(670, y + 24, name, color=col, weight="bold", size=13)
    d.text(670, y + 42, who, color=GREY, size=11)
    d.text(670, y + 62, claim, color=NAVY, weight="bold", size=11)
    n1, n2 = note.split("\n")
    d.text(670, y + 80, n1, color=GREY, size=10)
    d.text(670, y + 93, n2, color=GREY, size=10)
    y += 108

d.save("yerkes-dodson-hull-and-the-three-traditions")
print("ok")
