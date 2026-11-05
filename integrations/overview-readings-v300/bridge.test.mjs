import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {createMediumAtlas} from '../medium-atlas-v298/adapter.mjs';
import {createOverviewReadingBridge} from './bridge.mjs';
const read = p => JSON.parse(readFileSync(new URL('../../'+p,import.meta.url),'utf8'));
const data=read('data/contracts/atlas_v300_overview_medium_reading_crosswalk.json');
const atlas=createMediumAtlas(read('data/deep/atlas_v297_source_checked_medium_content_delivery_bundle.json'));
const bridge=createOverviewReadingBridge(data,atlas);
const mutate=fn=>{const v=structuredClone(data);fn(v);return v;};
const row=(x,id)=>x.entries.find(r=>r.overview_id===id);
test('overview inputs are pinned and all 97 original records match',()=>{
 for(const p of data.preserved_inputs){const raw=readFileSync(new URL('../../'+p.path,import.meta.url));assert.equal(createHash('sha256').update(raw).digest('hex'),p.sha256);}
 const people=read('data/overview/volumes_and_people_v01.json').people,ev=read('data/overview/events_documents_v01.json'),ideas=read('data/overview/relationships_and_themes_v01.json').ideas;
 const original=new Map([...people,...ev.events,...ev.documents,...ideas].map(r=>[r.id,r]));
 for(const r of data.entries)assert.deepEqual(r.overview_record,original.get(r.overview_id));
 assert.equal(original.size,97);assert.equal(bridge.listOverview().length,97);
});
test('coverage distinguishes direct, partial, background and missing',()=>{
 assert.deepEqual(bridge.coverage,{total:97,direct:26,partial:15,background:4,missing:52});
 assert.equal(bridge.listOverview({status:'NO_MATCH'}).length,52);
 assert.equal(bridge.canPublish,false);
});
test('all declared targets resolve without altering the source crosswalk',()=>{
 const old=JSON.stringify(data);
 for(const r of data.entries){const initial=bridge.resolve(r.overview_id),all=bridge.resolve(r.overview_id,{includeRelated:true});
  assert.deepEqual(initial.readers.map(t=>t.id),r.reader_links.filter(t=>t.role==='PRIMARY').map(t=>t.reader_id));
  assert.deepEqual(all.readers.map(t=>t.id),r.reader_links.map(t=>t.reader_id));
  for(const target of all.readers)assert.ok(atlas.getReader(target.id));
 }
 assert.equal(JSON.stringify(data),old);
});
test('1530 Augsburg submission is never mapped to 1555 peace',()=>{
 assert.deepEqual(bridge.resolve('OV-E-019',{includeRelated:true}).readers.map(r=>r.id),['MEDIUM-AUGSBURG']);
 assert.equal(bridge.resolve('OV-E-022').readers[0].id,'THEME-AUGSBURG_PEACE');
});
test('1536 event and first edition stay separate from 1559 follow-up reading',()=>{
 assert.deepEqual(bridge.resolve('OV-E-020',{includeRelated:true}).readers.map(r=>r.id),['MEDIUM-CALVIN1536']);
 assert.deepEqual(bridge.resolve('OV-D-012').readers.map(r=>r.id),['MEDIUM-CALVIN1536']);
 assert.deepEqual(bridge.resolve('OV-D-012',{includeRelated:true}).readers.map(r=>r.id),['MEDIUM-CALVIN1536','MEDIUM-CALVIN1559']);
});
test('same-name authors, medieval Basel and later reformers are not fuzzy matched',()=>{
 assert.equal(bridge.resolve('OV-P-001').status,'NO_MATCH');assert.deepEqual(bridge.resolve('OV-P-001').readers,[]);
 assert.equal(bridge.resolve('OV-P-021').readers[0].id,'PERSON-IGNATIUS');
 assert.equal(bridge.resolve('OV-D-005').readers[0].id,'MEDIUM-HUS');
 assert.equal(bridge.resolve('OV-E-014').status,'NO_MATCH');
});
test('Waldo gets background only on explicit request; missing Wesley gets none',()=>{
 const w=bridge.resolve('OV-P-008');assert.equal(w.hasPrimaryReading,false);assert.deepEqual(w.readers,[]);
 assert.equal(bridge.resolve('OV-P-008',{includeRelated:true}).readers[0].role,'BACKGROUND');
 assert.equal(bridge.resolve('OV-P-024',{includeRelated:true}).readers.length,0);
 assert.equal(bridge.resolve('OV-P-024').status,'NO_MATCH');
 assert.equal(bridge.resolve('존 웨슬리'),null);assert.equal(bridge.resolve('OV-P-999'),null);
});
test('reverse links are navigation references with role and scope',()=>{
 const links=bridge.forReader('MEDIUM-CALVIN1559');assert.ok(links.some(r=>r.overviewId==='OV-D-012'&&r.role==='FOLLOWUP'));
 assert.ok(!links.some(r=>r.overviewId==='OV-E-020'));assert.deepEqual(bridge.forReader('missing'),[]);
});
test('returned objects and caller input cannot change internal mappings',()=>{
 const input=structuredClone(data),b=createOverviewReadingBridge(input,atlas);row(input,'OV-P-013').reader_links=[];
 b.resolve('OV-P-013').readers.length=0;b.forReader('MEDIUM-HUS').length=0;
 assert.equal(b.resolve('OV-P-013').readers.length,2);assert.ok(b.forReader('MEDIUM-HUS').length>0);
});
const invalid=[
 ['bad version',x=>{x.version='9';}],['publication state',x=>{x.publication_gate.published=true;}],
 ['missing overview',x=>x.entries.pop()],['duplicate overview ID',x=>{x.entries[1].overview_id=x.entries[0].overview_id;}],
 ['wrong source identity',x=>{x.entries[0].overview_record.id='OV-P-999';}],
 ['unknown reader',x=>{row(x,'OV-P-013').reader_links[0].reader_id='missing';}],
 ['renamed target',x=>{row(x,'OV-P-013').reader_links[0].title='wrong';}],
 ['unknown role',x=>{row(x,'OV-P-013').reader_links[0].role='IDENTITY';}],
 ['background upgraded',x=>{row(x,'OV-P-008').reader_links[0].role='PRIMARY';}],
 ['missing scope',x=>{row(x,'OV-P-013').scope='';}],
 ['missing exclusion rules',x=>{x.exclusions=[];}],
 ['wrong Augsburg match',x=>{row(x,'OV-E-019').reader_links=[{reader_id:'THEME-AUGSBURG_PEACE',title:atlas.getReader('THEME-AUGSBURG_PEACE').title,role:'PRIMARY'}];}],
];
for(const [name,change]of invalid)test('reject '+name,()=>assert.throws(()=>createOverviewReadingBridge(mutate(change),atlas)));
test('requires the tested editorial consumer contract',()=>assert.throws(()=>createOverviewReadingBridge(data,{contractVersion:'future',canPublish:false})));
