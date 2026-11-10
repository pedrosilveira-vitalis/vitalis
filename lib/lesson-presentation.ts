/** Split at a reviewed, exact H2 boundary, retaining every source character. */
export function splitLessonForVisual(content: string, beforeHeading?: string): [string, string] {
  if (!beforeHeading) return [content, ""];
  const escaped = beforeHeading.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = new RegExp(`^## ${escaped}\\r?$`, "m").exec(content);
  return match ? [content.slice(0, match.index), content.slice(match.index)] : [content, ""];
}
