import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
const read=p=>readFile(fileURLToPath(new URL(p,import.meta.url)),"utf8");
const p=JSON.parse(await read("../../research/data/ATLAS_V481_VOL07_KOREAN_CHURCH_READER_CANDIDATE.json"));
const master=JSON.parse(await read("../../research/data/V4_50_L1_24_CHAPTER_INTEGRATED_REVISED_MASTER.json"));
const gate=JSON.parse(await read("../../research/data/V4_44_GO_NO_GO_MASTER_GATE_REGISTER.json"));
const register=JSON.parse(await read("../../research/data/V4_47_53_CLAIM_SOURCE_AND_TEXT_POSITION_REGISTER.json"));
const md=await read("./V481_VOL07_KOREAN_CHURCH_ORIGINS_AND_BIBLE_EDITIONS_KO.md");
const decision=await read("./V481_VOL07_HISTORICAL_EVIDENCE_DECISION_KO.md");
const old=master.volumes.find(x=>x.id==="VOL-07").chapters.find(x=>x.id==="L448-07-02");
const ids=new Set(p.sourceRegistry.map(s=>s.id));
const cites=t=>[...new Set([...t.matchAll(/\[(S481-[A-Z0-9-]+)\]/g)].map(x=>x[1]))];

test("V4.81 preserves the real V4.50 VOL07 source chapter while producing substantive Korean prose",()=>{
 assert.equal(p.volumeId,"VOL-07");assert.equal(p.chapterId,"L448-07-02");
 assert.equal(p.legacy.originalBodyChars,old.bodyMarkdown.length);
 assert.equal(p.legacy.originalBodyMarkdown,old.bodyMarkdown);
 assert.equal(old.bodyMarkdown.length,1164);
 assert.deepEqual(p.legacy.sourceUrls,old.sourceUrls);
 assert.deepEqual(p.legacy.crossLinks,old.crossLinks);
 assert.equal(p.newContent.l0ParagraphCount,4);
 assert.equal(p.newContent.l0Markdown.split(/\n\s*\n/).length,4);
 assert.equal(p.newContent.l1SectionCount,10);
 assert.equal((p.newContent.l1Markdown.match(/^### /gm)||[]).length,10);
 assert.ok(p.newContent.l1Markdown.length>=5500);
 assert.ok(p.newContent.l1Markdown.length>=5*old.bodyMarkdown.length);
 assert.ok(md.includes(p.newContent.l0Markdown));
 assert.ok(md.includes(p.newContent.l1Markdown));
});
test("1779 evidence is retrospective and contested while 1784 baptism is separately described",()=>{
 assert.deepEqual(p.comparisons.slice(0,2).map(x=>x.year),["1779","1784"]);
 assert.match(p.comparisons[0].notEstablished,/강학.*천주교|천주교.*교리/);
 assert.match(p.newContent.l1Markdown,/정약용.*묘지명/);
 assert.match(p.newContent.l1Markdown,/북경.*세례/);
 assert.match(p.newContent.l1Markdown,/달레/);
 assert.match(p.highRiskHolds.find(x=>x.id==="H481-1779-EARLY-CHURCH").description,/강학/);
});
test("1882 single gospels, 1887 NT, 1900 local NT, 1906 authorized text and 1911 full Bible cannot be collapsed",()=>{
 assert.deepEqual(p.comparisons.map(x=>x.year),["1779","1784","1882","1885","1887","1900","1906","1911"]);
 assert.match(p.comparisons.find(x=>x.year==="1882").notEstablished,/27권/);
 assert.match(p.comparisons.find(x=>x.year==="1887").object,/27권/);
 assert.match(p.comparisons.find(x=>x.year==="1900").notEstablished,/1906/);
 assert.match(p.comparisons.find(x=>x.year==="1911").object,/신구약/);
 assert.match(p.newContent.l1Markdown,/1906년.*공인역/);
 assert.match(p.newContent.l1Markdown,/이수정/);
 assert.match(p.newContent.l1Markdown,/개신교.*성서/);
});
test("12 registered sources identify document genre and all prose/chronology source references resolve",()=>{
 assert.equal(p.sourceRegistry.length,12);assert.equal(ids.size,12);
 assert.ok(p.sourceRegistry.every(s=>s.url.startsWith("https://")&&s.kind&&s.limit));
 assert.ok(p.sourceRegistry.every(s=>s.originalHistoricObjectDirectlyCollated===false&&s.linkOnlyNoCopyrightedScan===true));
 assert.equal(p.sourceRegistry.find(s=>s.id==="S481-AKS-GANGHAK").kind,"ACADEMIC_ENCYCLOPEDIA_HISTORIOGRAPHY");
 assert.equal(p.sourceRegistry.find(s=>s.id==="S481-BSK-HISTORY").kind,"BIBLE_SOCIETY_INSTITUTIONAL_HISTORY");
 assert.match(p.sourceRegistry.find(s=>s.id==="S481-CAMBRIDGE").limit,/403/);
 const found=cites(p.newContent.l0Markdown+"\n"+p.newContent.l1Markdown);
 assert.ok(found.length>=10);
 assert.ok(found.every(id=>ids.has(id)));
 for(const x of p.comparisons)assert.ok(x.sourceIds.every(id=>ids.has(id)));
});
test("Original Korean translation helpers and typesetting are recorded without inventing exact verse attribution",()=>{
 assert.match(p.newContent.l1Markdown,/이응찬/);
 assert.match(p.newContent.l1Markdown,/백홍준/);
 assert.match(p.newContent.l1Markdown,/서상륜/);
 assert.match(p.newContent.l1Markdown,/김청송/);
 assert.match(p.newContent.l1Markdown,/백홍준\/백홍진/);
 assert.ok(p.highRiskHolds.some(h=>h.id==="H481-ROSS-TRANSLATORS"));
 assert.equal(p.claimAudit.find(c=>c.id==="C481-09").highRisk,true);
});
test("Twenty source-anchored claims and seven unresolved historical holds contain zero expert signoff",()=>{
 assert.equal(p.claimAudit.length,20);
 assert.equal(new Set(p.claimAudit.map(x=>x.id)).size,20);
 assert.equal(p.highRiskHolds.length,7);
 for(const x of p.claimAudit){
  assert.equal(x.reviewDecision,"PENDING");assert.equal(x.historianReviewer,null);
  assert.equal(x.originalHistoricalObjectDirectlyCompared,false);
  assert.ok(x.sourceIds.length&&x.sourceIds.every(id=>ids.has(id)),x.id);
 }
 assert.ok(p.claimAudit.filter(x=>x.highRisk).length>=8);
});
test("All four VOL07 P0 plus one P1 docket stay NOT_SUBMITTED and all release gates closed",()=>{
 const prior=gate.highRiskAndSecondaryReviews.filter(x=>x.targetVolumeIds.includes("VOL-07"));
 assert.equal(prior.length,5);assert.equal(p.priorReviewDockets.length,5);
 assert.equal(prior.filter(x=>x.priority==="P0").length,4);
 assert.equal(prior.filter(x=>x.priority==="P1").length,1);
 for(const x of prior){
  const current=p.priorReviewDockets.find(y=>y.id===x.id);
  assert.ok(current);assert.equal(current.status,"NOT_SUBMITTED");
  assert.equal(current.actualReviewerCount,0);assert.deepEqual(current.claimIds,x.claimIds);
  assert.ok(x.claimIds.every(id=>register.sourceLinkedClaims.some(c=>c.id===id&&c.volumeId==="VOL-07")));
 }
 assert.equal(p.validation.originalDocumentFolioCollationCount,0);
 assert.equal(p.validation.actualHistoricalExperts,0);
 assert.equal(p.validation.actualReaderSessions,0);
 assert.equal(p.validation.externalEmailsSent,0);
 assert.equal(p.validation.webAppChanges,0);
 assert.equal(p.validation.legacyMasterChanged,false);
 assert.ok(Object.values(p.releaseGate).every(x=>x===false));
 assert.match(md,/can_ship=false/);assert.match(decision,/NOT_SUBMITTED/);
});
