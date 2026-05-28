"use client";

import Link from "next/link";
import UserNav from "./UserNav";

type NavLink = {
  href: string;
  label: string;
};

const NAV_LINKS: NavLink[] = [
  { href: "/", label: "Home" },
  { href: "/tutor", label: "Tutor" },
  { href: "/practice", label: "Practice" },
  { href: "/flashcards", label: "Flashcards" },
  { href: "/study", label: "Study" },
  { href: "/study-plan", label: "My Plan" },
  { href: "/voice-cases", label: "Voice Cases" },
  { href: "/score-calculator", label: "Score Calc" },
];

function Logo() {
  return (
    <Link href="/" className="flex items-center gap-2.5">
      <svg width="36" height="20" viewBox="0 0 60 28" fill="none" className="flex-shrink-0">
        <path
          d="M2 14 L12 14 L16 6 L22 22 L28 4 L34 18 L38 14 L48 14"
          stroke="#a8324a"
          strokeWidth="2.4"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        <circle cx="50" cy="14" r="2.2" fill="#a8324a" />
      </svg>
      <span className="font-serif font-semibold text-[22px] tracking-tight text-[#0c1a2e]">Vitalis</span>
    </Link>
  );
}

type MainNavProps = {
  active?: string;
  badge?: string;
  rightSlot?: React.ReactNode;
  compact?: boolean;
};

export default function MainNav({ active, badge, rightSlot, compact }: MainNavProps) {
  return (
    <nav className={`flex items-center justify-between border-b border-[#0c1a2e15] bg-[#f5f1ea] ${compact ? "px-8 py-4" : "px-10 py-5"}`}>
      <Logo />
      <div className="hidden md:flex gap-5 text-sm font-medium">
        {NAV_LINKS.map((link) => {
          const isActive =
            active === link.label.toLowerCase().replace(/\s+/g, "-") ||
            active === link.label.toLowerCase() ||
            (active && link.href === `/${active}`);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={
                isActive
                  ? "opacity-100 border-b border-[#a8324a] pb-0.5"
                  : "opacity-60 hover:opacity-100 transition-opacity"
              }
            >
              {link.label}
            </Link>
          );
        })}
      </div>
      <div className="flex items-center gap-3">
        {badge && (
          <div className="font-mono text-[11px] tracking-[0.12em] uppercase opacity-50">{badge}</div>
        )}
        {rightSlot ?? <UserNav />}
      </div>
    </nav>
  );
}