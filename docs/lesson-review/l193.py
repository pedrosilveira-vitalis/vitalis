import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 872,
      "A workspace, not a waiting room",
      "Short-term memory holds; working memory holds while you do something to it",
      "Top left: the Peterson and Peterson result, recall of a three-letter trigram plotted against the delay "
      "filled with counting backwards, falling from near perfect at three seconds to about a tenth by eighteen — "
      "the evidence for a fifteen to thirty second span without rehearsal. Top right: chunking, with twelve "
      "loose letters recoded as four familiar acronyms so that the same material costs four slots instead of "
      "twelve. Middle: the four experimental effects that reveal the phonological loop — phonological "
      "similarity, word length, articulatory suppression and irrelevant speech — each with what it shows. "
      "Bottom: short-term memory against working memory, passive store against active workspace, with the "
      "capacity and duration figures and the prefrontal involvement that distinguishes them."
      )

# ---------------- Panel A: Peterson & Peterson ----------------
d.rect(40, 156, 420, 262, BLUE, "none", rx=12, width=2)
d.text(250, 184, "Block rehearsal and it is gone in 18 s", color=BLUE, weight="bold", size=15)

m = d.axes(112, 206, 300, 120, "seconds of counting backwards", "% recalled",
           (0, 19), (0, 100), ticks_x=[3, 9, 15, 18], ticks_y=[10, 50, 80])
d.curve(m, [(t / 10, 92 * math.exp(-(t / 10) / 7.2) + 5) for t in range(0, 191)], BLUE, 2.8)
px, py = m(3, 92 * math.exp(-3 / 7.2) + 5)
d.circle(px, py, 4, NAVY, NAVY)
px, py = m(18, 92 * math.exp(-18 / 7.2) + 5)
d.circle(px, py, 4, RED, RED)
d.text(px - 8, py - 14, "≈ 10%", anchor="end", color=RED, weight="bold", size=13)

d.text(250, 392, "15–30 s is the span when nothing refreshes it",
       color=NAVY, weight="bold", size=14)

# ---------------- Panel B: chunking ----------------
d.rect(480, 156, 400, 262, GOLD, "none", rx=12, width=2)
d.text(680, 184, "Chunking buys slots, not storage", color=GOLD, weight="bold", size=15)

letters = list("FBICIANFLNBA")
x = 520
for i, ch in enumerate(letters):
    d.rect(x, 206, 26, 28, GREY, "#faf6ee", rx=4, width=1.5)
    d.text(x + 13, 226, ch, color=GREY, weight="bold", size=13)
    x += 30
d.text(680, 252, "12 items — over capacity", color=GREY, size=13)

d.arrow(680, 262, 680, 282, NAVY, width=2)

x = 528
for grp in ("FBI", "CIA", "NFL", "NBA"):
    d.rect(x, 292, 76, 34, GOLD, FILL[GOLD], rx=7, width=2)
    d.text(x + 38, 315, grp, color=GOLD, weight="bold", size=15)
    x += 84
d.text(680, 348, "4 chunks — comfortably inside it", color=NAVY, weight="bold", size=14)

d.text(680, 378, "Miller said 7 ± 2; Cowan's stricter tests say 4 ± 1", color=GREY, size=13)
d.text(680, 400, "expertise is a library of chunks, not a bigger store", color=GREY, size=12)

# ---------------- Panel C: phonological loop evidence ----------------
d.rect(40, 434, 840, 194, SAGE, "none", rx=12, width=2)
d.text(460, 462, "Four effects that give the phonological loop away",
       color=SAGE, weight="bold", size=16)

effects = [("phonological similarity", "B C D G P T are hard;", "the store codes sound"),
           ("word length", "short words beat long ones;", "rehearsal runs in real time"),
           ("articulatory suppression", "say \"the, the, the\" and", "the length effect vanishes"),
           ("irrelevant speech", "background talk intrudes", "even when ignored")]
x = 62
for name, a, b in effects:
    d.rect(x, 480, 196, 104, SAGE, FILL[SAGE], rx=10, width=2)
    d.text(x + 98, 506, name, color=SAGE, weight="bold", size=12)
    d.text(x + 98, 534, a, color=NAVY, size=11)
    d.text(x + 98, 552, b, color=NAVY, size=11)
    x += 206

d.text(460, 608, "store ≈ 2 s of sound; the inner voice refreshes it before it fades",
       color=GREY, size=13)

# ---------------- Panel D: STM vs WM ----------------
d.rect(40, 644, 840, 204, NAVY, "none", rx=12, width=2)
d.text(460, 672, "Same material, two different jobs", color=NAVY, weight="bold", size=16)

d.rect(70, 692, 370, 134, BLUE, FILL[BLUE], rx=10, width=2)
d.text(255, 718, "SHORT-TERM MEMORY", color=BLUE, weight="bold", size=15)
for i, line in enumerate(["a passive store: hold it as given",
                          "7 ± 2 items, or 4 ± 1 chunks",
                          "15–30 s without rehearsal",
                          "Atkinson and Shiffrin, 1968"]):
    d.text(255, 744 + i * 20, line, color=NAVY, size=12)

d.rect(480, 692, 370, 134, SAGE, FILL[SAGE], rx=10, width=2)
d.text(665, 718, "WORKING MEMORY", color=SAGE, weight="bold", size=15)
for i, line in enumerate(["an active workspace: hold and transform",
                          "executive + loop + sketchpad + buffer",
                          "maintained by processing, not repetition",
                          "Baddeley and Hitch, 1974; prefrontal"]):
    d.text(665, 744 + i * 20, line, color=NAVY, size=12)

d.save("short-term-and-working-memory")
print("ok")
