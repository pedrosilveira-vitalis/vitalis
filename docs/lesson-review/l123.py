import sys, math; sys.path.insert(0,'/home/claude/dkit')
from dkit import *

def profile(anchors):
    def f(x):
        for i in range(len(anchors)-1):
            x0,y0 = anchors[i]; x1,y1 = anchors[i+1]
            if x0 <= x <= x1:
                if x1 == x0: return y0
                t = (x-x0)/(x1-x0)
                s = (1-math.cos(math.pi*t))/2
                return y0 + (y1-y0)*s
        return anchors[-1][1]
    return f

UNCAT = profile([(0,40),(1.0,40),(2.6,100),(4.6,66),(6.4,86),(8.2,20),(10,20)])
CAT   = profile([(0,40),(1.0,40),(2.6,70),(4.6,58),(6.4,62),(8.2,20),(10,20)])

d = D(1180, 900, "The barrier, and what changes it",
      "Thermodynamics says whether. Kinetics says how fast. The barrier belongs to the mechanism — so a catalyst can move it, and ΔH cannot.",
      "A two-step reaction coordinate diagram plots potential energy against reaction progress. Reactants sit at 40, rise to a first transition state at 100, fall to an intermediate at 66, rise again to a second transition state at 86, and end as products at 20. The first barrier is the taller peak, so step one is rate determining. The forward activation energy is the climb from reactants to the highest peak, 60 kilojoules per mole; the reverse activation energy is the climb back from products to that same peak, 80; and the difference between them is the enthalpy change, minus 20. A dashed red curve shows the catalysed route over the same endpoints with both peaks lowered, which speeds the forward and the reverse directions alike and therefore leaves the enthalpy change and the equilibrium constant untouched. Panels beside it give the rules. Transition state against intermediate: a transition state is an energy maximum, cannot be isolated and lasts about ten to the minus thirteen seconds, while an intermediate is a local minimum between two transition states, is a real species and can sometimes be detected. The three quantities on the diagram are linked by the enthalpy change equals the forward activation energy minus the reverse activation energy, which holds whether the reaction is exothermic or endothermic; know any two and the third follows, and neither barrier is fixed by the enthalpy change alone. Below, an Arrhenius plot of the natural logarithm of the rate constant against the reciprocal of temperature is a straight line of slope minus activation energy over the gas constant and intercept the logarithm of the frequency factor, so activation energy equals minus the slope times the gas constant; a slope of minus nine thousand six hundred kelvin gives seventy nine point eight kilojoules per mole. The last panel converts a change in barrier height into a change in rate: at body temperature every factor of ten in rate costs about five point nine kilojoules per mole, so ten to the sixth needs about thirty five and ten to the seventeenth about one hundred, which is the range real enzymes work in. Footers note that the two-temperature form is the natural logarithm of the ratio of rate constants equals the activation energy over the gas constant times the quantity one over the first temperature minus one over the second, that temperature must be in kelvin, and that a catalyst changes neither the free energy change nor the equilibrium constant, only the rate at which equilibrium is reached.")

F = d.axes(70, 150, 540, 310, "reaction progress", "potential energy", xr=(0,10), yr=(0,115), ticks_x=[], ticks_y=[])
d.curve(F, [(i/40, UNCAT(i/40)) for i in range(0, 401)], NAVY, 3)
d.curve(F, [(i/40, CAT(i/40)) for i in range(0, 401)], RED, 2.5, dash=True)

def P(x, y): return F(x, y)
# level guides
for yv, lab in ((40, "reactants"), (20, "products"), (66, "intermediate")):
    x0, _ = P(0.15, yv); x1, _ = P(9.9, yv)
    _, yy = P(0, yv)
    d.line(x0, yy, x1, yy, "#d9d2c4", 1, True)
