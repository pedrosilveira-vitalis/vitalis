export const sections = ['bio-biochem', 'chem-phys', 'psych-soc', 'cars'] as const;
export type Section = typeof sections[number];
export type Question = {
  id: string; question_text: string; choice_a: string; choice_b: string;
  choice_c: string; choice_d: string; correct_answer: string; explanation: string;
  topic: string; section: string; difficulty: string;
  passage?: { title: string; content: string };
  wrongAnswerExplanations: Record<string, string>;
};
export function sessionSettings(input: Record<string, unknown>) {
  const section = input.section;
  const count = input.count ?? 10;
  const difficulty = input.difficulty ?? 'mixed';
  const format = input.format ?? 'standalone';
  if (typeof section !== 'string' || ![...sections, 'mixed'].includes(section)) throw new Error('Choose a valid section.');
  if (typeof count !== 'number' || !Number.isInteger(count) || count < 1 || count > 20) throw new Error('Choose 1–20 questions.');
  if (!['mixed', 'easy', 'medium', 'hard'].includes(String(difficulty))) throw new Error('Choose a valid difficulty.');
  if (!['standalone', 'passage', 'guide', 'drills'].includes(String(format))) throw new Error('Choose a valid format.');
  return { section, count, difficulty: String(difficulty), format: String(format) };
}
export function allocateSections(section: string, count: number): { section: Section; count: number }[] {
  if (section !== 'mixed') return [{ section: section as Section, count }];
  return sections.map((s, i) => ({ section: s, count: Math.floor(count / 4) + (i < count % 4 ? 1 : 0) })).filter(x => x.count > 0);
}
function object(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Invalid generated content.');
  return value as Record<string, unknown>;
}
function text(value: unknown): string {
  if (typeof value !== 'string' || !value.trim()) throw new Error('Incomplete generated content.');
  return value.trim();
}
export function parseQuestions(value: unknown, section: string, count: number, needsPassage: boolean, difficulty = 'mixed'): Question[] {
  const data = object(value);
  if (!Array.isArray(data.questions) || data.questions.length !== count) throw new Error('Incorrect question count.');
  const passage = needsPassage ? object(data.passage) : undefined;
  const context = passage ? { title: text(passage.title), content: text(passage.content) } : undefined;
  return data.questions.map((raw, i) => {
    const q = object(raw), choices = object(q.choices);
    const answer = text(q.correctAnswer);
    if (!['A','B','C','D'].includes(answer)) throw new Error('Invalid answer key.');
    const level = text(q.difficulty);
    if (!['easy','medium','hard'].includes(level) || (difficulty !== 'mixed' && level !== difficulty)) throw new Error('Invalid difficulty.');
    const wrong = object(q.wrongAnswerExplanations);
    const explanations: Record<string, string> = {};
    for (const letter of ['A','B','C','D']) if (letter !== answer) explanations[letter] = text(wrong[letter]);
    return { id: `${section}-${i+1}`, question_text: text(q.stem), choice_a: text(choices.A), choice_b: text(choices.B), choice_c: text(choices.C), choice_d: text(choices.D), correct_answer: answer, explanation: text(q.explanation), topic: text(q.concept), section, difficulty: level, passage: context, wrongAnswerExplanations: explanations };
  });
}
export function parseCards(value: unknown, count: number) {
  const data = object(value);
  if (!Array.isArray(data.deck) || data.deck.length !== count) throw new Error('Incorrect card count.');
  return data.deck.map(raw => { const card = object(raw); return { front: text(card.front), back: text(card.back) }; });
}
