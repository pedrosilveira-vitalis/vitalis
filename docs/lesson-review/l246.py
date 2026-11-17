import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 960,
      "Where the world is on the curve",
      "The same model, read across regions instead of across centuries",
      "Top: the two transitions running in parallel. The demographic transition tracks how many people are "
      "born and die; the epidemiological transition tracks what they die OF. They move together because "
      "surviving infection is what lets a population live long enough to develop chronic disease. Middle: "
      "where the major regions sit today, which is the usual way a passage sets up its question. Bottom left: "
      "momentum, the reason a population keeps growing for decades after fertility reaches replacement. "
      "Bottom right: what the model is criticised for, which the exam does ask about."
      )

# ---------------- Panel A: parallel transitions ----------------
d.rect(40, 180, 840, 238, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Two transitions, one clock", color=NAVY, weight="bold", size=15)

d.text(72, 240, "DEMOGRAPHIC", anchor="start", color=BLUE, weight="bold", size=10.5)
d.text(72, 336, "EPIDEMIOLOGICAL", anchor="start", color=RED, weight="bold", size=10.5)
d.text(72, 352, "(Omran, 1971)", anchor="start", color=GREY, size=8)

demo = [("high births\nhigh deaths", BLUE), ("deaths FALL\nbirths stay high", BLUE),
        ("births FALL\ndeaths low", BLUE), ("both low\nageing", BLUE)]
epi = [("pestilence\nand famine", RED), ("receding\npandemics", RED),
       ("degenerative\ndisease", RED), ("delayed\ndegenerative", RED)]
cx = 230
for i in range(4):
    for row, (txt, col), ytop in ((0, demo[i], 232), (1, epi[i], 328)):
        d.rect(cx, ytop, 148, 56, col, FILL[col], rx=8, width=1.6)
        for j, ln in enumerate(txt.split("\n")):
            d.text(cx + 74, ytop + 24 + j * 15, ln, color=NAVY, size=9)
    d.text(cx + 74, 306, "STAGE " + str(i + 1), color=GREY, weight="bold", size=9)
    if i < 3:
        d.arrow(cx + 152, 260, cx + 174, 260, GREY, width=1.4)
        d.arrow(cx + 152, 356, cx + 174, 356, GREY, width=1.4)
    cx += 174

d.text(460, 400, "the DOUBLE BURDEN: a country still fighting infection while obesity and diabetes rise — India, Nigeria, Brazil, South Africa",
       color=GOLD, weight="bold", size=9.5)

# ---------------- Panel B: where regions sit ----------------
d.rect(40, 434, 840, 182, GOLD, "none", rx=12, width=2)
d.text(460, 462, "Where the regions sit now", color=GOLD, weight="bold", size=14)

regions = [("SUB-SAHARAN\nAFRICA", "stage 2 → early 3", "TFR 4–6; most of the\nworld's growth to 2100", RED),
           ("SOUTH ASIA", "stage 3", "India near replacement\nat about 2.0", GOLD),
           ("LATIN AMERICA", "stage 3–4", "fertility falling,\ngrowth slowing", SAGE),
           ("EUROPE · N. AMERICA", "stage 4", "below replacement,\noffset by immigration", BLUE),
           ("EAST ASIA", "stage 4–5", "Japan 1.2, Korea under\n1.0; shrinking", NAVY)]
cx = 56
for name, stage, note, col in regions:
    d.rect(cx, 480, 162, 118, col, FILL[col], rx=9, width=1.8)
    lines = name.split("\n")
    for j, ln in enumerate(lines):
        d.text(cx + 81, 502 + j * 13, ln, color=col, weight="bold", size=9.5)
    d.text(cx + 81, 538, stage, color=NAVY, weight="bold", size=10)
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 81, 562 + j * 14, ln, color=GREY, size=8.5)
    cx += 166

# ---------------- Panel C: momentum ----------------
d.rect(40, 632, 410, 308, SAGE, "none", rx=12, width=2)
d.text(245, 660, "Why growth outlives high fertility", color=SAGE, weight="bold", size=13.5)

d.rect(66, 682, 358, 46, SAGE, FILL[SAGE], rx=8, width=1.6)
d.text(245, 700, "fertility reaches replacement, 2.1", color=NAVY, weight="bold", size=10)
d.text(245, 718, "a woman now has just enough children to replace herself", color=GREY, size=8.5)

d.arrow(245, 732, 245, 754, GREY)

d.rect(66, 760, 358, 58, GOLD, FILL[GOLD], rx=8, width=1.6)
d.text(245, 780, "but the last large cohorts are still children", color=NAVY, weight="bold", size=10)
d.text(245, 798, "they have not reached childbearing age yet, and there", color=GREY, size=8.5)
d.text(245, 812, "are far more of them than there are old people", color=GREY, size=8.5)

d.arrow(245, 822, 245, 844, GREY)

d.rect(66, 850, 358, 64, RED, FILL[RED], rx=8, width=1.8)
d.text(245, 872, "POPULATION MOMENTUM", color=RED, weight="bold", size=11)
d.text(245, 890, "births keep exceeding deaths for DECADES", color=NAVY, weight="bold", size=9.5)
d.text(245, 906, "after fertility itself has stopped falling", color=NAVY, size=9)

d.text(245, 930, "it is why the world is projected to peak near 10 billion around 2080–2100", color=GREY, size=8.5)

# ---------------- Panel D: criticisms ----------------
d.rect(470, 632, 410, 308, BLUE, "none", rx=12, width=2)
d.text(675, 660, "What the model is criticised for", color=BLUE, weight="bold", size=13.5)

crit = [("EUROCENTRIC", "built on 18th–19th century western Europe;\nother regions need not follow the same path"),
        ("ASSUMES ONE LINE", "countries can stall, reverse, or skip —\nthe stages are not a timetable"),
        ("IGNORES MIGRATION", "it models births minus deaths only, yet\nmigration now drives growth in Stage 4 countries"),
        ("DESCRIBES, NOT EXPLAINS", "it says THAT fertility falls, not exactly\nwhy or when — so it predicts policy poorly"),
        ("THE AFRICAN EXCEPTION", "mortality fell without the expected\nfertility decline across several generations")]
y = 682
for name, note in crit:
    d.rect(494, y, 362, 46, BLUE, FILL[BLUE], rx=7, width=1.4)
    d.text(675, y + 17, name, color=BLUE, weight="bold", size=10)
    for j, ln in enumerate(note.split("\n")):
        d.text(675, y + 31 + j * 11, ln, color=GREY, size=8)
    y += 52

d.save("two-transitions-regions-and-momentum")
print("ok")
