import { auth } from "@/auth";
import { isAdmin, validateCall } from "@/lib/engagement";
import { portalDb } from "@/lib/portal-db";
import { saveCall } from "@/lib/portal-store";
async function change(request: Request, context: { params: Promise<{ id: string }> }, cancel: boolean) {
  const email = (await auth())?.user?.email;
  if (!email) return Response.json({ error: "Please sign in." }, { status: 401 });
  if (!isAdmin(email)) return Response.json({ error: "Administrator access required." }, { status: 403 });
  const { id } = await context.params;
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(id)) return Response.json({ error: "Invalid call." }, { status: 400 });
  let input;
  if (!cancel) {
    try { input = validateCall(await request.json()); }
    catch (error) { return Response.json({ error: error instanceof Error ? error.message : "Invalid call." }, { status: 400 }); }
  }
  try {
    const db = await portalDb();
    const found = cancel
      ? (await db.query("UPDATE vitalis_calls SET cancelled=TRUE WHERE id=$1 RETURNING id", [id])).rows.length > 0
      : await saveCall(db, input!, email, id, true);
    return found ? Response.json({ saved: true }) : Response.json({ error: "Call not found." }, { status: 404 });
  } catch { return Response.json({ error: "Could not update the call. Please retry." }, { status: 503 }); }
}
export async function PATCH(request: Request, context: { params: Promise<{ id: string }> }) { return change(request, context, false); }
export async function DELETE(request: Request, context: { params: Promise<{ id: string }> }) { return change(request, context, true); }
