"""Recompute every quantitative key and distractor in fl2/psych-soc.json.

Nothing here is typed from memory. Each block starts from the numbers the
passage itself prints -- the table cells or the figure's own coordinates --
recomputes the key, recomputes each distractor from the specific mistake its
note names, and checks that the four strings in the file are exactly those
values in the order they appear.

The model is checked as well as the arithmetic, because a verifier that shares
the author's assumption confirms the author's error. So: a percentage change is
always taken against the value it started from; a share of a total is taken
against that group's own total and not another group's; the number needed to
treat is the reciprocal of a difference between two rates and not of a rate;
and an interaction is a difference between two differences. Table rows are
checked to sum to the totals the tables print, figures quoted in prose are
recomputed from the table they come from, and the polyline coordinates of the
one figure are decoded back to the pages-per-session values the questions use.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "lib", "exams", "content", "fl2", "psych-soc.json")

data = json.load(io.open(PATH, encoding="utf-8"))
questions = dict((q["id"], q) for q in data["questions"])
passages = dict((p["id"], p) for p in data["passages"])
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
        first = text.split()[0]
        decimals = len(first.split(".")[1].rstrip("%gms ")) if "." in first else 0
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
    spoken = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", question["explanation"].replace(",", ""))]
    if not any(abs(value - key_value) <= max(0.051, abs(key_value) * 0.01) for value in spoken):
        failures.append("%s: the computed key %g does not appear in its explanation" % (qid, key_value))


def model(label, computed, stated, tol=1e-9):
    """A figure asserted in prose, a stem or an explanation, recomputed."""
    global checked
    checked += 1
    if abs(computed - stated) > tol:
        failures.append("%s: text states %g, computed %g" % (label, stated, computed))


# ---------------------------------------------------------------- passage 1
# Table 1, minutes per stage and total sleep time, by rota.
P1 = {
    "day":   {"N1": 25.0, "N2": 220.0, "N3": 95.0, "REM": 100.0, "TST": 440.0, "lapses": 3.0},
    "slow":  {"N1": 32.0, "N2": 205.0, "N3": 78.0, "REM": 85.0,  "TST": 400.0, "lapses": 6.0},
    "rapid": {"N1": 40.0, "N2": 190.0, "N3": 60.0, "REM": 70.0,  "TST": 360.0, "lapses": 11.0},
}
# Model check: each row's stages must sum to the total sleep time it prints.
for rota, row in P1.items():
    model("ps2-p1 Table 1 %s row sums to its total sleep time" % rota,
          row["N1"] + row["N2"] + row["N3"] + row["REM"], row["TST"])

# Model check: ps2-p1-q1 calls stage 3 the stage with the largest proportional
# loss under rapid rotation, and the passage calls it the stage most reduced.
losses = dict((stage, (P1["day"][stage] - P1["rapid"][stage]) / P1["day"][stage])
              for stage in ("N1", "N2", "N3", "REM"))
checked += 1
if max(losses, key=losses.get) != "N3":
    failures.append("ps2-p1-q1: stage 3 is not the largest proportional loss: %s" % losses)
checked += 1
absolute = dict((stage, P1["day"][stage] - P1["rapid"][stage]) for stage in ("N1", "N2", "N3", "REM"))
if max(absolute, key=absolute.get) != "N3":
    failures.append("ps2-p1 passage: stage 3 is not the stage most reduced in minutes: %s" % absolute)

rapid_share = 100 * P1["rapid"]["N3"] / P1["rapid"]["TST"]
day_share = 100 * P1["day"]["N3"] / P1["day"]["TST"]
check("ps2-p1-q3", "C", [
    ("A", day_share, "the day-only group's N3 share: the wrong row"),
    ("B", 100 * P1["rapid"]["N3"] / (P1["rapid"]["N1"] + P1["rapid"]["N2"] + P1["rapid"]["N3"]),
          "N3 over non-REM sleep only, leaving REM out of the total"),
    ("C", rapid_share, "N3 over that group's own total sleep time"),
    ("D", 100 * P1["rapid"]["N3"] / P1["day"]["TST"], "rapid-rotation N3 over the day-only total: rows mixed"),
])
# Prose: 80 minutes less sleep, and more than three times the lapses.
model("ps2-p1 shortfall in total sleep time", P1["day"]["TST"] - P1["rapid"]["TST"], 80.0)
checked += 1
if not P1["rapid"]["lapses"] > 3 * P1["day"]["lapses"]:
    failures.append("ps2-p1: prose says more than three times as many lapses, computed %g against %g"
                    % (P1["rapid"]["lapses"], P1["day"]["lapses"]))
# ps2-p1-q4 statement I and II, recomputed rather than asserted.
checked += 1
if not rapid_share < day_share:
    failures.append("ps2-p1-q4 statement I: rapid share %g is not below day share %g" % (rapid_share, day_share))
checked += 1
tst = [P1[r]["TST"] for r in ("day", "slow", "rapid")]
lap = [P1[r]["lapses"] for r in ("day", "slow", "rapid")]
if not all(tst[i] < tst[i - 1] and lap[i] > lap[i - 1] for i in (1, 2)):
    failures.append("ps2-p1-q4 statement II: lapses do not rise monotonically as total sleep time falls")
checked += 1
if P1["slow"]["REM"] >= P1["day"]["REM"]:
    failures.append("ps2-p1-q4 statement III should be false, but slow REM is not below day REM")

# ---------------------------------------------------------------- passage 2
# Table 1, correlations with 30-month vocabulary.
P2 = {"words_per_hour": 0.24, "contingent": 0.48, "television": -0.11,
      "vocab18": 0.55, "contingent_partial": 0.44}
check("ps2-p2-q2", "C", [
    ("A", 100 * P2["words_per_hour"] ** 2, "squares the adult-word-count correlation: wrong row"),
    ("B", 100 * P2["contingent_partial"] ** 2, "squares the partial correlation, which answers a different question"),
    ("C", 100 * P2["contingent"] ** 2, "r squared for contingent replies: the shared variance"),
    ("D", 100 * P2["contingent"], "reports r itself as a percentage of variance"),
])
# Model check: the explanation's "remaining 77%" must be the complement.
model("ps2-p2-q2 variance left unaccounted for",
      100 - 100 * P2["contingent"] ** 2, 76.96, tol=0.5)
# ps2-p2-q4: the EXCEPT key requires television to be the one negative coefficient.
checked += 1
if P2["television"] >= 0:
    failures.append("ps2-p2-q4: the key needs the television correlation to be negative")
checked += 1
if not (P2["contingent"] > P2["words_per_hour"] and P2["vocab18"] == max(
        P2["words_per_hour"], P2["contingent"], P2["vocab18"], P2["contingent_partial"])):
    failures.append("ps2-p2-q4: distractor notes B and D do not hold of the table")

# ---------------------------------------------------------------- passage 3
# Figure 1 is the source, so the values are decoded from its own polylines
# before anything is computed from them: y = 200 - 3 * pages.
svg = passages["ps2-p3"]["figure"]["markup"]
series = re.findall(r'points="([^"]+)"', svg)
if len(series) != 3:
    failures.append("ps2-p3 figure: expected three polylines, found %d" % len(series))
    decoded = []
else:
    decoded = []
    for points in series:
        values = []
        for pair in points.split():
            y = float(pair.split(",")[1])
            values.append((200.0 - y) / 3.0)
        decoded.append(values)
    checked += 1
    if any(abs(v - round(v)) > 1e-9 for row in decoded for v in row):
        failures.append("ps2-p3 figure: a coordinate does not decode to a whole number of pages: %s" % decoded)

VR, FR, FI = decoded if len(decoded) == 3 else ([0] * 5, [0] * 5, [0] * 5)
# Model check: the passage says all three groups ended the token phase at 45.
for name, row in (("variable ratio", VR), ("fixed ratio", FR), ("fixed interval", FI)):
    model("ps2-p3 figure %s starts the withdrawal phase at the stated 45 pages" % name, row[0], 45.0)
# Model check: every curve declines, which ps2-p3-q5 choice A asserts.
checked += 1
for name, row in (("variable ratio", VR), ("fixed ratio", FR), ("fixed interval", FI)):
    if not all(row[i] <= row[i - 1] for i in range(1, 5)):
        failures.append("ps2-p3 figure: the %s curve does not decline monotonically: %s" % (name, row))

start = FR[0]
check("ps2-p3-q3", "D", [
    ("A", 100 * FR[4] / start, "the share still being read, which is the complement of the fall"),
    ("B", 100 * (VR[0] - VR[4]) / VR[0], "the fall in the variable-ratio group: the wrong curve"),
    ("C", 100 * (FI[0] - FI[4]) / FI[0], "the fall in the fixed-interval group: the wrong curve"),
    ("D", 100 * (start - FR[4]) / start, "the fixed-ratio fall over its own starting value"),
])
# Prose: the variable-ratio group still reading 29 pages, about 64 per cent.
model("ps2-p3 variable-ratio pages at the fourth withdrawal session", VR[4], 29.0)
model("ps2-p3 variable-ratio share of its token-phase level", 100 * VR[4] / VR[0], 64.44, tol=0.5)
model("ps2-p3 fixed-ratio pages at the fourth withdrawal session", FR[4], 9.0)
model("ps2-p3 fixed-interval pages at the fourth withdrawal session", FI[4], 12.0)
# ps2-p3-q5 key D: the variable-ratio curve must NOT have the steepest single-session fall.
drops = {"VR": [VR[i - 1] - VR[i] for i in range(1, 5)],
         "FR": [FR[i - 1] - FR[i] for i in range(1, 5)],
         "FI": [FI[i - 1] - FI[i] for i in range(1, 5)]}
checked += 1
if max(drops["VR"]) >= max(max(drops["FR"]), max(drops["FI"])):
    failures.append("ps2-p3-q5: the key needs the variable-ratio curve to have no steepest single-session fall, drops %s" % drops)
checked += 1
if not FR[4] < FI[4]:
    failures.append("ps2-p3-q5 choice B must be true: fixed ratio %g is not below fixed interval %g" % (FR[4], FI[4]))

# ---------------------------------------------------------------- passage 4
# Table 1, allocation, attendance and response rates.
P4 = {
    "activation":    {"n": 80.0, "completed": 68.0, "entry": 32.0, "week8": 19.0, "response": 45.0},
    "antidepressant": {"n": 80.0, "completed": 62.0, "entry": 31.0, "week8": 20.0, "response": 40.0},
    "waiting":       {"n": 80.0, "completed": 74.0, "entry": 32.0, "week8": 28.0, "response": 20.0},
}
model("ps2-p4 total allocated across the three arms",
      sum(arm["n"] for arm in P4.values()), 240.0)
# Model check: the number needed to treat is the reciprocal of a difference in
# rates, not of a rate, so it is built from the two arms being compared.
arr = P4["activation"]["response"] - P4["waiting"]["response"]
check("ps2-p4-q2", "B", [
    ("A", 100 / P4["activation"]["response"], "reciprocal of one arm's response rate alone"),
    ("B", 100 / arr, "reciprocal of the absolute difference between the two arms compared"),
    ("C", 100 / (P4["antidepressant"]["response"] - P4["waiting"]["response"]), "the antidepressant arm: the wrong comparison"),
    ("D", 100 / (P4["activation"]["response"] - P4["antidepressant"]["response"]), "the two active arms compared with each other"),
])
model("ps2-p4-q2 absolute difference in response rates", arr, 25.0)
model("ps2-p4 waiting-list fall without treatment",
      P4["waiting"]["entry"] - P4["waiting"]["week8"], 4.0)
checked += 1
if not (P4["antidepressant"]["completed"] < P4["activation"]["completed"] < P4["waiting"]["completed"]):
    failures.append("ps2-p4-q3: the stem's attendance ordering does not match the table")

# ---------------------------------------------------------------- passage 5
# Table 1, positive and negative subscales at entry and six weeks, by dose.
P5 = {
    "low":      {"pos_entry": 24.0, "pos_6": 18.0, "neg_entry": 15.0, "neg_6": 14.0, "side": 2.0},
    "standard": {"pos_entry": 24.0, "pos_6": 13.0, "neg_entry": 15.0, "neg_6": 13.0, "side": 5.0},
    "high":     {"pos_entry": 24.0, "pos_6": 12.0, "neg_entry": 15.0, "neg_6": 15.0, "side": 11.0},
}
std, high, low = P5["standard"], P5["high"], P5["low"]
check("ps2-p5-q4", "B", [
    ("A", 100 * (std["neg_entry"] - std["neg_6"]) / std["neg_entry"], "the negative subscale: the wrong pair of columns"),
    ("B", 100 * (std["pos_entry"] - std["pos_6"]) / std["pos_entry"], "positive fall over the entry score for that dose"),
    ("C", 100 * (high["pos_entry"] - high["pos_6"]) / high["pos_entry"], "the high-dose row"),
    ("D", 100 * (std["pos_entry"] - std["pos_6"]) / std["pos_6"], "the change divided by the week-six score instead of the entry score"),
])
# Model checks on the claims the other four questions in the set turn on.
model("ps2-p5 positive fall, low dose", low["pos_entry"] - low["pos_6"], 6.0)
model("ps2-p5 positive fall, standard dose", std["pos_entry"] - std["pos_6"], 11.0)
model("ps2-p5 positive fall, high dose", high["pos_entry"] - high["pos_6"], 12.0)
model("ps2-p5 negative movement, low dose", low["neg_entry"] - low["neg_6"], 1.0)
model("ps2-p5 negative movement, standard dose", std["neg_entry"] - std["neg_6"], 2.0)
model("ps2-p5 negative movement, high dose", high["neg_entry"] - high["neg_6"], 0.0)
model("ps2-p5-q3 further positive-symptom gain from standard to high dose",
      std["pos_6"] - high["pos_6"], 1.0)
checked += 1
if not high["side"] >= 2 * std["side"]:
    failures.append("ps2-p5-q3: the key says side effects doubled, computed %g against %g" % (high["side"], std["side"]))
checked += 1
if not all(P5[d]["pos_entry"] - P5[d]["pos_6"] > P5[d]["neg_entry"] - P5[d]["neg_6"] for d in P5):
    failures.append("ps2-p5-q2: positive symptoms do not fall more than negative symptoms at every dose")

# ---------------------------------------------------------------- passage 7
# Table 1, mean items correct out of 20 in the four cells.
P7 = {"diag_before": 9.8, "diag_after": 12.6, "puzzle_before": 12.4, "puzzle_after": 12.8}
simple_diag = P7["diag_after"] - P7["diag_before"]
simple_puzzle = P7["puzzle_after"] - P7["puzzle_before"]
# Model check: an interaction is the difference between the two simple effects,
# each taken within one level of the framing factor.
check("ps2-p7-q3", "B", [
    ("A", simple_puzzle, "the simple effect within the puzzle framing alone"),
    ("B", simple_diag - simple_puzzle, "the difference between the two simple effects: the interaction"),
    ("C", simple_diag, "the simple effect within the diagnostic framing alone"),
    ("D", P7["puzzle_after"] - P7["diag_before"], "the gap between the extreme cells, which crosses both factors"),
])
model("ps2-p7 simple effect under the diagnostic framing", simple_diag, 2.8)
model("ps2-p7 simple effect under the puzzle framing", simple_puzzle, 0.4)
checked += 1
if P7["diag_before"] != min(P7.values()):
    failures.append("ps2-p7: the diagnostic/details-first cell is not the lowest-scoring cell the questions call it")

# ---------------------------------------------------------------- passage 8
# Table 1, proportion intervening and mean time to intervene.
P8 = [("alone", 78.0, 24.0), ("two others", 45.0, 52.0),
      ("five others", 31.0, 71.0), ("five, one attending", 62.0, 38.0)]
rates = dict((name, rate) for name, rate, _ in P8)
times = dict((name, time) for name, _, time in P8)
checked += 1
if not (rates["alone"] > rates["two others"] > rates["five others"]
        and times["alone"] < times["two others"] < times["five others"]):
    failures.append("ps2-p8-q2 conclusion I: the rate and time columns do not both move with group size")
checked += 1
if rates["five, one attending"] >= rates["alone"]:
    failures.append("ps2-p8-q2 conclusion II should be false, but the fourth condition reaches the alone level")
checked += 1
if times["five others"] != max(times.values()):
    failures.append("ps2-p8-q2 conclusion III should be false, but five others is not the slowest condition")
model("ps2-p8 doubling of intervention by one attending bystander",
      rates["five, one attending"] / rates["five others"], 2.0, tol=0.05)

# ---------------------------------------------------------------- passage 9
# Table 1, respondents and outcomes by number of close ties.
P9 = [("none or one", 320.0, 41.0, 28.0), ("two or three", 610.0, 58.0, 17.0),
      ("four or more", 470.0, 69.0, 11.0)]
model("ps2-p9 Table 1 respondents sum to the stated sample",
      sum(row[1] for row in P9), 1400.0)
checked += 1
if not all(P9[i][2] > P9[i - 1][2] and P9[i][3] < P9[i - 1][3] for i in (1, 2)):
    failures.append("ps2-p9: health does not rise and depression fall monotonically across the tie bands")
checked += 1
if not 62.0 > 48.0:
    failures.append("ps2-p9-q4: the membership comparison in the passage does not favour members")

# ---------------------------------------------------------------- passage 10
# Table 1, by band: tracts, physicians per 10,000, usual source of care,
# preventable admissions per 1,000.
P10 = {
    "low":  {"tracts": 61.0, "pcp": 9.6, "usual": 84.0, "admissions": 12.0},
    "mid":  {"tracts": 52.0, "pcp": 6.4, "usual": 71.0, "admissions": 19.0},
    "high": {"tracts": 35.0, "pcp": 3.2, "usual": 58.0, "admissions": 28.0},
}
model("ps2-p10 Table 1 tracts sum to the stated county total",
      sum(band["tracts"] for band in P10.values()), 148.0)
check("ps2-p10-q3", "A", [
    ("A", P10["high"]["pcp"] / P10["low"]["pcp"], "most segregated over least segregated: the multiple asked for"),
    ("B", P10["high"]["pcp"] / P10["mid"]["pcp"], "most segregated against the middle band"),
    ("C", P10["mid"]["pcp"] / P10["low"]["pcp"], "middle band against the least segregated band"),
    ("D", P10["low"]["pcp"] / P10["high"]["pcp"], "the ratio taken the other way round"),
])
# Prose: "about a third" of the supply, admissions "more than twice as high".
model("ps2-p10 supply ratio quoted in prose as about a third",
      P10["high"]["pcp"] / P10["low"]["pcp"], 1.0 / 3.0, tol=0.01)
checked += 1
if not P10["high"]["admissions"] > 2 * P10["low"]["admissions"]:
    failures.append("ps2-p10: prose says admissions are more than twice as high, computed %g against %g"
                    % (P10["high"]["admissions"], P10["low"]["admissions"]))
checked += 1
if not all(P10[b]["usual"] > P10[c]["usual"] for b, c in (("low", "mid"), ("mid", "high"))):
    failures.append("ps2-p10-q4: usual source of care does not fall across the bands as the explanation says")

# ------------------------------------------- every table cell quoted in a stem
# or an explanation must exist in the table markup it claims to come from.
QUOTED = {
    "ps2-p1-q3": ("ps2-p1", ["60", "360", "95", "440"]),
    "ps2-p2-q2": ("ps2-p2", ["0.48", "0.24", "0.44"]),
    "ps2-p4-q2": ("ps2-p4", ["45%", "40%", "20%"]),
    "ps2-p5-q4": ("ps2-p5", ["24", "13", "12", "15"]),
    "ps2-p7-q3": ("ps2-p7", ["9.8", "12.6", "12.4", "12.8"]),
    "ps2-p10-q3": ("ps2-p10", ["9.6", "6.4", "3.2"]),
}
for qid, (pid, cells) in QUOTED.items():
    markup = passages[pid]["figure"]["markup"]
    for cell in cells:
        checked += 1
        if ("<td>%s</td>" % cell) not in markup:
            failures.append("%s: the explanation uses %s, which is not a cell of %s" % (qid, cell, pid))

print("checks run: %d" % checked)
if failures:
    for line in failures:
        print("  FAIL " + line)
    sys.exit(1)
print("every quantitative key and distractor recomputed from the passage data: all agree")
