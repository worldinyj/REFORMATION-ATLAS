import assert from 'node:assert/strict';
import {readFileSync, mkdirSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PARENT='data/contracts/atlas_v327_methodist_question_edition_concordance.json';
const PATH='data/contracts/atlas_v328_methodist_1785_1789_witness_scope.json';
const json=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
export function loadInputs(){return {parent:json(PARENT),contract:json(PATH)}}
export function verifyV328({parent,contract}){
 assert.equal(execFileSync('git',['hash-object',PARENT],{cwd:ROOT,encoding:'utf8'}).trim(),contract.parent.locked_parent_blob_sha,'V3.27 prior blob must remain untouched');
 assert.equal(parent.version,'3.27');assert.equal(contract.version,'3.28');assert.equal(contract.depth,'MEDIUM');assert.equal(contract.status,'DRAFT');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{readers:513,sections:1539,source_records:723,overviews:97,curated_events:26,typed_relations:12,v327_edition_records:6,v327_question_fragments:11});
 assert.equal(contract.sources.length,11);assert.equal(new Set(contract.sources.map(s=>s.id)).size,11);
 assert.equal(contract.topic_evidence.length,6);
 assert.equal(contract.claim_cards.length,12);assert.equal(new Set(contract.claim_cards.map(c=>c.id)).size,12);
 assert.equal(contract.readings.length,3);
 assert.equal(contract.readings.reduce((n,r)=>n+r.sections.length,0),9);
 assert.equal(contract.open_issues.length,8);
 const src=new Set(contract.sources.map(s=>s.id));
 assert.ok([...contract.topic_evidence,...contract.claim_cards].every(x=>x.source_ids.length>0&&x.source_ids.every(id=>src.has(id))),'all claims must trace sources');
 const get=id=>contract.topic_evidence.find(e=>e.id==='V328-E-'+id);
 assert.equal(get('1770-BRITAIN').months,3);
 assert.equal(get('1770-BRITAIN').proof,'DIRECT_PRINT_VISUAL');
 assert.equal(get('1770-BRITAIN').direct_year_edition_body_page_read,true);
 assert.equal(get('1785-AMERICA').months,2);
 assert.equal(get('1785-AMERICA').proof,'LATER_ACADEMIC_QUOTATION');
 assert.equal(get('1785-AMERICA').direct_year_edition_body_page_read,false);
 assert.equal(get('1789-AMERICA').months,6);
 assert.equal(get('1789-AMERICA').proof,'NINETEENTH_CENTURY_RETROSPECTIVE');
 assert.equal(get('1789-GENERAL-RULES').months,null);
 assert.equal(get('1789-GENERAL-RULES').proof,'NINETEENTH_CENTURY_HISTORY_NOT_ORIGINAL_LEAF');
 assert.equal(get('1798-AMERICA').months,6);
 assert.equal(get('1798-AMERICA').proof,'PDF_TEXT_NOT_PARAGRAPH_SCREENSHOT');
 assert.deepEqual(contract.topic_evidence.filter(x=>x.direct_year_edition_body_page_read).map(x=>x.id),['V328-E-1770-BRITAIN']);
 assert.equal(contract.witness_ledger.british_1770_Q18_scan_pages,1);
 assert.equal(contract.witness_ledger.american_1785_Q16_Q17_original_pages,0);
 assert.equal(contract.witness_ledger.american_1789_six_month_original_pages,0);
 assert.equal(contract.witness_ledger.american_1789_general_rules_original_pages,0);
 assert.equal(contract.witness_ledger.american_1798_six_month_specific_screenshot_pages,0);
 assert.equal(contract.witness_ledger.original_1785_to_1789_aligned_print_pairs,0);
 assert.equal(contract.metrics.original_corpus_mutations,0);
 assert.ok(contract.held_inferences.some(s=>s.includes('1789 full General Rules inclusion')));
 assert.ok(contract.held_inferences.some(s=>s.includes('1789 six-month revision')));
 assert.ok(contract.held_inferences.some(s=>s.includes('1785 Q42 anti-slavery')));
 assert.ok(contract.open_issues.every(x=>x.status==='ORIGINAL_WITNESS_NOT_YET_COLLATED'));
 const p0=contract.open_issues.filter(x=>x.priority==='P0');
 assert.equal(p0.length,3);
 assert.equal(contract.metrics.sources,11);
 assert.equal(contract.metrics.edition_topic_records,6);
 assert.equal(contract.metrics.claims,12);
 assert.equal(contract.metrics.sections,9);
 return {sources:11,editions:6,claims:12,readings:3,sections:9,issues:8};
}
export function reviewOnlyOutputs({contract}){
 const flag={version:'3.28',status:'RESEARCH_DRAFT',publication_ready:false,webapp_integrated:false,original_1785_to_1789_same_text_pairs:0};
 return {
  'v328_methodist_1785_1789_claims.json':{...flag,count:contract.claim_cards.length,claims:contract.claim_cards,source_registry:contract.sources},
  'v328_methodist_edition_events.json':{...flag,count:contract.topic_evidence.length,editions:contract.topic_evidence,limitations:contract.held_inferences},
  'v328_primary_source_research_gaps.json':{...flag,count:contract.open_issues.length,issues:contract.open_issues,ledger:contract.witness_ledger}
 };
}
export function build(){const x=loadInputs();verifyV328(x);const outputs=reviewOnlyOutputs(x);
 const dir=path.join(ROOT,'out','atlas-v328');mkdirSync(dir,{recursive:true});
 for(const [name,obj] of Object.entries(outputs))writeFileSync(path.join(dir,name),JSON.stringify(obj,null,2)+'\n');
 return outputs;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const output=build();for(const [name,item] of Object.entries(output))console.log(name+' '+item.count+' REVIEW_ONLY');
}
