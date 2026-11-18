import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
import {scoreReaderSession,evaluatePilot} from "./score-reader-session.mjs";

async function load(name) {
  const path=fileURLToPath(new URL("../../research/data/"+name,import.meta.url));
  return JSON.parse(await readFile(path,"utf8"));
}
const instrument=await load("ATLAS_V457_READER_PILOT_INSTRUMENT.json");
const claims=await load("ATLAS_V457_CLAIM_SOURCE_CRITICAL_REGISTER.json");
const validAnswers=Object.fromEntries(instrument.questions.map(q=>[q.id,q.answerKey]));
const allTasks=Object.fromEntries(instrument.tasks.map(t=>[t.id,true]));

test("V4.57 all 14 claims have a traceable published source and expert flags",()=>{
  assert.equal(claims.claims.length,14);
  assert.equal(new Set(claims.claims.map(c=>c.id)).size,14);
  assert.ok(Object.keys(claims.sourceRegistry).length>=2);
  for(const c of claims.claims){
    assert.equal(c.expertApproved,false);
    assert.equal(c.canShip,false);
    assert.ok(c.sources.length>0);
    for(const ref of c.sources)assert.ok(claims.sourceRegistry[ref]?.url?.startsWith("https://"),ref);
  }
  assert.equal(claims.reviewWorkflow.pendingHighRisk,claims.claims.filter(c=>c.risk==="HIGH").length);
});

test("V4.57 3 tasks and 9 questions have complete mapping, and 7 critical items",()=>{
  assert.equal(instrument.tasks.length,3);
  assert.equal(instrument.questions.length,9);
  const ids=new Set(instrument.questions.map(q=>q.id));
  const claimIds=new Set(claims.claims.map(c=>c.id));
  assert.equal(ids.size,9);
  const referenced=[];
  for(const t of instrument.tasks){
    assert.equal(t.questionIds.length,3);
    for(const id of t.questionIds){assert.ok(ids.has(id));referenced.push(id);}
  }
  assert.equal(new Set(referenced).size,9);
  for(const q of instrument.questions){
    assert.equal(q.choices.length,4);
    assert.equal(new Set(q.choices.map(c=>c.id)).size,4);
    assert.ok(q.choices.some(c=>c.id===q.answerKey));
    assert.ok(claimIds.has(q.linkedClaim),q.linkedClaim);
    assert.ok(instrument.tasks.some(t=>t.id===q.taskId&&t.questionIds.includes(q.id)));
  }
  assert.equal(instrument.scoring.criticalIds.length,7);
});

test("V4.57 scorer enforces correct answers, task completion and critical threshold",()=>{
  const perfect=scoreReaderSession(instrument,{answers:validAnswers,completedTasks:allTasks});
  assert.equal(perfect.score,9);
  assert.equal(perfect.criticalScore,7);
  assert.equal(perfect.passed,true);
  const incomplete=scoreReaderSession(instrument,{answers:validAnswers,completedTasks:{...allTasks,"TASK-02":false}});
  assert.equal(incomplete.passed,false);
  const wrong={...validAnswers,Q01:"A",Q02:"A"};
  const risky=scoreReaderSession(instrument,{answers:wrong,completedTasks:allTasks});
  assert.equal(risky.score,7);
  assert.equal(risky.criticalScore,5);
  assert.equal(risky.passed,false);
  assert.throws(()=>scoreReaderSession(instrument,{answers:{Q01:"X"},completedTasks:{}}),/invalid answer choice/);
  assert.throws(()=>scoreReaderSession(instrument,{answers:{Q99:"A"},completedTasks:{}}),/unknown question/);
});

test("V4.57 pilot gate rejects missing participants and repeated key misconceptions",()=>{
  const empty=evaluatePilot(instrument,[]);
  assert.equal(empty.reviewEligible,false);
  assert.equal(empty.canShip,false);
  const allGood=Array.from({length:6},(_,i)=>({
    sessionId:"P"+String(i+1).padStart(2,"0"),answers:validAnswers,completedTasks:allTasks
  }));
  const synthetic=evaluatePilot(instrument,allGood);
  assert.equal(synthetic.reviewEligible,true);
  assert.equal(synthetic.canShip,false);
  const errors=allGood.map((s,i)=>({...s,answers:{...validAnswers,Q01:i<2?"A":"B"}}));
  assert.equal(evaluatePilot(instrument,errors).reviewEligible,false);
  assert.throws(()=>evaluatePilot(instrument,[allGood[0],allGood[0]]),/unique/);
});

test("V4.57 public release cannot be inferred from research-only instruments",()=>{
  assert.equal(instrument.status,"PILOT_READY_NOT_ADMINISTERED");
  assert.equal(instrument.pilotObservations.actualParticipants,0);
  assert.equal(claims.reviewWorkflow.reviewers,0);
  assert.equal(instrument.release.canShip,false);
  assert.equal(claims.release.canImportAIStudio,false);
});
