"use client";
import { useEffect } from "react";
import Nori from "./Nori";
import type { StudyReward as Reward } from "@/lib/study-rewards";
export default function StudyReward({ reward, onDismiss }: { reward: Reward | null; onDismiss: () => void }) {
  useEffect(() => {
    if (!reward) return;
    const timer = setTimeout(onDismiss, 7000);
    return () => clearTimeout(timer);
  }, [reward, onDismiss]);
  return <div className="study-reward-region" role="status" aria-live="polite" aria-atomic="true">
    {reward && <div className="study-reward" key={reward.day}>
      <div className="study-reward-nori" aria-hidden="true"><Nori/><span>✦</span></div>
      <div><strong>{reward.title}</strong><p>{reward.message}</p></div>
      <button type="button" aria-label="Dismiss progress celebration" onClick={onDismiss}>×</button>
    </div>}
  </div>;
}
