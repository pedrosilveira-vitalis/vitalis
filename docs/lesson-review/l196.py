import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 900,
      "Why you forget, and why the delay is the experiment",
      "The serial position curve is two memory systems measured at once",
      "Top: free recall of a word list gives a U-shaped curve. The early items were rehearsed into long-term "
      "store, so the primacy end survives a delay; the final items are still sitting in working memory, so the "
      "recency end disappears the moment you insert thirty seconds of counting backwards. That single "
      "manipulation is the classic evidence for two separate stores. Middle: the forgetting mechanisms, with "
      "the one question that separates them — was the memory never stored, stored and faded, stored but "
      "crowded out, stored but uncued, or stored and kept out. Interference is the dominant explanation for "
      "everyday long-term forgetting. Bottom: proactive against retroactive interference, decided by asking "
      "which list is being tested rather than which was learned first."
      )

# ---------------- Panel A: serial position ----------------
d.rect(40, 150, 840, 300, BLUE, "none", rx=12, width=2)
d.text(460, 178, "One curve, two stores", color=BLUE, weight="bold", size=16)

m = d.axes(110, 206, 420, 164, "position in the list", "proportion recalled",
           (1, 15), (0, 1.0), ticks_x=None, ticks_y=None)

imm = [(1, .86), (2, .74), (3, .62), (4, .50), (5, .42), (6, .37), (7, .34), (8, .33),
       (9, .34), (10, .37), (11, .44), (12, .56), (13, .70), (14, .82), (15, .92)]
dly = [(1, .83), (2, .71), (3, .60), (4, .49), (5, .41), (6, .36), (7, .33), (8, .32),
       (9, .32), (10, .33), (11, .33), (12, .32), (13, .31), (14, .30), (15, .29)]
d.curve(m, imm, BLUE, 2.8)
d.curve(m, dly, RED, 2.6, dash="6,4")

px, py = m(2.4, .93)
d.text(px, py, "PRIMACY", anchor="start", color=SAGE, weight="bold", size=12)
d.text(px, py + 16, "rehearsed into long-term store", anchor="start", color=GREY, size=11)
px, py = m(13.4, .99)
d.text(px, py, "RECENCY", anchor="end", color=BLUE, weight="bold", size=12)
d.text(px, py + 16, "still in working memory", anchor="end", color=BLUE, size=11)
px, py = m(13.0, .22)
d.text(px, py, "… and gone after 30 s of counting backwards",
       anchor="end", color=RED, weight="bold", size=11)

d.legend(576, 216, [(BLUE, "immediate free recall", None),
                    (RED, "after a filled 30 s delay", "6,4")])

d.rect(576, 286, 272, 136, SAGE, FILL[SAGE], rx=10, width=2)
d.text(712, 312, "WHAT THE DELAY PROVES", color=SAGE, weight="bold", size=13)
d.text(712, 336, "primacy survives → long-term store", color=NAVY, size=12)
d.text(712, 356, "recency vanishes → short-term store", color=NAVY, size=12)
d.text(712, 384, "two ends, two systems, one list", color=GREY, weight="bold", size=12)
d.text(712, 406, "slower presentation raises primacy only", color=GREY, size=11)

# ---------------- Panel B: forgetting mechanisms ----------------
d.rect(40, 466, 840, 244, GOLD, "none", rx=12, width=2)
d.text(460, 494, "Five ways a memory fails to come back", color=GOLD, weight="bold", size=16)

rows = [
    ("Encoding failure", "it was never stored", "shallow processing; not really forgetting", GREY),
    ("Decay", "stored, then faded", "sensory and short-term store; weak for long-term", BLUE),
    ("Interference", "stored, but crowded", "the main cause of everyday long-term forgetting", RED),
    ("Retrieval failure", "stored, but uncued", "tip of the tongue; recognition beats recall", SAGE),
    ("Motivated forgetting", "stored, but kept out", "suppression is conscious, repression is not", GOLD),
]
y = 512
for name, mid, note, col in rows:
    d.rect(70, y, 200, 34, col, FILL[col], rx=7, width=2)
    d.text(170, y + 22, name, color=col, weight="bold", size=13)
    d.text(292, y + 22, mid, anchor="start", color=NAVY, weight="bold", size=12)
    d.text(506, y + 22, note, anchor="start", color=GREY, size=11)
    y += 38

# ---------------- Panel C: PI vs RI ----------------
d.rect(40, 726, 840, 150, SAGE, "none", rx=12, width=2)
d.text(460, 754, "Which interference? Ask what is being tested, not what was learned first",
       color=SAGE, weight="bold", size=16)

d.rect(70, 772, 380, 84, BLUE, FILL[BLUE], rx=10, width=2)
d.text(260, 796, "PROACTIVE — old blocks new", color=BLUE, weight="bold", size=14)
d.text(260, 818, "learned Spanish → now tested on Italian", color=NAVY, size=12)
d.text(260, 840, "the NEWER memory is the one being tested", color=GREY, weight="bold", size=12)

d.rect(470, 772, 380, 84, RED, FILL[RED], rx=10, width=2)
d.text(660, 796, "RETROACTIVE — new blocks old", color=RED, weight="bold", size=14)
d.text(660, 818, "learned Italian → now tested on Spanish", color=NAVY, size=12)
d.text(660, 840, "the OLDER memory is the one being tested", color=GREY, weight="bold", size=12)

d.save("serial-position-forgetting-and-interference")
print("ok")
