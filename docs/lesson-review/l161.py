import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 790,
      "Impulse is the area; momentum is the thing that survives",
      "Same Δp spread over a longer time means a smaller average force",
      "Left: a force-versus-time graph with two pulses of equal area, a tall narrow one for a hard landing and a low "
      "wide one for a padded landing, showing that the same change in momentum can be delivered by a large force for "
      "a short time or a small force for a long time. Right: a table of collision types showing that momentum is "
      "conserved in all of them while kinetic energy is conserved only in elastic collisions. Bottom: the condition "
      "for conservation, the two separate steps of the ballistic pendulum, and the equal-mass elastic special cases.")

# ---------------- Panel A: impulse as area ----------------
d.rect(40, 112, 430, 356, RED, "none", rx=12, width=2)
d.text(255, 142, "Same area, different peak", color=RED, weight="bold", size=17)

f = d.axes(96, 178, 330, 174, "time", "force", xr=(0, 10), yr=(0, 10),
           ticks_x=[], ticks_y=[])

hard = [(0, 0), (1.5, 9), (3, 0)]
soft = [(3, 0), (6.5, 3.86), (10, 0)]
d.path("M" + " L".join(f"{f(a, b)[0]:.1f} {f(a, b)[1]:.1f}" for a, b in hard) + " Z",
       RED, 2.5, FILL[RED])
d.path("M" + " L".join(f"{f(a, b)[0]:.1f} {f(a, b)[1]:.1f}" for a, b in soft) + " Z",
       SAGE, 2.5, FILL[SAGE])

d.text(f(1.5, 5.0)[0], f(1.5, 5.0)[1], "J", color=RED, weight="bold", size=17)
d.text(f(6.5, 1.7)[0], f(6.5, 1.7)[1], "J", color=SAGE, weight="bold", size=17)
d.text(f(1.5, 9.9)[0], f(1.5, 9.9)[1], "hard landing", color=RED, weight="bold", size=14)
d.text(f(6.5, 5.0)[0], f(6.5, 5.0)[1], "airbag, padding, bent knees",
       color=SAGE, weight="bold", size=14)

d.text(255, 428, "J = area under F–t = Δp = mvᶠ − mvᵢ", color=NAVY, weight="bold", size=16)
d.text(255, 452, "F_avg = Δp / Δt — fix Δp, stretch Δt, and F falls", color=GREY, size=15)

# ---------------- Panel B: collision types ----------------
d.rect(486, 112, 394, 356, BLUE, "none", rx=12, width=2)
d.text(683, 142, "What survives each collision", color=BLUE, weight="bold", size=17)

rows = [("elastic", "p ✓   KE ✓", "steel balls, molecules", SAGE),
        ("inelastic", "p ✓   KE ✗", "most real collisions", GOLD),
        ("perfectly inelastic", "p ✓   KE ✗ (max loss)", "they stick: vᶠ = Σmv / Σm", RED),
        ("explosion / recoil", "p ✓   KE rises", "starts at rest: Σp stays 0", BLUE)]
y = 168
for name, cons, note, col in rows:
    d.rect(506, y, 356, 60, col, FILL[col], rx=9, width=2)
    d.text(524, y + 24, name, anchor="start", color=col, weight="bold", size=16)
    d.text(844, y + 24, cons, anchor="end", color=NAVY, weight="bold", size=15)
    d.text(524, y + 46, note, anchor="start", color=GREY, size=13)
    y += 68

d.text(683, 452, "Momentum is conserved in every row; kinetic energy only in the first",
       color=BLUE, weight="bold", size=14)

# ---------------- Bottom ----------------
bottom = [(40, "When is p conserved?", NAVY,
           ["ΣF_external = 0", "internal forces cancel in pairs",
            "brief collisions: gravity's", "impulse is negligible"]),
          (320, "Ballistic pendulum: 2 steps", GOLD,
           ["1. collision: mv = (m+M)v′", "2. swing: ½(m+M)v′² = (m+M)gh",
            "never carry KE across", "the collision itself"]),
          (600, "Equal masses, elastic", SAGE,
           ["head-on: they swap velocities", "glancing: they separate at 90°",
            "light vs heavy wall: bounces", "back at nearly the same speed"])]
for x, head, col, lines in bottom:
    d.rect(x, 498, 280, 162, col, FILL[col], rx=10, width=2)
    d.text(x + 140, 528, head, color=col, weight="bold", size=16)
    for i, ln in enumerate(lines):
        d.text(x + 140, 558 + i * 26, ln, color=NAVY if i == 0 else GREY,
               weight="bold" if i == 0 else None, size=15 if i == 0 else 13)

d.text(460, 706, "p = mv is a vector: a reversal flips its sign, so Δp can exceed either momentum alone",
       color=NAVY, weight="bold", size=16)
d.text(460, 738, "A ball hitting 40 m/s and leaving at 50 m/s the other way changes by 90 m/s worth, not 10",
       color=GREY, size=15)
d.text(460, 768, "Units: kg·m/s = N·s", color=GREY, size=15)

d.save("impulse-area-and-collision-types")
print("ok")
