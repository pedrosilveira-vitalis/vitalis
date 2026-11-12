#!/usr/bin/env python3
"""Offline structural audit of every lesson review in the Vitalis repo.

Checks the classes of defect that silently break a review *without* failing a
build: wrong field prefixes, non-unique anchors, fingerprint/guard shape,
missing or mis-sized diagrams, duplicate assets, unregistered files.

Cannot check factual accuracy -- that needs the live lesson text.
"""
import json, os, re, sys, hashlib
from collections import defaultdict

ROOT = "/home/claude/vitalis"
PATCH_DIR = os.path.join(ROOT, "lib/lesson-reviews")
UPD_DIR = os.path.join(ROOT, "lib/lesson-updates")
DIAG = os.path.join(ROOT, "public/lesson-diagrams")

QCOLS = {"question_text", "choice_a", "choice_b", "choice_c", "choice_d",
         "correct_answer", "explanation"}
LCOLS = {"title", "content"}

problems = []
def bad(where, msg):
    problems.append((where, msg))

svg_users = defaultdict(list)


def check_visual(where, v, lesson_id):
    if not isinstance(v, dict):
        return bad(where, "visual is not an object")
    for k in ("title", "src", "width", "height", "alt", "caption"):
        if k not in v:
            bad(where, f"visual missing '{k}'")
    src = v.get("src", "")
    if not isinstance(src, str) or not src.startswith("/lesson-diagrams/"):
        return bad(where, f"visual.src not under /lesson-diagrams/: {src!r}")
    svg_users[src].append(lesson_id)
    path = os.path.join(ROOT, "public", src.lstrip("/"))
    if not os.path.exists(path):
        return bad(where, f"visual.src file missing on disk: {src}")
    head = open(path, encoding="utf-8").read(4000)
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', head)
    if not m:
        bad(where, "SVG has no parseable viewBox")
    else:
        vw, vh = float(m.group(1)), float(m.group(2))
        if (vw, vh) != (float(v.get("width", -1)), float(v.get("height", -1))):
            bad(where, f"declared {v.get('width')}x{v.get('height')} "
                       f"but SVG viewBox is {vw:g}x{vh:g}")
    for k in ("alt", "caption", "title"):
        if not str(v.get(k, "")).strip():
            bad(where, f"visual.{k} is empty")
    if len(str(v.get("alt", ""))) < 80:
        bad(where, "visual.alt is suspiciously short for a screen reader")


def check_sources(where, srcs):
    if not isinstance(srcs, list) or not srcs:
        return bad(where, "no sources listed")
    for s in srcs:
        if not isinstance(s, dict) or not s.get("title") or not s.get("url"):
            bad(where, f"malformed source entry: {s!r}")
        elif not str(s["url"]).startswith("http"):
            bad(where, f"source url is not a URL: {s['url']!r}")


# ---------------------------------------------------------------- patch system
patch_ids = set()
for fn in sorted(os.listdir(PATCH_DIR)):
    if not fn.endswith(".json"):
        continue
    where = f"lesson-reviews/{fn}"
    try:
        r = json.load(open(os.path.join(PATCH_DIR, fn), encoding="utf-8"))
    except Exception as e:
        bad(where, f"invalid JSON: {e}")
        continue
    want = int(re.search(r"(\d+)", fn).group(1))
    if r.get("lessonId") != want:
        bad(where, f"lessonId {r.get('lessonId')} does not match filename")
    patch_ids.add(r.get("lessonId"))

    for k in ("lessonId", "reviewedAt", "questionIds", "fingerprint", "patches",
              "sources", "visual"):
        if k not in r:
            bad(where, f"missing required key '{k}'")
    if not re.fullmatch(r"[0-9a-f]{64}", str(r.get("fingerprint", ""))):
        bad(where, "fingerprint is not 64 hex chars")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r.get("reviewedAt", ""))):
        bad(where, f"reviewedAt not YYYY-MM-DD: {r.get('reviewedAt')!r}")
    qids = r.get("questionIds") or []
    if not qids or len(set(qids)) != len(qids):
        bad(where, "questionIds empty or contains duplicates")
    if qids != sorted(qids):
        bad(where, "questionIds not in ascending order (fingerprint is order-sensitive)")

    seen = defaultdict(list)
    for i, p in enumerate(r.get("patches", [])):
        pw = f"{where} patch[{i}]"
        if not isinstance(p, dict):
            bad(pw, "not an object"); continue
        for k in ("field", "old", "new"):
            if k not in p:
                bad(pw, f"missing '{k}'")
        f = p.get("field", "")
        m = re.fullmatch(r"lesson\.(\w+)|questions\.(\d+)\.(\w+)", f)
        if not m:
            bad(pw, f"field {f!r} does not match lesson.<col> or questions.<id>.<col>"
                    " -- locate() will return undefined and the whole review is dropped")
        elif m.group(1):
            if m.group(1) not in LCOLS:
                bad(pw, f"unknown lesson column {m.group(1)!r}")
        else:
            if int(m.group(2)) not in qids:
                bad(pw, f"question {m.group(2)} is not in questionIds")
            if m.group(3) not in QCOLS:
                bad(pw, f"unknown question column {m.group(3)!r}")
        if p.get("old") == p.get("new"):
            bad(pw, "no-op patch (old == new)")
        if not str(p.get("old", "")).strip():
            bad(pw, "empty 'old' anchor")
        seen[f].append(p.get("old", ""))

    # within one field, no anchor may contain another: applying the first
    # rewrites the text the second is still looking for.
    for f, olds in seen.items():
        for a in olds:
            for b in olds:
                if a is not b and a and b and a in b:
                    bad(f"{where} field {f}",
                        f"anchor {a[:48]!r}... is contained in another anchor"
                        " -- patches will collide")
    check_sources(where, r.get("sources"))
    check_visual(where, r.get("visual"), r.get("lessonId"))

