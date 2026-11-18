/**
 * Highlighting and strikethrough, the way the real exam does it.
 *
 * On test day a student selects text anywhere — passage, stem or answer
 * choice — and clicks Highlight or Strikethrough. Rather than mutating the DOM
 * (which fights React and breaks on re-render), a mark is stored as a pair of
 * character offsets into the plain text of a labelled container, and the text
 * is re-rendered split around the marks. That makes marks serialisable, so a
 * student who reloads mid-section does not lose an hour of annotation.
 */

export type MarkKind = "highlight" | "strike";
export interface Mark {
  start: number;
  end: number;
  kind: MarkKind;
}
/** Marks for every annotatable region, keyed by its data-annotate value. */
export type MarkMap = Record<string, Mark[]>;

/** Where a selection fell, in offsets into each region it touched. */
interface Hit {
  key: string;
  start: number;
  end: number;
}

/**
 * Reads the current selection and reports which annotatable regions it covers.
 * Returns an empty list for a collapsed selection or one outside any region.
 */
export function readSelection(root: ParentNode = document): Hit[] {
  const selection = typeof window === "undefined" ? null : window.getSelection();
  if (!selection || selection.isCollapsed || !selection.rangeCount) return [];
  const range = selection.getRangeAt(0);
  const hits: Hit[] = [];

  for (const container of Array.from(root.querySelectorAll<HTMLElement>("[data-annotate]"))) {
    const key = container.dataset.annotate;
    if (!key || !range.intersectsNode(container)) continue;

    let offset = 0;
    let start: number | null = null;
    let end: number | null = null;
    const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);

    while (walker.nextNode()) {
      const node = walker.currentNode as Text;
      const length = node.nodeValue?.length ?? 0;
      if (range.intersectsNode(node)) {
        const localStart = node === range.startContainer ? Math.min(range.startOffset, length) : 0;
        const localEnd = node === range.endContainer ? Math.min(range.endOffset, length) : length;
        if (localEnd > localStart) {
          start = start === null ? offset + localStart : Math.min(start, offset + localStart);
          end = end === null ? offset + localEnd : Math.max(end, offset + localEnd);
        }
      }
      offset += length;
    }

    if (start !== null && end !== null && end > start) hits.push({ key, start, end });
  }

  return hits;
}

/** Merges touching or overlapping marks of the same kind. */
function merge(marks: Mark[]): Mark[] {
  const sorted = marks.slice().sort((a, b) => a.start - b.start || a.end - b.end);
  const out: Mark[] = [];
  for (const mark of sorted) {
    const last = out[out.length - 1];
    if (last && last.kind === mark.kind && mark.start <= last.end) {
      last.end = Math.max(last.end, mark.end);
    } else {
      out.push({ ...mark });
    }
  }
  return out;
}

/** Removes a span from every mark of one kind, splitting marks as needed. */
function cut(marks: Mark[], kind: MarkKind, start: number, end: number): Mark[] {
  const out: Mark[] = [];
  for (const mark of marks) {
    if (mark.kind !== kind || mark.end <= start || mark.start >= end) {
      out.push(mark);
      continue;
    }
    if (mark.start < start) out.push({ ...mark, end: start });
    if (mark.end > end) out.push({ ...mark, start: end });
  }
  return out;
}

/** True when every character of the span already carries this kind of mark. */
function fullyMarked(marks: Mark[], kind: MarkKind, start: number, end: number): boolean {
  let cursor = start;
  for (const mark of merge(marks.filter(item => item.kind === kind))) {
    if (mark.start > cursor) return false;
    cursor = Math.max(cursor, mark.end);
    if (cursor >= end) return true;
  }
  return cursor >= end;
}

/**
 * Applies the tool to the current selection, toggling: selecting text that is
 * already fully highlighted and pressing Highlight again clears it, which is
 * how the real interface behaves.
 */
export function applyTool(current: MarkMap, kind: MarkKind, hits: Hit[]): MarkMap {
  if (!hits.length) return current;
  const next: MarkMap = { ...current };
  // One mixed selection is treated as a single gesture: if every region is
  // already marked, the gesture clears; otherwise it marks.
  const clearing = hits.every(hit => fullyMarked(next[hit.key] ?? [], kind, hit.start, hit.end));
  for (const hit of hits) {
    const existing = next[hit.key] ?? [];
    next[hit.key] = clearing
      ? cut(existing, kind, hit.start, hit.end)
      : merge([...existing, { start: hit.start, end: hit.end, kind }]);
  }
  return next;
}

export interface Piece {
  text: string;
  highlight: boolean;
  strike: boolean;
}

/** Splits a string into pieces carrying the marks that cover them. */
export function pieces(text: string, marks: Mark[] = []): Piece[] {
  if (!marks.length) return [{ text, highlight: false, strike: false }];
  const bounds = new Set<number>([0, text.length]);
  for (const mark of marks) {
    if (mark.start > 0 && mark.start < text.length) bounds.add(mark.start);
    if (mark.end > 0 && mark.end < text.length) bounds.add(mark.end);
  }
  const edges = [...bounds].sort((a, b) => a - b);
  const out: Piece[] = [];
  for (let index = 0; index < edges.length - 1; index += 1) {
    const start = edges[index];
    const end = edges[index + 1];
    if (end <= start) continue;
    out.push({
      text: text.slice(start, end),
      highlight: marks.some(mark => mark.kind === "highlight" && mark.start <= start && mark.end >= end),
      strike: marks.some(mark => mark.kind === "strike" && mark.start <= start && mark.end >= end),
    });
  }
  return out;
}

/** Clears the browser's selection after a tool has been applied. */
export function dropSelection() {
  if (typeof window === "undefined") return;
  window.getSelection()?.removeAllRanges();
}
