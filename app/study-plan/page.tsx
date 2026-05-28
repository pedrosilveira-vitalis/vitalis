"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import MainNav from "@/components/MainNav";

type TopicRating = "Strong" | "OK" | "Weak";
type TopicRatings = Record<string, TopicRating>;

type PlanItem = {
  id: string;
  type: "read_unit" | "practice_questions" | "unit_test" | "review" | "aamc_test";
  unitId?: number;
  section?: string;
  title: string;
  description: string;
};

type PlanWeek = {
  weekNumber: number;
  theme: string;
  rationale: string;
  estimatedHours: number;
  items: PlanItem[];
};

type PlanData = {
  summary: string;
  weeks: PlanWeek[];
};

type Plan = {
  id: number;
  weeksCount: number;
  planData: PlanData;
  completedItems: string[];
  unitToFirstLesson: Record<number, number>;
  submission: {
    bio: number;
    chem: number;
    psych: number;
    cars: number;
    total: number;
    topicRatings: TopicRatings;
    testDate: string | null;
    weeksUntilTest: number;
    submittedAt: string;
  };
};

const TOPICS_BY_SECTION: Record<string, string[]> = {
  "Bio / Biochem": ["Biochemistry", "Cell biology", "Genetics", "Physiology", "Molecular biology", "Immunology"],
  "Chem / Phys": ["General chem", "Organic chem", "Physics (mechanics)", "Physics (waves/optics)", "Thermodynamics"],
  "Psych / Soc": ["Learning & cognition", "Disorders & therapy", "Social psych", "Sociology", "Research methods"],
  "CARS": ["Reading speed", "Argument mapping", "Inference questions", "Author tone & purpose"],
};

const SECTION_COLORS: Record<string, string> = {
  "Bio / Biochem": "#a8324a",
  "Chem / Phys": "#2e4a6b",
  "Psych / Soc": "#8a6b2e",
  "CARS": "#4a3b6b",
};

const ITEM_TYPE_LABELS: Record<string, string> = {
  read_unit: "Read",
  practice_questions: "Practice",
  unit_test: "Unit test",
  review: "Review",
  aamc_test: "AAMC test",
};

const ITEM_TYPE_COLORS: Record<string, string> = {
  read_unit: "#0c1a2e",
  practice_questions: "#a8324a",
  unit_test: "#8a6b2e",
  review: "#4a3b6b",
  aamc_test: "#2e4a6b",
};

