import { auth } from "@/auth";
import { validTimeZone } from "@/lib/engagement";
import { portalDb } from "@/lib/portal-db";
import { activity } from "@/lib/portal-store";
import { questionToken, validQuestionToken } from "@/lib/question-token";
export async function POST(request: Request) {
  const session = await auth();
  if (!session?.user?.email) return Response.json({ error: "Sign in to save your streak." }, { status: 401 });
  let input;
  try { input = await request.json(); } catch { return Response.json({ error: "Invalid request." }, { status: 400 }); }
  if (!input || !validTimeZone(input.timeZone) || !["visit", "answer"].includes(input.kind)) return Response.json({ error: "Invalid activity." }, { status: 400 });
  if (input.kind === "answer" && (!validQuestionToken(input.token) || !["A", "B", "C", "D"].includes(input.answer))) {
    return Response.json({ error: "Reload the questions and submit an answer to save today's practice." }, { status: 400 });
  }
  try {
    const result = await activity(await portalDb(), session.user.email, input.timeZone, input.kind === "answer");
    return Response.json({ ...result, warmupToken: questionToken("dashboard-warmup") }, { headers: { "Cache-Control": "no-store" } });
  } catch {
    return Response.json({ error: "Your progress could not be saved. Please retry." }, { status: 503 });
  }
}
