#!/usr/bin/env bash
# Run the pure-logic tests without node_modules.
#
# The workspace has no network, so `npm test` (tsx + pglite) cannot run here.
# Node can strip types on its own, but it needs explicit file extensions on
# relative imports, so this copies the files it needs to a scratch directory,
# rewrites the specifiers, and runs them there. Tests that need a database or
# JSX are skipped — those still have to go through Vercel's build.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

cp -r "$root/lib" "$work/lib"
mkdir -p "$work/components/exam"
cp "$root/components/exam/annotations.ts" "$work/components/exam/" 2>/dev/null || true
mkdir -p "$work/tests"
for name in "$@"; do cp "$root/tests/$name" "$work/tests/"; done

python3 - "$work" <<'PY'
import os, re, sys
work = sys.argv[1]
for base, _, files in os.walk(work):
    for name in files:
        if not name.endswith(".ts"):
            continue
        path = os.path.join(base, name)
        text = open(path).read()
        text = re.sub(
            r'(from\s+")(\.[^"]*?)(")',
            lambda m: m.group(1) + m.group(2) + ("" if m.group(2).endswith(".ts") else ".ts") + m.group(3),
            text,
        )
        open(path, "w").write(text)
PY

cd "$work"
node --experimental-strip-types --test tests/*.test.ts
