export type Streak = { current: number; best: number; total: number; completedToday: boolean; week: { date: string; done: boolean }[] };
export function calendarDay(now: Date, timeZone: string) {
  return new Intl.DateTimeFormat("en-CA", { timeZone, year: "numeric", month: "2-digit", day: "2-digit" }).format(now);
}
export function validTimeZone(value: unknown): value is string {
  if (typeof value !== "string" || value.length > 80) return false;
  try { new Intl.DateTimeFormat("en", { timeZone: value }).format(); return true; } catch { return false; }
}
function previousDay(day: string, offset = 1) {
  return new Date(Date.parse(day + "T12:00:00Z") - offset * 86400000).toISOString().slice(0, 10);
}
export function summarizeStreak(days: string[], today: string): Streak {
  const ordered = [...new Set(days)].filter(day => day <= today).sort();
  const set = new Set(ordered);
  let best = 0, run = 0, previous = "";
  for (const day of ordered) {
    run = previous === previousDay(day) ? run + 1 : 1;
    best = Math.max(best, run);
    previous = day;
  }
  let cursor = set.has(today) ? today : previousDay(today), current = 0;
  while (set.has(cursor)) { current++; cursor = previousDay(cursor); }
  return {
    current, best, total: ordered.length, completedToday: set.has(today),
    week: Array.from({ length: 7 }, (_, i) => {
      const date = previousDay(today, 6 - i);
      return { date, done: set.has(date) };
    }),
  };
}
export function isAdmin(email: string | null | undefined) {
  const emails = process.env.VITALIS_ADMIN_EMAILS ?? "pedrodocoutto@gmail.com";
  return !!email && emails.split(",").some(item => item.trim().toLowerCase() === email.toLowerCase());
}
export function zoomLink(value: unknown) {
  if (typeof value !== "string" || value.length > 2048) throw new Error("Enter a valid Zoom meeting link.");
  let url: URL;
  try { url = new URL(value.trim()); } catch { throw new Error("Enter a valid Zoom meeting link."); }
  if (url.protocol !== "https:" || url.username || url.password ||
    !(url.hostname === "zoom.us" || url.hostname.endsWith(".zoom.us") || url.hostname === "zoom.com" || url.hostname.endsWith(".zoom.com"))) {
    throw new Error("Use an https:// Zoom meeting link.");
  }
  return url.toString();
}
export type CallInput = { studentEmail: string; title: string; startsAt: string; durationMinutes: number; zoomUrl: string; notes: string };
export function validateCall(raw: unknown, now = new Date()): CallInput {
  if (!raw || typeof raw !== "object") throw new Error("Enter the call details.");
  const v = raw as Record<string, unknown>;
  const studentEmail = typeof v.studentEmail === "string" ? v.studentEmail.trim().toLowerCase() : "";
  const title = typeof v.title === "string" ? v.title.trim() : "";
  const notes = typeof v.notes === "string" ? v.notes.trim() : "";
  const date = typeof v.startsAt === "string" ? new Date(v.startsAt) : new Date(NaN);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(studentEmail) || studentEmail.length > 254) throw new Error("Enter the student's Google sign-in email.");
  if (!title || title.length > 120) throw new Error("Use a title of 1–120 characters.");
  if (!Number.isFinite(date.getTime()) || date <= now) throw new Error("Choose a future date and time.");
  if (!Number.isInteger(v.durationMinutes) || Number(v.durationMinutes) < 5 || Number(v.durationMinutes) > 180) throw new Error("Choose a duration of 5–180 minutes.");
  if (notes.length > 1000) throw new Error("Keep notes within 1,000 characters.");
  return { studentEmail, title, notes, startsAt: date.toISOString(), durationMinutes: Number(v.durationMinutes), zoomUrl: zoomLink(v.zoomUrl) };
}
