# Lesson review checkpoint — 2026-11-08

## Delivered in chunk 1
- Nori opens a non-modal chat panel on the current page. Minimize retains messages in memory; New chat resets them. Refresh clears the chat. Uses existing /api/chat and API key. No new provider.
- Lesson 6 (Acid-Base Chemistry of Amino Acids): full text and five quiz items read; 30 targeted corrections across seven fields, with three original schematic diagrams in one SVG.
- Correction overlay is applied only if the title, content, and all five original quiz items match their stored hashes. Source edits cause an all-or-nothing skip. No database content is overwritten.
- Sources are shown below the visual aid. This is a targeted review, not an exhaustive accuracy certification. MCAT frequency predictions were not verified.

## Combined update — batch 2 (held for final installation)
- Lessons 4 and 5: full text and all ten quiz questions read. 68 targeted field replacements integrated with source links and old/new audit records (33 in lesson 4, 35 in lesson 5).
- Corrected amino-acid charge classifications, free versus peptide-bound groups, proline terminology, ribosomal peptide formation, collagen motifs, glycosylation caveats, A280 contributors, and selected clinical oversimplifications. Removed the second defensible answer in question 21 by isolating the charge effect.
- Added two original labeled SVG visual aids. Both rendered and visually checked; each lesson now supplies its own title, accessible description, caption and full-size image link.
- Expanded all-or-nothing guards to reject added, removed or duplicate quiz questions. Reordering alone is safe. Tests check every protected field for all three reviewed lessons.
- Cumulative integrated lessons: **3/250** (IDs 4, 5, 6). Earlier chunk-1 installer does not include batch 2; user requested one final combined installation and should wait.
- Automated suite: 26 passing tests. Production build passed after final edits (TypeScript and all 38 static pages). Authenticated browser chat/lesson checks on Vercel remain pending.

## Remaining scope
- 247 lessons still need final review/integration; diagrams are NOT installed across all sections yet.
- Earlier draft reviews exist for the lesson IDs below. A draft is NOT a finished or deployed review.
- Next chunk: lessons 7 and 8 (peptide bonds/protein secondary structure), then remaining biochemistry. Revalidate draft corrections against primary sources and the complete lesson, add relevant diagrams, run tests/build. Accumulate changes for one final installer rather than asking the user to install each batch.
- Continue remaining biochemistry, biology, chemistry, physics, psychology, sociology, and CARS in bounded batches. Do not re-review completed fields unless source hashes change.

Draft lesson IDs: 4, 5, 6, 7, 8, 44, 45, 46, 47, 48, 89, 90, 91, 92, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 149, 150, 151, 183, 184, 185, 219.

## Validation limits
- Automated tests and production build run locally. On-page chat still requires an authenticated Vercel Preview check with its existing API key. Live AI replies and browser interactions are not verified here.
- Diagram rendered to PNG and visually inspected.
- GitHub push from this workspace is unavailable: no GitHub write credentials. Installer runs checks and pushes a new feature branch from the user's authenticated Codespace; it never merges main.
- Prior npm audit reports require separate dependency triage before production release; no force updates were performed.

## Batch 3 — continued work (2026-11-08)
- Integrated IDs 7 and 8: complete lesson text and 10 questions read; 86 targeted replacements, two original SVG diagrams rendered and inspected, all source-field guards retained.
- Cumulative integrated lesson count is now **5/250**; 245 remain. IDs 9 and 10 are being reviewed next. Earlier remaining counts above describe earlier checkpoints.
- Flashcard generation now trims credentials, validates requests, rejects duplicate/oversized/incomplete decks, bounds the provider call, and logs only sanitized diagnostic categories and a request ID.
- A provider failure returns an explicitly labeled fixed core deck (6 cards per section, 24 total) instead of a blank failure screen. The client also offers these cards without a server request. It requests 8 AI cards rather than 20, cancels stale requests, and offers a repeat round for cards marked for review.
- All 29 tests and production build passed. Provider failure modes were tested with mocked responses. Actual production provider credentials and authenticated browser behavior have not been verified. No deployment or GitHub push performed.
- User explicitly requested continuous work without waiting between batches, then confirmed additional credits. Continue through the remaining review, preserving audit scope honestly. Do not ask the user to install each batch.

## Batches 4 and 5 — continued review (2026-11-08)
- Integrated IDs 9–14 after reading complete lesson text and all 30 associated questions. Corrected folding thermodynamics, Hsp70 cycling, inherited prions, reversed sickle mutation, binding-affinity and CO-shift errors, insulin maturation order, glycosylation compartments, enzyme classification and ambiguous quiz distractors.
- Added six original, accessible SVG visual aids and rendered/inspected all six.
- Cumulative: **11/250 lessons, 55 quiz questions** have targeted reviews integrated. **239 lessons remain.** This is not an exhaustive accuracy certification.
- Full production build and 31-test suite passed before the additional semantic regression test. Subsequent validation is recorded in the next checkpoint.
- No deployment performed. All batches are held for one final combined installer.

