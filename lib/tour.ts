import { PLANS, type Capabilities, type PlanId } from "./billing";

/**
 * The guided tour someone sees straight after paying.
 *
 * Steps are chosen from what the plan actually unlocks, so nobody is walked
 * through a door that is locked for them. The order is the order we want a
 * student to work in — test date first, because every other feature is more
 * useful once the calendar exists.
 */
export type TourProp =
  | "calendar"
  | "book"
  | "cards"
  | "clipboard"
  | "chat"
  | "headset"
  | "chart"
  | "lock";

export type TourPose = "wave" | "point" | "lean" | "hop" | "read";

export interface TourStep {
  id: string;
  /** Short label for the progress rail. */
  label: string;
  heading: string;
  /** Nori's line, first person. Kept to one sentence. */
  says: string;
  body: string;
  href: string;
  cta: string;
  prop: TourProp;
  pose: TourPose;
  accent: string;
  /** A locked step is shown greyed, as an upsell, not as something to click. */
  locked?: boolean;
}

const BLUE = "#245574";
const SAGE = "#5b7a64";
const GOLD = "#987740";
const CLARET = "#a8324a";

const PLANNER: TourStep = {
  id: "planner",
  label: "Your date",
  heading: "Start with your test date.",
  says: "Tell me when you sit the exam and I'll work backwards from there.",
  body: "The planner spreads the units across the weeks you have left, so you always know what today is for. Everything else on the site reads from it.",
  href: "/study-plan",
  cta: "Set my test date",
  prop: "calendar",
  pose: "wave",
  accent: BLUE,
};

const LESSONS: TourStep = {
  id: "lessons",
  label: "Lessons",
  heading: "All 250 lessons are open.",
  says: "Every one of these was checked line by line against published sources.",
  body: "Twenty-eight units across all four sections, each lesson with its own diagrams for when the words aren't enough. Read them in planner order or jump to whatever is shaky.",
  href: "/study",
  cta: "Open the lessons",
  prop: "book",
  pose: "read",
  accent: SAGE,
};

const SHEETS: TourStep = {
  id: "cheatsheets",
  label: "Cheat sheets",
  heading: "One page per unit.",
  says: "Print these. Stick them where you'll see them.",
  body: "Twenty-eight one-pagers — the equations, pathways and traps for a unit on a single sheet. Built to print cleanly, so they work on a wall or in a folder.",
  href: "/cheatsheets",
  cta: "See the cheat sheets",
  prop: "cards",
  pose: "hop",
  accent: GOLD,
};

const QUESTIONS: TourStep = {
  id: "practice",
  label: "Questions",
  heading: "1,250 questions, every one explained.",
  says: "Get it wrong here rather than on test day.",
  body: "Full written explanations on every answer — not just the right one, but why each wrong choice was tempting. Flag anything you want to come back to.",
  href: "/practice",
  cta: "Try five questions",
  prop: "clipboard",
  pose: "point",
  accent: BLUE,
};

const TUTOR: TourStep = {
  id: "tutor",
  label: "Ask Nori",
  heading: "Ask me anything, any hour.",
  says: "Stuck on a question at 2am? That's what I'm for.",
  body: "Ask about a concept, a question you just missed, or how to spend the next hour. No limits on your plan.",
  href: "/tutor",
  cta: "Ask me something",
  prop: "chat",
  pose: "lean",
  accent: SAGE,
};

const REVIEWS: TourStep = {
  id: "calls",
  label: "Live review",
  heading: "A live review before your test date.",
  says: "Bring your worst questions — we'll work them live.",
  body: "Group sessions run before every MCAT date inside your window. They show up here as soon as they're scheduled, and you keep the recording.",
  href: "/calls",
  cta: "See upcoming sessions",
  prop: "headset",
  pose: "wave",
  accent: CLARET,
};

const EXTRAS: TourStep = {
  id: "extras",
  label: "Extras",
  heading: "And the small things.",
  says: "These are the bits people find in week three. Have them now.",
  body: "Flashcards for recall, flagged questions for the ones that got you, and a score calculator that turns raw counts into a scaled estimate.",
  href: "/flashcards",
  cta: "Open flashcards",
  prop: "chart",
  pose: "hop",
  accent: GOLD,
};

function upsell(): TourStep {
  const complete = PLANS.find(plan => plan.id === "complete");
  return {
    id: "upgrade",
    label: "Locked",
    heading: "The lessons and cheat sheets are still shut.",
    says: "This part isn't on your plan yet — no rush, it's here if you want it.",
    body: `${complete?.name ?? "Complete"} adds all 250 written lessons, the 28 printable cheat sheets and a live group review before each test date. You can move up at any point and we credit what you've already paid for the days you haven't used.`,
    href: "/plans",
    cta: "See what Complete adds",
    prop: "lock",
    pose: "lean",
    accent: "#6d716f",
    locked: true,
  };
}

export function tourFor(capabilities: Capabilities): TourStep[] {
  const steps: TourStep[] = [PLANNER];
  if (capabilities.lessons) steps.push(LESSONS, SHEETS);
  if (capabilities.questions) steps.push(QUESTIONS);
  steps.push(TUTOR);
  if (capabilities.liveReviews) steps.push(REVIEWS);
  steps.push(EXTRAS);
  if (!capabilities.lessons) steps.push(upsell());
  return steps;
}

export function planName(plan: PlanId | null | undefined): string {
  return PLANS.find(item => item.id === plan)?.name ?? "Vitalis";
}
