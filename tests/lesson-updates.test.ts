import mendelian from "./fixtures/lesson-44.json";
import eukRegulation from "./fixtures/lesson-43.json";
import operons from "./fixtures/lesson-42.json";
import proteinTargeting from "./fixtures/lesson-41.json";
import geneticCode from "./fixtures/lesson-39.json";
import translation from "./fixtures/lesson-40.json";
import rnaProcessing from "./fixtures/lesson-38.json";
import transcription from "./fixtures/lesson-37.json";
import repair from "./fixtures/lesson-36.json";
import replication from "./fixtures/lesson-35.json";
import dna from "./fixtures/lesson-34.json";
import homeostasis from "./fixtures/lesson-33.json";
import fuel from "./fixtures/lesson-31.json";
import gng from "./fixtures/lesson-32.json";
import atp from "./fixtures/lesson-29.json";
import fermentation from "./fixtures/lesson-30.json";
import amphibolic from "./fixtures/lesson-27.json";
import etc from "./fixtures/lesson-28.json";
import pdh from "./fixtures/lesson-25.json";
import tca from "./fixtures/lesson-26.json";
import processing from "./fixtures/lesson-13.json";
import catalysis from "./fixtures/lesson-14.json";
import models from "./fixtures/lesson-15.json";
import kinetics from "./fixtures/lesson-16.json";
import reciprocal from "./fixtures/lesson-17.json";
import inhibition from "./fixtures/lesson-18.json";
import cofactors from "./fixtures/lesson-19.json";
import allostery from "./fixtures/lesson-20.json";
import regulation from "./fixtures/lesson-21.json";
import energy from "./fixtures/lesson-22.json";
import glycolysis from "./fixtures/lesson-23.json";
import glycolyticControl from "./fixtures/lesson-24.json";
import test from "node:test";
import assert from "node:assert/strict";
import peptide from "./fixtures/lesson-7.json";
import secondary from "./fixtures/lesson-8.json";
import assembly from "./fixtures/lesson-9.json";
import stability from "./fixtures/lesson-10.json";
import binding from "./fixtures/lesson-11.json";
import hemoglobin from "./fixtures/lesson-12.json";
import fixture from "./fixtures/lesson-6.json";
import structure from "./fixtures/lesson-4.json";
import classification from "./fixtures/lesson-5.json";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { applyLessonUpdates } from "../lib/lesson-updates";

test("review overlay fixes charge chemistry and the quiz answer together without mutating source", () => {
  const before = JSON.stringify(fixture);
  const result = applyLessonUpdates(fixture.lesson, fixture.questions);
  assert.ok(result.review);
  assert.match(result.lesson.content, /pI\(His\).*7.6/);
  assert.doesNotMatch(result.lesson.content, /pI\(His\).*3.9/);
  assert.equal(result.questions.find(q => q.id === 30)?.correct_answer, "B");
  assert.equal(result.questions.find(q => q.id === 29)?.choice_a, "Approximately 15%");
  assert.equal(JSON.stringify(fixture), before);
});
test("changed source is left untouched and not marked reviewed", (t) => {
  t.mock.method(console, "warn", () => {});
  const changed = structuredClone(fixture);
  changed.questions[4].choice_b += " Edited";
  const result = applyLessonUpdates(changed.lesson, changed.questions);
  assert.equal(result.review, null);
  assert.deepEqual(result.questions, changed.questions);
  assert.equal(result.lesson.content, changed.lesson.content);
});
test("unreviewed lessons are left untouched", () => {
  const other = { ...fixture.lesson, id: 45 };
  assert.deepEqual(applyLessonUpdates(other, fixture.questions), { lesson: other, questions: fixture.questions, review: null });
});

test("structure review repairs cysteine charge and ribosomal quiz wording together", () => {
  const before = JSON.stringify(structure);
  const result = applyLessonUpdates(structure.lesson, structure.questions);
  assert.match(result.lesson.content, /mostly protonated at physiological pH; about 11% deprotonated/);
  assert.match(result.lesson.content, /malate-aspartate shuttle/);
  assert.match(result.lesson.content, /higher atomic number/);
  const peptide = result.questions.find(q => q.id === 20)!;
  assert.equal(peptide.correct_answer, "B");
  assert.doesNotMatch(peptide.choice_b, /releasing water/);
  assert.match(peptide.explanation, /deacylated tRNA rather than water/);
  assert.equal(JSON.stringify(structure), before);
});

