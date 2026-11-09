"use client";
import { useEffect,useState } from "react";
import Link from "next/link";
import MainNav from "@/components/MainNav";
import { listFlags,toggleFlag } from "@/lib/flagged";
import type { Question } from "@/lib/practice";

export default function FlaggedPage(){
  const [questions,setQuestions]=useState<Question[]>([]);
  const [ready,setReady]=useState(false);
  const [error,setError]=useState("");
  const [section,setSection]=useState("all");
  useEffect(()=>{
    function load(){try{setQuestions(listFlags());}catch{setError("Please enable browser storage to use flags.");}setReady(true);}
    load();window.addEventListener("storage",load);return ()=>window.removeEventListener("storage",load);
  },[]);
  return <><MainNav badge="Flagged questions" contentId="saved-questions"/><main id="saved-questions" className="max-w-4xl mx-auto px-6 py-10">
    <p className="text-sm text-[#245574]">Your practice notebook</p><h1 className="font-sans text-4xl my-3">Flagged questions</h1>
    <p>Revisit questions saved in this browser. Open a question to try it again before revealing its explanation.</p>
    <p role="status">{error}</p>
    {ready && !questions.length && <p className="my-8">Use “Flag for later” during a session to save your first question. <Link className="underline" href="/practice">Open practice</Link></p>}
    {!!questions.length && <label className="block my-6">Section <select className="p-2 border rounded-lg" value={section} onChange={e=>setSection(e.target.value)}><option value="all">All sections</option>{[...new Set(questions.map(q=>q.section))].map(s=><option key={s}>{s}</option>)}</select></label>}
    {questions.filter(q=>section==="all"||section===q.section).map(q=><details key={q.id} className="my-3 border rounded-xl p-5">
      <summary className="cursor-pointer"><small>{q.section} · {q.topic}</small><br/>{q.question_text}</summary>
      {q.passage && <article className="p-4 my-3 bg-white/60"><strong>{q.passage.title}</strong><p className="whitespace-pre-wrap">{q.passage.content}</p></article>}
      <ol className="list-[upper-alpha] ml-6 my-4">{[q.choice_a,q.choice_b,q.choice_c,q.choice_d].map((c,i)=><li key={i}>{c}</li>)}</ol>
      <details><summary className="cursor-pointer underline">Reveal answer and explanation</summary><p className="my-3"><strong>{q.correct_answer}.</strong> {q.explanation}</p></details>
      <button className="mt-4 text-sm underline" onClick={()=>{try{toggleFlag(q);setQuestions(listFlags());setSection("all");}catch{setError("Could not update this flag.");}}}>Remove flag</button>
    </details>)}
  </main></>;
}
