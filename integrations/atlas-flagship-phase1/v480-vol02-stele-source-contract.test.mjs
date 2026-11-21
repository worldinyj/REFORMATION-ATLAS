import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
const read=p=>readFile(fileURLToPath(new URL(p,import.meta.url)),"utf8");
const p=JSON.parse(await read("../../research/data/ATLAS_V480_VOL02_JINGJIAO_READER_CANDIDATE.json"));
const master=JSON.parse(await read("../../research/data/V4_50_L1_24_CHAPTER_INTEGRATED_REVISED_MASTER.json"));
const reviews=JSON.parse(await read("../../research/data/V4_44_GO_NO_GO_MASTER_GATE_REGISTER.json"));
const claimRegister=JSON.parse(await read("../../research/data/V4_47_53_CLAIM_SOURCE_AND_TEXT_POSITION_REGISTER.json"));
const prose=await read("./V480_VOL02_JINGJIAO_635_781_L0_L1_KO.md");
const decision=await read("./V480_VOL02_STELE_RUBBING_TRANSLATION_EDITORIAL_DECISION_KO.md");
const old=master.volumes.find(v=>v.id==="VOL-02").chapters.find(c=>c.id==="L448-02-02");
const sourceIds=new Set(p.sourceRegistry.map(s=>s.id));
const extractIds=t=>[...new Set([...t.matchAll(/\[(S480-[A-Z0-9-]+)\]/g)].map(x=>x[1]))];

test("V4.80 retains the exact original VOL02 master chapter and writes a genuinely expanded reader manuscript",()=>{
 assert.equal(p.volumeId,"VOL-02");assert.equal(p.chapterId,"L448-02-02");
 assert.equal(p.legacy.originalTitle,old.title);
 assert.equal(p.legacy.originalBodyMarkdown,old.bodyMarkdown);
 assert.equal(p.legacy.originalBodyChars,old.bodyMarkdown.length);
 assert.deepEqual(p.legacy.sourceUrls,old.sourceUrls);
 assert.deepEqual(p.legacy.crossLinks,old.crossLinks);
 assert.equal(p.newContent.l0Markdown.split(/\n\s*\n/).length,4);
 assert.equal((p.newContent.l1Markdown.match(/^### /gm)||[]).length,8);
 assert.equal(p.newContent.l0ParagraphCount,4);assert.equal(p.newContent.l1SectionCount,8);
 assert.ok(p.newContent.l1Markdown.length>=4000);
 assert.ok(p.newContent.l1Markdown.length>=7*old.bodyMarkdown.length);
 assert.ok(prose.includes(p.newContent.l0Markdown));assert.ok(prose.includes(p.newContent.l1Markdown));
});
test("635, 638, 781, 1620s and twentieth-century material witnesses remain distinct",()=>{
 assert.deepEqual(p.comparisons.map(x=>x.epoch),["635","638","781","1620s","20th c."]);
 assert.equal(p.comparisons[0].objectType,"781년 경교비에 기재된 과거 사건");
 assert.match(p.comparisons[1].notEstablished,/조서/);
 assert.match(p.comparisons[2].objectType,/당대 기념 석각/);
 assert.match(p.comparisons[3].notEstablished,/1623\/1625/);
 assert.match(p.comparisons[4].objectType,/후대 종이/);
 for(const c of p.comparisons)assert.ok(c.sourceIds.length&&c.sourceIds.every(id=>sourceIds.has(id)));
});
test("Exact institutional provenance prevents Smithsonian/Australian 20th-century rubbings becoming Tang original",()=>{
 assert.equal(p.sourceRegistry.length,8);
 assert.equal(sourceIds.size,8);
 assert.ok(p.sourceRegistry.every(x=>x.url.startsWith("https://")&&x.kind&&x.limit));
 const smith=p.sourceRegistry.find(x=>x.id==="S480-SMITH");
 const australian=p.sourceRegistry.find(x=>x.id==="S480-AUSTRALIAN");
 const fordham=p.sourceRegistry.find(x=>x.id==="S480-FORDHAM1917");
 assert.equal(smith.kind,"RUBBING_OBJECT_CATALOGUE");
 assert.match(smith.observed,/F1976|20th century/);
 assert.equal(australian.kind,"MUSEUM_RUBBING_TECHNIQUE_AND_RECORD");
 assert.equal(fordham.kind,"EDITED_HISTORIC_TRANSLATION");
 assert.match(fordham.limit,/1917년 번역/);
 assert.match(p.newContent.l1Markdown,/1976/);
});
test("Actual source IDs in the new L0 and L1 are all registered and individual claims are pending",()=>{
 const citations=extractIds(p.newContent.l0Markdown+"\n"+p.newContent.l1Markdown);
 assert.ok(citations.length>=7);
 assert.ok(citations.every(id=>sourceIds.has(id)));
 assert.equal(p.claimAudit.length,16);
 assert.equal(new Set(p.claimAudit.map(c=>c.id)).size,16);
 assert.ok(p.claimAudit.filter(c=>c.highRisk).length>=6);
 for(const c of p.claimAudit){
  assert.equal(c.reviewDecision,"PENDING");
  assert.equal(c.reviewer,null);
  assert.equal(c.originalChineseSyriacCollated,false);
  assert.ok(c.sourceIds.length&&c.sourceIds.every(id=>sourceIds.has(id)),c.id);
 }
});
test("Historical source limitations are explicit: 638 independent edict, 1623/25 and original scripts are NOT verified",()=>{
 assert.ok(p.highRiskHolds.some(x=>x.id==="H480-CHINESE-SYRIAC"));
 assert.ok(p.highRiskHolds.some(x=>x.id==="H480-638-EDICT"));
 assert.ok(p.highRiskHolds.some(x=>x.id==="H480-1623-1625"));
 assert.ok(p.highRiskHolds.some(x=>x.id==="H480-RUBBINGS"));
 assert.ok(p.highRiskHolds.length>=6);
 assert.match(p.newContent.l1Markdown,/638년/);
 assert.match(p.newContent.l1Markdown,/보편적 종교자유/);
 assert.match(p.newContent.l1Markdown,/1623년과 1625년/);
 assert.match(decision,/전문가/);
});
test("Original G443-09 stays NOT_SUBMITTED; no phantom historian, reader, rights or production approval",()=>{
 const original=reviews.highRiskAndSecondaryReviews.find(x=>x.id==="G443-09");
 assert.ok(original);
 assert.equal(original.currentStatus,"NOT_SUBMITTED");
 assert.equal(p.priorReviewGate.status,original.currentStatus);
 assert.deepEqual(p.priorReviewGate.originalClaimIds,original.claimIds);
 assert.ok(p.priorReviewGate.originalClaimIds.every(id=>claimRegister.sourceLinkedClaims.some(c=>c.id===id&&c.volumeId==="VOL-02")));
 assert.equal(p.expertReviewsCompleted,0);assert.equal(p.actualReaderSessions,0);
 assert.equal(p.originalStoneFolioCollationCount,0);assert.equal(p.rubbingsPhysicallyCompared,0);
 assert.equal(p.productionAppChanges,0);assert.equal(p.externalEmailsSent,0);
 assert.ok(Object.values(p.releaseGate).every(x=>x===false));
 assert.match(prose,/can_ship=false/);
});
