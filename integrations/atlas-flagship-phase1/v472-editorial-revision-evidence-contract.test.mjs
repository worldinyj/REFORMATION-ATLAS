import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
const f = path => readFile(fileURLToPath(new URL(path,import.meta.url)),"utf8");
const data = JSON.parse(await f("../../research/data/ATLAS_V472_MARBURG_REVISED_READER_CANDIDATE_AND_REDLINES.json"));
const v470 = await f("./V470_MARBURG_1529_READER_COPYTEXT_DIFFERENCES_KO.md");
const v472 = await f("./V472_MARBURG_1529_L0_L1_REVISED_READER_CANDIDATE_KO.md");
const old = JSON.parse(await f("../../research/data/ATLAS_V471_SENTENCE_PROVENANCE_AND_REVIEW_KIT.json"));
test("V4.72 is a full L0/L1 candidate, not a silent edit to V4.70",()=>{
 assert.ok(v470.includes("## 2. L0"));
 assert.ok(v472.includes("## L0 |") && v472.includes("## L1 |"));
 assert.equal((v472.match(/^### [1-6]\./gm)||[]).length,6);
 assert.equal(data.qa.originalV470TextPreserved,true);
 assert.equal(data.contentBlocks.length,7);
});
test("All four exact V4.71 high priority flags are addressed in the new research copy",()=>{
 const ids=["V471-S03","V471-S07","V471-S18","V471-S21"];
 assert.deepEqual(data.targetedRedlines.slice(0,4).map(s=>s.sentenceId),ids);
 for(const change of data.targetedRedlines.slice(0,4)){
   assert.ok(old.sentenceAnnotations.some(x=>x.id===change.sentenceId));
   assert.ok(v472.includes(change.accept),change.sentenceId+" missing revised phrase");
   assert.ok(change.status.startsWith("ADOPTED"));
 }
 assert.ok(!v472.includes("가장 어려운 부분"));
 assert.ok(!v472.includes("널리 읽히는"));
});
test("Source types have traceable URLs and claims cannot masquerade as K/Z original handwriting",()=>{
 assert.equal(data.sourceRegistry.length,6);
 assert.ok(data.sourceRegistry.every(x=>x.url.startsWith("https://")));
 assert.ok(data.contentBlocks.every(b=>b.sourceIds?.every(id=>data.sourceRegistry.some(s=>s.id===id))));
 assert.match(v472,/서명 필사본 K·Z와 별개의 인쇄 증인/);
 assert.match(v472,/GHDI 영어 번역/);
 assert.match(v472,/목록/);
 assert.ok(data.issuesToHold.some(x=>x.includes("genealogy")));
});
test("Bibliographic second edition remains explicitly Schaff-attested, not title-page proof",()=>{
 assert.ok(v472.includes("필립 샤프는 1847년 카셀 간행과 1854년 제2판"));
 assert.ok(v472.includes("실물 표제지와 판권면"));
 assert.ok(data.issuesToHold.some(x=>x.includes("physical imprint")));
});
test("Actual human, archival, CI and production release gates are fail closed",()=>{
 const g=data.gates;
 for(const k of ["canShip","canMergeMain","canImportAIStudio","mainModified","operatingAppModified"]) assert.equal(g[k],false);
 for(const k of ["historianApprovals","readerParticipants","autographKZOriginalsReviewed","latinOriginalPrintsReviewed","emailsSent","paidOrders"]) assert.equal(g[k],0);
 assert.equal(data.qa.actualNativeNodeTestObserved,false);
 assert.equal(data.qa.originalImagesUploaded,false);
});
