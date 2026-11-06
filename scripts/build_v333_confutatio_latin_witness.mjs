import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PARENT='data/contracts/atlas_v332_augsburg_article_response_triads.json';
const CURRENT='data/contracts/atlas_v333_confutatio_cr27_latin_excerpts_witness_audit.json';
const read=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
export const loadInputs=()=>({parent:read(PARENT),contract:read(CURRENT)});

export function validateV333({parent,contract}){
 assert.equal(execFileSync('git',['hash-object',PARENT],{cwd:ROOT,encoding:'utf8'}).trim(),contract.parent.locked_parent_blob_sha,'V3.32 contract hash changed');
 assert.equal(parent.version,'3.32');
 assert.equal(contract.version,'3.33');assert.equal(contract.depth,'MEDIUM');assert.equal(contract.status,'DRAFT');
 assert.equal(contract.research_focus,'V324-ISS02');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{readers:513,sections:1539,sources:723,overviews:97,events:26,relations:12,v332_triads:5,v332_claims:15});
 assert.equal(contract.source_records.length,12);
 assert.equal(contract.latin_clause_records.length,7);
 assert.equal(contract.article_claim_adjudications.length,4);
 assert.equal(contract.publication_stages.length,6);
 assert.equal(contract.readings.length,4);
 assert.equal(contract.readings.reduce((n,x)=>n+x.sections.length,0),12);
 assert.equal(contract.open_issues.length,10);
 assert.equal(contract.blocked_inferences.length,12);
 const sourceMap=new Map(contract.source_records.map(s=>[s.id,s]));
 const clauseMap=new Map(contract.latin_clause_records.map(c=>[c.id,c]));
 const caseMap=new Map(contract.article_claim_adjudications.map(x=>[x.id,x]));
 assert.equal(sourceMap.size,12);assert.equal(clauseMap.size,7);assert.equal(caseMap.size,4);
 assert.ok(contract.source_records.every(s=>s.contemporary_1530_manuscript_visually_inspected===false&&s.critical_1859_printed_leaf_visually_inspected===false),'no original witness leaf was seen');
 for(const c of contract.latin_clause_records){
  assert.ok(c.source_ids.length>=1&&c.source_ids.every(id=>sourceMap.has(id)),'latin lemma source missing');
  assert.equal(c.literal_1530_original_checked,false);
  assert.ok(c.lemma.length>15&&c.approx_korean.length>=10);
 }
 for(const c of contract.article_claim_adjudications){
  assert.ok(c.confutatio_latin_lemma_ids.length>=1&&c.augustana_latin_lemma_ids.length>=1);
  assert.ok([...c.confutatio_latin_lemma_ids,...c.augustana_latin_lemma_ids].every(id=>clauseMap.has(id)));
  assert.ok(c.english_source_ids.every(id=>sourceMap.has(id)));
 }
 const get=id=>clauseMap.get(id);
 assert.equal(get('V333-L01').article,'IV');
 assert.equal(get('V333-L01').source_ids[0],'V333-S-CR27-GOOGLE');
 assert.equal(get('V333-L01').critical_reference,'CR XXVII (1859) printed p99 / Google Books popular passage');
 assert.equal(get('V333-L02').article,'VII');
 assert.equal(get('V333-L02').critical_reference,'CR XXVII (1859) col102, cited in CPH Spanish note 169');
 assert.equal(get('V333-L03').critical_reference,'CR XXVII (1859) col104, cited in CPH Spanish note 181');
 assert.equal(get('V333-L04').article,'VIII');
 assert.equal(get('V333-L04').lemma,'acceptatur cum sancta romana ecclesia');
 assert.equal(get('V333-L04').critical_reference,'CR XXVII (1859) col105, cited in CPH Spanish note 189');
 assert.equal(get('V333-L05').level,'AUGUSTANA_LATIN_LATER_UNCOLLATED_TRANSCRIPTION');
 assert.equal(caseMap.get('V333-C01').confutatio_stance,'ACCEPTS_ANTI_PELAGIAN_LIMIT_THEN_DISPUTES_MERIT');
 assert.equal(caseMap.get('V333-C02').confutatio_stance,'CONDITIONAL_REJECTION_OF_CHURCH_DEFINITION');
 assert.equal(caseMap.get('V333-C03').confutatio_stance,'PRAISES_LOCAL_RITUAL_VARIETY_BUT_DISTINGUISHES_UNIVERSAL');
 assert.equal(caseMap.get('V333-C04').confutatio_stance,'EXPLICIT_ACCEPTANCE_OF_ARTICLE_VIII');
 const events=new Map(contract.publication_stages.map(x=>[x.id,x]));
 assert.equal(events.size,6);
 assert.equal(events.get('V333-D02').date,'1530-08-03');
 assert.equal(events.get('V333-D02').type,'CONFUTATIO_PUBLIC_GERMAN_READING');
 assert.equal(events.get('V333-D03').type,'COCHLAEUS_SUMMARY_NOT_FULL_CONFUTATIO');
 assert.equal(events.get('V333-D04').date,'1573');
 assert.equal(events.get('V333-D04').type,'FIRST_FULL_LATIN_CONFUTATIO_PRINT_FABRICIUS');
 assert.deepEqual(contract.publication_stages.filter(x=>x.first_published_latin_full_text).map(x=>x.id),['V333-D04']);
 assert.equal(events.get('V333-D05').type,'GERMAN_ARCHIVAL_CRITICAL_PUBLICATION_MUELLER');
 assert.equal(events.get('V333-D06').type,'CORPUS_REFORMATORUM_27_MULTIWITNESS_CRITICAL_EDITION');
 for(const stage of contract.publication_stages)assert.ok(stage.source_ids.length>=1&&stage.source_ids.every(id=>sourceMap.has(id)));
 const ledger=contract.witness_ledger;
 for(const key of ['direct_1530_german_original_pages','direct_1530_latin_confutatio_public_print_pages','direct_1573_fabricius_latin_print_pages','direct_1859_CR27_print_pages','direct_original_1530_1531_parallel_text_pairs'])assert.equal(ledger[key],0);
 assert.equal(ledger.CR27_page_99_google_snippet_looked_up,true);
 assert.equal(ledger.CR27_col_102_104_105_quoted_via_CPH_es,true);
 assert.equal(ledger.BSB_1859_catalogue_342_scans_found,true);
 assert.ok(contract.readings.every(r=>r.sections.length===3&&r.sections.every(s=>s.body.length>=130)));
 assert.ok(contract.blocked_inferences.some(s=>s.includes('1530 public German reading')));
 assert.ok(contract.blocked_inferences.some(s=>s.includes('1573 first Latin printed')));
 assert.ok(contract.blocked_inferences.some(s=>s.includes('VIII explicit acceptatur')));
 assert.ok(contract.blocked_inferences.some(s=>s.includes('Wycliffe/Hus')));
 assert.equal(contract.metrics.original_primary_folios_directly_collated,0);
 assert.equal(contract.metrics.original_corpus_mutations,0);
 return {sources:12,latin_lemmas:7,article_cases:4,publication_events:6,essays:4,sections:12,gaps:10};
}
export function draftReviewOutputs({contract}){
 const flag={version:'3.33',draft:true,research_only:true,published:false,webapp_integrated:false,expert_approved:false,actual_original_latin_folios_seen:0};
 return {
  'v333_latin_clause_evidence_grade.json':{...flag,count:contract.latin_clause_records.length,clauses:contract.latin_clause_records,sources:contract.source_records,article_cases:contract.article_claim_adjudications},
  'v333_1530_1573_1859_publication_genealogy.json':{...flag,count:contract.publication_stages.length,stages:contract.publication_stages,limitations:contract.blocked_inferences},
  'v333_original_language_primary_witness_queue.json':{...flag,count:contract.open_issues.length,issues:contract.open_issues,witness_ledger:contract.witness_ledger}
 };
}
export function writeReviewOnly(){
 const d=loadInputs();validateV333(d);const out=draftReviewOutputs(d);
 const dir=path.join(ROOT,'out','atlas-v333');mkdirSync(dir,{recursive:true});
 for(const [name,obj] of Object.entries(out))writeFileSync(path.join(dir,name),JSON.stringify(obj,null,2)+'\n');
 return out;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const out=writeReviewOnly();for(const [name,obj] of Object.entries(out))console.log(name+' '+obj.count+' REVIEW_ONLY');
}
