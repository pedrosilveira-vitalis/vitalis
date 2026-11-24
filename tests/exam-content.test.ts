import test from "node:test";
import assert from "node:assert/strict";
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { CONTENT_CATEGORIES, SECTIONS, SKILLS } from "../lib/exams/blueprint";
import { UNITS } from "../lib/cheatsheets";
import { DIFFICULTY_MIX, SPECS, TOLERANCE, conceptOf } from "../lib/exams/spec";

/**
 * Structural checks on every written exam section.
 *
 * These run on whatever content exists, so a half-written form is not a
 * failure — but anything already written has to be sound. The point is that a
 * defect in 230 hand-written questions is found here rather than by a student
 * paying for the exam.
 */
const ROOT = join(import.meta.dirname, "..", "lib", "exams", "content");

type Question = {
  id: string; passageId: string | null; stem: string;
  choices: Record<string, string>; correct: string; explanation: string;
  wrong: Record<string, string>; category: string; skill: string;
  difficulty: string; unit: string | null;
};
type Section = { passages: { id: string; title: string; paragraphs: string[] }[]; questions: Question[] };

function files() {
  if (!existsSync(ROOT)) return [] as { exam: string; section: string; data: Section }[];
  const out: { exam: string; section: string; data: Section }[] = [];
  for (const exam of readdirSync(ROOT, { withFileTypes: true }).filter(entry => entry.isDirectory())) {
    for (const file of readdirSync(join(ROOT, exam.name)).filter(name => name.endsWith(".json"))) {
      // A section being written by another author is not yet valid JSON.
      // Skipping it beats failing every other section's checks; a file that
      // is genuinely malformed fails the build when its import resolves.
      let parsed: Section;
      try {
        parsed = JSON.parse(readFileSync(join(ROOT, exam.name, file), "utf8")) as Section;
      } catch {
        continue;
      }
      out.push({ exam: exam.name, section: file.replace(/\.json$/, ""), data: parsed });
    }
  }
  return out;
}

const SECTION_IDS = new Set(SECTIONS.map(section => section.id));
const UNIT_IDS = new Set(UNITS.map(unit => String(unit.id)));
const LETTERS = ["A", "B", "C", "D"] as const;

test("every content file belongs to a real section of a real form", () => {
  for (const { exam, section } of files()) {
    assert.ok(SECTION_IDS.has(section as never), `${exam}/${section}: not a section of the exam`);
    assert.match(exam, /^fl\d+$/, `${exam}: unexpected form name`);
  }
});

test("question ids are unique across the whole form and passages are never orphaned", () => {
  const byExam = new Map<string, Set<string>>();
  for (const { exam, section, data } of files()) {
    const seen = byExam.get(exam) ?? new Set<string>();
    const passageIds = new Set(data.passages.map(passage => passage.id));
    for (const question of data.questions) {
      assert.ok(!seen.has(question.id), `${exam}/${section}: duplicate question id ${question.id}`);
      seen.add(question.id);
      if (question.passageId !== null) {
        assert.ok(passageIds.has(question.passageId), `${question.id}: points at missing passage ${question.passageId}`);
      }
    }
    byExam.set(exam, seen);
    const used = new Set(data.questions.map(question => question.passageId));
    const blueprint = SECTIONS.find(item => item.id === section);
    for (const passage of data.passages) {
      // Only once the section is finished. An author writing a section builds
      // its passages and questions in interleaved passes, so an orphan passage
      // mid-write is normal; failing on it puts a red suite in front of every
      // other author and teaches them to read past failures that are not
      // theirs, which is how a real one gets ignored.
      if (blueprint && data.questions.length !== blueprint.questions) continue;
      assert.ok(used.has(passage.id), `${exam}/${section}: passage ${passage.id} has no questions`);
      assert.ok(passage.paragraphs.length >= 2, `${passage.id}: a passage needs at least two paragraphs`);
      // CARS passages carry no title on the real exam; science passages do.
      if (section !== "cars") {
        assert.ok(passage.title.length > 4, `${passage.id}: passage needs a real title`);
      }
    }
  }
});

