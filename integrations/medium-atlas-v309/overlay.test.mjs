import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {assembleV308} from '../medium-atlas-v308/assemble.mjs';
import {assembleV309} from './overlay.mjs';
const parse=p=>JSON.parse(readFileSync(new URL('../../'+p,import.meta.url)));
const m=parse('integrations/medium-atlas-v308/manifest.json');
const inputs=m.inputs.map(o=>parse(o.path)),audit=parse('data/contracts/atlas_v309_source_evidence_audit.json');
const old=assembleV308(...inputs),current=assembleV309(inputs,audit);
test('all 513 reader bodies, original selected claims and 97 links preserved',()=>{
 assert.deepEqual(current.delivery.readers,old.delivery.readers);
 assert.deepEqual(current.delivery.source_verification,old.delivery.source_verification);
 assert.deepEqual(current.delivery.reader_source_cards,old.delivery.reader_source_cards);
 assert.deepEqual(current.crosswalk,old.crosswalk);
});
test('only one of 723 source links changes and provenance is retained',()=>{
 assert.equal(current.delivery.sources.length,723);
 const diff=current.delivery.sources.filter((s,i)=>s.url!==old.delivery.sources[i].url);
 assert.equal(diff.length,1);assert.equal(diff[0].id,'V307-S08');
 assert.equal(diff[0].original_url,audit.link_corrections[0].original_url);
 assert.equal(diff[0].url,audit.link_corrections[0].replacement_url);
 assert.equal(diff[0].inspection_level,'PUBLIC_LANDING_PAGE_OR_SEARCH_EXCERPT');
 assert.equal(diff[0].link_correction.historical_claim_validation,'NOT_CHANGED');
 assert.equal(current.delivery.publication_gate.published,false);
});
test('scope warnings and 10 targeted source audit findings persist',()=>{
 assert.equal(audit.findings.length,10);
 assert.ok(audit.findings.some(f=>f.source_id==='V307-S23'&&f.status==='METADATA_CONFLICT'));
 assert.ok(audit.findings.some(f=>f.source_id==='V307-S01'&&f.status==='SECONDARY_DATE_VARIANT'));
 assert.ok(audit.findings.some(f=>f.source_id==='V307-S10'&&f.status==='CURRENT_ACCESS_RESTRICTED'));
});
test('unsupported URL or revoked publication HOLD cannot be silently applied',()=>{
 const altered=structuredClone(audit);altered.link_corrections[0].replacement_url='https://unknown.example/';
 assert.throws(()=>assembleV309(inputs,altered),/unreviewed corrected URL/);
 const withdrawn=structuredClone(audit);withdrawn.publication_gate.published=true;
 assert.throws(()=>assembleV309(inputs,withdrawn),/HOLD/);
 const badSource=structuredClone(inputs);badSource[3].sources.find(s=>s.id==='S08').url='https://not-original.example';
 assert.throws(()=>assembleV309(badSource,audit),/unexpected original source link/);
});
