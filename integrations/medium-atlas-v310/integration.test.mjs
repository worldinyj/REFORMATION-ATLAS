import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleV309} from '../medium-atlas-v309/overlay.mjs';
import {assembleV310} from './overlay.mjs';
import {createMediumAtlas} from './adapter.mjs';
import {createOverviewReadingBridge} from './bridge.mjs';
const load=p=>readFileSync(new URL('../../'+p,import.meta.url));
const manifest=JSON.parse(load('integrations/medium-atlas-v310/manifest.json'));
const inputs=manifest.inputs.map(x=>JSON.parse(load(x.path)));
const [v309,v310]=manifest.auditInputs.map(x=>JSON.parse(load(x.path)));
const baseline=assembleV309(inputs,v309),result=assembleV310(inputs,v309,v310);
const {delivery:b,crosswalk:x}=result,atlas=createMediumAtlas(b),bridge=createOverviewReadingBridge(x,atlas);
test('all six source files are unchanged from pinned Git or SHA256',()=>{
 for(const item of [...manifest.inputs,...manifest.auditInputs]){
  const raw=load(item.path);
  if(item.sha256)assert.equal(createHash('sha256').update(raw).digest('hex'),item.sha256);
  if(item.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+raw.length+'\0'),raw])).digest('hex'),item.gitBlobSha1);
 }
});
test('all 513 reader bodies, 723 sources, and 22 selected claims remain identical',()=>{
 assert.deepEqual(b.readers,baseline.delivery.readers);
 assert.deepEqual(b.sources,baseline.delivery.sources);
 assert.deepEqual(b.reader_source_cards,baseline.delivery.reader_source_cards);
 assert.deepEqual(b.source_verification,baseline.delivery.source_verification);
 assert.equal(b.metrics.readers,513);
 assert.equal(b.metrics.sections,1539);
 assert.equal(b.sources.find(s=>s.id==='V307-S08').url,'https://www.bskorea.or.kr/bbs/content.php?co_id=subpage2_3_3_1_1');
 assert.equal(atlas.counts.claims,22);
 assert.equal(atlas.counts.guides,11);
});
test('all 19 limited entries audited, 10 scoped corrections and 6 independent source dossiers',()=>{
 assert.equal(v310.coverage_audit.length,19);
 assert.deepEqual(new Set(v310.coverage_audit.map(e=>e.overview_id)).size,19);
 assert.equal(x.quality_audit.audited_limited_overviews,19);
 assert.equal(v310.navigation_patches.length,10);
 assert.equal(x.quality_audit.patched_overviews,10);
 assert.equal(b.source_reading_dossiers_v310.length,6);
 assert.ok(b.source_reading_dossiers_v310.every(d=>d.verification_boundary&&d.inspected_representation));
 assert.ok(b.source_reading_dossiers_v310.every(d=>d.source_url.startsWith('https://')));
 assert.ok(v310.coverage_audit.every(x=>x.expert_reviewed===false&&x.original_witness_collated===false));
 assert.equal(b.editorial_audit.v310_quality_review.expert_approved,false);
});
test('overview records retain original content but corrected navigation has readable targets',()=>{
 assert.deepEqual(x.entries.map(e=>e.overview_record),baseline.crosswalk.entries.map(e=>e.overview_record));
 assert.deepEqual(bridge.coverage,{total:97,direct:78,partial:19,background:0,missing:0});
 assert.equal(bridge.listOverview().length,97);
 assert.equal(bridge.listOverview({status:'BACKGROUND_ONLY'}).length,0);
 for(const p of v310.navigation_patches){
  const row=x.entries.find(r=>r.overview_id===p.id);
  assert.equal(row.scope,p.scope);
  const current=bridge.resolve(p.id,{includeRelated:true});
  assert.ok(p.targets.every(t=>current.readers.some(r=>r.id===t.reader_id&&r.role===t.role)));
  for(const t of p.targets)assert.ok(atlas.getReader(t.reader_id));
 }
 assert.deepEqual(bridge.resolve('TOP-08').readers.map(r=>r.id),
 ['DOCUMENT-PIA_DESIDERIA1675','EVENT-ATLANTIC_AWAKENING1730','DOCUMENT-CAREY_ENQUIRY1792']);
 assert.equal(bridge.resolve('TOP-08').status,'PARTIAL_COVERAGE');
 assert.ok(bridge.resolve('TOP-06').readers.some(x=>x.id==='DOCUMENT-NICENE_CREED325'));
 assert.ok(bridge.resolve('TOP-07').readers.some(x=>x.id==='DOCUMENT-KOREAN_EARLY_BIBLES'));
});
test('unmodified 87 overview links preserve old order, status and scope',()=>{
 const patched=new Set(v310.navigation_patches.map(p=>p.id));
 const old=new Map(baseline.crosswalk.entries.map(e=>[e.overview_id,e]));
 for(const row of x.entries)if(!patched.has(row.overview_id))assert.deepEqual(row,old.get(row.overview_id));
 assert.equal(x.entries.filter(e=>!patched.has(e.overview_id)).length,87);
});
test('revoked HOLD, unknown reader, unapproved status and false claim of expert review are blocked',()=>{
 const x1=structuredClone(v310);x1.publication_gate.published=true;
 assert.throws(()=>assembleV310(inputs,v309,x1),/publication HOLD/);
 const x2=structuredClone(v310);x2.navigation_patches[0].targets[0].reader_id='UNKNOWN_READER';
 assert.throws(()=>assembleV310(inputs,v309,x2),/unknown or changed reader/);
 const x3=structuredClone(v310);x3.navigation_patches[0].new_status='DIRECT_TOPIC';
 assert.throws(()=>assembleV310(inputs,v309,x3),/unreviewed status promotion/);
 const x4=structuredClone(v310);x4.coverage_audit[0].expert_reviewed=true;
 assert.throws(()=>assembleV310(inputs,v309,x4),/false source-verification promotion/);
 const x5=structuredClone(v310);x5.navigation_patches.pop();
 assert.throws(()=>assembleV310(inputs,v309,x5),/incomplete quality audit/);
});