rx, ry = P(0.5, 40); d.text(rx+30, ry+22, "reactants", color=GREY, size=11, anchor="start")
px, py = P(8.4, 20); d.text(px, py-14, "products", color=GREY, size=11, anchor="middle")
ix, iy = P(4.6, 66); d.text(ix+86, iy-6, "intermediate", color=NAVY, size=11.5, weight=700)
t1x, t1y = P(2.6, 100); d.text(t1x, t1y-14, "TS₁ — tallest peak", color=NAVY, size=11.5, weight=700)
t2x, t2y = P(6.4, 86); d.text(t2x+40, t2y-14, "TS₂", color=NAVY, size=11.5, weight=700)
# Ea forward
ax, ay40 = P(1.55, 40); _, ay100 = P(1.55, 100)
d.arrow(ax, ay40, ax, ay100, SAGE, width=2)
d.text(ax-8, (ay40+ay100)/2, "Eₐ fwd = 60", color=SAGE, size=11.5, weight=700, anchor="end")
# Ea reverse
bx, by20 = P(8.9, 20); _, by100 = P(8.9, 100)
d.line(t1x, ay100, bx, by100, "#d9d2c4", 1, True)
d.arrow(bx, by20, bx, by100, GOLD, width=2)
d.text(bx+8, (by20+by100)/2, "Eₐ rev = 80", color=GOLD, size=11.5, weight=700, anchor="start")
# delta H
cx, cy40 = P(9.55, 40); _, cy20 = P(9.55, 20)
d.arrow(cx, cy40, cx, cy20, RED, width=2)
d.text(cx-6, (cy40+cy20)/2 + 4, "ΔH = −20", color=RED, size=11.5, weight=700, anchor="end")
d.text(340, 528, "step 1 is rate determining — it has the highest point on the diagram", color=GREY, size=11.5)
d.legend(214, 392, [(NAVY, "uncatalysed", False), (RED, "catalysed — same ends, lower peaks", True)])

d.box(648, 150, 504, 150, "Transition state vs. intermediate",
      "TRANSITION STATE — an energy *maximum*. Not a species: bonds half broken, half formed, lifetime ~10⁻¹³ s. Cannot be isolated.\nINTERMEDIATE — a local *minimum* between two transition states. A real species with a finite lifetime, sometimes detectable.",
      NAVY, chars=62, size=12, head_size=13)
d.box(648, 318, 504, 142, "The only link between barriers and ΔH",
      "ΔH = Eₐ(forward) − Eₐ(reverse)   — true for exothermic and endothermic alike. Know two, get the third. But ΔH fixes *neither* barrier on its own: a strongly exothermic reaction can still have an enormous Eₐ.",
      GOLD, chars=62, size=12, head_size=13)

G = d.axes(70, 582, 400, 196, "1 / T  (K⁻¹)", "ln k", xr=(0,10), yr=(0,10), ticks_x=[], ticks_y=[])
d.curve(G, [(1.0, 8.6), (9.0, 1.4)], BLUE, 3)
gx, gy = G(5.0, 5.0)
d.text(gx+70, gy-16, "slope = −Eₐ / R", color=BLUE, size=13, weight=700)
d.text(gx+70, gy+6, "intercept = ln A", color=GREY, size=11.5)
d.text(270, 848, "Eₐ = −slope × R   ·   slope −9,600 K → 9,600 × 8.314 = 79.8 kJ/mol", color=NAVY, size=12, weight=700)

d.rect(512, 560, 640, 236, NAVY, FILL[NAVY], 12, 2)
d.text(832, 588, "WHAT A LOWER BARRIER BUYS YOU", color=NAVY, weight=700, size=13)
d.text(832, 610, "at 37 °C every factor of ten in rate costs 5.9 kJ/mol  (RT·ln10)", color=GREY, size=11.5)
rows = [("−10 kJ/mol", "≈ 50×"), ("−20 kJ/mol", "≈ 2,300×"),
        ("−35 kJ/mol", "10⁶ — a modest enzyme"), ("−70 kJ/mol", "10¹²"),
        ("−100 kJ/mol", "10¹⁷ — the record holders")]
yy = 642
for lab, val in rows:
    d.text(560, yy, lab, color=NAVY, size=12, weight=700, anchor="start")
    d.text(1104, yy, val, color=GREY, size=12, anchor="end")
    yy += 25
d.text(832, 772, "Reductions of 10–20 kJ/mol do NOT give 10⁶-fold — check the arithmetic", color=RED, size=11.5, weight=700)

d.text(590, 874, "Two-temperature form: ln(k₂/k₁) = (Eₐ/R)(1/T₁ − 1/T₂)  ·  T in kelvin, always  ·  a catalyst lowers both barriers equally, so ΔG and K are untouched — only the rate changes",
       color=NAVY, size=12, weight=700)
print(d.save("activation-energy-barrier"))
