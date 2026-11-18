"use client";

import { pieces, type Mark } from "./annotations";

/**
 * A run of exam text that can carry highlights and strikethrough.
 *
 * The `data-annotate` key is what the selection reader looks for, so every
 * annotatable region on screen — each passage paragraph, each stem, each
 * answer choice — needs its own stable key.
 */
export default function Annotated({
  text,
  marks,
  annotateKey,
  className = "",
  as: Tag = "p",
}: {
  text: string;
  marks?: Mark[];
  annotateKey: string;
  className?: string;
  as?: "p" | "span" | "div";
}) {
  return (
    <Tag data-annotate={annotateKey} className={className}>
      {pieces(text, marks).map((piece, index) => {
        if (!piece.highlight && !piece.strike) return <span key={index}>{piece.text}</span>;
        const classes = [piece.highlight ? "exam-hl" : "", piece.strike ? "exam-st" : ""].filter(Boolean).join(" ");
        return (
          <span key={index} className={classes}>
            {piece.text}
          </span>
        );
      })}
    </Tag>
  );
}
