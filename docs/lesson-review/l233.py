import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 948,
      "Who else is in the room, and what are they doing there?",
      "Two questions sort almost every group effect on the exam",
      "Top: the crossover that defines social facilitation. An audience raises arousal, and arousal strengthens "
      "whatever response is already dominant — so performance improves when the dominant response is the "
      "correct one and gets worse when it is not. Note that “simple” and “complex” are relative to the "
      "performer, not to the task: the same laparoscopic procedure is simple for the attending and complex for "
      "the intern, and the audience helps one and hurts the other. Bottom left: the sorting question that "
      "separates facilitation from loafing — whose task is it, and can anyone see your share. Bottom right: "
      "groupthink against polarization, which get confused because both end in unanimity, though for opposite "
      "reasons."
      )

# ---------------- Panel A: the crossover ----------------
d.rect(40, 180, 840, 318, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Arousal strengthens the dominant response", color=NAVY, weight="bold", size=15)

d.rect(360, 228, 200, 42, GREY, FILL[GREY], rx=8, width=1.6)
d.text(460, 246, "AN AUDIENCE", color=NAVY, weight="bold", size=11.5)
d.text(460, 262, "→ physiological arousal", color=GREY, size=9.5)

d.arrow(400, 276, 270, 302, SAGE)
d.arrow(520, 276, 650, 302, RED)

d.rect(80, 310, 340, 168, SAGE, FILL[SAGE], rx=10, width=2)
d.text(250, 334, "TASK IS WELL-PRACTISED", color=SAGE, weight="bold", size=12)
d.text(250, 352, "…for this performer", color=GREY, size=9.5)
d.line(120, 364, 380, 364, SAGE, 1, dash="3,3")
d.text(250, 388, "dominant response = CORRECT", color=NAVY, weight="bold", size=11)
d.text(250, 416, "PERFORMANCE IMPROVES", color=SAGE, weight="bold", size=13)
d.text(250, 442, "the concert pianist, the attending surgeon", color=GREY, size=9.5)
d.text(250, 462, "the cyclist racing rather than riding alone", color=GREY, size=9.5)

d.rect(500, 310, 340, 168, RED, FILL[RED], rx=10, width=2)
d.text(670, 334, "TASK IS NOT YET LEARNED", color=RED, weight="bold", size=12)
d.text(670, 352, "…for this performer", color=GREY, size=9.5)
d.line(540, 364, 800, 364, RED, 1, dash="3,3")
d.text(670, 388, "dominant response = ERROR", color=NAVY, weight="bold", size=11)
d.text(670, 416, "PERFORMANCE WORSENS", color=RED, weight="bold", size=13)
d.text(670, 442, "the student recital, the intern's first case", color=GREY, size=9.5)
d.text(670, 462, "same audience, opposite effect", color=GREY, size=9.5)

# ---------------- Panel B: facilitation vs loafing ----------------
d.rect(40, 514, 410, 414, GOLD, "none", rx=12, width=2)
d.text(245, 542, "Facilitation or loafing?", color=GOLD, weight="bold", size=14)

d.rect(64, 562, 362, 44, GREY, FILL[GREY], rx=8, width=1.6)
d.text(245, 582, "WHOSE TASK IS IT, AND WHO CAN SEE", color=NAVY, weight="bold", size=10.5)
d.text(245, 598, "your individual share of the result?", color=GREY, size=9.5)

d.rect(64, 618, 362, 128, SAGE, FILL[SAGE], rx=9, width=2)
d.text(245, 642, "MY OWN TASK, VISIBLE", color=SAGE, weight="bold", size=12)
d.text(245, 662, "→ SOCIAL FACILITATION", color=SAGE, weight="bold", size=12)
for j, ln in enumerate(["others are watching or working alongside",
                        "effort goes UP; accuracy depends on skill",
                        "studying in a library, racing, performing"]):
    d.text(245, 688 + j * 18, ln, color=GREY, size=9.5)

d.rect(64, 758, 362, 160, RED, FILL[RED], rx=9, width=2)
d.text(245, 782, "SHARED TASK, SHARE HIDDEN", color=RED, weight="bold", size=12)
d.text(245, 802, "→ SOCIAL LOAFING", color=RED, weight="bold", size=12)
for j, ln in enumerate(["Ringelmann: 1 person pulls at 100%,",
                        "three at about 85%, eight at about 49%",
                        "diffused responsibility, no identifiability,",
                        "free riders — and the sucker effect in reply",
                        "cured by making each share visible"]):
    d.text(245, 828 + j * 18, ln, color=NAVY if j == 4 else GREY,
           weight="bold" if j == 4 else "normal", size=9.5)

# ---------------- Panel C: groupthink vs polarization ----------------
d.rect(470, 514, 410, 414, BLUE, "none", rx=12, width=2)
d.text(675, 542, "Both end unanimous — for opposite reasons", color=BLUE, weight="bold", size=12.5)

d.rect(494, 562, 362, 172, RED, FILL[RED], rx=9, width=2)
d.text(675, 586, "GROUPTHINK", color=RED, weight="bold", size=13)
d.text(675, 606, "debate is SUPPRESSED", color=NAVY, weight="bold", size=11)
d.line(540, 618, 810, 618, RED, 1, dash="3,3")
for j, ln in enumerate(["needs a cohesive, insulated group under stress",
                        "self-censorship, illusion of unanimity,",
                        "mindguards, pressure on dissenters",
                        "the decision gets WORSE",
                        "fix: devil's advocate, outside experts,",
                        "leader speaks last, second-chance meeting"]):
    d.text(675, 640 + j * 15, ln, color=NAVY if j == 3 else GREY,
           weight="bold" if j == 3 else "normal", size=9)

d.rect(494, 746, 362, 172, SAGE, FILL[SAGE], rx=9, width=2)
d.text(675, 770, "GROUP POLARIZATION", color=SAGE, weight="bold", size=13)
d.text(675, 790, "debate is what DOES it", color=NAVY, weight="bold", size=11)
d.line(540, 802, 810, 802, SAGE, 1, dash="3,3")
for j, ln in enumerate(["no cohesion required",
                        "arguments heard all point one way",
                        "— and people position themselves against the group",
                        "the group ends MORE EXTREME in the",
                        "direction it already leaned, risky OR cautious",
                        "jury rooms, echo chambers, radicalisation"]):
    d.text(675, 824 + j * 15, ln, color=NAVY if j == 3 else GREY,
           weight="bold" if j == 3 else "normal", size=9)

d.save("social-facilitation-crossover-loafing-and-group-decisions")
print("ok")
