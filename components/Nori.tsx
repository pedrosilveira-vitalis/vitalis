import { useId } from "react";
export default function Nori({ className = "" }: { className?: string }) {
  const id = useId().replace(/:/g, "");
  return <svg className={`nori-art ${className}`} viewBox="0 0 200 210" fill="none" aria-hidden="true">
    <defs>
      <linearGradient id={id} x1="75" y1="75" x2="148" y2="180" gradientUnits="userSpaceOnUse"><stop stopColor="#ffe3c8"/><stop offset=".46" stopColor="#f6b99f"/><stop offset="1" stopColor="#df847e"/></linearGradient>
    </defs>
    <ellipse cx="102" cy="197" rx="46" ry="7" fill="#172f43" opacity=".12"/>
    <g stroke="#223d54" strokeWidth="8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M73 93 58 68 52 38M58 68 33 60 28 49M101 87 104 49 118 30 119 17M104 49 88 35 85 22M131 91 149 65 155 39M149 65 172 62 181 51"/>
      <path d="M153 147c39-32 44 6 18 15l-18 5" strokeWidth="6"/>
      <path d="m78 168-5 20h-10m63-20 8 20h10"/>
      <path d="M101 76c-12 15-51 22-54 57-5 54 100 64 107 8 4-32-25-48-53-65Z" fill={`url(#${id})`}/>
      <path d="M51 145c-24-9-24 22-12 19m0-10v10m7-11v9m105-18c19-6 27 18 17 21m-1-10 1 10m-9-10 1 8" fill="#f8c4a6" strokeWidth="5"/>
    </g>
    <path d="M67 113c4-10 13-13 20-17" stroke="#fff4e1" strokeWidth="7" strokeLinecap="round" opacity=".75"/>
    <g className="nori-eyes" fill="#223d54"><ellipse cx="80" cy="131" rx="5.5" ry="8"/><ellipse cx="120" cy="131" rx="5.5" ry="8"/></g>
    <ellipse cx="65" cy="145" rx="9" ry="5" fill="#e98286"/><ellipse cx="136" cy="145" rx="9" ry="5" fill="#e98286"/>
    <path d="M91 145q9 13 19 0" stroke="#223d54" strokeWidth="4.5" strokeLinecap="round"/>
    <circle cx="78" cy="128" r="1.7" fill="white"/><circle cx="118" cy="128" r="1.7" fill="white"/>
  </svg>;
}
