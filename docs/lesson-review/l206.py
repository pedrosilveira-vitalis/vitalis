import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 912,
      "The brain's rules for grouping, and for depth",
      "Perception is a hypothesis: the simplest arrangement that explains the image",
      "Top: the Gestalt principles, each drawn as the smallest figure that makes it visible. Proximity groups "
      "by distance, similarity by feature, good continuation by smooth path, closure by completing a shape "
      "that was never drawn, common fate by shared motion, and symmetry by balance — all of them special "
      "cases of Prägnanz, the preference for the simplest stable reading. Bottom: the depth cues, sorted by "
      "how many eyes they need. The pictorial cues all work in a photograph, which is why a painting can look "
      "deep; motion parallax needs the observer to move; disparity and convergence need two eyes and work "
      "best close up. Lose an eye and the whole top row survives — which is why monocular pilots can still "
      "judge distance, especially while moving."
      )

# ---------------- Panel A: Gestalt ----------------
d.rect(40, 170, 840, 300, SAGE, "none", rx=12, width=2)
d.text(460, 198, "Seven ways the brain groups", color=SAGE, weight="bold", size=16)

bx, by, bw, bh = 66, 218, 194, 112


def cell(col, row, title, note, color):
    x = bx + col * 206
    y = by + row * 124
    d.rect(x, y, bw, bh, color, FILL[color], rx=9, width=2)
    d.text(x + bw / 2, y + 22, title, color=color, weight="bold", size=12)
    d.text(x + bw / 2, y + 104, note, color=GREY, size=10)
    return x, y


# proximity
x, y = cell(0, 0, "PROXIMITY", "near things belong together", BLUE)
for i in range(6):
    gx = x + 34 + (i // 3) * 76 + (i % 3) * 16
    for j in range(2):
        d.circle(gx, y + 52 + j * 18, 5, BLUE, BLUE)

# similarity
x, y = cell(1, 0, "SIMILARITY", "like features belong together", RED)
for i in range(6):
    for j in range(2):
        col = RED if i % 2 == 0 else GREY
        d.circle(x + 44 + i * 22, y + 52 + j * 18, 5, col, col)

# continuation
x, y = cell(2, 0, "GOOD CONTINUATION", "the smooth path wins", GOLD)
d.path("M%d %d q40 -24 80 0 q40 24 80 0" % (x + 18, y + 62), GOLD, 2.6, "none")
d.path("M%d %d q40 24 80 0 q40 -24 80 0" % (x + 18, y + 62), GREY, 2.2, "none", dash="5,4")

# continuation note replaced below
x, y = cell(3, 0, "CLOSURE", "a shape that was never drawn", SAGE)
cx0, cy0 = x + bw / 2, y + 64
import math
for k in range(3):
    ang = math.radians(90 + k * 120)
    px, py = cx0 + 26 * math.cos(ang), cy0 - 26 * math.sin(ang)
    d.circle(px, py, 10, SAGE, FILL[SAGE], width=2)
d.path("M%.1f %.1f L%.1f %.1f L%.1f %.1f z" % (
    cx0, cy0 - 26, cx0 - 23, cy0 + 13, cx0 + 23, cy0 + 13), SAGE, 1.4, "none", dash="3,3")

# common fate
x, y = cell(0, 1, "COMMON FATE", "moving together = one thing", BLUE)
for i in range(4):
    d.arrow(x + 32 + i * 34, y + 66, x + 50 + i * 34, y + 46, BLUE, width=2)

# symmetry
x, y = cell(1, 1, "SYMMETRY", "balanced regions read as figure", RED)
d.path("M%d %d q24 -26 46 0 q-22 26 -46 0 z" % (x + 44, y + 56), RED, 2.2, FILL[RED])
d.path("M%d %d q-24 -26 -46 0 q22 26 46 0 z" % (x + 150, y + 56), RED, 2.2, FILL[RED])
d.line(x + bw / 2, y + 36, x + bw / 2, y + 76, GREY, 1.4, dash="3,3")

# figure-ground
x, y = cell(2, 1, "FIGURE–GROUND", "the edge belongs to the figure", GREY)
d.rect(x + 36, y + 34, 122, 46, GREY, "#e9e4da", rx=5, width=1.6)
d.circle(x + 97, y + 57, 17, NAVY, "#dde4ea", width=2)

# pragnanz
x, y = cell(3, 1, "PRÄGNANZ", "all of the above, in one rule", NAVY)
d.text(x + bw / 2, y + 62, "simplest stable reading", color=NAVY, weight="bold", size=12)

# ---------------- Panel B: depth cues ----------------
d.rect(40, 486, 840, 396, BLUE, "none", rx=12, width=2)
d.text(460, 514, "Depth cues, by how many eyes they need", color=BLUE, weight="bold", size=16)

d.rect(66, 534, 788, 148, SAGE, FILL[SAGE], rx=10, width=2)
d.text(460, 558, "MONOCULAR — one eye is enough", color=SAGE, weight="bold", size=14)
mono = [("linear perspective", "parallels converge"), ("relative size", "smaller = farther"),
        ("interposition", "the one in front is nearer"), ("texture gradient", "denser = farther"),
        ("aerial perspective", "hazier and bluer = farther"), ("shading", "light is assumed from above"),
        ("motion parallax", "near things sweep past faster"), ("accommodation", "lens effort, under 2 m")]
for i, (a, b) in enumerate(mono):
    col = i % 2
    row = i // 2
    x = 200 + col * 420
    y = 584 + row * 24
    d.text(x, y, a, anchor="end", color=NAVY, weight="bold", size=11)
    d.text(x + 12, y, b, anchor="start", color=GREY, size=11)

d.rect(66, 698, 788, 112, RED, FILL[RED], rx=10, width=2)
d.text(460, 722, "BINOCULAR — needs both", color=RED, weight="bold", size=14)
d.text(300, 750, "binocular disparity", anchor="end", color=NAVY, weight="bold", size=11)
d.text(312, 750, "the two retinal images differ; the strongest cue, best within ~10 m",
       anchor="start", color=GREY, size=11)
d.text(300, 776, "convergence", anchor="end", color=NAVY, weight="bold", size=11)
d.text(312, 776, "how far the eyes turn inward; useful under about 6 m",
       anchor="start", color=GREY, size=11)

d.text(460, 840, "a painting has only the pictorial cues · a one-eyed observer keeps every monocular "
                 "cue, and leans on parallax",
       color=NAVY, weight="bold", size=12)
d.text(460, 862, "3D cinema fakes disparity but cannot fake convergence or accommodation — which is "
                 "why it can make people queasy",
       color=GREY, size=11)

d.save("gestalt-principles-and-depth-cues")
print("ok")
