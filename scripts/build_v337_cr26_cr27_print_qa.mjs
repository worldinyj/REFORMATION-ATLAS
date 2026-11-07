import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PARENT='data/contracts/atlas_v336_bornkamm_fabricius_two_text_stemma.json';
const CURRENT='data/contracts/atlas_v337_cr26_latin_original_print_vs_web_transcription.json';
const REPORT='docs/02_RESEARCH/V337_CR26_1858_ORIGINAL_PRINT_VS_LATIN_TRANSCRIPTION_AUDIT.md';
const read=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
export function loadInputs(){return {parent:read(PARENT),contract:read(CURRENT)}}
export function verifyV337({parent,contract}){
 assert.equal(execFileSync('git',['hash-object',PARENT],{cwd:ROOT,encoding:'utf8'}).trim(),contract.parent.locked_parent_blob_sha,'V3.36 parent blob MUST remain unchanged');
 assert.equal(parent.version,'3.36');assert.equal(contract.version,'3.37');
 assert.equal(contract.status,'DRAFT');assert.equal(contract.depth,'MEDIUM');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{readers:513,sections:1539,sources:723,overviews:97,events:26,relations:12});
 assert.equal(contract.sources.length,10);
 assert.equal(contract.print_page_map_cr26.length,7);
 assert.equal(contract.print_column_map_cr27.length,4);
 assert.equal(contract.online_latin_qa.length,4);
 assert.equal(contract.edition_apparatus_notes.length,6);
 assert.equal(contract.readings.length,3);
 assert.equal(contract.readings.reduce((n,x)=>n+x.sections.length,0),9);
 assert.equal(contract.open_issues.length,7);
 assert.equal(contract.metrics.original_corpus_mutations,0);
 const p=contract.print_provenance;
 assert.equal(p.cr26.year,1858);assert.equal(p.cr26.work,'CONFESSIO_AUGUSTANA');
 assert.equal(p.cr26.pdf_page_count,420);
 assert.equal(p.cr26.sha256,'55832391489b20ee3cf6b64a318d234a28716eb830069c9eed604b004c1a7827');
 assert.equal(p.cr27.year,1859);assert.equal(p.cr27.work,'ROMAN_CONFUTATIO');
 assert.equal(p.cr27.pdf_page_count,360);
 assert.equal(p.cr27.sha256,'ba1995d5587375a13f5298001e7a6c42d68f1c6b161ae86335471a1c4f30b29d');
 assert.equal(p.source_archive_run,42368740203);
 assert.equal(p.archived_images,'atlas-v337-cr26-1858-vs-cr27-1859-original-folio-images');
 const source=new Map(contract.sources.map(x=>[x.id,x]));
 assert.equal(source.size,10);
 assert.ok(contract.sources.every(x=>x.first_1573_folio_seen===false));
 for(const x of contract.print_page_map_cr26){
  assert.equal(x.right_printed_page,x.left_printed_page+1);
  assert.equal(x.left_printed_page,2*x.pdf_page-49);
  assert.equal(x.viewed,true);
 }
 for(const x of contract.print_column_map_cr27){
  assert.equal(x.right_printed_column,x.left_printed_column+1);
  assert.equal(x.left_printed_column,2*x.pdf_page-45);
  assert.equal(x.viewed,true);
 }
 assert.deepEqual(contract.print_page_map_cr26.slice(0,5).map(x=>[x.pdf_page,x.left_printed_page]),[[137,225],[156,263],[161,273],[162,275],[163,277]]);
 assert.deepEqual(contract.print_column_map_cr27.map(x=>[x.pdf_page,x.left_printed_column]),[[70,95],[73,101],[74,103],[75,105]]);
 assert.deepEqual(contract.online_latin_qa.map(x=>[x.article,x.online,x.printed,x.book_page,x.pdf_page]),[
  ['IV','iustificenter','iustificentur',275,162],
  ['VII','consentiere','consentire',277,163],
  ['VIII','malii','mali',277,163],
  ['VIII','sentibant','sentiebant',277,163]
 ]);
 for(const c of contract.online_latin_qa){
  assert.equal(c.type,'ONLINE_LATIN_DIFFERS_FROM_PHYSICAL_1858_PRINT');
  assert.equal(c.original_1530_manuscript_checked,false);
  assert.ok(c.source_ids.every(x=>source.has(x)));
 }
 const notes=new Map(contract.edition_apparatus_notes.map(x=>[x.id,x]));
 assert.equal(notes.size,6);
 assert.equal(notes.get('V337-N1').type,'BIBLIOGRAPHY');
 assert.equal(notes.get('V337-N2').type,'SIGLA');
 assert.equal(notes.get('V337-N5').type,'ARTICLE_VII_NOTE40');
 assert.equal(notes.get('V337-N5').volume,27);
 assert.equal(notes.get('V337-N5').printed_location,103);
 assert.equal(notes.get('V337-N6').printed_location,105);
 assert.ok(notes.get('V337-N6').evidence.includes('Fabr.'));
 assert.ok(contract.edition_apparatus_notes.every(x=>x.modern_editor_report_directly_seen&&x.original_1573_folio_read===false));
 const w=contract.witness_ledger;
 assert.deepEqual(w.cr26_claim_supporting_pdf_pages,[137,156,161,162,163]);
 assert.deepEqual(w.cr27_reinspected_pdf_pages,[70,73,74,75]);
 assert.equal(w.online_word_discrepancies_reconciled,4);
 assert.deepEqual(w.cr27_reported_fabricius_footnote_cols,[103,105]);
 assert.equal(w.all_manuscript_variants_verified,false);
 assert.equal(w.fabricius1573_original_interior_pages,0);
 assert.equal(w.confessio1530_original_manuscript_pages,0);
 assert.equal(w.confutatio1530_original_german_pages,0);
 assert.equal(w.paired1573_v1859_latin_texts,0);
 assert.ok(contract.readings.every(x=>x.sections.length===3&&x.sections.every(y=>y.body.length>=180)));
 const text=readFileSync(path.join(ROOT,REPORT),'utf8');
 for(const s of ['iustificentur','consentire','sentiebant','mali','Fabr.','1573','1858','1859','출판 HOLD'])assert.ok(text.includes(s),'report lacks '+s);
 assert.equal(contract.metrics.online_corrections,4);
 assert.equal(contract.metrics.apparatus_notes,6);
 assert.equal(contract.metrics.original_corpus_mutations,0);
 return {sources:10,cr26_pages:7,cr27_pages:4,online_corrections:4,editorial_notes:6,essays:3,sections:9,open_issues:7};
}
export function reviewOnly({contract}){
 const gate={version:'3.37',status:'RESEARCH_DRAFT_HOLD',published:false,webapp_updated:false,original_1573_pages_seen:0,direct_1573_to_1859_original_pairs:0};
 return {
  'v337_cr26_cr27_original_print_page_map.json':{...gate,count:contract.print_page_map_cr26.length+contract.print_column_map_cr27.length,cr26:contract.print_page_map_cr26,cr27:contract.print_column_map_cr27,prints:contract.print_provenance},
  'v337_online_latin_transcription_errata.json':{...gate,count:contract.online_latin_qa.length,corrections:contract.online_latin_qa,sources:contract.sources},
  'v337_editorial_variant_source_grade.json':{...gate,count:contract.edition_apparatus_notes.length,notes:contract.edition_apparatus_notes,ledger:contract.witness_ledger,issues:contract.open_issues}
 };
}
export function build(){
 const data=loadInputs();verifyV337(data);const out=reviewOnly(data);
 const dest=path.join(ROOT,'out','atlas-v337');mkdirSync(dest,{recursive:true});
 for(const [name,obj] of Object.entries(out))writeFileSync(path.join(dest,name),JSON.stringify(obj,null,2)+'\n');
 return out;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 for(const [name,obj] of Object.entries(build()))console.log(name+' '+obj.count+' DRAFT_RESEARCH_ONLY');
}