test("classification review removes second charge-loss answer and repairs A280 explanation", () => {
  const before = JSON.stringify(classification);
  const result = applyLessonUpdates(classification.lesson, classification.questions);
  const charge = result.questions.find(q => q.id === 21)!;
  assert.equal(charge.correct_answer, "C");
  assert.equal(charge.choice_d, "Glutamine replaced by asparagine");
  assert.match(charge.question_text, /unchanged active-site geometry/);
  assert.match(result.questions.find(q => q.id === 23)!.explanation, /contributes little at 280 nm/);
  assert.match(result.lesson.content, /selenocysteine/);
  assert.match(result.lesson.content, /where X is not proline/);
  assert.doesNotMatch(result.lesson.content, /His.*best physiological buffer/);
  assert.equal(JSON.stringify(classification), before);
});

test("each reviewed lesson has a distinct, accessible visual and valid quiz keys", () => {
  const paths = new Set<string>();
  for (const source of [structure, classification, fixture, peptide, secondary, assembly, stability, binding, hemoglobin, processing, catalysis, models, kinetics, reciprocal, inhibition, cofactors, allostery, regulation, energy, glycolysis, glycolyticControl, pdh, tca, amphibolic, etc, atp, fermentation, fuel, gng, homeostasis, dna, replication, repair, transcription, rnaProcessing, geneticCode, translation, proteinTargeting, operons, eukRegulation, mendelian]) {
    const { review, questions } = applyLessonUpdates(source.lesson, source.questions);
    assert.ok(review);
    paths.add(review.visual.src);
    assert.ok(review.visual.alt.length > 50);
    assert.ok(review.visual.title.length > 5);
    assert.ok(review.visual.width > 0 && review.visual.height > 0);
    const path = join(process.cwd(), "public", review.visual.src);
    assert.ok(existsSync(path));
    const svg = readFileSync(path, "utf8");
    assert.match(svg, /<title/);
    assert.match(svg, /<desc/);
    for (const q of questions) {
      assert.match(q.correct_answer, /^[ABCD]$/);
      assert.equal(new Set([q.choice_a, q.choice_b, q.choice_c, q.choice_d]).size, 4);
    }
  }
  assert.equal(paths.size, 41);
});

test("added, missing or duplicate questions invalidate review; changed order does not", (t) => {
  t.mock.method(console, "warn", () => {});
  for (const source of [structure, classification, fixture, peptide, secondary, assembly, stability, binding, hemoglobin, processing, catalysis, models, kinetics, reciprocal, inhibition, cofactors, allostery, regulation, energy, glycolysis, glycolyticControl, pdh, tca, amphibolic, etc, atp, fermentation, fuel, gng, homeostasis, dna, replication, repair, transcription, rnaProcessing, geneticCode, translation, proteinTargeting, operons, eukRegulation, mendelian]) {
    const qs = source.questions;
    const variants = [qs.slice(1), [...qs, { ...qs[0], id: 99999 }], [...qs.slice(1), qs[1]]];
    for (const variant of variants) {
      const result = applyLessonUpdates(source.lesson, variant);
      assert.equal(result.review, null);
      assert.equal(result.questions, variant);
      assert.equal(result.lesson, source.lesson);
    }
    assert.ok(applyLessonUpdates(source.lesson, [...qs].reverse()).review);
  }
});

