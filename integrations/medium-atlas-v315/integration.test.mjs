import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleV314} from '../medium-atlas-v314/overlay.mjs';
import {assembleV315} from './overlay.mjs';
const bytes=p=>readFileSync(new URL('../../'+p,import.meta.url));
const load=p=>JSON.parse(bytes(p));
const m=load('integrations/medium-atlas-v315/manifest.json');
const base=m.inputs.map(x=>load(x.path)),audits=m.auditInputs.map(x=>load(x.path));
const [a,b,c,d,e]=[m.addendumInput,m.latinInput,m.editionInput,m.authInput,m.wordingInput].map(x=>load(x.path));
const prev=assembleV314(base,...audits,a,b,c,d),next=assembleV315(base,...audits,a,b,c,d,e);
const change=fn=>{const x=structuredClone(e);fn(x);return ()=>assembleV315(base,...audits,a,b,c,d,x);};
test('original SHA pinned sources, audits, and research extension inputs',()=>{
 for(const s of [...m.inputs,...m.auditInputs,m.addendumInput,m.latinInput,m.editionInput,m.authInput,m.wordingInput]){
  const raw=bytes(s.path);
  if(s.sha256)assert.equal(createHash('sha256').update(raw).digest('hex'),s.sha256,s.path);
  if(s.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+raw.length+'\0'),raw])).digest('hex'),s.gitBlobSha1,s.path);
 }
});
test('513 originals, 723 sources, 97 overviews and earlier research are untouched',()=>{
 for(const k of ['readers','sources','source_verification','primary_passage_addenda','primary_passage_claims',
  'latin_english_limited_concordance_v312','edition_archive_provenance_v313','source_attestation_v314'])
  assert.deepEqual(next.delivery[k],prev.delivery[k],k);
 assert.deepEqual(next.crosswalk,prev.crosswalk);
 assert.equal(next.delivery.publication_gate.published,false);
 assert.equal(next.delivery.editorial_audit.v315_wording.original_pages_inspected,0);
});
test('museum Latin forms and modern historian sources do not change evidence type',()=>{
 assert.deepEqual(e.claim_cards.filter(x=>x.latin_fragment).map(x=>x.latin_fragment),
  ['cum originalibus contulimus','cum eis concordare reperimus','manu propria subscripsimus','Ego Angelus Massarellus']);
 assert.ok(e.claim_cards.filter(x=>x.id.startsWith('H')).every(x=>x.source_layer==='MODERN_HISTORIAN_ACCOUNT'&&x.latin_fragment===null));
 assert.equal(e.source_records.find(x=>x.id==='ARNDT-1648').access,'FULL_HTML_PRINT_VIEW_READ');
 assert.equal(e.inspection.original_treaty_pages,0);
});
test('two medium depth reading notes, eight claims and defensive copies for parent navigation',()=>{
 assert.equal(e.reading_notes.length,2);
 assert.equal(e.reading_notes.reduce((n,x)=>n+x.sections.length,0),6);
 assert.equal(e.metrics.body_characters,1590);
 assert.equal(e.claim_cards.length,8);
 const v=next.getForV314('V314-MASSARELLI-AUTHENTICATION');
 assert.equal(v.length,1);assert.equal(v[0].claims.length,4);
 const w=next.getForV314('V314-PRINT-AUTHORITY-WESTPHALIA');
 assert.equal(w.length,1);assert.equal(w[0].claims.length,4);
 v[0].sections[0].body='tampered';
 assert.notEqual(next.getForV314('V314-MASSARELLI-AUTHENTICATION')[0].sections[0].body,'tampered');
 assert.throws(()=>next.getForV314('NOPE'),/unknown V314 parent/);
});
test('fabricated collation, unsupported Latin, broken source and released status are rejected',()=>{
 assert.throws(change(x=>x.inspection.original_museum_pages=1),/false original collation/);
 assert.throws(change(x=>x.claim_cards[0].latin_fragment='invention'),/unverified Latin/);
 assert.throws(change(x=>x.claim_cards[5].source_layer='MUSEUM_TRANSCRIBED_LATIN'),/secondary evidence promoted/);
 assert.throws(change(x=>x.claim_cards[0].source_id='UNKNOWN'),/invalid claim/);
 assert.throws(change(x=>x.publication_gate.published=true),/publication HOLD/);
});
