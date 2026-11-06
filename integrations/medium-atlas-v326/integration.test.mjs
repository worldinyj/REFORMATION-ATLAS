import test from 'node:test';
import assert from 'node:assert/strict';
import {loadResearch,validateWitnessAudit,draftOutputs} from '../../scripts/build_v326_methodist_witness_audit.mjs';
const copy=x=>structuredClone(x);
test('V3.25 immutable parent and V3.26 source-bound evidence audit',()=>{
 const data=loadResearch();const v=validateWitnessAudit(data);
 assert.deepEqual(v,{records:14,stages:5,cards:12,readings:3,sections:9});
 assert.equal(data.contract.publication_gate.published,false);
 assert.equal(data.contract.metrics.actual_1785_original_pages_collated,0);
});
test('opening 24 December and printed-title 27 December cannot be silently conflated',()=>{
 const data=loadResearch(),acts=data.contract.dated_acts;
 const a=id=>acts.find(x=>x.id===id);
 assert.equal(a('M326-E01').date,'1784-12-24');
 assert.equal(a('M326-E02').date,'1784-12-27');
 const broken=copy(data);
 broken.contract.dated_acts.find(x=>x.id==='M326-E02').date='1784-12-24';
 assert.throws(()=>validateWitnessAudit(broken),/Expected values to be strictly equal/);
 const broken2=copy(data);
 broken2.contract.dated_acts.find(x=>x.id==='M326-E01').type='DATE_ON_1785_PRINTED_BOOK_TITLE';
 assert.throws(()=>validateWitnessAudit(broken2),/Expected values to be strictly equal/);
});
test('imprint 1785 cannot become 1784 title-event year',()=>{
 const data=loadResearch(),bad=copy(data);
 bad.contract.dated_acts.find(x=>x.id==='M326-E04').date='1784';
 assert.throws(()=>validateWitnessAudit(bad),/Expected values to be strictly equal/);
 const b2=copy(data);
 b2.contract.dated_acts.find(x=>x.id==='M326-E04').precision='DAY';
 assert.throws(()=>validateWitnessAudit(b2),/The expression evaluated to a falsy value/);
});
test('cannot convert 1898 scanned historian source to a 1785 original page inspected',()=>{
 const x=loadResearch();
 const falselyVerified=copy(x);
 falselyVerified.contract.observed_source_levels.contemporary_1785_full_text_pages_visually_inspected=1;
 assert.throws(()=>validateWitnessAudit(falselyVerified),/Expected values to be strictly equal/);
 const falselyClaimed=copy(x);
 falselyClaimed.contract.source_records.find(s=>s.id==='M326-07').is_1785_original=true;
 assert.throws(()=>validateWitnessAudit(falselyClaimed),/The expression evaluated to a falsy value/);
});
test('later 1785 approval wording must stay unresolved and cannot be silently published',()=>{
 const data=loadResearch();
 assert.ok(data.contract.open_issues.some(x=>x.risk==='1785_GENERAL_RULES_APPROVAL'&&x.status==='OPEN'));
 const b=copy(data);
 b.contract.open_issues.find(x=>x.risk==='1785_GENERAL_RULES_APPROVAL').status='RESOLVED';
 assert.throws(()=>validateWitnessAudit(b),/The expression evaluated to a falsy value/);
 const c=copy(data);
 c.contract.suggested_reader_copy.public_release_allowed=true;
 assert.throws(()=>validateWitnessAudit(c),/Expected values to be strictly equal/);
});
test('provenance links are known and no missing claims, safe draft-only exports',()=>{
 const data=loadResearch(),check=validateWitnessAudit(data);
 const outputs=draftOutputs(data);
 assert.equal(check.cards,12);
 assert.deepEqual(Object.keys(outputs),[
 'v326_methodist_chronology_evidence.json',
 'v326_methodist_open_questions.json',
 'v326_methodist_claim_review_cards.json'
 ]);
 assert.deepEqual(Object.values(outputs).map(x=>x.count),[5,5,12]);
 assert.ok(Object.values(outputs).every(x=>x.publication_ready===false&&x.draft===true&&x.full_1785_original_seen===false));
});
