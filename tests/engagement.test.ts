import test from "node:test";
import assert from "node:assert/strict";
import { PGlite } from "@electric-sql/pglite";
import { activity, getCalls, portalSchema, saveCall, type Database } from "../lib/portal-store";
import { calendarDay, isAdmin, summarizeStreak, validTimeZone, validateCall, zoomLink } from "../lib/engagement";
import { questionToken, validQuestionToken } from "../lib/question-token";

test("streaks count distinct dates, retain yesterday, reset after a missed day, and keep best", () => {
  const days = ["2026-10-30", "2026-10-31", "2026-11-01", "2026-11-01"];
  assert.equal(summarizeStreak(days, "2026-11-01").current, 3);
  assert.equal(summarizeStreak(days, "2026-11-02").current, 3);
  const missed = summarizeStreak(days, "2026-11-03");
  assert.equal(missed.current, 0); assert.equal(missed.best, 3); assert.equal(missed.total, 3);
  assert.equal(summarizeStreak([...days, "2026-11-03"], "2026-11-03").current, 1);
  assert.equal(summarizeStreak([], "2026-11-03").week.length, 7);
});
test("calendar days follow the student zone across midnight and daylight saving", () => {
  assert.equal(calendarDay(new Date("2026-11-01T03:59:59Z"), "America/New_York"), "2026-10-31");
  assert.equal(calendarDay(new Date("2026-11-01T06:30:00Z"), "America/New_York"), "2026-11-01");
  assert.equal(calendarDay(new Date("2026-11-02T04:59:59Z"), "America/New_York"), "2026-11-01");
  assert.equal(calendarDay(new Date("2026-11-02T05:00:00Z"), "America/New_York"), "2026-11-02");
  assert.equal(validTimeZone("made-up"), false); assert.equal(validTimeZone("America/New_York"), true);
});
test("admin identity is exact and Zoom links reject impersonation, credentials and unsafe schemes", () => {
  assert.ok(isAdmin("PedroDocoutto@gmail.com")); assert.equal(isAdmin("pedrodocoutto@gmail.com.attacker.com"), false);
  assert.equal(isAdmin(null), false);
  assert.equal(zoomLink("https://us02web.zoom.us/j/123?pwd=abc"), "https://us02web.zoom.us/j/123?pwd=abc");
  for (const bad of ["javascript:alert(1)", "https://zoom.us.evil.com/j/1", "https://evilzoom.us/j/1", "http://zoom.us/j/1", "https://x@y.zoom.us/j/1"]) assert.throws(() => zoomLink(bad));
});
test("only server-issued, recent question tokens qualify an answer", () => {
  const original = process.env.AUTH_SECRET;
  process.env.AUTH_SECRET = "test-only-secret";
  try {
    const now = Date.now(), token = questionToken("question-1", now)!;
    assert.ok(validQuestionToken(token, now + 500));
    assert.equal(validQuestionToken(token + "tamper", now), false);
    assert.equal(validQuestionToken(token, now - 1), false);
    assert.equal(validQuestionToken(token, now + 86400001), false);
    assert.equal(validQuestionToken(undefined), false);
  } finally { if (original === undefined) delete process.env.AUTH_SECRET; else process.env.AUTH_SECRET = original; }
});
test("call validation enforces future dates, duration, required fields and bounded notes", () => {
  const raw = { studentEmail: " Student@Example.com ", title: "Study", startsAt: "2030-11-06T20:00:00Z", durationMinutes: 30, zoomUrl: "https://zoom.us/j/123", notes: "" };
  assert.equal(validateCall(raw).studentEmail, "student@example.com");
  for (const patch of [{ durationMinutes: 0 }, { durationMinutes: 30.5 }, { startsAt: "2020-01-01" }, { studentEmail: "bad" }, { title: "" }, { notes: "x".repeat(1001) }]) {
    assert.throws(() => validateCall({ ...raw, ...patch }));
  }
});
test("PostgreSQL persistence handles visits, simultaneous answers, account isolation, rescheduling and cancellation", async () => {
  const pg = new PGlite();
  const db: Database = { query: (sql, values) => pg.query(sql, values) };
  try {
    for (const sql of portalSchema) await db.query(sql);
    const first = await activity(db, "a@example.com", "America/New_York", false, new Date("2026-11-01T14:00:00Z"));
    assert.equal(first.visitDays, 1); assert.equal(first.streak.current, 0);
    await Promise.all(Array.from({ length: 4 }, () => activity(db, "a@example.com", "America/New_York", true, new Date("2026-11-01T15:00:00Z"))));
    const repeated = await activity(db, "a@example.com", "Pacific/Auckland", false, new Date("2026-11-02T03:00:00Z"));
    assert.equal(repeated.timeZone, "America/New_York"); assert.equal(repeated.visitDays, 1); assert.equal(repeated.streak.current, 1);
    const next = await activity(db, "a@example.com", "America/New_York", true, new Date("2026-11-02T16:00:00Z"));
    assert.equal(next.streak.current, 2); assert.equal(next.visitDays, 2);
    const second = await activity(db, "b@example.com", "UTC", false, new Date("2026-11-02T16:00:00Z"));
    assert.equal(second.streak.current, 0); assert.equal(second.visitDays, 1);
    const skipped = await activity(db, "a@example.com", "America/New_York", true, new Date("2026-11-04T16:00:00Z"));
    assert.equal(skipped.streak.current, 1); assert.equal(skipped.streak.best, 2);
    const id = crypto.randomUUID();
    const input = validateCall({ studentEmail: "A@example.com", title: "Check-in", startsAt: "2030-11-06T20:00:00Z", durationMinutes: 30, zoomUrl: "https://zoom.us/j/123", notes: "Review acids." });
    await saveCall(db, input, "admin@example.com", id);
    await saveCall(db, input, "admin@example.com", id);
    assert.equal((await getCalls(db, "A@example.com", false)).length, 1);
    assert.equal((await getCalls(db, "b@example.com", false)).length, 0);
    assert.equal((await getCalls(db, "admin@example.com", true)).length, 1);
    await saveCall(db, { ...input, studentEmail: "b@example.com", title: "Moved" }, "admin@example.com", id, true);
    assert.equal((await getCalls(db, "a@example.com", false)).length, 0);
    assert.equal((await getCalls(db, "b@example.com", false))[0].title, "Moved");
    await db.query("UPDATE vitalis_calls SET cancelled=TRUE WHERE id=$1", [id]);
    assert.equal((await getCalls(db, "b@example.com", false)).length, 0);
    assert.equal(await saveCall(db, input, "admin@example.com", id, true), false);
  } finally { await pg.close(); }
});
