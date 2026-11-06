import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const OLD='data/contracts/atlas_v328_methodist_1785_1789_witness_scope.json';
const CURRENT='data/contracts/atlas_v329_general_rules_1788_annex_correction.json';
const json=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
export const loadInputs=()=>({parent:json(OLD),contract:json(CURRENT)});

export function validateV329({parent,contract}){
 const blob=execFileSync('git',['hash-object',OLD],{cwd:ROOT,encoding:'utf8'}).trim();
 assert.equal(blob,contract.parent.locked_parent_blob_sha,'V3.28 parent contract must be unchanged');
 assert.equal(parent.version,'3.28');assert.equal(contract.version,'3.29');
 assert.equal(contract.status,'DRAFT');assert.equal(contract.depth,'MEDIUM');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{
  readers:513,sections:1539,original_source_records:723,overviews:97,curated_events:26,
  original_typed_relations:12,prior_v328_claim_cards:12
 });
 assert.equal(contract.sources.length,12);
 assert.equal(contract.witness_nodes.length,7);
 assert.equal(contract.relations.length,6);
 assert.equal(contract.supersession_cards.length,4);
 assert.equal(contract.readings.length,3);
 assert.equal(contract.readings.reduce((n,r)=>n+r.sections.length,0),9);
 assert.equal(contract.open_issues.length,8);
 const sm=new Map(contract.sources.map(x=>[x.id,x]));
 const wm=new Map(contract.witness_nodes.map(x=>[x.id,x]));
 assert.equal(sm.size,12);assert.equal(wm.size,7);
 for(const w of contract.witness_nodes){
  assert.ok(w.source_ids.length>0&&w.source_ids.every(s=>sm.has(s)),'dangling witness source');
  assert.equal(w.original_edition_relevant_page_read,false,'1788/1789 original print was not visually read');
 }
 for(const edge of contract.relations){
  assert.ok(wm.has(edge.from)&&wm.has(edge.to),'dangling witness graph link');
  assert.ok(edge.source_ids.length>0&&edge.source_ids.every(s=>sm.has(s)),'dangling claim source');
  assert.equal(edge.exact_original_page_comparison,false);
 }
 const witness=id=>wm.get('V329-'+id);
 const link=id=>contract.relations.find(x=>x.id==='V329-'+id);
 assert.equal(witness('W03').year,1788);
 assert.equal(witness('W03').status,'RULES_SEPARATE_ANNEX_ATTESTED_BY_1898_HISTORIOGRAPHY');
 assert.equal(witness('W04').year,1787);
 assert.equal(witness('W04').status,'INTERNAL_DATE_1787_05_28_NOT_1788_IMPRINT');
 assert.equal(witness('W05').year,1789);
 assert.equal(witness('W05').work,'1789_FIFTH_NEW_YORK_ROSS');
 assert.equal(witness('W06').year,1790);
 assert.equal(link('REL01').from,'V329-W04');
 assert.equal(link('REL01').to,'V329-W03');
 assert.equal(link('REL01').type,'HISTORIAN_ATTESTED_SEPARATE_ANNEX');
 assert.equal(link('REL03').from,'V329-W03');
 assert.equal(link('REL03').to,'V329-W05');
 assert.equal(sm.get('V329-S-TIGERT106').level,'1898_PRINT_P106_VISUALLY_SCREENED');
 assert.equal(sm.get('V329-S-TIGERT107').level,'1898_PRINT_P107_VISUALLY_SCREENED');
 assert.equal(sm.get('V329-S-VANDERBILT1788').level,'ACADEMIC_LIBRARY_HOLDING');
 assert.equal(sm.get('V329-S-NEWS1912').level,'1912_NEWSPAPER_OCR_HISTORIC_WITNESS_REPORT');
 assert.ok(sm.get('V329-S-TIGERT106').description.includes('reprints omitted annexed useful pieces'));
 const corrections=new Map(contract.supersession_cards.map(x=>[x.id,x]));
 assert.equal(corrections.size,4);
 assert.equal(corrections.get('V329-CORR01').target_version,'3.28');
 assert.equal(corrections.get('V329-CORR01').status,'SUPERSEDED_OVERBROAD');
 assert.ok(corrections.get('V329-CORR01').replacement.includes('1788'));
 assert.equal(corrections.get('V329-CORR02').status,'SUPERSEDED_OVERBROAD');
 assert.ok(contract.central_correction.includes('first American General Rules print in 1789 is overbroad'));
 assert.ok(contract.central_correction.includes('1788 first-ever status remains unproved'));
 for(const x of contract.supersession_cards)assert.equal(x.delete_upstream_file,false);
 assert.equal(contract.source_scope.historical_1898_printed_pages_visually_read,2);
 assert.equal(contract.source_scope.original_1788_general_rules_pages_visually_read,0);
 assert.equal(contract.source_scope.original_1789_general_rules_pages_visually_read,0);
 assert.equal(contract.source_scope.original_1785_Q16_Q17_pages_visually_read,0);
 assert.equal(contract.source_scope.direct_1788_1789_page_pairs_collated,0);
 assert.equal(contract.source_scope.scanned_1912_newspaper_image_seen,false);
 assert.equal(contract.metrics.original_corpus_mutations,0);
 assert.ok(contract.open_issues.some(x=>x.id==='V329-I-1788_ANNEX_PAGE'&&x.priority==='P0'));
 assert.ok(contract.open_issues.some(x=>x.id==='V329-I-1789_FIFTH_ORIGINAL'&&x.priority==='P0'));
 assert.ok(contract.publication_warnings.includes('1789 first ever General Rules printing superseded'));
 assert.ok(contract.publication_warnings.includes('1788 first ever printing NOT proven'));
 return {sources:12,witnesses:7,links:6,corrections:4,readings:3,sections:9,issues:8};
}
export function reviewOnly({contract}){
 const head={version:'3.29',status:'DRAFT_HOLD',publication_ready:false,webapp_integrated:false,
    original_1788_1789_aligned_page_pairs:0};
 return {
   'v329_explicit_supersession_ledger.json':{...head,count:contract.supersession_cards.length,items:contract.supersession_cards,
      correction:contract.central_correction},
   'v329_1787_1790_rules_edition_graph.json':{...head,count:contract.relations.length,relations:contract.relations,
      nodes:contract.witness_nodes,sources:contract.sources},
   'v329_original_witness_followup_queue.json':{...head,count:contract.open_issues.length,issues:contract.open_issues,
      witness_scope:contract.source_scope}
 };
}
export function build(){
 const x=loadInputs();validateV329(x);const out=reviewOnly(x);
 const directory=path.join(ROOT,'out','atlas-v329');mkdirSync(directory,{recursive:true});
 for(const [name,object] of Object.entries(out))writeFileSync(path.join(directory,name),JSON.stringify(object,null,2)+'\n');
 return out;
}
if(process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const data=build();for(const [name,obj] of Object.entries(data))console.log(name+' '+obj.count+' REVIEW_ONLY');
}
