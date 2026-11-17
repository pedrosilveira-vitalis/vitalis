"use client";

/**
 * Save as PDF is just the browser's print dialog, which every platform offers
 * as a "Save as PDF" destination. No PDF library, no server round trip, and
 * the output honours the print stylesheet.
 */
export default function PrintButton({ accent }: { accent: string }) {
  return (
    <button
      type="button"
      onClick={() => window.print()}
      className="rounded-xl px-5 py-3 font-sans text-sm font-medium text-[#f5f1ea]"
      style={{ background: accent }}
    >
      Save as PDF &darr;
    </button>
  );
}
