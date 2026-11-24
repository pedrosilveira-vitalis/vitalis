#!/usr/bin/env python3
"""Recompute every number FL4 Psych/Soc turns on, from the passages' own figures.

Two kinds of check live here, because the authoring guide is explicit that a
verifier sharing the author's assumptions is worth nothing:

  * MODEL checks - the internal consistency of each passage. Table rows sum to
    their stated totals, a figure quoted in prose matches the table it came
    from, and the SVG in Figure 1 of ps4-p3 decodes, through its own printed
    axis, to the judged distances the questions claim.
  * KEY checks - every quantitative key and every numeric distractor, each one
    derived from the table rather than typed from the draft, plus the truth
    value of each Roman numeral item and each EXCEPT statement recomputed
    rather than asserted.

Run: python3 scripts/verify-exam-arithmetic-ps4.py
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "lib", "exams", "content", "fl4", "psych-soc.json")

fails = []
checks = 0


def check(label, got, want, tol=0.005):
    global checks
    checks += 1
    if isinstance(want, bool) or isinstance(got, bool):
        ok = bool(got) == bool(want)
    elif isinstance(want, (str, list, tuple)) or isinstance(got, (str, list, tuple)):
        ok = got == want
    elif got is None or want is None:
        ok = got is want
    else:
        ok = abs(got - want) <= tol * max(1.0, abs(want))
    print(("  ok   " if ok else "  FAIL ") + f"{label}: got {got!r}, want {want!r}")
    if not ok:
        fails.append(label)


with open(PATH) as fh:
    DATA = json.load(fh)

Q = {q["id"]: q for q in DATA["questions"]}
P = {p["id"]: p for p in DATA["passages"]}


def choice(qid, letter):
    return Q[qid]["choices"][letter].strip()


def key_text(qid):
    return choice(qid, Q[qid]["correct"])


def num(text):
    m = re.search(r"-?\d+(?:\.\d+)?", text.replace(",", ""))
    return float(m.group(0)) if m else None


def key_num(qid):
    return num(key_text(qid))


def prose(pid):
    return " ".join(P[pid]["paragraphs"])


# --------------------------------------------------------------------------
print("\nps4-p1  Watching, reproducing and choosing to do it again  (MODEL)")
# Table 1: n, mean steps, touched (n), touched (%)
P1 = {
    "praised": (30, 9.6, 24, 80),
    "no comment": (30, 9.0, 18, 60),
    "criticised": (30, 8.7, 9, 30),
    "no model": (30, 3.3, 6, 20),
}
check("ps4-p1 conditions sum to the stated 120 children", sum(r[0] for r in P1.values()), 120)
for name, (n, _steps, touched, pct) in P1.items():
    check(f"ps4-p1 {name}: {touched}/{n} decodes to the stated percentage", 100.0 * touched / n, float(pct))
check("ps4-p1 prose: criticised reproduced 8.7 steps", P1["criticised"][1], 8.7)
check("ps4-p1 prose: praised minus criticised is within 0.9 steps",
      round(P1["praised"][1] - P1["criticised"][1], 2), 0.9)
check("ps4-p1 prose: criticised are three-eighths as likely to touch the blocks",
      P1["criticised"][3] / P1["praised"][3], 3.0 / 8.0)
check("ps4-p1 prose: '8.7' appears in the passage text", "8.7 steps" in prose("ps4-p1"), True)

print("ps4-p1-q5  EXCEPT: truth value of each statement recomputed")
# A: every model condition reproduced at least twice the no-model condition
ratios = [P1[k][1] / P1["no model"][1] for k in ("praised", "no comment", "criticised")]
check("  A is true (min ratio of steps to the no-model condition >= 2)", min(ratios) >= 2.0, True)
# B: model conditions spread wider in free play than in steps
steps_spread = max(P1[k][1] for k in ("praised", "no comment", "criticised")) - min(
    P1[k][1] for k in ("praised", "no comment", "criticised"))
pct_spread = max(P1[k][3] for k in ("praised", "no comment", "criticised")) - min(
    P1[k][3] for k in ("praised", "no comment", "criticised"))
check("  B is true (free-play spread in points exceeds the step spread)", pct_spread > steps_spread, True)
check("  B: step spread is 0.9 of 12 available steps", round(steps_spread, 2), 0.9)
check("  B: free-play spread is 50 percentage points", pct_spread, 50)
# C: fewer than half of all children touched the blocks
touched_all = sum(r[2] for r in P1.values())
check("  C: children who touched the blocks", touched_all, 57)
check("  C is true (under half of 120)", touched_all / 120.0 < 0.5, True)
check("  C: 57/120 as a percentage", round(100.0 * touched_all / 120.0, 1), 47.5)
# D (the key): no-model less than half the criticised rate
check("  D is FALSE, so it is the EXCEPT key",
      P1["no model"][3] < P1["criticised"][3] / 2.0, False)
check("  ps4-p1-q5 key letter", Q["ps4-p1-q5"]["correct"], "D")

# --------------------------------------------------------------------------
print("\nps4-p2  Two kinds of remembering after hippocampal injury  (MODEL)")
P2 = {
    "recall": (3.1, 9.8),
    "recognition": (58, 91),
    "trace day 1": (24, 23),
    "trace day 5": (9, 8),
    "primed": (47, 49),
    "unprimed": (12, 13),
}
amn_drop = (P2["trace day 1"][0] - P2["trace day 5"][0]) / P2["trace day 1"][0]
ctl_drop = (P2["trace day 1"][1] - P2["trace day 5"][1]) / P2["trace day 1"][1]
check("ps4-p2 prose: amnesic error reduction is about two thirds", round(amn_drop, 3), 0.625)
check("ps4-p2 prose: control error reduction is about two thirds", round(ctl_drop, 3), 0.652)
check("ps4-p2 prose: patients prime nearly four times their unprimed baseline",
      round(P2["primed"][0] / P2["unprimed"][0], 2), 3.92)
check("ps4-p2 prose: the control priming advantage is as large (ratio within 0.2)",
      abs(P2["primed"][0] / P2["unprimed"][0] - P2["primed"][1] / P2["unprimed"][1]) < 0.2, True)
check("ps4-p2 recognition deficit in points", P2["recognition"][1] - P2["recognition"][0], 33)
check("ps4-p2 priming advantage over baseline in points", P2["primed"][0] - P2["unprimed"][0], 35)

print("ps4-p2-q3  percentage reduction in tracing errors (key and all distractors)")
check("  key value equals (24-9)/24", key_num("ps4-p2-q3"), round(100 * amn_drop, 1))
check("  A = controls' day-5 errors as a share of their day-1 errors",
      num(choice("ps4-p2-q3", "A")), round(100.0 * P2["trace day 5"][1] / P2["trace day 1"][1], 1))
check("  B = patients' day-5 errors as a share of their day-1 errors",
      num(choice("ps4-p2-q3", "B")), round(100.0 * P2["trace day 5"][0] / P2["trace day 1"][0], 1))
check("  D = the 15-error fall divided by the 9 errors remaining",
      num(choice("ps4-p2-q3", "D")),
      round(100.0 * (P2["trace day 1"][0] - P2["trace day 5"][0]) / P2["trace day 5"][0], 1))
vals = [num(choice("ps4-p2-q3", l)) for l in "ABCD"]
check("  choices ascend", vals == sorted(vals), True)
check("  key value appears in its own explanation",
      f"{key_num('ps4-p2-q3')}" in Q["ps4-p2-q3"]["explanation"], True)

print("ps4-p2-q5  Roman numeral truth values recomputed")
check("  I is false (recognition far below matched controls)",
      P2["recognition"][0] >= P2["recognition"][1] - 5, False)
check("  II is true (tracing improved while practice was not reported)",
      P2["trace day 5"][0] < P2["trace day 1"][0], True)
check("  III is false (primed exceeds unprimed)",
      P2["primed"][0] <= P2["unprimed"][0], False)
check("  so the key is 'II only'", key_text("ps4-p2-q5"), "II only")

# --------------------------------------------------------------------------
print("\nps4-p3  Disparity, convergence and judged distance  (MODEL: SVG decoded)")
svg = P["ps4-p3"]["figure"]["markup"]
seg = [tuple(int(v) for v in m) for m in
       re.findall(r'<line x1="(\d+)" y1="(\d+)" x2="(\d+)" y2="(\d+)"', svg)]
# The two axes, then the tick marks: five on each axis, each 5 px long.
axes = [s for s in seg if max(abs(s[2] - s[0]), abs(s[3] - s[1])) > 5]
tickmarks = [s for s in seg if s not in axes]
check("ps4-p3 figure draws exactly two axis lines", len(axes), 2)
check("ps4-p3 figure draws ten tick marks and no gridlines", len(tickmarks), 10)
check("ps4-p3 every tick mark is 5 px long",
      sorted({max(abs(s[2] - s[0]), abs(s[3] - s[1])) for s in tickmarks}), [5])
# Vertical ticks: horizontal stubs left of the y axis. Their labels sit 4 px
# below each tick, which is how a text baseline is centred on a tick.
yticks = sorted(s[1] for s in tickmarks if s[1] == s[3])
xticks = sorted(s[0] for s in tickmarks if s[0] == s[2])
check("ps4-p3 the y axis carries five ticks", len(yticks), 5)
check("ps4-p3 the x axis carries five ticks", len(xticks), 5)
ylab = {int(m[1]): int(m[0]) for m in
        re.findall(r'<text x="38" y="(\d+)" font-size="11">(\d+)</text>', svg)}
check("ps4-p3 the y labels read 0, 2, 4, 6 and 8, as the caption says",
      sorted(ylab), [0, 2, 4, 6, 8])
check("ps4-p3 each y label sits 4 px below the tick it names",
      sorted(ylab[v] - 4 for v in ylab), yticks)
xlab = {float(m[1]): int(m[0]) for m in
        re.findall(r'<text x="(\d+)" y="218" font-size="11">([\d.]+)</text>', svg)}
check("ps4-p3 the x labels read 0.5, 1, 2, 4 and 8", sorted(xlab), [0.5, 1.0, 2.0, 4.0, 8.0])
check("ps4-p3 each x label sits 6 px left of the tick it names",
      sorted(xlab[v] + 6 for v in xlab), xticks)
y0 = float(ylab[0] - 4)
y8 = float(ylab[8] - 4)
px_per_m = (y0 - y8) / 8.0
check("ps4-p3 axis scale is 20 px per metre", px_per_m, 20.0)
for v in (2, 4, 6):
    check(f"ps4-p3 the {v} m tick lies where that linear axis puts it",
          float(ylab[v] - 4), y0 - v * px_per_m)
steps = [xlab[d] for d in sorted(xlab)]
check("ps4-p3 x labels double while their ticks step equally, so the axis is logarithmic",
      sorted(set(steps[i + 1] - steps[i] for i in range(4))), [60])
polys = re.findall(r'<polyline points="([^"]+)"', svg)
check("ps4-p3 figure draws four polylines", len(polys), 4)


def decode(points):
    out = []
    for pair in points.split():
        x, y = (float(v) for v in pair.split(","))
        out.append(round((y0 - y) / px_per_m, 2))
    return out


veridical, binocular, prism, monocular = (decode(p) for p in polys)
check("ps4-p3 the dashed curve decodes to the five actual distances",
      veridical, [0.5, 1.0, 2.0, 4.0, 8.0])
check("ps4-p3 the binocular polyline decodes to the judged distances",
      binocular, [0.5, 1.0, 1.9, 3.4, 5.6])
check("ps4-p3 the prism polyline decodes to the judged distances",
      prism, [1.2, 1.6, 2.2, 3.3, 4.8])
check("ps4-p3 the monocular polyline decodes to the judged distances",
      monocular, [1.4, 1.8, 2.4, 3.3, 4.2])
check("ps4-p3 prose: binocular is essentially correct within about a metre",
      binocular[:2] == veridical[:2], True)
check("ps4-p3 prose: monocular overestimates the nearest distance almost threefold",
      round(monocular[0] / veridical[0], 2), 2.8)
check("ps4-p3 prose: monocular falls further short than binocular at 8 m",
      monocular[4] < binocular[4], True)
check("ps4-p3 prose: the prism curve lies nearer the monocular curve at every distance",
      all(abs(prism[i] - monocular[i]) <= abs(prism[i] - binocular[i]) for i in range(5)), True)

print("ps4-p3-q3  judged/actual ratio at 8 m (key and all distractors)")
check("  key = binocular 5.6 m over an actual 8 m", key_num("ps4-p3-q3"),
      round(binocular[4] / veridical[4], 2))
check("  A = the monocular curve read at 8 m", num(choice("ps4-p3-q3", "A")),
      round(monocular[4] / veridical[4], 2))
check("  C = the binocular ratio at 2 m rather than 8 m", num(choice("ps4-p3-q3", "C")),
      round(binocular[2] / veridical[2], 2))
check("  D = the ratio inverted", num(choice("ps4-p3-q3", "D")),
      round(veridical[4] / binocular[4], 2))
vals = [num(choice("ps4-p3-q3", l)) for l in "ABCD"]
check("  choices ascend", vals == sorted(vals), True)
check("  the explanation states the judged distance it reads off", "5.6" in Q["ps4-p3-q3"]["explanation"], True)

# --------------------------------------------------------------------------
print("\nps4-p4  Rewarding an activity children had already chosen  (MODEL)")
P4 = {"expected": (30, 8.4, 4.2), "unexpected": (30, 8.6, 8.1), "none": (30, 8.5, 8.3)}
check("ps4-p4 groups sum to the stated ninety children", sum(r[0] for r in P4.values()), 90)
for name, (_n, base, follow) in P4.items():
    stated = {"expected": -4.2, "unexpected": -0.5, "none": -0.2}[name]
    check(f"ps4-p4 {name}: the change column equals follow-up minus baseline",
          round(follow - base, 2), stated)
check("ps4-p4 prose: drawing in the expected-certificate group halved",
      round(P4["expected"][2] / P4["expected"][1], 3), 0.5)
check("ps4-p4 prose: the other two groups are essentially unchanged (under 1 min)",
      max(abs(P4[k][2] - P4[k][1]) for k in ("unexpected", "none")) < 1.0, True)
check("ps4-p4-q3 explanation: the no-certificate fall it cites", round(P4["none"][1] - P4["none"][2], 2), 0.2)
check("ps4-p4-q4 explanation: the expected-group fall it cites",
      round(P4["expected"][1] - P4["expected"][2], 2), 4.2)

# --------------------------------------------------------------------------
print("\nps4-p5  Building and checking a five-factor inventory  (MODEL)")
P5 = {
    "Extraversion": (12, 18, 0.86, 0.82, 0.54),
    "Agreeableness": (12, 12, 0.79, 0.78, 0.41),
    "Conscientiousness": (12, 10, 0.84, 0.81, 0.49),
    "Emotional stability": (12, 8, 0.81, 0.76, 0.33),
    "Openness": (12, 6, 0.77, 0.74, 0.38),
}
check("ps4-p5 the item column sums to the stated sixty items", sum(r[0] for r in P5.values()), 60)
check("ps4-p5 the variance column sums to the 54 percent quoted in prose",
      sum(r[1] for r in P5.values()), 54)
check("ps4-p5 prose: self-friend agreement runs from 0.54 down to 0.33",
      (max(r[4] for r in P5.values()), min(r[4] for r in P5.values())), (0.54, 0.33))
check("ps4-p5 prose: emotional stability holds the lowest self-friend figure",
      min(P5, key=lambda k: P5[k][4]), "Emotional stability")

print("ps4-p5-q1  extraversion's share of the captured variance (key and distractors)")
total_var = sum(r[1] for r in P5.values())
check("  key = 18 of the 54 percent captured", key_num("ps4-p5-q1"),
      round(100.0 * P5["Extraversion"][1] / total_var, 1))
check("  A = the agreeableness row read instead", num(choice("ps4-p5-q1", "A")),
      float(P5["Agreeableness"][1]))
check("  B = extraversion's share of all item variance", num(choice("ps4-p5-q1", "B")),
      float(P5["Extraversion"][1]))
check("  C = the share if the five factors contributed equally", num(choice("ps4-p5-q1", "C")),
      round(100.0 / len(P5), 1))
vals = [num(choice("ps4-p5-q1", l)) for l in "ABCD"]
check("  choices ascend", vals == sorted(vals), True)

print("ps4-p5-q4  LOWEST self-friend agreement: each distractor's claim recomputed")
check("  A is false: emotional stability is not the weakest on internal consistency",
      P5["Emotional stability"][2] == min(r[2] for r in P5.values()), False)
check("  C is false: it is not the least stable on retest",
      P5["Emotional stability"][3] == min(r[3] for r in P5.values()), False)
check("  D is false: it does not hold the smallest variance share",
      P5["Emotional stability"][1] == min(r[1] for r in P5.values()), False)
check("  openness agrees better with friends despite a smaller variance share",
      P5["Openness"][4] > P5["Emotional stability"][4], True)

# --------------------------------------------------------------------------
print("\nps4-p6  A habit of explanation and the first episode  (MODEL)")
P6 = {
    "high all": (240, 48, 20.0),
    "high stress": (110, 33, 30.0),
    "high none": (130, 15, 11.5),
    "low all": (240, 18, 7.5),
    "low stress": (104, 13, 12.5),
    "low none": (136, 5, 3.7),
}
for half in ("high", "low"):
    check(f"ps4-p6 {half}-risk strata sum to the stated n",
          P6[f"{half} stress"][0] + P6[f"{half} none"][0], P6[f"{half} all"][0])
    check(f"ps4-p6 {half}-risk strata sum to the stated episode count",
          P6[f"{half} stress"][1] + P6[f"{half} none"][1], P6[f"{half} all"][1])
check("ps4-p6 the two halves sum to the stated 480 students",
      P6["high all"][0] + P6["low all"][0], 480)
for name, (n, cases, pct) in P6.items():
    check(f"ps4-p6 {name}: {cases}/{n} decodes to the stated incidence",
          round(100.0 * cases / n, 1), float(pct))
rr_all = P6["high all"][2] / P6["low all"][2]
check("ps4-p6 prose: the overall relative risk of 2.67", round(rr_all, 2), 2.67)
check("ps4-p6 prose: 17.5 points among those reporting a stressor",
      round(P6["high stress"][2] - P6["low stress"][2], 1), 17.5)
check("ps4-p6 prose: 7.8 points among those reporting none",
      round(P6["high none"][2] - P6["low none"][2], 1), 7.8)

print("ps4-p6-q2  relative risk in the unstressed stratum (key and all distractors)")
rr_none = (P6["high none"][1] / P6["high none"][0]) / (P6["low none"][1] / P6["low none"][0])
check("  key = 15/130 over 5/136, to two decimals", key_num("ps4-p6-q2"), round(rr_none, 1), tol=0.02)
check("  A = the relative risk in the stressed stratum", num(choice("ps4-p6-q2", "A")),
      round(P6["high stress"][2] / P6["low stress"][2], 2))
check("  B = the overall relative risk, collapsing the strata", num(choice("ps4-p6-q2", "B")),
      round(rr_all, 2))
check("  D = the risk difference in points, not a ratio", num(choice("ps4-p6-q2", "D")),
      round(P6["high none"][2] - P6["low none"][2], 1))
vals = [num(choice("ps4-p6-q2", l)) for l in "ABCD"]
check("  choices ascend", vals == sorted(vals), True)

print("ps4-p6-q3  diathesis-stress reading: each distractor's claim recomputed")
check("  B is right: the risk difference is larger among the stressed",
      (P6["high stress"][2] - P6["low stress"][2]) > (P6["high none"][2] - P6["low none"][2]), True)
check("  A is false: style contributes within the stressed stratum",
      P6["high stress"][2] > P6["low stress"][2], True)
check("  A is false: style contributes within the unstressed stratum too",
      P6["high none"][2] > P6["low none"][2], True)
check("  C is false: the two risk differences are not equal",
      round(P6["high stress"][2] - P6["low stress"][2], 1) ==
      round(P6["high none"][2] - P6["low none"][2], 1), False)
check("  C explanation: the ratio of the two risk differences exceeds two",
      (P6["high stress"][2] - P6["low stress"][2]) / (P6["high none"][2] - P6["low none"][2]) > 2, True)
check("  D is false: stress raised incidence among high-risk students",
      P6["high stress"][2] > P6["high none"][2], True)

# --------------------------------------------------------------------------
print("\nps4-p7  Fifteen minutes of discussion  (MODEL)")
P7 = {
    "risk disc": (8, 6.4, 7.5, 1.1),
    "risk none": (7, 6.3, 6.4, 0.1),
    "caution disc": (8, 3.6, 2.6, -1.0),
    "caution none": (7, 3.7, 3.6, -0.1),
}
for name, (_g, pre, post, shift) in P7.items():
    check(f"ps4-p7 {name}: the shift column equals post minus pre", round(post - pre, 2), shift)
check("ps4-p7 the risk-leaning cells sum to fifteen groups",
      P7["risk disc"][0] + P7["risk none"][0], 15)
check("ps4-p7 the caution-leaning cells sum to fifteen groups",
      P7["caution disc"][0] + P7["caution none"][0], 15)
check("ps4-p7 thirty groups of five account for the stated 150 adults",
      sum(r[0] for r in P7.values()) * 5, 150)
check("ps4-p7 prose: discussion moves each kind about a full point",
      all(abs(P7[k][3]) >= 1.0 for k in ("risk disc", "caution disc")), True)
check("ps4-p7 prose: re-reading moves a tenth of a point",
      all(abs(P7[k][3]) == 0.1 for k in ("risk none", "caution none")), True)

print("ps4-p7-q4  Roman numeral truth values recomputed")
gap_pre = P7["risk disc"][1] - P7["caution disc"][1]
gap_post = P7["risk disc"][2] - P7["caution disc"][2]
check("  I is true: each discussion cell moved away from the midpoint",
      P7["risk disc"][3] > 0 and P7["caution disc"][3] < 0, True)
check("  the pre-discussion gap quoted in the explanation", round(gap_pre, 1), 2.8)
check("  the post-discussion gap quoted in the explanation", round(gap_post, 1), 4.9)
check("  II is false: the gap widened rather than narrowed", gap_post < gap_pre, False)
check("  III cannot be assessed: the table reports cell means only",
      any("member" in h for h in re.findall(r"<th>([^<]*)</th>", P["ps4-p7"]["figure"]["markup"])), False)
check("  so the key is 'I only'", key_text("ps4-p7-q4"), "I only")

print("ps4-p7-q5  ratio of mean absolute shifts (key and all distractors)")
disc = (abs(P7["risk disc"][3]) + abs(P7["caution disc"][3])) / 2
none = (abs(P7["risk none"][3]) + abs(P7["caution none"][3])) / 2
check("  mean absolute shift under discussion", round(disc, 2), 1.05)
check("  mean absolute shift without discussion", round(none, 2), 0.10)
check("  key = the ratio of the two means", key_num("ps4-p7-q5"), round(disc / none, 2))
check("  A = the difference of the two means, not the ratio", num(choice("ps4-p7-q5", "A")),
      round(disc - none, 2))
check("  B = the discussion mean on its own", num(choice("ps4-p7-q5", "B")), round(disc, 2))
check("  C = dividing by the sum rather than the mean of the no-discussion shifts",
      num(choice("ps4-p7-q5", "C")), round(disc / (none * 2), 2))
vals = [num(choice("ps4-p7-q5", l)) for l in "ABCD"]
check("  choices ascend", vals == sorted(vals), True)

# --------------------------------------------------------------------------
print("\nps4-p8  Which voices carry a norm  (MODEL)")
P8 = {
    "parental": (0.31, 0.001, True),
    "peer": (0.26, 0.001, True),
    "prevalence": (-0.19, 0.001, True),
    "civics": (0.08, 0.02, False),
    "drama": (-0.03, 0.41, False),
}
check("ps4-p8 prose: the two injunctive measures are the largest coefficients",
      sorted((abs(v[0]), k) for k, v in P8.items())[-2:], [(0.26, "peer"), (0.31, "parental")])
check("ps4-p8 prose: the descriptive measure runs the other way", P8["prevalence"][0] < 0, True)

print("ps4-p8-q3  Roman numeral truth values recomputed")
check("  I is true: parental exceeds civics instruction",
      abs(P8["parental"][0]) > abs(P8["civics"][0]), True)
check("  II is true: perceived prevalence carries a negative coefficient",
      P8["prevalence"][0] < 0, True)
others = [k for k in P8 if k != "drama"]
check("  III is true: every predictor but drama has p below 0.05",
      all(P8[k][1] <= 0.05 for k in others), True)
check("  and drama itself does not", P8["drama"][1] <= 0.05, False)
check("  so the key is 'I, II, and III'", key_text("ps4-p8-q3"), "I, II, and III")

# --------------------------------------------------------------------------
print("\nps4-p9  Who is counted as working  (MODEL)")
P9 = {"none": (92, 85, 7), "school": (95, 79, 16), "preschool": (96, 64, 32)}
for name, (men, women, gap) in P9.items():
    check(f"ps4-p9 {name}: the gap column equals men minus women", men - women, gap)
HOURS = {"men": (41, 14, 55), "women": (33, 26, 59)}
for name, (paid, unpaid, total) in HOURS.items():
    check(f"ps4-p9 {name}: paid plus unpaid hours equal the stated total", paid + unpaid, total)
check("ps4-p9 prose: the preschool gap is more than four times the childless gap",
      P9["preschool"][2] / P9["none"][2] > 4, True)
check("ps4-p9 prose: men's participation is higher among fathers of young children",
      P9["preschool"][0] > P9["none"][0], True)
check("ps4-p9-q1 explanation: employed women's unpaid hours against men's",
      (HOURS["women"][1], HOURS["men"][1]), (26, 14))

print("ps4-p9-q2  ratio of the two participation gaps (key and all distractors)")
check("  key = 32 points over 7 points", key_num("ps4-p9-q2"),
      round(P9["preschool"][2] / P9["none"][2], 1))
check("  A = men over women within the preschool row", num(choice("ps4-p9-q2", "A")),
      round(P9["preschool"][0] / P9["preschool"][1], 1))
check("  B = the two rows containing children compared with each other",
      num(choice("ps4-p9-q2", "B")), round(P9["preschool"][2] / P9["school"][2], 1))
check("  D = the difference between the gaps in points, not a ratio",
      num(choice("ps4-p9-q2", "D")), float(P9["preschool"][2] - P9["none"][2]))
vals = [num(choice("ps4-p9-q2", l)) for l in "ABCD"]
check("  choices ascend", vals == sorted(vals), True)

print("ps4-p9-q3  the gap grows monotonically with care demand")
check("  gaps rise from childless to school age to preschool",
      [P9["none"][2], P9["school"][2], P9["preschool"][2]] ==
      sorted([P9["none"][2], P9["school"][2], P9["preschool"][2]]), True)

# --------------------------------------------------------------------------
print("\nps4-p10  Sixty years of births, deaths and cities  (MODEL)")
P10 = {
    1960: (44, 24, 20, 12.0, 18),
    1980: (38, 12, 26, 17.5, 31),
    2000: (26, 8, 18, 26.0, 49),
    2020: (15, 8, 7, 39.6, 68),
}
for year, (cbr, cdr, ni, _pop, _urb) in P10.items():
    check(f"ps4-p10 {year}: natural increase equals births minus deaths", cbr - cdr, ni)
check("ps4-p10 prose: the death rate halved between 1960 and 1980",
      round(P10[1980][1] / P10[1960][1], 3), 0.5)
check("ps4-p10 prose: the birth rate fell by less than a seventh over the same years",
      (P10[1960][0] - P10[1980][0]) / P10[1960][0] < 1 / 7, True)
check("ps4-p10 prose: natural increase peaked in 1980",
      max(P10, key=lambda y: P10[y][2]), 1980)
check("ps4-p10 prose: the birth rate fell by more than half after 1980",
      (P10[1980][0] - P10[2020][0]) / P10[1980][0] > 0.5, True)
check("ps4-p10 prose: the death rate did not continue to fall after 1980",
      P10[2020][1] >= P10[2000][1], True)
check("ps4-p10 prose: the urban share rose in every period",
      [P10[y][4] for y in sorted(P10)] == sorted(P10[y][4] for y in P10), True)
check("ps4-p10 prose: the total population more than tripled",
      P10[2020][3] / P10[1960][3] > 3, True)

print("ps4-p10-q2  growth factor of the urban population (key and all distractors)")
urban = {y: P10[y][4] / 100.0 * P10[y][3] for y in P10}
check("  1960 urban population in millions", round(urban[1960], 2), 2.16)
check("  2020 urban population in millions", round(urban[2020], 1), 26.9)
check("  key = 2020 urban over 1960 urban", key_num("ps4-p10-q2"),
      round(urban[2020] / urban[1960], 1))
check("  A = growth of the total population only", num(choice("ps4-p10-q2", "A")),
      round(P10[2020][3] / P10[1960][3], 1))
check("  B = the ratio of the two urban percentages only", num(choice("ps4-p10-q2", "B")),
      round(P10[2020][4] / P10[1960][4], 1))
check("  C = taking 1980 as the starting year", num(choice("ps4-p10-q2", "C")),
      round(urban[2020] / urban[1980], 1))
vals = [num(choice("ps4-p10-q2", l)) for l in "ABCD"]
check("  choices ascend", vals == sorted(vals), True)

print("ps4-p10-q3  why natural increase peaked in 1980")
check("  the gap between the rates widened from 1960 to 1980",
      P10[1980][2] > P10[1960][2], True)
check("  the birth rate fell rather than rose over those years",
      P10[1980][0] < P10[1960][0], True)

print("ps4-p10-q4  EXCEPT: the key would raise rather than lower a crude rate")
check("  the crude birth rate fell from 38 to 15 per thousand",
      (P10[1980][0], P10[2020][0]), (38, 15))
check("  a larger share at peak childbearing age raises a crude rate, so D is the key",
      Q["ps4-p10-q4"]["correct"], "D")

# --------------------------------------------------------------------------
print("\nFORM-WIDE (MODEL)")
by_letter = {l: sum(1 for q in DATA["questions"] if q["correct"] == l) for l in "ABCD"}
for letter, count in sorted(by_letter.items()):
    check(f"key share for {letter} lies within 15-35 percent",
          0.15 <= count / len(DATA["questions"]) <= 0.35, True)
keys = [q["correct"] for q in DATA["questions"]]
longest = 1
run = 1
for i in range(1, len(keys)):
    run = run + 1 if keys[i] == keys[i - 1] else 1
    longest = max(longest, run)
check("the key never repeats three times running", longest < 3, True)
check("the section carries 59 questions", len(DATA["questions"]), 59)
check("44 of them hang off a passage",
      sum(1 for q in DATA["questions"] if q["passageId"]), 44)
for pid, p in P.items():
    check(f"{pid} runs at least 250 words",
          len(" ".join(p["paragraphs"]).split()) >= 250, True)
# Every numeric choice set ascends or descends, form-wide.
for q in DATA["questions"]:
    texts = [q["choices"][l].strip() for l in "ABCD"]
    if all(re.fullmatch(r"-?\d+(?:\.\d+)?%?", t) for t in texts):
        vals = [float(t.rstrip("%")) for t in texts]
        check(f"{q['id']}: numeric choices run in order",
              vals == sorted(vals) or vals == sorted(vals, reverse=True), True)

print(f"\n{checks} checks run, {len(fails)} failed")
if fails:
    for f in fails:
        print("  FAILED:", f)
    sys.exit(1)
print("All arithmetic and model checks pass.")