export default function StudyPlanPage() {
  const [loading, setLoading] = useState(true);
  const [authed, setAuthed] = useState<boolean | null>(null);
  const [plan, setPlan] = useState<Plan | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  // Form state
  const [bio, setBio] = useState("");
  const [chem, setChem] = useState("");
  const [psych, setPsych] = useState("");
  const [cars, setCars] = useState("");
  const [weeksUntilTest, setWeeksUntilTest] = useState("8");
  const [testDate, setTestDate] = useState("");
  const [topicRatings, setTopicRatings] = useState<TopicRatings>({});

  useEffect(() => {
    loadPlan();
  }, []);

  async function loadPlan() {
    setLoading(true);
    try {
      const res = await fetch("/api/study-plan");
      if (res.status === 401) {
        setAuthed(false);
        setLoading(false);
        return;
      }
      const data = await res.json();
      setAuthed(true);
      setPlan(data.plan || null);
      if (!data.plan) setShowForm(true);
    } catch {
      setError("Couldn't load your study plan.");
    }
    setLoading(false);
  }

  function setRating(topic: string, rating: TopicRating) {
    setTopicRatings((prev) => ({ ...prev, [topic]: rating }));
  }

  function validateForm(): string | null {
    const scores = [bio, chem, psych, cars];
    for (const s of scores) {
      const n = parseInt(s, 10);
      if (isNaN(n) || n < 118 || n > 132) {
        return "All section scores must be between 118 and 132.";
      }
    }
    const w = parseInt(weeksUntilTest, 10);
    if (isNaN(w) || w < 1 || w > 26) {
      return "Weeks until test must be between 1 and 26.";
    }
    const totalTopics = Object.values(TOPICS_BY_SECTION).flat().length;
    const ratedTopics = Object.keys(topicRatings).length;
    if (ratedTopics < totalTopics) {
      return `Please rate all ${totalTopics} topics. (${totalTopics - ratedTopics} remaining)`;
    }
    return null;
  }

  async function submitForm() {
    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }
    setError("");
    setGenerating(true);
    try {
      const res = await fetch("/api/study-plan/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          bio: parseInt(bio, 10),
          chem: parseInt(chem, 10),
          psych: parseInt(psych, 10),
          cars: parseInt(cars, 10),
          topicRatings,
          testDate: testDate || null,
          weeksUntilTest: parseInt(weeksUntilTest, 10),
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Couldn't generate plan. Try again.");
        setGenerating(false);
        return;
      }
      // Reload the plan
      await loadPlan();
      setShowForm(false);
      // Reset form
      setBio(""); setChem(""); setPsych(""); setCars("");
      setTopicRatings({}); setTestDate(""); setWeeksUntilTest("8");
    } catch {
      setError("Connection issue. Try again.");
    }
    setGenerating(false);
  }

  async function toggleItem(itemId: string, completed: boolean) {
    if (!plan) return;
    // Optimistic update
    const newCompleted = completed
      ? [...plan.completedItems, itemId]
      : plan.completedItems.filter((id) => id !== itemId);
    setPlan({ ...plan, completedItems: newCompleted });

    try {
      await fetch("/api/study-plan/toggle", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ itemId, completed }),
      });
    } catch {
      // Revert on error
      setPlan({ ...plan, completedItems: plan.completedItems });
    }
  }

  function getItemLink(item: PlanItem): string | null {
    if (!plan) return null;
    if (item.type === "read_unit" && item.unitId) {
      const firstLessonId = plan.unitToFirstLesson[item.unitId];
      if (firstLessonId) return `/study/lessons/${firstLessonId}`;
      return `/study`;
    }
    if (item.type === "practice_questions" && item.section) {
      return `/practice/${item.section}`;
    }
    if (item.type === "unit_test" && item.unitId) {
      const firstLessonId = plan.unitToFirstLesson[item.unitId];
      if (firstLessonId) return `/study/lessons/${firstLessonId}`;
      return `/study`;
    }
    if (item.type === "review") {
      return `/study`;
    }
    return null;
  }

  // ===== RENDER =====

  if (loading) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] flex items-center justify-center">
        <div className="text-center">
          <div className="flex items-center justify-center gap-2 mb-3">
            <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" />
            <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.15s" }} />
            <span className="w-2 h-2 rounded-full bg-[#0c1a2e] animate-bounce" style={{ animationDelay: "0.3s" }} />
          </div>
          <div className="font-mono text-[11px] uppercase tracking-[0.12em] opacity-60">Loading your study plan...</div>
        </div>
      </div>
    );
  }

  if (authed === false) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e]">
        <MainNav active="study-plan" badge="Study Plan" />
        <div className="max-w-md mx-auto px-10 py-20 text-center">
          <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4">Sign in required</div>
          <h1 className="font-serif text-4xl font-medium mb-4">Save your study plan.</h1>
          <p className="text-sm opacity-70 mb-7 leading-relaxed">
            Study plans are personal and tied to your account so you can track progress over weeks. Sign in to get started.
          </p>
          <Link href="/sign-in" className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-5 py-3 rounded-full hover:bg-[#1a2c4a]">
            Sign in →
          </Link>
        </div>
      </div>
    );
  }

  if (generating) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e]">
        <MainNav active="study-plan" badge="Building your plan" />
        <div className="max-w-md mx-auto px-10 py-20 text-center">
          <div className="flex items-center justify-center gap-2 mb-6">
            <span className="w-3 h-3 rounded-full bg-[#a8324a] animate-bounce" />
            <span className="w-3 h-3 rounded-full bg-[#a8324a] animate-bounce" style={{ animationDelay: "0.15s" }} />
            <span className="w-3 h-3 rounded-full bg-[#a8324a] animate-bounce" style={{ animationDelay: "0.3s" }} />
          </div>
          <h1 className="font-serif text-3xl font-medium mb-3">Generating your plan...</h1>
          <p className="text-sm opacity-70 leading-relaxed">
            We&apos;re analyzing your scores and building a {weeksUntilTest}-week plan tailored to your weak spots. This takes about 30 seconds.
          </p>
        </div>
      </div>
    );
  }

  // FORM VIEW
  if (showForm || !plan) {
    return (
      <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans relative overflow-hidden">
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-0 right-0 w-[1000px] h-[500px] bg-[#a8324a] opacity-[0.05] blur-[120px] rounded-full -translate-y-1/3 translate-x-1/4" />
        </div>
        <div className="relative z-10">
          <MainNav active="study-plan" badge="Build your plan" />

          <section className="px-10 pt-14 pb-8 border-b border-[#0c1a2e15]">
            <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
              <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
              Mode · Personalized study plan
            </div>
            <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(40px,5vw,76px)] max-w-4xl">
              {plan ? "Update your" : "Build your"} <span className="italic font-light text-[#a8324a]">plan.</span>
            </h1>
            <p className="text-[15px] opacity-70 mt-4 max-w-2xl leading-relaxed">
              Enter your most recent AAMC practice test scores and rate your topic strengths. We&apos;ll generate a week-by-week study plan tailored to your weak spots.
            </p>
            {plan && (
              <button onClick={() => setShowForm(false)} className="mt-4 font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-4 py-2 rounded-full hover:bg-[#0c1a2e0a]">
                ← Back to current plan
              </button>
            )}
          </section>

          <section className="px-10 py-10 max-w-3xl">
            {/* Section scores */}
            <div className="mb-10">
              <h2 className="font-serif text-2xl font-medium mb-2">Section scores</h2>
              <p className="text-[13px] opacity-65 mb-5">Enter your scores from your most recent AAMC practice test (each between 118-132).</p>
              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: "Bio / Biochem", value: bio, set: setBio, color: "#a8324a" },
                  { label: "Chem / Phys", value: chem, set: setChem, color: "#2e4a6b" },
                  { label: "Psych / Soc", value: psych, set: setPsych, color: "#8a6b2e" },
                  { label: "CARS", value: cars, set: setCars, color: "#4a3b6b" },
                ].map((s) => {
                  const n = parseInt(s.value, 10);
                  const valid = s.value !== "" && !isNaN(n) && n >= 118 && n <= 132;
                  const invalid = s.value !== "" && !valid;
                  return (
                    <label key={s.label} className="block">
                      <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2" style={{ color: s.color }}>{s.label}</div>
                      <input
                        type="text"
                        inputMode="numeric"
                        value={s.value}
                        onChange={(e) => s.set(e.target.value)}
                        placeholder="118-132"
                        className={`w-full px-4 py-3 border-2 rounded-xl bg-transparent outline-none text-xl font-serif font-medium ${
                          invalid ? "border-[#a8324a]" : valid ? "border-[#3e6b4a]" : "border-[#0c1a2e25] focus:border-[#0c1a2e]"
                        }`}
                      />
                    </label>
                  );
                })}
              </div>
            </div>

            {/* Time horizon */}
            <div className="mb-10">
              <h2 className="font-serif text-2xl font-medium mb-2">Time until your MCAT</h2>
              <p className="text-[13px] opacity-65 mb-5">How many weeks do you have? Plans are 1-26 weeks.</p>
              <div className="grid grid-cols-2 gap-4 max-w-md">
                <label className="block">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Weeks until test</div>
                  <input type="number" min="1" max="26" value={weeksUntilTest} onChange={(e) => setWeeksUntilTest(e.target.value)} className="w-full px-4 py-3 border-2 border-[#0c1a2e25] rounded-xl bg-transparent outline-none text-xl font-serif font-medium focus:border-[#0c1a2e]" />
                </label>
                <label className="block">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55 mb-2">Test date (optional)</div>
                  <input type="date" value={testDate} onChange={(e) => setTestDate(e.target.value)} className="w-full px-4 py-3 border-2 border-[#0c1a2e25] rounded-xl bg-transparent outline-none text-base font-medium focus:border-[#0c1a2e]" />
                </label>
              </div>
            </div>

            {/* Topic ratings */}
            <div className="mb-10">
              <h2 className="font-serif text-2xl font-medium mb-2">Topic self-assessment</h2>
              <p className="text-[13px] opacity-65 mb-5">For each topic, tap one: Weak (struggling), OK (decent), or Strong (confident). Be honest — this drives the plan.</p>

              {Object.entries(TOPICS_BY_SECTION).map(([section, topics]) => (
                <div key={section} className="mb-6">
                  <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-60 mb-3" style={{ color: SECTION_COLORS[section] }}>{section}</div>
                  <div className="space-y-2">
                    {topics.map((topic) => {
                      const r = topicRatings[topic];
                      return (
                        <div key={topic} className="flex items-center gap-3 flex-wrap">
                          <div className="flex-1 min-w-[150px] text-[14px]">{topic}</div>
                          <div className="flex gap-1.5">
                            {(["Weak", "OK", "Strong"] as TopicRating[]).map((rating) => {
                              const ratingColors = { Weak: "#a8324a", OK: "#8a6b2e", Strong: "#3e6b4a" };
                              const isSelected = r === rating;
                              return (
                                <button
                                  key={rating}
                                  onClick={() => setRating(topic, rating)}
                                  className={`px-3 py-1.5 rounded-full text-[11px] font-mono uppercase tracking-[0.08em] border-2 transition-all ${
                                    isSelected ? "text-[#f5f1ea]" : "border-[#0c1a2e25] hover:border-[#0c1a2e]"
                                  }`}
                                  style={isSelected ? { backgroundColor: ratingColors[rating], borderColor: ratingColors[rating] } : {}}
                                >
                                  {rating}
                                </button>
                              );
                            })}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>

            {error && (
              <div className="mb-5 p-3 bg-[#a8324a08] border border-[#a8324a25] rounded-lg text-[13px] text-[#a8324a]">
                {error}
              </div>
            )}

            <div className="flex gap-3 flex-wrap">
              <button onClick={submitForm} className="font-mono text-xs uppercase tracking-[0.08em] bg-[#0c1a2e] text-[#f5f1ea] px-6 py-3.5 rounded-full hover:bg-[#1a2c4a]">
                Generate my plan →
              </button>
              {plan && (
                <button onClick={() => setShowForm(false)} className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-6 py-3.5 rounded-full hover:bg-[#0c1a2e0a]">
                  Cancel
                </button>
              )}
            </div>
          </section>
        </div>
      </div>
    );
  }

  // PLAN VIEW
  const totalItems = plan.planData.weeks.reduce((sum, w) => sum + w.items.length, 0);
  const completedCount = plan.completedItems.length;
  const progressPct = totalItems > 0 ? Math.round((completedCount / totalItems) * 100) : 0;

  return (
    <div className="min-h-screen bg-[#f5f1ea] text-[#0c1a2e] font-sans">
      <MainNav active="study-plan" badge="My Study Plan" />

      <section className="px-10 pt-12 pb-8 border-b border-[#0c1a2e15]">
        <div className="font-mono text-[11px] tracking-[0.18em] uppercase opacity-60 mb-4 flex items-center gap-3">
          <span className="w-10 h-px bg-[#0c1a2e] opacity-40" />
          Your personalized plan
        </div>
        <div className="flex items-end justify-between gap-4 flex-wrap mb-5">
          <h1 className="font-serif font-normal leading-[0.95] tracking-[-0.03em] text-[clamp(36px,4.5vw,68px)]">
            {plan.submission.weeksUntilTest}-week <span className="italic font-light text-[#a8324a]">plan.</span>
          </h1>
          <button onClick={() => setShowForm(true)} className="font-mono text-xs uppercase tracking-[0.08em] border border-[#0c1a2e25] px-5 py-3 rounded-full hover:bg-[#0c1a2e0a]">
            Update scores →
          </button>
        </div>

        <div className="flex flex-wrap gap-6 mb-5">
          <div>
            <div className="font-mono text-[10px] tracking-[0.12em] uppercase opacity-55 mb-1">Current total</div>
            <div className="font-serif text-3xl font-medium">{plan.submission.total}</div>
          </div>
          <div>
            <div className="font-mono text-[10px] tracking-[0.12em] uppercase opacity-55 mb-1">Sections</div>
            <div className="font-mono text-sm">B:{plan.submission.bio} · C:{plan.submission.chem} · P:{plan.submission.psych} · R:{plan.submission.cars}</div>
          </div>
          {plan.submission.testDate && (
            <div>
              <div className="font-mono text-[10px] tracking-[0.12em] uppercase opacity-55 mb-1">Test date</div>
              <div className="font-mono text-sm">{plan.submission.testDate}</div>
            </div>
          )}
        </div>

        <div className="flex items-center gap-3 max-w-md">
          <div className="flex-1 h-2 bg-[#0c1a2e15] rounded-full overflow-hidden">
            <div className="h-full bg-[#a8324a] transition-all" style={{ width: `${progressPct}%` }} />
          </div>
          <div className="font-mono text-[11px] tracking-[0.1em] uppercase opacity-65 flex-shrink-0">
            {completedCount} / {totalItems} done · {progressPct}%
          </div>
        </div>

        {plan.planData.summary && (
          <p className="text-[14px] opacity-75 mt-5 max-w-3xl leading-relaxed italic">{plan.planData.summary}</p>
        )}
      </section>

      <section className="px-10 py-10 max-w-4xl">
        <div className="space-y-6">
          {plan.planData.weeks.map((week) => {
            const weekItems = week.items.length;
            const weekDone = week.items.filter((i) => plan.completedItems.includes(i.id)).length;
            const weekComplete = weekDone === weekItems && weekItems > 0;
            return (
              <div key={week.weekNumber} className={`border rounded-2xl overflow-hidden ${weekComplete ? "border-[#3e6b4a]" : "border-[#0c1a2e15]"}`}>
                <div className={`p-5 border-b ${weekComplete ? "bg-[#3e6b4a08] border-[#3e6b4a]" : "bg-[#0c1a2e0a] border-[#0c1a2e15]"}`}>
                  <div className="flex items-center justify-between mb-2 flex-wrap gap-2">
                    <div className="font-mono text-[10px] tracking-[0.14em] uppercase opacity-55">
                      Week {String(week.weekNumber).padStart(2, "0")} · {week.estimatedHours}h
                    </div>
                    <div className="font-mono text-[10px] tracking-[0.1em] uppercase opacity-65">
                      {weekDone} / {weekItems} {weekComplete && "✓"}
                    </div>
                  </div>
                  <h2 className="font-serif text-[22px] font-medium tracking-tight mb-1">{week.theme}</h2>
                  <p className="text-[13px] opacity-70 leading-relaxed">{week.rationale}</p>
                </div>
                <div className="divide-y divide-[#0c1a2e15]">
                  {week.items.map((item) => {
                    const isDone = plan.completedItems.includes(item.id);
                    const link = getItemLink(item);
                    const typeColor = ITEM_TYPE_COLORS[item.type] || "#0c1a2e";
                    return (
                      <div key={item.id} className={`p-4 flex items-start gap-3 ${isDone ? "opacity-50" : ""}`}>
                        <button
                          onClick={() => toggleItem(item.id, !isDone)}
                          className={`w-6 h-6 rounded border-2 flex-shrink-0 flex items-center justify-center transition-all ${
                            isDone ? "bg-[#3e6b4a] border-[#3e6b4a]" : "border-[#0c1a2e25] hover:border-[#0c1a2e]"
                          }`}
                        >
                          {isDone && (
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f5f1ea" strokeWidth="3">
                              <polyline points="20 6 9 17 4 12" />
                            </svg>
                          )}
                        </button>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1 flex-wrap">
                            <span className="font-mono text-[9px] tracking-[0.12em] uppercase px-2 py-0.5 rounded-full text-[#f5f1ea]" style={{ backgroundColor: typeColor }}>
                              {ITEM_TYPE_LABELS[item.type]}
                            </span>
                            <div className={`font-serif text-[15px] font-medium ${isDone ? "line-through" : ""}`}>
                              {item.title}
                            </div>
                          </div>
                          {item.description && (
                            <div className="text-[12.5px] opacity-65 leading-relaxed mb-1">{item.description}</div>
                          )}
                          {link && !isDone && (
                            <Link href={link} className="inline-block font-mono text-[10px] tracking-[0.1em] uppercase opacity-60 hover:opacity-100 hover:text-[#a8324a] mt-1">
                              Go to {ITEM_TYPE_LABELS[item.type]} →
                            </Link>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <div className="mx-10 my-7 p-3.5 px-5 border border-dashed border-[#0c1a2e25] rounded-lg font-mono text-[12px] leading-relaxed opacity-60">
        Plans are AI-generated based on your scores and self-assessment. Always cross-reference with official AAMC materials. Submit new scores anytime to regenerate your plan.
      </div>
    </div>
  );
}