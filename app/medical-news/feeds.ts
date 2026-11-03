export const feeds=[
 {name:"UN News",type:"Global health",home:"https://news.un.org/en/news/topic/health",url:"https://news.un.org/feed/subscribe/en/news/topic/health/feed/rss.xml",hosts:["news.un.org"]},
 {name:"BBC Health",type:"Health reporting",home:"https://www.bbc.com/news/health",url:"https://feeds.bbci.co.uk/news/health/rss.xml",hosts:["www.bbc.co.uk","www.bbc.com"]},
 {name:"ECDC",type:"Disease surveillance",home:"https://www.ecdc.europa.eu/en",url:"https://www.ecdc.europa.eu/en/taxonomy/term/1505/feed",hosts:["www.ecdc.europa.eu"]}
];
export type Story={title:string;href:string;time:number;source:string;category:string};
function decode(s:string){
 const named:Record<string,string>={amp:"&",lt:"<",gt:">",quot:'"',apos:"'",nbsp:" "};
 return s.replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos|nbsp);/gi,(whole:string,entity:string)=>{
  if(!entity.startsWith("#"))return named[entity.toLowerCase()]??whole;
  const n=entity[1].toLowerCase()==="x"?parseInt(entity.slice(2),16):Number(entity.slice(1));
  return n>0 && n<=0x10ffff?String.fromCodePoint(n):whole;
 });
}
export function parseFeed(xml:string, feed:typeof feeds[number],now=Date.now()):Story[]{
 if(!/<rss\b/i.test(xml))throw Error("Unexpected publisher response");
 const stories:Story[]=[];
 for(const [,item] of xml.matchAll(/<item(?:\s[^>]*)?>([\s\S]*?)<\/item>/gi)){
  const tag=(key:string)=>decode((item.match(new RegExp("<"+key+"(?:\\s[^>]*)?>([\\s\\S]*?)</"+key+">","i"))?.[1]||"").trim().replace(/^<!\[CDATA\[([\s\S]*)\]\]>$/,"$1")).trim();
  const title=tag("title"),time=Date.parse(tag("pubDate"));
  try{const href=new URL(tag("link"));if(!title||!Number.isFinite(time)||time>now+3600000||time<now-90*86400000||href.protocol!=="https:"||!feed.hosts.includes(href.hostname))continue;
   stories.push({title,href:href.href,time,source:feed.name,category:feed.type});
  }catch{/* Ignore malformed entries while keeping the publisher’s valid stories. */}
 }
 return stories;
}
