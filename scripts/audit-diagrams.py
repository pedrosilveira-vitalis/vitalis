#!/usr/bin/env python3
"""Offline geometry audit of every lesson diagram.

Catches the layout faults that are invisible in the SVG source but obvious
on screen: text running off the canvas, text spilling out of the panel that
is supposed to contain it, and panels drawn outside the viewBox.

Width is estimated from font size and character mix, so the margins below
are deliberately generous: this flags gross overflow, not kerning.
Run it from the repo root:  python3 -I scripts/audit-diagrams.py
"""
import glob, os, re, sys, html
from collections import defaultdict

DIAG = "public/lesson-diagrams"

# average advance width as a fraction of font-size, by character class
NARROW = set("iljtfr.,:;'|!()[]/\\ ")
WIDE = set("MWmw@%—–")
# sub- and superscript glyphs render at roughly half size
SMALL = set("₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₕₖₗₘₙₚₛₜ"
            "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱ′″")


def text_width(s, size):
    w = 0.0
    for ch in s:
        if ch in SMALL:
            w += 0.34
        elif ch in NARROW:
            w += 0.28
        elif ch in WIDE:
            w += 0.88
        elif ch.isupper() or ch.isdigit():
            w += 0.60
        else:
            w += 0.50
    return w * size


# The width above is an estimate, and the "which panel contains this text"
# inference is weaker still. Only report an overflow big enough that an
# estimate cannot explain it -- a tool that cries wolf gets ignored, which
# is exactly how the review bug survived nineteen deployments.
SLACK = 0.07


CLASS_SIZE = {"h": 26, "sub": 15, "small": 12, "": 15}
ATTR = re.compile(r'(\w[\w-]*)="([^"]*)"')


def attrs(tag):
    return dict(ATTR.findall(tag))


def font_size(a):
    m = re.search(r"font-size:\s*([\d.]+)px", a.get("style", ""))
    if m:
        return float(m.group(1))
    return CLASS_SIZE.get(a.get("class", ""), 15)


def audit(path):
    src = open(path, encoding="utf-8").read()
    out = []
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', src)
    if not m:
        return [("no viewBox", "")]
    VW, VH = float(m.group(1)), float(m.group(2))

    # panels: every rect that is not the full-canvas background
    panels = []
    for t in re.findall(r"<rect[^>]*>", src):
        a = attrs(t)
        try:
            x, y = float(a.get("x", 0)), float(a.get("y", 0))
            w, h = float(a["width"]), float(a["height"])
        except (KeyError, ValueError):
            continue
        if w >= VW - 1 and h >= VH - 1:
            continue  # background
        if x < -1 or y < -1 or x + w > VW + 1 or y + h > VH + 1:
            out.append(("panel outside canvas",
                        f"rect at ({x:g},{y:g}) {w:g}x{h:g} vs canvas {VW:g}x{VH:g}"))
        panels.append((x, y, w, h))

    for t, body in re.findall(r"(<text[^>]*>)(.*?)</text>", src, re.S):
        a = attrs(t)
        if "transform" in a:
            continue  # rotated labels: axis titles, not worth modelling
        txt = html.unescape(re.sub(r"<[^>]+>", "", body)).strip()
        if not txt:
            continue
        try:
            x, y = float(a["x"]), float(a["y"])
        except (KeyError, ValueError):
            continue
        size = font_size(a)
        w = text_width(txt, size)
        anchor = a.get("text-anchor", "start")
        x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
        x1 = x0 + w
        label = txt[:46] + ("…" if len(txt) > 46 else "")

        slack = max(6.0, w * SLACK)
        if y > VH + 1 or y - size < -1:
            out.append(("text off canvas vertically",
                        f"baseline y={y:g} vs height {VH:g} — {label!r}"))
        elif x0 < -slack or x1 > VW + slack:
            out.append(("text off canvas horizontally",
                        f"spans {x0:.0f}..{x1:.0f} vs width {VW:g} — {label!r}"))
            continue

        # inside which panel does this text start?
        host = None
        for (px, py, pw, ph) in panels:
            if px <= x <= px + pw and py - size <= y <= py + ph:
                if host is None or (pw * ph) < (host[2] * host[3]):
                    host = (px, py, pw, ph)
        if host:
            px, py, pw, ph = host
            if y > py + ph + 2:
                out.append(("text below its panel",
                            f"baseline y={y:g}, panel ends {py + ph:g} — {label!r}"))
            elif x0 < px - slack or x1 > px + pw + slack:
                out.append(("text wider than its panel",
                            f"spans {x0:.0f}..{x1:.0f}, panel {px:g}..{px + pw:g}"
                            f" — {label!r}"))
    return out


# A legend that names a colour no mark actually uses is worse than no legend:
# the reader is told to tell two things apart by a difference that isn't there.
FAMILIES = {
    "navy": ("#18364a",),
    "blue": ("#245574", "#24495c", "#18364a"),
    "red": ("#a8324a",),
    "burgundy": ("#a8324a",),
    "maroon": ("#a8324a",),
    "crimson": ("#a8324a",),
    "sage": ("#5b7a64",),
    "green": ("#5b7a64",),
    "gold": ("#987740",),
    "amber": ("#987740",),
    "grey": ("#6d716f",),
    "gray": ("#6d716f",),
}
LEGEND = re.compile(r"\b(navy|blue|red|burgundy|maroon|crimson|sage|green|gold"
                    r"|amber|grey|gray)\b"
                    r"\s*(?:=|:|—|–|-|\s+line\b|\s+curve\b|\s+bar\b)", re.I)


def audit_legend(path):
    src = open(path, encoding="utf-8").read()
    body = re.sub(r"<desc\b.*?</desc>", "", src, flags=re.S)
    words = {m.group(1).lower() for m in LEGEND.finditer(
        " ".join(html.unescape(re.sub(r"<[^>]+>", " ", body)).split()))}
    marks = set(re.findall(r'(?:stroke|fill)="(#[0-9a-fA-F]{6})"', body))
    marks |= set(re.findall(r"(?:stroke|fill):\s*(#[0-9a-fA-F]{6})", body))
    marks = {c.lower() for c in marks}
    out = []
    for w in sorted(words):
        if not (set(FAMILIES[w]) & marks):
            out.append(("legend names an unused colour",
                        f"text says {w!r} but no mark is drawn in it"))
    return out


# Running off the canvas is a definite fault; spilling out of a panel is a
# guess, because which rect "contains" a label is itself inferred. Keep the
# two apart so the hard failures stay worth reading.
ADVISORY = {"text wider than its panel"}

hard = defaultdict(list)
soft = defaultdict(list)
files = sorted(glob.glob(os.path.join(DIAG, "*.svg")))
for p in files:
    for kind, detail in audit(p) + audit_legend(p):
        (soft if kind in ADVISORY else hard)[os.path.basename(p)].append(
            (kind, detail))


def show(bucket, heading):
    n = sum(len(v) for v in bucket.values())
    print(f"\n{n} {heading} in {len(bucket)} diagram(s):\n")
    for name in sorted(bucket):
        print(f"  {name}")
        for kind, detail in bucket[name]:
            print(f"      {kind}: {detail}")


print(f"diagrams checked: {len(files)}")
if soft:
    show(soft, "possible panel overflow(s) - estimated, confirm by eye")
if hard:
    show(hard, "definite fault(s)")
    sys.exit(1)
print("\nPASS - nothing runs off a canvas and every legend colour is drawn.")
sys.exit(0)
