import test from 'node:test';
import assert from 'node:assert/strict';
import {loadInputs,validateRelationOverlay,createReviewOutputs} from '../../scripts/build_v324_typed_relations.mjs';
const clone=structuredClone;
test('upstream V3.23 contracts frozen and 12 evidence-typed relations verified',()=>{
 const d=loadInputs();
 const a=validateRelationOverlay(d);
 assert.equal(a.resolved.length,12);
 assert.equal(new Set(a.resolved.map(x=>x.id)).size,12);
 assert.equal(d.graph.events.length,26);
 assert.equal(d.readers.catalogue.length,513);
 assert.equal(d.contract.metrics.new_research_readings,4);
 assert.equal(d.contract.metrics.new_sections,12);
 assert.equal(d.contract.metrics.new_external_source_records,14);
 assert.equal(d.contract.publication_gate.published,false);
});
test('relation directional semantics for confutation, apology and textual edition',()=>{
 const a=validateRelationOverlay(loadInputs());
 const find=id=>a.resolved.find(x=>x.id===id);
 assert.equal(find('V324-R02').type,'FORMAL_CONFUTATION_OF');
 assert.equal(find('V324-R02').from.id,'V324-DOC-CONFUTATIO1530');
 assert.equal(find('V324-R02').to.id,'V323-W01');
 assert.equal(find('V324-R03').type,'APOLOGETIC_REBUTTAL_OF');
 assert.equal(find('V324-R03').from.id,'DOCUMENT-AUGSBURG_APOLOGY');
 assert.equal(find('V324-R03').to.id,'V324-DOC-CONFUTATIO1530');
 assert.equal(find('V324-R04').type,'DEFENSE_OF_CONFESSIONAL_DOCUMENT');
 assert.equal(find('V324-R05').type,'AUTHORIAL_EDITION_REVISION');
 assert.equal(find('V324-R06').type,'AUTHORIAL_EDITION_REVISION');
 assert.equal(find('V324-R07').type,'REPORTED_STRUCTURAL_INFLUENCE');
 assert.equal(find('V324-R08').type,'INSTITUTIONAL_FOLLOW_UP_PUBLICATION');
 assert.equal(find('V324-R11').type,'TREATY_RATIFICATION_PROCEDURE');
});
test('fake reader/document/witness nodes must be rejected',()=>{
 const d=loadInputs();
 const broken=clone(d);
 broken.contract.typed_relations[0].to.id='PERSON-FAKE-HUS';
 assert.throws(()=>validateRelationOverlay(broken),/dangling to ref/);
 const broken2=clone(d);
 broken2.contract.typed_relations[4].to.id='V323-W08';
 assert.throws(()=>validateRelationOverlay(broken2),/Expected values to be strictly deep-equal/);
});
test('no temporal priority can silently become historical causality or new original witness',()=>{
 const d=loadInputs(),x=clone(d);
 x.contract.typed_relations[0].causation_inferred_from_time_only=true;
 assert.throws(()=>validateRelationOverlay(x),/Expected values to be strictly equal/);
 const y=clone(d);y.contract.typed_relations[0].type='AUTOMATIC_CAUSALITY';
 assert.throws(()=>validateRelationOverlay(y),/unknown relation type/);
 const z=clone(d);z.contract.typed_relations[5].original_witness_pair_collated=true;
 assert.throws(()=>validateRelationOverlay(z),/Expected values to be strictly equal/);
});
test('1784 1785 source ambiguity cannot be quietly replaced by first adoption claim',()=>{
 const d=loadInputs();
 const issue=d.contract.open_issues.find(x=>x.id==='V324-ISS01');
 assert.match(issue.finding,/1784/);assert.match(issue.finding,/1785/);
 const modified=clone(d);modified.contract.open_issues.find(x=>x.id==='V324-ISS01').sources=['SRC-UMC-GLOSSARY'];
 assert.throws(()=>validateRelationOverlay(modified),/The expression evaluated to a falsy value/);
 const overreach=clone(d);overreach.contract.typed_relations[9].to.id='V323-E26';
 assert.throws(()=>validateRelationOverlay(overreach),/Expected values to be strictly deep-equal|1785 must remain context-only/);
});
test('generated view is review only and never a production index',()=>{
 const d=loadInputs(),validated=validateRelationOverlay(d);
 const outputs=createReviewOutputs(d,validated);
 assert.deepEqual(Object.keys(outputs),[
  'v324_typed_relation_overlay.json','v324_reader_relation_lookup.json','v324_open_source_conflicts.json'
 ]);
 assert.equal(outputs['v324_typed_relation_overlay.json'].count,12);
 assert.equal(outputs['v324_open_source_conflicts.json'].count,6);
 assert.ok(outputs['v324_reader_relation_lookup.json'].count>=5);
 assert.ok(Object.values(outputs).every(x=>x.publication_ready===false&&x.research_only===true&&x.never_infer_causality_from_chronology===true));
 assert.ok(outputs['v324_typed_relation_overlay.json'].edges.every(x=>!x.is_publication_approved&&!x.direct_original_witness_pair));
});
