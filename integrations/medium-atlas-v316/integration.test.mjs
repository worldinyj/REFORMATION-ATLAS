import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleV315} from '../medium-atlas-v315/overlay.mjs';
import {assembleV316} from './overlay.mjs';
const bytes=p=>readFileSync(new URL('../../'+p,import.meta.url));
const json=p=>JSON.parse(bytes(p));
const m=json('integrations/medium-atlas-v316/manifest.json');
const base=m.inputs.map(i=>json(i.path)),audit=m.auditInputs.map(i=>json(i.path));
const [a,b,c,d,e,f]=[m.addendumInput,m.latinInput,m.editionInput,m.authInput,m.wordingInput,m.witnessInput].map(i=>json(i.path));
const prev=assembleV315(base,...audit,a,b,c,d,e),now=assembleV316(base,...audit,a,b,c,d,e,f);
const mutate=change=>{const x=structuredClone(f);change(x);return ()=>assembleV316(base,...audit,a,b,c,d,e,x);};
test('historical JSON and every inherited immutable source is SHA-pinned',()=>{
 for(const s of [...m.inputs,...m.auditInputs,m.addendumInput,m.latinInput,m.editionInput,m.authInput,m.wordingInput,m.witnessInput]){
  const raw=bytes(s.path);
  if(s.sha256)assert.equal(createHash('sha256').update(raw).digest('hex'),s.sha256,s.path);
  if(s.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+raw.length+'\0'),raw])).digest('hex'),s.gitBlobSha1,s.path);
 }
});
test('513 manuscripts, 723 sources, 97 overview rows and all V3.11–15 research remain intact',()=>{
 for(const k of ['readers','sources','source_verification','primary_passage_addenda','primary_passage_claims',
   'latin_english_limited_concordance_v312','edition_archive_provenance_v313',
   'source_attestation_v314','attestation_wording_v315'])assert.deepEqual(now.delivery[k],prev.delivery[k],k);
 assert.deepEqual(now.crosswalk,prev.crosswalk);
 assert.equal(now.delivery.publication_gate.published,false);
 assert.equal(now.delivery.editorial_audit.v316_witness_printing.original_pages_inspected,0);
});
test('Stettin historical print, Paderborn German IPO, separate IPM and institutional Austrian source remain differentiated',()=>{
 const o=new Map(f.source_records.map(x=>[x.id,x]));
 assert.equal(o.get('STETTIN').tier,'CATALOGUE_SEARCH_INDEX');
 assert.equal(o.get('LWL741').tier,'SCHOLARLY_SEARCH_INDEX_ONLY');
 assert.equal(o.get('PADERBORN').work,'IPO');
 assert.equal(o.get('WS1649').work,'IPM');
 assert.equal(o.get('DDB1648').work,'IPM');
 assert.match(o.get('PADERBORN').verified,/VD17 12:187744L/);
 assert.equal(f.inspection.actual_textual_variants_proven,undefined);
 assert.equal(f.inspection.new_textual_variants_proven,0);
});
test('three chapter supplements and four unresolved issues remain source linked',()=>{
 assert.deepEqual(f.metrics,{sources:7,studies:3,sections:9,claims:10,unresolved_issues:4,body_characters:2350});
 assert.equal(f.studies.flatMap(x=>x.sections).length,9);
 assert.deepEqual(new Set(f.issues.map(i=>i.id)),
 new Set(['STETTIN_MONTH','PRINT_VARIANTS','SIGNING_VENUE','PRINT_AUTHORITY']));
 const linked=now.getForV315('V315-SIGNING');
 assert.equal(linked.length,3);
 assert.ok(linked.every(x=>x.source_records.length>0));
 assert.deepEqual(now.getForV315('V315-ATTESTATION'),[]);
 linked[0].sections[0].body='tampered';
 assert.notEqual(now.getForV315('V315-SIGNING')[0].sections[0].body,'tampered');
 assert.throws(()=>now.getForV315('UNLISTED'),/unknown V315 reading/);
});
test('no publication, false page collation, invented print authority or missing provenance can pass',()=>{
 assert.throws(mutate(x=>x.publication_gate.published=true),/publication HOLD/);
 assert.throws(mutate(x=>x.inspection.original_print_pages_collated=1),/false original witness examination/);
 assert.throws(mutate(x=>x.source_records.find(s=>s.id==='LWL741').tier='INSTITUTION_LIVE_HTML'),/LWL blocked text promoted/);
 assert.throws(mutate(x=>x.source_records.find(s=>s.id==='STETTIN').original_pages_read=true),/bad witness/);
 assert.throws(mutate(x=>x.source_records.find(s=>s.id==='DDB1648').work='IPO'),/two treaty identities merged/);
 assert.throws(mutate(x=>x.claim_cards[0].source_ids=['BOGUS']),/incomplete claim/);
 assert.throws(mutate(x=>x.issues.find(i=>i.id==='SIGNING_VENUE').status='RESOLVED'),/invalid unresolved issue/);
});
