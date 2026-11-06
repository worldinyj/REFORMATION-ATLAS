import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleV310} from '../medium-atlas-v310/overlay.mjs';
import {assembleV311} from './overlay.mjs';
import {createMediumAtlas} from '../medium-atlas-v310/adapter.mjs';
import {createOverviewReadingBridge} from '../medium-atlas-v310/bridge.mjs';
const raw=p=>readFileSync(new URL('../../'+p,import.meta.url));
const parse=p=>JSON.parse(raw(p));
const manifest=parse('integrations/medium-atlas-v311/manifest.json');
const base=manifest.inputs.map(r=>parse(r.path));
const oldLink=parse(manifest.auditInputs[0].path);
const oldQuality=parse(manifest.auditInputs[1].path);
const additions=parse(manifest.addendumInput.path);
const prev=assembleV310(base,oldLink,oldQuality),next=assembleV311(base,oldLink,oldQuality,additions);
test('frozen four sources, two prior audits, and the annex have exact bytes',()=>{
 for(const item of [...manifest.inputs,...manifest.auditInputs,manifest.addendumInput]){
  const b=raw(item.path);
  if(item.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),item.sha256,item.path);
  if(item.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),item.gitBlobSha1,item.path);
 }
});
test('513 original readers and 723 original sources remain unchanged',()=>{
 assert.deepEqual(next.delivery.readers,prev.delivery.readers);
 assert.deepEqual(next.delivery.sources,prev.delivery.sources);
 assert.deepEqual(next.delivery.source_verification,prev.delivery.source_verification);
 assert.deepEqual(next.delivery.reader_source_cards,prev.delivery.reader_source_cards);
 assert.deepEqual(next.crosswalk,prev.crosswalk);
 const old=structuredClone(next.delivery);old.version='3.10';
 const atlas=createMediumAtlas(old),bridge=createOverviewReadingBridge(next.crosswalk,atlas);
 assert.equal(atlas.counts.readers,513);assert.equal(atlas.counts.sources,723);
 assert.deepEqual(bridge.coverage,{total:97,direct:78,partial:19,background:0,missing:0});
});
test('four source-critical studies contain twelve new standalone sections',()=>{
 assert.deepEqual([additions.addenda.length,additions.claim_cards.length,additions.source_records.length],[4,12,10]);
 assert.equal(additions.addenda.reduce((sum,a)=>sum+a.sections.length,0),12);
 const chars=additions.addenda.reduce((sum,a)=>sum+a.sections.reduce((n,s)=>n+s.body.length,0),0);
 assert.equal(chars,4435);
 assert.equal(next.delivery.primary_passage_addenda.length,4);
 assert.equal(next.delivery.editorial_audit.v311_source_critical.original_language_collated,false);
 assert.equal(next.delivery.editorial_audit.v311_source_critical.expert_approved,false);
});
test('every dossier has a claim-to-passage locator with no false approvals',()=>{
 const claims=next.delivery.primary_passage_claims;
 assert.equal(new Set(claims.map(c=>c.id)).size,12);
 for(const c of claims){
  const annex=additions.addenda.find(a=>a.id===c.addendum_id);
  assert.ok(annex&&annex.sections[c.section_index]&&annex.source_ids.includes(c.source_id));
  assert.equal(c.original_witness_collated,false);
  assert.equal(c.historian_approved,false);
  assert.ok(c.locator.length>=8);
 }
 const laterVote=claims.find(c=>c.id==='WCC-03');
 assert.equal(laterVote.evidence_level,'RETROSPECTIVE_SOURCE_SEEN_NOT_VOTE_ORIGINAL');
 assert.equal(laterVote.source_id,'WCC-2002');
 const catalogue=additions.source_records.find(s=>s.id==='WCC-1948-CAT');
 assert.equal(catalogue.layer,'PRIMARY_REPORT_CATALOGUE_METADATA_ONLY');
 assert.match(catalogue.not_done,/읽지 않음/);
});
test('reader to addenda navigation is explicit and read-only',()=>{
 const tr=next.getAddendaForReader('MEDIUM-TRENT');
 assert.equal(tr.length,1);assert.equal(tr[0].id,'ATLAS-V311-TRENT');assert.equal(tr[0].claims.length,3);
 const wesley=next.getAddendaForReader('DOCUMENT-METHODIST_GENERAL_RULES1743');
 assert.equal(wesley[0].id,'ATLAS-V311-WESLEY');
 const wcc=next.getAddendaForReader('EVENT-WCC_FOUNDING1948');
 assert.equal(wcc[0].id,'ATLAS-V311-WCC');
 assert.deepEqual(next.getAddendaForReader('PERSON-YI_BYEOK'),[]);
 assert.throws(()=>next.getAddendaForReader('UNLISTED'),/unknown reader/);
 tr[0].sections[0].body='tampered';
 assert.notEqual(next.getAddendaForReader('MEDIUM-TRENT')[0].sections[0].body,'tampered');
});
test('bad claim references, invented collation and revoked HOLD are rejected',()=>{
 const bad=structuredClone(additions);
 bad.claim_cards[0].source_id='UNKNOWN-SOURCE';
 assert.throws(()=>assembleV311(base,oldLink,oldQuality,bad),/claim source or locator mismatch/);
 const approved=structuredClone(additions);
 approved.claim_cards[0].original_witness_collated=true;
 assert.throws(()=>assembleV311(base,oldLink,oldQuality,approved),/invalid claim approval/);
 const published=structuredClone(additions);
 published.publishing_gate.published=true;
 assert.throws(()=>assembleV311(base,oldLink,oldQuality,published),/publication HOLD/);
 const missing=structuredClone(additions);
 missing.addenda.pop();
 assert.throws(()=>assembleV311(base,oldLink,oldQuality,missing),/incomplete addenda/);
});
