import { auth } from "@/auth";
import { isAdmin, validateCall } from "@/lib/engagement";
import { portalDb } from "@/lib/portal-db";
import { getCalls, saveCall } from "@/lib/portal-store";
export async function GET(request: Request) {
  const email = (await auth())?.user?.email;
  if (!email) return Response.json({ error: "Sign in to view your calls." }, { status: 401 });
  const admin = new URL(request.url).searchParams.get("manage") === "1";
  if (admin && !isAdmin(email)) return Response.json({ error: "Administrator access required." }, { status: 403 });
  try { return Response.json({ calls: await getCalls(await portalDb(), email, admin), isAdmin: isAdmin(email) }, { headers: { "Cache-Control": "no-store" } }); }
  catch { return Response.json({ error: "Could not load calls. Please retry." }, { status: 503 }); }
}
export async function POST(request: Request) {
  const email = (await auth())?.user?.email;
  if (!email) return Response.json({ error: "Please sign in." }, { status: 401 });
  if (!isAdmin(email)) return Response.json({ error: "Administrator access required." }, { status: 403 });
  let input, id;
  try {
    const raw = await request.json();
    input = validateCall(raw); id = raw.id;
    if (typeof id !== "string" || !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(id)) throw new Error("Invalid appointment identifier.");
  } catch (error) { return Response.json({ error: error instanceof Error ? error.message : "Invalid call." }, { status: 400 }); }
  try { await saveCall(await portalDb(), input, email, id); return Response.json({ saved: true }, { status: 201 }); }
  catch { return Response.json({ error: "Could not save the call. Please retry." }, { status: 503 }); }
}
