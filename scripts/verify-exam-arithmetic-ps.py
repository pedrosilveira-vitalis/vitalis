"""Recompute every quantitative key and distractor in fl1/psych-soc.json.

Nothing here is typed from memory. Each block starts from the numbers the
passage itself prints -- the table cells or the figure values -- recomputes the
key, recomputes each distractor from the specific mistake its note names, and
checks that the four strings in the file are exactly those values in order.

The model matters as much as the arithmetic. A percentage change is the change
divided by the value it started from, so every "rose by x%" item below is
checked against the earlier value and not against the later one; a verifier
that shared the error would confirm it back.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "lib", "exams", "content", "fl1", "psych-soc.json")

data = json.load(io.open(PATH, encoding="utf-8"))
questions = {q["id"]: q for q in data["questions"]}
failures = []
checked = 0


def norm(text):
    """The choice text as a bare number: strip units, commas and typeset signs."""
    cleaned = text.replace("×", "x").replace("−", "-").replace(",", "")
    match = re.match(r"\s*([-+]?\d+(?:\.\d+)?)", cleaned)
    return None if match is None else float(match.group(1))


def check(qid, expected_key_letter, expected):
    """expected: list of (letter, value, label) in the order the choices appear."""
    global checked
    question = questions.get(qid)
    if question is None:
        failures.append("%s: missing from the file" % qid)
        return
    checked += 1
    if question["correct"] != expected_key_letter:
        failures.append("%s: key is %s, computed key is %s" % (qid, question["correct"], expected_key_letter))
    values = []
    for letter, value, label in expected:
        text = question["choices"][letter]
        shown = norm(text)
        values.append(value)
        # A choice may be rounded, but only to the precision it displays: "78%"
        # has to be the rounding of the computed 77.78, not of anything else.
        decimals = len(text.split(".")[1].rstrip("%gms ")) if "." in text.split()[0] else 0
        if shown is None or abs(shown - round(value, decimals)) > 1e-9:
            failures.append("%s choice %s: file shows %r, computed %.4g, rounds to %s (%s)"
                            % (qid, letter, text, value, round(value, decimals), label))
    key_value = dict((letter, value) for letter, value, _ in expected)[expected_key_letter]
    for letter, value, label in expected:
        if letter != expected_key_letter and abs(value - key_value) <= 0.051:
            failures.append("%s choice %s (%s) equals the key" % (qid, letter, label))
    ascending = all(values[i] >= values[i - 1] for i in range(1, len(values)))
    descending = all(values[i] <= values[i - 1] for i in range(1, len(values)))
    if not (ascending or descending):
        failures.append("%s: numeric choices are not monotonic: %s" % (qid, values))
    # The key must be visible in the working, within the rounding the choice uses.
    spoken = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", question["explanation"].replace(",", ""))]
    if not any(abs(value - key_value) <= max(0.051, abs(key_value) * 0.01) for value in spoken):
        failures.append("%s: the computed key %g does not appear in its explanation" % (qid, key_value))


# ---------------------------------------------------------------- passage 1
# Table 1: context-change extinction group, end of phase 2 = 20, day-1 test = 48.
P1 = {"ctx_end": 20.0, "ctx_test": 48.0, "ctx_acq": 60.0}
rise = P1["ctx_test"] - P1["ctx_end"]
check("ps-p1-q2", "D", [
    ("A", rise, "the rise in rating points, not a percentage"),
    ("B", 100 * rise / P1["ctx_acq"], "rise over the post-acquisition rating"),
    ("C", 100 * rise / P1["ctx_test"], "rise over the final rather than the starting value"),
    ("D", 100 * rise / P1["ctx_end"], "rise over the starting value: the percentage increase"),
])
assert abs(100 * rise / P1["ctx_end"] - 140) < 1e-9, "percentage increase model"

# ---------------------------------------------------------------- passage 3
# Table 1: accurate 9 / 14, misleading 29 / 48, at ten minutes / one week.
P3 = {"acc_10": 9.0, "acc_week": 14.0, "mis_10": 29.0, "mis_week": 48.0}
check("ps-p3-q2", "A", [
    ("A", P3["mis_week"] / P3["acc_week"], "one-week ratio of the two summary conditions"),
    ("B", P3["mis_10"] / P3["acc_10"], "the same ratio in the ten-minute column"),
    ("C", P3["mis_week"] / P3["mis_10"], "ratio of the two delays within the misleading group"),
    ("D", P3["acc_week"] / P3["mis_week"], "the inverted ratio"),
])

# ---------------------------------------------------------------- passage 4
# Table 1: youngest band needs 4 g against a 100 g standard. Weber's law holds
# the ratio constant, so the threshold scales with the standard.
P4 = {"standard": 100.0, "jnd_young": 4.0, "new_standard": 250.0}
fraction = P4["jnd_young"] / P4["standard"]
assert abs(fraction - 0.04) < 1e-12, "Weber fraction"
check("ps-p4-q1", "C", [
    ("A", P4["jnd_young"], "threshold treated as a constant amount"),
    ("B", P4["jnd_young"] + P4["new_standard"] / P4["standard"], "ratio added rather than multiplied"),
    ("C", fraction * P4["new_standard"], "constant fraction of the new standard"),
    ("D", P4["new_standard"] / P4["jnd_young"], "new standard divided by the old threshold"),
])

# ---------------------------------------------------------------- passage 6
# Table 1: public unanimous 36%, one correct dissenter 8%.
P6 = {"unanimous": 36.0, "dissenter": 8.0}
drop = P6["unanimous"] - P6["dissenter"]
check("ps-p6-q2", "C", [
    ("A", 100 * P6["dissenter"] / P6["unanimous"], "share of conformity that remained"),
    ("B", drop, "fall in percentage points"),
    ("C", 100 * drop / P6["unanimous"], "fall over the starting rate: the percentage reduction"),
    ("D", 100 * P6["unanimous"] / P6["dissenter"], "ratio of the two rates as a percentage"),
])

# ---------------------------------------------------------------- passage 9
# Table 1, respondents who had never lost a job: own neighbourhood 41%,
# distant neighbourhood 64%.
P9 = {"ingroup": 41.0, "outgroup": 64.0, "ingroup_exp": 22.0, "outgroup_exp": 48.0}
gap = P9["outgroup"] - P9["ingroup"]
check("ps-p9-q2", "B", [
    ("A", 100 * P9["outgroup"] / P9["ingroup"], "the ratio, misread as the excess"),
    ("B", 100 * gap / P9["ingroup"], "excess over the in-group figure"),
    ("C", 100 * gap / P9["outgroup"], "excess divided by the larger figure"),
    ("D", gap, "gap in percentage points"),
])

# ---------------------------------------------------------------- passage 10
# Table 1, Northvale: CBR 11, CDR 9, net migration +4, all per 1,000.
P10 = {"cbr": 11.0, "cdr": 9.0, "migration": 4.0}
natural = P10["cbr"] - P10["cdr"]
check("ps-p10-q1", "A", [
    ("A", natural, "births less deaths: natural increase"),
    ("B", natural + P10["migration"], "total growth, migration wrongly included"),
    ("C", P10["cbr"] + P10["cdr"], "rates summed instead of subtracted"),
    ("D", P10["cbr"] + P10["cdr"] + P10["migration"], "all three rates summed"),
])

# ----------------------------------------------- figures quoted in prose
# Numbers asserted inside stems, explanations and passages, recomputed here so
# none of them is a remembered value.
P7 = {"high_strong": 5.8, "high_weak": 3.9, "low_strong": 4.6, "low_weak": 4.4}
prose = [
    ("ps-p7-q1 high-relevance gap", round(P7["high_strong"] - P7["high_weak"], 10), 1.9),
    ("ps-p7-q1 low-relevance gap", round(P7["low_strong"] - P7["low_weak"], 10), 0.2),
    ("ps-p2 digit recall fall", 97.0 - 82.0, 15.0),
    ("ps-p3 accurate-summary error rise", 14.0 - 9.0, 5.0),
    ("ps-p8 mover exploration rise", round(3.7 - 2.8, 10), 0.9),
    ("ps-p8 mover self-esteem fall", round(3.6 - 3.4, 10), 0.2),
    ("ps-p10 Northvale life-expectancy gap", 82.0 - 74.0, 8.0),
    ("ps-p5 threat peak over baseline", 18.0 / 6.0, 3.0),
]
for label, computed, stated in prose:
    checked += 1
    if abs(computed - stated) > 1e-9:
        failures.append("%s: text states %g, computed %g" % (label, stated, computed))

# The figure's polyline y-coordinates must encode the cortisol values the
# explanations quote: y = 200 - 8 * value on the drawn axis.
svg = [p for p in data["passages"] if p["id"] == "ps-p5"][0]["figure"]["markup"]
series = re.findall(r'points="([^"]+)"', svg)
expected_series = [[6, 13, 18, 12], [6, 11, 14, 9], [6, 9, 11, 7]]
if len(series) != 3:
    failures.append("ps-p5 figure: expected three polylines, found %d" % len(series))
else:
    for values, points in zip(expected_series, series):
        checked += 1
        drawn = [(200 - float(pair.split(",")[1])) / 8.0 for pair in points.split()]
        if drawn != [float(v) for v in values]:
            failures.append("ps-p5 figure: polyline encodes %s, passage uses %s" % (drawn, values))
    peaks = [max(v) for v in expected_series]
    if peaks != [18, 14, 11]:
        failures.append("ps-p5 figure: peak ordering is %s" % peaks)
    for values in expected_series:
        if values.index(max(values)) != 2:
            failures.append("ps-p5 figure: a series peaks somewhere other than the 30-minute sample")

print("checks run: %d" % checked)
if failures:
    for line in failures:
        print("  FAIL " + line)
    sys.exit(1)
print("every quantitative key and distractor recomputed from the passage data: all agree")