test("every guarded lesson and question field blocks a stale review when changed", (t) => {
  t.mock.method(console, "warn", () => {});
  for (const source of [structure, classification, fixture, peptide, secondary, assembly, stability, binding, hemoglobin, processing, catalysis, models, kinetics, reciprocal, inhibition, cofactors, allostery, regulation, energy, glycolysis, glycolyticControl, pdh, tca, amphibolic, etc, atp, fermentation, fuel, gng, homeostasis, dna, replication, repair, transcription, rnaProcessing, geneticCode, translation, proteinTargeting, operons, eukRegulation, mendelian]) {
    for (const field of ["title", "content"] as const) {
      const changed = structuredClone(source);
      changed.lesson[field] += " changed";
      assert.equal(applyLessonUpdates(changed.lesson, changed.questions).review, null);
    }
    for (const index of source.questions.keys()) {
      for (const field of ["question_text", "choice_a", "choice_b", "choice_c", "choice_d", "correct_answer", "explanation"] as const) {
        const changed = structuredClone(source);
        changed.questions[index][field] += " changed";
        assert.equal(applyLessonUpdates(changed.lesson, changed.questions).review, null);
      }
    }
  }
});


test("folding review fixes energy signs, Hsp70 cycle and inherited prion claims", () => {
  const a = applyLessonUpdates(assembly.lesson, assembly.questions);
  assert.match(a.lesson.content, /ATP hydrolysis favors tight substrate binding/);
  assert.match(a.lesson.content, /α\/β-tubulin/);
  const s = applyLessonUpdates(stability.lesson, stability.questions);
  assert.match(s.lesson.content, /they cannot cancel each other/);
  assert.match(s.lesson.content, /16 subunits total/);
  assert.doesNotMatch(s.questions.find(q => q.id === 50)!.explanation, /prion diseases are not caused by mutations/);
  assert.match(s.questions.find(q => q.id === 50)!.explanation, /inherited/);
});


test("binding review corrects sickle mutation, affinity direction and CO curve shift", () => {
  const b = applyLessonUpdates(binding.lesson, binding.questions);
  assert.match(b.lesson.content, /Glu→Val substitution/);
  assert.match(b.lesson.content, /decreasing K_d as affinity improves/);
  assert.doesNotMatch(b.lesson.content, /met-Hb subunits lock remaining subunits in the T state/);
  const hb = applyLessonUpdates(hemoglobin.lesson, hemoglobin.questions);
  assert.match(hb.lesson.content, /left, not right/);
  assert.doesNotMatch(hb.lesson.content, /increased 2,3-BPG, CO binding to some subunits/);
});


test("processing and catalysis reviews repair maturation order and ambiguous quiz distractors", () => {
  const p = applyLessonUpdates(processing.lesson, processing.questions);
  assert.match(p.questions.find(q => q.id === 62)!.choice_b, /formed in proinsulin/);
  assert.match(p.lesson.content, /dolichol-pyrophosphate-linked/);
  const e = applyLessonUpdates(catalysis.lesson, catalysis.questions);
  assert.match(e.lesson.content, /seventh class/);
  assert.match(e.lesson.content, /adenosylcobalamin/);
  assert.doesNotMatch(e.questions.find(q => q.id === 70)!.choice_c, /urea/);
  assert.match(e.questions.find(q => q.id === 67)!.question_text, /preserved global folding/);
});

test("kinetics review distinguishes binding affinity and fixes reciprocal-plot direction", () => {
  const m = applyLessonUpdates(models.lesson, models.questions);
  assert.match(m.lesson.content, /independent equilibrium assay measures substrate Kd/);
  assert.doesNotMatch(m.lesson.content, /Tables are acceptable markdown/);
  const k = applyLessonUpdates(kinetics.lesson, kinetics.questions);
  assert.match(k.lesson.content, /more negative \(leftward\)/);
  assert.match(k.lesson.content, /no inflection point/);
  assert.match(k.questions.find(q => q.id === 78)!.question_text, /min\/nmol/);
});

test("inhibition reviews keep intercept algebra and reversibility consistent", () => {
  const r = applyLessonUpdates(reciprocal.lesson, reciprocal.questions);
  assert.match(r.lesson.content, /x-intercept stays at −1\/Km/);
  assert.doesNotMatch(r.lesson.content, /if… actually no/);
  const i = applyLessonUpdates(inhibition.lesson, inhibition.questions);
  assert.match(i.lesson.content, /x-intercept shifts left/);
  assert.doesNotMatch(i.lesson.content, /permanently tied up/);
  assert.match(i.lesson.content, /quadrant II or III/);
});

