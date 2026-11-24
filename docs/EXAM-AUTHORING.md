# Writing exam content

Every rule here exists because it was broken once. The defects are recorded
with them, because a rule without its reason gets dropped the first time it is
inconvenient.

Run before shipping any section:

```
node scripts/screen-exam-questions.mjs          # defect screen
node scripts/typeset-exam-content.mjs <file>    # ASCII shorthand -> real notation
node scripts/exam-gap.mjs fl1                   # what the section still needs
./scripts/run-tests.sh exam-content.test.ts exam-score.test.ts exam-simulation.test.ts
```

## The answer key

**Plan the key before writing the question, not after.** The defect: in the
first Chem/Phys batch the key was B in 50% of questions. It was not bad luck.
Building numeric choices as "one value below, two above" puts the key second
every time, and a form that keys 50% B is guessable, which makes the score
meaningless.

Use `node scripts/plan-answer-key.mjs <n>` to get a target sequence, and write
each question's distractors so the key lands on its assigned letter.

- No letter below 15% or above 35% of a section.
- Never three of the same letter in a row.
- Fix a skew by **rewriting distractors**, never by rotating choices. Each new
  distractor must be the result of a specific mistake a student makes.

## Choice order

**Anything with a natural order must appear in it.** The defect: the script
that rebalanced the key rotated choices freely, and produced patients listed
W, X, Z, Y; percentages 80, 64, 20, 41; magnifications 40x, 100x, 4000x, 400x;
and solubilities with the last two swapped. The real exam never does this, and
a student who notices the jumble learns to distrust the form.

- Numeric choices ascend or descend, never jump about.
- Labelled items (Patient W, Sample B, Experiment 2) run in their own order.
- Roman numeral sets run I only, I and II only, I and III only, I II and III.
- Prose choices have no natural order and may be arranged freely.

## Distractors

- Every distractor is a **specific mistake**, named in its note: using the
  normal value instead of the patient's, squaring a ratio that was already an
  area, halving a height that was already the rise.
- Only one choice is flawless; each of the other three has a definite flaw.
- **Keep the lengths even.** The defect: two keys ran nearly twice the length
  of any distractor. "Pick the longest answer" is the oldest guessing
  heuristic there is.
- No "all of the above" or "none of the above". The real exam does not use them.
- A note on a distractor explains why that choice is wrong, never restates the key.

## Question formats

The real exam uses these throughout, and a form without them leaves students
meeting the format for the first time on test day:

- **Roman numeral** items: two to eight per finished section.
- **Negative stems** (EXCEPT, LEAST, NOT, LOWEST): two to eight per section.

## Arithmetic

**Compute every quantitative key; never type it from memory.** Two defects
caught this way: a Bernoulli answer out by a factor of seven, and a charge
calculation out by a thousand (1.0 mA for 2.0 s is two millicoulombs, not two
coulombs).

**And verify the model, not just the arithmetic.** The verifier once confirmed
my own mistake back to me, because I had modelled continuity on a radius ratio
when the passage gave an area. A checker that shares your assumption is worth
nothing. Read the numbers it prints and ask whether they are physically
sensible.

Compute the distractors too, so none is accidentally also correct.

## Passages

- Science passages run 250-500 words; CARS passages 500-600.
  The defect: two passages shipped at 116 and 126 words, which makes their
  questions read as discretes with decoration.
- Every passage carries at least two paragraphs and 4-7 questions (5-7 in CARS).
- Where a passage states a fact that could be checked, record the source.

## Notation

Draft in ASCII and run the typesetter. It converts species, exponents, Greek
letters, deltas, multiplication signs and ranges. The defect: a whole section
shipped reading `[HCO3-]`, `PCO2`, `r^4` and `0.03 x PCO2`. A student who has
only ever read the shorthand has to translate on test day.

### What the typesetter will and will not touch

It converts a token only when the whole token decomposes into real element
symbols, so chemical formulas convert and biological names do not:

| Written | Becomes | |
|---|---|---|
| `H2O`, `CaC2O4`, `C6H12O6` | H₂O, CaC₂O₄, C₆H₁₂O₆ | real formulas |
| `Fe2+`, `NH4+` | Fe²⁺, NH₄⁺ | charges superscript |
| `SGLT2`, `CDK4`, `E2F`, `HER2`, `IL6`, `P450` | unchanged | no element "G", "D", "E"; P450 exceeds the two-digit cap |
| `beta-oxidation` | unchanged | only a standalone `eta` becomes η |

