import { auth } from "@/auth";
import { entitlementFor, hasStandingAccess } from "@/lib/billing";
import { portalDb } from "@/lib/portal-db";

const NO_STORE = { headers: { "Cache-Control": "no-store" } };

export async function GET() {
  const session = await auth();
  const email = session?.user?.email;
  if (!email) return Response.json({ signedIn: false, entitlement: null }, NO_STORE);

  if (hasStandingAccess(email)) {
    return Response.json({ signedIn: true, standing: true, entitlement: { plan: "complete", daysLeft: null } }, NO_STORE);
  }
  try {
    const entitlement = await entitlementFor(await portalDb(), email);
    return Response.json(
      { signedIn: true, entitlement: entitlement && { plan: entitlement.plan, daysLeft: entitlement.daysLeft, expiresAt: entitlement.expiresAt } },
      NO_STORE,
    );
  } catch {
    return Response.json({ signedIn: true, entitlement: null }, NO_STORE);
  }
}