test("every question has four distinct choices and a key among them", () => {
  for (const { section, data } of files()) {
    for (const question of data.questions) {
      assert.deepEqual(Object.keys(question.choices).sort(), ["A", "B", "C", "D"], `${question.id}: choice letters`);
      assert.ok(LETTERS.includes(question.correct as never), `${question.id}: key ${question.correct} is not a letter`);
      const texts = LETTERS.map(letter => question.choices[letter].trim().toLowerCase());
      assert.equal(new Set(texts).size, 4, `${question.id}: two choices say the same thing`);
      for (const letter of LETTERS) {
        assert.ok(question.choices[letter].trim().length > 0, `${question.id}: choice ${letter} is empty`);
      }
      assert.ok(question.stem.trim().length > 20, `${question.id}: stem is too thin to be a real question`);
      assert.ok(section === "cars" || question.explanation.trim().length > 60, `${question.id}: explanation is too thin`);
    }
  }
});

test("every wrong choice is explained, and the key is not", () => {
  for (const { data } of files()) {
    for (const question of data.questions) {
      const expected = LETTERS.filter(letter => letter !== question.correct).sort();
      assert.deepEqual(Object.keys(question.wrong).sort(), expected, `${question.id}: wrong-answer notes must cover exactly the distractors`);
      for (const [letter, note] of Object.entries(question.wrong)) {
        assert.ok(note.trim().length > 25, `${question.id}: the note for ${letter} says nothing useful`);
      }
    }
  }
});

test("no drafting debris survives into content", () => {
  // The mis-keyed question found in the lesson bank announced itself with
  // exactly this kind of leftover, so it is worth a standing check.
  const debris = /\b(wait,?\s+recalculat|TODO|FIXME|placeholder|lorem ipsum|XXX)\b/i;
  for (const { data } of files()) {
    for (const question of data.questions) {
      const whole = [question.stem, question.explanation, ...Object.values(question.choices), ...Object.values(question.wrong)].join(" ");
      assert.ok(!debris.test(whole), `${question.id}: drafting debris left in the text`);
    }
  }
});

test("tags are real: content category, reasoning skill, difficulty and unit", () => {
  for (const { section, data } of files()) {
    for (const question of data.questions) {
      assert.ok(["easy", "medium", "hard"].includes(question.difficulty), `${question.id}: difficulty`);
      assert.ok(question.skill in SKILLS, `${question.id}: unknown skill ${question.skill}`);
      if (section === "cars") {
        assert.equal(question.category, "", `${question.id}: CARS questions carry no content category`);
        assert.equal(question.unit, null, `${question.id}: CARS questions have no content unit`);
        assert.ok(question.skill.startsWith("cars-"), `${question.id}: CARS needs a CARS reasoning skill`);
      } else {
        assert.ok(question.category in CONTENT_CATEGORIES, `${question.id}: unknown content category ${question.category}`);
        assert.ok(question.unit && UNIT_IDS.has(question.unit), `${question.id}: unit ${question.unit} is not a real unit`);
        assert.ok(question.skill.startsWith("skill-"), `${question.id}: science needs a numbered reasoning skill`);
      }
    }
  }
});

test("no section is overfull, and a finished section matches the blueprint exactly", () => {
  for (const { exam, section, data } of files()) {
    const blueprint = SECTIONS.find(item => item.id === section);
    assert.ok(blueprint, `${section}: no blueprint`);
    assert.ok(
      data.questions.length <= blueprint.questions,
      `${exam}/${section}: ${data.questions.length} questions written but the blueprint allows ${blueprint.questions}`,
    );
    if (data.questions.length === blueprint.questions) {
      const discretes = data.questions.filter(question => question.passageId === null).length;
      assert.equal(discretes, blueprint.discreteQuestions, `${exam}/${section}: discrete count must match the blueprint`);
    }
  }
});

