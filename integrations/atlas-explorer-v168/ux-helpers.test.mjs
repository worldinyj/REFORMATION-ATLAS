import test from 'node:test';
import assert from 'node:assert/strict';
import {safeText,filterCards,resultMessage,loadJson} from './ux-helpers.mjs';
const cards=[{heading:'후스의 교회론',sub:'1413년',body:'프라하'},
{heading:'칼뱅',sub:'1559년',body:'제네바'}];
test('Korean search and empty result',()=>{
 assert.equal(filterCards(cards,'후스').length,1);
 assert.equal(filterCards(cards,'1559').length,1);
 assert.equal(filterCards(cards,'존재하지 않음').length,0);
 assert.match(resultMessage(0),/검색 결과가 없습니다/);
});
test('escaped injected HTML',()=>{
 assert.equal(safeText('<script>alert("x")</script>'),'&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;');
});
test('proper HTTP failures and successful JSON',async()=>{
 await assert.rejects(loadJson(async()=>({ok:false,status:404}),'/missing.json'),/404/);
 assert.deepEqual(await loadJson(async()=>({ok:true,json:async()=>({a:1})}),'/ok.json'),{a:1});
});
