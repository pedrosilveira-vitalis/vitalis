import Link from "next/link";
import { auth, signOut } from "@/auth";

export default async function UserNav() {
  const session = await auth();

  if (!session?.user) {
    return (
      <Link
        href="/sign-in"
        className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-4 py-2.5 rounded-full hover:bg-[#1a2c4a] transition-colors"
      >
        Sign in →
      </Link>
    );
  }

  const initials = (session.user.name || session.user.email || "?")
    .split(" ")
    .map((s) => s[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();

  return (
    <div className="flex items-center gap-3">
      {session.user.image ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={session.user.image}
          alt={session.user.name || "User"}
          className="w-8 h-8 rounded-full border border-[#0c1a2e25]"
        />
      ) : (
        <div className="w-8 h-8 rounded-full bg-[#0c1a2e] text-[#f5f1ea] flex items-center justify-center font-mono text-[11px] font-medium">
          {initials}
        </div>
      )}
      <form
        action={async () => {
          "use server";
          await signOut({ redirectTo: "/" });
        }}
      >
        <button
          type="submit"
          className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-60 hover:opacity-100 transition-opacity"
        >
          Sign out
        </button>
      </form>
    </div>
  );
}