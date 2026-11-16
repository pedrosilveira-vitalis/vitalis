import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 846,
      "Learning is a lasting change that experience produced",
      "Not maturation, not fatigue, not a drug — and it need not show up in behaviour straight away",
      "Top: the definition broken into its three tests, with examples of what each one excludes — a deepening "
      "voice is maturation, tiredness is a temporary state, and a surgeon who has only read the textbook has "
      "learned even though nothing is visible yet. Middle left: the ladder of learning types, from the "
      "non-associative pair habituation and sensitisation, through the two associative kinds, to observational "
      "and insight learning, with innate behaviour marked off below as not learning at all. Middle right: the "
      "four theoretical frameworks side by side with their central claim, their key names and the finding each "
      "struggles with. Bottom: the brain structures, with the hippocampus for new declarative memory, the "
      "amygdala for fear conditioning, the cerebellum for conditioned motor responses and the basal ganglia for "
      "habits, and the Hebbian rule underneath.")

# ---------------- Panel A: definition ----------------
d.rect(40, 136, 840, 150, BLUE, "none", rx=12, width=2)
d.text(460, 164, "\"A relatively permanent change in behaviour, or in the capacity for it, from experience\"",
       color=BLUE, weight="bold", size=15)

cards = [("relatively permanent", "so not fatigue,", "a drug, or adaptation", SAGE),
         ("behaviour OR capacity", "so it counts even if", "nothing is acted out yet", GOLD),
         ("from experience", "so not maturation:", "a voice deepening is not learning", RED)]
x = 70
for a, b, c, col in cards:
    d.rect(x, 192, 256, 76, col, FILL[col], rx=10, width=2)
    d.text(x + 128, 214, a, color=col, weight="bold", size=14)
    d.text(x + 128, 238, b, color=NAVY, size=12)
    d.text(x + 128, 256, c, color=NAVY, size=12)
    x += 270

# ---------------- Panel B: kinds of learning ----------------
d.rect(40, 302, 404, 318, SAGE, "none", rx=12, width=2)
d.text(242, 330, "What counts as learning", color=SAGE, weight="bold", size=16)

rows = [("non-associative", "habituation — less response to", "a harmless repeated stimulus", BLUE),
        ("", "sensitisation — more response", "after something noxious", BLUE),
        ("associative", "classical: stimulus with stimulus", "operant: behaviour with consequence", SAGE),
        ("cognitive / social", "observational learning, modelling,", "latent learning, insight", GOLD)]
y = 348
for lab, l1, l2, col in rows:
    if lab:
        d.text(70, y, lab, anchor="start", color=col, weight="bold", size=13)
        y += 18
    d.text(84, y, l1, anchor="start", color=NAVY, size=12)
    d.text(84, y + 15, l2, anchor="start", color=NAVY, size=12)
    y += 38

d.rect(62, 548, 360, 58, RED, FILL[RED], rx=10, width=2)
d.text(242, 570, "NOT learning: reflexes, fixed action patterns", color=RED, weight="bold", size=13)
d.text(242, 584, "— these come built in, not from experience", color=NAVY, size=12)

# ---------------- Panel C: frameworks ----------------
d.rect(466, 302, 414, 318, GOLD, "none", rx=12, width=2)
d.text(673, 330, "Four frameworks, four blind spots", color=GOLD, weight="bold", size=16)

fw = [("Behaviourism", "S–R bonds and reinforcement", "Watson, Skinner, Pavlov",
       "stuck on latent learning", BLUE),
      ("Cognitive", "mental maps and expectancies", "Tolman", "harder to operationalise", SAGE),
      ("Biological", "evolution constrains what is learnable", "Lorenz, Tinbergen, Seligman",
       "underrates flexibility", RED),
      ("Social learning", "watching others is enough", "Bandura", "underrates biology", GOLD)]
y = 356
for name, claim, who, weak, col in fw:
    d.text(492, y, name, anchor="start", color=col, weight="bold", size=14)
    d.text(492, y + 18, claim, anchor="start", color=NAVY, size=12)
    d.text(492, y + 35, who + "  •  " + weak, anchor="start", color=GREY, size=11)
    y += 62

# ---------------- Panel D: brain ----------------
d.rect(40, 636, 840, 190, NAVY, "none", rx=12, width=2)
d.text(460, 664, "Different kinds of learning, different structures",
       color=NAVY, weight="bold", size=16)

bits = [("hippocampus", "new declarative memories", BLUE),
        ("amygdala", "fear conditioning", RED),
        ("cerebellum", "conditioned motor responses", SAGE),
        ("basal ganglia", "habits and skills", GOLD)]
x = 70
for name, job, col in bits:
    d.rect(x, 684, 192, 64, col, FILL[col], rx=10, width=2)
    d.text(x + 96, 708, name, color=col, weight="bold", size=14)
    d.text(x + 96, 732, job, color=NAVY, size=12)
    x += 200

d.text(460, 778, "H.M. lost the first and kept the rest — which is how we know they are separate systems",
       color=GREY, size=13)
d.text(460, 808, "Underneath all of it: neurons that fire together wire together (LTP at the synapse)",
       color=NAVY, weight="bold", size=15)

d.save("what-learning-is-and-the-four-frameworks")
print("ok")
