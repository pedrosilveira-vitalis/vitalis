import { createHash } from "node:crypto";
import acidBase from "./lesson-updates/amino-acid-acid-base.json";
import structure from "./lesson-updates/amino-acid-structure.json";
import classification from "./lesson-updates/amino-acid-classification.json";

import peptide from "./lesson-updates/peptide-bonds.json";
import secondary from "./lesson-updates/protein-secondary.json";

import assembly from "./lesson-updates/protein-assembly.json";
import stability from "./lesson-updates/protein-stability.json";

import binding from "./lesson-updates/protein-binding.json";
import hemoglobin from "./lesson-updates/hemoglobin-binding.json";

import processing from "./lesson-updates/protein-processing.json";
import catalysis from "./lesson-updates/enzyme-catalysis.json";

import models from "./lesson-updates/binding-models.json";
import kinetics from "./lesson-updates/enzyme-kinetics.json";

import reciprocal from "./lesson-updates/reciprocal-plots.json";
import inhibition from "./lesson-updates/inhibition-models.json";

import cofactors from "./lesson-updates/cofactor-roles.json";
import allostery from "./lesson-updates/allosteric-models.json";

import regulation from "./lesson-updates/metabolic-regulation.json";
import energy from "./lesson-updates/bioenergetics-overview.json";

import glycolysis from "./lesson-updates/glycolysis-pathway.json";
import glycolyticControl from "./lesson-updates/glycolysis-regulation.json";

import pdh from "./lesson-updates/pyruvate-oxidation.json";
import tca from "./lesson-updates/citric-acid-cycle.json";

import amphibolic from "./lesson-updates/tca-amphibolic.json";
import etc from "./lesson-updates/electron-transport.json";

import atp from "./lesson-updates/atp-synthase.json";
import fermentation from "./lesson-updates/fermentation.json";

import fuel from "./lesson-updates/fuel-integration.json";
import gng from "./lesson-updates/gluconeogenesis.json";

import homeostasis from "./lesson-updates/whole-body-homeostasis.json";

import dna from "./lesson-updates/dna-structure.json";

import replication from "./lesson-updates/dna-replication.json";

import repair from "./lesson-updates/dna-repair.json";

import transcription from "./lesson-updates/transcription.json";

import rnaProcessing from "./lesson-updates/rna-processing.json";

import geneticCode from "./lesson-updates/genetic-code.json";
import translation from "./lesson-updates/translation.json";

import proteinTargeting from "./lesson-updates/protein-targeting.json";

import operons from "./lesson-updates/bacterial-operons.json";

import eukRegulation from "./lesson-updates/eukaryotic-regulation.json";

type Row = { id: number; [key: string]: unknown };
const reviews = [structure, classification, acidBase, peptide, secondary, assembly, stability, binding, hemoglobin, processing, catalysis, models, kinetics, reciprocal, inhibition, cofactors, allostery, regulation, energy, glycolysis, glycolyticControl, pdh, tca, amphibolic, etc, atp, fermentation, fuel, gng, homeostasis, dna, replication, repair, transcription, rnaProcessing, geneticCode, translation, proteinTargeting, operons, eukRegulation];
export function applyLessonUpdates<L extends Row, Q extends Row>(lesson: L, questions: Q[]) {
  const reviewed = reviews.find(entry => entry.lessonId === lesson.id);
  if (!reviewed) return { lesson, questions, review: null };
  // Reject additions, removals and duplicate question IDs as well as changed fields.
  const ids = new Set(questions.map(q => q.id));
  if (questions.length !== reviewed.questionIds.length || ids.size !== questions.length ||
      reviewed.questionIds.some(id => !ids.has(id))) {
    console.warn("Lesson review skipped: question set changed", lesson.id);
    return { lesson, questions, review: null };
  }
  const updatedLesson = { ...lesson };
  const updatedQuestions = questions.map(q => ({ ...q }));
  // All-or-nothing: never mix revised answer choices with an old answer key.
  for (const update of reviewed.guards) {
    const parts = update.field.split(".");
    const target = parts[0] === "lesson" ? updatedLesson : updatedQuestions.find(q => q.id === Number(parts[1]));
    const key = parts[0] === "lesson" ? parts[1] : parts[2];
    const value = target?.[key];
    if (typeof value !== "string" || createHash("sha256").update(value).digest("hex") !== update.sha256) {
      console.warn("Lesson review skipped: source changed", lesson.id, update.field);
      return { lesson, questions, review: null };
    }
  }
  for (const update of reviewed.updates) {
    const parts = update.field.split(".");
    const target: Row = parts[0] === "content" ? updatedLesson : updatedQuestions.find(q => q.id === Number(parts[1]))!;
    target[parts[0] === "content" ? "content" : parts[2]] = update.value;
  }
  return { lesson: updatedLesson, questions: updatedQuestions, review: { reviewedAt: reviewed.reviewedAt, sources: reviewed.sources, visual: reviewed.visual } };
}
