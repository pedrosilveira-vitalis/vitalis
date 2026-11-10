import test from "node:test";
import assert from "node:assert/strict";
import { splitLessonForVisual } from "../lib/lesson-presentation";
test("diagram placement splits only an exact level-two heading and preserves lesson text", () => {
 const text="# Title\n\nIntro\n\n## A (B)\nBody\n\n## Summary\nEnd";
 const pieces=splitLessonForVisual(text,"A (B)");
 assert.equal(pieces.join(""),text);
 assert.equal(pieces[1],"## A (B)\nBody\n\n## Summary\nEnd");
 assert.deepEqual(splitLessonForVisual(text,"A"),[text,""]);
 assert.deepEqual(splitLessonForVisual(text,".*"),[text,""]);
});
test("no placement or changed headings keep the whole lesson readable", () => {
 const text="## One\r\nBody\r\n## Two\r\nRest";
 assert.deepEqual(splitLessonForVisual(text),[text,""]);
 assert.deepEqual(splitLessonForVisual(text,"Missing"),[text,""]);
 assert.equal(splitLessonForVisual(text,"Two")[1],"## Two\r\nRest");
});
