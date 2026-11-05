import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createMediumAtlas} from './adapter.mjs';
import {createOverviewReadingBridge} from './bridge.mjs';
const read=p=>JSON.parse(readFileSync(new URL('../../'+p,import.meta.url),'utf8'));
const bundle=read('data/deep/atlas_v302_integrated_455_medium_delivery.json');
const original=read('data/deep/atlas_v297_source_checked_medium_content_delivery_bundle.json');
const additions=read('data/deep/atlas_v301_medium_depth_precursors_hussite_readers.json');
const atlas=createMediumAtlas(bundle);
const bridge=createOverviewReadingBridge(read('data/contracts/atlas_v302_overview_medium_reading_crosswalk.json'),atlas);
test('all prior readers, sources and verification records are unchanged',()=>{
 assert.deepEqual(bundle.readers.slice(0,435),original.readers);
 assert.deepEqual(bundle.sources.slice(0,626),original.sources);
 assert.deepEqual(bundle.source_verification,original.source_verification);
});
test('all twenty additions preserve text and scoped source inspection metadata',()=>{
 for(const c of additions.chapters){
  const detail=atlas.getReader(c.id);assert.deepEqual(detail.sections,c.sections);
  assert.equal(detail.readingQuestion,c.reading_question);
  assert.deepEqual(detail.sources.map(s=>s.id),c.sources.map(s=>'V301-'+s));
  assert.equal(detail.sourceGuide,null);
  for(const s of detail.sources){
   const prior=additions.sources.find(x=>'V301-'+x.id===s.id);
   assert.equal(s.access.status,'NOT_CHECKED');assert.equal(s.access.checkedOn,null);
   assert.equal(s.priorInspection.note,prior.inspection_note);assert.equal(s.priorInspection.scope,prior.scope);
   assert.equal(s.priorInspection.checkedOn,prior.checked_on);assert.equal(s.priorInspection.recheckedThisVersion,false);
  }
 }
});
test('all twelve overview promotions retain former links and choose the new reading first',()=>{
 const old=read('data/contracts/atlas_v300_overview_medium_reading_crosswalk.json');
 for(const u of additions.overview_link_updates){
  const out=bridge.resolve(u.overview_id);assert.equal(out.status,'DIRECT_TOPIC');assert.equal(out.readers[0].id,u.reader_id);
  const all=bridge.resolve(u.overview_id,{includeRelated:true});
  for(const l of old.entries.find(x=>x.overview_id===u.overview_id).reader_links)assert.ok(all.readers.some(x=>x.id===l.reader_id));
 }
});
test('new paths cover all additions and old navigation stays intact',()=>{
 assert.deepEqual(bundle.reading_paths.slice(0,18),original.reading_paths);
 assert.deepEqual(new Set(bundle.reading_paths.slice(18).flatMap(p=>p.reader_ids)),new Set(additions.chapters.map(c=>c.id)));
 assert.ok(atlas.search('양형 영성체',{limit:100}).items.some(c=>c.id==='PERSON-JAKOUBEK_STRIBRO'));
 assert.equal(bridge.resolve('OV-E-014').readers[0].id,'EVENT-BASEL_SETTLEMENT1433_1436');
 assert.equal(bridge.resolve('OV-D-007').readers[0].id,'DOCUMENT-BASEL_COMPACTATA');
});
test('incomplete new navigation is rejected',()=>{
 const x=structuredClone(bundle);x.reading_paths.pop();assert.throws(()=>createMediumAtlas(x),/snapshot/);
});
