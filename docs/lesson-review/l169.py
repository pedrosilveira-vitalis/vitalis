import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 830,
      "Decibels count factors of ten; the Doppler shift counts closing speed",
      "β = 10 log(I/I₀), I = P/4πr², and approaching always raises the pitch",
      "Top left: a decibel ladder from the threshold of hearing at 0 dB to the threshold of pain at 120 dB, with the "
      "intensity beside each level and the rules that ten times the intensity adds 10 dB and twice the intensity "
      "adds 3 dB. Top right: the inverse square law drawn as spreading spheres, with intensity falling to a quarter "
      "at twice the distance and a ninth at three times. Bottom left: a moving source with its wavefronts bunched "
      "ahead and stretched behind, with the Doppler formula and its sign rule. Bottom right: Doppler ultrasound, "
      "with the cosine factor, the impedance mismatch that makes gel necessary, and the pulse-echo depth formula.")

# ---------------- Panel A: decibel ladder ----------------
d.rect(40, 112, 416, 326, GOLD, "none", rx=12, width=2)
d.text(248, 142, "The decibel ladder", color=GOLD, weight="bold", size=17)

rungs = [(120, "threshold of pain", "1 W/m²", RED),
         (85, "damage with exposure", "10⁻³·⁵", GOLD),
         (60, "conversation", "10⁻⁶", NAVY),
         (30, "quiet library", "10⁻⁹", NAVY),
         (0, "threshold of hearing", "10⁻¹² W/m²", SAGE)]
TOPY, BOTY = 180, 350
d.line(150, TOPY - 10, 150, BOTY + 10, NAVY, 2)
for lvl, name, inten, col in rungs:
    y = BOTY - (lvl / 120) * (BOTY - TOPY)
    d.line(142, y, 158, y, col, 3)
    d.text(136, y + 5, f"{lvl} dB", anchor="end", color=col, weight="bold", size=14)
    d.text(168, y + 1, name, anchor="start", color=NAVY, size=13)
    d.text(168, y + 16, inten, anchor="start", color=GREY, size=11)

d.rect(62, 372, 372, 50, GOLD, FILL[GOLD], rx=9, width=2)
d.text(248, 392, "×10 intensity ⇒ +10 dB   •   ×2 ⇒ +3 dB   •   ×4 ⇒ +6 dB",
       color=NAVY, weight="bold", size=14)
d.text(248, 412, "two 60 dB sources make 63 dB, never 120", color=RED, weight="bold", size=13)

# ---------------- Panel B: inverse square ----------------
d.rect(472, 112, 408, 326, BLUE, "none", rx=12, width=2)
d.text(676, 142, "Spreading over a bigger sphere", color=BLUE, weight="bold", size=17)

SX, SY = 520, 290
d.circle(SX, SY, 7, RED, RED)
for k, (r, lab, drop) in enumerate([(46, "r", "I"), (92, "2r", "I/4"), (138, "3r", "I/9")]):
    d.path(f"M{SX + r * math.cos(math.radians(-32))} {SY + r * math.sin(math.radians(-32))} "
           f"A{r} {r} 0 0 1 {SX + r * math.cos(math.radians(32))} {SY + r * math.sin(math.radians(32))}",
           BLUE, 2.5)
    d.text(SX + r - 2, SY - r * 0.53 - 12, lab, color=GREY, weight="bold", size=13)
    d.text(SX + r - 4, SY + 6, drop, color=NAVY, weight="bold", size=15)

d.text(676, 386, "I = P / 4πr²", color=NAVY, weight="bold", size=17)
d.text(676, 410, "triple the distance ⇒ one ninth the intensity ⇒ −9.5 dB",
       color=GREY, size=14)
d.text(676, 430, "amplitude itself falls as 1/r, since I ∝ A²", color=GREY, size=14)

# ---------------- Panel C: Doppler ----------------
d.rect(40, 458, 416, 240, SAGE, "none", rx=12, width=2)
d.text(248, 486, "A moving source crowds its own waves", color=SAGE, weight="bold", size=17)

CY = 580
for k in range(5):
    cx = 150 + k * 17
    r = 64 - k * 13
    d.circle(cx, CY, r, GREY, "none", width=1.6)
d.circle(214, CY, 7, RED, RED)
d.arrow(224, CY, 264, CY, RED, width=2.5)
d.text(272, CY + 5, "v_s", anchor="start", color=RED, weight="bold", size=14)
d.text(296, 502, "crowded: higher pitch", anchor="start", color=NAVY, weight="bold", size=13)

d.text(62, 502, "stretched: lower pitch", anchor="start", color=GREY, weight="bold", size=13)


d.text(248, 652, "f_obs = fₛ (v ± v_o) / (v ∓ v_s)", color=NAVY, weight="bold", size=16)
d.text(248, 676, "pick the signs that make approaching raise f", color=GREY, size=14)

# ---------------- Panel D: ultrasound ----------------
d.rect(472, 458, 408, 240, RED, "none", rx=12, width=2)
d.text(676, 486, "Why the gel, and what the angle costs", color=RED, weight="bold", size=17)

d.rect(496, 508, 46, 58, NAVY, FILL[NAVY], rx=5, width=2)
d.text(519, 580, "probe", color=GREY, size=12)
d.rect(548, 508, 300, 58, BLUE, FILL[BLUE], rx=5, width=2)
d.text(700, 532, "tissue  Z ≈ 1.5 × 10⁶ rayl", color=NAVY, weight="bold", size=13)
d.text(700, 554, "air Z ≈ 400 rayl ⇒ almost all of it reflects", color=RED, size=12)
d.arrow(548, 596, 700, 596, NAVY, width=2)
d.arrow(700, 612, 548, 612, GREY, width=2)
d.text(716, 600, "pulse", anchor="start", color=NAVY, size=12)
d.text(716, 618, "echo", anchor="start", color=GREY, size=12)

d.text(676, 650, "Δf = 2fₛ·v·cosθ / c   —   θ = 90° shows no flow at all",
       color=NAVY, weight="bold", size=14)
d.text(676, 676, "depth d = v·t/2, with v ≈ 1,540 m/s in soft tissue", color=GREY, size=14)

d.text(460, 740, "Sound needs a medium and is longitudinal; 0 dB is the faintest audible, not silence",
       color=NAVY, weight="bold", size=16)
d.text(460, 772, "Higher ultrasound frequency buys resolution and loses depth — the two always trade",
       color=GREY, size=15)
d.text(460, 802, "Murmurs, bruits and Korotkoff sounds are turbulence; S1 and S2 are valves closing",
       color=GREY, size=15)

d.save("decibels-inverse-square-and-doppler")
print("ok")
