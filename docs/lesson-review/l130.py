import sys; sys.path.insert(0,'/home/claude/dkit')
from dkit import *

d = D(1180, 916, "What moves, and what does not",
      "Every equilibrium question is one of three things: which way does it run, what happens to K, or what does the algebra do to K. Only one stress on this page changes K at all.",
      "A number line places the reaction quotient against the equilibrium constant. Where the quotient is below the constant there is too little product, so the reaction runs forward; where they are equal the system is at equilibrium and nothing changes on balance; where the quotient is above the constant there is too much product, so the reaction runs in reverse. A worked clinical case follows: hyperventilation blows off carbon dioxide, which is a reactant in the carbonic acid equilibrium, so removing it shrinks the denominator and the quotient rises above the constant, and the reaction runs left, consuming hydrogen ions and raising blood pH, which is respiratory alkalosis. A table of stresses records, for each, which way the system shifts and whether the equilibrium constant itself changes. Adding a reactant or removing a product shifts the system right and leaves the constant unchanged. Compressing a gas mixture shifts it toward whichever side has fewer moles of gas and leaves the constant unchanged. Adding an inert gas at constant volume does nothing at all, because no partial pressure changes. Adding a catalyst does nothing to the position either; it only shortens the time taken to arrive. Changing the temperature is the only stress that changes the constant: for an exothermic reaction, heating lowers it, and for an endothermic reaction, heating raises it. A panel gives the algebra of manipulating equilibrium constants: reversing a reaction inverts the constant, multiplying all coefficients by a number raises the constant to that power, and adding two reactions multiplies their constants, which is the equilibrium counterpart of Hess's law. These are worked on a chain where A to B has a constant of 4.0 and B to C has 0.50, so A to C has 2.0, and where reversing and doubling A to B gives 0.0625. A final panel covers converting between the concentration and pressure forms of the constant: the pressure form equals the concentration form times the gas constant times temperature raised to the change in gaseous moles, worked for three reactions with changes of minus two, minus one and zero, and notes that the two constants describe the same equilibrium in different units, so the numerical difference between them is the conversion factor alone and says nothing about which side is favoured.")

d.rect(24, 150, 700, 200, NAVY, FILL[NAVY], 12, 2)
d.text(374, 178, "WHICH WAY DOES IT RUN? COMPARE Q WITH K", color=NAVY, weight=700, size=13)
ax0, ax1, axy = 70, 678, 250
d.line(ax0, axy, ax1, axy, NAVY, 2.5)
mid = (ax0 + ax1) / 2
d.line(mid, axy - 16, mid, axy + 16, NAVY, 2.5)
d.text(mid, axy + 34, "Q = K", color=NAVY, size=13, weight=700)
d.text(mid, axy + 52, "at equilibrium · no net change", color=GREY, size=10.5)
d.arrow(mid - 230, axy - 40, mid - 90, axy - 40, SAGE, width=2.5)
d.text(mid - 160, axy - 52, "runs FORWARD", color=SAGE, size=12, weight=700)
d.text(mid - 160, axy + 34, "Q < K", color=SAGE, size=13, weight=700)
d.text(mid - 160, axy + 52, "too little product yet", color=GREY, size=10.5)
d.arrow(mid + 230, axy - 40, mid + 90, axy - 40, RED, width=2.5)
d.text(mid + 160, axy - 52, "runs in REVERSE", color=RED, size=12, weight=700)
d.text(mid + 160, axy + 34, "Q > K", color=RED, size=13, weight=700)
d.text(mid + 160, axy + 52, "too much product", color=GREY, size=10.5)
d.text(374, 326, "Q has the same form as K — it just uses the concentrations you have right now",
       color=NAVY, size=11.5, weight=700)

d.rect(744, 150, 408, 200, RED, FILL[RED], 12, 2)
d.text(948, 178, "WORKED — HYPERVENTILATION", color=RED, weight=700, size=12.5)
for i, t in enumerate([
        "CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻",
        "",
        "blow off CO₂ → a REACTANT is removed",
        "the denominator shrinks → Q RISES",
        "Q > K → the reaction runs LEFT",
        "H⁺ is consumed → pH rises",
        "",
        "respiratory alkalosis"]):
    if not t:
        continue
    c = NAVY if i < 6 else RED
    d.text(948, 210 + i*19, t, color=c, size=11.5,
           weight=700 if i in (0, 7) else 400)

