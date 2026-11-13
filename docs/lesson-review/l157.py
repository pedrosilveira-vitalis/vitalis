import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 800,
      "Centripetal force: always inward, never a new force",
      "Name the physical force that supplies mv²/r, then set the inward sum equal to it",
      "Left: a circle with velocity arrows drawn tangentially and acceleration arrows drawn inward at four points, "
      "showing that v and a are perpendicular, with the relations v = 2 pi r over T and a = v squared over r. "
      "Right: four suppliers of the centripetal force — tension, gravity in orbit, the normal force on a banked "
      "curve, and friction on a flat turn — each with its equation. Bottom: the sign of the normal force at four "
      "points, inside the top of a loop, at the bottom of a loop, over the crest of a hill, and on a flat turn.")

# ---------------- Panel A: kinematics ----------------
d.rect(40, 112, 396, 356, BLUE, "none", rx=12, width=2)
d.text(238, 142, "v is tangential, a is radial", color=BLUE, weight="bold", size=17)

ox, oy, R = 238, 292, 104
d.circle(ox, oy, R, GREY, "none", width=2)
d.circle(ox, oy, 4, NAVY, NAVY)
for k in range(4):
    ang = math.radians(90 * k + 45)
    cx, cy = ox + R * math.cos(ang), oy - R * math.sin(ang)
    tx, ty = -math.sin(ang), -math.cos(ang)          # tangent (counter-clockwise on screen)
    d.arrow(cx, cy, cx + tx * 54, cy + ty * 54, SAGE, width=2.5)
    d.arrow(cx, cy, ox - (ox - cx) * 0.42, oy - (oy - cy) * 0.42, RED, width=2.5)
d.text(ox + 118, oy - 118, "v", color=SAGE, weight="bold", size=17)
d.text(ox + 26, oy - 34, "aᴄ", color=RED, weight="bold", size=17)
d.text(ox + 14, oy + R * 0.55, "r", anchor="start", color=NAVY, weight="bold", size=16)
d.line(ox, oy, ox, oy + R, NAVY, 1, True)

d.text(238, 424, "v = 2πr / T   •   aᴄ = v²/r = 4π²r/T²",
       color=NAVY, weight="bold", size=16)
d.text(238, 450, "speed constant, direction never is ⇒ always accelerating",
       color=GREY, size=14)

# ---------------- Panel B: who supplies it ----------------
d.rect(452, 112, 428, 356, SAGE, "none", rx=12, width=2)
d.text(666, 142, "Which real force is supplying mv²/r?", color=SAGE, weight="bold", size=17)

rows = [("string, ball on a table", "T = mv²/r", BLUE),
        ("gravity, satellite in orbit", "GMm/r² = mv²/r  ⇒  v = √(GM/r)", NAVY),
        ("normal force, banked curve", "N sinθ = mv²/r  ⇒  tanθ = v²/rg", GOLD),
        ("static friction, flat turn", "fₛ = mv²/r  ⇒  vₘₐₓ = √(μₛ rg)", RED),
        ("magnetic force, charge in B", "qvB = mv²/r  ⇒  r = mv/qB", GREY)]
y = 160
for label, eq, col in rows:
    d.rect(470, y, 392, 50, col, FILL[col], rx=9, width=2)
    d.text(486, y + 20, label, anchor="start", color=col, weight="bold", size=14)
    d.text(486, y + 40, eq, anchor="start", color=NAVY, size=15)
    y += 56

d.text(666, 452, "Fᴄ is the net inward force — never drawn as an extra arrow",
       color=SAGE, weight="bold", size=15)

# ---------------- Panel C: the sign of N ----------------
d.text(60, 506, "The sign of N depends on which side of the car the track is",
       anchor="start", color=RED, weight="bold", size=17)

panels = [("inside, top of loop", "track above", "N + mg = mv²/r", "N = 0 at v = √(gr)", RED),
          ("inside, bottom of loop", "track below", "N − mg = mv²/r", "N = mg + mv²/r: heavy", GOLD),
          ("crest of a hill", "track below", "mg − N = mv²/r", "N = mg − mv²/r: light", BLUE),
          ("flat turn", "track below", "fₛ = mv²/r", "N = mg: normal weight", SAGE)]
x = 40
for head, where, eq, note, col in panels:
    d.rect(x, 528, 200, 140, col, FILL[col], rx=10, width=2)
    d.text(x + 100, 556, head, color=col, weight="bold", size=15)
    d.text(x + 100, 578, where, color=GREY, size=13)
    d.text(x + 100, 612, eq, color=NAVY, weight="bold", size=15)
    d.text(x + 100, 644, note, color=NAVY, size=13)
    x += 213

d.text(460, 708, "Centre of the circle first, then add the inward forces as positive",
       color=NAVY, weight="bold", size=16)
d.text(460, 736, "Over a crest the centre is below the car, so gravity is the inward one",
       color=GREY, size=15)
d.text(460, 764, "Fᴄ does no work in uniform circular motion: it is ⊥ to v, so KE never changes",
       color=GREY, size=15)

d.save("centripetal-suppliers-and-signs")
print("ok")
