import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import {assembleV313} from '../medium-atlas-v313/overlay.mjs';
import {assembleV314} from './overlay.mjs';
const buf=p=>readFileSync(new URL('../../'+p,import.meta.url)),parse=p=>JSON.parse(buf(p));
const m=parse('integrations/medium-atlas-v314/manifest.json');
const base=m.inputs.map(s=>parse(s.path)),[audit309,audit310]=m.auditInputs.map(s=>parse(s.path));
const add311=parse(m.addendumInput.path),latin312=parse(m.latinInput.path),ed313=parse(m.editionInput.path),auth314=parse(m.authInput.path);
const prev=assembleV313(base,audit309,audit310,add311,latin312,ed313);
const current=assembleV314(base,audit309,audit310,add311,latin312,ed313,auth314);
const run=x=>assembleV314(base,audit309,audit310,add311,latin312,ed313,x);
test('pinned legacy inputs, V3.13 edition inventory and V3.14 authentication contract',()=>{
 for(const i of [...m.inputs,...m.auditInputs,m.addendumInput,m.latinInput,m.editionInput,m.authInput]){
  const b=buf(i.path);
  if(i.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),i.sha256,i.path);
  if(i.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),i.gitBlobSha1,i.path);
 }
});
test('513 manuscripts, 723 legacy source entries, 22 selected claims and 97 overview links are not touched',()=>{
 assert.deepEqual(current.delivery.readers,prev.delivery.readers);
 assert.deepEqual(current.delivery.sources,prev.delivery.sources);
 assert.deepEqual(current.delivery.source_verification,prev.delivery.source_verification);
 assert.deepEqual(current.crosswalk,prev.crosswalk);
 assert.deepEqual(current.delivery.primary_passage_addenda,prev.delivery.primary_passage_addenda);
 assert.deepEqual(current.delivery.edition_archive_provenance_v313,prev.delivery.edition_archive_provenance_v313);
 assert.equal(current.delivery.publication_gate.published,false);
});
test('1564 museum-copy IDs and textual limits are explicit',()=>{
 const a=current.getAuthenticationNotesForStudy('V313-TRENT-PRINTS');
 assert.equal(a.length,1);
 assert.equal(a[0].id,'V314-MASSARELLI-AUTHENTICATION');
 assert.ok(a[0].sources.some(s=>s.id==='V314-TRENT-MD243'&&s.finding.includes('USTC')));
 assert.ok(a[0].sources.some(s=>s.id==='V314-TRENT-MUSEUM'));
 assert.equal(current.delivery.editorial_audit.v314_source_attestation.physical_original_pages_read,0);
});
test('IPO and IPM primary instruments and 1648 licensed prints not confused with official originals',()=>{
 const a=current.getAuthenticationNotesForStudy('V313-WESTPHALIA-PRINTS');
 assert.equal(a.length,1);
 assert.equal(a[0].id,'V314-PRINT-AUTHORITY-WESTPHALIA');
 assert.ok(a[0].sources.some(s=>s.id==='V314-WESTPHALIA-LWL741'&&s.access.includes('MAINTENANCE')));
 assert.equal(auth314.archive_inspection.actual_textual_variants_proven,0);
});
test('six source cards and all six medium sections preserve evidentiary boundaries',()=>{
 assert.deepEqual([auth314.sources.length,auth314.claims.length,auth314.studies.length],[6,6,2]);
 assert.equal(auth314.studies.reduce((n,r)=>n+r.sections.length,0),6);
 assert.equal(auth314.studies.reduce((n,r)=>n+r.sections.reduce((p,c)=>p+c.body.length,0),2017);
 assert.ok(auth314.claims.every(c=>!c.original_page_collated&&!c.historian_approved));
});
test('invented archive inspections, false validations and invalid references fail closed',()=>{
 const mod=fn=>{const c=structuredClone(auth314);fn(c);return ()=>run(c);};
 assert.throws(mod(c=>c.archive_inspection.museum_original_page_images_inspected=1),/invented original image collation/);
 assert.throws(mod(c=>c.claims[0].original_page_collated=true),/claim overstates archival inspection/);
 assert.throws(mod(c=>c.sources[2].access='HTML_FULL_TEXT_READ'),/blocked website marked read/);
 assert.throws(mod(c=>c.studies[0].parent_v313_study='MISSING'),/orphan study/);
 assert.throws(mod(c=>c.publication_gate.published=true),/publication HOLD/);
});
