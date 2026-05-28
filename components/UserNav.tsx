"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type User = {
  name: string | null;
  email: string | null;
  image: string | null;
};

export default function UserNav() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/session")
      .then((r) => r.json())
      .then((data) => {
        setUser(data.user);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="w-8 h-8 rounded-full bg-[#0c1a2e15]" />;
  }

  if (!user) {
    return (
      <Link
        href="/sign-in"
        className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-4 py-2.5 rounded-full hover:bg-[#1a2c4a] transition-colors"
      >
        Sign in →
      </Link>
    );
  }

  const initials = (user.name || user.email || "?")
    .split(" ")
    .map((s) => s[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();

  function handleSignOut() {
    window.location.href = "/api/auth/signout?callbackUrl=/";
  }

  return (
    <div className="flex items-center gap-3">
      {user.image ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={user.image}
          alt={user.name || "User"}
          className="w-8 h-8 rounded-full border border-[#0c1a2e25]"
        />
      ) : (
        <div className="w-8 h-8 rounded-full bg-[#0c1a2e] text-[#f5f1ea] flex items-center justify-center font-mono text-[11px] font-medium">
          {initials}
        </div>
      )}
      <button
        type="button"
        onClick={handleSignOut}
        className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-60 hover:opacity-100 transition-opacity"
      >
        Sign out
      </button>
    </div>
  );
}