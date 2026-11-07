import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PARENT='data/contracts/atlas_v335_fabricius_1573_first_print_bibliography.json';
const CURRENT='data/contracts/atlas_v336_bornkamm_fabricius_two_text_stemma.json';
const read=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
export function loadStudy(){return {parent:read(PARENT),contract:read(CURRENT)}}
export function validateV336({parent,contract}){
 assert.equal(execFileSync('git',['hash-object',PARENT],{cwd:ROOT,encoding:'utf8'}).trim(),contract.parent.locked_parent_blob_sha,'V3.35 parent sha changed');
 assert.equal(parent.version,'3.35');assert.equal(contract.version,'3.36');
 assert.equal(contract.depth,'MEDIUM');assert.equal(contract.status,'DRAFT');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{readers:513,reader_sections:1539,source_records:723,overviews:97,curated_events:26,typed_relations:12,prior_v335_sources:15});
 assert.equal(contract.sources.length,19);
 assert.equal(contract.witness_nodes.length,11);
 assert.equal(contract.relations.length,10);
 assert.equal(contract.claim_cards.length,15);
 assert.equal(contract.readings.length,3);
 assert.equal(contract.readings.reduce((n,x)=>n+x.sections.length,0),9);
 assert.equal(contract.open_issues.length,10);
 assert.equal(contract.blocked_overclaims.length,12);
 assert.equal(contract.digital_latin_transcription_flags.length,3);
 const source=new Map(contract.sources.map(x=>[x.id,x]));
 const witnesses=new Map(contract.witness_nodes.map(x=>[x.id,x]));
 const links=new Map(contract.relations.map(x=>[x.id,x]));
 const cards=new Map(contract.claim_cards.map(x=>[x.id,x]));
 assert.equal(source.size,19);assert.equal(witnesses.size,11);
 assert.equal(links.size,10);assert.equal(cards.size,15);
 assert.ok(contract.sources.every(x=>x.original_1573_1577_1597_page_read===false));
 for(const witness of contract.witness_nodes)assert.equal(witness.original_sixteenth_century_folio_newly_seen,false);
 for(const link of contract.relations){
  assert.ok(witnesses.has(link.from)&&witnesses.has(link.to),'invalid stemma node');
  assert.ok(link.source_ids.length>0&&link.source_ids.every(x=>source.has(x)),'unknown relation source');
  assert.equal(link.direct_1573_print_sentence_pair_proven,false);
 }
 for(const claim of contract.claim_cards){
  assert.ok(claim.source_ids.length>0&&claim.source_ids.every(x=>source.has(x)),'unknown claim source');
  assert.equal(claim.historian_approved,false);
  assert.equal(claim.original_1573_internal_folio_read,false);
 }
 assert.equal(witnesses.get('V336-N05').name,'FABRICIUS_PRINTED_AUGUSTANA');
 assert.equal(witnesses.get('V336-N05').document_domain,'CONFESSION_IN_EDITORIAL_COLLECTION');
 assert.equal(witnesses.get('V336-N06').document_domain,'CATHOLIC_REBUTTAL_DISTINCT_WORK');
 assert.equal(witnesses.get('V336-N07').year,1577);
 assert.equal(witnesses.get('V336-N09').year,1597);
 assert.equal(witnesses.get('V336-N10').year,1858);
 assert.equal(witnesses.get('V336-N10').name,'CR26_LATIN_AUGUSTANA_COLLATION_1858');
 assert.equal(witnesses.get('V336-N11').year,1859);
 assert.equal(witnesses.get('V336-N11').name,'CR27_LATIN_CONFUTATIO_CRITICAL_TEXT');
 assert.equal(links.get('V336-L05').type,'REPRINT_OF_FABRICIUS_CONFESSION_TEXT');
 assert.equal(links.get('V336-L05').to,'V336-N07');
 assert.equal(links.get('V336-L06').type,'BIBLIOGRAPHIC_FIRST_FULL_LATIN_CONFUTATIO_PUBLICATION');
 assert.equal(links.get('V336-L07').type,'CR26_CONFESSION_COLLATION_REFERENCE');
 assert.ok(links.get('V336-L07').claim.includes('1858'));
 assert.equal(links.get('V336-L07').to,'V336-N10');
 assert.equal(links.get('V336-L10').type,'SAME_VOLUME_DIFFERENT_WORKS');
 assert.equal(links.get('V336-L10').from,'V336-N05');
 assert.equal(links.get('V336-L10').to,'V336-N06');
 assert.ok(cards.get('V336-C07').claim.includes('1577'));
 assert.ok(cards.get('V336-C08').claim.includes('CR26'));
 assert.ok(cards.get('V336-C13').claim.includes('1858'));
 assert.ok(cards.get('V336-C14').claim.includes('not direct images'));
 assert.ok(cards.get('V336-C15').claim.includes('without page image'));
 assert.equal(source.get('V336-S15').grade,'UNIVERSITY_LIBRARY_CR26_AND_CR27_DATE_RECORD');
 assert.equal(source.get('V336-S16').grade,'WEB_EDITORIAL_TRANSCRIPTION_CR26_WITH_EXACT_SOURCE');
 assert.equal(source.get('V336-S17').grade,'DERIVATIVE_EDITORIAL_LATIN_WEB_TEXT');
 const f=contract.digital_latin_transcription_flags;
 assert.deepEqual(f.map(x=>x.article),['IV','VII','VIII']);
 assert.deepEqual(f.map(x=>x.transcribed),['gratis iustificenter','consentiere','malii / sentibant']);
 assert.deepEqual(f.map(x=>x.comparator),['gratis iustificentur','consentire','mali / sentiebant']);
 assert.ok(f.every(x=>x.original_1858_print_checked===false&&x.status==='ONLINE_TRANSCRIPTION_POSSIBLE_ERROR_OR_VARIANT_UNCOLLATED'));
 assert.ok(contract.readings.every(x=>x.sections.length===3 && x.sections.every(y=>y.body.length>150)));
 const e=contract.evidence_ledger;
 assert.deepEqual(e.bornkamm_modern_print_pages_visually_seen,[10,14,15]);
 assert.deepEqual(e.bornkamm_pdf_pagenos_zero_based,[11,15,16]);
 assert.equal(e.original_Fabricius_1573_book_interior_pages_read,0);
 assert.equal(e.original_Coelestin_1577_pages_read,0);
 assert.equal(e.original_Coelestin_1597_pages_read,0);
 assert.equal(e.CR26_1858_original_print_folios_read,0);
 assert.equal(e.CR26_1858_online_transcription_article_pages_read,3);
 assert.equal(e.CR26_1858_vs_online_transcription_pairs_collated,0);
 assert.deepEqual(e.CR27_1859_original_confutatio_pages_prior_V334,[70,73,74,75]);
 assert.equal(e.direct_original_1573_vs_1859_sentence_pairs,0);
 assert.equal(contract.metrics.original_corpus_changes,0);
 assert.equal(contract.metrics.new_original_1573_folios,0);
 assert.equal(contract.metrics.digital_web_transcription_flags,3);
 assert.ok(contract.blocked_overclaims.some(x=>x.includes('Do not label CR XXVI as printed in 1859')));
 assert.ok(contract.blocked_overclaims.some(x=>x.includes('Do not mistake independent Fabricius')));
 return {sources:19,edition_and_manuscript_nodes:11,relations:10,claims:15,readings:3,sections:9,web_transcription_flags:3,open_issues:10};
}
export function reviewOnly({contract}){
 const base={version:'3.36',status:'RESEARCH_DRAFT_HOLD',published:false,webapp_integrated:false,first_1573_interior_print_folios_seen:0};
 return {
  'v336_two_text_augustana_confutatio_stemma.json':{...base,count:contract.witness_nodes.length,witness_nodes:contract.witness_nodes,relations:contract.relations,sources:contract.sources},
  'v336_bornkamm_source_grade_claims.json':{...base,count:contract.claim_cards.length,claims:contract.claim_cards,ledger:contract.evidence_ledger},
  'v336_cr26_1858_web_transcription_followups.json':{...base,count:contract.open_issues.length,issues:contract.open_issues,transcription_flags:contract.digital_latin_transcription_flags,overclaims:contract.blocked_overclaims}
 };
}
export function build(){
 const data=loadStudy();validateV336(data);const out=reviewOnly(data);
 const dst=path.join(ROOT,'out','atlas-v336');mkdirSync(dst,{recursive:true});
 for(const [filename,obj] of Object.entries(out))writeFileSync(path.join(dst,filename),JSON.stringify(obj,null,2)+'\n');
 return out;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 for(const [name,obj] of Object.entries(build()))console.log(name+' '+obj.count+' REVIEW_ONLY');
}
