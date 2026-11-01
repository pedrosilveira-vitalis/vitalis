"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import UserNav from "./UserNav";

const links = [
  { href: '/', label: 'Overview', symbol: '◫' },
  { href: '/practice', label: 'Practice', symbol: '◎' },
  { href: '/study', label: 'Lessons', symbol: '▤' },
  { href: '/flashcards', label: 'Flashcards', symbol: '▱' },
  { href: '/tutor', label: 'AI Tutor', symbol: '✦' },
  { href: '/study-plan', label: 'Study Plan', symbol: '▦' },
];
const extra = [{ href: '/voice-cases', label: 'Voice Cases', symbol: '◌' }, { href: '/score-calculator', label: 'Score Calculator', symbol: '∑' }];
function Logo() {
  return <Link href="/" className="flex items-center gap-2 text-[#0c1a2e]" aria-label="Vitalis home"><svg width="30" height="25" viewBox="0 0 50 30" fill="none" aria-hidden="true"><path d="M1 15h10l5-9 7 19 7-23 7 18 4-5h8" stroke="#a8324a" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg><span className="font-serif text-3xl tracking-tight font-semibold">Vitalis</span></Link>;
}
export default function MainNav({ badge, rightSlot }: { active?: string; badge?: string; rightSlot?: React.ReactNode; compact?: boolean }) {
  const pathname = usePathname();
  const selected = (href: string) => href === '/' ? pathname === '/' : pathname === href || pathname.startsWith(href + '/');
  const renderLink = (link: typeof links[number]) => <Link key={link.href} href={link.href} aria-current={selected(link.href) ? 'page' : undefined} className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm transition-colors ${selected(link.href) ? 'bg-[#a8324a10] text-[#972d43] font-semibold' : 'text-[#52606c] hover:bg-[#0c1a2e08] hover:text-[#0c1a2e]'}`}><span aria-hidden="true" className="text-xl w-5 text-center">{link.symbol}</span>{link.label}</Link>;
  return <>
    <a href="#page-content" className="skip-link">Skip to content</a>
    <aside className="vitalis-sidebar"><div className="px-4 pt-8 pb-10"><Logo /><p className="mt-3 text-[10px] tracking-[0.18em] uppercase text-[#768079]">For the physician in you</p></div><nav aria-label="Main navigation" className="space-y-1">{links.map(renderLink)}<p className="px-4 pt-8 pb-2 text-[10px] font-semibold uppercase tracking-widest text-[#788087]">Explore</p>{extra.map(renderLink)}</nav><div className="mt-auto p-4 pt-12"><div className="border-t border-[#0c1a2e15] pt-5 text-xs leading-6 text-[#68717b]">A little progress, every day.<br /><span className="text-[#a8324a]">Your next step starts here.</span></div></div></aside>
    <header className="vitalis-topbar"><div className="lg:hidden"><Logo /></div><div className="hidden lg:block text-sm text-[#68717b]">{badge || 'Your MCAT study space'}</div><div className="flex items-center gap-4">{rightSlot ?? <UserNav />}<details key={pathname} className="lg:hidden relative"><summary className="cursor-pointer border border-[#0c1a2e25] rounded-lg px-3 py-2 text-sm">Menu</summary><nav aria-label="Mobile navigation" className="absolute right-0 top-12 w-64 bg-[#fcfaf6] rounded-2xl border border-[#0c1a2e20] shadow-xl p-3 z-50">{[...links,...extra].map(renderLink)}</nav></details></div></header>
    <span id="page-content" tabIndex={-1} />
  </>;
}
