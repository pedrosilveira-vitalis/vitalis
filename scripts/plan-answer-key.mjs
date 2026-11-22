// A target key sequence to write against, so the key is planned rather than
// patched. Spreads the four letters evenly and never repeats one three times
// in a row, which is what a real form looks like.
//
// Usage: node scripts/plan-answer-key.mjs 53 [seed]
const count = Number(process.argv[2] ?? 59);
let seed = Number(process.argv[3] ?? 20261122);

// A small deterministic generator, so a run is reproducible and reviewable.
const next = () => {
  seed = (seed * 1103515245 + 12345) & 0x7fffffff;
  return seed / 0x7fffffff;
};

const LETTERS = ["A", "B", "C", "D"];
const quota = LETTERS.map((_, index) => Math.floor(count / 4) + (index < count % 4 ? 1 : 0));
const plan = [];

while (plan.length < count) {
  const options = LETTERS
    .map((letter, index) => ({ letter, index }))
    .filter(({ index }) => quota[index] > 0)
    .filter(({ letter }) => !(plan.length >= 2 && plan[plan.length - 1] === letter && plan[plan.length - 2] === letter));
  const pool = options.length ? options : LETTERS.map((letter, index) => ({ letter, index })).filter(({ index }) => quota[index] > 0);
  const pick = pool[Math.floor(next() * pool.length)];
  quota[pick.index] -= 1;
  plan.push(pick.letter);
}

const tally = Object.fromEntries(LETTERS.map(letter => [letter, plan.filter(x => x === letter).length]));
console.log(plan.join(" "));
console.log("\ncounts:", tally);
let longest = 1, run = 1;
for (let i = 1; i < plan.length; i += 1) {
  run = plan[i] === plan[i - 1] ? run + 1 : 1;
  longest = Math.max(longest, run);
}
console.log("longest run:", longest);
