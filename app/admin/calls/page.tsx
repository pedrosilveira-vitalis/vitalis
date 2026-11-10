import { auth } from "@/auth";
import { isAdmin } from "@/lib/engagement";
import Link from "next/link";
import MainNav from "@/components/MainNav";
import CallManager from "@/components/CallManager";
export default async function AdminCallsPage() {
  const email = (await auth())?.user?.email;
  return <><MainNav contentId="manage-calls" badge="Schedule calls"/><main id="manage-calls" className="portal-page"><p className="eyebrow">VITALIS ADMIN</p><h1>Make time for your students.</h1>
    {!email ? <p><Link href="/sign-in">Sign in</Link> with your administrator account to schedule calls.</p> : !isAdmin(email) ? <p>This page is available to your Vitalis administrator. <Link href="/calls">View your own calls →</Link></p> : <CallManager/>}
  </main></>;
}
