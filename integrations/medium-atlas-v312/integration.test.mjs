import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleV311} from '../medium-atlas-v311/overlay.mjs';
import {assembleV312} from './overlay.mjs';
const bytes=p=>readFileSync(new URL('../../'+p,import.meta.url));
const json=p=>JSON.parse(bytes(p));
const manifest=json('integrations/medium-atlas-v312/manifest.json');
const inputs=manifest.inputs.map(i=>json(i.path)),audits=manifest.auditInputs.map(i=>json(i.path));
const v311=json(manifest.addendumInput.path),latin=json(manifest.latinInput.path);
const prev=assembleV311(inputs,...audits,v311),current=assembleV312(inputs,...audits,v311,latin);
test('all prior snapshots and new Latin dataset are hash-pinned',()=>{
 for(const i of [...manifest.inputs,...manifest.auditInputs,manifest.addendumInput,manifest.latinInput]){
   const raw=bytes(i.path);
   if(i.sha256)assert.equal(createHash('sha256').update(raw).digest('hex'),i.sha256,i.path);
   if(i.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+raw.length+'\0'),raw])).digest('hex'),i.gitBlobSha1,i.path);
 }
});
test('frozen 513 originals, 723 source records, 22 legacy claim audits and 97 overview items remain identical',()=>{
 assert.deepEqual(current.delivery.readers,prev.delivery.readers);
 assert.deepEqual(current.delivery.sources,prev.delivery.sources);
 assert.deepEqual(current.delivery.source_verification,prev.delivery.source_verification);
 assert.deepEqual(current.delivery.primary_passage_addenda,prev.delivery.primary_passage_addenda);
 assert.deepEqual(current.delivery.primary_passage_claims,prev.delivery.primary_passage_claims);
 assert.deepEqual(current.crosswalk,prev.crosswalk);
});
test('Latin transcription locations, English translations and parent claim IDs stay paired',()=>{
 assert.equal(latin.concordance_cards.length,4);
 assert.deepEqual(latin.concordance_cards.map(c=>c.parent_v311_claim),['TR-02','TR-03','WF-02','WF-03']);
 const ids=new Set(latin.source_records.map(s=>s.id));
 for(const c of latin.concordance_cards){
  assert.ok(ids.has(c.latin_source_id)&&ids.has(c.english_source_id));
  assert.equal(c.original_witness_collated,false);
  assert.ok(c.original_fragment.split(/\s+/).length<13);
  assert.ok(c.interpretation_ko.length>=30);
 }
 assert.equal(current.delivery.editorial_audit.v312_latin_concordance.archival_original_collations,0);
});
test('bounded reading notes connect to V3.11 addenda without inflating the reader catalogue',()=>{
 assert.equal(current.getLatinNotesForAddendum('ATLAS-V311-TRENT').length,1);
 assert.equal(current.getLatinNotesForAddendum('ATLAS-V311-WESTPHALIA').length,1);
 assert.deepEqual(current.getLatinNotesForAddendum('ATLAS-V311-WCC'),[]);
 assert.throws(()=>current.getLatinNotesForAddendum('UNLISTED'),/unknown parent addendum/);
 assert.equal(current.delivery.readers.length,513);
 assert.equal(latin.medium_readings.reduce((n,r)=>n+r.sections.length,0),6);
});
test('unsupported source ID, invented archival proof and revoked HOLD fail closed',()=>{
 const bad=structuredClone(latin);bad.concordance_cards[0].english_source_id='NO-SOURCE';
 assert.throws(()=>assembleV312(inputs,...audits,v311,bad),/missing English translation/);
 const falseApproval=structuredClone(latin);falseApproval.concordance_cards[0].original_witness_collated=true;
 assert.throws(()=>assembleV312(inputs,...audits,v311,falseApproval),/unqualified evidence/);
 const released=structuredClone(latin);released.publication_gate.published=true;
 assert.throws(()=>assembleV312(inputs,...audits,v311,released),/publication HOLD/);
});
