import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 918,
      "Two chemical senses, two touch pathways, one gate",
      "The spinal cord is where the exam lives: what crosses, and where",
      "Top: taste splits by mechanism, not by region of the tongue — sweet, bitter and umami run through G "
      "protein receptors and gustducin, salt comes straight through a sodium channel, sour through a proton "
      "channel. Smell is the one modality that reaches cortex without a thalamic relay, which is why an odour "
      "can summon a memory before you have named it. Middle: the two ascending somatosensory pathways, "
      "distinguished entirely by where they cross. Fine touch, vibration and position sense climb the same "
      "side of the cord and cross in the medulla; pain and temperature cross within a level or two of "
      "entering. Hemisect the cord and you get the split deficit that carries Brown-Séquard's name. Bottom: "
      "the gate, which is why rubbing a bruise helps."
      )

# ---------------- Panel A: chemical senses ----------------
d.rect(40, 170, 840, 212, GOLD, "none", rx=12, width=2)
d.text(460, 198, "The chemical senses", color=GOLD, weight="bold", size=16)

d.rect(70, 218, 390, 142, GOLD, FILL[GOLD], rx=10, width=2)
d.text(265, 242, "TASTE — split by mechanism", color=GOLD, weight="bold", size=13)
tastes = [("sweet · bitter · umami", "T1R/T2R → gustducin → PLCβ2"),
          ("salty", "Na⁺ straight through ENaC"),
          ("sour", "H⁺ through OTOP1")]
y = 266
for a, b in tastes:
    d.text(258, y, a, anchor="end", color=NAVY, weight="bold", size=11)
    d.text(272, y, b, anchor="start", color=GREY, size=11)
    y += 22
d.text(265, 340, "CN VII front · CN IX back · CN X epiglottis → NTS", color=NAVY, weight="bold", size=11)

d.rect(488, 218, 362, 142, SAGE, FILL[SAGE], rx=10, width=2)
d.text(669, 242, "SMELL — the one that skips the thalamus", color=SAGE, weight="bold", size=13)
d.text(669, 268, "GPCR → G-olf → cAMP → CNG channel", color=NAVY, size=11)
d.text(669, 288, "one receptor per neuron; combinatorial code", color=NAVY, size=11)
d.text(669, 312, "bulb → piriform cortex · amygdala · entorhinal", color=SAGE, weight="bold", size=11)
d.text(669, 340, "ammonia and menthol are trigeminal, not olfactory", color=GREY, size=11)

# ---------------- Panel B: the two pathways ----------------
d.rect(40, 398, 840, 300, BLUE, "none", rx=12, width=2)
d.text(460, 426, "Where it crosses is the whole question", color=BLUE, weight="bold", size=16)

# cord schematic
d.rect(380, 452, 160, 210, GREY, "#efe9df", rx=16, width=2.2)
d.text(460, 446, "spinal cord → medulla → thalamus", color=GREY, size=11)
d.line(380, 556, 540, 556, GREY, 1.4, dash="4,4")
d.text(548, 560, "medulla", anchor="start", color=GREY, size=10)

# DCML
d.path("M420 650 L420 560 L470 520 L500 470", BLUE, 3, "none")
d.circle(420, 650, 9, BLUE, FILL[BLUE], width=2)
d.text(300, 572, "DCML", anchor="end", color=BLUE, weight="bold", size=13)
d.text(300, 592, "fine touch · vibration", anchor="end", color=NAVY, size=11)
d.text(300, 608, "proprioception", anchor="end", color=NAVY, size=11)
d.text(300, 632, "ascends the SAME side,", anchor="end", color=BLUE, weight="bold", size=11)
d.text(300, 648, "crosses in the MEDULLA", anchor="end", color=BLUE, weight="bold", size=11)
d.text(300, 668, "both end in VPL → S1", anchor="end", color=GREY, size=10)

# spinothalamic
d.path("M500 650 L440 630 L440 470", RED, 3, "none")
d.circle(500, 650, 9, RED, FILL[RED], width=2)
d.text(620, 572, "SPINOTHALAMIC", anchor="start", color=RED, weight="bold", size=13)
d.text(620, 592, "pain · temperature", anchor="start", color=NAVY, size=11)
d.text(620, 608, "crude touch", anchor="start", color=NAVY, size=11)
d.text(620, 632, "crosses AT ENTRY,", anchor="start", color=RED, weight="bold", size=11)
d.text(620, 648, "within a level or two", anchor="start", color=RED, weight="bold", size=11)

d.text(460, 684, "hemisection → ipsilateral loss of touch and position, contralateral loss of pain and "
                 "temperature · Brown-Séquard",
       color=NAVY, weight="bold", size=12)

# ---------------- Panel C: the gate ----------------
d.rect(40, 714, 840, 174, SAGE, "none", rx=12, width=2)
d.text(460, 742, "The gate in the dorsal horn", color=SAGE, weight="bold", size=16)

d.rect(70, 762, 360, 106, BLUE, FILL[BLUE], rx=10, width=2)
d.text(250, 786, "BIG FIBRES (Aβ, touch)", color=BLUE, weight="bold", size=13)
d.text(250, 808, "EXCITE the inhibitory interneuron", color=NAVY, size=12)
d.text(250, 830, "gate CLOSES — less pain through", color=BLUE, weight="bold", size=12)
d.text(250, 854, "rubbing a bruise; TENS; spinal stimulators", color=GREY, size=11)

d.rect(490, 762, 360, 106, RED, FILL[RED], rx=10, width=2)
d.text(670, 786, "SMALL FIBRES (Aδ, C — pain)", color=RED, weight="bold", size=13)
d.text(670, 808, "INHIBIT that same interneuron", color=NAVY, size=12)
d.text(670, 830, "gate OPENS — pain gets through", color=RED, weight="bold", size=12)
d.text(670, 854, "from above, PAG and raphe can close it again", color=GREY, size=11)

d.save("chemical-senses-somatosensory-tracts-and-the-gate")
print("ok")
