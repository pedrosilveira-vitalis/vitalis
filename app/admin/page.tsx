import Link from "next/link";
import { auth } from "@/auth";
import { isAdmin } from "@/lib/engagement";
import MainNav from "@/components/MainNav";
import AdminOverview from "@/components/AdminOverview";

export default async function AdminPage() {
  const email = (await auth())?.user?.email;

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[900px] h-[500px] bg-[#245574] opacity-[0.05] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
      </div>
      <div className="relative z-10">
        <MainNav badge="Admin" />
        <section className="px-10 pt-14 pb-8 border-b border-[#0c1a2e15]">
          <div className="font-sans text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Vitalis admin
          </div>
          <h1 className="font-sans font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(40px,5vw,72px)]">
            Who&rsquo;s here, and <span className="italic font-light text-[#245574]">what they bought.</span>
          </h1>
        </section>

        {!email ? (
          <section className="px-10 py-12">
            <p className="text-[15px] opacity-70">
              <Link href="/sign-in?next=%2Fadmin" className="underline">Sign in</Link> with your administrator
              account.
            </p>
          </section>
        ) : !isAdmin(email) ? (
          <section className="px-10 py-12">
            <p className="text-[15px] opacity-70 max-w-xl">
              This page is for the Vitalis administrator.{" "}
              <Link href="/study" className="underline">Back to studying &rarr;</Link>
            </p>
          </section>
        ) : (
          <AdminOverview />
        )}
      </div>
    </div>
  );
}
