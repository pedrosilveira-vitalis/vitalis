import { createHash, randomInt } from "node:crypto";
import { Pool } from "pg";
import { sections, type Question, type Section, type sessionSettings } from "@/lib/practice";
import { starterQuestions } from "./starter";
import supplement from "./foundation.json";

type Settings = ReturnType<typeof sessionSettings>;
type Entry = Question & { variant?: boolean; family: string; mode: "guide" | "both" | "passage" };
const hash = (s: string) => createHash("sha256").update(s).digest("hex").slice(0,24);
function stemKey(stem: string) {
  return hash(stem.toLowerCase().normalize("NFKC").replace(/[^\p{L}\p{N}]+/gu, " ").trim());
}
const fixed: Entry[] = sections.flatMap(section =>
  starterQuestions(section, "passage", "mixed").map(q => ({ ...q, id: stemKey(q.question_text), family: q.topic, mode: section === "cars" ? "passage" as const : "both" as const })));
for (const q of supplement) fixed.push({ ...q, mode: q.section === "cars" ? "passage" : "both" });

let pool: Pool | undefined;
let cache: { rows: Entry[]; until: number; connected: boolean } | undefined;
let pending: Promise<NonNullable<typeof cache>> | undefined;
async function readCatalog() {
  let rows: Entry[] = [];
  let connected = false;
  if (process.env.POSTGRES_URL) {
    try {
      pool ??= new Pool({ connectionString: process.env.POSTGRES_URL, connectionTimeoutMillis: 3000, statement_timeout: 5000 });
      const result = await pool.query(`
        SELECT q.question_text, q.choice_a, q.choice_b, q.choice_c, q.choice_d, q.correct_answer, q.explanation, l.title AS topic, u.section
        FROM study_lesson_questions q JOIN study_lessons l ON l.id=q."lessonId" JOIN study_units u ON u.id=l."unitId"
        UNION ALL
        SELECT q.question_text, q.choice_a, q.choice_b, q.choice_c, q.choice_d, q.correct_answer, q.explanation, u.title AS topic, u.section
        FROM study_unit_questions q JOIN study_units u ON u.id=q."unitId"`);
      const known = new Set(fixed.map(q => stemKey(q.question_text)));
      for (const q of result.rows) {
        const choices = [q.choice_a,q.choice_b,q.choice_c,q.choice_d];
        if (!sections.includes(q.section) || ![q.question_text,q.explanation,...choices].every(x => typeof x === "string" && x.trim())) continue;
        const answer=String(q.correct_answer).trim().toUpperCase(), id=stemKey(q.question_text);
        if (!"ABCD".split("").includes(answer) || known.has(id) || new Set(choices.map(x=>x.trim().toLowerCase())).size!==4) continue;
        known.add(id);
        rows.push({...q,id,correct_answer:answer,difficulty:"unrated",family:q.topic,mode:"guide",wrongAnswerExplanations:{}});
      }
      connected = true;
    } catch { console.warn("Practice guide bank unavailable"); }
  }
  cache = { rows: [...fixed,...rows], connected, until: Date.now()+(connected ? 60000 : 10000) };
  return cache;
}

export async function catalog() {
  if (cache && cache.until > Date.now()) return cache;
  pending ??= readCatalog().finally(()=>{pending=undefined;});
  return pending;
}

export function fresh(items: Question[], seen: Set<string>, count: number) {
  const result: Question[] = [];
  for (const q of items) {
    const id=stemKey(q.question_text);
    if (seen.has(id) || seen.has(stemKey(q.question_text.split("\n\n").at(-1) || q.question_text))) continue;
    result.push({...q,id}); seen.add(id);
    if (result.length===count) break;
  }
  return result;
}

export async function reserveQuestions(settings: Settings, seen: Set<string>, needed: number, section: Section) {
  const {rows} = await catalog();
  const recent = new Map([...seen].map((id,index)=>[id,index]));
  const last = new Map<string,number>();
  const groups = new Map<string,Entry[]>();
  for (const q of rows) {
    if (q.section !== section) continue;
    const index=recent.get(q.id);
    if (index !== undefined) { last.set(q.family,Math.max(index,last.get(q.family) ?? -1)); continue; }
    if (settings.format==="drills" && !q.variant) continue;
    if (settings.difficulty !== "mixed" && q.difficulty !== settings.difficulty) continue;
    if (settings.format==="guide" ? q.mode !== "guide" : q.mode==="guide" && (settings.format==="passage" || section==="cars")) continue;
    if (!groups.has(q.family)) groups.set(q.family,[]);
    groups.get(q.family)!.push(q);
  }
  const order=[...groups.keys()].filter(family=>settings.format==="drills" || !groups.get(family)![0].variant || !last.has(family));
  for(let i=order.length-1;i>0;i--){const j=randomInt(i+1);[order[i],order[j]]=[order[j],order[i]];}
  order.sort((a,b)=>(last.get(a)??-1)-(last.get(b)??-1));
  const result: Question[]=[];
  while (order.length && result.length<needed) {
    const family=order.shift()!, group=groups.get(family)!;
    const [q]=group.splice(randomInt(group.length),1);
    const inline=(settings.format==="standalone" || settings.format==="drills") && section!=="cars" && q.passage;
    result.push({...q,question_text:inline ? q.passage!.content+"\n\n"+q.question_text : q.question_text,passage:inline ? undefined : q.passage});
    seen.add(q.id);
    if(group.length && (!q.variant || settings.format==="drills")) order.push(family);
  }
  return result;
}