Two more collisions were found by authors and fixed in the rule rather than
worked around in prose: `N2` was being read as nitrogen, which turned the
sleep stage N2 into N₂, so the standalone nitrogen rule is gone (write it
inside a longer formula if you need it); and the optics variables `do` and
`di` fired on ordinary English, turning "what each schedule should do, which"
into "should dₒ, which" — they now convert only in `1/do` and `1/di`.

The defect: an earlier version subscripted any letters-and-digits token, which
turned SGLT2 into SGLT₂ and E2F into E₂F. An agent writing the Bio/Biochem
section had to spell those names out in prose to avoid it. Write the names
normally; if something still converts wrongly, fix the rule rather than the
content.

## Reports

**A section with no questions is unscored, not zero.** The defect: three
unwritten sections each scored the floor of 118, which produced a
confident-looking total of 481 and advice telling the student that CARS was
"dragging the total" and sat "9 points below your best section" — about a
section with nothing in it. A form with any unscored section yields no total.

### Read the output, not just the exit code

Six explanations shipped across two forms with a bracket that never closed,
because the exponent rule `\^\(?(-?\d+)\)?` consumed the parenthesis after
`^2` as well as the one in `^(-2)`. `(v2^2 - v1^2)` became `(v₂² - v₁²`.
Every test passed throughout: no test read the prose. The screen now checks
bracket balance in every stem, choice, note and paragraph, but the lesson is
that a passing suite is not the same as a correct one.

### Running the checks while others are writing

`screen-exam-questions.mjs` and the content test walk every file under
`content/`, so a section another author is part-way through writing used to
take them down with "Unexpected end of JSON input". Both now skip a file that
will not parse and say so. A file that is genuinely malformed still fails the
build when its import resolves, so nothing broken gets through on the
strength of being skipped.

## When a check is wrong

A broken check does not merely fail to catch defects — it introduces them. The
overlap screen once flagged a numeric choice set because "1.6 mM" is a
substring of "0.016 mM", and the author replaced a good distractor with a
weaker one to satisfy it. Another replaced a "156%" option, the best wrong
answer on its question, because it contained "56%".

If a check objects to something you believe is right, say so and leave the
content alone. Report it rather than degrading the question to pass.

## Copyright

No content from AAMC, UWorld, Kaplan, Blueprint or any other publisher, in any
form, including paraphrase. Questions are written from the published blueprint
only. This is not caution: reusing a competitor's items is the easiest lawsuit
a prep company can invite, and the site tells students nothing is copied.

## Quoted phrases must exist in the passage

**The defect.** Two CARS sections shipped with questions quoting words that
were not in their passage — five in one, three in another. The screen was
clean, all 25 tests passed, and the arithmetic verifiers had nothing to say,
because none of them compares the words inside quotation marks against the
words in the text.

**The cause is mechanical, not careless.** A passage is drafted long, the
questions are written against that draft, and then the passage is trimmed to
its 500–600 word limit. Every cut is a chance to orphan a quotation. One
author found five in its own section this way and said plainly that the
trimming pass was the cause.

**Why it matters more than it looks.** A CARS question whose quoted phrase is
absent is not a hard question. It is unanswerable: the student is told to find
words that are not there, and will spend minutes of a timed section looking.

**The rule.** Run `node scripts/verify-passage-quotations.mjs` after any edit
to a passage, and never trim a passage after writing its questions without
re-running it. The same check runs inside the test suite, so it cannot be
skipped.

**What counts.** A quotation must be verbatim, including inflection. Three
live questions quoted `'dissolves the problem'`, `'an error with a
discoverable answer'` and `'is making a decision...'` where the passages read
*dissolve*, *errors* and *they are making*. Each was the author silently
conjugating the quote to fit the sentence around it. Put the altered word
outside the quotation marks instead. An ellipsis is a legitimate elision and
the check follows it, provided the fragments appear in order.

**What the check deliberately ignores.** A stem may invent quoted material —
a new-information question routinely puts words in a hypothetical writer's
mouth — and a choice may quote that invention back. Those are not checked,
but they count as a source an explanation may quote from.

## Fixing a typesetter rule does not fix what it already corrupted

The `do`/`di` optics rule once matched ordinary English and turned *do* into
*d-subscript-o*. The rule was fixed. The five corrupted words it had already
written stayed in two live forms for a week, and were found only because the
quotation check could not match a phrase containing one.

After changing any rule in `scripts/typeset-exam-content.mjs`, grep every
content file for the class of damage the old rule could have done. A
sub- or superscript glyph flanked by ASCII letters is almost always
corruption: `Eₐ` and `1/dₒ + 1/dᵢ` are correct physics, but `performers dₒ`
and `Sₙ2` are not — the second being a notation error as well, since
nucleophilic substitution takes a capital N.
