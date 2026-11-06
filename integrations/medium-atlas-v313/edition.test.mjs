import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleV312} from '../medium-atlas-v312/overlay.mjs';
import {assembleV313} from './overlay.mjs';
const raw=p=>readFileSync(new URL('../../'+p,import.meta.url));
const parse=p=>JSON.parse(raw(p));
const m=parse('integrations/medium-atlas-v313/manifest.json');
const base=m.inputs.map(x=>parse(x.path)),audit=m.auditInputs.map(x=>parse(x.path));
const old=assembleV312(base,...audit,parse(m.addendumInput.path),parse(m.latinInput.path));
const p313=parse(m.editionInput.path);
const next=assembleV313(base,...audit,parse(m.addendumInput.path),parse(m.latinInput.path),p313);
test('exact input snapshots and catalog are Git-hash pinned',()=>{
 for(const i of [...m.inputs,...m.auditInputs,m.addendumInput,m.latinInput,m.editionInput]){
  const buf=raw(i.path);
  if(i.sha256)assert.equal(createHash('sha256').update(buf).digest('hex'),i.sha256,i.path);
  if(i.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+buf.length+'\0'),buf])).digest('hex'),i.gitBlobSha1,i.path);
 }
});
test('513 readers, 723 source records, 97 overview entries and V311-V312 supplements are unchanged',()=>{
 assert.deepEqual(next.delivery.readers,old.delivery.readers);
 assert.deepEqual(next.delivery.sources,old.delivery.sources);
 assert.deepEqual(next.delivery.source_verification,old.delivery.source_verification);
 assert.deepEqual(next.crosswalk,old.crosswalk);
 assert.deepEqual(next.delivery.primary_passage_addenda,old.delivery.primary_passage_addenda);
 assert.deepEqual(next.delivery.primary_passage_claims,old.delivery.primary_passage_claims);
 assert.deepEqual(next.delivery.latin_english_limited_concordance_v312,old.delivery.latin_english_limited_concordance_v312);
 assert.equal(next.delivery.publication_gate.published,false);
});
test('1564 Roman folio/quarto/Dillingen and Padua 1738 metadata are not falsely collated',()=>{
 const t=new Map(p313.sources.map(x=>[x.id,x]));
 assert.deepEqual(['TR-ROME-1564-F','TR-ROME-1564-Q','TR-DILLINGEN-1564'].map(x=>t.get(x).year),[1564,1564,1564]);
 assert.equal(t.get('TR-PADUA-1738').year,1738);
 assert.ok(p313.relations.some(x=>x.type==='SAME_IMPRINT_YEAR_DISTINCT_FORMATS_VARIANT_UNPROVEN'));
 assert.equal(p313.metrics.verified_textual_variants,0);
 assert.ok(p313.sources.every(x=>x.original_pages_collated===false));
});
test('IPO 1648 archival original, IPO 1650 print, two IPM German imprints remain separate',()=>{
 const t=new Map(p313.sources.map(x=>[x.id,x]));
 assert.equal(t.get('IPO-AK-1648').role,'ARCHIVAL_ORIGINAL_HOLDING_RECORD');
 assert.equal(t.get('IPO-LATIN-1650').year,1650);
 assert.deepEqual(['IPM-GERMAN-1648','IPM-GERMAN-1649'].map(id=>t.get(id).year),[1648,1649]);
 assert.ok(p313.relations.some(x=>x.type==='DIFFERENT_TREATIES_NOT_EDITION'));
 assert.equal(t.get('LWL-PRINT-CAUTION').role,'HISTORICAL_EDITORIAL_INDEX_ONLY');
 assert.equal(next.delivery.editorial_audit.v313_edition_archive.original_pages_collated,0);
});
test('two scoped readings, eight relations and nine bibliographic claim cards stay linked',()=>{
 assert.deepEqual([p313.studies.length,p313.relations.length,p313.provenance_claims.length],[2,8,9]);
 assert.equal(p313.studies.reduce((a,x)=>a+x.sections.length,0),6);
 assert.equal(p313.metrics.body_characters,1812);
 assert.equal(next.getEditionSourcesForStudy('V313-WESTPHALIA-PRINTS').length,7);
 assert.throws(()=>next.getEditionSourcesForStudy('UNLISTED'),/unknown V313 study/);
 const arr=next.getEditionSourcesForStudy('V313-TRENT-PRINTS');arr[0].bibliography='tampered';
 assert.notEqual(next.getEditionSourcesForStudy('V313-TRENT-PRINTS')[0].bibliography,'tampered');
});
test('false source age, claimed variants, fake archival collation, broken edges and public release fail',()=>{
 const v=(changes)=>{const r=structuredClone(p313);changes(r);return ()=>assembleV313(base,...audit,parse(m.addendumInput.path),parse(m.latinInput.path),r);};
 assert.throws(v(x=>x.sources.find(s=>s.id==='IPO-LATIN-1650').year=1648),/chronology drift/);
 assert.throws(v(x=>x.metrics.verified_textual_variants=1),/metrics out of scope/);
 assert.throws(v(x=>x.sources[0].original_pages_collated=true),/false page inspection/);
 assert.throws(v(x=>x.relations[0].to='UNKNOWN'),/false edition genealogy/);
 assert.throws(v(x=>x.publication_gate.published=true),/edition HOLD missing/);
});