d.rect(24, 374, 700, 230, BLUE, FILL[BLUE], 12, 2)
d.text(374, 402, "STRESS → WHICH WAY IT SHIFTS, AND WHETHER K CHANGES", color=BLUE, weight=700, size=12.5)
d.text(700, 426, "does K change?", color=GREY, size=9.5, anchor="end")
STRESS = [("add a reactant / remove a product", "shifts right", "no"),
          ("compress the gas (raise P)", "toward fewer moles of gas", "no"),
          ("add inert gas at constant V", "no shift at all", "no"),
          ("add a catalyst", "no shift — just gets there sooner", "no"),
          ("RAISE T, exothermic", "shifts left", "YES — K falls"),
          ("RAISE T, endothermic", "shifts right", "YES — K rises")]
yy = 452
for a, b, k in STRESS:
    hot = k.startswith("YES")
    d.text(48, yy, a, color=RED if hot else NAVY, size=11.5, weight=700 if hot else 400, anchor="start")
    d.text(600, yy, b, color=GREY, size=11, anchor="end")
    d.text(700, yy, k, color=RED if hot else GREY, size=11, weight=700 if hot else 400, anchor="end")
    yy += 24
d.text(374, 590, "Temperature is the ONLY stress that changes K — everything else just moves the mixture along a fixed K",
       color=BLUE, size=11.5, weight=700)

d.rect(744, 374, 408, 230, SAGE, FILL[SAGE], 12, 2)
d.text(948, 402, "THE ALGEBRA OF K", color=SAGE, weight=700, size=12.5)
ALG = [("reverse the reaction", "K → 1/K"),
       ("multiply coefficients by n", "K → Kⁿ"),
       ("add two reactions", "K → K₁ × K₂")]
yy = 434
for a, b in ALG:
    d.text(768, yy, a, color=NAVY, size=11.5, anchor="start")
    d.text(1128, yy, b, color=SAGE, size=12, weight=700, anchor="end")
    yy += 26
d.line(768, 516, 1128, 516, "#d9d2c4", 1, True)
for i, t in enumerate(["A ⇌ B  K = 4.0     B ⇌ C  K = 0.50",
                       "A ⇌ C   →   4.0 × 0.50 = 2.0",
                       "2B ⇌ 2A  →  (1/4.0)² = 0.0625"]):
    d.text(948, 538 + i*21, t, color=NAVY, size=11.5, weight=700 if i else 400)

d.rect(24, 628, 1128, 160, GOLD, FILL[GOLD], 12, 2)
d.text(588, 656, "Kₚ = Kᴄ (RT)^Δn     Δn = moles of GASEOUS products − moles of GASEOUS reactants", color=GOLD, weight=700, size=13)
CASES = [("N₂ + 3H₂ ⇌ 2NH₃", "Δn = 2 − 4 = −2", "Kₚ = Kᴄ / (RT)²", "Kₚ < Kᴄ"),
         ("2SO₂ + O₂ ⇌ 2SO₃", "Δn = 2 − 3 = −1", "Kₚ = Kᴄ / RT", "Kₚ < Kᴄ"),
         ("H₂ + I₂ ⇌ 2HI", "Δn = 2 − 2 = 0", "Kₚ = Kᴄ", "identical")]
yy = 690
for eq, dn, form, note in CASES:
    d.text(60, yy, eq, color=NAVY, size=11.5, anchor="start")
    d.text(520, yy, dn, color=GOLD, size=11.5, weight=700, anchor="end")
    d.text(800, yy, form, color=NAVY, size=11.5, weight=700, anchor="end")
    d.text(1140, yy, note, color=GREY, size=11, anchor="end")
    yy += 26
d.text(588, 772, "Solids and liquids are not counted in Δn — and Kₚ ≠ Kᴄ is a change of UNITS, not of which side is favoured",
       color=GOLD, size=11.5, weight=700)

d.box(24, 806, 1128, 88, "The one that is not about equilibrium at all",
      "A large K says the products win at equilibrium; it says nothing about how long that takes. Diamond is thermodynamically unstable with respect to graphite and sits on your finger for a lifetime. Kinetics and thermodynamics answer different questions.",
      NAVY, chars=150, size=12, head_size=13.5)
print(d.save("equilibrium-what-moves"))
