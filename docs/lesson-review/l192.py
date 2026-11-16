import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 876,
      "You see far more than you can report",
      "Sensory memory is wide and brief; attention decides the sliver that survives",
      "Top left: Sperling's grid of twelve letters flashed for fifty milliseconds, with whole report recovering "
      "only four or five while a tone cueing a single row recovers three of its four, implying that about nine of "
      "the twelve were briefly available. Top right: the number of letters still recoverable plotted against the "
      "delay before the cue, falling from about nine at no delay to the whole-report level of four or five by one "
      "second — the fading of the icon, not a limit on how much was seen. Middle: the three filter models placed "
      "on the same processing stream, with Broadbent's filter before meaning is extracted, Treisman's attenuator "
      "turning unattended channels down rather than off, and the late-selection bottleneck after full semantic "
      "analysis. Bottom: the durations of the sensory registers side by side, and the failures that follow when "
      "attention is elsewhere."
      )

# ---------------- Panel A: Sperling ----------------
d.rect(40, 156, 420, 274, BLUE, "none", rx=12, width=2)
d.text(250, 184, "Sperling: whole report against partial report", color=BLUE, weight="bold", size=15)

GX, GY = 110, 206
for r in range(3):
    for c in range(4):
        col = GOLD if r == 1 else GREY
        d.rect(GX + c * 36, GY + r * 34, 30, 28, col, FILL[col] if r == 1 else "#faf6ee", rx=4, width=1.8)
        d.text(GX + c * 36 + 15, GY + r * 34 + 20, "X", color=col, weight="bold", size=14)
d.text(GX + 72, GY - 10, "50 ms flash", color=GREY, size=12)
d.arrow(GX + 152, GY + 48, GX + 184, GY + 48, GOLD, width=2)
d.text(GX + 168, GY + 36, "tone", color=GOLD, weight="bold", size=12)

d.rect(306, 206, 132, 46, GREY, "#e9e4da", rx=8, width=2)
d.text(372, 226, "whole report", color=GREY, weight="bold", size=12)
d.text(372, 244, "4–5 of 12", color=NAVY, weight="bold", size=14)
d.rect(306, 262, 132, 46, GOLD, FILL[GOLD], rx=8, width=2)
d.text(372, 282, "partial report", color=GOLD, weight="bold", size=12)
d.text(372, 300, "3 of 4 ⇒ ≈9 of 12", color=NAVY, weight="bold", size=13)

d.text(250, 352, "the limit is not how much was seen", color=NAVY, weight="bold", size=14)
d.text(250, 376, "but how fast the image fades while you report it", color=GREY, size=13)
d.text(250, 404, "the store is pre-categorical: raw form, not yet \"letters\"",
       color=GREY, size=12)

# ---------------- Panel B: decay curve ----------------
d.rect(480, 156, 400, 274, GOLD, "none", rx=12, width=2)
d.text(680, 184, "Why the cue has to come at once", color=GOLD, weight="bold", size=15)

m = d.axes(548, 206, 290, 134, "delay before the cue (s)", "letters available",
           (0, 1.1), (0, 10), ticks_x=[0, 0.5, 1], ticks_y=[5, 9])
d.curve(m, [(t / 100, 4.5 + 4.5 * math.exp(-(t / 100) / 0.32)) for t in range(0, 111)], GOLD, 2.8)
px, py = m(0, 9)
d.circle(px, py, 5, NAVY, NAVY)
d.text(px + 10, py - 8, "≈ 9 available", anchor="start", color=NAVY, weight="bold", size=12)
px, py = m(1.0, 4.65)
d.text(px - 8, py - 12, "back to whole-report level", anchor="end", color=GREY, size=12)

d.text(680, 414, "iconic ≈ 250–500 ms • echoic ≈ 3–4 s • haptic ≈ 2 s",
       color=NAVY, weight="bold", size=14)

# ---------------- Panel C: the three filters ----------------
d.rect(40, 446, 840, 212, SAGE, "none", rx=12, width=2)
d.text(460, 474, "Where does the bottleneck sit?", color=SAGE, weight="bold", size=16)

LY = 560
d.line(120, LY, 800, LY, GREY, 3)
for x, lab in [(120, "sensory\ninput"), (360, "physical\nfeatures"), (580, "meaning\nextracted"), (800, "awareness,\nresponse")]:
    d.circle(x, LY, 6, NAVY, NAVY)
    a, b = lab.split("\n")
    d.text(x, LY + 26, a, color=GREY, size=12)
    d.text(x, LY + 42, b, color=GREY, size=12)

models = [(300, "Broadbent", "filter: unattended\nchannels blocked", BLUE),
          (440, "Treisman", "attenuator: turned\ndown, not off", GOLD),
          (680, "Deutsch–Norman", "late: everything\nanalysed first", RED)]
for x, name, note, col in models:
    d.line(x, LY - 20, x, LY - 6, col, 3, True)
    d.text(x, LY - 30, name, color=col, weight="bold", size=13)
    a, b = note.split("\n")
    d.text(x, LY - 66, a, color=GREY, size=11)
    d.text(x, LY - 50, b, color=GREY, size=11)

d.text(460, 626, "Lavie: the bottleneck slides — early when the task is demanding, late when it is easy",
       color=NAVY, weight="bold", size=14)
d.text(460, 648, "your own name getting through is the evidence against a hard early filter",
       color=GREY, size=12)

# ---------------- Panel D: failures of attention ----------------
d.rect(40, 674, 840, 174, RED, "none", rx=12, width=2)
d.text(460, 702, "What happens to what you do not attend to", color=RED, weight="bold", size=16)

fails = [("inattentional blindness", "the gorilla walks through\nand you never see it"),
         ("change blindness", "a large change across a cut\ngoes unregistered"),
         ("psychological refractory period", "two responses in quick succession:\nthe second always waits"),
         ("vigilance decrement", "watch for a rare signal long enough\nand you start missing it")]
x = 62
for name, note in fails:
    d.rect(x, 720, 196, 104, RED, FILL[RED], rx=10, width=2)
    d.text(x + 98, 746, name, color=RED, weight="bold", size=12)
    a, b = note.split("\n")
    d.text(x + 98, 776, a, color=NAVY, size=11)
    d.text(x + 98, 794, b, color=NAVY, size=11)
    x += 206

d.save("sensory-memory-and-the-attention-bottleneck")
print("ok")
