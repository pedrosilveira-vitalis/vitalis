import { auth } from "@/auth";
import { entitlementFor, hasStandingAccess } from "@/lib/billing";
import { isAdmin } from "@/lib/engagement";
import { portalDb } from "@/lib/portal-db";

const NO_STORE = { headers: { "Cache-Control": "no-store" } };

export async function GET() {
  const session = await auth();
  const email = session?.user?.email;
  if (!email) return Response.json({ signedIn: false, entitlement: null }, NO_STORE);

  const standing = isAdmin(email) || hasStandingAccess(email);
  try {
    const entitlement = await entitlementFor(await portalDb(), email);
    if (entitlement) {
      return Response.json(
        {
          signedIn: true,
          standing,
          entitlement: { plan: entitlement.plan, daysLeft: entitlement.daysLeft, expiresAt: entitlement.expiresAt },
        },
        NO_STORE,
      );
    }
  } catch {
    // Fall through: standing access should still work if the database blinks.
  }
  if (standing) {
    return Response.json({ signedIn: true, standing: true, entitlement: { plan: "complete", daysLeft: null } }, NO_STORE);
  }
  return Response.json({ signedIn: true, standing: false, entitlement: null }, NO_STORE);
}
