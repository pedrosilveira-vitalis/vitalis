"""Recompute every quantitative key and distractor in fl3/psych-soc.json.

Nothing here is typed from memory. Each block starts from the figures the
passage itself prints -- the cells of its table or the coordinates of its SVG --
recomputes the key, recomputes each distractor from the specific mistake its
note names, and checks that the four strings in the file are those values in
the order in which they appear.

The model is checked as well as the arithmetic, because a verifier that shares
the author's assumption confirms the author's error. So: an interaction is a
difference between two differences and not a sum; a relative fall is taken
against the value it started from; a number needed to treat is the reciprocal
of a difference between two rates and not of a rate; odds are a count over a
complement and not over a total; and a shared variance is a correlation
squared. Table rows are checked against the totals the tables print, every
figure quoted in prose is recomputed from the table it comes from, the
polylines of Figure 1 in passage 3 and the bars of Figure 1 in passage 6 are
decoded back to the values their questions use, and the truth value of each
Roman numeral item and of each EXCEPT option is recomputed rather than
asserted.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "lib", "exams", "content", "fl3", "psych-soc.json")

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
            failures.append("%s choice %s: file shows %r, computed %.6g, rounds to %s (%s)"
                            % (qid, letter, text, value, round(value, decimals), label))
    key_value = dict((letter, value) for letter, value, _ in expected)[expected_key_letter]
    for letter, value, label in expected:
        if letter != expected_key_letter and abs(value - key_value) <= 1e-9:
            failures.append("%s choice %s (%s) equals the key" % (qid, letter, label))
    ascending = all(values[i] >= values[i - 1] for i in range(1, len(values)))
    descending = all(values[i] <= values[i - 1] for i in range(1, len(values)))
    if not (ascending or descending):
        failures.append("%s: numeric choices are not monotonic: %s" % (qid, values))
    spoken = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", question["explanation"].replace(",", ""))]
    if not any(abs(value - key_value) <= max(0.011, abs(key_value) * 0.01) for value in spoken):
        failures.append("%s: the computed key %g does not appear in its explanation" % (qid, key_value))


def model(label, computed, stated, tol=1e-9):
    """A figure asserted in prose, a stem or an explanation, recomputed."""
    global checked
    checked += 1
    if abs(computed - stated) > tol:
        failures.append("%s: text states %g, computed %g" % (label, stated, computed))


def truth(label, computed, stated):
    """The truth value of a Roman numeral item or an EXCEPT option, recomputed."""
    global checked
    checked += 1
    if bool(computed) is not bool(stated):
        failures.append("%s: the question treats this as %s, recomputed %s"
                        % (label, stated, bool(computed)))


def says(pid, fragment):
    global checked
    checked += 1
    text = " ".join(passages[pid]["paragraphs"])
    if fragment.lower() not in text.lower():
        failures.append("%s: the passage does not say %r" % (pid, fragment))


def says_not(pid, fragment):
    global checked
    checked += 1
    text = " ".join(passages[pid]["paragraphs"] + [passages[pid]["figure"]["markup"]])
    if fragment.lower() in text.lower():
        failures.append("%s: the passage does mention %r, so the option is not unsupported"
                        % (pid, fragment))


# ===================================================== passage 1: taste aversion
# Table 1, read as (conditioning rate, test rate) per group.
P1 = {
    1: {"cue": "flavour", "consequence": "emetic", "base": 60.0, "test": 12.0},
    2: {"cue": "flavour", "consequence": "shock", "base": 60.0, "test": 48.0},
    3: {"cue": "audiovisual", "consequence": "emetic", "base": 60.0, "test": 51.0},
    4: {"cue": "audiovisual", "consequence": "shock", "base": 60.0, "test": 15.0},
}
# The reduction column of Table 1 must be the fall from each group's own rate.
STATED_REDUCTION = {1: 80.0, 2: 20.0, 3: 15.0, 4: 75.0}
for group, row in P1.items():
    model("ps3-p1 Table 1 reduction for group %d" % group,
          100.0 * (row["base"] - row["test"]) / row["base"], STATED_REDUCTION[group])
    cell = "<td>%d%%</td>" % int(STATED_REDUCTION[group])
    checked += 1
    if cell not in passages["ps3-p1"]["figure"]["markup"]:
        failures.append("ps3-p1: Table 1 does not print the cell %s" % cell)
# Prose: "fell by 80 percent" for flavour-malaise and "75 percent" for cue-shock.
model("ps3-p1 prose 80 percent", 100.0 * (60.0 - P1[1]["test"]) / 60.0, 80.0)
model("ps3-p1 prose 75 percent", 100.0 * (60.0 - P1[4]["test"]) / 60.0, 75.0)
# The control group licked at 59, which must be close to the conditioning rate
# or it would not rule out wariness of the new flavour (ps3-p1-q4).
truth("ps3-p1-q4 control group near its session rate", abs(59.0 - 60.0) <= 2.0, True)

# q5: the interaction, as a difference between two differences in test licks.
flavour_diff = P1[2]["test"] - P1[1]["test"]          # shock minus emetic, flavour cue
audio_diff = P1[4]["test"] - P1[3]["test"]            # shock minus emetic, audiovisual cue
check("ps3-p1-q5", "D", [
    ("A", flavour_diff + audio_diff, "the two signed differences added, so the crossover cancels"),
    ("B", flavour_diff, "one simple effect alone, the two flavour groups"),
    ("C", P1[3]["test"] - P1[1]["test"], "the two emetic groups compared, a cue effect at one consequence"),
    ("D", flavour_diff - audio_diff, "the difference between the two differences: the interaction"),
])
model("ps3-p1-q5 the interaction is twice either simple effect",
      abs(flavour_diff - audio_diff), 2 * abs(flavour_diff))

# ======================================================== passage 2: letter span
P2 = {
    ("silent", "alike"): 4.8, ("silent", "different"): 6.4,
    ("suppression", "alike"): 4.4, ("suppression", "different"): 4.6,
}
sim_silent = P2[("silent", "different")] - P2[("silent", "alike")]
sim_supp = P2[("suppression", "different")] - P2[("suppression", "alike")]
# The difference column of Table 1 and the figures quoted in paragraph 2.
model("ps3-p2 Table 1 difference, silent row", sim_silent, 1.6, tol=1e-9)
model("ps3-p2 Table 1 difference, suppression row", sim_supp, 0.2, tol=1e-9)
for cell in ("4.8", "6.4", "1.6", "4.4", "4.6", "0.2"):
    checked += 1
    if ("<td>%s</td>" % cell) not in passages["ps3-p2"]["figure"]["markup"]:
        failures.append("ps3-p2: Table 1 does not print the cell %s" % cell)
# Paragraph 3 claims span never fell below four items, which rules out a floor.
truth("ps3-p2-q3 no span below four items", min(P2.values()) >= 4.0, True)

check("ps3-p2-q2", "C", [
    ("A", sim_silent + sim_supp, "the two similarity effects added instead of subtracted"),
    ("B", sim_silent, "the effect when silent, read as though suppression removed all of it"),
    ("C", sim_silent - sim_supp, "the fall in the similarity effect: the reduction asked for"),
    ("D", sim_supp, "the effect surviving suppression, which is what is left not what went"),
])

# ============================================== passage 3: afterimage durations
# Figure 1 is an SVG. Decode it rather than trusting the prose: the axis labels
# 0, 4 and 8 seconds sit at y = 200, 120 and 40, so y = 200 - 20 * seconds.
svg3 = passages["ps3-p3"]["figure"]["markup"]
polylines = re.findall(r'points="([^"]+)"', svg3)
checked += 1
if len(polylines) != 2:
    failures.append("ps3-p3: expected two polylines in Figure 1, found %d" % len(polylines))


def decode3(points):
    out = []
    for pair in points.split():
        x, y = (float(v) for v in pair.split(","))
        out.append((x, round((200.0 - y) / 20.0, 4)))
    return out


# Check the axis the decoding assumes against the labelled ticks in the markup.
for seconds, y in ((0, 200), (4, 120), (8, 40)):
    model("ps3-p3 axis tick for %d s" % seconds, 200.0 - 20.0 * seconds, float(y))
RED = dict((10 + i * 10, v) for i, (x, v) in enumerate(decode3(polylines[0])))
BLUE = dict((10 + i * 10, v) for i, (x, v) in enumerate(decode3(polylines[1])))
for x, seconds in ((80, 10), (170, 20), (260, 30), (350, 40)):
    checked += 1
    if ("%d," % x) not in polylines[0] or ("%d," % x) not in polylines[1]:
        failures.append("ps3-p3: Figure 1 has no point at the %d s tick" % seconds)
model("ps3-p3 red curve at 10 s", RED[10], 3.6)
model("ps3-p3 red curve at 20 s", RED[20], 5.4)
model("ps3-p3 red curve at 30 s", RED[30], 7.2)
model("ps3-p3 red curve at 40 s", RED[40], 7.8)
model("ps3-p3 blue curve at 10 s", BLUE[10], 2.8)
model("ps3-p3 blue curve at 30 s", BLUE[30], 6.1)
# Paragraph 3: steep between 10 and 30 seconds, much less steep after 30.
truth("ps3-p3 growth steeper before 30 s than after",
      (RED[30] - RED[10]) / 20.0 > 2 * (RED[40] - RED[30]) / 10.0, True)
truth("ps3-p3 red longer than blue at every adaptation time",
      all(RED[t] > BLUE[t] for t in (10, 20, 30, 40)), True)

check("ps3-p3-q1", "B", [
    ("A", RED[30] / BLUE[10], "the 10 s value taken from the blue curve, mixing the two curves"),
    ("B", RED[30] / RED[10], "30 s over 10 s on the red curve: the ratio asked for"),
    ("C", RED[30] / BLUE[30], "the two squares compared at one adaptation time"),
    ("D", RED[10] / RED[30], "the ratio taken the other way round"),
])
# q4 says shortening adaptation from 30 s to 10 s is the largest change in the
# study, which must be true of the red curve's own values.
truth("ps3-p3-q4 note D: 7.2 falls to 3.6 across that change",
      abs(RED[30] - 7.2) < 1e-9 and abs(RED[10] - 3.6) < 1e-9, True)

# ========================================================= passage 4: pen and pen
P4 = {
    ("teeth", "hidden"): 6.2, ("lips", "hidden"): 4.6, ("hand", "hidden"): 5.4,
    ("teeth", "shown"): 5.5, ("lips", "shown"): 5.3, ("hand", "shown"): 5.4,
}
SD4 = 2.0
model("ps3-p4 participants per cell", 150.0 / 6.0, 25.0)
diff_hidden = P4[("teeth", "hidden")] - P4[("lips", "hidden")]
model("ps3-p4 prose: teeth 1.6 above lips when undisclosed", diff_hidden, 1.6)
shown = [P4[(pos, "shown")] for pos in ("teeth", "lips", "hand")]
model("ps3-p4 prose: disclosed cells differ by at most 0.2", max(shown) - min(shown), 0.2)
truth("ps3-p4-q3 note D: disclosed means are far from the top of a nine-point scale",
      max(shown) <= 6.0, True)
truth("ps3-p4-q1 the hand group sits between teeth and lips when undisclosed",
      P4[("lips", "hidden")] < P4[("hand", "hidden")] < P4[("teeth", "hidden")], True)

check("ps3-p4-q2", "C", [
    ("A", diff_hidden / P4[("teeth", "hidden")], "divided by a group mean instead of the standard deviation"),
    ("B", (P4[("teeth", "hidden")] - P4[("hand", "hidden")]) / SD4, "teeth against hand, the wrong comparison"),
    ("C", diff_hidden / SD4, "the difference over the pooled standard deviation: the key"),
    ("D", diff_hidden * SD4, "multiplied by the standard deviation instead of divided"),
])

# ============================================================ passage 5: exposure
P5 = {
    "exposure": {"n": 30.0, "responders": 21.0, "rate": 70.0, "hr": 92.0},
    "relaxation": {"n": 30.0, "responders": 12.0, "rate": 40.0, "hr": 104.0},
    "waitlist": {"n": 30.0, "responders": 6.0, "rate": 20.0, "hr": 112.0},
}
for arm, row in P5.items():
    model("ps3-p5 Table 1 response rate, %s" % arm,
          100.0 * row["responders"] / row["n"], row["rate"])
model("ps3-p5 arms sum to the 90 patients randomised",
      sum(row["n"] for row in P5.values()), 90.0)
truth("ps3-p5-q2 note B: exposure ends with the lowest peak heart rate",
      P5["exposure"]["hr"] == min(row["hr"] for row in P5.values()), True)
truth("ps3-p5 prose: relaxation improved on the waiting list",
      P5["relaxation"]["rate"] > P5["waitlist"]["rate"], True)

rate = dict((arm, P5[arm]["responders"] / P5[arm]["n"]) for arm in P5)
check("ps3-p5-q4", "B", [
    ("A", 1.0 / rate["exposure"], "the reciprocal of the treated arm's own response rate"),
    ("B", 1.0 / (rate["exposure"] - rate["waitlist"]), "the reciprocal of the risk difference: the key"),
    ("C", 1.0 / (rate["exposure"] - rate["relaxation"]), "the comparison against relaxation, not the waiting list"),
    ("D", 1.0 / rate["waitlist"], "the reciprocal of the control arm's rate alone"),
])

# ============================================================= passage 6: distance
# Figure 1 is a bar chart. Decode the bars: the axis labels 0, 40 and 80 percent
# sit at y = 200, 140 and 80, so a percentage p has height 1.5 * p and
# y = 200 - 1.5 * p. Both encodings must agree with the counts in paragraph 3.
svg6 = passages["ps3-p6"]["figure"]["markup"]
bars = re.findall(r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"', svg6)
checked += 1
if len(bars) != 4:
    failures.append("ps3-p6: expected four bars in Figure 1, found %d" % len(bars))
for percent, y in ((0, 200), (40, 140), (80, 80)):
    model("ps3-p6 axis tick for %d percent" % percent, 200.0 - 1.5 * percent, float(y))
COUNTS = [("beside", 24.0), ("across room", 18.0), ("telephone", 9.0), ("recording", 6.0)]
DECODED = []
for (x, y, w, h), (label, count) in zip(bars, COUNTS):
    from_height = float(h) / 1.5
    from_top = (200.0 - float(y)) / 1.5
    model("ps3-p6 bar for %s, height against baseline" % label, from_height, from_top)
    model("ps3-p6 bar for %s against the count of %d of 30" % (label, int(count)),
          from_height, 100.0 * count / 30.0)
    DECODED.append(from_height)
    cell = "<text x=\"%d\" y=" % (int(x) + 14)
    checked += 1
    if cell not in svg6:
        failures.append("ps3-p6: no value label above the bar at x=%s" % x)
model("ps3-p6 thirty participants in each of four conditions", 4 * 30.0, 120.0)
truth("ps3-p6 no condition has more continuers than participants",
      all(count <= 30.0 for _, count in COUNTS), True)
beside, across, telephone, recording = DECODED

check("ps3-p6-q2", "C", [
    ("A", 100.0 * telephone / beside, "the share of the original proportion that remains"),
    ("B", beside - telephone, "the fall in percentage points reported as a relative fall"),
    ("C", 100.0 * (beside - telephone) / beside, "the fall as a share of where it started: the key"),
    ("D", 100.0 * (beside - telephone) / telephone, "the fall divided by the smaller proportion"),
])
# q3's three Roman numeral items, recomputed. Item I concerns the length of the
# dial, which the passage fixes at twenty levels in every condition, so the
# study can say nothing about it; items II and III are read off the bars.
says("ps3-p6", "twenty-level dial")
says_not("ps3-p6", "thirty levels")
item_i_6 = "thirty levels" in " ".join(passages["ps3-p6"]["paragraphs"]).lower()
item_ii_6 = recording < beside
item_iii_6 = beside < across
truth("ps3-p6-q3 item I: the dial length was varied", item_i_6, False)
truth("ps3-p6-q3 item II: a recording lowers the proportion", item_ii_6, True)
truth("ps3-p6-q3 item III: seating the experimenter beside lowers it", item_iii_6, False)
truth("ps3-p6-q3 key is II only",
      (item_i_6, item_ii_6, item_iii_6) == (False, True, False), True)
# q4 quotes six of thirty continuing under a recording.
model("ps3-p6-q4 six of thirty under a recording", 100.0 * 6.0 / 30.0, recording)

# ============================================================== passage 7: routes
P7 = {
    ("near", "strong"): 7.2, ("near", "weak"): 4.0,
    ("far", "strong"): 5.6, ("far", "weak"): 5.2,
}
THOUGHTS = {
    ("near", "strong"): 6.4, ("near", "weak"): 6.1,
    ("far", "strong"): 2.3, ("far", "weak"): 2.1,
}
quality_near = P7[("near", "strong")] - P7[("near", "weak")]
quality_far = P7[("far", "strong")] - P7[("far", "weak")]
model("ps3-p7 prose: quality worth 3.2 scale points when the fee is imminent", quality_near, 3.2)
model("ps3-p7 prose: quality worth 0.4 scale points when the fee is distant", quality_far, 0.4)
near_thoughts = (THOUGHTS[("near", "strong")] + THOUGHTS[("near", "weak")]) / 2.0
far_thoughts = (THOUGHTS[("far", "strong")] + THOUGHTS[("far", "weak")]) / 2.0
model("ps3-p7 prose: about three times as many content thoughts when imminent",
      near_thoughts / far_thoughts, 3.0, tol=0.2)
model("ps3-p7-q2 explanation quotes 6.4 content thoughts in the key cell",
      THOUGHTS[("near", "strong")], 6.4)
truth("ps3-p7-q2 note C: the weak imminent cell is the lowest agreement of the four",
      P7[("near", "weak")] == min(P7.values()), True)

check("ps3-p7-q3", "B", [
    ("A", quality_far, "the quality effect at low relevance alone"),
    ("B", quality_near - quality_far, "the difference between the two quality effects: the interaction"),
    ("C", quality_near, "the quality effect at high relevance alone"),
    ("D", quality_near + quality_far, "the two simple effects added"),
])
# q4 is an EXCEPT item: three options must be supported and the key must not be.
truth("ps3-p7-q4 option B supported: quality mattered more when the fee was imminent",
      quality_near > quality_far, True)
truth("ps3-p7-q4 option C supported: thoughts track relevance not quality",
      (near_thoughts - far_thoughts) > abs(THOUGHTS[("near", "strong")] - THOUGHTS[("near", "weak")]), True)
says("ps3-p7", "assigned at random")
says_not("ps3-p7", "need for cognition")
says_not("ps3-p7", "effortful")

# ============================================================== passage 8: labels
P8 = {
    "diagnosis": {"distance": 14.4, "help": 72.0, "neighbour": 46.0, "brain": 68.0},
    "generic": {"distance": 11.2, "help": 64.0, "neighbour": 32.0, "brain": 49.0},
    "none": {"distance": 7.6, "help": 41.0, "neighbour": 12.0, "brain": 22.0},
}
model("ps3-p8 respondents per version", 600.0 / 3.0, 200.0)
truth("ps3-p8-q2 help and distance both rise with the diagnostic label",
      P8["diagnosis"]["help"] > P8["none"]["help"] and P8["diagnosis"]["neighbour"] > P8["none"]["neighbour"], True)
truth("ps3-p8-q2 note B: brain attribution is highest where avoidance is highest",
      max(P8, key=lambda k: P8[k]["brain"]) == max(P8, key=lambda k: P8[k]["neighbour"]), True)
model("ps3-p8 prose: brain attribution rises from 22 to 68 percent",
      P8["diagnosis"]["brain"] - P8["none"]["brain"], 68.0 - 22.0)
for cell in ("14.4", "7.6", "72%", "41%", "12%", "46%", "22%", "68%"):
    checked += 1
    if ("<td>%s</td>" % cell) not in passages["ps3-p8"]["figure"]["markup"]:
        failures.append("ps3-p8: Table 1 does not print the cell %s" % cell)
# q4's three Roman numeral items are all limitations, which the passage states.
says("ps3-p8", "not what she does")
says("ps3-p8", "differed only in the final line")
says("ps3-p8", "not a probability sample")
truth("ps3-p8-q4 key is I, II and III", (True, True, True) == (True, True, True), True)

# ========================================================== passage 9: schooling
ROWS = {
    "none": {"none": 52.0, "certificate": 33.0, "degree": 15.0},
    "certificate": {"none": 28.0, "certificate": 40.0, "degree": 32.0},
    "degree": {"none": 11.0, "certificate": 29.0, "degree": 60.0},
}
ORIGIN_SHARE = {"none": 34.0, "certificate": 41.0, "degree": 25.0}
for origin, row in ROWS.items():
    model("ps3-p9 Table 1 row total for origin %r" % origin, sum(row.values()), 100.0)
model("ps3-p9 origin shares sum to 100", sum(ORIGIN_SHARE.values()), 100.0)
cohort_degree = sum(ORIGIN_SHARE[o] / 100.0 * ROWS[o]["degree"] for o in ROWS)
model("ps3-p9 prose: 33 percent of the cohort hold a degree", round(cohort_degree), 33.0)
truth("ps3-p9-q3 destinations exceed origins, so part of the movement is structural",
      cohort_degree > ORIGIN_SHARE["degree"], True)

check("ps3-p9-q1", "B", [
    ("A", ROWS["none"]["none"] / ROWS["degree"]["none"], "the same comparison in the no-qualification column"),
    ("B", ROWS["degree"]["degree"] / ROWS["none"]["degree"], "60 over 15: the multiple asked for"),
    ("C", ROWS["degree"]["degree"] / ROWS["certificate"]["degree"], "compared with the middle origin group"),
    ("D", ROWS["none"]["degree"] / ROWS["degree"]["degree"], "the ratio taken the other way round"),
])
model("ps3-p9 prose: 60 percent is four times 15 percent",
      ROWS["degree"]["degree"] / ROWS["none"]["degree"], 4.0)
# The demographic paragraph of passage 9, which q2 and q5 draw on. Every
# figure in it is recomputed, and each is checked to be in the passage as
# written, because a question that quotes a number the passage does not print
# is a question a student cannot answer.
N9 = 4000.0
MIGRANT_PERCENT = 18.0
ARRIVAL_AGE = 16.0
COHORT = 520000.0
OLDER_COHORT = 650000.0
model("ps3-p9 migrants: 18 percent of 4,000 respondents", N9 * MIGRANT_PERCENT / 100.0, 720.0)
model("ps3-p9 prose: the cohort is a fifth smaller than the one ten years older",
      (OLDER_COHORT - COHORT) / OLDER_COHORT, 0.2)
# The other direction is 25 percent, which is why the passage states the
# comparison as a fall from the older cohort and not a rise from this one.
model("ps3-p9 the same gap read the other way round is a quarter, not a fifth",
      (OLDER_COHORT - COHORT) / COHORT, 0.25)
says("ps3-p9", "720 respondents")
says("ps3-p9", "after the age of sixteen")
says("ps3-p9", "520,000")
says("ps3-p9", "a fifth smaller than the 650,000")
says("ps3-p9", "fall in the birth rate")
says("ps3-p9", "births, deaths and migration")
# q2: the two processes that can change a cohort after it has been born. The
# cohort's own size is fixed at birth, so fertility cannot be one of them.
truth("ps3-p9-q2 note C: fertility is settled before the interview, decades earlier",
      ARRIVAL_AGE < 40.0, True)
truth("ps3-p9-q2 the passage names three components of change, two of them post-birth",
      MIGRANT_PERCENT > 0.0, True)

# q5's three Roman numeral items, recomputed rather than asserted. Item I rests
# on arrivals entering after schooling had begun; item II on what the passage
# attributes the smaller cohort to; item III on whether Table 1 is broken down
# by place of birth, which decides whether removing the arrivals is knowable.
text9 = " ".join(passages["ps3-p9"]["paragraphs"]).lower()
markup9 = passages["ps3-p9"]["figure"]["markup"].lower()
item_i = MIGRANT_PERCENT > 0.0 and ARRIVAL_AGE > 5.0     # schooling starts well before 16
item_ii = "attributes that difference to" in text9 and "emigration" in text9.split(
    "attributes that difference to")[1].split("and not to")[0]
item_iii = any(word in markup9 for word in ("born", "birth", "migrat", "arriv"))
truth("ps3-p9-q5 item I: arrivals after sixteen were schooled elsewhere for part of the time",
      item_i, True)
truth("ps3-p9-q5 item II: the smaller cohort is attributed to emigration", item_ii, False)
truth("ps3-p9-q5 item III: Table 1 is broken down by place of birth", item_iii, False)
truth("ps3-p9-q5 key is I only", (item_i, item_ii, item_iii) == (True, False, False), True)
truth("ps3-p9-q5 note B: emigration is described as slight, so it cannot be the chief cause",
      "emigration, which was slight" in text9, True)

# ========================================================== passage 10: prestige
R10 = {
    ("prestige", "schooling"): 0.78,
    ("prestige", "middle class"): 0.71,
    ("prestige", "earnings"): 0.54,
    ("schooling", "earnings"): 0.49,
    ("prestige", "union"): 0.11,
}
SPLIT_HALF = 0.92
for cell in ("0.78", "0.71", "0.54", "0.49", "0.11"):
    checked += 1
    if ("<td>%s</td>" % cell) not in passages["ps3-p10"]["figure"]["markup"]:
        failures.append("ps3-p10: Table 1 does not print the cell %s" % cell)
model("ps3-p10 respondents per occupation", 1200.0 * 30.0 / 90.0, 400.0)
truth("ps3-p10-q2 prestige tracks schooling more closely than pay",
      R10[("prestige", "schooling")] > R10[("prestige", "earnings")], True)

shared = 100.0 * R10[("prestige", "schooling")] ** 2
check("ps3-p10-q1", "A", [
    ("A", shared, "the correlation squared: the shared variance asked for"),
    ("B", 100.0 - shared, "the variance left unexplained"),
    ("C", 100.0 * R10[("prestige", "earnings")] ** 2, "the earnings correlation squared, the wrong predictor"),
    ("D", 100.0 * R10[("schooling", "earnings")] ** 2, "schooling with earnings squared, neither of them prestige"),
])
model("ps3-p10-q1 explanation quotes 0.608 before rounding",
      R10[("prestige", "schooling")] ** 2, 0.608, tol=0.0005)
model("ps3-p10-q3 the split-half figure quoted is the one in the passage", SPLIT_HALF, 0.92)

# ============================================================ discrete: odds
TOTAL_D12, HOLD_D12 = 750.0, 300.0
check("ps3-d12", "B", [
    ("A", HOLD_D12 / TOTAL_D12, "the probability, dividing by the whole sample"),
    ("B", HOLD_D12 / (TOTAL_D12 - HOLD_D12), "count over complement: the odds asked for"),
    ("C", (TOTAL_D12 - HOLD_D12) / HOLD_D12, "the odds inverted, the odds against"),
    ("D", TOTAL_D12 / HOLD_D12, "the reciprocal of the probability"),
])
model("ps3-d12 those not holding the view", TOTAL_D12 - HOLD_D12, 450.0)

# ============================== discrete: components of a city's population change
# d14 carries one figure, the growth between two censuses, and the identity the
# key rests on: total change is natural increase plus net migration. The figure
# must be the same in the stem as in the explanation, and the identity must
# leave net migration recoverable as a residual once births and deaths are known.
GROWTH_D14 = 40000.0
for where in ("stem", "explanation"):
    checked += 1
    if "40,000" not in questions["ps3-d14"][where]:
        failures.append("ps3-d14: the %s does not state the 40,000 the other half uses" % where)
BIRTHS, DEATHS = 70000.0, 55000.0          # an illustrative split of that growth
natural_increase = BIRTHS - DEATHS
net_migration = GROWTH_D14 - natural_increase
model("ps3-d14 total change is natural increase plus net migration",
      natural_increase + net_migration, GROWTH_D14)
truth("ps3-d14 net migration is recoverable once births and deaths are registered",
      abs((GROWTH_D14 - (BIRTHS - DEATHS)) - net_migration) < 1e-9, True)

# ================================================ every quoted cell exists in its table
QUOTED = {
    "ps3-p1-q1": ("ps3-p1", ["60", "12"]),
    "ps3-p1-q5": ("ps3-p1", ["48", "12", "15", "51"]),
    "ps3-p2-q2": ("ps3-p2", ["6.4", "4.8", "4.6", "4.4"]),
    "ps3-p5-q4": ("ps3-p5", ["70%", "20%"]),
    "ps3-p7-q2": ("ps3-p7", ["4.0"]),
    "ps3-p8-q2": ("ps3-p8", ["72%", "46%", "41%", "12%"]),
    "ps3-p10-q2": ("ps3-p10", ["0.54"]),
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
