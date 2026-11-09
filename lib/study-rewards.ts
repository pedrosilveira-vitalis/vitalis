import type { Streak } from "./engagement";

export type StudyReward = { day: string; title: string; message: string };
/** Celebrate only a confirmed answer that completes a previously unfinished day. */
export function dailyStudyReward(previous: Streak | null, next: Streak, kind: "visit" | "answer"): StudyReward | null {
  const day = next.week.at(-1)?.date;
  if (kind !== "answer" || !next.completedToday || !day) return null;
  const sameDay = previous?.week.at(-1)?.date === day;
  if (sameDay && previous?.completedToday) return null;
  const milestones: Record<number, string> = { 1: "Your first step is in!", 7: "A week of showing up!", 14: "Two weeks of practice!", 30: "30 days. One steady habit." };
  return {
    day,
    title: milestones[next.current] ?? "Today’s practice is saved!",
    message: `${next.current}-day streak. One answer at a time. Take a moment to notice your progress.`,
  };
}
