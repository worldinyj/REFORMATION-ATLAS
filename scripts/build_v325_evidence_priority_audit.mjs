import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const load=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
const parentPath='data/contracts/atlas_v324_typed_influence_response_reception_graph.json';
const auditPath='data/contracts/atlas_v325_evidence_strength_priority_audit.json';

export function loadAudit() { return {parent:load(parentPath),audit:load(auditPath)}; }
export function validateAudit({parent,audit}) {
 const actual=execFileSync('git',['hash-object',parentPath],{cwd:ROOT,encoding:'utf8'}).trim();
 assert.equal(actual,audit.parent.locked_parent_contract_blob_sha,'V3.24 historical relation contract changed');
 assert.equal(audit.version,'3.25');
 assert.equal(audit.status,'DRAFT');
 assert.equal(audit.depth,'MEDIUM');
 assert.deepEqual(audit.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(audit.inheritance,{
  original_reader_count:513, original_section_count:1539, original_source_records:723,
  overview_records:97,original_selected_claims:22,curated_historical_events:26,
  overview_reader_links:156,parent_relation_count:12,parent_unresolved_count:6
 });
 const relations=new Map(parent.typed_relations.map(x=>[x.id,x]));
 const issues=new Map(parent.open_issues.map(x=>[x.id,x]));
 const sourceIds=new Set(parent.evidence_sources.map(x=>x.id));
 assert.equal(relations.size,12);
 assert.equal(audit.assessments.length,12);
 assert.equal(new Set(audit.assessments.map(a=>a.relation_id)).size,12);
 const allowedBands=new Set(Object.keys(audit.grading_scale));
 for(const a of audit.assessments) {
  const original=relations.get(a.relation_id);
  assert.ok(original,'unknown historic relation '+a.relation_id);
  assert.equal(a.relation_type,original.type,'historic relation changed '+a.relation_id);
  assert.deepEqual(a.source_ids,original.source_ids,'historic source changed '+a.relation_id);
  assert.ok(allowedBands.has(a.evidence_band),'undefined evidence band '+a.evidence_band);
  assert.ok(['P0','P1','P2'].includes(a.editorial_priority));
  if(a.linked_issue_id!==null)assert.ok(issues.has(a.linked_issue_id));
  assert.ok(a.claim_scope.length>15);
  assert.equal(a.verified_original_print_pair,false);
  assert.equal(a.allowed_as_unqualified_primary_source_proof,false);
  assert.equal(a.app_publication_approved,false);
  assert.equal(a.historical_confidence_not_numeric,true);
  assert.ok(a.source_ids.length>0&&a.source_ids.every(id=>sourceIds.has(id)));
 }
 assert.equal(audit.priority_queue.length,6);
 assert.equal(new Set(audit.priority_queue.map(x=>x.issue_id)).size,6);
 for(const q of audit.priority_queue) {
  const orig=issues.get(q.issue_id);
  assert.ok(orig,'unknown issue '+q.issue_id);
  assert.equal(q.topic,orig.topic);
  assert.equal(q.original_status,orig.status);
  assert.deepEqual(q.inherited_source_ids,orig.sources);
  assert.equal(q.verification_required,orig.next);
  for(const part of ['impact','evidence_gap','reader_exposure'])assert.ok(Number.isInteger(q[part])&&q[part]>=1&&q[part]<=3);
  assert.equal(q.triage_score,2*q.impact+q.evidence_gap+q.reader_exposure);
  assert.equal(q.priority,q.triage_score>=10?'P0':q.triage_score>=8?'P1':'P2');
  assert.equal(q.expert_reviewed,false);
  assert.match(q.metric_disclaimer,/not scientific probability/);
 }
 assert.deepEqual(audit.priority_queue.map(x=>x.issue_id),[...audit.priority_queue].sort((a,b)=>b.triage_score-a.triage_score||a.issue_id.localeCompare(b.issue_id)).map(x=>x.issue_id));
 const high=audit.priority_queue.filter(x=>x.priority==='P0');
 const medium=audit.priority_queue.filter(x=>x.priority==='P1');
 assert.equal(high.length,3);
 assert.equal(medium.length,3);
 assert.deepEqual(new Set(high.map(x=>x.issue_id)),new Set(['V324-ISS01','V324-ISS02','V324-ISS06']));
 assert.equal(audit.metrics.high_urgency_issues,3);
 assert.equal(audit.metrics.medium_urgency_issues,3);
 assert.equal(audit.metrics.relations_assessed,12);
 const methodistIds=new Set(audit.methodist_source_records.map(x=>x.id));
 assert.equal(methodistIds.size,6);
 assert.equal(audit.methodist_stage_records.length,5);
 for(const s of audit.methodist_stage_records) {
  assert.ok(s.source_ids.every(id=>methodistIds.has(id)),'missing Methodist source');
  assert.equal(s.direct_contemporary_witness,false);
  assert.ok(['YEAR','MONTH','DAY'].includes(s.date_precision));
  assert.equal(s.date_precision,s.date.length===4?'YEAR':s.date.length===7?'MONTH':'DAY');
 }
 const stage=id=>audit.methodist_stage_records.find(x=>x.id===id);
 assert.equal(stage('V325-M03').date,'1784-12');
 assert.equal(stage('V325-M03').event_role,'CHRISTMAS_CONFERENCE_ADOPTION_ORGANIZATION');
 assert.equal(stage('V325-M04').date,'1785');
 assert.equal(stage('V325-M04').event_role,'FIRST_AMERICAN_DISCIPLINE_PRINT_IMPRINT_YEAR');
 assert.equal(stage('V325-M05').event_role,'LATER_GLOSSARY_APPROVAL_TERM_UNRESOLVED');
 assert.equal(stage('V325-M05').public_copy_allowed,null,'never publish unverified second approval');
 assert.equal(audit.reader_display_policy.approved_for_public_app,false);
 assert.equal(audit.metrics.new_original_print_pages_visually_inspected,0);
 assert.equal(audit.metrics.physical_page_collations,0);
 assert.equal(audit.readings.length,2);
 assert.equal(audit.readings.reduce((n,r)=>n+r.sections.length,0),6);
 assert.equal(parent.metrics.new_typed_relations,12);
 return {relations:relations.size,issues:issues.size,high:high.length,medium:medium.length};
}
export function reviewOutputs(inputs) {
 const {audit}=inputs;
 return {
  'v325_relation_evidence_matrix.json':{
   schema:'ATLAS_V325_RELATION_EVIDENCE_REVIEW',version:'3.25',publication_ready:false,
   count:audit.assessments.length,criteria:audit.grading_scale,items:audit.assessments
  },
  'v325_ordered_source_research_queue.json':{
   schema:'ATLAS_V325_ISSUE_PRIORITIES',version:'3.25',publication_ready:false,
   count:audit.priority_queue.length,method:audit.triage_scoring,items:audit.priority_queue
  },
  'v325_methodist_chronology_distinctions.json':{
   schema:'ATLAS_V325_METHODIST_DATES',version:'3.25',publication_ready:false,
   count:audit.methodist_stage_records.length,sources:audit.methodist_source_records,
   stages:audit.methodist_stage_records,public_display:audit.reader_display_policy
  }
 };
}
export function writeReviewOnly() {
 const input=loadAudit();
 validateAudit(input);
 const output=reviewOutputs(input);
 const dest=path.join(ROOT,'out','atlas-v325');
 mkdirSync(dest,{recursive:true});
 for(const [name,item] of Object.entries(output))writeFileSync(path.join(dest,name),JSON.stringify(item,null,2)+'\n');
 return output;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const outputs=writeReviewOnly();
 for(const [name,d] of Object.entries(outputs))console.log(name+': '+d.count+' REVIEW ONLY');
}
