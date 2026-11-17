import Nori from "./Nori";

/**
 * Nori holding something different for each subject. The character art is
 * shared rather than redrawn per subject: one Nori, a themed prop, and the
 * section's accent colour behind.
 */
const PROPS = {
  flask: (
    <g>
      <path d="M78 24h44M86 24v30L62 104a14 14 0 0 0 13 20h50a14 14 0 0 0 13-20l-24-50V24" fill="#ffffff" fillOpacity=".55" stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M70 92h60" stroke="currentColor" strokeWidth="6" strokeLinecap="round" />
      <circle cx="90" cy="106" r="5" fill="currentColor" opacity=".55" />
      <circle cx="112" cy="112" r="4" fill="currentColor" opacity=".4" />
    </g>
  ),
  cell: (
    <g>
      <circle cx="100" cy="78" r="52" fill="#ffffff" fillOpacity=".5" stroke="currentColor" strokeWidth="7" />
      <circle cx="100" cy="78" r="22" fill="currentColor" fillOpacity=".3" stroke="currentColor" strokeWidth="6" />
      <circle cx="68" cy="56" r="7" fill="currentColor" opacity=".45" />
      <circle cx="132" cy="98" r="8" fill="currentColor" opacity=".35" />
      <circle cx="126" cy="50" r="5" fill="currentColor" opacity=".4" />
    </g>
  ),
  brain: (
    <g stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" fill="none">
      <path d="M100 32c-16-10-36-2-38 16-14 4-18 22-8 32-8 12 0 28 14 30 4 14 22 20 32 10z" fill="#ffffff" fillOpacity=".5" />
      <path d="M100 32c16-10 36-2 38 16 14 4 18 22 8 32 8 12 0 28-14 30-4 14-22 20-32 10z" fill="#ffffff" fillOpacity=".35" />
      <path d="M100 32v88M78 60c8 4 10 12 8 20M124 66c-8 4-10 12-8 20" strokeWidth="5" />
    </g>
  ),
  book: (
    <g stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round">
      <path d="M100 48c-14-12-34-14-50-10v74c16-4 36-2 50 10 14-12 34-14 50-10V38c-16-4-36-2-50 10z" fill="#ffffff" fillOpacity=".55" />
      <path d="M100 48v74" strokeWidth="6" />
      <path d="M66 62h20M66 80h20M114 62h20M114 80h20" strokeWidth="5" opacity=".6" />
    </g>
  ),
} as const;

export default function NoriSubject({
  prop,
  accent,
  className = "",
}: {
  prop: keyof typeof PROPS;
  accent: string;
  className?: string;
}) {
  return (
    <div className={`relative ${className}`} aria-hidden="true">
      <svg viewBox="0 0 200 150" className="absolute -top-2 left-1/2 -translate-x-1/2 w-[58%]" style={{ color: accent }}>
        {PROPS[prop]}
      </svg>
      <Nori className="relative w-full" />
    </div>
  );
}
