"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import Nori from "./Nori";
export default function NoriCompanion() {
  const path = usePathname();
  if (path.startsWith("/tutor") || path === "/sign-in") return null;
  return <Link href="/tutor" className="nori-companion" aria-label="Ask Nori — open the AI tutor">
    <span className="nori-hint">A little help?</span><Nori/><span className="nori-chat-label">Ask Nori <span aria-hidden="true">↗</span></span>
  </Link>;
}
