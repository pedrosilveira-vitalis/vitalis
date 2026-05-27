/**
 * Vitalis Study Guide Generator
 *
 * Phase 1 (--titles): Generate lesson titles for each unit. Saves to scripts/lesson-titles.json.
 * Phase 2 (--lessons): Read titles, generate full lessons + 5 questions, save to DB. Resumable.
 * Phase 3 (--unit-tests): Generate 15-question unit tests for each unit.
 *
 * Usage:
 *   npx tsx scripts/generate-lessons.ts --titles
 *   npx tsx scripts/generate-lessons.ts --lessons
 *   npx tsx scripts/generate-lessons.ts --unit-tests
 */

import Anthropic from "@anthropic-ai/sdk";
import { Pool } from "pg";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { config } from "dotenv";

config({ path: ".env.local" });

const TITLES_FILE = "scripts/lesson-titles.json";
const PROGRESS_FILE = "scripts/generation-progress.json";

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
const pool = new Pool({
  connectionString: process.env.POSTGRES_URL,
  ssl: { rejectUnauthorized: false },
});

const LESSONS_PER_UNIT_TARGET: Record<string, Record<number, number>> = {
  "bio-biochem": { 1: 10, 2: 8, 3: 12, 4: 10, 5: 9, 6: 10, 7: 15, 8: 6, 9: 5 },
  "chem-phys": { 1: 8, 2: 10, 3: 8, 4: 15, 5: 5, 6: 10, 7: 10, 8: 9 },
  "psych-soc": { 1: 8, 2: 10, 3: 8, 4: 10, 5: 8, 6: 10, 7: 10, 8: 6 },
  "cars": { 1: 6, 2: 8, 3: 6 },
};

type Unit = {
  id: number;
  section: string;
  unit_number: number;
  title: string;
  description: string;
};

type LessonTitle = {
  unitId: number;
  section: string;
  unitTitle: string;
  lessonNumber: number;
  title: string;
  description: string;
};

type Progress = {
  titlesGenerated: boolean;
  lessonsCompleted: number[];
  unitTestsCompleted: number[];
};

function loadProgress(): Progress {
  if (existsSync(PROGRESS_FILE)) {
    return JSON.parse(readFileSync(PROGRESS_FILE, "utf-8"));
  }
  return { titlesGenerated: false, lessonsCompleted: [], unitTestsCompleted: [] };
}

function saveProgress(p: Progress) {
  writeFileSync(PROGRESS_FILE, JSON.stringify(p, null, 2));
}

function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

async function callClaude(systemPrompt: string, userPrompt: string, maxRetries = 3): Promise<string> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await client.messages.create({
        model: "claude-sonnet-4-6",
        max_tokens: 8000,
        system: systemPrompt,
        messages: [{ role: "user", content: userPrompt }],
        temperature: 0.7,
      });
      const text = response.content
        .filter((b) => b.type === "text")
        .map((b) => (b.type === "text" ? b.text : ""))
        .join("\n")
        .trim();
      return text;
    } catch (error: unknown) {
      const err = error as { status?: number; message?: string };
      console.error(`  Attempt ${attempt}/${maxRetries} failed:`, err.message || error);
      if (attempt < maxRetries) {
        const wait = attempt * 5000;
        console.log(`  Waiting ${wait / 1000}s before retry...`);
        await sleep(wait);
      } else {
        throw error;
      }
    }
  }
  throw new Error("All retries exhausted");
}

