import { auth } from "@/auth";
import { entitlementFor } from "@/lib/billing";
import { portalDb } from "@/lib/portal-db";

export async function GET() {
  const session = await auth();
  if (!session?.user?.email) {
    return Response.json({ signedIn: false, entitlement: null }, { headers: { "Cache-Control": "no-store" } });
  }
  try {
    const entitlement = await entitlementFor(await portalDb(), session.user.email);
    return Response.json(
      { signedIn: true, entitlement: entitlement && { plan: entitlement.plan, daysLeft: entitlement.daysLeft, expiresAt: entitlement.expiresAt } },
      { headers: { "Cache-Control": "no-store" } },
    );
  } catch {
    return Response.json({ signedIn: true, entitlement: null }, { headers: { "Cache-Control": "no-store" } });
  }
}
