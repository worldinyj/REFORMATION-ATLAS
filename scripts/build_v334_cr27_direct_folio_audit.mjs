import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PARENT='data/contracts/atlas_v333_confutatio_cr27_latin_excerpts_witness_audit.json';
const CURRENT='data/contracts/atlas_v334_cr27_1859_direct_folio_inspection.json';
const read=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
export function loadInputs(){return {parent:read(PARENT),contract:read(CURRENT)}}

export function validateV334({parent,contract}){
 assert.equal(execFileSync('git',['hash-object',PARENT],{cwd:ROOT,encoding:'utf8'}).trim(),
  contract.parent.locked_parent_blob_sha,'V3.33 parent contract must remain immutable');
 assert.equal(parent.version,'3.33');
 assert.equal(parent.witness_ledger.direct_1859_CR27_print_pages,0,
  'Historical V3.33 zero must remain recorded as its then-current witness status');
 assert.equal(contract.version,'3.34');
 assert.equal(contract.status,'DRAFT');
 assert.equal(contract.depth,'MEDIUM');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{original_readers:513,original_sections:1539,original_sources:723,overviews:97,curated_events:26,relations:12,v333_latin_clauses:7});
 assert.equal(contract.sources.length,9);
 assert.equal(contract.print_page_map.length,8);
 assert.equal(contract.latin_fragments.length,4);
 assert.equal(contract.observations.length,7);
 assert.equal(contract.corrections.length,5);
 assert.equal(contract.readings.length,4);
 assert.equal(contract.readings.reduce((n,r)=>n+r.sections.length,0),12);
 assert.equal(contract.open_issues.length,9);
 assert.equal(contract.source_pdf.pdf_page_count,360);
 assert.equal(contract.source_pdf.pdf_bytes,30637982);
 assert.equal(contract.source_pdf.pdf_sha256,'ba1995d5587375a13f5298001e7a6c42d68f1c6b161ae86335471a1c4f30b29d');
 assert.equal(contract.source_pdf.printed_edition_year,1859);
 assert.deepEqual(contract.source_pdf.verified_workflow_run_ids,[42232566430,42232790784,42232985301]);
 assert.equal(contract.source_pdf.separate_from_BSB_342_image_copy,true);
 const sourceMap=new Map(contract.sources.map(x=>[x.id,x]));
 const pageMap=new Map(contract.print_page_map.map(x=>[x.pdf_page_1based,x]));
 const fragmentMap=new Map(contract.latin_fragments.map(x=>[x.id,x]));
 const observationMap=new Map(contract.observations.map(x=>[x.id,x]));
 assert.equal(sourceMap.size,9);assert.equal(pageMap.size,8);
 assert.equal(fragmentMap.size,4);assert.equal(observationMap.size,7);
 assert.ok(contract.sources.every(x=>x.original_1530_or_1573_print_visually_seen===false));
 for(const p of contract.print_page_map){
  assert.equal(p.pdf_page_0based,p.pdf_page_1based-1);
  assert.equal(p.printed_right_col,p.printed_left_col+1);
  assert.equal(p.visually_checked,true);
 }
 const expectedPages=[[69,93,94],[70,95,96],[71,97,98],[72,99,100],[73,101,102],[74,103,104],[75,105,106],[76,107,108]];
 assert.deepEqual(contract.print_page_map.map(x=>[x.pdf_page_1based,x.printed_left_col,x.printed_right_col]),expectedPages);
 for(const fragment of contract.latin_fragments){
  assert.equal(fragment.actual_1859_print_image_verified,true);
  assert.equal(fragment.original_1530_or_1573_leaf_seen,false);
  assert.ok(fragment.source_ids.every(x=>sourceMap.has(x)));
  const page=pageMap.get(fragment.pdf_page_1based);
  assert.ok(page && [page.printed_left_col,page.printed_right_col].includes(fragment.printed_col),'printed column and scanned page do not align');
 }
 const a=fragmentMap.get('V334-F1'),b=fragmentMap.get('V334-F2'),c=fragmentMap.get('V334-F3'),d=fragmentMap.get('V334-F4');
 assert.deepEqual([a.article,a.printed_col,a.pdf_page_1based],['IV',96,70]);
 assert.equal(a.latin,'Gratia Dei praevenit voluntatem');
 assert.deepEqual([b.article,b.printed_col,b.pdf_page_1based],['VII',102,73]);
 assert.ok(b.translation_and_context.includes('103열'));
 assert.deepEqual([c.article,c.printed_col,c.pdf_page_1based],['VII',104,74]);
 assert.deepEqual([d.article,d.printed_col,d.pdf_page_1based],['VIII',105,75]);
 assert.equal(d.latin,'acceptatur cum sancta romana ecclesia');
 assert.equal(observationMap.get('V334-O02').type,'VII_CROSS_COLUMN_CONDITION');
 assert.equal(observationMap.get('V334-O04').type,'VIII_AFFIRMATIVE_ACCEPTANCE');
 assert.equal(observationMap.get('V334-O05').type,'HUSS_WYCLIFFE_POLEMIC');
 const correction=new Map(contract.corrections.map(x=>[x.id,x]));
 assert.equal(correction.size,5);
 assert.equal(correction.get('V334-C1').previous_id,'V333-L01');
 assert.equal(correction.get('V334-C1').disposition,'CORRECT_FALSE_PRINTED_PAGE_LOCATOR');
 assert.ok(correction.get('V334-C1').replacement.includes('column 96'));
 assert.equal(correction.get('V334-C2').disposition,'ADD_REQUIRED_CROSS_COLUMN_CONDITION');
 assert.equal(correction.get('V334-C5').disposition,'SUPERSEDE_WITNESS_LEVEL_NOT_MUTATE_PARENT');
 assert.ok(contract.corrections.every(x=>x.previous_data_remains_immutable===true));
 const scope=contract.source_scope;
 assert.deepEqual(scope.claim_supporting_1859_pdf_pages_visually_read,[70,73,74,75]);
 assert.deepEqual(scope.verified_printed_columns,[96,102,103,104,105]);
 assert.equal(scope.full_1859_variant_apparatus_collated,false);
 assert.equal(scope.original_1530_german_manuscript_pages_visually_read,0);
 assert.equal(scope.original_1573_first_latin_print_pages_visually_read,0);
 assert.equal(scope.original_1530_vs_1573_pairs_collated,0);
 assert.equal(scope.historian_expert_approved,false);
 assert.ok(contract.readings.every(r=>r.sections.length===3 && r.sections.every(x=>x.body.length>=100)));
 assert.ok(contract.blocked_claims.some(x=>x.includes('Article VIII rejected')));
 assert.ok(contract.blocked_claims.some(x=>x.includes('Google Books 99')));
 assert.ok(contract.blocked_claims.some(x=>x.includes('Hus and Wycliffe')));
 assert.equal(contract.metrics.verified_1859_claim_supporting_pages,4);
 assert.equal(contract.metrics.original_1530_witness_pages,0);
 assert.equal(contract.metrics.original_reader_mutations,0);
 return {sources:9,printed_page_pairs:8,latin_clauses:4,findings:7,corrections:5,essays:4,sections:12,open_issues:9};
}
export function reviewOnly({contract}){
 const common={version:'3.34',draft:true,release_approved:false,google_ai_studio_integrated:false,original_1530_or_1573_direct_folios:0,source_1859_print_image_pages_checked:4};
 return {
  'v334_1859_folio_lemma_evidence.json':{...common,count:contract.latin_fragments.length,clauses:contract.latin_fragments,pages:contract.print_page_map,file:contract.source_pdf},
  'v334_v333_locator_and_evidence_corrections.json':{...common,count:contract.corrections.length,changes:contract.corrections,findings:contract.observations},
  'v334_1573_1530_original_witness_queue.json':{...common,count:contract.open_issues.length,issues:contract.open_issues,source_scope:contract.source_scope}
 };
}
export function build(){
 const input=loadInputs();validateV334(input);const files=reviewOnly(input);
 const dir=path.join(ROOT,'out','atlas-v334');mkdirSync(dir,{recursive:true});
 for(const [filename,record] of Object.entries(files))writeFileSync(path.join(dir,filename),JSON.stringify(record,null,2)+'\n');
 return files;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const files=build();for(const [name,record] of Object.entries(files))console.log(name+' '+record.count+' REVIEW_ONLY');
}