async function generateTitles() {
  console.log("\n=== PHASE 1: GENERATING LESSON TITLES ===\n");
  const progress = loadProgress();
  if (progress.titlesGenerated && existsSync(TITLES_FILE)) {
    console.log("Titles already generated. Delete scripts/lesson-titles.json to regenerate.");
    return;
  }

  const unitsRes = await pool.query<Unit>(
    `SELECT id, section, unit_number, title, description FROM study_units ORDER BY section, unit_number`
  );
  const units = unitsRes.rows;
  const allTitles: LessonTitle[] = [];

  for (const unit of units) {
    const targetCount = LESSONS_PER_UNIT_TARGET[unit.section]?.[unit.unit_number] || 8;
    console.log(`Generating ${targetCount} titles for ${unit.section} / ${unit.title}...`);

    const systemPrompt = "You are an expert MCAT curriculum designer. Generate lesson titles for the AAMC content outline at college level.";
    const userPrompt = [
      `Section: ${unit.section}`,
      `Unit: ${unit.title}`,
      `Unit description: ${unit.description}`,
      ``,
      `Generate exactly ${targetCount} lesson titles for this unit. Each lesson should cover one specific, focused topic students need to master.`,
      `Topics should progress logically from foundational to more advanced within the unit.`,
      `Each lesson should be ~3,000-4,000 words of college-level content when written out.`,
      ``,
      `Return ONLY valid JSON, no markdown fences:`,
      `[`,
      `  {"title": "Lesson title here", "description": "One-sentence description of what this lesson covers"},`,
      `  ...`,
      `]`,
    ].join("\n");

    try {
      const response = await callClaude(systemPrompt, userPrompt);
      const firstBracket = response.indexOf("[");
      const lastBracket = response.lastIndexOf("]");
      const jsonStr = firstBracket !== -1 && lastBracket > firstBracket
        ? response.substring(firstBracket, lastBracket + 1)
        : response;
      const parsed = JSON.parse(jsonStr);
      const titles = parsed.slice(0, targetCount);
      titles.forEach((t: { title: string; description: string }, i: number) => {
        allTitles.push({
          unitId: unit.id,
          section: unit.section,
          unitTitle: unit.title,
          lessonNumber: i + 1,
          title: t.title,
          description: t.description,
        });
      });
      console.log(`  ✓ ${titles.length} titles generated`);
      await sleep(1500);
    } catch (error) {
      console.error(`  ✗ Failed to generate titles for ${unit.title}:`, error);
      throw error;
    }
  }

  writeFileSync(TITLES_FILE, JSON.stringify(allTitles, null, 2));
  console.log(`\n✓ All ${allTitles.length} titles saved to ${TITLES_FILE}`);
  console.log(`\nREVIEW the file. When happy, run: npx tsx scripts/generate-lessons.ts --lessons`);

  progress.titlesGenerated = true;
  saveProgress(progress);
}