## Batch 6 — binding models and kinetics
- IDs 15 and 16: complete text and ten questions reviewed, 53 targeted replacements, two SVG diagrams rendered and inspected.
- Cumulative **13/250 lessons and 65 questions** integrated; **237 lessons remain**. Next: ID 17.
- Latest full suite: 33 tests (pending completion at checkpoint); production build running. No live deployment or final installer yet.

## Batches 7–9 — inhibitors, cofactors and metabolic foundations
- Integrated IDs 17–22 after reading all six complete lessons and their 30 quiz questions. Added six distinct SVG visual aids, rendered and visually inspected.
- Corrected reciprocal-plot algebra, inhibitor reversibility, emergency-glucose wording, coenzyme classification, missing kinetic assumptions, bacterial-versus-human regulation, zymogen activation, energy-charge definition, proton-pumping complexes and ATP bookkeeping.
- Cumulative **19/250 lessons and 95 questions** have targeted reviews integrated; **231 lessons remain**. Next: IDs 23 and 24. No exhaustive certification is claimed.
- **36 tests passed.** Full production build passed for IDs 4–20; next build must include the newly integrated IDs 21–22. No live deployment or final combined installer yet.
- Nori on-page chat and flashcard recovery are implemented in the accumulated branch. Live authenticated AI checks remain pending. All work stays together for the requested combined update.

## Batch 10 — glycolysis through respiratory-chain accounting
- Integrated IDs 23–28 after reading each full lesson and all 30 associated quiz questions. Added six distinct, rendered and visually inspected SVG diagrams.
- Corrected glycolytic ATP counts, glucokinase kinetics, PDC inhibition versus activation, TCA carbon tracking, malate-aspartate shuttle direction, CPS-II nitrogen donor, heme-question causality, Complex-IV proton counts, ATP-synthase binding states and reversible CO inhibition.
- Cumulative **25/250 lessons and 125 quiz questions** have targeted reviews integrated; **225 lessons remain**. No exhaustive certification is claimed.
- **39 tests passed; full production build passed** with IDs 4–28. No live deployment or final combined installer yet. Next: ATP synthase and fermentation (29–30).

## Batch 11 — ATP, fuel integration and DNA foundations (2026-11-09)
- Integrated IDs 29–34 after reading full text and all 30 quiz questions, with six distinct SVG visual aids rendered and inspected.
- Corrected ATP synthase terminology, lactate redox/proton accounting, human threonine metabolism, gluconeogenic isotope assumptions, hepatic insulin signaling, AMPK/ADP regulation, DNA sugar-ring chemistry and universal chromatin hierarchy claims.
- Cumulative **31/250 lessons and 155 questions** have targeted reviews integrated; **219 lessons remain**. No exhaustive certification is claimed.
- **43 tests passed.** Full production build passed through ID 33; the next build will include ID 34 and subsequent reviews. No live deployment or final combined installer yet.

## Batch 12 — replication, repair and production smoke checks (2026-11-09)
- Integrated IDs 35–36 after complete text and ten quiz-question reviews; two accessible diagrams rendered and inspected. Corrected helicase polarity, primer/template distinctions, polymerase exceptions, repair-pathway scope and outdated imetelstat wording.
- Cumulative **33/250 lessons and 165 quiz questions**; **217 lessons remain**. Reviews are targeted, not exhaustive certification.
- Nori API now validates conversation roles/content, preserves tutor image support, limits requests, bounds provider duration and returns sanitized failures with request IDs.
- **47 tests passed; full production build passed.** Started the production server and verified four core-deck API responses, home and flashcard pages, the new repair SVG, and invalid-chat rejection.
- Browser installation failed, so no browser-interaction pass is claimed. Live authenticated AI and deployment checks remain pending. No push or deployment performed.

## Batch 13 — transcription and RNA processing (2026-11-09)
- Integrated IDs 37–38 after reading both full lessons and all ten quiz questions: 96 targeted corrections, two distinct SVG diagrams rendered and visually inspected.
- Corrected exon definitions, sigma retention, active-center subunits, promoter scope, CPSF73 cleavage, dystrophin exon/intron counts, familial dysautonomia variant location, NMD distance reference and ivacaftor mechanism. Rewrote an ambiguous splice-site question around a measured RNA outcome.
- Cumulative **35/250 lessons and 175 quiz questions**, with **215 lessons remaining**. No exhaustive certification claimed.
- **49 tests passed; full production build passed** through ID 38. Earlier production-server flashcard/Nori validation remains recorded above. Live authenticated AI and actual browser interaction checks remain pending.
- Next lesson: ID 39. All changes remain in the combined work branch; no push/deployment or final installer yet.

