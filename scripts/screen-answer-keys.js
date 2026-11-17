/**
 * Answer-key screen.
 *
 * Paste into the browser console on the live site, or run it after any batch of
 * question edits. It looks for three things across every lesson:
 *
 *   1. An explanation that names a letter as correct or incorrect in a way that
 *      contradicts the stored key. This is the defect that matters most: it
 *      marks a student wrong for reasoning correctly.
 *   2. Drafting debris left in student-facing text ("Wait, recalculating", and
 *      friends).
 *   3. A keyed choice whose number never appears in the explanation while some
 *      other choice's number does — the signature of lesson 253's mis-key.
 *
 * Heuristic 3 produces occasional false positives, usually a Unicode minus sign
 * that does not match an ASCII hyphen. Every flag is meant to be read by a
 * human, not auto-fixed.
 *
 * Usage:  await screenAnswerKeys()            // all lessons
 *         await screenAnswerKeys(240, 253)    // a range
 */
async function screenAnswerKeys(first = 1, last = 260) {
  const LETTERS = ["A", "B", "C", "D"];
  const debris =
    /\b(wait,|recalculat|let me reconsider|let me recalculate|actually, i |hmm,|as an ai|i apologi|todo|placeholder|lorem ipsum|\[insert|xxx)/i;

  const state = { lessons: 0, questions: 0, flags: [], missing: [] };
  const ids = [];
  for (let id = first; id <= last; id += 1) ids.push(id);

  for (let i = 0; i < ids.length; i += 8) {
    await Promise.all(
      ids.slice(i, i + 8).map(async id => {
        let data;
        try {
          const response = await fetch(`/api/study/lessons/${id}`);
          if (!response.ok) return;
          data = await response.json();
        } catch {
          return;
        }
        if (data.locked) {
          state.missing.push(id);
          return;
        }
        state.lessons += 1;
        for (const question of data.questions || []) {
          state.questions += 1;
          const key = String(question.correct_answer || "").trim().toUpperCase();
          const explanation = String(question.explanation || "");
          const choices = { A: question.choice_a, B: question.choice_b, C: question.choice_c, D: question.choice_d };
          const issues = [];

          if (!LETTERS.includes(key)) issues.push(`key is not A-D: ${key}`);
          if (debris.test(explanation)) issues.push(`debris: ${(explanation.match(debris) || [""])[0]}`);

          let match;
          const saysRight = /(?:choice|answer|option)\s+([A-D])\b[^.]{0,40}?\bis\s+(?:the\s+)?(?:correct|right|best)\b/gi;
          while ((match = saysRight.exec(explanation))) {
            if (match[1].toUpperCase() !== key) issues.push(`says ${match[1]} is correct, key is ${key}`);
          }
          const saysWrong = /(?:choice|answer|option)\s+([A-D])\b[^.]{0,40}?\bis\s+(?:incorrect|wrong|not\s+correct)\b/gi;
          while ((match = saysWrong.exec(explanation))) {
            if (match[1].toUpperCase() === key) issues.push(`says ${match[1]} is incorrect, but it is the key`);
          }

          const numbers = value => (String(value || "").match(/-?\d+(?:\.\d+)?/g) || []).filter(n => n.length > 1 || Number(n) > 4);
          const keyNumbers = numbers(choices[key]);
          if (keyNumbers.length && !keyNumbers.some(n => explanation.includes(n))) {
            const cited = LETTERS.filter(letter => letter !== key)
              .flatMap(letter => numbers(choices[letter]).filter(n => explanation.includes(n)).map(n => `${letter}=${n}`));
            if (cited.length) issues.push(`explanation cites ${cited.join(",")} but not key ${key}=${keyNumbers.join("/")}`);
          }

          if (issues.length) state.flags.push({ lesson: id, question: question.id, key, issues });
        }
      }),
    );
  }

  console.table(state.flags);
  if (state.missing.length) {
    console.warn(`${state.missing.length} lessons were locked and could not be screened. Sign in on a Complete plan to screen them.`);
  }
  console.log(`Screened ${state.questions} questions across ${state.lessons} lessons. ${state.flags.length} to read by hand.`);
  return state;
}

if (typeof window !== "undefined") window.screenAnswerKeys = screenAnswerKeys;
if (typeof module !== "undefined") module.exports = { screenAnswerKeys };
