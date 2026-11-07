import { createHmac, timingSafeEqual } from "node:crypto";
function secret() { return process.env.AUTH_SECRET || process.env.NEXTAUTH_SECRET; }
export function questionToken(id: string, now = Date.now()) {
  const key = secret();
  if (!key) return undefined;
  const payload = Buffer.from(JSON.stringify({ id, issued: now })).toString("base64url");
  return payload + "." + createHmac("sha256", key).update(payload).digest("base64url");
}
export function validQuestionToken(token: unknown, now = Date.now()) {
  const key = secret();
  if (!key || typeof token !== "string" || token.length > 1200) return false;
  const parts = token.split(".");
  if (parts.length !== 2) return false;
  const expected = createHmac("sha256", key).update(parts[0]).digest();
  const supplied = Buffer.from(parts[1], "base64url");
  if (supplied.length !== expected.length || !timingSafeEqual(expected, supplied)) return false;
  try {
    const payload = JSON.parse(Buffer.from(parts[0], "base64url").toString());
    return typeof payload.id === "string" && typeof payload.issued === "number" &&
      payload.issued <= now && now - payload.issued <= 86400000;
  } catch { return false; }
}
export function withQuestionTokens<T extends { id: string | number }>(questions: T[]) {
  return questions.map(q => ({ ...q, activityToken: questionToken(String(q.id)) }));
}
