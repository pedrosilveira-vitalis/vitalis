import Link from "next/link";

/**
 * The pressable subject squares: a saturated gradient, oversized artwork
 * bleeding off the right edge, and a white Open pill. Each subject gets its
 * own drawing rather than a recoloured copy of one shape.
 */
type Art = "cell" | "flask" | "brain" | "book";

type Palette = { from: string; from2: string; to: string; ink: string };

const PALETTE: Record<Art, Palette> = {
  cell: { from: "#4e9c6b", from2: "#2f7a52", to: "#1f5c3e", ink: "#eafaf0" },
  flask: { from: "#5b6fd6", from2: "#4152b8", to: "#2e3a8c", ink: "#eef0ff" },
  brain: { from: "#d4587a", from2: "#b83f63", to: "#8f2f4e", ink: "#ffeef3" },
  book: { from: "#7b61d9", from2: "#5f46bd", to: "#432e96", ink: "#f1ecff" },
};

function Artwork({ art }: { art: Art }) {
  const common = { fill: "#ffffff" };
  if (art === "cell") {
    return (
      <g>
        <circle cx="300" cy="105" r="92" {...common} opacity=".16" />
        <circle cx="300" cy="105" r="60" {...common} opacity=".20" />
        <circle cx="300" cy="105" r="27" {...common} opacity=".55" />
        <circle cx="236" cy="52" r="15" {...common} opacity=".32" />
        <circle cx="372" cy="160" r="20" {...common} opacity=".26" />
        <circle cx="366" cy="48" r="10" {...common} opacity=".4" />
        <path d="M196 180c38-26 38-62 0-88s-38-62 0-88" stroke="#ffffff" strokeOpacity=".45" strokeWidth="9" fill="none" strokeLinecap="round" />
        <path d="M232 180c-38-26-38-62 0-88s38-62 0-88" stroke="#ffffff" strokeOpacity=".3" strokeWidth="9" fill="none" strokeLinecap="round" />
      </g>
    );
  }
  if (art === "flask") {
    return (
      <g>
        <circle cx="312" cy="96" r="96" {...common} opacity=".13" />
        <path d="M268 18h74M282 18v52l-44 86c-9 18 4 40 25 40h92c21 0 34-22 25-40l-44-86V18" fill="#ffffff" fillOpacity=".26" stroke="#ffffff" strokeOpacity=".75" strokeWidth="10" strokeLinejoin="round" strokeLinecap="round" />
        <path d="M250 128h128" stroke="#ffffff" strokeOpacity=".55" strokeWidth="9" strokeLinecap="round" />
        <circle cx="288" cy="152" r="11" {...common} opacity=".65" />
        <circle cx="330" cy="166" r="8" {...common} opacity=".5" />
        <circle cx="352" cy="140" r="6" {...common} opacity=".4" />
        <path d="M372 44l6 16 16 6-16 6-6 16-6-16-16-6 16-6z" {...common} opacity=".6" />
      </g>
    );
  }
  if (art === "brain") {
    return (
      <g stroke="#ffffff" strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" fill="none">
        <circle cx="306" cy="100" r="94" fill="#ffffff" fillOpacity=".12" stroke="none" />
        <path d="M304 24c-24-14-56-4-58 24-22 6-28 34-12 48-12 18 0 42 22 46 6 20 34 28 48 14z" fill="#ffffff" fillOpacity=".26" strokeOpacity=".8" />
        <path d="M304 24c24-14 56-4 58 24 22 6 28 34 12 48 12 18 0 42-22 46-6 20-34 28-48 14z" fill="#ffffff" fillOpacity=".16" strokeOpacity=".65" />
        <path d="M304 24v132M268 64c12 6 15 18 12 30M344 72c-12 6-15 18-12 30" strokeWidth="8" strokeOpacity=".7" />
      </g>
    );
  }
  return (
    <g>
      <circle cx="306" cy="100" r="94" fill="#ffffff" opacity=".12" />
      <path d="M304 46c-20-17-48-20-70-14v104c22-6 50-3 70 14 20-17 48-20 70-14V32c-22-6-50-3-70 14z" fill="#ffffff" fillOpacity=".3" stroke="#ffffff" strokeOpacity=".8" strokeWidth="10" strokeLinejoin="round" />
      <path d="M304 46v104" stroke="#ffffff" strokeOpacity=".75" strokeWidth="9" strokeLinecap="round" />
      <path d="M256 68h30M256 92h30M322 68h30M322 92h30" stroke="#ffffff" strokeOpacity=".5" strokeWidth="8" strokeLinecap="round" />
    </g>
  );
}

export default function SubjectTile({
  href,
  eyebrow,
  title,
  meta,
  art,
}: {
  href: string;
  eyebrow?: string;
  title: string;
  meta: string;
  art: Art;
}) {
  const palette = PALETTE[art];
  const id = `tile-${art}`;

  return (
    <Link
      href={href}
      className="group relative block overflow-hidden rounded-[20px] min-h-[190px] transition-transform duration-200 hover:-translate-y-1"
    >
      <svg viewBox="0 0 420 200" preserveAspectRatio="xMidYMid slice" className="absolute inset-0 w-full h-full">
        <defs>
          <linearGradient id={id} x1="0" y1="0" x2="420" y2="200" gradientUnits="userSpaceOnUse">
            <stop stopColor={palette.from} />
            <stop offset=".5" stopColor={palette.from2} />
            <stop offset="1" stopColor={palette.to} />
          </linearGradient>
        </defs>
        <rect width="420" height="200" fill={`url(#${id})`} />
        <Artwork art={art} />
      </svg>

      <div className="relative z-10 p-6 flex flex-col h-full min-h-[190px]">
        {eyebrow && (
          <div className="font-sans text-[10px] tracking-[0.16em] uppercase font-semibold mb-1.5" style={{ color: palette.ink, opacity: 0.8 }}>
            {eyebrow}
          </div>
        )}
        <h2 className="font-sans text-[26px] leading-[1.1] font-medium max-w-[62%]" style={{ color: palette.ink }}>
          {title}
        </h2>
        <div className="mt-auto pt-5 flex items-center gap-3">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-white px-4 py-2 font-sans text-[13px] font-semibold text-[#1a2c3d] shadow-sm">
            Open <span aria-hidden="true">&rsaquo;</span>
          </span>
          <span className="font-sans text-[11px] tracking-[0.1em] uppercase" style={{ color: palette.ink, opacity: 0.75 }}>
            {meta}
          </span>
        </div>
      </div>
    </Link>
  );
}
