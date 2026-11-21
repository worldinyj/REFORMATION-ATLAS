import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
const read=p=>readFile(fileURLToPath(new URL(p,import.meta.url)),"utf8");
const p=JSON.parse(await read("../../research/data/ATLAS_V478_EIGHT_VOLUME_BASELINE_AND_PRIORITIES.json"));
const l0=JSON.parse(await read("../../research/data/V4_47_TWO_SOURCE_GROUNDED_L0_HISTORY_CORRECTIONS.json"));
const l1=JSON.parse(await read("../../research/data/V4_50_L1_24_CHAPTER_INTEGRATED_REVISED_MASTER.json"));
const claims=JSON.parse(await read("../../research/data/V4_47_53_CLAIM_SOURCE_AND_TEXT_POSITION_REGISTER.json"));
const gate=JSON.parse(await read("../../research/data/V4_44_GO_NO_GO_MASTER_GATE_REGISTER.json"));
const nav=await read("./V478_EIGHT_VOLUME_READER_NAV_ARCHITECTURE_KO.md");
const plan=await read("./V478_PRIORITIZED_REAL_CONTENT_AUTHORING_PLAN_KO.md");

test("V4.78 L0/L1 lengths and links are computed from the actual 8-volume master",()=>{
 assert.equal(p.volumes.length,8);
 assert.equal(p.source.l0TotalChars,18626);
 assert.equal(p.source.l1TotalChars,15031);
 assert.equal(p.source.l1ChapterCount,24);
 assert.equal(p.source.l1SourceOccurrences,74);
 assert.equal(p.source.l1DistinctSourceUrls,53);
 assert.equal(p.source.claimRegisterCount,53);
 for(const v of p.volumes){
  const a=l0.volumes.find(x=>x.id===v.id),b=l1.volumes.find(x=>x.id===v.id);
  assert.ok(a&&b);
  assert.equal(v.baseline.l0Chars,a.bodyMarkdown.length);
  assert.equal(v.baseline.l1Chars,b.chapters.reduce((n,c)=>n+c.bodyMarkdown.length,0));
  assert.equal(v.baseline.l1Chapters,b.chapters.length);
  assert.deepEqual(v.chapters.map(c=>c.id),b.chapters.map(c=>c.id));
  assert.equal(v.baseline.l0MappedClaimCount,claims.sourceLinkedClaims.filter(c=>c.volumeId===v.id).length);
 }
});
test("VOL01–07 are chronological, VOL08 is a thematic map rather than a ninth era",()=>{
 assert.deepEqual(p.volumes.map(v=>v.id),Array.from({length:8},(_,i)=>"VOL-0"+(i+1)));
 assert.equal(p.volumes.filter(v=>v.kind==="CHRONOLOGICAL_HISTORY").length,7);
 assert.equal(p.volumes[7].kind,"THEMATIC_COMPARISON");
 assert.equal(p.canonicalNavigation.modes.length,3);
 assert.equal(p.canonicalNavigation.themes.length,6);
 assert.match(nav,/제8권/);
});
test("Six thematic reader routes only name extant chapters and have no invented signoff",()=>{
 const chapterIds=new Set(l1.volumes.flatMap(v=>v.chapters.map(c=>c.id)));
 for(const t of p.canonicalNavigation.themes){
  assert.ok(t.chapterIds.length>=3);
  assert.ok(t.chapterIds.every(id=>chapterIds.has(id)));
  assert.ok(t.chapterIds.some(id=>id.startsWith("L448-08-")));
  assert.equal(t.linkStatus,"RESEARCH_EDITORIAL_PROPOSAL_NOT_VALIDATED_BY_READERS");
  assert.equal(t.requiresHumanExpertReview,true);
 }
});
test("All 66 original chapter crosslinks are retained without making causal claims",()=>{
 const actual=l1.volumes.flatMap(v=>v.chapters.flatMap(c=>(c.crossLinks||[]).map(to=>[v.id,c.id,to])));
 assert.deepEqual(p.canonicalNavigation.chapterEdges.map(e=>[e.sourceVolumeId,e.sourceChapterId,e.targetVolumeId]),actual);
 assert.equal(actual.length,66);
 assert.ok(p.canonicalNavigation.chapterEdges.every(e=>e.kind==="AUTHOR_DEFINED_CROSSLINK_NOT_HISTORICAL_CAUSATION"));
});
test("The 8 P0 and 4 P1 research reviews are still NOT_SUBMITTED, with all gates closed",()=>{
 assert.equal(p.expertStatus.pendingP0.length,8);
 assert.equal(p.expertStatus.pendingP1.length,4);
 assert.ok(gate.highRiskAndSecondaryReviews.every(x=>x.currentStatus==="NOT_SUBMITTED"));
 assert.equal(p.source.actualReviewerSignoffs,0);
 assert.equal(p.source.actualReaderSessions,0);
 assert.ok(Object.values(p.releaseGate).every(v=>v===false));
 assert.ok(p.volumes.every(v=>v.expertApproved===false&&v.realReadersObserved===0));
});
test("The roadmap targets real narrative work rather than another redundant preview",()=>{
 assert.match(plan,/1715\/1719/);
 assert.match(plan,/635년/);
 assert.match(plan,/V4.50/);
 assert.match(nav,/V451_L0_L1_OFFLINE_READER_PILOT.html/);
 assert.match(nav,/실제 참여 0명/);
 assert.match(nav,/can_import_ai_studio=false/);
 assert.equal(p.qualitativePriorities.length,4);
 assert.ok(p.qualitativePriorities[0].volumeIds.includes("VOL-06"));
 assert.ok(p.qualitativePriorities[1].volumeIds.includes("VOL-02"));
});
