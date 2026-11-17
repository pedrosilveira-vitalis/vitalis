/**
 * One-page cheat sheets, one per unit.
 *
 * Content lives here rather than in the database because these are editorial
 * documents, not user data: they are reviewed, versioned and diffed like the
 * lessons are. A unit with no sheet yet simply has no entry, and the UI says so
 * rather than rendering an empty page.
 */
import { BIO_BIOCHEM } from "./sheets/bio-biochem";
import { CHEM_PHYS } from "./sheets/chem-phys";
import { PSYCH_SOC } from "./sheets/psych-soc";
import { CARS } from "./sheets/cars";
import type { Block, CheatSheet, SectionId } from "./sheets/types";

export type { Block, CheatSheet, SectionId };

export const CHEAT_SHEETS: CheatSheet[] = [...BIO_BIOCHEM, ...CHEM_PHYS, ...PSYCH_SOC, ...CARS];

export interface SectionMeta {
  id: SectionId;
  name: string;
  short: string;
  blurb: string;
  accent: string;
  tint: string;
  prop: "flask" | "cell" | "brain" | "book";
}

export const SECTIONS: SectionMeta[] = [
  {
    id: "bio-biochem",
    name: "Biology & Biochemistry",
    short: "Bio / Biochem",
    blurb: "Nine units, from amino acids to microbes.",
    accent: "#5b7a64",
    tint: "#e5ece3",
    prop: "cell",
  },
  {
    id: "chem-phys",
    name: "Chemistry & Physics",
    short: "Chem / Phys",
    blurb: "Eight units, from pKa to circuits.",
    accent: "#245574",
    tint: "#e6edf1",
    prop: "flask",
  },
  {
    id: "psych-soc",
    name: "Psychology & Sociology",
    short: "Psych / Soc",
    blurb: "Eight units, from conditioning to statistics.",
    accent: "#a8324a",
    tint: "#f2e4e4",
    prop: "brain",
  },
  {
    id: "cars",
    name: "Critical Analysis & Reasoning",
    short: "CARS",
    blurb: "Three units. No content to memorise, only method.",
    accent: "#987740",
    tint: "#f1eadc",
    prop: "book",
  },
];

export function sectionMeta(id: string): SectionMeta | undefined {
  return SECTIONS.find(section => section.id === id);
}

/** Every unit, so the index can show what exists and what is still to come. */
export const UNITS: { id: number; section: SectionId; number: number; title: string }[] = [
  { id: 1, section: "bio-biochem", number: 1, title: "Biochemistry Foundations" },
  { id: 2, section: "bio-biochem", number: 2, title: "Enzymes" },
  { id: 3, section: "bio-biochem", number: 3, title: "Cellular Metabolism" },
  { id: 4, section: "bio-biochem", number: 4, title: "Molecular Biology" },
  { id: 5, section: "bio-biochem", number: 5, title: "Genetics" },
  { id: 6, section: "bio-biochem", number: 6, title: "Cell Biology" },
  { id: 7, section: "bio-biochem", number: 7, title: "Physiology" },
  { id: 8, section: "bio-biochem", number: 8, title: "Immunology" },
  { id: 9, section: "bio-biochem", number: 9, title: "Microbiology" },
  { id: 10, section: "chem-phys", number: 1, title: "Acid-Base Chemistry" },
  { id: 11, section: "chem-phys", number: 2, title: "Thermodynamics & Kinetics" },
  { id: 12, section: "chem-phys", number: 3, title: "Solutions & Equilibrium" },
  { id: 13, section: "chem-phys", number: 4, title: "Organic Chemistry" },
  { id: 14, section: "chem-phys", number: 5, title: "Electrochemistry" },
  { id: 15, section: "chem-phys", number: 6, title: "Mechanics" },
  { id: 16, section: "chem-phys", number: 7, title: "Fluids, Waves & Optics" },
  { id: 17, section: "chem-phys", number: 8, title: "Electricity & Magnetism" },
  { id: 18, section: "psych-soc", number: 1, title: "Learning & Conditioning" },
  { id: 19, section: "psych-soc", number: 2, title: "Cognition & Memory" },
  { id: 20, section: "psych-soc", number: 3, title: "Sensation & Perception" },
  { id: 21, section: "psych-soc", number: 4, title: "Emotion, Motivation, Personality" },
  { id: 22, section: "psych-soc", number: 5, title: "Psychological Disorders" },
  { id: 23, section: "psych-soc", number: 6, title: "Social Psychology" },
  { id: 24, section: "psych-soc", number: 7, title: "Sociology & Demographics" },
  { id: 25, section: "psych-soc", number: 8, title: "Research Methods & Statistics" },
  { id: 26, section: "cars", number: 1, title: "Reading Strategy" },
  { id: 27, section: "cars", number: 2, title: "Question Types & Approach" },
  { id: 28, section: "cars", number: 3, title: "Passage Genres & Practice" },
];

export function unitsFor(section: string) {
  return UNITS.filter(unit => unit.section === section).sort((a, b) => a.number - b.number);
}

export function sheetsFor(section: string): CheatSheet[] {
  return CHEAT_SHEETS.filter(sheet => sheet.section === section);
}

export function sheetFor(section: string, unitId: number): CheatSheet | undefined {
  return CHEAT_SHEETS.find(sheet => sheet.section === section && sheet.unitId === unitId);
}
