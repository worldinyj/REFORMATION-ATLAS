import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
const root=new URL("../../research/data/",import.meta.url);
const file=name=>readFile(fileURLToPath(new URL(name,root)),"utf8");
const registry=JSON.parse(await file("ATLAS_V471_SENTENCE_PROVENANCE_AND_REVIEW_KIT.json"));
const src=JSON.parse(await file("ATLAS_V470_W2119_ART15_TRANSLATION_GAP_AND_HEPPE_EDITION_CANDIDATE.json"));
const older=JSON.parse(await file("ATLAS_V457_CLAIM_SOURCE_CRITICAL_REGISTER.json"));
const pilot=JSON.parse(await file("ATLAS_V457_READER_PILOT_INSTRUMENT.json"));
const md=await readFile(fileURLToPath(new URL("./V470_MARBURG_1529_READER_COPYTEXT_DIFFERENCES_KO.md",import.meta.url)),"utf8");
test("All 29 L0/L1 exact candidate sentences still occur in unchanged V4.70",()=>{
 assert.equal(registry.sentenceAnnotations.length,29);
 assert.equal(registry.counts.l0,8);
 assert.equal(registry.counts.l1,21);
 assert.equal(new Set(registry.sentenceAnnotations.map(s=>s.id)).size,29);
 for(const s of registry.sentenceAnnotations)assert.ok(md.includes(s.originalSentence),s.id+" text drift");
});
test("Every factual annotation uses an existing source and claim; editorial is explicitly separate",()=>{
 const sources=new Set([...src.sourceRegistry.map(s=>s.id),...Object.keys(older.sourceRegistry)]);
 const claims=new Set([...src.claims.map(c=>c.id),...older.claims.map(c=>c.id)]);
 for(const s of registry.sentenceAnnotations){
  assert.ok(["HIGH","MEDIUM","LOW"].includes(s.risk));
  assert.ok(["REVISE_BEFORE_REVIEW","EXPERT_REVIEW","REVIEW_CANDIDATE","EDITORIAL_NO_HISTORICAL_ASSERTION"].includes(s.disposition));
  if(s.disposition!=="EDITORIAL_NO_HISTORICAL_ASSERTION")assert.ok(s.sourceIds.length>0&&s.claimIds.length>0,s.id);
  for(const id of s.sourceIds) assert.ok(sources.has(id),id);
  for(const id of s.claimIds) assert.ok(claims.has(id),id);
  assert.equal(s.decision,"PENDING");
  assert.equal(s.reviewer1,null);
  assert.equal(s.reviewer2,null);
 }
});
test("Ambiguous phrases have explicit safer replacement proposals",()=>{
 const target=["V471-S03","V471-S07","V471-S18","V471-S21"];
 for(const id of target){
  const a=registry.sentenceAnnotations.find(s=>s.id===id);
  assert.equal(a.disposition,"REVISE_BEFORE_REVIEW");
  assert.ok(a.proposedRewrite.length>20);
  assert.notEqual(a.proposedRewrite,a.originalSentence);
 }
 assert.equal(registry.counts.needsRewrite,4);
});
test("Reader pilot unchanged, additional calibration questions unscored and no real data",()=>{
 assert.deepEqual(registry.readerProtocol.existingTasks,pilot.tasks.map(t=>t.id));
 assert.deepEqual(registry.readerProtocol.existingQuestions,pilot.questions.map(q=>q.id));
 assert.equal(registry.readerProtocol.additionalUnscoredCalibrationQuestions,3);
 assert.equal(registry.readerProtocol.existingThresholdsUnchanged,true);
 assert.equal(registry.gate.readerSessionsCollected,0);
 assert.equal(registry.readerProtocol.answerKeyIsPublicInExistingRepo,true);
});
test("All actual review, archive-mail, shipping and AI Studio gates remain closed",()=>{
 const g=registry.gate;
 for(const k of ["canShip","canMergeMain","canImportAIStudio","originalContentModified","productionAppModified","participantRecruitmentStarted"])assert.equal(g[k],false);
 for(const k of ["expertInvitationsSent","expertReviewsReceived","readerSessionsCollected","archiveRequestsSent","newPaidOrders","autographKZImagesReviewed"])assert.equal(g[k],0);
 assert.equal(registry.expertProtocol.allActualReviewsPending,true);
});
