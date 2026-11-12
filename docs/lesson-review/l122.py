import sys, math; sys.path.insert(0,'/home/claude/dkit')
from dkit import *
A0 = 1.0
kz, kf, ks = 0.10, 0.25, 0.60
def z(t): return max(A0 - kz*t, 0)
def f(t): return A0*math.exp(-kf*t)
def s(t): return 1.0/(1.0/A0 + ks*t)
d = D(1160, 800, "Three orders, three signatures",
      "Same starting concentration, three different shapes. Identify the order and every other fact follows from it.",
      "A concentration against time plot shows the three orders decaying from the same starting concentration. Zero order falls as a straight line and hits zero at a definite time. First order decays exponentially, halving in equal steps and never quite reaching zero. Second order falls steeply at first and then develops a long slow tail. Below, three panels, one per order. Zero order: the rate equals the rate constant, concentration equals initial concentration minus the rate constant times time, a plot of concentration against time is the straight line, the half-life equals the initial concentration over twice the rate constant and therefore shortens as the reaction proceeds, and the rate constant carries units of molar per second; this is the behaviour of a saturated catalyst or an enzyme running at maximum velocity, and of ethanol elimination at ordinary doses. First order: the rate equals the rate constant times concentration, concentration equals the initial value times e to the minus rate constant times time, a plot of the natural logarithm of concentration against time is the straight line with slope minus the rate constant, the half-life equals 0.693 over the rate constant and is constant no matter the concentration, and the rate constant carries units of reciprocal seconds; this is radioactive decay and most drug elimination. Second order: the rate equals the rate constant times concentration squared, the reciprocal of concentration equals the reciprocal of the initial concentration plus the rate constant times time, a plot of the reciprocal of concentration against time is the straight line with slope equal to the rate constant, the half-life equals one over the rate constant times the initial concentration and therefore lengthens as the reaction proceeds, and the rate constant carries units of reciprocal molar per second. Two footers follow. The first is on reading the rate law: the exponents are experimental and are not the balanced equation's coefficients, except in a single elementary step; given a table, compare two runs in which only one concentration changed and solve the ratio of rates equals the ratio of concentrations raised to the order; given a mechanism, the rate law comes from the slow step, and any intermediate appearing in it must be substituted out using a preceding fast equilibrium. The second is on what changes the rate constant: temperature and activation energy, through the Arrhenius equation, rate constant equals the frequency factor times e to the minus activation energy over the gas constant times temperature, so a plot of the logarithm of the rate constant against the reciprocal of temperature is a straight line of slope minus activation energy over the gas constant; a catalyst lowers the activation energy for the forward and the reverse directions equally, which speeds the approach to equilibrium while changing neither the free energy change nor the equilibrium constant.")
F = d.axes(70, 130, 460, 290, "time", "[A]", xr=(0, 10), yr=(0, 1), ticks_x=[0,2,4,6,8,10], ticks_y=[0,0.25,0.5,0.75,1])
d.curve(F, [(i/20, z(i/20)) for i in range(0, 201)], SAGE, 3)
d.curve(F, [(i/20, f(i/20)) for i in range(0, 201)], BLUE, 3)
d.curve(F, [(i/20, s(i/20)) for i in range(0, 201)], RED, 3)
d.legend(300, 170, [(SAGE, "zero order — straight line", False),
                    (BLUE, "first order — exponential", False),
                    (RED, "second order — long tail", False)])
d.box(560, 130, 576, 134, "The one that matters clinically",
      "First order means a constant *fraction* leaves per unit time, so the half-life never changes — 50%, 25%, 12.5%. Zero order means a constant *amount* leaves per unit time, so a saturated system (ethanol at ordinary doses, an enzyme at Vₘₐₓ) clears at a flat rate and the half-life shortens as it goes.",
      NAVY, chars=70, size=12, head_size=13)
d.box(560, 280, 576, 140, "Reading the rate law",
      "The exponents are experimental — NOT the balanced equation's coefficients. The one exception is a single elementary step.  From a table: pick two runs where only one concentration moved, then solve  Rate₂/Rate₁ = ([A]₂/[A]₁)^m.  From a mechanism: the rate law comes from the slow step, and any intermediate in it must be substituted out via the fast equilibrium before it.",
      NAVY, chars=70, size=12, head_size=13)
cols = [("ZERO ORDER", SAGE, "Rate = k", "[A] = [A]₀ − kt", "[A] vs t", "t½ = [A]₀ / 2k", "shortens as it goes", "M·s⁻¹", "saturated catalyst · enzyme at Vₘₐₓ"),
        ("FIRST ORDER", BLUE, "Rate = k[A]", "ln[A] = ln[A]₀ − kt", "ln[A] vs t", "t½ = 0.693 / k", "constant — always", "s⁻¹", "radioactive decay · most drug elimination"),
        ("SECOND ORDER", RED, "Rate = k[A]²", "1/[A] = 1/[A]₀ + kt", "1/[A] vs t", "t½ = 1 / k[A]₀", "lengthens as it goes", "M⁻¹·s⁻¹", "bimolecular self-reaction")]
for i,(name, c, rate, integ, plot, half, halfnote, units, eg) in enumerate(cols):
    x = 24 + i*376
    d.rect(x, 452, 360, 216, c, FILL.get(c), 11, 2)
    d.text(x+180, 480, name, color=c, weight=700, size=13.5)
    rows = [("rate law", rate), ("integrated", integ), ("linear plot", plot), ("half-life", half), ("", halfnote), ("units of k", units)]
    yy = 508
    for lab, val in rows:
        if lab:
            d.text(x+24, yy, lab, color=GREY, size=10.5, anchor="start")
            d.text(x+336, yy, val, color=NAVY, weight=700, size=12, anchor="end")
            yy += 22
        else:
            d.text(x+336, yy, val, color=c, weight=700, size=11, anchor="end")
            yy += 20
    d.line(x+24, 646, x+336, 646, "#d9d2c4", 1, True)
    d.lines(x+180, 662, eg, chars=44, lh=13, color=GREY, size=11)
d.box(24, 688, 1112, 96, "What changes k — and what doesn't",
      "Temperature and activation energy, through Arrhenius:  k = Ae^(−Eₐ/RT), so ln k against 1/T is a straight line of slope −Eₐ/R.  A catalyst lowers Eₐ for the forward and reverse directions *equally* — it speeds the approach to equilibrium and changes neither ΔG nor K. Concentration never changes k; it changes the rate.",
      NAVY, chars=132, size=12, head_size=13.5)
print(d.save("reaction-orders"))
