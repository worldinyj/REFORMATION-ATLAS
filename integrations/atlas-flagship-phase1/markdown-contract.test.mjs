import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {parseResearchMarkdown} from './research-markdown.mjs';

const source=await readFile(fileURLToPath(new URL('./preview-1529-1540.html',import.meta.url)),'utf8');
const parser=await readFile(fileURLToPath(new URL('./research-markdown.mjs',import.meta.url)),'utf8');
const js=source.split('<script>')[1]?.split('</script>')[0];
const payload=JSON.parse(source.split('id="data">')[1].split('</script>')[0]);

test('standalone HTML and React reference the exact same Markdown parser implementation',()=>{
  const begin=js.indexOf('function tokenizeInline(value) {');
  const end=js.indexOf('function renderResearchMarkdown(container,source){');
  assert.ok(begin>=0 && end>begin);
  const embedded=js.slice(begin,end).trim();
  const shared=parser.slice(0,parser.indexOf('export {parseResearchMarkdown};')).trim();
  assert.equal(embedded,shared);
});
test('L0 prose becomes headings, paragraphs, emphasis and a divider without changing research words',()=>{
  const blocks=parseResearchMarkdown(payload.l0.text);
  assert.equal(blocks.filter(b=>b.tag==='h3').length,4);
  assert.equal(blocks.filter(b=>b.tag==='hr').length,1);
  assert.ok(blocks.some(b=>b.segments.some(t=>t.kind==='strong')));
  assert.ok(blocks.some(b=>b.segments.some(t=>t.kind==='em')));
  assert.equal(payload.events.length,4);
  assert.equal(payload.docs.length,2);
  assert.equal(payload.canShip,false);
});
test('L1 preserves source while removing only Markdown presentation markers',()=>{
  const blocks=parseResearchMarkdown(payload.l1.text);
  assert.ok(blocks.length>=2);
  assert.equal(blocks.filter(b=>b.tag==='h3').length,0);
  const words=blocks.flatMap(b=>b.segments.map(t=>t.text)).join(' ');
  assert.match(words,/마르부르크/);
  assert.match(words,/Variata/);
  assert.doesNotMatch(words,/\*\*/);
});
test('HTML-looking strings are never emitted as executable HTML by parser',()=>{
  const input='### Test\n\n<img src=x onerror=alert(1)> **safe** *italic*';
  const parsed=parseResearchMarkdown(input);
  assert.equal(parsed[0].tag,'h3');
  assert.equal(parsed[1].tag,'p');
  assert.equal(parsed[1].segments[0].text,'<img src=x onerror=alert(1)> ');
  assert.deepEqual(parsed[1].segments.slice(1).map(t=>t.kind),['strong','text','em']);
  assert.doesNotMatch(js,/innerHTML|insertAdjacentHTML|dangerouslySetInnerHTML/);
});
