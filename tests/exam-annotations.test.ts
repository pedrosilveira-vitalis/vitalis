import test from "node:test";
import assert from "node:assert/strict";
import { applyTool, pieces, type MarkMap } from "../components/exam/annotations";

const hit = (key: string, start: number, end: number) => ({ key, start, end });

test("a mark is applied, then cleared by the same gesture", () => {
  let marks: MarkMap = {};
  marks = applyTool(marks, "highlight", [hit("p0", 5, 10)]);
  assert.deepEqual(marks.p0, [{ start: 5, end: 10, kind: "highlight" }]);
  marks = applyTool(marks, "highlight", [hit("p0", 5, 10)]);
  assert.deepEqual(marks.p0, []);
});

test("overlapping marks of one kind merge instead of stacking", () => {
  let marks: MarkMap = {};
  marks = applyTool(marks, "highlight", [hit("p0", 0, 10)]);
  marks = applyTool(marks, "highlight", [hit("p0", 8, 20)]);
  assert.deepEqual(marks.p0, [{ start: 0, end: 20, kind: "highlight" }]);
});

test("clearing the middle of a mark splits it in two", () => {
  let marks: MarkMap = {};
  marks = applyTool(marks, "highlight", [hit("p0", 0, 30)]);
  marks = applyTool(marks, "highlight", [hit("p0", 10, 20)]);
  assert.deepEqual(marks.p0, [
    { start: 0, end: 10, kind: "highlight" },
    { start: 20, end: 30, kind: "highlight" },
  ]);
});

test("highlight and strikethrough are independent on the same text", () => {
  let marks: MarkMap = {};
  marks = applyTool(marks, "highlight", [hit("p0", 0, 10)]);
  marks = applyTool(marks, "strike", [hit("p0", 0, 10)]);
  assert.equal(marks.p0.filter(m => m.kind === "highlight").length, 1);
  assert.equal(marks.p0.filter(m => m.kind === "strike").length, 1);
  // Clearing the strike leaves the highlight alone.
  marks = applyTool(marks, "strike", [hit("p0", 0, 10)]);
  assert.deepEqual(marks.p0, [{ start: 0, end: 10, kind: "highlight" }]);
});

test("a selection spanning two regions marks both, and clears both", () => {
  let marks: MarkMap = {};
  marks = applyTool(marks, "highlight", [hit("p0", 4, 9), hit("p1", 0, 6)]);
  assert.equal(marks.p0.length, 1);
  assert.equal(marks.p1.length, 1);
  marks = applyTool(marks, "highlight", [hit("p0", 4, 9), hit("p1", 0, 6)]);
  assert.deepEqual(marks.p0, []);
  assert.deepEqual(marks.p1, []);
});

test("a part-marked selection marks the rest rather than clearing", () => {
  let marks: MarkMap = {};
  marks = applyTool(marks, "highlight", [hit("p0", 0, 5)]);
  marks = applyTool(marks, "highlight", [hit("p0", 0, 20)]);
  assert.deepEqual(marks.p0, [{ start: 0, end: 20, kind: "highlight" }]);
});

test("an empty selection changes nothing", () => {
  const marks = applyTool({ p0: [{ start: 0, end: 5, kind: "highlight" as const }] }, "highlight", []);
  assert.deepEqual(marks.p0, [{ start: 0, end: 5, kind: "highlight" }]);
});

test("text splits into pieces that carry the right marks and lose no characters", () => {
  const text = "The enzyme was inhibited by the compound.";
  const split = pieces(text, [
    { start: 4, end: 10, kind: "highlight" },
    { start: 15, end: 24, kind: "strike" },
  ]);
  assert.equal(split.map(piece => piece.text).join(""), text);
  assert.equal(split.find(piece => piece.highlight)?.text, "enzyme");
  assert.equal(split.find(piece => piece.strike)?.text, "inhibited");
  // Unmarked text is still returned, so nothing silently disappears.
  assert.ok(split.some(piece => !piece.highlight && !piece.strike));
});

test("overlapping marks of different kinds produce a piece carrying both", () => {
  const split = pieces("abcdefghij", [
    { start: 0, end: 6, kind: "highlight" },
    { start: 3, end: 10, kind: "strike" },
  ]);
  assert.equal(split.map(piece => piece.text).join(""), "abcdefghij");
  const both = split.find(piece => piece.highlight && piece.strike);
  assert.equal(both?.text, "def");
});

test("marks at the very edges of the text are kept", () => {
  const split = pieces("abcdef", [{ start: 0, end: 6, kind: "highlight" }]);
  assert.equal(split.length, 1);
  assert.equal(split[0].text, "abcdef");
  assert.equal(split[0].highlight, true);
});
