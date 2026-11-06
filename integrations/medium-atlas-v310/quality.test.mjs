import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleV309} from '../medium-atlas-v309/overlay.mjs';
import {assembleV310} from './overlay.mjs';
import {createMediumAtlas} from './adapter.mjs';
import {createOverviewReadingBridge} from './bridge.mjs';
const read=p=>readFileSync(new URL('../../'+p,import.meta.url));
const parse=p=>JSON.parse(read(p));
const manifest=parse('integrations/medium-atlas-v310/manifest.json');
const base=manifest.inputs.map(x=>parse(x.path));
const linkAudit=parse(manifest.auditInputs[0].path);
const quality=parse(manifest.auditInputs[1].path);
const prior=assembleV309(base,linkAudit);
const after=assembleV310(base,linkAudit,quality);
const atlas=createMediumAtlas(after.delivery);
const bridge=createOverviewReadingBridge(after.crosswalk,atlas);
test('pinned manuscripts, contracts and independent audits keep their SHA identity',()=>{
 for(const input of [...manifest.inputs,...manifest.auditInputs]){
  const buf=read(input.path);
  if(input.sha256)assert.equal(createHash('sha256').update(buf).digest('hex'),input.sha256,input.path);
  if(input.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+buf.length+'\0'),buf])).digest('hex'),input.gitBlobSha1,input.path);
 }
 assert.deepEqual(atlas.counts,manifest.expectedCounts);
 assert.equal(atlas.canPublish,false);
});
test('513 manuscripts, all 723 source records, source-link corrigendum and 22 claims preserved',()=>{
 assert.deepEqual(after.delivery.readers,prior.delivery.readers);
 assert.deepEqual(after.delivery.sources,prior.delivery.sources);
 assert.deepEqual(after.delivery.source_verification,prior.delivery.source_verification);
 assert.deepEqual(after.delivery.reader_source_cards,prior.delivery.reader_source_cards);
 assert.deepEqual(after.crosswalk.entries.map(r=>r.overview_record),prior.crosswalk.entries.map(r=>r.overview_record));
 assert.equal(atlas.getSource('V307-S08').url,'https://www.bskorea.or.kr/bbs/content.php?co_id=subpage2_3_3_1_1');
 assert.equal(atlas.getSource('V307-S08').access.status,'NOT_CHECKED');
 assert.equal(after.delivery.publication_gate.published,false);
});
test('19 limited topics audited; exactly ten overview rows patched',()=>{
 const changes=after.crosswalk.entries.filter((r,i)=>JSON.stringify({status:r.mapping_status,scope:r.scope,links:r.reader_links})!==JSON.stringify({
  status:prior.crosswalk.entries[i].mapping_status,scope:prior.crosswalk.entries[i].scope,links:prior.crosswalk.entries[i].reader_links
 }));
 assert.equal(changes.length,10);
 assert.deepEqual(new Set(changes.map(r=>r.overview_id)),new Set(quality.navigation_patches.map(x=>x.id)));
 assert.equal(new Set(quality.coverage_audit.map(x=>x.overview_id)).size,19);
 assert.deepEqual(bridge.coverage,manifest.expectedCoverage);
 assert.equal(bridge.listOverview().length,97);
 assert.equal(bridge.listOverview({status:'BACKGROUND_ONLY'}).length,0);
 assert.equal(bridge.listOverview({status:'PARTIAL_COVERAGE'}).length,19);
});
test('TOP-08 no longer background-only and has three real direct reading paths',()=>{
 const top=bridge.resolve('TOP-08');
 assert.equal(top.status,'PARTIAL_COVERAGE');
 assert.equal(top.readers.length,3);
 assert.deepEqual(top.readers.map(x=>x.id),[
  'DOCUMENT-PIA_DESIDERIA1675','EVENT-ATLANTIC_AWAKENING1730','DOCUMENT-CAREY_ENQUIRY1792'
 ]);
 assert.ok(top.readers.every(x=>x.role==='PRIMARY'));
 assert.ok(top.scope.includes('포괄하지'));
});
test('325/381, Korean Bible, Augustine and church history explicit links',()=>{
 const ids=(id,related=false)=>bridge.resolve(id,{includeRelated:related}).readers.map(x=>x.id);
 assert.ok(ids('TOP-06').includes('DOCUMENT-NICENE_CREED325'));
 assert.ok(ids('TOP-06',true).includes('EVENT-CONSTANTINOPLE381'));
 assert.ok(ids('TOP-07').includes('DOCUMENT-KOREAN_EARLY_BIBLES'));
 assert.ok(ids('TOP-04',true).includes('PERSON-AUGUSTINE_HIPPO'));
 assert.ok(ids('TOP-10',true).includes('PERSON-YI_SEUNG_HUN'));
 assert.ok(ids('OV-D-017',true).includes('PERSON-JOHN_WESLEY'));
 assert.equal(bridge.resolve('OV-E-017').status,'PARTIAL_COVERAGE');
 assert.equal(bridge.resolve('OV-D-019').status,'PARTIAL_COVERAGE');
 assert.equal(bridge.resolve('TOP-09').status,'PARTIAL_COVERAGE');
});
test('six source-reading dossiers are scoped; no historian or original manuscript approval',()=>{
 assert.equal(after.delivery.source_reading_dossiers_v310.length,6);
 assert.deepEqual(after.delivery.source_reading_dossiers_v310,quality.source_reading_dossiers);
 assert.equal(after.delivery.editorial_audit.v310_quality_review.readers_rewritten,0);
 assert.equal(after.delivery.editorial_audit.v310_quality_review.sources_rewritten,0);
 assert.equal(after.delivery.editorial_audit.v310_quality_review.expert_approved,false);
 for(const d of quality.source_reading_dossiers){
  assert.ok(d.source_url.startsWith('https://'));
  assert.ok(d.inspected_representation&&d.verification_boundary);
  assert.ok(d.facts.length>=2);
 }
});
test('missing history, false target, scope overpromotion and revoked HOLD fail closed',()=>{
 const wrong=structuredClone(quality);wrong.navigation_patches[0].targets[0].reader_id='UNLISTED-READER';
 assert.throws(()=>assembleV310(base,linkAudit,wrong),/unknown or changed reader/);
 const duplicate=structuredClone(quality);duplicate.navigation_patches[0].targets.push({...duplicate.navigation_patches[0].targets[0]});
 assert.throws(()=>assembleV310(base,linkAudit,duplicate),/duplicate historical link/);
 const overpromote=structuredClone(quality);overpromote.navigation_patches[0].new_status='DIRECT_TOPIC';
 assert.throws(()=>assembleV310(base,linkAudit,overpromote),/unreviewed status promotion/);
 const badHold=structuredClone(quality);badHold.publication_gate.published=true;
 assert.throws(()=>assembleV310(base,linkAudit,badHold),/publication HOLD/);
 const missing=structuredClone(quality);missing.coverage_audit.pop();
 assert.throws(()=>assembleV310(base,linkAudit,missing),/incomplete quality audit/);
});