test("the answer key is spread across all four letters", () => {
  // A form whose key is 40% one letter is guessable, which makes the score
  // meaningless. Only checked once a section has enough questions to judge.
  for (const { exam, section, data } of files()) {
    if (data.questions.length < 40) continue;
    for (const letter of LETTERS) {
      const share = data.questions.filter(question => question.correct === letter).length / data.questions.length;
      assert.ok(share >= 0.15 && share <= 0.35, `${exam}/${section}: ${letter} is the key ${Math.round(share * 100)}% of the time`);
    }
  }
});

/* ------------------------------------------------------------------ *
 * Blueprint accuracy
 *
 * These fire only once a section is complete, because a half-written
 * section is legitimately lopsided. They are what let us say the forms are
 * built to the AAMC's published weighting rather than to our own taste.
 * ------------------------------------------------------------------ */

/**
 * A quoted phrase has to exist in the passage it is quoted from.
 *
 * Passages are drafted long, questions are written against the draft, then
 * the passage is trimmed to its word limit — and every cut can orphan a
 * quotation. One CARS section shipped five such questions and a second had
 * three, with the screen clean and every other test passing, because nothing
 * compared the words in quotation marks against the words in the passage. A
 * question whose quoted phrase is not in the text is not hard, it is
 * unanswerable.
 *
 * Only explanations and distractor notes are checked: a stem may legitimately
 * invent quoted material, and a choice may quote that invention back, so both
 * join the haystack instead.
 */
