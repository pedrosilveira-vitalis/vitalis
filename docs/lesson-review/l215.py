import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 912,
      "The signals that say eat, and the ones that say stop",
      "One nucleus reads them all; everything else is a messenger",
      "Top: the arcuate nucleus as the switchboard. Two opposing cell populations sit there — one "
      "releasing NPY and AgRP that drives eating, one releasing POMC products and CART that stops it — and "
      "every hormone in the picture works by pushing one of those two. Ghrelin from the stomach is the only "
      "peripheral hormone that says eat; everything else in the list says stop. Leptin from fat is the "
      "long-term signal, and the reason obesity is not a leptin deficiency: the level is high and the brain "
      "has stopped listening. Bottom left: the two models of body weight and what each one has to explain. "
      "Bottom right: hormones acting on sexual behaviour at two different times of life — permanently "
      "before birth, reversibly in adulthood."
      )

# ---------------- Panel A: arcuate switchboard ----------------
d.rect(40, 180, 840, 300, GOLD, "none", rx=12, width=2)
d.text(460, 208, "Everything routes through the arcuate nucleus", color=GOLD, weight="bold", size=16)

d.rect(330, 300, 260, 110, GOLD, FILL[GOLD], rx=12, width=2.4)
d.text(460, 326, "ARCUATE NUCLEUS", color=GOLD, weight="bold", size=14)
d.rect(346, 338, 110, 58, RED, FILL[RED], rx=8, width=2)
d.text(401, 360, "NPY / AgRP", color=RED, weight="bold", size=11)
d.text(401, 378, "EAT", color=RED, weight="bold", size=14)
d.rect(464, 338, 110, 58, SAGE, FILL[SAGE], rx=8, width=2)
d.text(519, 360, "POMC / CART", color=SAGE, weight="bold", size=11)
d.text(519, 378, "STOP", color=SAGE, weight="bold", size=14)

# orexigenic side
d.rect(70, 300, 210, 72, RED, FILL[RED], rx=10, width=2)
d.text(175, 324, "GHRELIN", color=RED, weight="bold", size=14)
d.text(175, 344, "from the STOMACH", color=NAVY, size=11)
d.text(175, 362, "peaks before meals", color=GREY, size=11)
d.arrow(284, 336, 326, 342, RED, width=2.4)
d.text(175, 394, "the only peripheral", color=RED, weight="bold", size=11)
d.text(175, 410, "hormone that says EAT", color=RED, weight="bold", size=11)

# anorexigenic side
sigs = [("LEPTIN", "fat mass · long-term"), ("INSULIN", "pancreas · after glucose"),
        ("CCK", "small intestine · fat and protein"), ("PYY · GLP-1", "ileum and colon · after a meal")]
y = 236
for name, note in sigs:
    d.rect(640, y, 210, 46, SAGE, FILL[SAGE], rx=8, width=2)
    d.text(745, y + 20, name, color=SAGE, weight="bold", size=12)
    d.text(745, y + 36, note, color=GREY, size=10)
    y += 52
d.arrow(636, 342, 596, 348, SAGE, width=2.4)
d.text(745, 456, "all four say STOP", color=SAGE, weight="bold", size=12)

d.text(230, 452, "obesity is not low leptin — leptin is HIGH and ignored",
       color=NAVY, weight="bold", size=12)

# ---------------- Panel B: set point vs settling point ----------------
d.rect(40, 500, 420, 384, BLUE, "none", rx=12, width=2)
d.text(250, 528, "Two models of body weight", color=BLUE, weight="bold", size=15)

d.rect(66, 548, 368, 150, BLUE, FILL[BLUE], rx=10, width=2)
d.text(250, 572, "SET POINT", color=BLUE, weight="bold", size=13)
d.text(250, 594, "the body defends a target", color=NAVY, weight="bold", size=12)
for i, t in enumerate(["twins raised apart share BMI",
                       "metabolism falls more than mass does",
                       "ghrelin stays high after dieting",
                       "leptin falls, removing the brake"]):
    d.text(250, 618 + i * 19, t, color=GREY, size=11)

d.rect(66, 712, 368, 150, SAGE, FILL[SAGE], rx=10, width=2)
d.text(250, 736, "SETTLING POINT", color=SAGE, weight="bold", size=13)
d.text(250, 758, "genes AND environment find a level", color=NAVY, weight="bold", size=12)
for i, t in enumerate(["populations gained weight in 50 years",
                       "genes cannot move that fast",
                       "cheap, dense, palatable food shifts it",
                       "so the level itself can drift upward"]):
    d.text(250, 782 + i * 19, t, color=GREY, size=11)

# ---------------- Panel C: organizational vs activational ----------------
d.rect(480, 500, 400, 384, RED, "none", rx=12, width=2)
d.text(680, 528, "Hormones act at two different times", color=RED, weight="bold", size=15)

d.rect(506, 548, 348, 150, GOLD, FILL[GOLD], rx=10, width=2)
d.text(680, 574, "ORGANISATIONAL", color=GOLD, weight="bold", size=13)
d.text(680, 596, "before birth and just after", color=NAVY, weight="bold", size=12)
d.text(680, 620, "androgens build the circuits themselves", color=GREY, size=11)
d.text(680, 638, "sexually dimorphic nucleus; later orientation", color=GREY, size=11)
d.text(680, 666, "PERMANENT — a window, then it closes", color=GOLD, weight="bold", size=12)
d.text(680, 686, "congenital adrenal hyperplasia is the natural test", color=GREY, size=10)

d.rect(506, 712, 348, 150, BLUE, FILL[BLUE], rx=10, width=2)
d.text(680, 738, "ACTIVATIONAL", color=BLUE, weight="bold", size=13)
d.text(680, 760, "in adulthood, on circuits already built", color=NAVY, weight="bold", size=12)
d.text(680, 784, "testosterone drives libido in BOTH sexes", color=GREY, size=11)
d.text(680, 802, "castration or oophorectomy lowers it", color=GREY, size=11)
d.text(680, 830, "REVERSIBLE — restore the hormone,", color=BLUE, weight="bold", size=12)
d.text(680, 848, "restore the behaviour", color=BLUE, weight="bold", size=12)

d.save("arcuate-switchboard-and-hormone-timing")
print("ok")
