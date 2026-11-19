"use client";
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import Nori from './Nori';
import UserNav from './UserNav';
import StudyIcon from './StudyIcon';
import { TOUR_EVENT } from './WelcomeTour';
const groups = [
 { title: 'Your workspace', links: [{href:'/',label:'Home',icon:'home'},{href:'/study-plan',label:'Study planner',icon:'calendar'},{href:'/tutor',label:'Ask Nori',icon:'tutor'},{href:'/calls',label:'Your calls',icon:'calendar'}]},
 { title: 'Learn & practice', links: [{href:'/study',label:'Study guides',icon:'book'},{href:'/cheatsheets',label:'Cheat sheets',icon:'cards'},{href:'/practice',label:'Practice questions',icon:'practice'},{href:'/exams',label:'Full-length exams',icon:'score'},{href:'/exams/scores',label:'Score history',icon:'score'},{href:'/flagged',label:'Flagged questions',icon:'book'},{href:'/flashcards',label:'Flashcards',icon:'cards'}]},
 { title: 'Explore', links: [{href:'/resume',label:'Résumé builder',icon:'book'},{href:'/medical-news',label:'Medical news',icon:'book'},{href:'/voice-cases',label:'Voice cases',icon:'voice'},{href:'/score-calculator',label:'Score calculator',icon:'score'}]},
];
const adminGroup = { title: 'Admin', links: [{href:'/admin',label:'Students & revenue',icon:'score'},{href:'/admin/calls',label:'Schedule sessions',icon:'calendar'}]};
function Logo() { return <Link href="/" className="vitalis-brand" aria-label="Vitalis home"><Nori className="brand-nori"/><span>Vitalis<span className="brand-dot">.</span></span></Link>; }
export default function MainNav({badge,rightSlot,contentId}: {contentId?:string;active?:string;badge?:string;rightSlot?:React.ReactNode;compact?:boolean}) {
 const pathname=usePathname();
 const [admin,setAdmin]=useState(false);
 // Someone who has already paid should not be looking at a tab that sells
 // them the thing they own. Once a plan is live the sales tab becomes "Your
 // access" — renewals still need a door — and the tour becomes replayable.
 const [paid,setPaid]=useState<boolean|null>(null);
 useEffect(()=>{let live=true;fetch('/api/session').then(r=>r.json()).then(d=>{if(live)setAdmin(!!d.isAdmin);}).catch(()=>{});return()=>{live=false;};},[]);
 useEffect(()=>{let live=true;fetch('/api/entitlement').then(r=>r.json()).then(d=>{if(live)setPaid(!!d.entitlement);}).catch(()=>{if(live)setPaid(false);});return()=>{live=false;};},[]);
 const accountGroup={title:'Account',links:[paid?{href:'/plans',label:'Your access',icon:'score'}:{href:'/plans',label:'Plans & access',icon:'score'}]};
 const workspace=paid?{...groups[0],links:[...groups[0].links,{href:'#tour',label:'Tour of your plan',icon:'tutor'}]}:groups[0];
 const shown=[workspace,...groups.slice(1),accountGroup,...(admin?[adminGroup]:[])];
 const selected=(href:string)=>href==='/'?pathname==='/':pathname===href||pathname.startsWith(href+'/');
 const navigation=shown.map(group=><div className="nav-group" key={group.title}><p>{group.title}</p>{group.links.map(link=>link.href==='#tour'?<button key={link.href} type="button" className="nav-item" onClick={()=>window.dispatchEvent(new Event(TOUR_EVENT))}><StudyIcon name={link.icon}/>{link.label}</button>:<Link key={link.href} href={link.href} className="nav-item" aria-current={selected(link.href)?'page':undefined}><StudyIcon name={link.icon}/>{link.label}</Link>)}</div>);
 return <><a href={`#${contentId || "page-content"}`} className="skip-link">Skip to content</a><aside className="vitalis-sidebar"><div className="sidebar-brand"><Logo/><span className="brand-caption">MCAT PREPARATION</span></div><nav className="min-h-0 overflow-y-auto" aria-label="Main navigation">{navigation}</nav><div className="sidebar-note"><span>THE PHYSICIAN IN YOU</span><p>Built one concept<br/>at a time.</p><Link href="/study-plan">Find your study rhythm <span aria-hidden="true">↗</span></Link></div></aside><header className="vitalis-topbar"><div className="mobile-brand"><Logo/></div><div className="desktop-breadcrumb">Your workspace <span>/</span> <strong>{badge || shown.flatMap(g=>g.links).find(l=>selected(l.href))?.label || 'MCAT'}</strong></div><div className="topbar-actions">{rightSlot ?? <UserNav/>}<details key={pathname} className="mobile-menu"><summary>Menu</summary><nav aria-label="Mobile navigation">{navigation}</nav></details></div></header>{!contentId && <div id="page-content" tabIndex={-1} className="content-start"/>}</>;
}
