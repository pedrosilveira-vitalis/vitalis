import type { CSSProperties } from 'react';
export default function StudyIcon({ name, style }: { name: string; style?: CSSProperties }) {
 const paths: Record<string, React.ReactNode> = {
 home: <><path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1Z"/><path d="M9 21v-8h6v8"/></>,
 book: <><path d="M12 5v16M3 4c4-1 6 0 9 2 3-2 5-3 9-2v15c-4-1-6 0-9 2-3-2-5-3-9-2Z"/></>,
 practice: <><rect x="5" y="3" width="14" height="19" rx="2"/><path d="m8 10 2 2 5-5M8 16h8"/></>,
 cards: <><rect x="7" y="7" width="14" height="14" rx="2"/><path d="M16 3H5a2 2 0 0 0-2 2v11M11 12h6m-6 4h4"/></>,
 tutor: <><path d="m12 2 2.7 7.3L22 12l-7.3 2.7L12 22l-2.7-7.3L2 12l7.3-2.7Z"/></>,
 calendar: <><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 2v6m10-6v6M3 11h18m-13 5h3m3 0h3"/></>,
 bio: <><path d="M7 2c0 8 10 12 10 20M17 2c0 8-10 12-10 20M7 4h10M8 8h8m-8 8h8m-9 4h10"/></>,
 atom: <><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(-45 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(45 12 12)"/><circle cx="12" cy="12" r="1"/></>,
 people: <><circle cx="9" cy="7" r="3"/><path d="M2 21v-3a7 7 0 0 1 14 0v3M17 4a3 3 0 0 1 0 6m2 4a5 5 0 0 1 3 5v2"/></>,
 voice: <><rect x="8" y="2" width="8" height="13" rx="4"/><path d="M4 10v2a8 8 0 0 0 16 0v-2m-8 10v3m-4 0h8"/></>,
 score: <><path d="M4 21V12m8 9V3m8 18V8"/></>,
 arrow: <path d="M4 12h16m-6-6 6 6-6 6"/>,
 };
 return <svg style={style} className="study-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.65" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name] || paths.book}</svg>;
}
