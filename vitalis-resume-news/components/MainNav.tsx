"use client";
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import UserNav from './UserNav';
import StudyIcon from './StudyIcon';
const groups = [
 { title: 'Your workspace', links: [{href:'/',label:'Home',icon:'home'},{href:'/study-plan',label:'Study planner',icon:'calendar'},{href:'/tutor',label:'AI tutor',icon:'tutor'}]},
 { title: 'Learn & practice', links: [{href:'/study',label:'Study guides',icon:'book'},{href:'/practice',label:'Practice questions',icon:'practice'},{href:'/flagged',label:'Flagged questions',icon:'book'},{href:'/flashcards',label:'Flashcards',icon:'cards'}]},
 { title: 'Explore', links: [{href:'/resume',label:'Résumé builder',icon:'book'},{href:'/medical-news',label:'Medical news',icon:'book'},{href:'/voice-cases',label:'Voice cases',icon:'voice'},{href:'/score-calculator',label:'Score calculator',icon:'score'}]},
];
function Logo() { return <Link href="/" className="vitalis-brand" aria-label="Vitalis home"><svg width="34" height="30" viewBox="0 0 50 30" fill="none" aria-hidden="true"><path d="M1 15h10l5-9 7 19 7-23 7 18 4-5h8" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"/></svg><span>Vitalis<span className="brand-dot">.</span></span></Link>; }
export default function MainNav({badge,rightSlot,contentId}: {contentId?:string;active?:string;badge?:string;rightSlot?:React.ReactNode;compact?:boolean}) {
 const pathname=usePathname();
 const selected=(href:string)=>href==='/'?pathname==='/':pathname===href||pathname.startsWith(href+'/');
 const navigation=groups.map(group=><div className="nav-group" key={group.title}><p>{group.title}</p>{group.links.map(link=><Link key={link.href} href={link.href} className="nav-item" aria-current={selected(link.href)?'page':undefined}><StudyIcon name={link.icon}/>{link.label}</Link>)}</div>);
 return <><a href={`#${contentId || "page-content"}`} className="skip-link">Skip to content</a><aside className="vitalis-sidebar"><div className="sidebar-brand"><Logo/><span className="brand-caption">MCAT PREPARATION</span></div><nav className="min-h-0 overflow-y-auto" aria-label="Main navigation">{navigation}</nav><div className="sidebar-note"><span>THE PHYSICIAN IN YOU</span><p>Built one concept<br/>at a time.</p><Link href="/study-plan">Find your study rhythm <span aria-hidden="true">↗</span></Link></div></aside><header className="vitalis-topbar"><div className="mobile-brand"><Logo/></div><div className="desktop-breadcrumb">Your workspace <span>/</span> <strong>{badge || groups.flatMap(g=>g.links).find(l=>selected(l.href))?.label || 'MCAT'}</strong></div><div className="topbar-actions">{rightSlot ?? <UserNav/>}<details key={pathname} className="mobile-menu"><summary>Menu</summary><nav aria-label="Mobile navigation">{navigation}</nav></details></div></header>{!contentId && <div id="page-content" tabIndex={-1} className="content-start"/>}</>;
}
