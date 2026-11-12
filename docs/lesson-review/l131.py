import sys; sys.path.insert(0,'/home/claude/dkit')
from dkit import *

d = D(1180, 920, "Q first, then the ICE table",
      "Q decides which way x points. Get that wrong and every number after it is wrong — so it is step two, before the table is drawn.",
      "A five-step workflow runs down the left: write the balanced equation and the equilibrium expression, excluding pure solids and liquids; compute the reaction quotient from the concentrations you were given; compare it with the equilibrium constant, which fixes the direction and therefore the sign of x; build the initial, change and equilibrium rows; and solve, then check by substituting back. A branch below sets out the three ways to solve: if both sides are perfect squares, take the square root of the whole expression, which is much faster than expanding; if the equilibrium constant is small enough that the initial concentration divided by it exceeds four hundred, drop x from the denominator and take x as the square root of the constant times the initial concentration; otherwise expand and use the quadratic formula. A worked table shows hydrogen plus iodine giving hydrogen iodide with a constant of 49: initial values of 1.00, 1.00 and zero, changes of minus x, minus x and plus 2x, equilibrium values of one minus x, one minus x and 2x, and the perfect-square shortcut giving 2x over one minus x equals seven, so x is 0.778 and the hydrogen iodide concentration is 1.56 molar. A second panel shows how the sign of x flips: when the quotient is below the constant the reaction runs forward, so reactants take minus x and products plus x; when the quotient is above the constant the reaction runs backwards, so reactants take plus x and products minus x. A footer gives the validity test for dropping x: the approximation holds when x is under five per cent of the initial concentration, which because x is the square root of the constant times the concentration means the concentration must exceed four hundred times the constant, not one hundred, since a ratio of one hundred gives a ten per cent error and fails the test.")

STEPS = [("1", "Write the equation and K", "exclude pure solids and liquids"),
         ("2", "Compute Q from what you were given", "same expression, current values"),
         ("3", "Compare Q with K", "this fixes the DIRECTION — and the sign of x"),
         ("4", "Build the I, C, E rows", "coefficients multiply x"),
         ("5", "Solve, then substitute back to check", "")]
d.rect(24, 150, 520, 258, NAVY, FILL[NAVY], 12, 2)
d.text(284, 178, "THE ORDER THAT KEEPS YOU OUT OF TROUBLE", color=NAVY, weight=700, size=13)
yy = 210
for n, head, sub in STEPS:
    d.text(50, yy, n, color=NAVY, size=14, weight=700, anchor="start")
    d.text(76, yy, head, color=NAVY, size=12.5, weight=700, anchor="start")
    if sub:
        d.text(76, yy + 17, sub, color=GREY, size=10.5, anchor="start")
    yy += 40
d.text(284, 392, "Step 2 is the one people skip — and it is the one that sets the sign", color=NAVY, size=11, weight=700)

d.rect(24, 428, 520, 236, BLUE, FILL[BLUE], 12, 2)
d.text(284, 456, "THREE WAYS TO SOLVE — PICK BEFORE YOU EXPAND", color=BLUE, weight=700, size=12.5)
WAYS = [("both sides a perfect square", "take √ of the WHOLE expression", "2x/(c−x) = √K"),
        ("K small:  C / K > 400", "drop x from the denominator", "x ≈ √(K·C)"),
        ("anything else", "expand and use the quadratic", "x = (−b ± √(b²−4ac)) / 2a")]
yy = 490
for cond, what, form in WAYS:
    d.text(48, yy, cond, color=BLUE, size=11.5, weight=700, anchor="start")
    d.text(48, yy + 17, what, color=GREY, size=10.5, anchor="start")
    d.text(520, yy + 8, form, color=NAVY, size=11.5, weight=700, anchor="end")
    yy += 50
d.text(284, 644, "Spotting the perfect square saves more time than any other move in equilibrium", color=BLUE, size=11, weight=700)

d.rect(564, 150, 588, 300, SAGE, FILL[SAGE], 12, 2)
d.text(858, 178, "WORKED — H₂ + I₂ ⇌ 2HI,  Kᴄ = 49", color=SAGE, weight=700, size=12.5)
COLS = [(760, "H₂"), (900, "I₂"), (1040, "HI")]
for x, h in COLS:
    d.text(x, 208, h, color=NAVY, size=12.5, weight=700)
ROWS = [("I", ["1.00", "1.00", "0"]), ("C", ["−x", "−x", "+2x"]),
        ("E", ["1.00 − x", "1.00 − x", "2x"])]
yy = 234
for lab, vals in ROWS:
    d.text(604, yy, lab, color=SAGE, size=12, weight=700, anchor="start")
    for (x, _), v in zip(COLS, vals):
        d.text(x, yy, v, color=NAVY, size=12)
    yy += 26
d.line(596, 318, 1120, 318, "#d9d2c4", 1, True)
for i, t in enumerate(["Kᴄ = (2x)² / (1.00 − x)²  —  a perfect square on both sides",
                       "√ both sides:   2x / (1.00 − x) = 7",
                       "2x = 7 − 7x   →   9x = 7   →   x = 0.778",
                       "[H₂] = [I₂] = 0.222 M      [HI] = 2x = 1.56 M"]):
    d.text(858, 340 + i*23, t, color=NAVY if i else GREY, size=11.5, weight=700 if i == 3 else 400)
d.text(858, 436, "check: (1.56)² / (0.222)² = 49.1 ✓", color=SAGE, size=11, weight=700)

d.rect(564, 470, 588, 194, RED, FILL[RED], 12, 2)
d.text(858, 498, "THE SIGN OF x FLIPS WITH Q", color=RED, weight=700, size=12.5)
d.text(712, 526, "Q < K  — runs FORWARD", color=SAGE, size=11.5, weight=700)
d.text(1004, 526, "Q > K  — runs BACKWARD", color=RED, size=11.5, weight=700)
PAIRS = [("reactants", "−x", "+x"), ("products", "+x", "−x")]
yy = 554
for name, left, right in PAIRS:
    d.text(596, yy, name, color=GREY, size=11, anchor="start")
    d.text(712, yy, left, color=SAGE, size=13, weight=700)
    d.text(1004, yy, right, color=RED, size=13, weight=700)
    yy += 26
d.text(858, 624, "Set the signs from Q, not from habit — products are not always “plus”",
       color=RED, size=11, weight=700)

d.box(24, 688, 1128, 110, "When may you drop x? The test that is usually quoted wrong",
      "The approximation holds when x is under 5% of the initial concentration. Since x ≈ √(K·C), that means √(K/C) < 0.05, so C must exceed 400×K — not 100×K. A ratio of 100 gives √(1/100) = 10%, which fails the 5% test outright. Worked: acetic acid, Kₐ = 1.8×10⁻⁵, needs C > 7.2×10⁻³ M. At 0.10 M the shortcut is fine (1.3% dissociated); at 0.0010 M it is not (13%), and the quadratic is required.",
      NAVY, chars=148, size=12, head_size=13.5)

d.box(24, 814, 1128, 86, "Two more things that change the table",
      "PRODUCTS PRESENT AT THE START do not change the method — they change the initial row, and Q tells you which way x then runs. · A PURE SOLID OR LIQUID has no row at all: its amount never enters Q, which is why adding more CaCO₃ to CaCO₃(s) ⇌ CaO(s) + CO₂(g) shifts nothing.",
      NAVY, chars=148, size=12, head_size=13.5)
print(d.save("ice-table-workflow"))
