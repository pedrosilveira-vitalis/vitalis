"""Break runs of the same answer key without breaking choice order.

Two moves are allowed, matching the two kinds of choice set:

  numeric  reverse the list, which turns ascending into descending. Both are
           orders the real exam uses, and the key moves from position p to
           position 5-p.
  prose    rotate the key onto a chosen letter, which is safe only when the
           choices carry no order of their own.

Labelled sets (Patient W, Sample B) and Roman numeral sets are never touched:
their order is part of the question.
"""
import io, json, re, sys

path = sys.argv[1]
data = json.load(io.open(path, encoding="utf-8"))
L = "ABCD"

LABEL = re.compile(r"^(?:patient|sample|subject|group|curve|compound|experiment|trial)\s+[A-Z0-9]\b", re.I)
ROMAN = re.compile(r"^(?:i{1,3})(?:\s*(?:,|and)\s*i{1,3})*\s*(?:only)?$", re.I)

def magnitude(text):
    t = text.replace("×", "x").replace(",", "")
    m = re.match(r"^\s*([-+]?\d+(?:\.\d+)?)", t)
    if not m:
        return None
    value = float(m.group(1))
    sup = {"¹":"1","²":"2","³":"3","⁰":"0","⁴":"4","⁵":"5",
           "⁶":"6","⁷":"7","⁸":"8","⁹":"9","⁻":"-"}
    e = re.search(r"x\s*10\s*([" + "".join(sup) + r"]+)", t)
    if e:
        try:
            return value * 10 ** int("".join(sup.get(c, c) for c in e.group(1)))
        except ValueError:
            return value
    return value

def kind(q):
    texts = [q["choices"][l].strip() for l in L]
    if any(LABEL.match(t) for t in texts):
        return "locked"
    if all(ROMAN.match(t) for t in texts):
        return "locked"
    vals = [magnitude(t) for t in texts]
    if all(v is not None for v in vals):
        up = all(vals[i] >= vals[i-1] for i in range(1, 4))
        down = all(vals[i] <= vals[i-1] for i in range(1, 4))
        if up or down:
            return "numeric"
        return "locked"          # already out of order; leave it to be fixed by hand
    return "prose"

def reverse(q):
    order = list(reversed(L))
    choices = {L[i]: q["choices"][order[i]] for i in range(4)}
    key = next(l for l in L if choices[l] == q["choices"][q["correct"]])
    notes = {q["choices"][l]: n for l, n in q["wrong"].items()}
    q["choices"] = choices
    q["correct"] = key
    q["wrong"] = {l: notes[choices[l]] for l in L if l != key}

def rotate(q, target):
    key = q["choices"][q["correct"]]
    rest = [q["choices"][l] for l in L if l != q["correct"]]
    notes = {q["choices"][l]: n for l, n in q["wrong"].items()}
    choices, wrong, it = {}, {}, iter(rest)
    for letter in L:
        if letter == target:
            choices[letter] = key
        else:
            text = next(it)
            choices[letter] = text
            wrong[letter] = notes[text]
    q["choices"], q["correct"], q["wrong"] = choices, target, wrong

questions = data["questions"]
moved = []
for _ in range(40):
    keys = [q["correct"] for q in questions]
    runs = [i for i in range(1, len(keys) - 1) if keys[i - 1] == keys[i] == keys[i + 1]]
    if not runs:
        break
    index = runs[0]
    counts = {l: keys.count(l) for l in L}
    fixed = False
    # Try the middle of the run first, then its neighbours.
    for candidate in (index, index + 1, index - 1):
        q = questions[candidate]
        shape = kind(q)
        if shape == "locked":
            continue
        before = keys[candidate - 1] if candidate > 0 else None
        after = keys[candidate + 1] if candidate + 1 < len(keys) else None
        if shape == "numeric":
            reverse(q)
            if q["correct"] not in (before, after):
                moved.append((q["id"], "reversed", q["correct"]))
                fixed = True
                break
            reverse(q)               # put it back; the flip did not help
            continue
        target = min((l for l in L if l not in (before, after, q["correct"])), key=lambda l: counts[l], default=None)
        if target:
            rotate(q, target)
            moved.append((q["id"], "rotated", target))
            fixed = True
            break
    if not fixed:
        print("could not break the run at", index, "- fix by hand")
        break

json.dump(data, io.open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=True)
keys = [q["correct"] for q in questions]
longest, run = 1, 1
for i in range(1, len(keys)):
    run = run + 1 if keys[i] == keys[i - 1] else 1
    longest = max(longest, run)
for item in moved:
    print("  moved", item[0], item[1], "->", item[2])
print("key:", {l: f"{keys.count(l)} ({round(100*keys.count(l)/len(keys))}%)" for l in L}, "longest run:", longest)
