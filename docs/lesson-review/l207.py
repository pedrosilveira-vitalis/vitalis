import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 884,
      "The illusions are the rules showing their working",
      "Constancy is useful almost always; an illusion is what it costs the rest of the time",
      "Top: the Müller-Lyer figure, which is the one students most often memorise backwards. Both shafts "
      "are the same length. The one whose fins splay outward reads as the inside corner of a room, which is "
      "farther from you, and since the brain scales a retinal image up with distance, that line looks longer. "
      "The one with arrowheads closing inward reads as the near, outside corner of a building, so it looks "
      "shorter. That is size constancy, correctly applied to a flat drawing that does not deserve it — and "
      "people raised where buildings are not full of right angles are measurably less fooled. Bottom left: the "
      "five constancies. Bottom right: the direction of influence that each illusion exposes."
      )

# ---------------- Panel A: Muller-Lyer ----------------
d.rect(40, 176, 840, 272, GOLD, "none", rx=12, width=2)
d.text(460, 204, "Same length. Not the same percept.", color=GOLD, weight="bold", size=16)


def ml(cx, y, outward, col, label, reads, looks):
    half = 110
    d.line(cx - half, y, cx + half, y, col, 3)
    f = 30
    for sgn in (-1, 1):
        ex = cx + sgn * half
        if outward:
            d.line(ex, y, ex + sgn * f, y - f * 0.7, col, 2.6)
            d.line(ex, y, ex + sgn * f, y + f * 0.7, col, 2.6)
        else:
            d.line(ex, y, ex - sgn * f, y - f * 0.7, col, 2.6)
            d.line(ex, y, ex - sgn * f, y + f * 0.7, col, 2.6)
    d.text(cx, y - 58, label, color=col, weight="bold", size=13)
    d.text(cx, y + 56, reads, color=NAVY, size=12)
    d.text(cx, y + 76, looks, color=col, weight="bold", size=13)


ml(250, 290, True, SAGE, "fins splay OUTWARD",
   "reads as an inside corner — farther", "so it looks LONGER")
ml(670, 290, False, RED, "arrowheads close INWARD",
   "reads as an outside corner — nearer", "so it looks SHORTER")

d.line(460, 240, 460, 400, GREY, 1.4, dash="4,4")
d.text(460, 424, "both shafts are 220 px · measure them · the depth story is what differs",
       color=GREY, size=12)

# ---------------- Panel B: constancies ----------------
d.rect(40, 464, 420, 390, BLUE, "none", rx=12, width=2)
d.text(250, 492, "The five constancies", color=BLUE, weight="bold", size=15)

rows = [
    ("SIZE", "retinal image shrinks", "scaled by perceived distance"),
    ("SHAPE", "a tilted plate is an ellipse", "still perceived as a circle"),
    ("LIGHTNESS", "sunlight or candlelight", "ratios to neighbours stay fixed"),
    ("COLOUR", "the illuminant changes", "the brain discounts it"),
    ("POSITION", "every saccade shifts the image", "corollary discharge cancels it"),
]
y = 514
for name, before, after in rows:
    d.rect(66, y, 368, 56, BLUE, FILL[BLUE], rx=8, width=1.8)
    d.text(250, y + 20, name, color=BLUE, weight="bold", size=12)
    d.text(250, y + 36, before, color=GREY, size=11)
    d.text(250, y + 50, after, color=NAVY, size=11)
    y += 62

d.text(250, 842, "push your own eyeball and the world jumps — no motor command, no cancellation",
       color=GREY, size=10)

# ---------------- Panel C: what each illusion exposes ----------------
d.rect(480, 464, 400, 390, RED, "none", rx=12, width=2)
d.text(680, 492, "What each one exposes", color=RED, weight="bold", size=15)

items = [
    ("Müller-Lyer · Ponzo", "size constancy misapplied to depth cues", GOLD),
    ("Mach bands", "lateral inhibition at a border", BLUE),
    ("Checker shadow", "lightness constancy discounting a shadow", SAGE),
    ("Necker cube · Rubin vase", "two readings, neither preferred", GREY),
    ("Phi phenomenon", "motion built from still frames", RED),
    ("Waterfall aftereffect", "fatigue in direction-tuned neurons", RED),
    ("Autokinetic effect", "no frame of reference to anchor to", GREY),
]
y = 516
for name, what, col in items:
    d.text(500, y, name, anchor="start", color=col, weight="bold", size=12)
    d.text(500, y + 16, what, anchor="start", color=GREY, size=11)
    y += 44

d.text(680, 824, "none of them go away when you are told", color=NAVY, weight="bold", size=12)
d.text(680, 842, "knowing is top-down; the assumption sits lower", color=GREY, size=10)

d.save("muller-lyer-constancies-and-illusions")
print("ok")
