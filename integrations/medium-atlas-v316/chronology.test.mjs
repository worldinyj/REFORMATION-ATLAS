import test from 'node:test';import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';import {createHash} from 'node:crypto';
import {assembleV315} from '../medium-atlas-v315/overlay.mjs';import {assembleV316} from './overlay.mjs';
const bytes=p=>readFileSync(new URL('../../'+p,import.meta.url)),read=p=>JSON.parse(bytes(p));
const m=read('integrations/medium-atlas-v316/manifest.json'),inputs=m.inputs.map(s=>read(s.path)),audits=m.auditInputs.map(s=>read(s.path));
const extensions=[m.addendumInput,m.latinInput,m.editionInput,m.authInput,m.wordingInput].map(s=>read(s.path));
const dataset=read(m.ratificationInput.path),v315=assembleV315(inputs,...audits,...extensions),v316=assembleV316(inputs,...audits,...extensions,dataset);
const changed=fn=>{const item=structuredClone(dataset);fn(item);return ()=>assembleV316(inputs,...audits,...extensions,item);};
test('inputs and new ratification data byte hashes match Git blobs',()=>{
 for(const item of [...m.inputs,...m.auditInputs,m.addendumInput,m.latinInput,m.editionInput,m.authInput,m.wordingInput,m.ratificationInput]){
  const b=bytes(item.path);
  if(item.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),item.sha256,item.path);
  if(item.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),item.gitBlobSha1,item.path);
 }
});
test('all 513 manuscripts 723 sources 22 selected claims 97 overview entries and prior studies unchanged',()=>{
 for(const key of ['readers','sources','source_verification','attestation_wording_v315','source_attestation_v314',
 'edition_archive_provenance_v313','latin_english_limited_concordance_v312','primary_passage_addenda'])
  assert.deepEqual(v316.delivery[key],v315.delivery[key],key);
 assert.deepEqual(v316.crosswalk,v315.crosswalk);
 assert.equal(v316.delivery.publication_gate.published,false);
});
test('four historical events are disjoint and dated from source-specific chronology',()=>{
 assert.deepEqual(dataset.chronology.map(x=>x.date),['1648-10-24','1648-10-25','1649-02-18','1649-02-21']);
 assert.deepEqual(dataset.chronology.map(x=>x.type),['SIGNING_AND_SEALING','PUBLIC_PROCLAMATION','ACTUAL_RATIFICATION_EXCHANGE','PUBLIC_RATIFICATION_CELEBRATION']);
 assert.equal(v316.delivery.ratification_event_v316.claims.length,5);
 assert.equal(dataset.reading.sections.reduce((n,s)=>n+s.body.length,0),1055);
 assert.equal(v316.getRatificationReadingForV315('V315-SIGNING').length,1);
 assert.deepEqual(v316.getRatificationReadingForV315('V315-ATTESTATION'),[]);
});
test('museum, treaty, bibliography and original-holding evidence never upgrade automatically',()=>{
 assert.equal(dataset.inspection.original_treaty_pages_viewed,0);
 const a=new Map(dataset.source_records.map(x=>[x.id,x]));
 assert.match(a.get('V316-ARCHIVE-IPM').locator,/34 aufgedrückte Siegel/);
 assert.match(a.get('V316-IPM-PARAGRAPHS').access,/MAINTENANCE/);
 assert.ok(dataset.claim_cards.every(c=>c.historian_approved===false&&c.source_images_inspected===false));
});
test('unverified dates, broken archive references, changed HOLD and fake physical inspections fail closed',()=>{
 assert.throws(changed(x=>x.chronology[2].date='1648-12-19'),/unverified date/);
 assert.throws(changed(x=>x.chronology[2].type='PUBLIC_RATIFICATION_CELEBRATION'),/unverified date/);
 assert.throws(changed(x=>x.source_records[0].locator='unknown'),/improper archival seal count/);
 assert.throws(changed(x=>x.source_records[1].access='HTML_FULL_TEXT_READ'),/inaccessible text promoted/);
 assert.throws(changed(x=>x.inspection.original_treaty_pages_viewed=1),/invented original treaty inspection/);
 assert.throws(changed(x=>x.publication_gate.published=true),/publication HOLD/);
});
