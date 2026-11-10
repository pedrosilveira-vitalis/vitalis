import test from "node:test";
import assert from "node:assert/strict";
import { dailyStudyReward } from "../lib/study-rewards";
import { summarizeStreak } from "../lib/engagement";
test("visits and unconfirmed days never produce a celebration", () => {
 const unfinished=summarizeStreak([], "2026-11-09");
 const completed=summarizeStreak(["2026-11-09"], "2026-11-09");
 assert.equal(dailyStudyReward(null,completed,"visit"),null);
 assert.equal(dailyStudyReward(null,unfinished,"answer"),null);
});
test("first confirmed answer celebrates once; repeat answers do not", () => {
 const before=summarizeStreak([],"2026-11-09");
 const after=summarizeStreak(["2026-11-09"],"2026-11-09");
 assert.match(dailyStudyReward(before,after,"answer")!.title,/first step/);
 assert.equal(dailyStudyReward(after,after,"answer"),null);
});
test("a new calendar day can celebrate after yesterday was completed", () => {
 const previous=summarizeStreak(["2026-11-08"],"2026-11-08");
 const next=summarizeStreak(["2026-11-08","2026-11-09"],"2026-11-09");
 assert.equal(dailyStudyReward(previous,next,"answer")!.day,"2026-11-09");
});
test("week milestone follows confirmed streak, not answer volume", () => {
 const dates=Array.from({length:7},(_,i)=>`2026-11-${String(i+3).padStart(2,"0")}`);
 const next=summarizeStreak(dates,"2026-11-09");
 assert.equal(dailyStudyReward(null,next,"answer")!.title,"A week of showing up!");
});
