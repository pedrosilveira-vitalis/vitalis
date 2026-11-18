import Nori from "./Nori";
import type { TourPose, TourProp } from "@/lib/tour";

/**
 * Nori holding a different prop and standing a different way for each step of
 * the tour. One shared character drawing; the pose is a CSS class and the prop
 * is an SVG layered behind, so there is no second Nori to keep in sync.
 */
const PROPS: Record<TourProp, React.ReactNode> = {
  calendar: (
    <g stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round">
      <rect x="48" y="34" width="104" height="92" rx="12" fill="#fffdf7" fillOpacity=".92" />
      <path d="M48 62h104" />
      <path d="M74 34V20M126 34V20" />
      <circle cx="78" cy="86" r="6" fill="currentColor" opacity=".45" stroke="none" />
      <circle cx="100" cy="86" r="6" fill="currentColor" opacity=".3" stroke="none" />
      <path d="M116 104l9 9 18-20" strokeWidth="8" />
    </g>
  ),
  book: (
    <g stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round">
      <path d="M100 48c-14-12-34-14-50-10v74c16-4 36-2 50 10 14-12 34-14 50-10V38c-16-4-36-2-50 10z" fill="#fffdf7" fillOpacity=".9" />
      <path d="M100 48v74" strokeWidth="6" />
      <path d="M66 62h20M66 80h20M114 62h20M114 80h20" strokeWidth="5" opacity=".55" />
    </g>
  ),
  cards: (
    <g stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round">
      <rect x="44" y="46" width="76" height="84" rx="10" fill="#fffdf7" fillOpacity=".85" transform="rotate(-9 82 88)" />
      <rect x="80" y="38" width="76" height="84" rx="10" fill="#fffdf7" fillOpacity=".95" transform="rotate(7 118 80)" />
      <path d="M96 66h44M96 84h44M96 102h26" strokeWidth="6" opacity=".55" />
    </g>
  ),
  clipboard: (
    <g stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round">
      <rect x="56" y="30" width="88" height="100" rx="12" fill="#fffdf7" fillOpacity=".92" />
      <rect x="84" y="18" width="32" height="20" rx="8" fill="currentColor" opacity=".3" />
      <path d="M74 64l9 9 16-18M74 98l9 9 16-18" strokeWidth="7" />
      <path d="M112 68h20M112 102h20" strokeWidth="6" opacity=".5" />
    </g>
  ),
  chat: (
    <g stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round">
      <path d="M46 40h108v62H92l-24 22V102H46z" fill="#fffdf7" fillOpacity=".92" />
      <circle cx="78" cy="70" r="5" fill="currentColor" stroke="none" opacity=".55" />
      <circle cx="100" cy="70" r="5" fill="currentColor" stroke="none" opacity=".45" />
      <circle cx="122" cy="70" r="5" fill="currentColor" stroke="none" opacity=".35" />
    </g>
  ),
  headset: (
    <g stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round">
      <path d="M54 94V74a46 46 0 0 1 92 0v20" fill="none" />
      <rect x="38" y="88" width="26" height="40" rx="12" fill="#fffdf7" fillOpacity=".92" />
      <rect x="136" y="88" width="26" height="40" rx="12" fill="#fffdf7" fillOpacity=".92" />
      <path d="M100 36v-14" strokeWidth="6" />
      <circle cx="100" cy="16" r="7" fill="currentColor" stroke="none" opacity=".4" />
    </g>
  ),
  chart: (
    <g stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round">
      <rect x="44" y="34" width="112" height="94" rx="12" fill="#fffdf7" fillOpacity=".92" />
      <path d="M64 108V86M90 108V66M116 108V76M136 108V52" strokeWidth="9" />
    </g>
  ),
  lock: (
    <g stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round">
      <rect x="56" y="70" width="88" height="62" rx="14" fill="#fffdf7" fillOpacity=".92" />
      <path d="M74 70V54a26 26 0 0 1 52 0v16" fill="none" />
      <circle cx="100" cy="98" r="8" fill="currentColor" stroke="none" opacity=".45" />
      <path d="M100 106v10" strokeWidth="6" />
    </g>
  ),
};

export default function NoriPose({
  prop,
  pose,
  accent,
  className = "",
}: {
  prop: TourProp;
  pose: TourPose;
  accent: string;
  className?: string;
}) {
  return (
    <div className={`nori-pose nori-pose-${pose} ${className}`} aria-hidden="true">
      <svg viewBox="0 0 200 150" className="nori-pose-prop" style={{ color: accent }}>
        {PROPS[prop]}
      </svg>
      <Nori className="nori-pose-art" />
    </div>
  );
}
