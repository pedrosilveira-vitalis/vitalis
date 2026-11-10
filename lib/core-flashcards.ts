import { sections, type Section } from './practice';
export type CoreCard = { front: string; back: string };
const sources: Record<Section, string> = {
  'bio-biochem': 'https://openstax.org/books/organic-chemistry/pages/26-2-amino-acids-and-the-henderson-hasselbalch-equation-isoelectric-points',
  'chem-phys': 'https://openstax.org/books/chemistry-2e/pages/14-6-buffers',
  'psych-soc': 'https://openstax.org/books/psychology-2e/pages/6-3-operant-conditioning',
  cars: 'https://students-residents.aamc.org/whats-mcat-exam/critical-analysis-and-reasoning-skills-section-overview',
};
// A deliberately small, fixed set. Never presented as newly generated or comprehensive.
const decks: Record<Section, CoreCard[]> = {
  'bio-biochem': [
    { front: 'What does an amino acid’s isoelectric point (pI) describe?', back: 'The pH at which its average net charge is zero. Charged groups can still be present.' },
    { front: 'At a pH below its pI, what is an amino acid’s average net charge?', back: 'Positive: lower pH favors more protonated forms.' },
    { front: 'At a pH above its pI, what is an amino acid’s average net charge?', back: 'Negative: higher pH favors more deprotonated forms.' },
    { front: 'Which pKa values determine the pI of a free amino acid?', back: 'Average the two pKa values bracketing its net-zero charge form. Do not automatically average all pKa values.' },
    { front: 'An amino acid has pKa values 2, 4, and 9. Its net-zero form lies between the first two transitions. What is its pI?', back: '3, from (2 + 4) / 2.' },
    { front: 'Is a zwitterion the same as a molecule without charged groups?', back: 'No. A zwitterion contains both positive and negative charges, with zero net charge.' },
  ],
  'chem-phys': [
    { front: 'What pair commonly forms an acid–base buffer?', back: 'A weak acid and its conjugate base in appreciable amounts.' },
    { front: 'Write the Henderson–Hasselbalch equation using concentrations.', back: 'pH ≈ pKa + log10([A−]/[HA]). This concentration form assumes activities can be approximated appropriately.' },
    { front: 'When [A−] = [HA], how does buffer pH compare with pKa?', back: 'pH ≈ pKa, because log10(1) = 0.' },
    { front: 'When [A−]/[HA] = 10, how does buffer pH compare with pKa?', back: 'pH ≈ pKa + 1.' },
    { front: 'How does an HA/A− buffer respond to a small addition of strong acid?', back: 'A− consumes added H3O+ to form HA, limiting the pH change.' },
    { front: 'Can a buffer resist an unlimited amount of added acid or base?', back: 'No. Buffer capacity is finite; a large addition can exhaust a component and cause a large pH change.' },
  ],
  'psych-soc': [
    { front: 'In operant conditioning, what makes a consequence reinforcement?', back: 'It increases the future frequency of the behavior.' },
    { front: 'What makes a consequence punishment?', back: 'It decreases the future frequency of the behavior.' },
    { front: 'What do “positive” and “negative” mean in operant conditioning?', back: 'Positive means adding a stimulus; negative means removing one. They do not mean good and bad.' },
    { front: 'A driver buckles up to stop a warning tone and subsequently buckles up more often. What process is this?', back: 'Negative reinforcement: removing the tone increases buckling behavior.' },
    { front: 'A reward is delivered after every five completed responses. Which schedule is this?', back: 'Fixed ratio: reinforcement follows a predictable number of responses.' },
    { front: 'What is shaping?', back: 'Reinforcing successive approximations toward a target behavior.' },
  ],
  cars: [
    { front: 'What disciplines supply CARS passages?', back: 'Humanities and social sciences. The section tests reasoning about the passage rather than specialized subject knowledge.' },
    { front: 'What is the focus of Foundations of Comprehension?', back: 'Understanding the passage’s basic meaning, including its main idea and implied meaning.' },
    { front: 'What is the focus of Reasoning Within the Text?', back: 'Integrating and evaluating ideas and relationships within the passage.' },
    { front: 'What is the focus of Reasoning Beyond the Text?', back: 'Applying passage ideas to new situations or considering how new information affects them.' },
    { front: 'Can an answer be generally true but still fail a CARS question?', back: 'Yes. It must answer the specific question using the passage’s reasoning and context.' },
    { front: 'Do these CARS strategy flashcards replace passage practice?', back: 'No. Apply these skills while reading passages and answering passage-based questions.' },
  ],
};
export function coreDeck(section: Section | 'mixed', count: number) {
  const selected = section === 'mixed' ? [...sections] : [section];
  const cards = selected.flatMap(s => decks[s].map(card => ({ ...card })));
  for (let i = cards.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [cards[i], cards[j]] = [cards[j], cards[i]];
  }
  return { cards: cards.slice(0, count), sources: selected.map(s => sources[s]) };
}
