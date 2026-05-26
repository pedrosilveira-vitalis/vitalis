import Link from "next/link";
import { signIn } from "@/auth";

function Logo() {
  return (
    <div className="flex items-center gap-2.5">
      <svg width="36" height="20" viewBox="0 0 60 28" fill="none" className="flex-shrink-0">
        <path d="M2 14 L12 14 L16 6 L22 22 L28 4 L34 18 L38 14 L48 14" stroke="#a8324a" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" fill="none" />
        <circle cx="50" cy="14" r="2.2" fill="#a8324a" />
      </svg>
      <span className="font-serif font-semibold text-[22px] tracking-tight text-[#0c1a2e]">Vitalis</span>
    </div>
  );
}

export default function SignInPage() {
  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans flex flex-col">
      <header className="flex items-center justify-between px-10 py-5 border-b border-[#0c1a2e15]">
        <Link href="/">
          <Logo />
        </Link>
        <Link href="/" className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-60 hover:opacity-100">
          ← Back home
        </Link>
      </header>

      <div className="flex-1 flex items-center justify-center px-8 py-14">
        <div className="w-full max-w-md">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
            <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
            Sign in
          </div>
          <h1 className="font-serif text-[clamp(36px,5vw,56px)] font-medium leading-[1.05] tracking-tight mb-3">
            Welcome to <span className="italic font-light text-[#a8324a]">Vitalis.</span>
          </h1>
          <p className="text-[14px] opacity-70 leading-relaxed mb-10">
            Sign in to save your progress, build custom flashcards, and access your tutor conversation history.
          </p>

          <form
            action={async () => {
              "use server";
              await signIn("google", { redirectTo: "/" });
            }}
          >
            <button
              type="submit"
              className="w-full flex items-center justify-center gap-3 px-5 py-3.5 border-2 border-[#0c1a2e25] rounded-xl hover:bg-[#0c1a2e08] transition-colors font-medium text-[15px]"
            >
              <svg width="20" height="20" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
              </svg>
              Sign in with Google
            </button>
          </form>

          <div className="mt-6 text-center font-mono text-[10px] tracking-[0.1em] uppercase opacity-50">
            Microsoft sign-in coming next
          </div>
        </div>
      </div>
    </div>
  );
}