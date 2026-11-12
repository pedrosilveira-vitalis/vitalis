import sys, math; sys.path.insert(0,'/home/claude/dkit')
from dkit import *

def profile(anchors):
    def f(x):
        for i in range(len(anchors)-1):
            x0,y0 = anchors[i]; x1,y1 = anchors[i+1]
            if x0 <= x <= x1:
                if x1 == x0: return y0
                t = (x-x0)/(x1-x0)
                return y0 + (y1-y0)*((1-math.cos(math.pi*t))/2)
        return anchors[-1][1]
    return f

K = profile([(0,50),(1.6,50),(3.1,76),(5.0,36),(6,36)])
T = profile([(0,50),(1.6,50),(3.1,93),(5.0,17),(6,17)])

d = D(1180, 850, "Fastest is not the same as most stable",
      "When a reaction can give two products, the conditions decide which one you isolate — and the two answers are different compounds.",
      "An energy against reaction coordinate plot shows one set of reactants at 50 branching into two routes. The kinetic route climbs a low barrier to 76 and falls to a shallow product at 36. The thermodynamic route climbs a higher barrier to 93 and falls to a deeper product at 17. So the kinetic product has the smaller activation energy and forms faster, while the thermodynamic product is the more stable of the two. Panels beside the plot set out which product you get under which conditions. Under kinetic control, with low temperature, short reaction time and irreversible conditions, the products cannot interconvert, the system is trapped where it landed first, and the product is the one over the lower barrier. Under thermodynamic control, with higher temperature, long reaction time and reversible conditions, the products can interconvert through the reactant, the system equilibrates, and the product is the more stable one. The deciding factor is whether the barrier back out of the kinetic well can be crossed in the time and at the temperature of the experiment. A worked case follows: hydrogen bromide added to 1,3-butadiene. At minus 80 degrees the 1,2 addition product dominates, which is the kinetic product because the proton adds to give an allylic cation that is captured fastest at the nearer carbon. At 40 degrees the 1,4 addition product dominates, which is the thermodynamic product because its double bond is internal and more substituted, and therefore more stable; neither product is conjugated. Footers note that a catalyst lowers both barriers and so speeds the approach to equilibrium without changing which product is the more stable one or where the equilibrium lies, and that enzymes work the other way, using exquisite transition state selectivity to hold a reaction under kinetic control and deliver one stereoisomer or regioisomer that simple equilibration would not favour.")

F = d.axes(64, 142, 560, 330, "reaction coordinate", "free energy", xr=(0,6), yr=(0,105), ticks_x=[], ticks_y=[])
d.curve(F, [(i/50, K(i/50)) for i in range(0, 301)], BLUE, 3)
d.curve(F, [(i/50, T(i/50)) for i in range(0, 301)], RED, 3)

rx, ry = F(0.55, 50); d.text(rx, ry+26, "reactants", color=GREY, size=11.5)
kx, ky = F(4.25, 36); d.text(kx, ky-16, "KINETIC \u00b7 forms faster", color=BLUE, size=12, weight=700)
tx, ty = F(4.25, 17); d.text(tx, ty-16, "THERMODYNAMIC \u00b7 more stable", color=RED, size=12, weight=700)
p2x, p2y = F(3.1, 93); d.text(p2x+34, p2y-8, "E\u2090 thermodynamic \u2014 higher", color=RED, size=11, weight=700, anchor="start")
ax, a50 = F(2.45, 50); _, a76 = F(2.45, 76)
d.arrow(ax, a50, ax, a76, BLUE, width=2)
d.text(ax+10, (a50+a76)/2, "E\u2090 kinetic \u2014 lower", color=BLUE, size=11, weight=700, anchor="start")
bx, b50 = F(1.45, 50); _, b93 = F(1.45, 93)
d.arrow(bx, b50, bx, b93, RED, width=2)

d.rect(648, 142, 504, 166, BLUE, FILL[BLUE], 12, 2)
d.text(900, 170, "KINETIC CONTROL", color=BLUE, weight=700, size=13)
for i, t in enumerate(["low temperature · short time · irreversible",
                       "the products cannot interconvert, so the system",
                       "is trapped wherever it landed first",
                       "→ you get the product over the LOWER barrier"]):
    d.text(672, 198 + i*24, t, color=NAVY, size=11.5,
           weight=700 if t.startswith("→") else 400, anchor="start")

d.rect(648, 322, 504, 166, RED, FILL[RED], 12, 2)
d.text(900, 350, "THERMODYNAMIC CONTROL", color=RED, weight=700, size=13)
for i, t in enumerate(["higher temperature · long time · reversible",
                       "the products can interconvert back through the",
                       "reactant, so the system equilibrates",
                       "→ you get the MORE STABLE product"]):
    d.text(672, 378 + i*24, t, color=NAVY, size=11.5,
           weight=700 if t.startswith("→") else 400, anchor="start")

d.box(648, 504, 504, 110, "The switch is one question",
      "Can the system climb back OUT of the kinetic well in the time and at the temperature of the experiment? If yes, thermodynamics wins. If no, whatever formed first is what you isolate.",
      NAVY, chars=66, size=12, head_size=13)

d.rect(24, 536, 600, 180, GOLD, FILL[GOLD], 12, 2)
d.text(324, 564, "THE WORKED CASE — HBr + 1,3-BUTADIENE", color=GOLD, weight=700, size=13)
rows = [("−80 °C", "1,2-addition", "KINETIC", BLUE,
         "the allylic cation is captured fastest at the nearer carbon"),
        ("40 °C", "1,4-addition", "THERMODYNAMIC", RED,
         "its double bond is internal and more substituted")]
yy = 594
for temp, prod, tag, c, why in rows:
    d.text(46, yy, temp, color=NAVY, size=12.5, weight=700, anchor="start")
    d.text(124, yy, prod, color=NAVY, size=12.5, weight=700, anchor="start")
    d.text(602, yy, tag, color=c, size=11.5, weight=700, anchor="end")
    d.text(124, yy+20, why, color=GREY, size=11, anchor="start")
    yy += 52
d.text(324, 700, "Neither product is conjugated — the 1,4 product wins on substitution, not conjugation.",
       color=GOLD, size=11.5, weight=700)

d.box(24, 740, 1128, 92, "Where a catalyst fits — and where an enzyme goes further",
      "A catalyst lowers BOTH barriers, so it speeds the approach to equilibrium without changing which product is the more stable or where the equilibrium lies. An enzyme exploits the opposite end: by stabilising one transition state and not the others it holds a reaction under kinetic control, delivering a single stereoisomer or regioisomer that plain equilibration would never favour.",
      NAVY, chars=148, size=12, head_size=13.5)
print(d.save("kinetic-vs-thermodynamic-control"))
