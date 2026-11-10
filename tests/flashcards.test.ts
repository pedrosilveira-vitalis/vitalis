import test from 'node:test';
import assert from 'node:assert/strict';
import { POST } from '../app/api/flashcards/generate/route';
import { coreDeck } from '../lib/core-flashcards';
import { sections } from '../lib/practice';
const request = (body: unknown) => new Request('http://localhost/api/flashcards/generate', { method: 'POST', body: JSON.stringify(body) });
const message = (deck: unknown, stop = 'end_turn') => Response.json({ id: 'msg_test', type: 'message', role: 'assistant', model: 'claude-sonnet-4-6', content: [{ type: 'text', text: JSON.stringify({ deck }) }], stop_reason: stop, usage: { input_tokens: 10, output_tokens: 10 } });
test('core decks contain distinct, usable cards and sources without padding', () => {
  for (const section of sections) {
    const deck = coreDeck(section, 20);
    assert.equal(deck.cards.length, 6); assert.equal(deck.sources.length, 1);
    assert.equal(new Set(deck.cards.map(c => c.front)).size, 6);
    assert.ok(deck.cards.every(c => c.front.trim() && c.back.trim()));
    assert.equal(coreDeck(section, 2).cards.length, 2);
  }
  assert.equal(coreDeck('mixed', 20).cards.length, 20);
});
test('flashcards reject malformed inputs before calling provider', async () => {
  for (const body of [null, [], {section:'__proto__'}, {section:'cars',count:0}, {section:'cars',count:'8'}, {section:'cars',mode:'invalid'}]) {
    assert.equal((await POST(request(body))).status, 400);
  }
  assert.equal((await POST(new Request('http://localhost', {method:'POST',body:'{'}))).status,400);
});
test('flashcards support core mode, trimmed keys, and safe provider fallbacks', async () => {
  const original = globalThis.fetch, key = process.env.ANTHROPIC_API_KEY, warn = console.warn;
  const warnings: unknown[] = [];
  console.warn = (...args) => { warnings.push(args); };
  let calls = 0;
  try {
    delete process.env.ANTHROPIC_API_KEY;
    globalThis.fetch = async () => { calls++; throw new Error('Must not call'); };
    const missing = await (await POST(request({section:'cars',count:20}))).json();
    assert.equal(missing.source,'core'); assert.equal(missing.cards.length,6); assert.equal(calls,0);
    process.env.ANTHROPIC_API_KEY = '  test-only  ';
    const core = await (await POST(request({section:'chem-phys',mode:'core'}))).json();
    assert.equal(core.source,'core'); assert.equal(calls,0);
    globalThis.fetch = async (_url, init) => {
      assert.equal(new Headers(init?.headers).get('x-api-key'), 'test-only');
      return message([{front:'One?',back:'First.'},{front:'Two?',back:'Second.'}]);
    };
    const good = await (await POST(request({section:'bio-biochem',count:2}))).json();
    assert.equal(good.source,'ai'); assert.equal(good.cards.length,2); assert.ok(good.requestId);
    for (const response of [
      () => Response.json({error:{type:'authentication_error',message:'secret-provider-body'}},{status:401}),
      () => Response.json({error:{type:'rate_limit_error',message:'secret-provider-body'}},{status:429}),
      () => message([{front:'Only one',back:'Answer'}]),
      () => message([{front:'Same',back:'A'},{front:'same',back:'B'}]),
      () => message([{front:'Q',back:''},{front:'Q2',back:'A2'}]),
      () => message([], 'max_tokens'),
      () => { throw new Error('secret-provider-body'); },
    ]) {
      globalThis.fetch = async () => response();
      const fallback = await (await POST(request({section:'psych-soc',count:2}))).json();
      assert.equal(fallback.source,'core'); assert.equal(fallback.cards.length,2);
      assert.match(fallback.notice,/AI generation is unavailable/); assert.ok(fallback.requestId);
    }
    assert.ok(!JSON.stringify(warnings).includes('secret-provider-body'));
    assert.ok(!JSON.stringify(warnings).includes('test-only'));
  } finally {
    globalThis.fetch = original; console.warn = warn;
    if (key === undefined) delete process.env.ANTHROPIC_API_KEY; else process.env.ANTHROPIC_API_KEY = key;
  }
});
