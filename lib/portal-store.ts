import { calendarDay, summarizeStreak, type CallInput } from "./engagement";
export interface Database {
  query(sql: string, values?: unknown[]): Promise<{ rows: Record<string, unknown>[] }>;
}
export const portalSchema = [
  `CREATE TABLE IF NOT EXISTS vitalis_profiles (
    email TEXT PRIMARY KEY, timezone TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
  )`,
  `CREATE TABLE IF NOT EXISTS vitalis_days (
    email TEXT NOT NULL REFERENCES vitalis_profiles(email), day DATE NOT NULL,
    answered BOOLEAN NOT NULL DEFAULT FALSE, PRIMARY KEY (email, day)
  )`,
  `CREATE TABLE IF NOT EXISTS vitalis_calls (
    id UUID PRIMARY KEY, student_email TEXT NOT NULL, title TEXT NOT NULL,
    starts_at TIMESTAMPTZ NOT NULL, duration_minutes INTEGER NOT NULL CHECK (duration_minutes BETWEEN 5 AND 180),
    zoom_url TEXT NOT NULL, notes TEXT NOT NULL DEFAULT '', created_by TEXT NOT NULL,
    cancelled BOOLEAN NOT NULL DEFAULT FALSE, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
  )`,
  `CREATE INDEX IF NOT EXISTS vitalis_calls_student_start ON vitalis_calls(student_email, starts_at)`,
];
export async function activity(db: Database, email: string, timeZone: string, answered: boolean, now = new Date()) {
  const normalized = email.toLowerCase();
  // The stored zone is fixed on first visit so moving devices cannot count a day twice.
  await db.query("INSERT INTO vitalis_profiles (email, timezone) VALUES ($1, $2) ON CONFLICT (email) DO NOTHING", [normalized, timeZone]);
  const profile = await db.query("SELECT timezone FROM vitalis_profiles WHERE email = $1", [normalized]);
  const zone = String(profile.rows[0].timezone);
  const today = calendarDay(now, zone);
  // One atomic upsert handles retries and concurrent tabs without incrementing a counter.
  await db.query(`INSERT INTO vitalis_days (email, day, answered) VALUES ($1, $2::date, $3)
    ON CONFLICT (email, day) DO UPDATE SET answered = vitalis_days.answered OR EXCLUDED.answered`, [normalized, today, answered]);
  const days = await db.query("SELECT to_char(day, 'YYYY-MM-DD') AS day, answered FROM vitalis_days WHERE email = $1 ORDER BY day", [normalized]);
  return {
    streak: summarizeStreak(days.rows.filter(row => row.answered).map(row => String(row.day)), today),
    visitDays: days.rows.length, timeZone: zone,
  };
}
export async function getCalls(db: Database, email: string, admin: boolean) {
  const result = await db.query(`SELECT id, student_email AS "studentEmail", title,
      starts_at AS "startsAt", duration_minutes AS "durationMinutes", zoom_url AS "zoomUrl", notes
    FROM vitalis_calls WHERE cancelled = FALSE AND starts_at + duration_minutes * INTERVAL '1 minute' > NOW()
      AND ($2::boolean OR student_email = $1)
    ORDER BY starts_at LIMIT 200`, [email.toLowerCase(), admin]);
  return result.rows;
}
export async function saveCall(db: Database, input: CallInput, creator: string, id: string, update = false) {
  const values = [id, input.studentEmail, input.title, input.startsAt, input.durationMinutes, input.zoomUrl, input.notes, creator];
  if (update) {
    const result = await db.query(`UPDATE vitalis_calls SET student_email=$2, title=$3, starts_at=$4,
      duration_minutes=$5, zoom_url=$6, notes=$7, created_by=$8 WHERE id=$1 AND cancelled=FALSE RETURNING id`, values);
    return !!result.rows.length;
  }
  // Idempotent create: retrying the same form cannot create a duplicate appointment.
  await db.query(`INSERT INTO vitalis_calls (id,student_email,title,starts_at,duration_minutes,zoom_url,notes,created_by)
    VALUES ($1,$2,$3,$4,$5,$6,$7,$8) ON CONFLICT (id) DO NOTHING`, values);
  return true;
}
