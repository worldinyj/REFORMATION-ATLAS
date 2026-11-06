import assert from 'node:assert/strict';
import {readFileSync, mkdirSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PARENT='data/contracts/atlas_v325_evidence_strength_priority_audit.json';
const TARGET='data/contracts/atlas_v326_methodist_1784_1785_discipline_witness_audit.json';
const read=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
export function loadResearch(){return {parent:read(PARENT),contract:read(TARGET)}}
export function validateWitnessAudit({parent,contract}) {
 const currentBlob=execFileSync('git',['hash-object',PARENT],{cwd:ROOT,encoding:'utf8'}).trim();
 assert.equal(currentBlob,contract.parent.locked_prior_contract_blob_sha,'V3.25 contract must be unchanged');
 assert.equal(contract.version,'3.26');assert.equal(contract.status,'DRAFT');assert.equal(contract.depth,'MEDIUM');
 assert.equal(contract.focus_issue_id,'V324-ISS01');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{readers:513,reader_sections:1539,sources:723,overviews:97,selected_claims:22,curated_events:26,relations:12,previous_priority_issues:6});
 assert.equal(parent.version,'3.25');
 assert.ok(parent.priority_queue.some(i=>i.issue_id===contract.focus_issue_id&&i.priority==='P0'));
 assert.equal(contract.source_records.length,14);
 const validSources=new Set(contract.source_records.map(s=>s.id));
 assert.equal(validSources.size,14);
 assert.ok(contract.source_records.every(s=>s.is_1785_original===false));
 assert.equal(contract.dated_acts.length,5);
 assert.equal(contract.claim_cards.length,12);
 assert.equal(contract.readings.length,3);
 assert.equal(contract.readings.reduce((a,r)=>a+r.sections.length,0),9);
 assert.equal(contract.open_issues.length,5);
 const event=id=>contract.dated_acts.find(e=>e.id===id);
 assert.equal(event('M326-E01').date,'1784-12-24');
 assert.equal(event('M326-E01').type,'CONFERENCE_OPENING_HISTORIC_RECONSTRUCTION');
 assert.equal(event('M326-E02').date,'1784-12-27');
 assert.equal(event('M326-E02').type,'DATE_ON_1785_PRINTED_BOOK_TITLE');
 assert.equal(event('M326-E03').date,'1784-12');
 assert.equal(event('M326-E03').type,'DECISION_ORGANIZATION_GENERAL_RULES_ADOPTION_LATER_REPORT');
 assert.equal(event('M326-E04').date,'1785');
 assert.equal(event('M326-E04').type,'PRINT_IMPRINT_1785_CIST_MINUTES');
 assert.equal(event('M326-E05').type,'APPROVAL_WORDING_IN_LATER_GLOSSARY_UNRESOLVED');
 assert.ok(contract.dated_acts.every(e=>e.source_ids.length>0&&e.source_ids.every(id=>validSources.has(id))));
 assert.ok(contract.dated_acts.every(e=>e.independent_original_conference_minutes===false));
 const precision=date=>date.length===10?'DAY':date.length===7?'MONTH':'YEAR';
 assert.ok(contract.dated_acts.every(e=>e.precision===precision(e.date)));
 assert.ok(contract.claim_cards.every(c=>c.source_ids.every(id=>validSources.has(id))));
 assert.ok(contract.claim_cards.every(c=>!c.expert_approved&&!c.original_1785_full_page_collated));
 assert.equal(contract.observed_source_levels.historical_1898_print_page_visually_examined,1);
 assert.equal(contract.observed_source_levels.contemporary_1785_full_text_pages_visually_inspected,0);
 assert.equal(contract.observed_source_levels.independent_1784_christmas_conference_journal_read,0);
 assert.equal(contract.observed_source_levels.composite_1784_1785_scan_read,0);
 assert.equal(contract.metrics.actual_1785_original_pages_collated,0);
 assert.equal(contract.metrics.direct_1784_conference_minutes_read,0);
 assert.equal(contract.metrics.reviewed_1898_historical_reprint_pages,1);
 assert.equal(contract.metrics.prior_513_mutations,0);
 assert.equal(contract.suggested_reader_copy.public_release_allowed,false);
 assert.match(contract.adjudication.not_resolved,/Dec 27/i);
 assert.ok(contract.open_issues.some(i=>i.risk==='DEC24_DEC27_TITLE_DIFFERENCE'&&i.status==='OPEN'));
 assert.ok(contract.open_issues.some(i=>i.risk==='1785_GENERAL_RULES_APPROVAL'&&i.status==='OPEN'));
 assert.ok(contract.blocked_reading.length>=5);
 return {records:contract.source_records.length,stages:contract.dated_acts.length,cards:contract.claim_cards.length,readings:contract.readings.length,sections:9};
}
export function draftOutputs(input){
 const {contract}=input,base={version:'3.26',draft:true,publication_ready:false,expert_approved:false,full_1785_original_seen:false};
 return {
  'v326_methodist_chronology_evidence.json':{...base,count:contract.dated_acts.length,stages:contract.dated_acts,sources:contract.source_records},
  'v326_methodist_open_questions.json':{...base,count:contract.open_issues.length,issues:contract.open_issues,blocked_copies:contract.blocked_reading},
  'v326_methodist_claim_review_cards.json':{...base,count:contract.claim_cards.length,claims:contract.claim_cards}
 };
}
export function writeDraft(){
 const data=loadResearch();validateWitnessAudit(data);const outputs=draftOutputs(data),dir=path.join(ROOT,'out','atlas-v326');
 mkdirSync(dir,{recursive:true});
 for(const [name,obj] of Object.entries(outputs))writeFileSync(path.join(dir,name),JSON.stringify(obj,null,2)+'\n');
 return outputs;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const out=writeDraft();for(const [name,d] of Object.entries(out))console.log(name+': '+d.count+' DRAFT_ONLY');
}
