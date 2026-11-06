import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PREVIOUS='data/contracts/atlas_v330_1788_1789_general_rules_integration_review.json';
const CURRENT='data/contracts/atlas_v331_1788_1789_primary_page_access_matrix.json';
const read=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
export const loadStudy=()=>({previous:read(PREVIOUS),contract:read(CURRENT)});
export function validateV331({previous,contract}){
 const parent_sha=execFileSync('git',['hash-object',PREVIOUS],{cwd:ROOT,encoding:'utf8'}).trim();
 assert.equal(parent_sha,contract.parent.locked_parent_contract_blob_sha,'Upstream V3.30 historical data was changed');
 assert.equal(previous.version,'3.30');
 assert.equal(contract.version,'3.31');
 assert.equal(contract.depth,'MEDIUM');
 assert.equal(contract.status,'DRAFT');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{
  reader_count:513,original_reader_section_count:1539,original_source_records:723,
  overviews:97,curated_events:26,original_typed_relations:12,prior_v330_claims:14,prior_v330_links:7
 });
 assert.equal(contract.source_registry.length,14);
 assert.equal(contract.original_page_requests.length,9);
 assert.equal(contract.comparison_cards.length,10);
 assert.equal(contract.readings.length,3);
 assert.equal(contract.readings.reduce((n,r)=>n+r.sections.length,0),9);
 assert.equal(contract.open_issues.length,9);
 assert.equal(contract.differentiated_research_conclusions.length,6);
 const src=new Map(contract.source_registry.map(s=>[s.id,s]));
 const targets=new Map(contract.original_page_requests.map(t=>[t.id,t]));
 const compare=new Map(contract.comparison_cards.map(c=>[c.id,c]));
 assert.equal(src.size,14);
 assert.equal(targets.size,9);
 assert.equal(compare.size,10);
 for(const s of contract.source_registry){
  assert.equal(s.contemporary_1788_1789_page_directly_seen,false,'source evidence incorrectly upgraded '+s.id);
  assert.ok(/^https:\/\//.test(s.url),'external source must have HTTPS provenance');
 }
 for(const target of contract.original_page_requests){
  assert.ok(target.source_ids.length>0 && target.source_ids.every(x=>src.has(x)),'unknown source in acquisition target '+target.id);
  assert.equal(target.original_leaf_visual_check_pass,false,'missing original must not become visually verified');
  assert.equal(target.expert_reviewed,false);
  assert.ok(['NO_DIRECT_IMAGE','INDEX_ONLY'].includes(target.access_status));
  assert.equal(target.request_kind,'RESEARCH_ONLY_NO_AUTOMATED_SCRAPING');
 }
 for(const c of contract.comparison_cards){
  assert.ok(src.has(c.primary_source_id),'comparison source missing');
  assert.ok(targets.has(c.verification_target_id),'comparison target missing');
  assert.equal(c.original_pages_compared,0);
  assert.equal(c.approved_for_publication,false);
 }
 const target=id=>targets.get('V331-'+id);
 assert.equal(target('T01').year,1788);
 assert.equal(target('T01').edition,'KOLLOCK_BOOK_TITLE');
 assert.equal(target('T01').access_status,'NO_DIRECT_IMAGE');
 assert.equal(target('T02').target_type,'SEPARATE_TITLE_AND_FIRST_PAGE');
 assert.equal(target('T03').target_type,'PRINTED_P41');
 assert.equal(target('T04').year,1789);
 assert.equal(target('T04').edition,'ROSS_FIFTH_TITLE');
 assert.equal(target('T05').target_type,'HEADING_AND_PAGE_BOUNDARY');
 assert.equal(target('T06').target_type,'DRUNKENNESS_CLAUSE');
 assert.equal(target('T08').year,1787);
 assert.equal(target('T08').access_status,'INDEX_ONLY');
 assert.equal(target('T09').target_type,'SCHOLARLY_PAGE_CITATIONS');
 assert.equal(src.get('V331-S10').evidence_type,'CHRONOLOGICAL_FALSE_FRIEND');
 assert.ok(src.get('V331-S10').what_verified.includes('one century newer'));
 assert.equal(src.get('V331-S09').evidence_type,'DIGITAL_TRANSCRIPTION_INDEX_JAVASCRIPT_GATE');
 assert.ok(compare.get('V331-X07').claim.includes('1888'));
 assert.equal(compare.get('V331-X08').verification_target_id,'V331-T08');
 assert.equal(compare.get('V331-X04').primary_source_id,'V331-S06');
 assert.equal(compare.get('V331-X05').verification_target_id,'V331-T03');
 assert.equal(contract.inspection_ledger.original_1788_Kollock_p41_image_pass,0);
 assert.equal(contract.inspection_ledger.original_1788_annex_title_image_pass,0);
 assert.equal(contract.inspection_ledger.original_1789_Ross_main_rules_image_pass,0);
 assert.equal(contract.inspection_ledger.original_1789_Ross_temperance_image_pass,0);
 assert.equal(contract.inspection_ledger.original_1789_Ross_six_month_rule_image_pass,0);
 assert.equal(contract.inspection_ledger.contemporary_original_1788_1789_folios_newly_read,0);
 assert.equal(contract.inspection_ledger.original_same_passage_pairs_aligned,0);
 assert.equal(contract.inspection_ledger.scholarly_Ruth_1997_print_pages_visual_previous_V330,2);
 assert.equal(contract.inspection_ledger.historical_Tigert_1898_print_pages_visual_previous_V329,2);
 assert.ok(contract.blocked_unsafe_upgrades.some(x=>x.includes('1888')));
 assert.ok(contract.blocked_unsafe_upgrades.some(x=>x.includes('Evans TCP 1787')));
 assert.ok(contract.blocked_unsafe_upgrades.some(x=>x.includes('Bangs')));
 assert.equal(contract.metrics.original_page_pairs_collated,0);
 assert.equal(contract.metrics.original_reader_mutations,0);
 assert.equal(contract.metrics.source_records,14);
 assert.equal(contract.metrics.requested_original_page_targets,9);
 assert.equal(contract.metrics.source_graded_comparisons,10);
 assert.equal(contract.metrics.medium_sections,9);
 assert.equal(contract.metrics.differentiated_conclusions,6);
 assert.ok(contract.open_issues.some(x=>x.id==='V331-I01' && x.priority==='P0'));
 assert.ok(contract.open_issues.some(x=>x.id==='V331-I03' && x.priority==='P0'));
 return {sources:14,targets:9,comparisons:10,readings:3,sections:9,issues:9};
}
export function reviewOnly({contract}){
 const common={version:'3.31',status:'RESEARCH_DRAFT',public_release_approved:false,
   expert_approved:false,webapp_integrated:false,original_1788_1789_print_page_pairs:0};
 return {
  'v331_original_folio_request_manifest.json':{...common,count:contract.original_page_requests.length,items:contract.original_page_requests,source_registry:contract.source_registry},
  'v331_source_level_edition_claims.json':{...common,count:contract.comparison_cards.length,items:contract.comparison_cards,conclusions:contract.differentiated_research_conclusions},
  'v331_unresolved_original_access_flags.json':{...common,count:contract.open_issues.length,issues:contract.open_issues,ledger:contract.inspection_ledger,blocked:contract.blocked_unsafe_upgrades}
 };
}
export function buildReview(){
 const input=loadStudy();validateV331(input);const files=reviewOnly(input);
 const dir=path.join(ROOT,'out','atlas-v331');mkdirSync(dir,{recursive:true});
 for(const [name,item] of Object.entries(files))writeFileSync(path.join(dir,name),JSON.stringify(item,null,2)+'\n');
 return files;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const files=buildReview();for(const [name,item] of Object.entries(files))console.log(name+' '+item.count+' REVIEW_ONLY');
}
