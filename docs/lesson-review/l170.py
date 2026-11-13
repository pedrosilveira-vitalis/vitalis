import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 820,
      "From air to fluid to a nerve impulse",
      "The middle ear fixes an impedance mismatch; the cochlea turns frequency into position",
      "Top: the chain from ear canal to cochlea, with the canal resonating near 3.4 kilohertz, the eardrum's 55 square "
      "millimetres concentrated onto the oval window's 3.2, and the ossicular lever adding another factor, together "
      "worth roughly 20 to 30 decibels. Bottom left: the uncoiled cochlea, narrow and stiff at the base where high "
      "frequencies peak and wide and floppy at the apex where low frequencies peak. Bottom right: the hair cell "
      "cascade, from stereocilia bending through potassium entry from endolymph to glutamate release onto the "
      "cochlear nerve, with the outer hair cells amplifying through prestin.")

# ---------------- Panel A: the chain ----------------
d.rect(40, 112, 840, 230, BLUE, "none", rx=12, width=2)
d.text(460, 142, "Why the middle ear exists", color=BLUE, weight="bold", size=17)

stages = [(80, "ear canal", "≈2.5 cm, a closed pipe", "resonates ≈ 3.4 kHz", SAGE),
          (272, "eardrum", "area ≈ 55 mm²", "collects the force", NAVY),
          (464, "ossicles", "lever ≈ 1.3×", "malleus–incus–stapes", GOLD),
          (656, "oval window", "area ≈ 3.2 mm²", "17–20× the pressure", RED)]
for x, name, line2, line3, col in stages:
    d.rect(x, 172, 168, 94, col, FILL[col], rx=9, width=2)
    d.text(x + 84, 198, name, color=col, weight="bold", size=16)
    d.text(x + 84, 222, line2, color=NAVY, size=14)
    d.text(x + 84, 244, line3, color=GREY, size=12)
    if x < 600:
        d.arrow(x + 170, 219, x + 190, 219, NAVY, width=2.5)
d.arrow(826, 219, 858, 219, NAVY, width=2.5)
d.text(846, 268, "cochlea", color=NAVY, weight="bold", size=13)

d.text(460, 296, "Air meets fluid: without this stage ≈ 99.9% of the energy would reflect",
       color=NAVY, weight="bold", size=15)
d.text(460, 322, "area ratio × lever ⇒ a pressure gain worth roughly 20–30 dB",
       color=GREY, size=14)

# ---------------- Panel B: tonotopy ----------------
d.rect(40, 362, 416, 300, GOLD, "none", rx=12, width=2)
d.text(248, 392, "The cochlea, uncoiled", color=GOLD, weight="bold", size=17)

BX0, BX1, BY = 80, 420, 470
d.path(f"M{BX0} {BY - 10} L{BX1} {BY - 34} L{BX1} {BY + 34} L{BX0} {BY + 10} Z", GOLD, 2, FILL[GOLD])
d.text(BX0 - 8, BY + 4, "base", anchor="end", color=NAVY, weight="bold", size=14)
d.text(BX1 + 8, BY + 4, "apex", anchor="start", color=NAVY, weight="bold", size=14)
d.text(BX0 + 34, BY + 52, "narrow, stiff", color=GREY, size=12)
d.text(BX1 - 40, BY + 60, "wide, floppy", color=GREY, size=12)

for frac, lab, col in [(0.08, "20 kHz", RED), (0.45, "2 kHz", GOLD), (0.9, "20 Hz", SAGE)]:
    x = BX0 + frac * (BX1 - BX0)
    d.line(x, BY - 26, x, BY + 26, col, 2.5)
    d.text(x, BY - 46, lab, color=col, weight="bold", size=13)

wave = [(BX0 + i * 3.4, BY + 86 - 26 * math.exp(-((i - 48) / 22) ** 2) * math.sin(i / 2.4))
        for i in range(0, 101)]
d.path("M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in wave), BLUE, 2)
d.text(248, 598, "the wave peaks where the membrane matches the tone",
       color=BLUE, weight="bold", size=14)
d.text(248, 626, "noise and ageing hit the base first: high tones go first",
       color=GREY, size=14)

# ---------------- Panel C: the hair cell ----------------
d.rect(472, 362, 408, 300, SAGE, "none", rx=12, width=2)
d.text(676, 392, "How bending becomes firing", color=SAGE, weight="bold", size=17)

steps = [("stereocilia bend", "shear against the tectorial membrane"),
         ("tip links pull open K⁺ channels", "endolymph is the rare high-K⁺ fluid"),
         ("K⁺ flows in", "+80 mV endolymph vs −70 mV cell ⇒ 150 mV push"),
         ("Ca²⁺ enters, glutamate out", "onto the cochlear nerve, CN VIII")]
y = 404
for head, note in steps:
    d.text(498, y + 16, head, anchor="start", color=NAVY, weight="bold", size=15)
    d.text(498, y + 36, note, anchor="start", color=GREY, size=12)
    if head.startswith("Ca"):
        break
    d.arrow(508, y + 44, 508, y + 56, SAGE, width=2)
    y += 52

d.rect(492, 604, 376, 48, RED, FILL[RED], rx=9, width=2)
d.text(680, 624, "Outer hair cells amplify by 40–50 dB using prestin;", color=RED, weight="bold", size=13)
d.text(680, 642, "lose them and the loss is sensorineural, not conductive", color=RED, weight="bold", size=13)

d.text(460, 700, "Open pipe: fₙ = nv/2L, every n   •   Closed pipe: fₙ = nv/4L, odd n only",
       color=NAVY, weight="bold", size=16)
d.text(460, 732, "A closed pipe sounds an octave below an open pipe of the same length",
       color=GREY, size=15)
d.text(460, 762, "Beats: f = |f₁ − f₂|, the trick behind tuning and Doppler flow probes",
       color=GREY, size=15)
d.text(460, 792, "Conductive loss spares the cochlea; sensorineural loss starts at high frequencies",
       color=GREY, size=15)

d.save("ear-impedance-and-tonotopy")
print("ok")
