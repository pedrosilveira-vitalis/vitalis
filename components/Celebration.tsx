"use client";

import { useEffect, useState } from "react";
import Nori from "./Nori";

/**
 * The moment someone has just paid. Two cannons fire once, Nori jumps, and
 * then it settles — a loop would get irritating on a page people linger on.
 * Pure CSS and SVG: no animation library to install, and it respects
 * prefers-reduced-motion.
 */
const COLOURS = ["#245574", "#5b7a64", "#987740", "#a8324a", "#d4aa98", "#426d86"];

type Piece = { id: number; x: number; y: number; rotate: number; delay: number; colour: string; round: boolean };

function burst(side: "left" | "right", count: number, offset: number): Piece[] {
  return Array.from({ length: count }, (_, index) => {
    const spread = (index / count) * 70 + Math.random() * 14;
    const distance = 160 + Math.random() * 220;
    const radians = ((side === "left" ? -spread - 12 : -180 + spread + 12) * Math.PI) / 180;
    return {
      id: offset + index,
      x: Math.cos(radians) * distance,
      y: Math.sin(radians) * distance - Math.random() * 60,
      rotate: Math.random() * 720 - 360,
      delay: Math.random() * 0.12,
      colour: COLOURS[index % COLOURS.length],
      round: index % 3 === 0,
    };
  });
}

export default function Celebration() {
  const [pieces, setPieces] = useState<Piece[]>([]);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    setPieces([...burst("left", 26, 0), ...burst("right", 26, 100)]);
  }, []);

  return (
    <div className="celebration" aria-hidden="true">
      <div className="celebration-nori">
        <Nori />
      </div>

      {(["left", "right"] as const).map(side => (
        <div key={side} className={`cannon cannon-${side}`}>
          <svg viewBox="0 0 60 40" className="cannon-art">
            <rect x="2" y="26" width="34" height="12" rx="4" fill="#0c1a2e" opacity=".9" />
            <path d="M30 32 L56 16 L60 24 L34 38 Z" fill="#245574" />
            <circle cx="12" cy="32" r="3" fill="#f5f1ea" opacity=".5" />
          </svg>
        </div>
      ))}

      {pieces.map(piece => (
        <span
          key={piece.id}
          className={`confetti ${piece.id >= 100 ? "confetti-right" : "confetti-left"}`}
          style={
            {
              background: piece.colour,
              borderRadius: piece.round ? "50%" : "2px",
              animationDelay: `${piece.delay}s`,
              "--dx": `${piece.x}px`,
              "--dy": `${piece.y}px`,
              "--spin": `${piece.rotate}deg`,
            } as React.CSSProperties
          }
        />
      ))}
    </div>
  );
}
