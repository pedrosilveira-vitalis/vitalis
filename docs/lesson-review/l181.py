import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 846,
      "Only a CHANGING flux induces anything",
      "Φ = BA cosθ — change B, change A or turn the loop, and Lenz decides which way the current runs",
      "Top left: magnetic flux as the field lines caught by a loop, maximum when the field is along the loop's "
      "normal and zero when the field lies in the plane of the loop, with the three ways flux can change. Top "
      "right: Lenz's law shown with a bar magnet approaching north pole first, the induced current running so "
      "that the loop presents a north pole back and pushes against the magnet. Middle: a straight wire's field "
      "circles it, so a loop lying in the same plane as the wire catches that field while a loop lying in a plane "
      "perpendicular to the wire catches none of it. Bottom: the transformer, with the turns ratio setting the "
      "voltage, power conserved so current moves the other way, and nothing at all happening on direct current."
      )

# ---------------- Panel A: flux ----------------
d.rect(40, 136, 420, 250, BLUE, "none", rx=12, width=2)
d.text(250, 164, "Flux = the field lines a loop catches", color=BLUE, weight="bold", size=15)

for cx, lab, ang, sub in [(150, "θ = 0°", 0, "Φ = BA (max)"),
                          (350, "θ = 90°", 1, "Φ = 0")]:
    if ang == 0:
        d.path(f"M{cx-52} 232 L{cx+52} 232 L{cx+30} 258 L{cx-74} 258 Z", NAVY, 2, FILL[BLUE])
        for x in range(cx - 48, cx + 50, 24):
            d.arrow(x - 10, 196, x - 10 + 0, 240, SAGE, width=1.6)
    else:
        d.rect(cx - 16, 196, 32, 62, NAVY, FILL[BLUE], rx=2, width=2)
        for y in range(206, 256, 16):
            d.arrow(cx - 60, y, cx + 60, y, SAGE, width=1.6)
    d.text(cx, 284, lab, color=NAVY, weight="bold", size=14)
    d.text(cx, 306, sub, color=BLUE, weight="bold", size=13)

d.text(250, 338, "three ways to change it: B, A, or θ", color=NAVY, weight="bold", size=14)
d.text(250, 362, "|EMF| = N · ΔΦ/Δt  —  a big steady field induces nothing",
       color=GREY, size=13)

# ---------------- Panel B: Lenz ----------------
d.rect(476, 136, 404, 250, RED, "none", rx=12, width=2)
d.text(678, 164, "Lenz: the loop pushes back", color=RED, weight="bold", size=15)

d.rect(560, 196, 86, 34, NAVY, FILL[NAVY], rx=4, width=2)
d.text(582, 219, "S", color=NAVY, weight="bold", size=17)
d.text(624, 219, "N", color=RED, weight="bold", size=17)
d.arrow(652, 213, 700, 213, NAVY, width=2.4)
d.text(676, 192, "moving in", color=NAVY, weight="bold", size=12)

d.path("M740 186 A 26 56 0 0 1 740 298", GOLD, 3)
d.path("M740 186 A 26 56 0 0 0 740 298", GOLD, 3, dash=True)
d.text(740, 320, "loop", color=GOLD, weight="bold", size=13)

d.text(678, 348, "flux toward the loop is rising, so the induced current",
       color=GREY, size=13)
d.text(678, 368, "makes a north pole facing the magnet — it repels",
       color=RED, weight="bold", size=13)

# ---------------- Panel C: wire and loops ----------------
d.rect(40, 406, 840, 212, SAGE, "none", rx=12, width=2)
d.text(460, 434, "A straight wire's field circles it — so orientation is everything",
       color=SAGE, weight="bold", size=16)

WX = 250
d.line(WX, 456, WX, 596, NAVY, 4)
d.arrow(WX, 520, WX, 486, NAVY, width=2)
d.text(WX, 448, "I", color=NAVY, weight="bold", size=15)
for yy in (478, 528, 578):
    d.text(WX + 60, yy + 5, "×", color=SAGE, weight="bold", size=19)
    d.text(WX - 60, yy + 5, "•", color=SAGE, weight="bold", size=22)
d.text(WX + 96, 470, "B into page", anchor="start", color=SAGE, size=12)
d.text(WX - 96, 470, "B out", anchor="end", color=SAGE, size=12)

d.rect(352, 496, 74, 70, BLUE, FILL[BLUE], rx=3, width=2.4)
d.text(389, 536, "X", color=BLUE, weight="bold", size=19)
d.text(400, 586, "same plane as the wire", color=BLUE, weight="bold", size=12)
d.text(389, 604, "field pierces it ⇒ EMF", color=NAVY, weight="bold", size=13)

d.path("M600 530 L690 506 L780 530 L690 554 Z", RED, 2.4, FILL[RED])
d.text(690, 536, "Y", color=RED, weight="bold", size=19)
d.text(690, 586, "plane ⊥ to the wire", color=RED, weight="bold", size=12)
d.text(690, 604, "field lies in its plane ⇒ no EMF", color=NAVY, weight="bold", size=13)

# ---------------- Panel D: transformer ----------------
d.rect(40, 638, 840, 196, GOLD, "none", rx=12, width=2)
d.text(460, 666, "Transformer: the turns ratio sets the voltage", color=GOLD, weight="bold", size=16)

d.rect(390, 688, 140, 92, GREY, "#e9e4da", rx=4, width=3)
d.text(460, 740, "iron core", color=GREY, weight="bold", size=12)
for y in range(698, 772, 18):
    d.path(f"M356 {y} q -22 9 0 18", BLUE, 2.4)
    d.path(f"M564 {y} q 22 9 0 18", RED, 2.4)
d.text(300, 712, "primary", anchor="end", color=BLUE, weight="bold", size=14)
d.text(300, 734, "N_p turns", anchor="end", color=BLUE, size=13)
d.text(620, 712, "secondary", anchor="start", color=RED, weight="bold", size=14)
d.text(620, 734, "N_s turns", anchor="start", color=RED, size=13)

d.text(460, 802, "V_s/V_p = N_s/N_p  •  V_pI_p = V_sI_s  •  step the voltage up and the current steps down",
       color=NAVY, weight="bold", size=14)
d.text(460, 828, "On DC the flux never changes, so a transformer does nothing at all",
       color=RED, weight="bold", size=15)

d.save("flux-faraday-lenz-and-the-transformer")
print("ok")
