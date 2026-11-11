// Regenerates lib/lesson-reviews/index.ts from the lesson-NNN.json files in that folder.
import { readdirSync, writeFileSync } from "node:fs";
const dir = new URL("../lib/lesson-reviews/", import.meta.url);
const files = readdirSync(dir).filter(f => /^lesson-\d+\.json$/.test(f)).sort();
const lines = ['import type { PatchReview } from "../lesson-patches";'];
files.forEach((f, i) => lines.push(`import r${i} from "./${f}";`));
lines.push("", `export const patchReviews: PatchReview[] = [${files.map((_, i) => `r${i}`).join(", ")}];`, "");
writeFileSync(new URL("index.ts", dir), lines.join("\n"));
console.log(`Indexed ${files.length} reviews`);