test("every quoted phrase appears in the passage it is quoted from", () => {
  const normalise = (text: string) =>
    text
      .replace(/[\u2018\u2019]/g, "'")
      .toLowerCase()
      .replace(/[^a-z0-9' ]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();

  const quotations = (text: string) => {
    const out: string[] = [];
    for (const match of text.matchAll(/(?:^|[\s(\[\u2014\u2013-])'([^']+)'(?=$|[\s.,;:!?)\]\u2014\u2013-])/g)) {
      const phrase = match[1].trim();
      if (phrase.split(/\s+/).length >= 3) out.push(phrase);
    }
    return out;
  };

  for (const { exam, section, data } of files()) {
    const passages = new Map(data.passages.map(passage => [passage.id, normalise(passage.paragraphs.join(" "))]));
    for (const question of data.questions) {
      const passage = passages.get(question.passageId ?? "");
      if (!passage) continue;
      const invented = normalise([question.stem, ...Object.values(question.choices)].join(" "));
      const sources: [string, string][] = [
        ["explanation", question.explanation],
        ...Object.entries(question.wrong).map(([letter, note]) => [`note ${letter}`, note] as [string, string]),
      ];
      for (const [where, text] of sources) {
        for (const phrase of quotations(text)) {
          // An ellipsis marks a legitimate elision: each fragment must appear,
          // and in the order the ellipsis implies.
          let cursor = 0;
          for (const fragment of phrase.split(/\s*\.\.\.\s*/).map(normalise).filter(Boolean)) {
            const at = passage.indexOf(fragment, cursor);
            if (at === -1) {
              assert.ok(
                invented.includes(fragment),
                `${exam}/${section} ${question.id} ${where}: the passage does not contain the quoted "${fragment}"`,
              );
              break;
            }
            cursor = at + fragment.length;
          }
        }
      }
    }
  }
});

test("a finished section matches the AAMC's published distribution", () => {
  for (const { exam, section, data } of files()) {
    const spec = SPECS[section as keyof typeof SPECS];
    const blueprint = SECTIONS.find(item => item.id === section);
    if (!spec || !blueprint || data.questions.length !== blueprint.questions) continue;
    const total = data.questions.length;
    const share = (count: number) => count / total;

    for (const [concept, target] of Object.entries(spec.foundationalConcepts)) {
      const actual = share(data.questions.filter(question => conceptOf(question.category) === concept).length);
      assert.ok(
        Math.abs(actual - target) <= TOLERANCE,
        `${exam}/${section}: foundational concept ${concept} is ${Math.round(actual * 100)}% but should be about ${Math.round(target * 100)}%`,
      );
    }

    for (const [skill, target] of Object.entries(spec.skills)) {
      const actual = share(data.questions.filter(question => question.skill === skill).length);
      assert.ok(
        Math.abs(actual - (target as number)) <= TOLERANCE,
        `${exam}/${section}: ${skill} is ${Math.round(actual * 100)}% but should be about ${Math.round((target as number) * 100)}%`,
      );
    }

    // Not stacked toward hard: that is the single most common defect in
    // third-party forms, and it makes the score estimate pessimistic.
    for (const [level, target] of Object.entries(DIFFICULTY_MIX)) {
      const actual = share(data.questions.filter(question => question.difficulty === level).length);
      assert.ok(
        Math.abs(actual - target) <= TOLERANCE + 0.04,
        `${exam}/${section}: ${level} questions are ${Math.round(actual * 100)}% but should be about ${Math.round(target * 100)}%`,
      );
    }

    /**
     * Every content category of this section's concepts has to be present.
     *
     * The concept-level percentages above can be met exactly while a whole
     * content category is missing, because a concept holds several of them.
     * That is how Full-Length 3 came to have no question at all on
     * intermolecular forces and only one on the nervous and endocrine
     * systems: ten assigned passage topics clustered, every published
     * percentage was hit, and nothing noticed. A student notices.
     *
     * Two is the floor rather than a proportional target: the AAMC does not
     * publish per-category weights, and some categories are genuinely thin.
     */
    const concepts = Object.keys(spec.foundationalConcepts);
    const belongs = Object.keys(CONTENT_CATEGORIES).filter(code => concepts.includes(conceptOf(code)));
    for (const code of belongs) {
      const count = data.questions.filter(question => question.category === code).length;
      assert.ok(
        count >= 2,
        `${exam}/${section}: content category ${code} (${CONTENT_CATEGORIES[code]}) has ${count} question${count === 1 ? "" : "s"}; every category of concepts ${concepts.join("/")} needs at least 2, or a student sits a form with a hole in it`,
      );
    }

    const passageCount = data.passages.length;
    assert.equal(passageCount, spec.passages.count, `${exam}/${section}: should have ${spec.passages.count} passage sets`);
    for (const passage of data.passages) {
      const attached = data.questions.filter(question => question.passageId === passage.id).length;
      const [min, max] = spec.passages.questionsEach;
      assert.ok(
        attached >= min && attached <= max,
        `${exam}/${section}: passage ${passage.id} carries ${attached} questions, outside the ${min}-${max} the real exam uses`,
      );
    }
  }
});

test("passages are the length the real exam uses", () => {
  for (const { exam, section, data } of files()) {
    const spec = SPECS[section as keyof typeof SPECS];
    if (!spec) continue;
    const [min, max] = spec.passageWords;
    for (const passage of data.passages) {
      const words = passage.paragraphs.join(" ").trim().split(/\s+/).length;
      /**
       * The floor used to carry 40% slack, which hid a real gap: every one of
       * Full-Length 1's Chem/Phys passages is shorter than the range this
       * project documents, four of them under 200 words against a 250 floor.
       * A short passage is an easier passage — less to hold in mind, fewer
       * places for a distractor to come from — so the slack was quietly
       * making the flagship free form softer than the exam it imitates.
       *
       * The ceiling keeps a little slack because an over-long passage costs
       * the student time rather than fidelity, and 25% of 500 words is still
       * readable inside the pacing the section allows.
       */
      assert.ok(words <= max * 1.25, `${exam}/${section}: ${passage.id} runs ${words} words, well over the ${max} the real exam uses`);
      assert.ok(words >= min, `${exam}/${section}: ${passage.id} is ${words} words against a floor of ${min}; a short passage is an easier passage`);
    }
  }
});

test("choices that have a natural order are presented in it", () => {
  // Rotating choices to balance the answer key is safe for prose, but not for
  // choices that carry an order of their own: a real exam never lists
  // percentages as 80, 64, 20, 41, or patients as W, X, Z, Y.
  const LABEL = /^(?:patient|sample|subject|group|curve|compound|experiment|trial)\s+([A-Z0-9])\b/i;
  const QUANTITY = /^[-+]?(\d+(?:\.\d+)?)\s*(?:×\s*10\s*[¹²³⁰⁴-⁹⁻]+)?\s*(?:%|[A-Za-z°μ/]{0,6})$/;

  const magnitude = (text: string) => {
    const cleaned = text.replace(/×/g, "x").replace(/,/g, "");
    const match = cleaned.match(/^([-+]?\d+(?:\.\d+)?)/);
    if (!match) return null;
    const mantissa = parseFloat(match[1]);
    const sup: Record<string, string> = { "⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9","⁻":"-" };
    const exp = cleaned.match(/x\s*10\s*([¹²³⁰⁴-⁹⁻]+)/);
    if (exp) {
      const value = parseInt([...exp[1]].map(c => sup[c] ?? c).join(""), 10);
      if (Number.isFinite(value)) return mantissa * 10 ** value;
    }
    return mantissa;
  };

  const monotonic = (values: number[]) =>
    values.every((v, i) => i === 0 || v >= values[i - 1]) ||
    values.every((v, i) => i === 0 || v <= values[i - 1]);

  for (const { exam, section, data } of files()) {
    for (const question of data.questions) {
      const texts = ["A", "B", "C", "D"].map(letter => question.choices[letter].trim());

      // Labelled items: the letters must run in order.
      const labels = texts.map(text => text.match(LABEL)?.[1]?.toUpperCase() ?? null);
      if (labels.every(label => label !== null)) {
        const sorted = [...labels as string[]].sort();
        assert.deepEqual(labels, sorted, `${exam}/${section}/${question.id}: labelled choices are out of order (${labels.join(", ")})`);
      }

      // Bare quantities: they must run up or down, not jump about.
      if (texts.every(text => QUANTITY.test(text) || /^[-+]?[\d.]+\s*(?:×\s*10)/.test(text))) {
        const values = texts.map(magnitude);
        if (values.every(value => value !== null)) {
          assert.ok(
            monotonic(values as number[]),
            `${exam}/${section}/${question.id}: numeric choices are out of order (${texts.join(", ")})`,
          );
        }
      }
    }
  }
});

test("a finished science section uses the question formats the real exam uses", () => {
  // Roman numeral items and negative stems are used throughout the real exam.
  // A student who has only ever practised on questions without them meets
  // both formats cold on test day, and both cost time the first time.
  for (const { exam, section, data } of files()) {
    const blueprint = SECTIONS.find(item => item.id === section);
    if (!blueprint || data.questions.length !== blueprint.questions) continue;

    const roman = data.questions.filter(q => /\bI\.\s/.test(q.stem) && /\bII\.\s/.test(q.stem));
    const negative = data.questions.filter(q => /\b(EXCEPT|LEAST|LOWEST|NOT)\b/.test(q.stem));

    assert.ok(roman.length >= 2, `${exam}/${section}: only ${roman.length} Roman numeral questions; the real exam uses them throughout`);
    assert.ok(roman.length <= 8, `${exam}/${section}: ${roman.length} Roman numeral questions is more than the real exam uses`);
    assert.ok(negative.length >= 2, `${exam}/${section}: only ${negative.length} questions with a negative or reversed stem`);
    assert.ok(negative.length <= 8, `${exam}/${section}: ${negative.length} negative stems overloads the form`);

    // A Roman numeral question must offer combinations, not single items.
    for (const question of roman) {
      const texts = ["A", "B", "C", "D"].map(letter => question.choices[letter]);
      assert.ok(
        texts.some(text => /\band\b/i.test(text)),
        `${question.id}: a Roman numeral question needs combination choices`,
      );
    }
  }
});

test("the answer key never repeats a letter three times running", () => {
  // A real form does not key three in a row, and a student who notices a run
  // starts answering the pattern rather than the question.
  for (const { exam, section, data } of files()) {
    if (data.questions.length < 20) continue;
    let run = 1;
    for (let index = 1; index < data.questions.length; index += 1) {
      run = data.questions[index].correct === data.questions[index - 1].correct ? run + 1 : 1;
      assert.ok(
        run < 3,
        `${exam}/${section}: ${data.questions[index].correct} is the key for questions ${index - 1} to ${index + 1} in a row`,
      );
    }
  }
});
