"use client";
import {useState,type FormEvent} from "react";
import MainNav from "@/components/MainNav";
import "./resume.css";

const categories=["Clinical Experience","Research","Community Service","Leadership & Teaching","Employment","Honors & Publications"] as const;
type Category=typeof categories[number];
type Entry={id:number;category:Category;role:string;org:string;start:string;end:string;detail:string;result:string;meaningful:boolean};
const emptyEntry=(id:number):Entry=>({id,category:"Clinical Experience",role:"",org:"",start:"",end:"",detail:"",result:"",meaningful:false});
const hints:Record<Category,string>={
 "Clinical Experience":"Describe what you personally did for patients or the care team, within your role.",
 Research:"Name the question, the method you used, and your contribution. Include a presentation or publication only if it happened.",
 "Community Service":"Who did you serve, what did you do, and over what period?",
 "Leadership & Teaching":"What did you organize or teach? Describe a change you helped bring about.",
 Employment:"Describe a responsibility and the skill or result it demonstrates.",
 "Honors & Publications":"Give the award or citation, issuer or journal, and your actual authorship or publication status."
};
function month(v:string){return v?new Date(v+"-01T12:00:00Z").toLocaleDateString("en-US",{month:"short",year:"numeric",timeZone:"UTC"}):"";}
export default function Resume(){
 const [profile,setProfile]=useState({name:"",email:"",location:"",school:"",degree:"",grad:""});
 const [entries,setEntries]=useState<Entry[]>([emptyEntry(1)]);
 const [focus,setFocus]=useState<Category|"auto">("auto");
 const [ready,setReady]=useState(false);
 const change=(key:keyof typeof profile,value:string)=>setProfile({...profile,[key]:value});
 const edit=(id:number,patch:Partial<Entry>)=>setEntries(entries.map(e=>e.id===id?{...e,...patch}:e));
 const current=entries.filter(e=>e.role.trim()||e.org.trim()||e.detail.trim()||e.result.trim());
 const priority=(category:Category)=>current.filter(e=>e.category===category).reduce((n,e)=>n+1+(e.meaningful?100:0),0);
 const ordered=[...categories].sort((a,b)=>focus===a?-1:focus===b?1:priority(b)-priority(a));
 const bullets=(e:Entry)=>[...e.detail.split("\n"),e.result.trim()].filter(Boolean).map(s=>s.trim().replace(/^[-•]\s*/,"")).filter(Boolean);
 function downloadText(){
   const text=document.querySelector<HTMLElement>(".vr-paper")?.innerText;
   if(!text)return;
   const url=URL.createObjectURL(new Blob([text+"\n"],{type:"text/plain;charset=utf-8"}));
   const a=document.createElement("a");a.href=url;a.download="medical-school-resume.txt";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 }
 function generate(ev:FormEvent){ev.preventDefault();setReady(true);window.scrollTo(0,0);}
 return <><MainNav contentId="resume-main" badge="Résumé builder"/><main id="resume-main" className="vr-wrap">
 <div className="vr-controls"><p className="vr-kicker">APPLICATION WORKSHOP</p><h1>Medical school résumé</h1>
 <p>Turn your education and experiences into a résumé you can edit and print. Your entries stay on this page and clear when you leave.</p></div>
 {!ready?<form className="vr-form" onSubmit={generate}>
 <fieldset><legend>1. Education & contact</legend><div className="vr-grid">
 {([["name","Full name"],["email","Email"],["location","City and state (optional)"],["school","College or university"],["degree","Degree and major"],["grad","Graduation or expected graduation (optional)"]] as const).map(([key,label])=><label key={key}>{label}<input required={["name","school","degree"].includes(key)} type={key==="email"?"email":"text"} value={profile[key]} onChange={e=>change(key,e.target.value)}/></label>)}</div></fieldset>
 <fieldset><legend>2. Your experiences</legend><p>Choose experiences you can discuss in an interview. Add one action or result per line.</p>
 {entries.map((e,i)=><div className="vr-entry" key={e.id}><strong>Experience {i+1}</strong><div className="vr-grid">
 <label>Category<select value={e.category} onChange={v=>edit(e.id,{category:v.target.value as Category})}>{categories.map(c=><option key={c}>{c}</option>)}</select></label>
 <label>Role or title<input required={Boolean(e.org.trim()||e.detail.trim()||e.result.trim()||e.start||e.end)} value={e.role} onChange={v=>edit(e.id,{role:v.target.value})}/></label>
 <label>Organization<input value={e.org} onChange={v=>edit(e.id,{org:v.target.value})}/></label>
 <label>Start month<input type="month" value={e.start} onChange={v=>edit(e.id,{start:v.target.value})}/></label>
 <label>End month (blank if ongoing)<input type="month" min={e.start||undefined} value={e.end} onChange={v=>edit(e.id,{end:v.target.value})}/></label></div>
 <label>Contributions<textarea rows={3} value={e.detail} placeholder={hints[e.category]} onChange={v=>edit(e.id,{detail:v.target.value})}/></label>
 <label>Outcome or scope (optional)<input placeholder="For example, a poster presented, people trained, or hours volunteered" value={e.result} onChange={v=>edit(e.id,{result:v.target.value})}/></label>
 <label><input style={{width:"auto",display:"inline",marginRight:8}} type="checkbox" checked={e.meaningful} onChange={v=>edit(e.id,{meaningful:v.target.checked})}/>This experience was especially meaningful to me</label>
 <button type="button" className="vr-link" onClick={()=>setEntries(entries.filter(x=>x.id!==e.id))}>Remove experience</button></div>)}
 <button className="vr-outline" type="button" onClick={()=>setEntries([...entries,emptyEntry(Date.now())])}>+ Add experience</button></fieldset>
 <fieldset><legend>3. Choose your emphasis</legend><label>Which experience section should appear first after education?<select value={focus} onChange={e=>setFocus(e.target.value as Category|"auto")}><option value="auto">Suggest an order from my experiences</option>{categories.map(c=><option key={c}>{c}</option>)}</select></label></fieldset>
 <button className="vr-action">Build my résumé</button>
 <p className="vr-foot">For a U.S. application, follow each school’s submission instructions. See <a href="https://students-residents.aamc.org/media/11616/download">AAMC Work and Activities</a> and <a href="https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/">Harvard résumé guidance</a>.</p>
 </form>:<>
 <div className="vr-controls vr-toolbar"><button className="vr-outline" onClick={()=>setReady(false)}>Edit my information</button><button className="vr-action" onClick={()=>window.print()}>Print / Save as PDF</button><button className="vr-outline" onClick={downloadText}>Download editable text</button></div>
 <article className="vr-paper"><h2>{profile.name}</h2><p>{[profile.email,profile.location].filter(Boolean).join(" · ")}</p>
 <h3>Education</h3><b>{profile.school}</b><p>{[profile.degree,profile.grad].filter(Boolean).join(" · ")}</p>
 {ordered.map(c=>{const group=current.filter(e=>e.category===c).sort((a,b)=>(b.end||(b.start?"9999":"")).localeCompare(a.end||(a.start?"9999":""))||b.start.localeCompare(a.start));return group.length>0&&<section key={c}><h3>{c}</h3>{group.map(e=><div key={e.id} className="vr-item"><b>{[e.role,e.org].filter(Boolean).join(" · ")}</b><p>{[month(e.start),e.end?month(e.end):e.start?"Present":""].filter(Boolean).join(" – ")}</p>{bullets(e).length>0&&<ul>{bullets(e).map((s,i)=><li key={i}>{s}</li>)}</ul>}</div>)}</section>})}</article></>}
 </main></>;
}
