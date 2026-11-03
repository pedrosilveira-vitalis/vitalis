import test from 'node:test';
import assert from 'node:assert/strict';
import { parseQuestions, sessionSettings, allocateSections, parseCards } from '../lib/practice';
import { POST as generate } from '../app/api/practice/generate/route';
import { POST as explain } from '../app/api/practice/explain/route';
import { fetchJson } from '../lib/fetch-json';
const q = { stem:'Which process produces ATP?', choices:{A:'Glycolysis',B:'Diffusion',C:'Osmosis',D:'Transcription'}, correctAnswer:'A', explanation:'Glycolysis produces ATP by substrate-level phosphorylation.', concept:'Glycolysis', difficulty:'medium', wrongAnswerExplanations:{B:'Passive diffusion does not produce ATP.',C:'Osmosis moves water.',D:'Transcription consumes energy.'} };
test('generator payload maps to the fields displayed and graded by the session',()=>{const [value]=parseQuestions({questions:[q]},'bio-biochem',1,false);assert.equal(value.question_text,q.stem);assert.equal(value.choice_a,q.choices.A);assert.equal(value.correct_answer,'A');assert.equal(value.topic,q.concept);assert.equal(value.wrongAnswerExplanations.B,q.wrongAnswerExplanations.B);});
test('CARS requires and retains its passage',()=>{assert.throws(()=>parseQuestions({questions:[q]},'cars',1,true));assert.equal(parseQuestions({questions:[q],passage:{title:'Argument',content:'Passage context'}},'cars',1,true)[0].passage?.content,'Passage context');});
test('reject incomplete counts, answers, choices and difficulty',()=>{assert.throws(()=>parseQuestions({questions:[q]},'bio-biochem',5,false));for(const bad of [{...q,correctAnswer:'E'},{...q,choices:{A:'yes'}},{...q,difficulty:'unknown'}])assert.throws(()=>parseQuestions({questions:[bad]},'bio-biochem',1,false));assert.throws(()=>parseQuestions({questions:[q]},'bio-biochem',1,false,'hard'));});
test('mixed sessions cover sections and retain exact requested count',()=>{for(const count of [5,10,15,20]){const groups=allocateSections('mixed',count);assert.equal(groups.length,4);assert.equal(groups.reduce((s,g)=>s+g.count,0),count);}});
test('invalid session inputs are rejected',()=>{for(const input of [{section:'other'},{section:'cars',count:100},{section:'cars',count:NaN},{section:'cars',difficulty:'expert'},{section:'cars',format:'other'}])assert.throws(()=>sessionSettings(input));assert.equal(sessionSettings({section:'cars',count:5,difficulty:'hard'}).difficulty,'hard');});
test('flashcards convert deck data and reject missing fields or counts',()=>{assert.deepEqual(parseCards({deck:[{front:'Q',back:'A'}]},1),[{front:'Q',back:'A'}]);assert.throws(()=>parseCards({deck:[{front:'Q'}]},1));assert.throws(()=>parseCards({deck:[]},1));});
test('generation rejects malformed requests before invoking AI',async()=>{const result=await generate(new Request('http://localhost/api/practice/generate',{method:'POST',body:JSON.stringify({section:'invalid'})}));assert.equal(result.status,400);});
test('explanation rejects messages without question context',async()=>{const result=await explain(new Request('http://localhost/api/practice/explain',{method:'POST',body:JSON.stringify({messages:[{role:'user',content:'Why?'}]})}));assert.equal(result.status,400);});
test('client surfaces server failures instead of treating them as success',async()=>{const original=globalThis.fetch;try{globalThis.fetch=async()=>Response.json({error:'Service unavailable'},{status:503});await assert.rejects(fetchJson('/test'),/Service unavailable/);}finally{globalThis.fetch=original;}});
test('client bounds a stalled request',async()=>{const original=globalThis.fetch;try{globalThis.fetch=async(_url,init)=>new Promise((_resolve,reject)=>init?.signal?.addEventListener('abort',()=>reject(new Error('aborted'))));await assert.rejects(fetchJson('/test',{},10),/longer than expected/);}finally{globalThis.fetch=original;}});
test('full practice handler produces a displayable five-question mixed session',async()=>{
 const original=globalThis.fetch, key=process.env.ANTHROPIC_API_KEY;
 process.env.ANTHROPIC_API_KEY='test-only';
 try {
  globalThis.fetch=async(_url,init)=>{
   const body=JSON.parse(String(init?.body));
   const count=Number(body.system.match(/EXACTLY (\d+) questions/)[1]);
   const payload={questions:Array.from({length:count},()=>q),passage:{title:'Reading',content:'Context for the questions.'}};
   return Response.json({id:'msg_test',type:'message',role:'assistant',model:'claude-sonnet-4-6',content:[{type:'text',text:JSON.stringify(payload)}],stop_reason:'end_turn',stop_sequence:null,usage:{input_tokens:10,output_tokens:10}});
  };
  const result=await generate(new Request('http://localhost/api/practice/generate',{method:'POST',body:JSON.stringify({section:'mixed',count:5,difficulty:'medium'})}));
  assert.equal(result.status,200);
  const body=await result.json();assert.equal(body.questions.length,5);assert.equal(new Set(body.questions.map((x:{section:string})=>x.section)).size,4);assert.ok(body.questions.find((x:{section:string})=>x.section==='cars').passage);assert.ok(body.questions.every((x:{question_text:string;choice_a:string})=>x.question_text&&x.choice_a));
 }finally{globalThis.fetch=original;if(key===undefined)delete process.env.ANTHROPIC_API_KEY;else process.env.ANTHROPIC_API_KEY=key;}
});
test('full explanation handler accepts the repaired screen payload',async()=>{
 const original=globalThis.fetch,key=process.env.ANTHROPIC_API_KEY;process.env.ANTHROPIC_API_KEY='test-only';
 try{
 globalThis.fetch=async(_url,init)=>{const body=JSON.parse(String(init?.body));assert.ok(body.system.includes(q.stem));return Response.json({id:'msg_test',type:'message',role:'assistant',model:'claude-sonnet-4-6',content:[{type:'text',text:'Let us work through the reasoning.'}],stop_reason:'end_turn',stop_sequence:null,usage:{input_tokens:10,output_tokens:10}});};
 const result=await explain(new Request('http://localhost/api/practice/explain',{method:'POST',body:JSON.stringify({question:parseQuestions({questions:[q]},'bio-biochem',1,false)[0],studentAnswer:'B',messages:[{role:'user',content:'Why?'}]})}));assert.equal(result.status,200);assert.equal((await result.json()).reply,'Let us work through the reasoning.');
 }finally{globalThis.fetch=original;if(key===undefined)delete process.env.ANTHROPIC_API_KEY;else process.env.ANTHROPIC_API_KEY=key;}
});
