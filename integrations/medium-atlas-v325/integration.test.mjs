import test from 'node:test';
import assert from 'node:assert/strict';
import {loadAudit,validateAudit,reviewOutputs} from '../../scripts/build_v325_evidence_priority_audit.mjs';
const clone=x=>structuredClone(x);
test('V3.24 evidence contract is immutable and all 12 V3.25 grades belong to known relations',()=>{
 const inputs=loadAudit();
 const result=validateAudit(inputs);
 assert.deepEqual(result,{relations:12,issues:6,high:3,medium:3});
 assert.equal(inputs.audit.publication_gate.published,false);
 assert.equal(inputs.audit.metrics.relations_assessed,12);
 assert.equal(inputs.audit.metrics.new_original_print_pages_visually_inspected,0);
});
test('editorial priority is deterministic and not a historical truth probability',()=>{
 const inputs=loadAudit(),a=inputs.audit;
 assert.equal(a.priority_queue.length,6);
 assert.equal(a.priority_queue[0].issue_id,'V324-ISS01');
 assert.equal(a.priority_queue[0].triage_score,12);
 assert.ok(a.priority_queue.every(x=>x.metric_disclaimer.includes('not scientific probability')));
 const forged=clone(inputs);forged.audit.priority_queue[0].triage_score=99;
 assert.throws(()=>validateAudit(forged),/Expected values to be strictly equal/);
 const partial=clone(inputs);partial.audit.priority_queue[0].priority='P2';
 assert.throws(()=>validateAudit(partial),/Expected values to be strictly equal/);
});
test('1784 Methodist adoption is not 1785 Philadelphia publication or isolated 1785 first approval',()=>{
 const inputs=loadAudit(),stages=inputs.audit.methodist_stage_records;
 const ev=id=>stages.find(x=>x.id===id);
 assert.equal(ev('V325-M03').date,'1784-12');
 assert.equal(ev('V325-M03').date_precision,'MONTH');
 assert.equal(ev('V325-M04').date,'1785');
 assert.equal(ev('V325-M04').date_precision,'YEAR');
 assert.equal(ev('V325-M05').public_copy_allowed,null);
 const wrong=clone(inputs);wrong.audit.methodist_stage_records.find(x=>x.id==='V325-M04').date='1784-12';
 assert.throws(()=>validateAudit(wrong),/Expected values to be strictly equal/);
 const wrong2=clone(inputs);wrong2.audit.methodist_stage_records.find(x=>x.id==='V325-M05').public_copy_allowed='approved as first adoption';
 assert.throws(()=>validateAudit(wrong2),/never publish unverified second approval/);
});
test('a historical relation source ID can never be silently changed',()=>{
 const inputs=loadAudit();
 const unknown=clone(inputs);unknown.audit.assessments[0].relation_id='V324-NOT-EXISTING';
 assert.throws(()=>validateAudit(unknown),/unknown historic relation/);
 const changed=clone(inputs);changed.audit.assessments[0].source_ids=['V325-UMC-GLOSSARY'];
 assert.throws(()=>validateAudit(changed),/historic source changed/);
 const approved=clone(inputs);approved.audit.assessments[0].app_publication_approved=true;
 assert.throws(()=>validateAudit(approved),/Expected values to be strictly equal/);
});
test('new sources remain metadata, edited accounts or library descriptions, not visually inspected originals',()=>{
 const inputs=loadAudit();
 assert.equal(inputs.audit.methodist_source_records.length,6);
 assert.ok(inputs.audit.methodist_source_records.every(x=>x.original_print_page_inspected===false));
 assert.ok(inputs.audit.methodist_source_records.filter(x=>x.id.startsWith('V325-UMC-')).length>=3);
 assert.equal(inputs.audit.metrics.physical_page_collations,0);
 assert.equal(inputs.audit.readings.length,2);
 assert.equal(inputs.audit.readings.flatMap(x=>x.sections).length,6);
});
test('all outputs are research-only and keep unknown 1785 approval off screen',()=>{
 const inputs=loadAudit(),verified=validateAudit(inputs),outs=reviewOutputs(inputs);
 assert.equal(verified.relations,12);
 assert.deepEqual(Object.keys(outs),[
  'v325_relation_evidence_matrix.json','v325_ordered_source_research_queue.json','v325_methodist_chronology_distinctions.json'
 ]);
 assert.deepEqual(Object.values(outs).map(o=>o.count),[12,6,5]);
 assert.ok(Object.values(outs).every(o=>o.publication_ready===false));
 assert.equal(outs['v325_methodist_chronology_distinctions.json'].public_display.approved_for_public_app,false);
 assert.equal(outs['v325_methodist_chronology_distinctions.json'].stages.find(x=>x.id==='V325-M05').public_copy_allowed,null);
});
