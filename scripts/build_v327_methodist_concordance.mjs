import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PARENT='data/contracts/atlas_v326_methodist_1784_1785_discipline_witness_audit.json';
const SELF='data/contracts/atlas_v327_methodist_question_edition_concordance.json';
const load=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));

export function loadInputs(){return {parent:load(PARENT),contract:load(SELF)}}
export function validateConcordance({parent,contract}){
 const sha=execFileSync('git',['hash-object',PARENT],{cwd:ROOT,encoding:'utf8'}).trim();
 assert.equal(sha,contract.parent.locked_contract_blob_sha,'V3.26 parent must remain unchanged');
 assert.equal(parent.version,'3.26');
 assert.equal(contract.version,'3.27');
 assert.equal(contract.status,'DRAFT');
 assert.equal(contract.depth,'MEDIUM');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{readers:513,sections:1539,sources:723,overviews:97,curated_events:26,typed_relations:12});
 assert.equal(contract.source_records.length,13);
 assert.equal(contract.probation_concordance.length,6);
 assert.equal(contract.question_fragments.length,11);
 assert.equal(contract.readings.length,3);
 assert.equal(contract.readings.reduce((sum,x)=>sum+x.sections.length,0),9);
 assert.equal(contract.open_issues.length,8);
 const sourceIds=new Set(contract.source_records.map(x=>x.id));
 assert.equal(sourceIds.size,13);
 for(const item of [...contract.probation_concordance,...contract.question_fragments]){
  assert.ok(item.source_ids.length>0);
  assert.ok(item.source_ids.every(x=>sourceIds.has(x)),'unknown evidence source '+item.id);
 }
 const row=(year,jurisdiction)=>contract.probation_concordance.find(x=>x.year===year&&x.jurisdiction===jurisdiction);
 assert.equal(row(1770,'BRITISH_WESLEYAN').trial_months,3);
 assert.equal(row(1770,'BRITISH_WESLEYAN').question,'Q18');
 assert.equal(row(1770,'BRITISH_WESLEYAN').body_original_print_page_visually_inspected,true);
 assert.equal(row(1785,'AMERICAN_MEC').trial_months,2);
 assert.equal(row(1785,'AMERICAN_MEC').question,'Q16');
 assert.equal(row(1785,'AMERICAN_MEC').body_original_print_page_visually_inspected,false);
 assert.equal(row(1785,'AMERICAN_MEC').basis,'LATER_STUDY_INDEX_NOT_DIRECT_1785_PRINT');
 assert.equal(row(1787,'AMERICAN_MEC').trial_months,2);
 assert.equal(row(1787,'AMERICAN_MEC').basis,'LATER_EDITION_STUDY_PROVISIONAL');
 assert.equal(row(1789,'AMERICAN_MEC').trial_months,6);
 assert.equal(row(1789,'AMERICAN_MEC').basis,'LATER_HISTORICAL_INDEX_PROVISIONAL');
 assert.equal(row(1789,'BRITISH_WESLEYAN').trial_months,2);
 assert.equal(row(1798,'AMERICAN_MEC').trial_months,6);
 assert.equal(row(1798,'AMERICAN_MEC').basis,'DIGITIZED_PDF_TEXT_NO_SCREENSHOT');
 const visual=contract.probation_concordance.filter(x=>x.body_original_print_page_visually_inspected);
 assert.deepEqual(visual.map(x=>x.year),[1770]);
 assert.equal(contract.publication_labels.original_1770_print_pages_visually_verified,1);
 assert.equal(contract.publication_labels.original_1785_body_images_read,0);
 assert.equal(contract.publication_labels.original_1798_print_pages_visually_verified,0);
 assert.equal(contract.publication_labels.first_edition_1785_all_81_question_collations,0);
 assert.equal(contract.publication_labels.public_app_approved,false);
 assert.equal(contract.metrics.original_corpus_changed??0,0);
 assert.equal(contract.metrics.unchanged_original_reader_count,513);
 const fragments=new Map(contract.question_fragments.map(x=>[x.question,x]));
 assert.equal(fragments.size,11);
 assert.equal(fragments.get('1785-Q03').topic,'NEW_EPISCOPAL_CHURCH_ORGANIZATION');
 assert.equal(fragments.get('1785-Q11').topic,'ATTENDANCE_VISITOR_TICKETS');
 assert.equal(fragments.get('1785-Q16').topic,'MEMBERSHIP_TICKET_TWO_MONTHS');
 assert.equal(fragments.get('1785-Q16').level,'SCHOLAR_INDEX_ONLY');
 assert.equal(fragments.get('1785-Q17').level,'SCHOLAR_INDEX_ONLY');
 assert.equal(fragments.get('1798-Q03').level,'PDF_TEXT_ONLY');
 assert.ok(contract.blocked_inferences.some(x=>x.includes('No proof Americans first introduced')));
 assert.ok(contract.blocked_inferences.some(x=>x.includes('No direct photographic collation')));
 assert.ok(contract.open_issues.some(x=>x.id==='V327-ISS-1785_Q16_Q17_P9'&&x.status==='OPEN'));
 assert.ok(contract.open_issues.some(x=>x.id==='V327-ISS-GENERAL_RULES_FULL_APPENDIX'&&x.status==='OPEN'));
 assert.ok(contract.source_records.some(x=>x.id==='V327-S-1789-BRITAIN'&&x.access==='UNCOLLATED_TRANSCRIPTION'));
 return {sources:sourceIds.size,editions:6,questions:11,readings:3,sections:9,issues:8};
}
export function deriveReviewOutputs({contract}){
 const flag={version:'3.27',research_only:true,published:false,webapp_integrated:false};
 return {
  'v327_1770_1798_probation_concordance.json':{...flag,count:contract.probation_concordance.length,editions:contract.probation_concordance,source_records:contract.source_records},
  'v327_1785_question_excerpt_index.json':{...flag,count:contract.question_fragments.length,questions:contract.question_fragments},
  'v327_remaining_witness_verification.json':{...flag,count:contract.open_issues.length,gaps:contract.open_issues,blocked_inferences:contract.blocked_inferences}
 };
}
export function writeReview(){
 const input=loadInputs();validateConcordance(input);
 const outputs=deriveReviewOutputs(input);
 const dir=path.join(ROOT,'out','atlas-v327');
 mkdirSync(dir,{recursive:true});
 for(const [filename,obj] of Object.entries(outputs))writeFileSync(path.join(dir,filename),JSON.stringify(obj,null,2)+'\n');
 return outputs;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const results=writeReview();
 for(const [filename,record] of Object.entries(results))console.log(filename+': '+record.count+' RESEARCH_ONLY');
}