## Installable checkpoint — 2026-11-09
- User requested delivery now, followed by the remaining lessons in later updates.
- Integrated complete-text targeted reviews of **40/250 lessons (IDs 4–43), 200 quiz questions**. **210 lessons remain unchanged.** ID 44 has been read but is not integrated or counted as reviewed.
- Latest additions (39–43): genetic code/tRNA, translation, protein targeting, bacterial and eukaryotic regulation. Corrected stored quiz keys, Trp attenuation, SMN1/SMN2, microRNA mechanisms and scope errors. Five new accessible SVGs rendered and inspected.
- On-page Nori and flashcard reliability changes are included with the original streak/calls features. Core fallback decks are explicitly labeled; 6 per section, 24 total. They are not claimed to be newly generated AI cards.
- 54 automated tests passed. Final production build and package reconstruction checks are recorded in the release README. No live deployment or authenticated AI/browser verification is claimed.
- Packaging excludes source snapshots and unfinished draft audits; guarded overlays preserve database content and skip changed lesson sources atomically.

## Typography and review checkpoint — 2026-11-09
- Standardized application typography on Geist sans; replaced decorative burgundy with blue in application UI and all 41 lesson diagrams. Preserved Nori's character coloring and the Google identity mark.
- Filled missing diagram title/dimension metadata; added assertions covering all reviewed visual metadata.
- Integrated lesson 44 after full lesson/five-question reading: 40 targeted corrections to Mendelian probability, genotype counting, linkage, pedigree scope and statistical interpretation. Added and rendered a Punnett-square/branch diagram.
- Total: **41/250 lessons, 205 quiz questions; 209 lessons remain**. No 100% accuracy guarantee or exhaustive certification.
- **55 tests passed; production build passed**. New SVG rendered with Sharp and visually inspected. Full browser interaction and live authenticated APIs have not been reverified for this checkpoint.
- No production deployment performed. Next content review: lesson 45.


## Glossy study experience + next 20 lessons — 2026-11-09
- Completed full-text targeted reviews of IDs **45–64**, with all **100 quiz items**, **627 source-linked corrections**, and **20 new scientific SVG diagrams**. Each diagram rendered and visually inspected; chamber-label overlap in the ECG diagram corrected during QA.
- Added exact heading-based inline diagram placement; tests verify every placement exists and preserve all lesson text. Selection/highlighting remains restricted to lesson text.
- Cumulative **61/250 lessons and 305 quiz questions** reviewed; **189 lessons remain**. Next lesson ID65. Review stopped at this requested batch.
- Restored stronger blue enamel buttons with sheen, depth and press feedback. Added server-confirmed first-answer daily celebration, milestone wording, session-completion Nori and reduced-motion support. No repeated reward for visits or repeated same-day answers.
- 67 tests passed, including all review guards/quiz uniqueness and corrected-key regressions; production build and TypeScript check passed.
- Browser QA blocked: managed preview supplies unsupported --host/--strictPort arguments to next dev. No working-app code was changed to bypass that limitation. Full authenticated browser/production verification remains a Preview acceptance task.
- Original database content is not overwritten; reviews skip atomically if stored content or quiz items have changed. Dependency audit warnings from the previous install have not been remediated in this feature update.

## Batch 14 — patch-based reviews, cardiovascular and respiratory (2026-11-11)
- New mechanism: `lib/lesson-patches.ts` applies exact old→new text patches from `lib/lesson-reviews/lesson-NNN.json` (index rebuilt by `scripts/build-review-index.mjs`). All-or-nothing: one SHA-256 fingerprint covers title, content and every quiz field; any patch text that is missing or appears more than once skips the whole review.
- Integrated IDs 65–71 (cardiac output, vascular physiology, BP control, capillary exchange, breathing mechanics, O2 transport, CO2/acid-base). Each patch records its reason; each lesson lists the sources consulted and has a new SVG diagram (rendered and inspected).
- Patch texts and fingerprints were checked against the live lesson API before saving.
- ID 72 (renal filtration): corrections drafted and diagram drawn; not yet verified against live text or integrated.
- Cumulative: **68/250 lessons** reviewed. 182 remain (IDs 72–253).
- Not yet run: `npm test` / `npm run build` (no package installs in this workspace). Push blocked until the Claude GitHub App is installed on the repo.
