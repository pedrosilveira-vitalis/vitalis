export type SectionId = "bio-biochem" | "chem-phys" | "psych-soc" | "cars";

export type Block =
  | { kind: "list"; heading: string; items: string[] }
  | { kind: "formulas"; heading: string; items: { label: string; formula: string; note?: string }[] }
  | { kind: "table"; heading: string; columns: string[]; rows: string[][] }
  | { kind: "trap"; heading: string; items: string[] };

export interface CheatSheet {
  unitId: number;
  section: SectionId;
  unit: string;
  summary: string;
  blocks: Block[];
}
