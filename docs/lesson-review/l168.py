import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 830,
      "The source picks f, the medium picks v, and λ has no say",
      "v = fλ — so crossing into a new medium changes λ, never the frequency",
      "Top left: a transverse wave labelled with crest, trough, amplitude and wavelength, above a longitudinal wave "
      "shown as alternating compressions and rarefactions. Top right: what each property is set by, and what happens "
      "when a wave crosses into a new medium — frequency unchanged, speed set by the new medium, wavelength following "
      "from v = f lambda. Bottom left: standing wave harmonics for a string or open pipe, where every harmonic is "
      "allowed and the fundamental wavelength is twice the length, against a closed pipe, where only odd harmonics "
      "fit and the fundamental wavelength is four times the length. Bottom right: the numbers to carry.")

# ---------------- Panel A: wave anatomy ----------------
d.rect(40, 112, 416, 330, BLUE, "none", rx=12, width=2)
d.text(248, 142, "Reading a wave", color=BLUE, weight="bold", size=17)

X0, MID, AMP, WL = 86, 228, 42, 150
pts = [(X0 + i, MID - AMP * math.sin(2 * math.pi * i / WL)) for i in range(0, 311, 3)]
d.line(X0, MID, X0 + 310, MID, GREY, 1.5, True)
d.path("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts), NAVY, 3)

d.arrow(X0 + 37, MID, X0 + 37, MID - AMP, RED, width=2)
d.text(X0 + 46, MID - AMP / 2 + 5, "A", anchor="start", color=RED, weight="bold", size=16)
d.line(X0 + 37, MID - AMP - 10, X0 + 187, MID - AMP - 10, SAGE, 2)
d.text(X0 + 112, MID - AMP - 18, "λ", color=SAGE, weight="bold", size=17)
d.text(X0 + 37, MID - AMP - 34, "crest", color=GREY, size=12)
d.text(X0 + 112, MID + AMP + 22, "trough", color=GREY, size=12)

d.text(248, 320, "longitudinal (sound): the same wave, drawn as density",
       color=GREY, weight="bold", size=14)
y0 = 340
for i in range(60):
    x = 92 + i * 5.2
    dens = 0.5 + 0.5 * math.cos(2 * math.pi * (x - 92) / 160)
    if dens > 0.45:
        for k in range(3):
            d.line(x, y0 + 6 + k * 12, x, y0 + 14 + k * 12, NAVY, 1.2 + dens)
d.text(172, y0 + 58, "rarefaction", color=GREY, weight="bold", size=12)
d.text(252, y0 + 58, "compression", color=NAVY, weight="bold", size=12)
d.text(332, y0 + 58, "rarefaction", color=GREY, weight="bold", size=12)

d.text(248, 428, "A sets energy (E ∝ A²); f sets pitch and colour",
       color=NAVY, weight="bold", size=15)

# ---------------- Panel B: who sets what ----------------
d.rect(472, 112, 408, 330, SAGE, "none", rx=12, width=2)
d.text(676, 142, "Who decides each quantity", color=SAGE, weight="bold", size=17)

rows = [("frequency f", "the source", SAGE), ("speed v", "the medium", BLUE),
        ("wavelength λ", "whatever v = fλ requires", GOLD)]
y = 170
for name, who, col in rows:
    d.rect(494, y, 364, 52, col, FILL[col], rx=9, width=2)
    d.text(512, y + 32, name, anchor="start", color=col, weight="bold", size=16)
    d.text(840, y + 32, who, anchor="end", color=NAVY, size=15)
    y += 60

d.rect(494, 354, 364, 72, RED, FILL[RED], rx=9, width=2)
d.text(676, 380, "Crossing into a new medium", color=RED, weight="bold", size=15)
d.text(676, 404, "f stays • v changes • λ follows: λ₂ = λ₁ · v₂/v₁",
       color=NAVY, weight="bold", size=15)

# ---------------- Panel C: harmonics ----------------
d.rect(40, 462, 416, 240, GOLD, "none", rx=12, width=2)
d.text(248, 490, "Which harmonics fit", color=GOLD, weight="bold", size=17)


def mode(x0, x1, y, n, closed=False):
    d.line(x0, y, x1, y, GREY, 1, True)
    L = x1 - x0
    pts = []
    for i in range(0, 101):
        xx = x0 + L * i / 100
        frac = i / 100
        if closed:
            amp = math.sin((2 * n - 1) * math.pi * frac / 2)
        else:
            amp = math.sin(n * math.pi * frac)
        pts.append((xx, y - 17 * amp))
    d.path("M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts), NAVY, 2)
    pts2 = [(a, 2 * y - b) for a, b in pts]
    d.path("M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts2), NAVY, 2)


d.text(132, 518, "string / open pipe", color=SAGE, weight="bold", size=14)
for i, n in enumerate((1, 2, 3)):
    mode(66, 198, 548 + i * 44, n)
    d.text(208, 553 + i * 44, f"n={n}", anchor="start", color=GREY, size=12)
d.text(132, 684, "λ₁ = 2L, every n", color=NAVY, weight="bold", size=14)

d.text(356, 518, "closed pipe", color=RED, weight="bold", size=14)
for i, n in enumerate((1, 2, 3)):
    mode(290, 422, 548 + i * 44, n, closed=True)
    d.text(432, 553 + i * 44, f"n={2 * n - 1}", anchor="start", color=GREY, size=12)
d.text(356, 684, "λ₁ = 4L, odd n only", color=NAVY, weight="bold", size=14)

# ---------------- Panel D: numbers ----------------
d.rect(472, 462, 408, 240, BLUE, "none", rx=12, width=2)
d.text(676, 490, "Numbers to carry", color=BLUE, weight="bold", size=17)

vals = [("sound in air (20°C)", "343 m/s"), ("sound in water", "≈1,480 m/s"),
        ("light in vacuum", "3.0 × 10⁸ m/s"), ("human hearing", "20 Hz – 20 kHz"),
        ("visible light", "400–700 nm"), ("threshold of hearing", "10⁻¹² W/m² = 0 dB")]
y = 520
for name, val in vals:
    d.text(498, y, name, anchor="start", color=GREY, size=14)
    d.text(854, y, val, anchor="end", color=NAVY, weight="bold", size=14)
    y += 28
d.text(676, 688, "+10 dB = 10× the intensity   •   I = P/4πr²",
       color=NAVY, weight="bold", size=14)

d.text(460, 742, "Beats: |f₁ − f₂|   •   constructive ΔL = nλ   •   destructive ΔL = (n + ½)λ",
       color=NAVY, weight="bold", size=16)
d.text(460, 774, "Doppler: approaching raises the pitch, receding lowers it — f_obs = f(v + v_o)/(v − v_s)",
       color=GREY, size=15)
d.text(460, 804, "Sound is longitudinal and needs a medium; light is transverse and does not",
       color=GREY, size=15)

d.save("wave-anatomy-and-harmonics")
print("ok")
