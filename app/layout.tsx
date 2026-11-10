import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import "./nori.css";
import "./study-polish.css";
import ActivityProvider from "@/components/ActivityProvider";
import NoriCompanion from "@/components/NoriCompanion";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Vitalis | MCAT study, one step at a time",
  description: "Practice MCAT questions, explore lessons, review flashcards, and work through concepts with your AI tutor.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col"><ActivityProvider>{children}<NoriCompanion/></ActivityProvider></body>
    </html>
  );
}
