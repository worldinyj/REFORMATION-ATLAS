/**
 * REFORMATION ATLAS cross-volume review-bundle contract, research data only.
 * Import validation in any volume's research workflow. This is NOT a release permit.
 */
const unique=(arr)=>new Set(arr).size===arr.length;
const validId=x=>typeof x==="string"&&x.trim().length>0;
const hasKeys=(obj,keys)=>obj&&typeof obj==="object"&&keys.every(k=>Object.hasOwn(obj,k));
export function validateAtlasReviewBundle(b){
 const errors=[],bad=(message)=>errors.push(message);
 if(!b||typeof b!=="object")return {valid:false,errors:["invalid bundle"]};
 if(b.schema!=="ATLAS_REVIEW_BUNDLE_V1")bad("unsupported schema");
 if(b.stage!=="RESEARCH_ONLY")bad("stage cannot be promoted here");
 if(!hasKeys(b.identity,["volumeId","chapterId","sceneId"])||!["volumeId","chapterId","sceneId"].every(k=>validId(b.identity[k])))bad("missing scoped identity");
 for(const key of ["canShip","canMergeMain","canImportAIStudio","expertApproved","readerValidated","rightsApproved","hostAccessVerified"]){
  if(b.releaseGate?.[key]!==false)bad("fail-closed release gate "+key);
 }
 const sources=Array.isArray(b.sources)?b.sources:[],events=Array.isArray(b.timeline)?b.timeline:[],layers=Array.isArray(b.layers)?b.layers:[];
 const sourceIds=sources.map(s=>s.id),eventIds=events.map(e=>e.id);
 if(!sources.length||!unique(sourceIds))bad("sources nonempty and unique");
 if(!events.length||!unique(eventIds))bad("events nonempty and unique");
 if(layers.length!==2||!unique(layers.map(l=>l.level))||!["L0","L1"].every(l=>layers.some(x=>x.level===l)))bad("two distinct L0/L1 layers required");
 for(const s of sources){
  if(!validId(s.id)||typeof s.url!=="string"||!/^https:\/\/[^\s]+$/.test(s.url))bad("invalid source URL "+s.id);
  if(!validId(s.sourceKind)||!validId(s.sourceLimit))bad("source typology and limitation absent "+s.id);
  if(!Array.isArray(s.eventIds)||s.eventIds.some(id=>!eventIds.includes(id)))bad("source uses undefined event "+s.id);
 }
 for(const e of events){
  if(!validId(e.id)||!Number.isInteger(e.year)||!validId(e.claimLimit)||!Array.isArray(e.sourceRefs)||e.sourceRefs.some(id=>!sourceIds.includes(id)))bad("event source/limitation missing "+e.id);
 }
 for(const l of layers){
  if(!validId(l.title)||!validId(l.markdown)||l.markdown.length<25)bad("empty layer");
  if(!Array.isArray(l.sourceRefs)||!l.sourceRefs.length||l.sourceRefs.some(id=>!sourceIds.includes(id)))bad("invalid layer source reference "+l.level);
  const tags=[...String(l.markdown||"").matchAll(/\[([A-Z]{2,10})\]/g)].map(x=>x[1]);
  if(tags.some(id=>!sourceIds.includes(id)))bad("unresolved Markdown evidence ID "+l.level);
 }
 if(!Array.isArray(b.comparisons)||b.comparisons.some(c=>!sourceIds.includes(c.sourceId)||c.originalAutographChecked!==false||!validId(c.limitation)))bad("witness comparison needs source and explicit unverified state");
 const claims=b.expertReview?.claims;
 if(!Array.isArray(claims)||!claims.length||!unique(claims.map(c=>c.id))||b.expertReview.claimCount!==claims.length)bad("invalid expert claims");
 else for(const c of claims){
  if(!validId(c.statement)||!["LOW","MEDIUM","HIGH"].includes(c.risk)||c.expertApproved!==false||c.decision!=="PENDING"||c.reviewer1!==null||c.reviewer2!==null)bad("unapproved claim must stay pending "+c.id);
  if(!Array.isArray(c.previewSourceIds)||!c.previewSourceIds.length||c.previewSourceIds.some(id=>!sourceIds.includes(id)))bad("invalid expert provenance "+c.id);
  if(c.requiredIndependentReviewers!==(c.risk==="HIGH"?2:1))bad("risk-level review count mismatch "+c.id);
 }
 if(Array.isArray(claims)&&b.expertReview?.highRiskCount!==claims.filter(c=>c.risk==="HIGH").length)bad("high risk count mismatch");
 if(b.expertReview?.reviewersEngaged!==0||b.expertReview?.actualDecisionsRecorded!==0)bad("actual human experts cannot be simulated");
 const p=b.participant, tasks=Array.isArray(p?.tasks)?p.tasks:[],questions=Array.isArray(p?.questions)?p.questions:[];
 if(!tasks.length||!unique(tasks.map(t=>t.id))||!questions.length||!unique(questions.map(q=>q.id)))bad("reader tasks/questions missing or duplicate");
 for(const t of tasks){
  if(!validId(t.id)||!Array.isArray(t.questionIds)||t.questionIds.some(id=>!questions.some(q=>q.id===id)))bad("reader task mapping broken "+t.id);
 }
 for(const q of questions){
  if(!tasks.some(t=>t.id===q.taskId)||!Array.isArray(q.choices)||q.choices.length<2||!unique(q.choices.map(c=>c.id))||!validId(q.prompt))bad("reader question malformed "+q.id);
  if("answerKey" in q||"correctChoice" in q||"correctAnswer" in q||"misconceptionCode" in q)bad("answer/evaluation metadata leaked in participant view "+q.id);
 }
 if(p?.actualParticipants!==0||p?.actualSessions!==0||p?.responseCollectionEnabled!==false||p?.assessmentKeysIncluded!==false)bad("reader data or answer key must not be invented");
 if(b.privacy?.legacyAnswerKeyInPublicRepo!==true||b.privacy?.blindPilotClaimPermitted!==false||b.privacy?.containsIdentifiableParticipants!==false||b.privacy?.answersCollected!==false)bad("privacy/bias controls missing");
 if(!Array.isArray(b.unresolved)||!b.unresolved.length)bad("unresolved source risks missing");
 return {valid:errors.length===0,errors};
}
export function assertAtlasReviewBundle(bundle){
 const result=validateAtlasReviewBundle(bundle);
 if(!result.valid)throw Error("ATLAS research bundle rejected: "+result.errors.join("; "));
 return bundle;
}
