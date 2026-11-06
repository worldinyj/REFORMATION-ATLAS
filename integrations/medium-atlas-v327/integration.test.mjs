import test from 'node:test';
import assert from 'node:assert/strict';
import {loadInputs,validateConcordance,deriveReviewOutputs} from '../../scripts/build_v327_methodist_concordance.mjs';
const clone=x=>structuredClone(x);
test('V3.26 parent locked; all 13 sources, 6 edition records, 11 questions and 9 sections pass',()=>{
 const data=loadInputs(),check=validateConcordance(data);
 assert.deepEqual(check,{sources:13,editions:6,questions:11,readings:3,sections:9,issues:8});
 assert.equal(data.contract.publication_gate.published,false);
 assert.equal(data.contract.publication_labels.first_edition_1785_all_81_question_collations,0);
});
test('British 1770 three-month original scan cannot be silently replaced with American 1785 two months',()=>{
 const d=loadInputs(),r=d.contract.probation_concordance;
 assert.equal(r.find(x=>x.year===1770).trial_months,3);
 assert.equal(r.find(x=>x.year===1785).trial_months,2);
 const fake=clone(d);fake.contract.probation_concordance.find(x=>x.year===1770).trial_months=2;
 assert.throws(()=>validateConcordance(fake),/Expected values to be strictly equal/);
});
test('1789 British and 1789 American edition years are separate jurisdiction-specific records',()=>{
 const data=loadInputs();validateConcordance(data);
 const a=data.contract.probation_concordance.filter(x=>x.year===1789);
 assert.equal(a.length,2);
 assert.equal(new Set(a.map(x=>x.jurisdiction)).size,2);
 assert.equal(a.find(x=>x.jurisdiction==='BRITISH_WESLEYAN').trial_months,2);
 assert.equal(a.find(x=>x.jurisdiction==='AMERICAN_MEC').trial_months,6);
 const fake=clone(data);fake.contract.probation_concordance.find(x=>x.year===1789&&x.jurisdiction==='BRITISH_WESLEYAN').trial_months=6;
 assert.throws(()=>validateConcordance(fake),/Expected values to be strictly equal/);
});
test('1785 Q16/17 cannot be upgraded to direct print page or complete 81-question collation',()=>{
 const d=loadInputs();
 const fake=clone(d);fake.contract.probation_concordance.find(x=>x.year===1785).body_original_print_page_visually_inspected=true;
 assert.throws(()=>validateConcordance(fake),/Expected values to be strictly equal|Expected values to be strictly deep-equal/);
 const second=clone(d);second.contract.publication_labels.first_edition_1785_all_81_question_collations=81;
 assert.throws(()=>validateConcordance(second),/Expected values to be strictly equal/);
 const third=clone(d);third.contract.question_fragments.find(x=>x.question==='1785-Q16').level='DIRECT_PRINT_SCAN';
 assert.throws(()=>validateConcordance(third),/Expected values to be strictly equal/);
});
test('1798 six-month rule remains PDF text only until the original scan screenshot passes',()=>{
 const d=loadInputs();
 assert.equal(d.contract.probation_concordance.find(x=>x.year===1798).basis,'DIGITIZED_PDF_TEXT_NO_SCREENSHOT');
 const falseView=clone(d);falseView.contract.publication_labels.original_1798_print_pages_visually_verified=1;
 assert.throws(()=>validateConcordance(falseView),/Expected values to be strictly equal/);
});
test('member ticket / visitors tickets are different question types and rules appendix is unresolved',()=>{
 const d=loadInputs();validateConcordance(d);
 const Q=d.contract.question_fragments;
 assert.equal(Q.find(x=>x.question==='1785-Q11').topic,'ATTENDANCE_VISITOR_TICKETS');
 assert.equal(Q.find(x=>x.question==='1785-Q16').topic,'MEMBERSHIP_TICKET_TWO_MONTHS');
 assert.ok(d.contract.open_issues.some(x=>x.id==='V327-ISS-GENERAL_RULES_FULL_APPENDIX'));
});
test('build only three review-only datasets without webapp publication',()=>{
 const d=loadInputs();validateConcordance(d);const out=deriveReviewOutputs(d);
 assert.deepEqual(Object.keys(out),[
  'v327_1770_1798_probation_concordance.json',
  'v327_1785_question_excerpt_index.json',
  'v327_remaining_witness_verification.json'
 ]);
 assert.deepEqual(Object.values(out).map(x=>x.count),[6,11,8]);
 assert.ok(Object.values(out).every(x=>x.research_only===true&&x.published===false&&x.webapp_integrated===false));
});
