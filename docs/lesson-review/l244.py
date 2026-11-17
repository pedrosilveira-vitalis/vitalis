import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 968,
      "How a social condition becomes a diagnosis",
      "Four pathways from the outside world to the inside of the body",
      "Top: the four routes by which position in society turns into disease. They are worth separating because "
      "questions usually ask which one a passage is describing. Material deprivation acts directly on what a "
      "person can buy and where they can live. The psychosocial route runs through chronic stress to the HPA "
      "axis and allostatic load. The behavioural route is real but is itself shaped by the first two, so an "
      "answer that stops at “poor choices” is usually the wrong one. Access is the healthcare route. Middle: "
      "the gradient and what it rules out. Bottom: fundamental cause theory, which explains why disparities "
      "outlive any particular risk factor, and the figures most often quoted."
      )

# ---------------- Panel A: four pathways ----------------
d.rect(40, 180, 840, 250, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Four pathways from position to pathology", color=NAVY, weight="bold", size=15)

paths = [("MATERIAL", "what you can buy,\nwhere you can live", BLUE,
          ["food, housing, heating",
           "neighbourhood exposure:",
           "lead, pollution, violence",
           "no cushion for a shock"]),
         ("PSYCHOSOCIAL", "chronic stress and\nlow control", RED,
          ["HPA axis → cortisol",
           "allostatic load",
           "shorter telomeres",
           "inflammation, insulin resistance"]),
         ("BEHAVIOURAL", "smoking, diet, activity,\nadherence", GOLD,
          ["real — but downstream of",
           "the first two",
           "“poor choices” is almost",
           "never the keyed answer"]),
         ("ACCESS", "whether care is got,\nand what kind", SAGE,
          ["insurance, distance, time off",
           "language and literacy",
           "provider bias once inside",
           "trust, or its absence"])]
cx = 60
for name, tag, col, items in paths:
    d.rect(cx, 228, 200, 182, col, FILL[col], rx=9, width=1.8)
    d.text(cx + 100, 252, name, color=col, weight="bold", size=11.5)
    for j, ln in enumerate(tag.split("\n")):
        d.text(cx + 100, 270 + j * 13, ln, color=NAVY, size=8.5)
    d.line(cx + 24, 300, cx + 176, 300, col, 1, dash="3,3")
    for j, ln in enumerate(items):
        d.text(cx + 100, 322 + j * 17, ln, color=GREY, size=8.5)
    cx += 205

# ---------------- Panel B: the gradient ----------------
d.rect(40, 446, 410, 240, GOLD, "none", rx=12, width=2)
d.text(245, 474, "It is a gradient, not a cliff", color=GOLD, weight="bold", size=14)

m = d.axes(96, 496, 300, 120, "", "", (0, 5), (0, 5), ticks_x=0, ticks_y=0)
d.curve(m, [(0.4, 4.3), (1.4, 3.3), (2.4, 2.4), (3.4, 1.6), (4.5, 1.0)], GOLD, 3)
for xv, yv in [(0.4, 4.3), (1.4, 3.3), (2.4, 2.4), (3.4, 1.6), (4.5, 1.0)]:
    px, py = m(xv, yv)
    d.circle(px, py, 4.5, GOLD, GOLD)
d.text(110, 640, "poorest", anchor="start", color=NAVY, weight="bold", size=9)
d.text(390, 640, "richest", anchor="end", color=NAVY, weight="bold", size=9)
d.text(60, 556, "worse", anchor="start", color=GREY, size=8.5)

d.text(245, 662, "every step up improves health — so a poverty", color=NAVY, weight="bold", size=9.5)
d.text(245, 678, "threshold cannot be the whole story", color=NAVY, weight="bold", size=9.5)

# ---------------- Panel C: fundamental cause ----------------
d.rect(470, 446, 410, 240, RED, "none", rx=12, width=2)
d.text(675, 474, "Why disparities outlive the risk factor", color=RED, weight="bold", size=13.5)

d.rect(494, 494, 362, 50, GREY, FILL[GREY], rx=8, width=1.6)
d.text(675, 514, "a new way to protect health appears", color=NAVY, weight="bold", size=10)
d.text(675, 532, "a vaccine, a screening test, a cessation programme", color=GREY, size=8.5)

d.arrow(675, 548, 675, 570, GREY)

d.rect(494, 576, 176, 52, SAGE, FILL[SAGE], rx=8, width=1.6)
d.text(582, 598, "HIGHER SES", color=SAGE, weight="bold", size=10)
d.text(582, 616, "takes it up first", color=GREY, size=8.5)
d.rect(680, 576, 176, 52, RED, FILL[RED], rx=8, width=1.6)
d.text(768, 598, "LOWER SES", color=RED, weight="bold", size=10)
d.text(768, 616, "takes it up later or not", color=GREY, size=8.5)

d.text(675, 650, "so the gap reappears around the NEW factor", color=NAVY, weight="bold", size=10)
d.text(675, 668, "Link and Phelan: SES is a FUNDAMENTAL cause", color=RED, weight="bold", size=10)

# ---------------- Panel D: the figures ----------------
d.rect(40, 702, 840, 246, BLUE, "none", rx=12, width=2)
d.text(460, 730, "The figures worth carrying in", color=BLUE, weight="bold", size=14)

figs = [("LIFE EXPECTANCY", "richest 1% vs poorest 1%:\n14.6 years for men, 10.1 for women", BLUE),
        ("INFANT MORTALITY", "Black infants die at about\n2.3 times the white rate", RED),
        ("MATERNAL MORTALITY", "Black women: 2–3 times the\nwhite rate, after adjusting for\nincome and education", RED),
        ("ACEs", "4 or more adverse childhood\nexperiences: sharply raised adult\ndisease across many systems", GOLD)]
cx = 60
for name, note, col in figs:
    d.rect(cx, 750, 200, 110, col, FILL[col], rx=9, width=1.8)
    d.text(cx + 100, 774, name, color=col, weight="bold", size=10)
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 100, 796 + j * 14, ln, color=GREY, size=8.5)
    cx += 205

d.text(460, 886, "AND THE ONE THAT RUNS THE OTHER WAY", color=SAGE, weight="bold", size=10.5)
d.text(460, 906, "the Hispanic paradox: lower mortality than non-Hispanic white Americans despite lower average income",
       color=NAVY, size=9.5)
d.text(460, 924, "explained by healthy-immigrant selection, dense family networks, and possibly salmon bias; it fades with time in the US",
       color=GREY, size=9)

d.save("four-pathways-gradient-and-fundamental-cause")
print("ok")
