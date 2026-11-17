import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 920,
      "Not how much motivation, but what kind",
      "The exam asks which theory explains a vignette — so learn what each one is for",
      "Top: Maslow's ladder, which answers \"which need is in charge right now\" and is the right tool for any "
      "vignette about deprivation — a patient who is food-insecure is not going to be moved by a lecture "
      "on long-term risk. Middle: the self-determination continuum, which is the real contribution of the "
      "theory. Motivation is not a switch between intrinsic and extrinsic; there are degrees of taking a "
      "reason inside yourself, and the two middle grades — doing it because you value the result, or "
      "because it is simply who you are — behave far more like intrinsic motivation than like being paid. "
      "Bottom left: why paying someone for something they already loved can backfire. Bottom right: the "
      "expectancy-value product, which is the tool for asking why someone capable does not even try."
      )

# ---------------- Panel A: Maslow ----------------
d.rect(40, 178, 420, 322, SAGE, "none", rx=12, width=2)
d.text(250, 206, "Maslow: which need is in charge", color=SAGE, weight="bold", size=15)

levels = [
    ("SELF-ACTUALISATION", "growth · becoming", SAGE, 120),
    ("ESTEEM", "mastery, recognition", BLUE, 180),
    ("LOVE AND BELONGING", "connection", GOLD, 240),
    ("SAFETY", "security, stability", RED, 300),
    ("PHYSIOLOGICAL", "food, water, sleep", GREY, 360),
]
y = 232
for name, note, col, w in levels:
    x = 250 - w / 2
    d.rect(x, y, w, 44, col, FILL[col], rx=7, width=2)
    d.text(250, y + 20, name, color=col, weight="bold", size=11)
    d.text(250, y + 36, note, color=GREY, size=10)
    y += 48

d.text(250, 490, "the bottom four are deficiency needs — they push from lack",
       color=NAVY, size=11)

# ---------------- Panel B: SDT continuum ----------------
d.rect(480, 178, 400, 322, BLUE, "none", rx=12, width=2)
d.text(680, 206, "Self-determination: degrees of owning it", color=BLUE, weight="bold", size=15)

steps = [
    ("AMOTIVATION", "why bother; nothing I do matters", GREY),
    ("EXTERNAL", "for the reward, or to dodge the punishment", RED),
    ("INTROJECTED", "to avoid guilt or protect my pride", RED),
    ("IDENTIFIED", "I don't enjoy it, but I value what it gets me", SAGE),
    ("INTEGRATED", "it is simply part of who I am", SAGE),
    ("INTRINSIC", "the doing is the reward", BLUE),
]
y = 230
for name, note, col in steps:
    d.rect(508, y, 344, 36, col, FILL[col], rx=7, width=2)
    d.text(680, y + 16, name, color=col, weight="bold", size=11)
    d.text(680, y + 30, note, color=GREY, size=10)
    y += 40

d.arrow(494, 450, 494, 236, GREY, width=2)
d.text(680, 486, "the two green bands are extrinsic — and behave almost like intrinsic",
       color=NAVY, size=11)

# ---------------- Panel C: overjustification ----------------
d.rect(40, 520, 420, 360, GOLD, "none", rx=12, width=2)
d.text(250, 548, "Why paying can backfire", color=GOLD, weight="bold", size=15)

seq = [
    ("the child draws for fun", "internal reason", SAGE),
    ("a prize is promised for drawing", "an external reason appears", GOLD),
    ("“I draw to get prizes”", "the perceived cause moves outward", RED),
    ("prize withdrawn → less drawing", "than children never rewarded", RED),
]
y = 572
for a, b, col in seq:
    d.rect(66, y, 368, 52, col, FILL[col], rx=8, width=2)
    d.text(250, y + 22, a, color=col, weight="bold", size=12)
    d.text(250, y + 40, b, color=GREY, size=10)
    if y < 740:
        d.arrow(250, y + 52, 250, y + 60, GREY, width=1.6)
    y += 62

d.text(250, 836, "what decides it is whether the reward feels CONTROLLING", color=NAVY, weight="bold", size=11)
d.text(250, 854, "or merely INFORMATIVE about how well you did", color=NAVY, weight="bold", size=11)
d.text(250, 872, "unexpected rewards and honest praise rarely hurt", color=GREY, size=10)

# ---------------- Panel D: expectancy-value ----------------
d.rect(480, 520, 400, 360, RED, "none", rx=12, width=2)
d.text(680, 548, "Expectancy × Value", color=RED, weight="bold", size=15)

d.rect(508, 568, 344, 56, RED, FILL[RED], rx=9, width=2)
d.text(680, 604, "zero in either → zero motivation", color=NAVY, weight="bold", size=14)

d.text(680, 650, "EXPECTANCY — can I do it?", color=BLUE, weight="bold", size=13)
d.text(680, 672, "self-efficacy, built mainly by past mastery", color=GREY, size=11)
d.text(680, 690, "then by seeing people like you succeed", color=GREY, size=11)

d.text(680, 724, "VALUE — is it worth it?", color=GOLD, weight="bold", size=13)
for i, (a, b) in enumerate([("interest", "do I enjoy it"),
                            ("attainment", "does it fit who I am"),
                            ("utility", "will it get me somewhere"),
                            ("cost", "subtract time, effort, dread")]):
    d.text(672, 748 + i * 20, a, anchor="end", color=NAVY, weight="bold", size=11)
    d.text(682, 748 + i * 20, b, anchor="start", color=GREY, size=11)

d.text(680, 848, "capable but not trying → look at value", color=RED, weight="bold", size=11)
d.text(680, 866, "willing but not starting → look at expectancy", color=RED, weight="bold", size=11)

d.save("maslow-sdt-continuum-and-expectancy-value")
print("ok")
