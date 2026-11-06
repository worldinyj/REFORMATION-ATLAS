import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const contract=JSON.parse(readFileSync(new URL('../../data/contracts/atlas_v319_ipm_print_privilege_dating.json',import.meta.url),'utf8'));
test('preserves prior V3.18 source contract hash and publication gates',()=>{
 const sha=execFileSync('git',['hash-object','data/contracts/atlas_v318_ipm1649_scan_page_evidence.json'],{encoding:'utf8'}).trim();
 assert.equal(sha,contract.parent.locked_prior_blob_sha);
 assert.equal(contract.version,'3.19');assert.equal(contract.depth,'MEDIUM');assert.equal(contract.status,'DRAFT');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{readers:513,sections:1539,original_sources:723,overviews:97,selected_claims:22,v318_original_scan_pages:3,v318_original_issues:4});
});
test('only two new pages, and they belong to 1649 IPM not 1648 IPM or IPO',()=>{
 assert.deepEqual(contract.sources.map(s=>s.scan_sequence),[5,6]);
 assert.deepEqual(contract.sources.map(s=>s.printed_page),[7,8]);
 for(const s of contract.sources){assert.equal(s.work,'IPM');assert.equal(s.printed_year,1649);assert.equal(s.kind,'DIRECT_PRINT_PAGE_SCAN_VISUALLY_INSPECTED');assert.ok(s.url.includes('/Seite:Westfaelischer_Friede_IPM_1649_0'));}
 assert.equal(contract.metrics.new_1649_scan_pages_visually_inspected,2);
 assert.equal(contract.metrics.cumulative_1649_ipm_scan_pages,5);
 assert.equal(contract.metrics.actual_1648_ipm_scan_pages,0);
 assert.equal(contract.metrics.actual_diplomatic_original_pages,0);
 assert.equal(contract.metrics.paired_1648_to_1649_print_paragraphs,0);
 assert.equal(contract.metrics.verified_textual_variants,0);
});
test('dated privilege never confused with treaty signature or edition year',()=>{
 assert.deepEqual(contract.chronology.map(x=>x.date),['1648-03-03','1648-10-24','1649']);
 assert.deepEqual(contract.chronology.map(x=>x.event),['PRINT_PRIVILEGE_DATE_AS_REPRODUCED','IPM_TREATY_SIGNATURE','PRINT_EDITION_YEAR']);
 assert.ok(contract.chronology[0].evidence.startsWith('IPM49-SCAN-006'));
});
test('medium readings, cards, and unresolved claims are evidence-limited',()=>{
 assert.equal(contract.readings.length,3);assert.equal(contract.readings.reduce((n,r)=>n+r.sections.length,0),9);
 assert.equal(contract.claims.length,9);assert.equal(new Set(contract.claims.map(c=>c.id)).size,9);
 assert.equal(contract.open_issues.length,4);
 assert.ok(contract.claims.every(c=>c.expert_approved===false && c.original_diplomatic_witness_collated===false));
 assert.ok(contract.open_issues.every(x=>x.status.startsWith('NOT_')));
});