test("cofactor and allostery reviews correct classification and missing comparison assumptions", () => {
  const c = applyLessonUpdates(cofactors.lesson, cofactors.questions);
  assert.match(c.lesson.content, /must not be delayed/);
  assert.match(c.questions.find(q => q.id === 92)!.question_text, /coenzyme and cosubstrate/);
  const a = applyLessonUpdates(allostery.lesson, allostery.questions);
  assert.match(a.lesson.content, /mixed T\/R subunits within one oligomer are excluded/);
  assert.match(a.questions.find(q => q.id === 98)!.question_text, /same Vmax and half-maximal/);
  assert.equal(a.questions.find(q => q.id === 100)!.choice_b, "Mixed inhibition with stronger inhibitor binding to free E than to ES.");
});


test("metabolic reviews distinguish species, actual free energy and respiratory pumps", () => {
  const r = applyLessonUpdates(regulation.lesson, regulation.questions);
  assert.match(r.questions.find(q => q.id === 105)!.question_text, /E. coli/);
  assert.doesNotMatch(r.lesson.content, /In mammals, a more complex arrangement/);
  assert.match(r.lesson.content, /not in intact chymotrypsinogen/);
  const e = applyLessonUpdates(energy.lesson, energy.questions);
  assert.match(e.lesson.content, /Complex II does not/);
  assert.match(e.lesson.content, /½\[ADP\]/);
  assert.match(e.questions.find(q => q.id === 108)!.question_text, /standard conditions/);
  assert.match(e.lesson.content, /not the CO₂ released in their first turn/);
});


test("glycolysis reviews repair ATP counts, tissue assumptions and analog experiment", () => {
  const g = applyLessonUpdates(glycolysis.lesson, glycolysis.questions);
  assert.match(g.lesson.content, /fluoride alone does not stop/);
  assert.doesNotMatch(g.lesson.content, /treats isolated hepatocytes/);
  const c = applyLessonUpdates(glycolyticControl.lesson, glycolyticControl.questions);
  assert.match(c.lesson.content, /not the committed step/);
  assert.match(c.lesson.content, /two ATP per glucose because two PEP/);
  assert.match(c.lesson.content, /LDH reaction consumes H⁺/);
  assert.doesNotMatch(c.questions.find(q => q.id === 116)!.question_text, /non-hydrolyzable/);
});

test("pyruvate and TCA reviews correct kinase direction, carbon accounting and shuttle direction", () => {
 const p = applyLessonUpdates(pdh.lesson, pdh.questions);
 assert.match(p.questions.find(q => q.id === 124)!.choice_a, /PDC is inhibited/);
 assert.match(p.questions.find(q => q.id === 125)!.choice_b, /Four carbons/);
 const t = applyLessonUpdates(tca.lesson, tca.questions);
 assert.match(t.lesson.content, /cytosolic MDH reduces OAA to malate/);
 assert.match(t.lesson.content, /α-ketoglutarate to D-2-hydroxyglutarate using NADPH/);
});

test("TCA and ETC reviews repair biosynthetic causality and proton accounting", () => {
 const a = applyLessonUpdates(amphibolic.lesson, amphibolic.questions);
 assert.match(a.lesson.content, /CPS II instead uses the amide nitrogen of glutamine/);
 assert.match(a.questions.find(q => q.id === 135)!.question_text, /ALA synthase/);
 const e = applyLessonUpdates(etc.lesson, etc.questions);
 assert.match(e.lesson.content, /4 \+ 4 \+ 2 = \*\*10 H⁺/);
 assert.match(e.lesson.content, /0 \+ 4 \+ 2 = \*\*6 H⁺/);
 assert.doesNotMatch(e.questions.find(q => q.id === 140)!.question_text, /irreversibly/);
 assert.match(e.lesson.content, /open \(allowing ATP release\)/);
});

