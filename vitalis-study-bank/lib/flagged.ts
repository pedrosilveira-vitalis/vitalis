import type { Question } from "./practice";
const prefix="vitalis.flagged.v1.";
export function flagged(id:string) { return localStorage.getItem(prefix+id)!==null; }
export function toggleFlag(q:Question) {
  if (flagged(q.id)) { localStorage.removeItem(prefix+q.id); return false; }
  localStorage.setItem(prefix+q.id,JSON.stringify({question:q,saved:Date.now()}));
  return true;
}
export function listFlags(): Question[] {
  const entries: {question:Question;saved:number}[]=[];
  for(const key of Object.keys(localStorage).filter(k=>k.startsWith(prefix))){
    try {const item=JSON.parse(localStorage.getItem(key) || "null");if(item?.question?.id)entries.push(item);} catch { /* Skip damaged entries. */ }
  }
  return entries.sort((a,b)=>b.saved-a.saved).map(item=>item.question);
}
