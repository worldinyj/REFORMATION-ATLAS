import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const parentPath='data/contracts/atlas_v329_general_rules_1788_annex_correction.json';
const currentPath='data/contracts/atlas_v330_1788_1789_general_rules_integration_review.json';
const parse=p=>JSON.parse(readFileSync(path.join(root,p),'utf8'));
export function loadResearch(){return {parent:parse(parentPath),contract:parse(currentPath)}}

export function validateV330({parent,contract}){
 const blob=execFileSync('git',['hash-object',parentPath],{cwd:root,encoding:'utf8'}).trim();
 assert.equal(blob,contract.parent.locked_parent_blob_sha,'V3.29 contract changed');
 assert.equal(parent.version,'3.29');
 assert.equal(contract.version,'3.30');
 assert.equal(contract.depth,'MEDIUM');
 assert.equal(contract.status,'DRAFT');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{
  readers:513,sections:1539,original_source_records:723,overviews:97,curated_events:26,
  original_typed_relations:12,v329_correction_cards:4,v329_witness_nodes:7
 });
 assert.equal(contract.sources.length,11);
 assert.equal(contract.document_nodes.length,7);
 assert.equal(contract.typed_relations.length,7);
 assert.equal(contract.claim_cards.length,14);
 assert.equal(contract.upgrades.length,4);
 assert.equal(contract.readings.length,3);
 assert.equal(contract.readings.reduce((sum,r)=>sum+r.sections.length,0),9);
 assert.equal(contract.unresolved.length,9);
 const sources=new Map(contract.sources.map(s=>[s.id,s]));
 const nodes=new Map(contract.document_nodes.map(n=>[n.id,n]));
 const links=new Map(contract.typed_relations.map(l=>[l.id,l]));
 assert.equal(sources.size,11);
 assert.equal(nodes.size,7);
 assert.equal(links.size,7);
 for(const edge of contract.typed_relations){
  assert.ok(nodes.has(edge.from)&&nodes.has(edge.to),'relation source or target missing '+edge.id);
  assert.ok(edge.source_ids.length>=1&&edge.source_ids.every(x=>sources.has(x)),'relation lacks known source '+edge.id);
  assert.equal(edge.direct_folio_comparison,false);
  assert.equal(edge.original_print_1788_1789_directly_seen,false);
  assert.ok(edge.claim.length>40);
 }
 for(const c of contract.claim_cards){
  assert.ok(c.source_ids.length>=1&&c.source_ids.every(id=>sources.has(id)),'invalid claim source '+c.id);
  assert.equal(c.first_print_direct_visual,false);
  assert.equal(c.approved_for_publication,false);
 }
 assert.equal(links.get('V330-L02').type,'ANNEX_TO_MAIN_BODY_REPOSITION');
 assert.equal(links.get('V330-L02').from,'V330-N03');
 assert.equal(links.get('V330-L02').to,'V330-N04');
 assert.deepEqual(links.get('V330-L02').source_ids,['V330-S01','V330-S03']);
 assert.equal(links.get('V330-L03').type,'OTHER_TRACTS_BECAME_NUMBERED_SECTIONS');
 assert.equal(links.get('V330-L03').to,'V330-N05');
 assert.equal(nodes.get('V330-N03').year,1788);
 assert.equal(nodes.get('V330-N03').status,'FIRST_KNOWN_ATTESTED_1788_ANNEX_NOT_FIRST_EVER');
 assert.equal(nodes.get('V330-N04').year,1789);
 assert.equal(nodes.get('V330-N04').status,'SCHOLARLY_CONFIRMED_GENERAL_RULES_MAIN_BODY_RELOCATION');
 assert.equal(nodes.get('V330-N05').year,1790);
 assert.equal(contract.upgrades.find(c=>c.id==='V330-REV01').new_status,'DOCUMENTED_BY_ACADEMIC_HISTORIAN_SECONDARY_NO_ORIGINAL_SCAN');
 assert.equal(contract.upgrades.find(c=>c.id==='V330-REV02').new_status,'CLARIFIED_OTHER_DOCTRINAL_TRACTS');
 assert.equal(sources.get('V330-S01').tier,'ACADEMIC_HISTORIAN_ARTICLE_PDF_TEXT');
 assert.equal(sources.get('V330-S06').journal_pages_visually_verified,true);
 assert.ok(contract.claim_cards.find(x=>x.id==='V330-C08').claim.includes('1788 printed Discipline p41'));
 assert.ok(contract.claim_cards.find(x=>x.id==='V330-C10').level==='UNCOLLATED_TRANSCRIPTION');
 assert.ok(contract.blocked_overclaims.some(s=>s==='1789 was first American publication of General Rules'));
 assert.ok(contract.blocked_overclaims.some(s=>s==='1790 was first year General Rules moved inside main body'));
 const w=contract.witness_ledger;
 assert.equal(w.scholarly_1997_print_pages_visually_inspected,2);
 assert.deepEqual(w.scholarly_Baker_PDF_text_read_pages,[47,48,49]);
 assert.equal(w.scholarly_Baker_exact_PDF_page_screenshots_read,0);
 assert.equal(w.scholarly_Baker_PDF_page_screenshot_error,'HTTP_403');
 assert.equal(w.original_1788_appendix_page_visually_inspected,0);
 assert.equal(w.original_1789_rules_main_body_page_visually_inspected,0);
 assert.equal(w.original_1788_1992_reprint_page41_visually_inspected,0);
 assert.equal(w.aligned_1788_1789_original_print_page_pairs,0);
 assert.equal(contract.metrics.original_513_reader_mutations,0);
 assert.equal(contract.metrics.full_original_same_sentence_pairs,0);
 assert.equal(contract.metrics.open_issues,9);
 assert.ok(contract.unresolved.some(x=>x.id==='V330-I02'&&x.priority==='P0'));
 assert.ok(contract.unresolved.some(x=>x.id==='V330-I03'&&x.priority==='P0'));
 return {sources:11,nodes:7,links:7,claims:14,upgrades:4,readings:3,sections:9,issues:9};
}

export function reviewOnly({contract}){
 const header={version:'3.30',status:'RESEARCH_DRAFT_HOLD',publication_ready:false,
  google_ai_studio_webapp_integrated:false,direct_1788_1789_original_print_pairs:0};
 return {
  'v330_1788_1789_edition_relocation_graph.json':{...header,count:contract.typed_relations.length,links:contract.typed_relations,nodes:contract.document_nodes},
  'v330_claim_source_provenance.json':{...header,count:contract.claim_cards.length,claims:contract.claim_cards,sources:contract.sources},
  'v330_original_pages_to_inspect.json':{...header,count:contract.unresolved.length,issues:contract.unresolved,witness_ledger:contract.witness_ledger}
 };
}
export function buildReviewOnly(){
 const loaded=loadResearch();validateV330(loaded);const outputs=reviewOnly(loaded);
 const dest=path.join(root,'out','atlas-v330');mkdirSync(dest,{recursive:true});
 for(const [filename,record] of Object.entries(outputs))
  writeFileSync(path.join(dest,filename),JSON.stringify(record,null,2)+'\n');
 return outputs;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const o=buildReviewOnly();
 for(const [name,data] of Object.entries(o))console.log(name+': '+data.count+' REVIEW_ONLY');
}
