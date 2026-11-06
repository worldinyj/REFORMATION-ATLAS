import assert from 'node:assert/strict';
import {readFileSync, mkdirSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const load = p => JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
const CONTRACT = 'data/contracts/atlas_v324_typed_influence_response_reception_graph.json';
const GRAPH = 'data/contracts/atlas_v323_curated_chronology_navigation_graph.json';
const READERS = 'data/deep/atlas_v307_remaining_overview_medium_readers.json';

export function loadInputs() {
 return {contract:load(CONTRACT),graph:load(GRAPH),readers:load(READERS)};
}
export function validateRelationOverlay({contract,graph,readers}) {
 const frozen = new Map(contract.frozen_inputs.map(f=>[f.path,f.blob_sha]));
 for(const [rel,expected] of frozen) {
  const sha = execFileSync('git',['hash-object',rel],{cwd:ROOT,encoding:'utf8'}).trim();
  assert.equal(sha,expected,'frozen upstream mismatch: '+rel);
 }
 assert.equal(contract.version,'3.24');
 assert.equal(contract.depth,'MEDIUM');
 assert.equal(contract.status,'DRAFT');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserved_original_corpus,{
  readers:513,reader_sections:1539,source_records:723,overviews:97,selected_claims:22,curated_events:26,overview_reader_edges:156,witness_nodes:10
 });
 assert.equal(readers.catalogue.length,513);
 assert.equal(graph.events.length,26);
 assert.equal(graph.document_witnesses.length,10);
 assert.equal(contract.typed_relations.length,12);
 assert.equal(contract.evidence_sources.length,14);
 assert.equal(contract.external_historical_documents.length,1);
 assert.equal(contract.readings.length,4);
 assert.equal(contract.readings.reduce((n,r)=>n+r.sections.length,0),12);
 assert.equal(contract.open_issues.length,6);
 assert.equal(contract.blocked_relationship_templates.length,6);
 const refs={
  reader:new Map(readers.catalogue.map(x=>[x.id,x.title])),
  event:new Map(graph.events.map(x=>[x.id,x.title||x.label||x.description||x.id])),
  witness:new Map(graph.document_witnesses.map(x=>[x.id,x.type+' ('+x.year+')'])),
  historical_document:new Map(contract.external_historical_documents.map(x=>[x.id,x.title]))
 };
 const sourceMap=new Map(contract.evidence_sources.map(x=>[x.id,x]));
 assert.equal(sourceMap.size,contract.evidence_sources.length);
 const relIds=new Set();
 const uniqueTriples=new Set();
 const acceptableTypes=new Set([
  'DOCUMENTED_INTELLECTUAL_INFLUENCE','FORMAL_CONFUTATION_OF','APOLOGETIC_REBUTTAL_OF',
  'DEFENSE_OF_CONFESSIONAL_DOCUMENT','AUTHORIAL_EDITION_REVISION','REPORTED_STRUCTURAL_INFLUENCE',
  'INSTITUTIONAL_FOLLOW_UP_PUBLICATION','DOCUMENT_AUTHORSHIP','FORMATION_TO_PRINT_PUBLICATION',
  'TREATY_RATIFICATION_PROCEDURE','PRINT_PRIVILEGE_REPRODUCED_IN_LATER_EDITION'
 ]);
 const resolved=contract.typed_relations.map(edge=>{
  assert.ok(!relIds.has(edge.id),'duplicate relation id '+edge.id);relIds.add(edge.id);
  assert.ok(acceptableTypes.has(edge.type),'unknown relation type '+edge.type);
  const fromName=refs[edge.from.kind]?.get(edge.from.id);
  const toName=refs[edge.to.kind]?.get(edge.to.id);
  assert.ok(fromName,'dangling from ref '+edge.id+' '+edge.from.id);
  assert.ok(toName,'dangling to ref '+edge.id+' '+edge.to.id);
  assert.ok(!(edge.from.kind===edge.to.kind && edge.from.id===edge.to.id),'self loop');
  assert.ok(edge.source_ids.length>0 && edge.source_ids.every(id=>sourceMap.has(id)),'source not found '+edge.id);
  assert.equal(edge.original_witness_pair_collated,false);
  assert.equal(edge.causation_inferred_from_time_only,false);
  assert.equal(edge.expert_approved,false);
  assert.ok(edge.claim.length>15);
  assert.ok(edge.limits.length>15);
  const signature=[edge.type,edge.from.kind,edge.from.id,edge.to.kind,edge.to.id].join('|');
  assert.ok(!uniqueTriples.has(signature),'duplicate typed edge');uniqueTriples.add(signature);
  return {
   id:edge.id,type:edge.type,
   from:{...edge.from,label:fromName},
   to:{...edge.to,label:toName},
   confidence:edge.confidence,
   source_ids:edge.source_ids,
   claim:edge.claim,limits:edge.limits,
   is_publication_approved:false,
   direct_original_witness_pair:false
  };
 });
 const index=id=>contract.typed_relations.find(x=>x.id===id);
 assert.deepEqual(index('V324-R02').to,{kind:'witness',id:'V323-W01'});
 assert.deepEqual(index('V324-R03').to,{kind:'historical_document',id:'V324-DOC-CONFUTATIO1530'});
 assert.deepEqual(index('V324-R04').to,{kind:'witness',id:'V323-W01'});
 assert.deepEqual(index('V324-R05').from,{kind:'witness',id:'V323-W02'});
 assert.deepEqual(index('V324-R05').to,{kind:'witness',id:'V323-W03'});
 assert.deepEqual(index('V324-R06').from,{kind:'witness',id:'V323-W04'});
 assert.deepEqual(index('V324-R06').to,{kind:'witness',id:'V323-W05'});
 assert.deepEqual(index('V324-R08').to,{kind:'reader',id:'DOCUMENT-ROMAN_CATECHISM'});
 assert.deepEqual(index('V324-R10').from,{kind:'event',id:'V323-E23'});
 assert.deepEqual(index('V324-R10').to,{kind:'event',id:'V323-E25'});
 assert.deepEqual(index('V324-R11').from,{kind:'event',id:'V323-E17'});
 assert.deepEqual(index('V324-R11').to,{kind:'event',id:'V323-E19'});
 assert.deepEqual(index('V324-R12').from,{kind:'event',id:'V323-E16'});
 assert.deepEqual(index('V324-R12').to,{kind:'event',id:'V323-E21'});
 const issue=contract.open_issues.find(x=>x.id==='V324-ISS01');
 assert.ok(issue&&issue.status==='SOURCE_DESCRIPTIONS_DIVERGE');
 assert.ok(['SRC-UMC-GLOSSARY','SRC-UMC-DOCTRINE','SRC-UMC-FOUNDATIONS'].every(id=>issue.sources.includes(id)));
 assert.ok(!contract.typed_relations.some(e=>e.from.id==='V323-E26'||e.to.id==='V323-E26'),'1785 must remain context-only until source reconciliation');
 assert.ok(contract.blocked_relationship_templates.some(b=>b.pattern==='WESLEY_1785_FIRST_AND_ONLY_ADOPTION'));
 assert.ok(contract.blocked_relationship_templates.some(b=>b.pattern==='SAME_CITY_MUENSTER_MEANS_SAME_TREATY'));
 assert.equal(contract.metrics.original_print_pages_newly_inspected,0);
 assert.equal(contract.metrics.edition_print_page_pairs_collated,0);
 assert.equal(contract.metrics.historical_claims_expert_approved,0);
 return {resolved,sourceMap,refMaps:refs};
}
export function createReviewOutputs(inputs,verified) {
 const {contract,graph}=inputs;
 const shared={version:'3.24',publication_ready:false,research_only:true,parent_curated_event_count:graph.events.length,never_infer_causality_from_chronology:true};
 const overlays={...shared,count:verified.resolved.length,nodes:verified.resolved.flatMap(e=>[e.from,e.to]).filter((x,i,a)=>a.findIndex(y=>y.kind===x.kind&&y.id===x.id)===i),edges:verified.resolved};
 const issueIndex={...shared,count:contract.open_issues.length,issues:contract.open_issues};
 const readerRelated=verified.resolved.flatMap(edge=>[
  ...(edge.from.kind==='reader'?[{reader_id:edge.from.id,relation_id:edge.id,role:'FROM'}]:[]),
  ...(edge.to.kind==='reader'?[{reader_id:edge.to.id,relation_id:edge.id,role:'TO'}]:[])
 ]);
 const readerIndex={...shared,count:new Set(readerRelated.map(x=>x.reader_id)).size,links:readerRelated};
 return {
  'v324_typed_relation_overlay.json':overlays,
  'v324_reader_relation_lookup.json':readerIndex,
  'v324_open_source_conflicts.json':issueIndex
 };
}
export function buildReviewArtifacts() {
 const inputs=loadInputs();
 const validated=validateRelationOverlay(inputs);
 const outputs=createReviewOutputs(inputs,validated);
 const dest=path.join(ROOT,'out','atlas-v324');
 mkdirSync(dest,{recursive:true});
 for(const [filename,value] of Object.entries(outputs))writeFileSync(path.join(dest,filename),JSON.stringify(value,null,2)+'\n');
 return outputs;
}
if(process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const outputs=buildReviewArtifacts();
 for(const [filename,item] of Object.entries(outputs)) console.log(filename+' '+item.count+' REVIEW_ONLY');
}
