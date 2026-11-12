import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 620,
      "Which disubstituted cyclohexane can get both groups equatorial?",
      "Only one of cis and trans can reach the diequatorial chair, and which one it is flips with the substitution pattern.",
      "A grid of the three disubstituted cyclohexane patterns, 1,2 and 1,3 and 1,4, against cis and "
      "trans. For 1,2 and 1,4 the trans isomer interconverts between diequatorial and diaxial while the "
      "cis isomer is axial-equatorial in both chairs; for 1,3 the two are swapped. A rule panel below "
      "states that for an even relationship trans reaches diequatorial and for an odd relationship cis does.")

COL_C, COL_T = 370, 660
ROW_X = 110
y = 118

d.text(COL_C, 104, "cis", color=NAVY, weight="bold", size=19)
d.text(COL_T, 104, "trans", color=NAVY, weight="bold", size=19)

rows = [
    ("1,2", "a,e in both chairs", "equivalent chairs", GREY,
            "e,e  ↔  a,a", "diequatorial wins", BLUE),
    ("1,3", "e,e  ↔  a,a", "diequatorial wins", BLUE,
            "a,e in both chairs", "equivalent chairs", GREY),
    ("1,4", "a,e in both chairs", "equivalent chairs", GREY,
            "e,e  ↔  a,a", "diequatorial wins", BLUE),
]

CW, CH = 262, 84
for label, ctxt, csub, ccol, ttxt, tsub, tcol in rows:
    d.text(ROW_X, y + 50, label + "-disubstituted", anchor="middle", color=NAVY, weight="bold", size=17)
    for cx, txt, sub, col in ((COL_C, ctxt, csub, ccol), (COL_T, ttxt, tsub, tcol)):
        d.rect(cx - CW / 2, y, CW, CH, col, FILL[col], rx=10, width=2)
        d.text(cx, y + 36, txt, color=col, weight="bold", size=19)
        d.text(cx, y + 62, sub, color=GREY, size=14)
    y += CH + 18

# rule panel
py = y + 14
d.rect(60, py, 780, 112, RED, FILL[RED], rx=12, width=2)
d.text(450, py + 28, "The pattern", color=RED, weight="bold", size=19)
d.text(450, py + 56, "1,2 and 1,4 (even gap): the TRANS isomer reaches diequatorial.",
       color=NAVY, size=16)
d.text(450, py + 80, "1,3 (odd gap): the CIS isomer reaches diequatorial.",
       color=NAVY, size=16)
d.text(450, py + 102, "The other isomer is locked axial-equatorial in both chairs, so with identical groups its two chairs are equal.",
       color=GREY, size=12)

d.legend(60, 576, [(BLUE, "Blue: a chair exists with both groups equatorial", False),
                   (GREY, "Grey: one axial and one equatorial whichever way the ring flips", False)])

d.save("cyclohexane-cis-trans-grid")