test("ATP and fermentation reviews keep disease genetics and proton balance correct", () => {
 const a = applyLessonUpdates(atp.lesson, atp.questions);
 assert.match(a.lesson.content, /MT-TL1 mitochondrial tRNA/);
 assert.match(a.questions.find(q => q.id === 144)!.explanation, /consume ATP/);
 const f = applyLessonUpdates(fermentation.lesson, fermentation.questions);
 assert.doesNotMatch(f.lesson.content, /wait, let's be precise/);
 assert.doesNotMatch(f.lesson.content, /preventing pyruvate from entering/);
 assert.match(f.lesson.content, /4 ATP plus 2 GTP/);
 assert.match(f.lesson.content, /reaction itself consumes H⁺/);
});

test("fuel and gluconeogenesis reviews correct transport, isotope assumptions and duplicate answers", () => {
 const f = applyLessonUpdates(fuel.lesson, fuel.questions);
 assert.match(f.lesson.content, /Fatty acids can cross the blood–brain barrier/);
 assert.match(f.questions.find(q => q.id === 154)!.explanation, /does not donate an amino group directly/);
 const g = applyLessonUpdates(gng.lesson, gng.questions);
 assert.match(g.lesson.content, /consumes NAD⁺ and produces NADH/);
 assert.match(g.questions.find(q => q.id === 159)!.choice_c, /Lower F2,6BP/);
 assert.match(g.questions.find(q => q.id === 160)!.question_text, /one uniformly carbon-labeled/);
});


test("whole-body review distinguishes AMPK regulation and hepatic kinase response", () => {
 const r = applyLessonUpdates(homeostasis.lesson, homeostasis.questions);
 assert.ok(r.review);
 assert.doesNotMatch(r.lesson.content, /Akt phosphorylates the bifunctional/);
 assert.match(r.lesson.content, /ADP.*protect Thr172/);
 assert.match(r.questions.find(q => q.id === 164)!.choice_b, /fatty acids can enter the brain/);
 assert.match(r.questions.find(q => q.id === 165)!.explanation, /PKA activates phosphorylase kinase/);
});


test("DNA review separates chemical counts from whole-molecule behavior", () => {
 const r = applyLessonUpdates(dna.lesson, dna.questions);
 assert.ok(r.review);
 assert.match(r.lesson.content, /four carbons and one oxygen/);
 assert.match(r.lesson.content, /historical model/);
 assert.match(r.lesson.content, /may relax several turns/);
 assert.match(r.questions.find(q => q.id === 169)!.choice_b, /neighboring sequence/);
});


test("replication review corrects helicase polarity and restarts quiz key", () => {
 const r = applyLessonUpdates(replication.lesson, replication.questions);
 assert.ok(r.review);
 assert.match(r.lesson.content, /5′→3′.*lagging-strand template in/);
 assert.match(r.lesson.content, /CST-associated Pol α–primase/);
 assert.equal(r.questions.find(q => q.id === 172)!.correct_answer, "A");
 assert.match(r.questions.find(q => q.id === 174)!.choice_b, /ribonucleoside triphosphates/);
});


test("repair review scopes human UV repair and distinguishes primers from templates", () => {
 const r = applyLessonUpdates(repair.lesson, repair.questions);
 assert.ok(r.review);
 assert.match(r.lesson.content, /RNA polymerases can also proofread/);
 assert.match(r.lesson.content, /June 2024/);
 assert.match(r.questions.find(q => q.id === 178)!.question_text, /human cell/);
 assert.doesNotMatch(r.questions.find(q => q.id === 179)!.choice_b, /degraded/);
});


test("transcription review preserves strand direction and processing exceptions", () => {
  const result = applyLessonUpdates(transcription.lesson, transcription.questions);
  assert.ok(result.review);
  assert.match(result.lesson.content, /reverse-complemented/);
  assert.match(result.lesson.content, /Exons are sequences retained/);
  assert.match(result.lesson.content, /CPSF73 is the endonuclease/);
  assert.doesNotMatch(result.lesson.content, /sigma factor dissociates and can be reused/);
  assert.match(result.questions.find(q => q.id === 181)!.question_text, /core enzyme/);
  assert.match(result.questions.find(q => q.id === 183)!.choice_c, /Reduced TBP/);
});


test("RNA processing review resolves ambiguous splice outcomes and NMD distance", () => {
  const result = applyLessonUpdates(rnaProcessing.lesson, rnaProcessing.questions);
  assert.ok(result.review);
  assert.match(result.lesson.content, /79 canonical exons separated by 78 introns/);
  assert.match(result.lesson.content, /Measure this distance to the junction/);
  assert.match(result.lesson.content, /not an exonic-splicing-enhancer mutation/);
  assert.match(result.questions.find(q => q.id === 190)!.question_text, /sequencing/);
  assert.match(result.questions.find(q => q.id === 190)!.explanation, /can also cause exon skipping/);
});


test("genetic-code review fixes mischarged-tRNA key and charging accounting", () => {
 const r = applyLessonUpdates(geneticCode.lesson, geneticCode.questions);
 assert.equal(r.questions.find(q => q.id === 192)!.correct_answer, "A");
 assert.match(r.questions.find(q => q.id === 192)!.explanation, /physically attached/);
 assert.match(r.lesson.content, /one ATP molecule/);
 assert.match(r.lesson.content, /E. coli tRNA genes encode it/);
 assert.doesNotMatch(r.lesson.content, /initiation complex at the 30S subunit/);
});
test("translation review fixes relative motion and separates release from rescue", () => {
 const r = applyLessonUpdates(translation.lesson, translation.questions);
 assert.match(r.questions.find(q => q.id === 198)!.explanation, /opposite direction/);
 assert.match(r.questions.find(q => q.id === 200)!.question_text, /any rescue pathway/);
 assert.match(r.lesson.content, /phosphate release gated/);
 assert.match(r.lesson.content, /ATF4/);
});


test("targeting review separates glycosylation compartments and ubiquitin outcomes", () => {
 const r = applyLessonUpdates(proteinTargeting.lesson, proteinTargeting.questions);
 assert.match(r.lesson.content, /Collagen O-glycans are attached to hydroxylysine/);
 assert.match(r.lesson.content, /PTS2/);
 assert.match(r.lesson.content, /C-terminal tail, creating docking sites/);
 assert.match(r.questions.find(q => q.id === 203)!.question_text, /Lys48-linked/);
 assert.doesNotMatch(r.questions.find(q => q.id === 201)!.explanation, /no well-established alternative/);
});

 test("operon review fixes superrepressor key and retains attenuation after trpR loss", () => {
 const r = applyLessonUpdates(operons.lesson, operons.questions);
 assert.equal(r.questions.find(q => q.id === 206)!.correct_answer, "A");
 assert.match(r.questions.find(q => q.id === 208)!.choice_b, /still responds/);
 assert.match(r.questions.find(q => q.id === 210)!.question_text, /repressor occupies/);
 assert.match(r.lesson.content, /covers \*\*region 2\*\*/);
 assert.doesNotMatch(r.lesson.content, /regardless of lactose or glucose/);
 });

test("eukaryotic regulation review separates SMN genes and RNA-decay mechanisms", () => {
 const r = applyLessonUpdates(eukRegulation.lesson, eukRegulation.questions);
 assert.match(r.lesson.content, /SMN2 gene predominantly skips exon 7/);
 assert.match(r.lesson.content, /not an obligatory intermediate/);
 assert.match(r.lesson.content, /AGO3 also has guide-dependent/);
 assert.match(r.questions.find(q => q.id === 212)!.explanation, /4-fold/);
 assert.doesNotMatch(r.lesson.content, /predominant outcome is translational repression with partial/);
});

 test("Mendelian review distinguishes finite samples and distinct genotypes", () => {
 const r=applyLessonUpdates(mendelian.lesson,mendelian.questions);
 assert.ok(r.review);
 assert.match(r.lesson.content,/nine distinct two-locus genotypes/);
 assert.doesNotMatch(r.lesson.content,/reappears in exactly 1\/4/);
 assert.match(r.questions.find(q=>q.id===217)!.question_text,/no crossing over/);
 assert.match(r.questions.find(q=>q.id===218)!.explanation,/not 16 distinct genotypes/);
 });
