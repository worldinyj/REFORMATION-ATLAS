import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleV316} from '../medium-atlas-v316/overlay.mjs';
import {assembleV317} from './overlay.mjs';
const bytes=p=>readFileSync(new URL('../../'+p,import.meta.url));
const read=p=>JSON.parse(bytes(p));
const m=read('integrations/medium-atlas-v317/manifest.json');
const base=m.inputs.map(x=>read(x.path)),audit=m.auditInputs.map(x=>read(x.path));
const [a,b,c,d,e,f,g]=[
 m.addendumInput,m.latinInput,m.editionInput,m.authInput,
 m.wordingInput,m.ratificationInput,m.witnessPrintInput].map(x=>read(x.path));
const old=assembleV316(base,...audit,a,b,c,d,e,f);
const now=assembleV317(base,...audit,a,b,c,d,e,f,g);
const bad=change=>{const copy=structuredClone(g);change(copy);return ()=>assembleV317(base,...audit,a,b,c,d,e,f,copy);};
test('all inherited sources, separate V3.16 chronology and V3.17 early print data are SHA pinned',()=>{
 for(const x of [...m.inputs,...m.auditInputs,m.addendumInput,m.latinInput,
  m.editionInput,m.authInput,m.wordingInput,m.ratificationInput,m.witnessPrintInput]){
  const data=bytes(x.path);
  if(x.sha256)assert.equal(createHash('sha256').update(data).digest('hex'),x.sha256,x.path);
  if(x.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+data.length+'\0'),data])).digest('hex'),x.gitBlobSha1,x.path);
 }
});
test('513 original readers, 723 sources and V3.11 through V3.16 research remain unchanged',()=>{
 for(const key of ['readers','sources','source_verification','primary_passage_addenda','primary_passage_claims',
 'latin_english_limited_concordance_v312','edition_archive_provenance_v313',
 'source_attestation_v314','attestation_wording_v315','ratification_event_v316'])
  assert.deepEqual(now.delivery[key],old.delivery[key],key);
 assert.deepEqual(now.crosswalk,old.crosswalk);
 assert.equal(now.delivery.ratification_event_v316.chronology.length,4);
 assert.equal(now.delivery.publication_gate.published,false);
});
test('Stettin metadata proves a 1648 edition and mentions July/August, not October signed text equality',()=>{
 const src=new Map(g.source_records.map(s=>[s.id,s]));
 assert.equal(src.get('STETTIN').tier,'DIGITAL_LIBRARY_LIVE_CATALOGUE_HTML');
 assert.match(src.get('STETTIN').verified,/7월 27일/);
 assert.match(src.get('STETTIN').verified,/8월 6일/);
 assert.match(src.get('STETTIN').boundary,/10월 24일/);
 assert.equal(src.get('STETTIN').original_pages_read,false);
 assert.equal(src.get('LWL741').tier,'SCHOLARLY_SEARCH_INDEX_ONLY');
 assert.match(src.get('LWL741').boundary,/유지관리/);
});
test('IPO / IPM source lines, three bounded readings and four unresolved issues are maintained',()=>{
 assert.deepEqual([g.source_records.length,g.studies.length,
  g.studies.flatMap(x=>x.sections).length,g.claim_cards.length,g.issues.length],[7,3,9,10,4]);
 assert.equal(g.metrics.body_characters,2446);
 assert.equal(g.inspection.new_textual_variants_proven,0);
 assert.equal(g.source_records.find(x=>x.id==='DDB1648').work,'IPM');
 assert.equal(g.source_records.find(x=>x.id==='PADERBORN').work,'IPO');
 assert.deepEqual(g.issues.map(x=>x.status),['UNRESOLVED','NOT_COLLATED','UNRESOLVED','NOT_COLLATED']);
 const r=now.getPrintWitnessStudiesForV315('V315-SIGNING');
 assert.equal(r.length,3);
 assert.ok(r[0].source_records.length>=3);
 const snapshot=r[0].sections[0].body;r[0].sections[0].body='modified';
 assert.equal(now.getPrintWitnessStudiesForV315('V315-SIGNING')[0].sections[0].body,snapshot);
 assert.throws(()=>now.getPrintWitnessStudiesForV315('MISSING'),/unknown V315 parent/);
});
test('fabricated source inspection, signed treaty, resolved issues and publication release fail closed',()=>{
 assert.throws(bad(x=>x.inspection.original_print_pages_collated=1),/fabricated original-page inspection/);
 assert.throws(bad(x=>x.inspection.new_textual_variants_proven=1),/fabricated original-page inspection/);
 assert.throws(bad(x=>x.source_records.find(s=>s.id==='STETTIN').boundary='proven final treaty'),/Stettin publication certainty overstated/);
 assert.throws(bad(x=>x.source_records.find(s=>s.id==='LWL741').tier='HISTORIAN_LIVE_HTML'),/LWL indexed note promoted/);
 assert.throws(bad(x=>x.issues[0].status='RESOLVED'),/issue status prematurely resolved/);
 assert.throws(bad(x=>x.claim_cards[0].source_ids=['NOT-FOUND']),/unsupported historical claim/);
 assert.throws(bad(x=>x.publication_gate.published=true),/publication HOLD/);
});
