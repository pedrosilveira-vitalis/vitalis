"""Spread the answer key across all four letters.

Two mechanisms, because the two kinds of question have different constraints.

Numeric choices are conventionally listed in order, so the key's position is
decided by the distractors around it. For those the fix is to rewrite the
distractor set with a plausible smaller value, which moves the key and gives
the question a better distractor than it had. Each new distractor below is a
real mistake a student makes, not filler.

Prose choices have no natural order, so those are simply rotated.
"""
import json, sys

path = sys.argv[1]
data = json.load(open(path))
by_id = {q["id"]: q for q in data["questions"]}

# --- 1. Numeric sets rewritten so the key is not always second -------------
REWRITES = {
    "cp-p1-q2": {
        "choices": {"A": "7.12", "B": "7.22", "C": "7.32", "D": "7.42"},
        "correct": "C",
        "wrong": {
            "A": "7.12 uses the normal PCO2 of 40 mmHg rather than this patient's 24 mmHg, which gives a ratio of 10 instead of 16.7.",
            "B": "7.22 would need a ratio of about 13, which means dividing 12 by 0.9 rather than by 0.72.",
            "D": "7.42 is above normal, but this patient has lost proportionally more bicarbonate than CO2, so the ratio and the pH must both fall.",
        },
    },
    "cp-p3-q2": {
        "choices": {"A": "0.12 m/s", "B": "0.30 m/s", "C": "0.75 m/s", "D": "1.9 m/s"},
        "correct": "C",
        "wrong": {
            "A": "0.12 m/s multiplies by 0.40 instead of dividing by it, which would have fluid slowing as the vessel narrows - impossible if the same volume passes each second.",
            "B": "0.30 m/s is the velocity in the healthy segment, unchanged. Continuity requires that it rise where the area falls.",
            "D": "1.9 m/s squares the area ratio. Squaring converts a radius ratio into an area ratio, but the passage has already given the area.",
        },
    },
    "cp-p5-q2": {
        "choices": {"A": "+156 kJ/mol", "B": "-78 kJ/mol", "C": "-156 kJ/mol", "D": "-313 kJ/mol"},
        "correct": "C",
        "wrong": {
            "A": "The sign is wrong. A spontaneous cell has a positive potential and therefore a negative free energy change.",
            "B": "-78 kJ/mol uses n = 1. The passage states that two electrons are released per glucose.",
            "D": "-313 kJ/mol uses n = 4, which would be two glucose molecules rather than one.",
        },
    },
    "cp-p6-q3": {
        "choices": {"A": "0.25", "B": "0.32", "C": "0.40", "D": "2.5"},
        "correct": "C",
        "wrong": {
            "A": "0.25 inverts part of the ratio or misreads which distance is which.",
            "B": "0.32 divides the spot distance by 10 cm rather than by the 8.0 cm the solvent front actually travelled.",
            "D": "2.5 divides the solvent front by the spot. A retention factor above 1 is impossible, since the spot cannot outrun the solvent carrying it.",
        },
    },
    "cp-p8-q3": {
        "choices": {"A": "3.4 J", "B": "17 J", "C": "34 J", "D": "343 J"},
        "correct": "C",
        "wrong": {
            "A": "3.4 J is a factor of ten low, usually from using 0.005 m for the height.",
            "B": "17 J halves the height, which would be right only if the 5 cm were the full peak-to-peak range and the lift were half of it. The passage gives the rise itself.",
            "D": "343 J uses h = 0.5 m rather than 0.05 m.",
        },
    },
    "cp-p9-q1": {
        "choices": {"A": "+228 kJ/mol", "B": "+11.5 kJ/mol", "C": "-11.5 kJ/mol", "D": "-120 kJ/mol"},
        "correct": "C",
        "wrong": {
            "A": "+228 kJ/mol adds the two magnitudes, which drops the sign on the enthalpy term.",
            "B": "The sign is wrong, which usually comes from subtracting 108 500 rather than adding it. Subtracting a negative adds.",
            "D": "-120 kJ/mol is the enthalpy alone and ignores the entropy term entirely.",
        },
    },
    "cp-p9-q2": {
        "choices": {"A": "298 K", "B": "310 K", "C": "343 K", "D": "373 K"},
        "correct": "C",
        "wrong": {
            "A": "298 K is standard room temperature and has nothing to do with this protein's numbers.",
            "B": "310 K is body temperature, where the previous calculation shows the free energy change is still negative and the protein is folded.",
            "D": "373 K is the boiling point of water, not a value derived from the enthalpy and entropy given.",
        },
    },
}

for qid, patch in REWRITES.items():
    q = by_id[qid]
    q["choices"] = patch["choices"]
    q["correct"] = patch["correct"]
    q["wrong"] = patch["wrong"]

# --- 2. Prose sets rotated to a target letter ------------------------------
TARGETS = {
    # B is over-represented; send prose questions to the thin letters.
    "cp-p2-q4": "D", "cp-p6-q1": "D", "cp-p7-q4": "D", "cp-p8-q5": "D",
    "cp-p9-q3": "A", "cp-p9-q4": "D", "cp-p10-q4": "A",
    # C is over-represented after the numeric rewrites above.
    "cp-p1-q3": "D", "cp-p1-q5": "A", "cp-p4-q4": "D", "cp-p10-q3": "B",
    "cp-p6-q4": "B", "cp-p3-q1": "D",
    # A is now heavy; move a few on.
    "cp-p2-q1": "B", "cp-p6-q5": "C", "cp-p10-q2": "C",
}
LETTERS = ["A", "B", "C", "D"]

for qid, target in TARGETS.items():
    q = by_id[qid]
    if q["correct"] == target:
        continue
    key_text = q["choices"][q["correct"]]
    others = [(letter, q["choices"][letter]) for letter in LETTERS if letter != q["correct"]]
    note_by_text = {q["choices"][letter]: note for letter, note in q["wrong"].items()}
    new_choices, new_wrong = {}, {}
    pool = iter(others)
    for letter in LETTERS:
        if letter == target:
            new_choices[letter] = key_text
        else:
            _, text = next(pool)
            new_choices[letter] = text
            new_wrong[letter] = note_by_text[text]
    q["choices"], q["correct"], q["wrong"] = new_choices, target, new_wrong

# --- 3. Report --------------------------------------------------------------
tally = {letter: sum(1 for q in data["questions"] if q["correct"] == letter) for letter in LETTERS}
total = len(data["questions"])
print("key distribution:", {k: f"{v} ({round(100*v/total)}%)" for k, v in tally.items()})
for q in data["questions"]:
    assert set(q["wrong"]) == set(LETTERS) - {q["correct"]}, q["id"]
    assert len({v.strip().lower() for v in q["choices"].values()}) == 4, q["id"]
json.dump(data, open(path, "w"), indent=1, ensure_ascii=True)
print("written")
