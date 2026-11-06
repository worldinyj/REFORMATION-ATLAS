import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const d=JSON.parse(readFileSync(new URL('../../data/contracts/atlas_v322_cross_document_date_age_gates.json',import.meta.url),'utf8'));
const ev=id=>d.event_taxonomy.find(x=>x.id===id);
const age=id=>d.age_rules.find(x=>x.id===id);
test('previous V321 evidence is bitwise frozen and V322 not published',()=>{
 assert.equal(execFileSync('git',['hash-object','data/contracts/atlas_v321_ipm_numeric_translation_quality.json'],{encoding:'utf8'}).trim(),d.parent.locked_prior_blob_sha);
 assert.equal(d.version,'3.22');assert.equal(d.depth,'MEDIUM');assert.equal(d.status,'DRAFT');
 assert.deepEqual(d.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(d.preserve,{readers:513,sections:1539,source_records:723,overview_records:97,selected_claims:22,prior_v321_discrepancies:4});
});
test('Trent seminary admission 12 is not ecclesiastical benefice 14',()=>{
 assert.equal(age('V322-A01').age_years,12);
 assert.equal(age('V322-A01').applies_to,'SEMINARY_ADMISSION');
 assert.equal(age('V322-A01').reform_chapter,18);
 assert.equal(age('V322-A02').age_years,14);
 assert.equal(age('V322-A02').applies_to,'HOLDING_ECCLESIASTICAL_BENEFICE');
 assert.equal(age('V322-A02').reform_chapter,6);
 assert.equal(age('V322-A01').session,23);
 assert.equal(age('V322-A02').session,23);
 assert.notEqual(age('V322-A01').applies_to,age('V322-A02').applies_to);
});
test('Trent sessions and papal confirmation are distinct',()=>{
 assert.deepEqual(['V322-E01','V322-E02','V322-E03','V322-E04','V322-E05'].map(id=>ev(id).date),['1545-12-13','1547-01-13','1563-07-15','1563-12-04','1564-01-26']);
 assert.notEqual(ev('V322-E04').type,ev('V322-E05').type);
});
test('Augsburg presentation, supervised print and 1540 revision cannot be same event',()=>{
 assert.equal(ev('V322-E06').date,'1530-06-25');
 assert.equal(ev('V322-E07').date,'1531-05');
 assert.equal(ev('V322-E08').date,'1540');
 assert.equal(new Set(['V322-E06','V322-E07','V322-E08'].map(id=>ev(id).type)).size,3);
});
test('Wesley formation, pamphlet publication, American reception separated',()=>{
 assert.deepEqual(['V322-E09','V322-E10','V322-E11'].map(id=>ev(id).date),['1738','1743','1785']);
 assert.equal(new Set(['V322-E09','V322-E10','V322-E11'].map(id=>ev(id).type)).size,3);
});
test('all claims grounded in sourced medium-only records',()=>{
 const ids=new Set(d.sources.map(x=>x.id));
 assert.equal(d.sources.length,9);assert.equal(d.event_taxonomy.length,11);assert.equal(d.age_rules.length,2);
 assert.equal(d.readings.length,4);assert.equal(d.readings.reduce((n,r)=>n+r.sections.length,0),12);
 assert.equal(d.cards.length,14);assert.equal(new Set(d.cards.map(x=>x.id)).size,14);
 assert.ok(d.cards.every(c=>ids.has(c.source_id)&&c.original_witness_collated===false&&c.expert_approved===false));
 assert.ok(d.event_taxonomy.every(e=>e.source_ids.every(id=>ids.has(id))));
 assert.ok(d.open_issues.every(x=>x.state.startsWith('NOT_')));
 assert.equal(d.metrics.direct_archival_print_pages,0);
 assert.equal(d.metrics.confirmed_original_witness_variants,0);
 assert.equal(d.metrics.original_reader_edits,0);
});
