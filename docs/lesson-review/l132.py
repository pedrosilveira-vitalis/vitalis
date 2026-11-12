import sys; sys.path.insert(0,'/home/claude/dkit')
from dkit import *

d = D(1180, 920, "Le Chatelier, and the price of using it",
      "The principle tells you which way a system moves, never how far or how fast. The Haber process is the standard case where all three questions have different answers.",
      "A plot of the equilibrium percentage of ammonia against temperature for three pressures, from published Haber-process data. At 100 atmospheres the yield falls from 81.7 per cent at 200 degrees to 52.5 at 300, 25.2 at 400 and 10.6 at 500. At 200 atmospheres it runs 89.0, 66.7, 38.8 and 18.3 over the same temperatures. At 400 atmospheres it runs 94.6, 79.7, 55.4 and 31.9. Every curve falls with temperature, because the reaction is exothermic and heating lowers the equilibrium constant, and every curve rises with pressure, because four moles of gas become two. The industrial operating window is marked at 400 to 450 degrees and about 200 atmospheres, which gives only about fifteen to twenty per cent: the much larger yield available at 300 degrees is rejected because the reaction takes far too long to get there, and the iron catalyst fixes the rate without touching the yield. A panel sets out the inert gas trap. Argon added at constant volume changes the total pressure but no partial pressure, so nothing shifts. Argon added at constant total pressure forces the volume to expand, which lowers every partial pressure and is equivalent to decompression, so the system shifts toward the side with more moles of gas. A panel gives three biological cases. In the carbonic acid system, exercise raises carbon dioxide, which pushes the equilibrium right and lowers pH, and faster breathing removes carbon dioxide, pushes it left and raises pH. In the Bohr effect, acid, carbon dioxide and heat in working tissue push the haemoglobin binding equilibrium left so oxygen is released where it is needed, which is the same event as the familiar right shift of the dissociation curve. In the common ion effect, added chloride pushes the silver chloride dissolution equilibrium left and precipitates more solid, while ammonia, which complexes silver, pulls it right and dissolves more. A footer states the two limits of the principle: it gives direction only, so any quantity needs an ICE table, and a catalyst changes neither the position nor the constant, only the time taken to arrive.")

F = d.axes(64, 160, 560, 320, "temperature (°C)", "% NH₃ at equilibrium",
           xr=(180, 720), yr=(0, 100), ticks_x=[200, 300, 400, 500, 600, 700],
           ticks_y=[0, 25, 50, 75, 100])
SERIES = [("400 atm", RED, [(200, 94.6), (300, 79.7), (400, 55.4), (500, 31.9)]),
          ("200 atm", NAVY, [(200, 89.0), (300, 66.7), (400, 38.8), (500, 18.3)]),
          ("100 atm", BLUE, [(200, 81.7), (300, 52.5), (400, 25.2), (500, 10.6), (700, 2.2)])]
for name, c, pts in SERIES:
    d.curve(F, pts, c, 3)
    anchor_pt = pts[3] if len(pts) > 4 else pts[-1]
    lx, ly = F(anchor_pt[0], anchor_pt[1])
    d.text(lx + 10, ly + (26 if len(pts) > 4 else 4), name, color=c, size=11.5, weight=700, anchor="start")
wx0, wy0 = F(400, 0); wx1, wy1 = F(450, 100)
d.rect(wx0, wy1, wx1 - wx0, wy0 - wy1, GOLD, FILL[GOLD], 0, 0)
d.text((wx0 + wx1) / 2, wy1 + 16, "industrial window", color=GOLD, size=11, weight=700)
for name, c, pts in SERIES:
    d.curve(F, pts, c, 3)
d.text(344, 552, "400–450 °C and ~200 atm gives only ≈15–20% NH₃",
       color=GOLD, size=11.5, weight=700)
d.text(344, 572, "the 67% available at 300 °C is refused because it arrives far too slowly",
       color=GOLD, size=11.5, weight=700)
d.text(344, 590, "Published equilibrium yields for a stoichiometric N₂/H₂ mixture", color=GREY, size=10)

d.rect(652, 160, 500, 196, BLUE, FILL[BLUE], 12, 2)
d.text(902, 188, "THE INERT GAS TRAP", color=BLUE, weight=700, size=13)
for i, (head, body, verdict, c) in enumerate([
    ("argon at CONSTANT VOLUME", "total pressure rises, but no partial pressure\nchanges — Q is untouched", "NO SHIFT", SAGE),
    ("argon at CONSTANT PRESSURE", "the volume must expand, so every partial\npressure falls — same as decompressing", "SHIFTS toward more moles of gas", RED)]):
    y = 214 + i*86
    d.text(676, y, head, color=NAVY, size=11.5, weight=700, anchor="start")
    for j, line in enumerate(body.split("\n")):
        d.text(676, y + 18 + j*15, line, color=GREY, size=10.5, anchor="start")
    d.text(1128, y, verdict, color=c, size=11.5, weight=700, anchor="end")

d.rect(652, 372, 500, 212, SAGE, FILL[SAGE], 12, 2)
d.text(902, 400, "THREE PLACES THE MCAT HIDES IT", color=SAGE, weight=700, size=12.5)
BIO = [("carbonic acid", "CO₂ + H₂O ⇌ H⁺ + HCO₃⁻",
        "exercise → ↑CO₂ → right → pH falls",
        "breathe faster → ↓CO₂ → left → pH rises"),
       ("Bohr effect", "Hb + O₂ ⇌ HbO₂",
        "acid, CO₂, heat in tissue → LEFT → O₂ released",
        "the same event as a RIGHT shift of the curve"),
       ("common ion", "AgCl(s) ⇌ Ag⁺ + Cl⁻",
        "add Cl⁻ → left → more solid precipitates",
        "add NH₃ (binds Ag⁺) → right → more dissolves")]
yy = 426
for name, eq, a, b in BIO:
    d.text(676, yy, name, color=SAGE, size=11.5, weight=700, anchor="start")
    d.text(1128, yy, eq, color=NAVY, size=11, anchor="end")
    d.text(676, yy + 16, a, color=GREY, size=10.5, anchor="start")
    d.text(676, yy + 31, b, color=GREY, size=10.5, anchor="start")
    yy += 54

d.box(24, 600, 1128, 92, "Why heating an exothermic reaction lowers K — the bit that is not just a rule",
      "Treat heat as a product. Raising T is adding product, so Q rises above K and the system runs backward. Thermodynamically: K is fixed by ΔG° = −RT ln K, and changing T changes ΔG° through ΔG° = ΔH° − TΔS° — which is why temperature is the ONE stress that moves K rather than merely moving the mixture along it.",
      NAVY, chars=150, size=12, head_size=13.5)

d.box(24, 708, 1128, 92, "The two things Le Chatelier will not tell you",
      "DIRECTION ONLY, NEVER MAGNITUDE. \"Shifts right\" does not say how far; any number needs an ICE table and the actual K. · A CATALYST IS NOT A STRESS. It lowers the barrier both ways by the same amount, so the position and K are untouched and only the time taken changes — which is exactly why the Haber plant needs one at a temperature chosen for speed.",
      NAVY, chars=150, size=12, head_size=13.5)
print(d.save("le-chatelier-haber"))
