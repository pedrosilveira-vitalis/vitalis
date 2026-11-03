import MainNav from "@/components/MainNav";
import {feeds,parseFeed} from "./feeds";
import "../resume/resume.css";


async function latest(feed:typeof feeds[number]){
 try{
  const res=await fetch(feed.url,{next:{revalidate:1800},signal:AbortSignal.timeout(6500)});
  if(!res.ok)throw Error("Publisher unavailable");
  return {feed,ok:true,stories:parseFeed(await res.text(),feed)};
 }catch{return {feed,ok:false,stories:[]};}
}
const date=(time:number)=>new Intl.DateTimeFormat("en-US",{year:"numeric",month:"short",day:"numeric",timeZone:"UTC"}).format(time);
export default async function News({searchParams}:{searchParams:Promise<{source?:string}>}){
 const selected=(await searchParams).source;
 const sources=feeds.filter(s=>s.name===selected);
 const replies=await Promise.all((sources.length?sources:feeds).map(latest));
 const seen=new Set<string>();
 const stories=replies.flatMap(s=>s.stories).sort((a,b)=>b.time-a.time).filter(s=>{
  const url=new URL(s.href),key=url.origin+url.pathname;if(seen.has(key))return false;seen.add(key);return true;
 }).slice(0,36);
 return <><MainNav contentId="news-main" badge="Medical news"/><main className="vn-wrap" id="news-main"><p className="vr-kicker">THE READING ROOM</p><h1>Medical news</h1><p>Global health reporting and disease surveillance. Read the original coverage, newest first.</p>
 <nav aria-label="Filter by publisher" className="flex flex-wrap gap-4 my-6">{[{name:"All publishers"},...feeds].map((f,i)=><a key={f.name} aria-current={(!i&&!sources.length)||selected===f.name?"page":undefined} href={i?"?source="+encodeURIComponent(f.name):"/medical-news"}>{f.name}</a>)}</nav>
 {replies.filter(s=>!s.ok).map(({feed})=><p key={feed.name} role="status">The {feed.name} feed is unavailable. <a href={feed.home}>Visit the publisher</a>.</p>)}
 {stories.length===0 && <p className="vn-card">No recent headlines are available in this view. Browse the publishers below or check back later.</p>}
 {stories.map(s=><article className="vn-card" key={s.href}><p><strong>{s.source}</strong> · {s.category} · <time dateTime={new Date(s.time).toISOString()}>{date(s.time)}</time></p><h3><a href={s.href}>{s.title}</a></h3></article>)}
 <footer className="vr-foot">Headlines come from feeds checked up to every 30 minutes while this page is in use. Showing items published in the past 90 days. <div>{feeds.map(f=><a className="mr-4" key={f.name} href={f.home}>{f.name}</a>)}</div></footer></main></>;
}
