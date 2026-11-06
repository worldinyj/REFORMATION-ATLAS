import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
const d = JSON.parse(readFileSync(new URL('../../data/contracts/atlas_v321_ipm_numeric_translation_quality.json', import.meta.url), 'utf8'));
const difference = id => d.discrepancies.find(x => x.id === id);
test('V3.20 input immutable and publication gate closed', () => {
 const sha = execFileSync('git',['hash-object','data/contracts/atlas_v320_ipm1648_witness_provenance.json'],{encoding:'utf8'}).trim();
 assert.equal(sha,d.parent.locked_contract_blob_sha);
 assert.equal(d.status,'DRAFT'); assert.equal(d.depth,'MEDIUM');
 assert.deepEqual(d.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(d.preserve,{readers:513,sections:1539,sources:723,overviews:97,selected_claims:22,prior_verified_1649_ipm_scan_pages:5});
});
test('OCR and translations cannot be reclassified as verified physical variants',()=>{
 assert.equal(d.metrics.new_physical_scan_pages,0);
 assert.equal(d.metrics.verified_1648_ipm_pages,0);
 assert.equal(d.metrics.paired_1648_1649_print_passages,0);
 assert.equal(d.metrics.confirmed_print_variants,0);
 assert.equal(d.metrics.ocr_1648_extracts,1);
 assert.equal(d.discrepancies.length,4);
 assert.ok(d.discrepancies.every(x=>x.printed_variant_confirmed===false&&x.archival_page_collated===false));
 assert.equal(difference('V321-D01').status,'SUSPECTED_OCR_ERROR_NOT_PRINT_VARIANT');
});
test('four numeric mismatches exact and public corrected values internally consistent',()=>{
 assert.equal(difference('V321-D01').low_trust_text,'600200');
 assert.equal(difference('V321-D01').cross_checked_value,'600000');
 assert.equal(difference('V321-D02').low_trust_text,'eight months');
 assert.equal(difference('V321-D02').cross_checked_value,'nine months');
 assert.equal(difference('V321-D03').low_trust_text,'40000');
 assert.equal(difference('V321-D03').cross_checked_value,'400000');
 assert.equal(difference('V321-D04').low_trust_text,'10000');
 assert.equal(difference('V321-D04').cross_checked_value,'100000');
 assert.equal(4*100000,400000);
});
test('material sources and small research articles validated',()=>{
 const known = new Set(d.sources.map(s=>s.id));
 assert.equal(d.sources.length,7);
 assert.equal(d.sources.find(s=>s.id==='IPO-CONTEXT').work,'IPO_OTHER_TREATY');
 assert.equal(d.sources.find(s=>s.id==='ZURICH-RI240-OCR').evidence,'OCR_UNVERIFIED');
 assert.ok(d.discrepancies.every(x=>x.source_ids.every(id=>known.has(id))));
 assert.equal(d.readings.length,3);
 assert.equal(d.readings.reduce((n,r)=>n+r.sections.length,0),9);
 assert.equal(d.cards.length,10);
 assert.ok(d.cards.every(c=>known.has(c.source_id)&&c.confirmed_print_variant===false&&c.expert_approved===false));
});
