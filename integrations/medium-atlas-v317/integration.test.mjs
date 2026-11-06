import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleV316} from '../medium-atlas-v316/overlay.mjs';
import {assembleV317} from './overlay.mjs';
const raw=p=>readFileSync(new URL('../../'+p,import.meta.url));
const read=p=>JSON.parse(raw(p));
const m=read('integrations/medium-atlas-v317/manifest.json');
const base=m.inputs.map(x=>read(x.path)),audit=m.auditInputs.map(x=>read(x.path));
const [v311,v312,v313,v314,v315,rat316,printing]=[
 m.addendumInput,m.latinInput,m.editionInput,m.authInput,m.wordingInput,
 m.ratificationInput,m.printingWitnessInput
].map(x=>read(x.path));
const previous=assembleV316(base,...audit,v311,v312,v313,v314,v315,rat316);
const next=assembleV317(base,...audit,v311,v312,v313,v314,v315,rat316,printing);
const invalid=fn=>{
 const edited=structuredClone(printing);fn(edited);
 return ()=>assembleV317(base,...audit,v311,v312,v313,v314,v315,rat316,edited);
};
test('every frozen input and new printing witness are SHA-pinned',()=>{
 for(const x of [...m.inputs,...m.auditInputs,m.addendumInput,m.latinInput,
    m.editionInput,m.authInput,m.wordingInput,m.ratificationInput,m.printingWitnessInput]){
  const data=raw(x.path);
  if(x.sha256)assert.equal(createHash('sha256').update(data).digest('hex'),x.sha256,x.path);
  if(x.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+data.length+'\0'),data])).digest('hex'),x.gitBlobSha1,x.path);
 }
});
test('513 canonical manuscripts, 723 canonical sources, 97 overviews and V3.11–V3.16 notes stay identical',()=>{
 for(const k of ['readers','sources','source_verification','primary_passage_addenda',
  'primary_passage_claims','latin_english_limited_concordance_v312',
  'edition_archive_provenance_v313','source_attestation_v314',
  'attestation_wording_v315','ratification_event_v316'])
  assert.deepEqual(next.delivery[k],previous.delivery[k],k);
 assert.deepEqual(next.crosswalk,previous.crosswalk);
 assert.equal(next.delivery.publication_gate.published,false);
 assert.deepEqual(next.delivery.ratification_event_v316.chronology.map(e=>e.date),
   ['1648-10-24','1648-10-25','1649-02-18','1649-02-21']);
});
test('original proposal keeps seven tiered source records, three readings, ten claims and four open questions',()=>{
 assert.equal(printing.source_records.length,7);
 assert.equal(printing.studies.length,3);
 assert.equal(printing.studies.flatMap(x=>x.sections).length,9);
 assert.equal(printing.metrics.body_characters,2350);
 assert.equal(printing.claim_cards.length,10);
 assert.equal(printing.issues.length,4);
 assert.ok(printing.source_records.every(x=>x.original_pages_read===false));
 assert.equal(next.delivery.editorial_audit.v317_print_witnesses.original_witnesses_collated,0);
});
test('Stettin is probable by indexed scholarship; publishing privilege and signing venue remain unproven',()=>{
 const sources=new Map(printing.source_records.map(s=>[s.id,s]));
 assert.equal(sources.get('STETTIN').tier,'CATALOGUE_SEARCH_INDEX');
 assert.equal(sources.get('LWL741').tier,'SCHOLARLY_SEARCH_INDEX_ONLY');
 assert.equal(sources.get('PADERBORN').work,'IPO');
 assert.equal(sources.get('DDB1648').work,'IPM');
 assert.equal(printing.claim_cards.find(c=>c.id==='ST-2').level,'INDEXED_EDITORIAL_PROBABILITY');
 assert.equal(printing.claim_cards.find(c=>c.id==='IP-3').level,'PRINTER_SELF_ATTESTATION');
 assert.equal(printing.claim_cards.find(c=>c.id==='VE-2').level,'UNRESOLVED_VENUE_DETAIL');
 assert.ok(printing.issues.every(q=>q.status!=='RESOLVED'));
});
test('new reader navigation returns defensive copies without touching earlier evidence',()=>{
 const a=next.getPrintStudiesForV315('V315-SIGNING');
 assert.equal(a.length,3);
 assert.ok(a.every(x=>x.source_records.length>0));
 assert.deepEqual(next.getPrintStudiesForV315('V315-ATTESTATION'),[]);
 a[0].sections[0].body='tampered';
 assert.notEqual(next.getPrintStudiesForV315('V315-SIGNING')[0].sections[0].body,'tampered');
 assert.throws(()=>next.getPrintStudiesForV315('NOT_A_PARENT'),/unknown V3.15 study/);
});
test('fabricated source inspections, first-print certainty, resolved venue and public release fail closed',()=>{
 assert.throws(invalid(x=>x.inspection.original_print_pages_collated=1),/fabricated printed/);
 assert.throws(invalid(x=>x.source_records.find(s=>s.id==='LWL741').tier='HISTORIAN_LIVE_HTML'),/blocked LWL source/);
 assert.throws(invalid(x=>x.source_records.find(s=>s.id==='STETTIN').tier='ORIGINAL_PRINT_DIRECTLY_READ'),/Stettin original/);
 assert.throws(invalid(x=>x.claim_cards.find(c=>c.id==='ST-2').level='CERTAIN_FIRST_PRINT'),/Stettin probability/);
 assert.throws(invalid(x=>x.claim_cards.find(c=>c.id==='IP-3').level='OFFICIAL_CRITICAL_EDITION'),/publisher self-claim/);
 assert.throws(invalid(x=>x.issues.find(q=>q.id==='SIGNING_VENUE').status='RESOLVED'),/unsupported resolution/);
 assert.throws(invalid(x=>x.publication_gate.published=true),/publication HOLD/);
});