async function generateLessons() {
  console.log("\n=== PHASE 2: GENERATING FULL LESSONS ===\n");
  if (!existsSync(TITLES_FILE)) {
    console.error("No titles file. Run --titles first.");
    return;
  }

  const titles: LessonTitle[] = JSON.parse(readFileSync(TITLES_FILE, "utf-8"));
  const progress = loadProgress();
  console.log(`Resume mode: ${progress.lessonsCompleted.length} lessons already done.`);

  const contentSystemPrompt = [
    "You are an expert MCAT tutor and college-level science writer creating premium study guide content.",
    "",
    "Your task: write a complete, college-level lesson on a specific MCAT topic.",
    "",
    "RULES:",
    "- Length: 3000-4000 words.",
    "- Use markdown: ## for section headers, ### for subsections, **bold** for key terms, *italics* for emphasis, bullet points (- ) for lists.",
    "- College-level prose. Direct, clear, no fluff.",
    "- Include numerical specifics (pKa values, ATP yields, etc.) where students need them.",
    "- Connect to MCAT relevance.",
    "- DO NOT use SVG, HTML tags, code blocks (no triple backticks), or any non-markdown formatting.",
    "- Output ONLY the lesson content as plain markdown. No JSON, no metadata, no preamble. Start directly with the lesson.",
  ].join("\n");

  const questionsSystemPrompt = [
    "You are an expert MCAT writer creating check-your-understanding questions.",
    "",
    "Generate 5 multiple-choice questions for a specific MCAT lesson.",
    "Each question tests application/reasoning, not memorization. AAMC-style.",
    "",
    "OUTPUT FORMAT: return ONLY a valid JSON array. No prose before or after.",
    "Use this exact structure:",
    "[",
    "  {",
    '    "question_text": "...",',
    '    "choice_a": "...", "choice_b": "...", "choice_c": "...", "choice_d": "...",',
    '    "correct_answer": "A",',
    '    "explanation": "3-5 sentence explanation of correct answer + most tempting wrong answer"',
    "  }",
    "]",
    "",
    "Keep all strings simple. No newlines inside strings, no special characters needing escape.",
  ].join("\n");

  let i = 0;
  for (const t of titles) {
    i++;
    const lessonKey = t.unitId * 1000 + t.lessonNumber;
    if (progress.lessonsCompleted.includes(lessonKey)) {
      console.log(`[${i}/${titles.length}] SKIP (already done): ${t.title}`);
      continue;
    }

    console.log(`[${i}/${titles.length}] Generating: ${t.section} / ${t.unitTitle} / ${t.title}`);

    try {
      const contentPrompt = [
        `Section: ${t.section}`,
        `Unit: ${t.unitTitle}`,
        `Lesson title: ${t.title}`,
        `Lesson description: ${t.description}`,
        ``,
        `Write the full lesson content as plain markdown. 3000-4000 words.`,
      ].join("\n");

      const content = await callClaude(contentSystemPrompt, contentPrompt);

      if (!content || content.length < 500) {
        console.error(`  ✗ Content too short for "${t.title}"`);
        continue;
      }

      const questionsPrompt = [
        `Lesson title: ${t.title}`,
        `Lesson description: ${t.description}`,
        ``,
        `Generate 5 multiple-choice questions testing the main concepts of this lesson.`,
        `Return ONLY the JSON array.`,
      ].join("\n");

      const questionsRaw = await callClaude(questionsSystemPrompt, questionsPrompt);
      let questions: Array<{
        question_text: string;
        choice_a: string;
        choice_b: string;
        choice_c: string;
        choice_d: string;
        correct_answer: string;
        explanation: string;
      }>;
      try {
        const firstBracket = questionsRaw.indexOf("[");
        const lastBracket = questionsRaw.lastIndexOf("]");
        const jsonStr = firstBracket !== -1 && lastBracket > firstBracket
          ? questionsRaw.substring(firstBracket, lastBracket + 1)
          : questionsRaw;
        questions = JSON.parse(jsonStr);
      } catch (e) {
        console.error(`  ✗ Could not parse questions for "${t.title}":`, e);
        continue;
      }

      if (!Array.isArray(questions) || questions.length < 5) {
        console.error(`  ✗ Expected 5 questions, got ${questions?.length}`);
        continue;
      }

      const wordCount = content.split(/\s+/).length;
      const estimatedMinutes = Math.max(10, Math.round(wordCount / 200));

      const lessonRes = await pool.query(
        `INSERT INTO study_lessons ("unitId", lesson_number, title, description, content, estimated_minutes)
         VALUES ($1, $2, $3, $4, $5, $6)
         RETURNING id`,
        [t.unitId, t.lessonNumber, t.title, t.description, content, estimatedMinutes]
      );
      const lessonId = lessonRes.rows[0].id;

      for (let qi = 0; qi < 5; qi++) {
        const q = questions[qi];
        await pool.query(
          `INSERT INTO study_lesson_questions ("lessonId", question_number, question_text, choice_a, choice_b, choice_c, choice_d, correct_answer, explanation)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
          [lessonId, qi + 1, q.question_text, q.choice_a, q.choice_b, q.choice_c, q.choice_d, q.correct_answer, q.explanation]
        );
      }

      progress.lessonsCompleted.push(lessonKey);
      saveProgress(progress);
      console.log(`  ✓ saved (lesson id ${lessonId}, ${wordCount} words, ${estimatedMinutes} min)`);
      await sleep(2000);
    } catch (error) {
      console.error(`  ✗ Failed for "${t.title}":`, error);
      await sleep(5000);
    }
  }

  console.log(`\n✓ Lesson generation complete. ${progress.lessonsCompleted.length} lessons in database.`);
}

async function generateUnitTests() {
  console.log("\n=== PHASE 3: GENERATING UNIT TESTS ===\n");
  const progress = loadProgress();

  const unitsRes = await pool.query<Unit>(
    `SELECT id, section, unit_number, title, description FROM study_units ORDER BY section, unit_number`
  );

  const systemPrompt = "You are an expert MCAT writer creating a comprehensive unit assessment.";

  for (const unit of unitsRes.rows) {
    if (progress.unitTestsCompleted.includes(unit.id)) {
      console.log(`SKIP unit ${unit.id} (already done)`);
      continue;
    }

    console.log(`Generating unit test for ${unit.section} / ${unit.title}...`);

    const lessonsRes = await pool.query(
      `SELECT title, description FROM study_lessons WHERE "unitId" = $1 ORDER BY lesson_number`,
      [unit.id]
    );

    const userPrompt = [
      `Section: ${unit.section}`,
      `Unit: ${unit.title}`,
      `Unit description: ${unit.description}`,
      ``,
      `Lessons in this unit:`,
      ...lessonsRes.rows.map((l, i) => `${i + 1}. ${l.title} — ${l.description}`),
      ``,
      `Generate 15 multiple-choice questions testing the MOST IMPORTANT concepts across these lessons. Mix difficulty (4 easy, 7 medium, 4 hard).`,
      `Questions should integrate ideas across lessons where natural. AAMC-style, application-focused, not trivia.`,
      `Keep all strings simple. No newlines inside strings.`,
      ``,
      `Return ONLY a valid JSON array of 15 questions, no prose before or after:`,
      `[`,
      `  {`,
      `    "question_text": "...",`,
      `    "choice_a": "...", "choice_b": "...", "choice_c": "...", "choice_d": "...",`,
      `    "correct_answer": "A",`,
      `    "explanation": "..."`,
      `  }`,
      `]`,
    ].join("\n");

    try {
      const response = await callClaude(systemPrompt, userPrompt);
      const firstBracket = response.indexOf("[");
      const lastBracket = response.lastIndexOf("]");
      const jsonStr = firstBracket !== -1 && lastBracket > firstBracket
        ? response.substring(firstBracket, lastBracket + 1)
        : response;
      const questions = JSON.parse(jsonStr);

      if (!Array.isArray(questions) || questions.length < 15) {
        console.error(`  ✗ Expected 15 questions, got ${questions?.length}`);
        continue;
      }

      for (let qi = 0; qi < 15; qi++) {
        const q = questions[qi];
        await pool.query(
          `INSERT INTO study_unit_questions ("unitId", question_number, question_text, choice_a, choice_b, choice_c, choice_d, correct_answer, explanation)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
          [unit.id, qi + 1, q.question_text, q.choice_a, q.choice_b, q.choice_c, q.choice_d, q.correct_answer, q.explanation]
        );
      }

      progress.unitTestsCompleted.push(unit.id);
      saveProgress(progress);
      console.log(`  ✓ 15 questions saved`);
      await sleep(2000);
    } catch (error) {
      console.error(`  ✗ Failed:`, error);
      await sleep(5000);
    }
  }
  console.log(`\n✓ Unit tests complete.`);
}

async function main() {
  const arg = process.argv[2];
  try {
    if (arg === "--titles") await generateTitles();
    else if (arg === "--lessons") await generateLessons();
    else if (arg === "--unit-tests") await generateUnitTests();
    else {
      console.log("Usage:");
      console.log("  npx tsx scripts/generate-lessons.ts --titles");
      console.log("  npx tsx scripts/generate-lessons.ts --lessons");
      console.log("  npx tsx scripts/generate-lessons.ts --unit-tests");
    }
  } finally {
    await pool.end();
  }
}

main();