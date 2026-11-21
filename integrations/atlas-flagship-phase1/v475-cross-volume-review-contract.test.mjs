import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
import {validateAtlasReviewBundle,assertAtlasReviewBundle} from "./atlas-review-bundle-contract.mjs";
const read=path=>readFile(fileURLToPath(new URL(path,import.meta.url)),"utf8");
const bundle=JSON.parse(await read("../../research/data/ATLAS_V475_CROSS_VOLUME_REVIEW_BUNDLE.json"));
const v474=JSON.parse(await read("../../research/data/ATLAS_V474_REACT_READER_PACK.json"));
const v457=JSON.parse(await read("../../research/data/ATLAS_V457_READER_PILOT_INSTRUMENT.json"));
const claims=JSON.parse(await read("../../research/data/ATLAS_V457_CLAIM_SOURCE_CRITICAL_REGISTER.json"));
const clone=x=>structuredClone(x);
test("V4.75 is valid, truly cross-volume reusable and preserves both exact V4.72 texts",()=>{
 assert.deepEqual(validateAtlasReviewBundle(bundle),{valid:true,errors:[]});
 assert.equal(assertAtlasReviewBundle(bundle),bundle);
 assert.equal(bundle.layers.find(x=>x.level==="L0").markdown,v474.l0.text);
 assert.equal(bundle.layers.find(x=>x.level==="L1").markdown,v474.l1.text);
 const other=clone(bundle);other.identity={...other.identity,volumeId:"VOL-SYNTH",chapterId:"CH-SYNTH",sceneId:"TEST-SYNTHETIC-NOT-HISTORICAL"};
 assert.equal(validateAtlasReviewBundle(other).valid,true,"no hardcoded fourth-volume IDs");
});
test("Evidence source taxonomy and unresolved K/Z manuscript stay separate",()=>{
 assert.equal(bundle.sources.length,6);
 assert.equal(bundle.timeline.length,4);
 assert.equal(bundle.comparisons.length,3);
 assert.equal(bundle.comparisons.find(x=>x.id==="KZ").originalAutographChecked,false);
 assert.equal(bundle.expertReview.claims.length,14);
 assert.equal(bundle.expertReview.highRiskCount,10);
 for(const c of bundle.expertReview.claims)assert.equal(c.requiredIndependentReviewers,c.risk==="HIGH"?2:1);
 assert.deepEqual(new Set(bundle.sources.map(s=>s.id)),new Set(v474.sources.map(s=>s.id)));
 assert.ok(bundle.unresolved.some(x=>x.id==="HOLD-KZ"));
 assert.ok(bundle.unresolved.some(x=>x.id==="HOLD-1531-1540"));
});
test("Participant package contains all 3 tasks/9 questions with NO answer key and Q09 corrected",()=>{
 assert.equal(bundle.participant.tasks.length,3);
 assert.equal(bundle.participant.questions.length,9);
 assert.deepEqual(bundle.participant.questions.map(x=>x.id),v457.questions.map(x=>x.id));
 for(const q of bundle.participant.questions){
  assert.equal(q.choices.length,4);
  assert.equal(Object.hasOwn(q,"answerKey"),false);
  assert.equal(Object.hasOwn(q,"misconceptionCode"),false);
  assert.deepEqual(q.choices,v457.questions.find(y=>y.id===q.id).choices);
 }
 assert.match(bundle.participant.questions.find(q=>q.id==="Q09").prompt,/여러 사료 카드/);
 assert.doesNotMatch(JSON.stringify(bundle.participant),/"answerKey"/);
 assert.equal(bundle.privacy.legacyAnswerKeyInPublicRepo,true);
});
test("Validator fails closed on promotion, phantom decisions and broken evidence",()=>{
 for(const mutate of [
  x=>x.releaseGate.canShip=true,
  x=>x.releaseGate.canImportAIStudio=true,
  x=>x.expertReview.claims[0].expertApproved=true,
  x=>x.expertReview.claims[1].reviewer1="fictional reviewer",
  x=>x.layers[0].sourceRefs=["UNREGISTERED"],
  x=>x.sources[0].url="http://untrusted.example/",
  x=>x.comparisons[0].originalAutographChecked=true,
  x=>x.participant.questions[0].answerKey="B",
  x=>x.participant.actualParticipants=8,
  x=>x.privacy.blindPilotClaimPermitted=true
 ]){
  const modified=clone(bundle);mutate(modified);
  assert.equal(validateAtlasReviewBundle(modified).valid,false);
 }
});
test("Every expert claim is copied from source register and actual approval count remains zero",()=>{
 for(const c of bundle.expertReview.claims){
  const src=claims.claims.find(x=>x.id===c.id);
  assert.ok(src);
  assert.equal(c.statement,src.claim);
  assert.equal(c.risk,src.risk);
  assert.equal(c.expertApproved,false);
  assert.equal(c.decision,"PENDING");
 }
 assert.equal(bundle.expertReview.reviewersEngaged,0);
 assert.equal(bundle.participant.actualSessions,0);
 assert.equal(bundle.releaseGate.hostAccessVerified,false);
});
