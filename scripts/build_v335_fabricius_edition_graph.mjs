import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PREVIOUS='data/contracts/atlas_v334_cr27_1859_direct_folio_inspection.json';
const CURRENT='data/contracts/atlas_v335_fabricius_1573_first_print_bibliography.json';
const read=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
export function loadInputs(){return {parent:read(PREVIOUS),contract:read(CURRENT)};}
export function validateV335({parent,contract}){
 assert.equal(execFileSync('git',['hash-object',PREVIOUS],{cwd:ROOT,encoding:'utf8'}).trim(),contract.parent.locked_parent_blob_sha,'V3.34 parent changed');
 assert.equal(parent.version,'3.34');
 assert.equal(contract.version,'3.35');
 assert.equal(contract.status,'DRAFT');
 assert.equal(contract.depth,'MEDIUM');
 assert.equal(contract.research_date,'2026-11-07');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{readers:513,sections:1539,source_records:723,overviews:97,curated_events:26,typed_relations:12,v334_direct_1859_latin_fragments:4});
 assert.equal(contract.source_records.length,15);
 assert.equal(contract.witness_nodes.length,8);
 assert.equal(contract.typed_relations.length,8);
 assert.equal(contract.chapter_comparison_requests.length,4);
 assert.equal(contract.digital_access_probes.length,4);
 assert.equal(contract.warnings.length,10);
 assert.equal(contract.readings.length,3);
 assert.equal(contract.readings.reduce((n,x)=>n+x.sections.length,0),9);
 assert.equal(contract.open_issues.length,10);
 const source=new Map(contract.source_records.map(x=>[x.id,x]));
 const node=new Map(contract.witness_nodes.map(x=>[x.id,x]));
 const relations=new Map(contract.typed_relations.map(x=>[x.id,x]));
 assert.equal(source.size,15);assert.equal(node.size,8);assert.equal(relations.size,8);
 assert.ok(contract.source_records.every(x=>x.direct_1573_folio_seen===false),'1573 source image was not directly seen');
 for(const n of contract.witness_nodes){
  assert.equal(n.direct_1573_edition_page,false);
  assert.ok(n.source_ids.length>=1&&n.source_ids.every(id=>source.has(id)));
 }
 for(const r of contract.typed_relations){
  assert.ok(node.has(r.from)&&node.has(r.to),'unknown witness relation endpoint');
  assert.ok(r.source_ids.length>0&&r.source_ids.every(id=>source.has(id)));
  assert.equal(r.exact_1573_1859_word_pairs_compared,0);
 }
 assert.equal(node.get('V335-E04').year,1573);
 assert.equal(node.get('V335-E04').work,'FABRICIUS_HARMONIA_FIRST_PRINT');
 assert.ok(node.get('V335-E04').source_ids.includes('V335-S01'));
 assert.ok(node.get('V335-E04').source_ids.includes('V335-S15'));
 assert.equal(node.get('V335-E05').year,1587);
 assert.equal(node.get('V335-E05').work,'FABRICIUS_HARMONIA_RICHER_SECOND_PRINT');
 assert.equal(node.get('V335-E06').year,1597);
 assert.equal(node.get('V335-E08').year,1859);
 assert.equal(source.get('V335-S01').grade,'NATIONAL_LIBRARY_1573_IMPRINT_CATALOGUE');
 assert.equal(source.get('V335-S05').grade,'UNIVERSITY_LIBRARY_1587_SECOND_EDITION');
 assert.ok(source.get('V335-S05').note.includes('Editio secunda'));
 assert.equal(source.get('V335-S15').grade,'RARE_BOOK_DEALER_CATALOGUE_PAGE_VISUALLY_SCREENED');
 assert.ok(source.get('V335-S15').note.includes('VD16 L940'));
 assert.equal(relations.get('V335-R01').type,'HISTORIOGRAPHIC_FIRST_FULL_LATIN_PUBLICATION');
 assert.equal(relations.get('V335-R02').type,'SEPARATE_REVISED_SECOND_EDITION');
 assert.equal(relations.get('V335-R03').type,'HISTORIOGRAPHIC_DERIVATION_WARNING');
 assert.equal(relations.get('V335-R05').exact_1573_1859_word_pairs_compared,0);
 assert.equal(relations.get('V335-R06').type,'DIFFERENT_TEXT_DOMAIN_WITHIN_SAME_COLLECTION');
 assert.ok(relations.get('V335-R06').source_ids.includes('V335-S15'));
 const expectedLoci=[['IV',96,70],['VII',102,73],['VII',104,74],['VIII',105,75]];
 assert.deepEqual(contract.chapter_comparison_requests.map(x=>[x.article,x.cr27_print_column,x.cr27_pdf_page_1based]),expectedLoci);
 for(const loc of contract.chapter_comparison_requests){
  assert.equal(loc.cr27_1859_visible,true);
  assert.equal(loc.fabricius_1573_exact_page_found,false);
  assert.equal(loc.fabricius_1573_phrase_visually_read,false);
  assert.equal(loc.original_pair_collated,false);
 }
 assert.equal(contract.digital_access_probes.filter(x=>x.http_status===200&&x.mime_type==='text/html'&&x.request_type==='reader').length,2);
 assert.equal(contract.digital_access_probes.filter(x=>x.http_status===403&&x.mime_type==='text/html'&&x.request_type==='download').length,2);
 assert.deepEqual(contract.digital_access_probes.map(x=>[x.volume_id,x.request_type,x.http_status]),[
  ['gTRjAAAAcAAJ','reader',200],['gTRjAAAAcAAJ','download',403],
  ['jyq4gUPcJpwC','reader',200],['jyq4gUPcJpwC','download',403]
 ]);
 assert.ok(contract.digital_access_probes.every(x=>!x.pdf_directly_available&&!x.original_print_folio_visually_read));
 const l=contract.provenance_ledger;
 assert.equal(l.original_1573_Fabricius_book_folios_directly_read,0);
 assert.equal(l.original_1587_second_edition_book_folios_directly_read,0);
 assert.equal(l.original_1597_Coelestin_book_folios_directly_read,0);
 assert.deepEqual(l.cr27_1859_claim_supporting_pdf_pages_read_prior_v334,[70,73,74,75]);
 assert.equal(l.parallel_1573_vs_1859_original_latin_lemma_pairs,0);
 assert.equal(l.editorial_sigla_1859_fully_transcribed,0);
 assert.equal(l.public_reader_get_200_html_count,2);
 assert.equal(l.pdf_download_get_403_html_count,2);
 assert.equal(l.google_actions_probe_id,42321490328);
 assert.equal(l.google_pdf_download_blocked,true);
 assert.equal(l.first_latin_publication_1573_is_later_historian_claim,true);
 assert.ok(contract.warnings.some(x=>x.code==='1573_ORIGINAL_VS_1587_SECOND'));
 assert.ok(contract.warnings.some(x=>x.code==='BOOK_COMPOSITE_CONFUTATIO_VS_CONFESSION'));
 assert.ok(contract.warnings.some(x=>x.code==='COELESTIN_1597_AUTHENTICITY_WARNING'));
 assert.ok(contract.warnings.some(x=>x.code==='CR27_APPARATUS_NOT_EXHAUSTIVE'));
 assert.ok(contract.readings.every(x=>x.sections.length===3&&x.sections.every(z=>z.body.length>=170)));
 assert.equal(contract.metrics.original_corpus_changes,0);
 assert.equal(contract.metrics.paired_original_1573_1859_passages,0);
 return {sources:15,witnesses:8,relations:8,needed_loci:4,probe_results:4,warnings:10,readings:3,sections:9,gaps:10};
}
export function reviewOnly({contract}){
 const gate={version:'3.35',status:'DRAFT_HOLD',publication_ready:false,webapp_integrated:false,original_1573_print_pages_seen:0,first_1573_to_1859_word_pairs:0};
 return {
  'v335_1573_1587_edition_graph.json':{...gate,count:contract.witness_nodes.length,witnesses:contract.witness_nodes,relations:contract.typed_relations,sources:contract.source_records},
  'v335_fabricius_access_and_reading_provenance.json':{...gate,count:contract.digital_access_probes.length,probe_results:contract.digital_access_probes,scope:contract.provenance_ledger},
  'v335_1573_1859_original_print_comparison_queue.json':{...gate,count:contract.open_issues.length,issues:contract.open_issues,loci:contract.chapter_comparison_requests,warnings:contract.warnings}
 };
}
export function buildReview(){
 const input=loadInputs();validateV335(input);const data=reviewOnly(input);
 const dst=path.join(ROOT,'out','atlas-v335');mkdirSync(dst,{recursive:true});
 for(const [name,record] of Object.entries(data))writeFileSync(path.join(dst,name),JSON.stringify(record,null,2)+'\n');
 return data;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const o=buildReview();
 for(const [name,obj] of Object.entries(o))console.log(name+' '+obj.count+' REVIEW_ONLY');
}