# every json registered in index.ts?
idx = open(os.path.join(PATCH_DIR, "index.ts"), encoding="utf-8").read()
for fn in sorted(os.listdir(PATCH_DIR)):
    if fn.endswith(".json") and f'"./{fn[:-5]}.json"' not in idx:
        bad("lesson-reviews/index.ts", f"{fn} exists but is never imported")

# --------------------------------------------------------------- update system
reg = open(os.path.join(ROOT, "lib/lesson-updates.ts"), encoding="utf-8").read()
upd_ids = set()
for fn in sorted(os.listdir(UPD_DIR)):
    if not fn.endswith(".json"):
        continue
    where = f"lesson-updates/{fn}"
    try:
        r = json.load(open(os.path.join(UPD_DIR, fn), encoding="utf-8"))
    except Exception as e:
        bad(where, f"invalid JSON: {e}")
        continue
    if f'"./lesson-updates/{fn}"' not in reg:
        bad(where, "exists but is never imported by lesson-updates.ts")
        continue
    lid = r.get("lessonId")
    if lid in upd_ids:
        bad(where, f"duplicate lessonId {lid} -- only the first wins")
    upd_ids.add(lid)
    if lid in patch_ids:
        bad(where, f"lesson {lid} has BOTH an update and a patch review"
                   " -- the patch review is dead code")

    guard_fields = set()
    for g in r.get("guards", []):
        gf = g.get("field", "")
        guard_fields.add(gf)
        if not re.fullmatch(r"lesson\.(\w+)|questions\.(\d+)\.(\w+)", gf):
            bad(where, f"guard field {gf!r} is malformed")
        if not re.fullmatch(r"[0-9a-f]{64}", str(g.get("sha256", ""))):
            bad(where, f"guard {gf} sha256 is not 64 hex chars")

    for u in r.get("updates", []):
        uf = u.get("field", "")
        # applyLessonUpdates writes lesson content via the bare field "content";
        # anything else is treated as questions.<id>.<col> and a "lesson."
        # prefix here dereferences undefined at runtime.
        if uf == "content":
            ok = True
        else:
            ok = bool(re.fullmatch(r"questions?\.(\d+)\.(\w+)", uf))
        if not ok:
            bad(where, f"update field {uf!r} is neither \"content\" nor "
                       "questions.<id>.<col> -- this throws at render time")
        if "value" not in u:
            bad(where, f"update {uf} has no 'value'")
        # every updated field must be guarded, or a stale edit can be applied
        # to text that has since changed underneath it.
        gf = "lesson.content" if uf == "content" else re.sub(r"^question\.", "questions.", uf)
        if gf not in guard_fields:
            bad(where, f"update to {uf} has no matching guard ({gf})")

    check_sources(where, r.get("sources"))
    check_visual(where, r.get("visual"), lid)

# -------------------------------------------------------------------- globals
for src, users in sorted(svg_users.items()):
    if len(users) > 1:
        bad("public/lesson-diagrams", f"{src} is used by lessons {users}")

orphans = sorted(set(os.path.basename(p) for p in os.listdir(DIAG) if p.endswith(".svg"))
                 - set(os.path.basename(s) for s in svg_users))
covered = sorted(patch_ids | upd_ids)

print(f"reviews audited : {len(patch_ids) + len(upd_ids)}"
      f"  ({len(upd_ids)} update-style, {len(patch_ids)} patch-style)")
print(f"lesson ids      : {covered[0]}-{covered[-1]}, "
      f"gaps: {[i for i in range(covered[0], covered[-1] + 1) if i not in set(covered)]}")
print(f"diagrams in use : {len(svg_users)} of {len(os.listdir(DIAG))} files")
if orphans:
    print(f"unreferenced svg: {', '.join(orphans)}")
print()
if not problems:
    print("PASS - no structural problems found.")
else:
    print(f"{len(problems)} PROBLEM(S):\n")
    for w, m in problems:
        print(f"  [{w}]\n      {m}")
sys.exit(1 if problems else 0)
