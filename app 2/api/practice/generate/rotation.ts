import { createHash, randomInt } from "node:crypto";
import { Pool } from "pg";
import { allocateSections, type Question, type Section, type sessionSettings } from "@/lib/practice";
import { starterQuestions } from "./starter";

type Settings = ReturnType<typeof sessionSettings>;
let pool: Pool | undefined;

async function lessonBank(section: Section): Promise<Question[]> {
  if (!process.env.POSTGRES_URL) return [];
  try {
    pool ??= new Pool({ connectionString: process.env.POSTGRES_URL, connectionTimeoutMillis: 2500, statement_timeout: 3500 });
    const result = await pool.query(
      `SELECT q.question_text, q.choice_a, q.choice_b, q.choice_c, q.choice_d,
              upper(trim(q.correct_answer)) AS correct_answer, q.explanation, l.title AS topic
       FROM study_lesson_questions q JOIN study_lessons l ON l.id=q."lessonId"
       JOIN study_units u ON u.id=l."unitId" WHERE u.section=$1`, [section]);
    return result.rows.filter(q => ["A","B","C","D"].includes(q.correct_answer) &&
      [q.question_text,q.choice_a,q.choice_b,q.choice_c,q.choice_d,q.explanation].every(x => typeof x === "string" && x.trim()))
      .map(q => ({ ...q, section, difficulty: "unrated", wrongAnswerExplanations: {} }));
  } catch { return []; }
}

export function fresh(items: Question[], seen: Set<string>, count: number) {
  const selected: Question[] = [];
  for (const q of items) {
    if (selected.length >= count) break;
    const stem = q.question_text.split("\n\n").at(-1) || q.question_text;
    const text = stem.toLowerCase().normalize("NFKC").replace(/[^\p{L}\p{N}]+/gu," ").trim();
    const id = createHash("sha256").update(text).digest("hex").slice(0,24);
    if (seen.has(id)) continue;
    seen.add(id);
    selected.push({ ...q, id });
  }
  return selected;
}

export async function reserveQuestions(settings: Settings, seen: Set<string>, needed: number, section: Section) {
  const items = starterQuestions(section, settings.format, settings.difficulty);
  if (settings.format === "standalone" && section !== "cars" && settings.difficulty === "mixed")
    items.push(...await lessonBank(section));
  for (let i=items.length-1; i>0; i--) {
    const j=randomInt(i+1);
    [items[i],items[j]]=[items[j],items[i]];
  }
  return fresh(items,seen,needed);
}

export async function reserveResponse(settings: Settings, seen: Set<string>) {
  const batches = await Promise.all(allocateSections(settings.section, settings.count)
    .map(g => reserveQuestions(settings,seen,g.count,g.section)));
  const questions=batches.flat();
  return Response.json({source:"starter", questions, exhausted:questions.length===0, section:settings.section});
}
