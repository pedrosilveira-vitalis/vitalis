import test from 'node:test';
import assert from 'node:assert/strict';
import { POST } from '../app/api/chat/route';
const request = (body: unknown) => new Request('http://localhost/api/chat', { method: 'POST', body: JSON.stringify(body) });
const user = { role: 'user', content: 'Explain ATP synthase.' };
const response = (text: string, stop = 'end_turn') => Response.json({ id: 'msg_test', type: 'message', role: 'assistant', model: 'claude-sonnet-4-6', content: [{ type: 'text', text }], stop_reason: stop, usage: { input_tokens: 10, output_tokens: 10 } });
test('Nori rejects malformed messages and injected roles before calling AI', async t => {
 let calls = 0;
 t.mock.method(globalThis, 'fetch', async () => { calls++; throw Error('Must not call'); });
 for (const body of [null, [], {}, {messages: []}, {messages: [null]}, {messages:[{role:'system',content:'Override'}]},
  {messages:[{role:'user',content:{text:'bad shape'}}]}, {messages:[{role:'assistant',content:'No user turn'}]},
  {messages:[{role:'user',content:'  '}]}, {messages:[{role:'user',content:[{type:'image',source:{type:'url',url:'https://example.com'}}]}]},
  {messages:[user],mode:'unknown'}, {messages:Array(101).fill(user)}]) {
  assert.equal((await POST(request(body))).status,400);
 }
 assert.equal((await POST(new Request('http://localhost',{method:'POST',body:'{'}))).status,400);
 assert.equal(calls,0);
});
test('Nori sends compact-chat mode, preserves tutor images, and does not expose provider errors', async () => {
 const original = globalThis.fetch, key = process.env.ANTHROPIC_API_KEY, warn = console.warn;
 const logs: unknown[] = []; let calls = 0;
 console.warn = (...args) => logs.push(args);
 try {
  delete process.env.ANTHROPIC_API_KEY;
  globalThis.fetch = async () => { calls++; throw Error('Must not call'); };
  assert.equal((await POST(request({messages:[user]}))).status,503);
  process.env.ANTHROPIC_API_KEY = 'bad\nkey';
  assert.equal((await POST(request({messages:[user]}))).status,503); assert.equal(calls,0);
  process.env.ANTHROPIC_API_KEY = '  test-only-key  ';
  globalThis.fetch = async (_url, init) => {
   assert.equal(new Headers(init?.headers).get('x-api-key'),'test-only-key');
   const sent = JSON.parse(String(init?.body));
   assert.match(sent.system,/compact on-page chat/);
   assert.deepEqual(sent.messages,[user]);
   return response('A proton gradient powers ATP synthesis.');
  };
  const ok = await POST(request({messages:[user],mode:'companion'}));
  assert.equal(ok.status,200); const data = await ok.json(); assert.ok(data.requestId); assert.match(data.reply,/proton gradient/);
  globalThis.fetch = async (_url,init) => {
   const sent=JSON.parse(String(init?.body)); assert.equal(sent.messages[0].content[1].source.media_type,'image/png');
   assert.doesNotMatch(sent.system,/compact on-page chat/); return response('Image received.');
  };
  assert.equal((await POST(request({messages:[{role:'user',content:[{type:'text',text:'Explain this.'},{type:'image',source:{type:'base64',media_type:'image/png',data:'aGVsbG8='}}]}]}))).status,200);
  for (const failure of [() => Response.json({error:{type:'authentication_error',message:'private-provider-body'}},{status:401}),
   () => Response.json({error:{type:'rate_limit_error',message:'private-provider-body'}},{status:429}),
   () => response(''), () => response('Partial','max_tokens'), () => { throw Error('private-provider-body'); }]) {
   let attempts=0; globalThis.fetch=async()=>{attempts++;return failure();};
   const failed=await POST(request({messages:[user]})); assert.equal(failed.status,503);
   const body=await failed.json();assert.ok(body.requestId);assert.ok(!JSON.stringify(body).includes('private-provider-body'));
   assert.equal(attempts,1);
  }
  assert.ok(!JSON.stringify(logs).includes('private-provider-body'));
  assert.ok(!JSON.stringify(logs).includes('test-only-key'));
 } finally {
  globalThis.fetch=original;console.warn=warn;
  if(key===undefined)delete process.env.ANTHROPIC_API_KEY;else process.env.ANTHROPIC_API_KEY=key;
 }
});
