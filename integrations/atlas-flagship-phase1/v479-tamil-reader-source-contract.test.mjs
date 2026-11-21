import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
const read=p=>readFile(fileURLToPath(new URL(p,import.meta.url)),"utf8");
const p=JSON.parse(await read("../../research/data/ATLAS_V479_VOL06_TAMIL_READER_CANDIDATE.json"));
const base=JSON.parse(await read("../../research/data/V4_50_L1_24_CHAPTER_INTEGRATED_REVISED_MASTER.json"));
const prior=JSON.parse(await read("../../research/data/V4_37_TAMIL_1719_PROVENANCE_ADJUDICATION.json"));
const prose=await read("./V479_VOL06_TAMIL_L0_L1_SOURCE_GROUNDED_KO.md");
const editorial=await read("./V479_TAMIL_EDITORIAL_HISTORICAL_DECISION_KO.md");
const old=base.volumes.find(v=>v.id==="VOL-06").chapters.find(c=>c.id==="L448-06-02");
const sourceIds=new Set(p.sourceRegistry.map(s=>s.id));
const citationIds=markdown=>[...new Set([...markdown.matchAll(/\[(S479-[A-Z0-9-]+)\]/g)].map(x=>x[1]))];
test("V4.79 actually expands one existing VOL06 history chapter with complete written paragraphs",()=>{
 assert.equal(p.volumeId,"VOL-06");
 assert.equal(p.chapterId,"L448-06-02");
 assert.equal(p.legacy.originalBodyMarkdown,old.bodyMarkdown);
 assert.equal(p.legacy.originalBodyChars,old.bodyMarkdown.length);
 assert.deepEqual(p.legacy.sourceUrls,old.sourceUrls);
 assert.deepEqual(p.legacy.crossLinks,old.crossLinks);
 assert.equal(p.newContent.l1SectionCount,8);
 assert.equal((p.newContent.l1Markdown.match(/^### /gm)||[]).length,8);
 assert.equal(p.newContent.l0Markdown.split(/\n\s*\n/).length,4);
 assert.ok(p.newContent.l1Markdown.length>=4500);
 assert.ok(p.newContent.l1Markdown.length>=8*old.bodyMarkdown.length);
 assert.ok(prose.includes(p.newContent.l0Markdown));
 assert.ok(prose.includes(p.newContent.l1Markdown));
});
test("The 1714 fragment, 1715 catalogue copy, 1719 exhibition and 1722 revised record remain separate",()=>{
 assert.deepEqual(p.comparisons.map(x=>x.year),["1706","1714","1715","1719","1722"]);
 assert.equal(p.comparisons[1].sourceId,"S479-HALLE-1714");
 assert.equal(p.comparisons[2].sourceId,"S479-WLB-1715");
 assert.equal(p.comparisons[3].sourceId,"S479-BSI-1719");
 assert.equal(p.comparisons[4].sourceId,"S479-WLB-1722");
 assert.equal(p.independent1719ExemplarIdentified,false);
 assert.equal(prior.determinations.find(x=>x.id==="C437-C").status,"EXHIBIT_ASSERTION_VERIFIED_PHYSICAL_ITEM_UNTRACED");
 assert.equal(prior.determinations.find(x=>x.id==="C437-D").status,"HYPOTHESES_NOT_ESTABLISHED");
 assert.match(p.newContent.l1Markdown,/(?:별도|독립) 소장번호/);
 assert.match(p.newContent.l1Markdown,/지울 수도 확정할 수도/);
});
test("All 10 source records distinguish item-level catalogue, exhibition, scholarship and interpretation",()=>{
 assert.equal(p.sourceRegistry.length,10);
 assert.equal(sourceIds.size,10);
 assert.ok(p.sourceRegistry.every(s=>s.url.startsWith("https://")&&s.kind&&s.readingLimit));
 assert.ok(p.sourceRegistry.every(s=>s.directItemPagesCompared===false));
 assert.equal(p.sourceRegistry.find(s=>s.id==="S479-HALLE-1714").kind,"ORIGINAL_PRINT_CATALOGUE");
 assert.equal(p.sourceRegistry.find(s=>s.id==="S479-BSI-1719").kind,"INSTITUTIONAL_EXHIBITION_NARRATIVE");
 for(const id of citationIds(p.newContent.l0Markdown+p.newContent.l1Markdown))assert.ok(sourceIds.has(id),"Unknown source ID "+id);
 for(const item of p.comparisons)assert.ok(sourceIds.has(item.sourceId));
});
test("Local voices are historic participants, not invented verse-level translation co-authors",()=>{
 assert.match(p.newContent.l1Markdown,/타밀어 교사/);
 assert.match(p.newContent.l1Markdown,/필사자/);
 assert.match(p.newContent.l1Markdown,/알레파/);
 assert.match(p.newContent.l1Markdown,/직접 번역/);
 assert.ok(p.holds.some(x=>x.id==="H479-LOCAL-ROLE"));
 assert.ok(p.claimAudit.some(x=>x.id==="C479-03"&&x.status==="ATTRIBUTION_HELD"));
 assert.ok(p.claimAudit.some(x=>x.id==="C479-13"&&x.highRisk));
});
test("Fifteen individual historical claims are source-anchored and pending real human review",()=>{
 assert.equal(p.claimAudit.length,15);
 const claimIds=p.claimAudit.map(x=>x.id);
 assert.equal(new Set(claimIds).size,15);
 for(const claim of p.claimAudit){
  assert.equal(claim.reviewDecision,"PENDING");
  assert.equal(claim.historianReviewer,null);
  assert.equal(claim.originalObjectFolioCollated,false);
  assert.ok(claim.sourceIds.length>=1&&claim.sourceIds.every(id=>sourceIds.has(id)),claim.id);
 }
 assert.ok(p.claimAudit.filter(x=>x.highRisk).length>=5);
 assert.ok(p.holds.length>=5);
});
test("No production mutation, fake approvals or rights claims; reviewer notes retain 1719 hold",()=>{
 assert.equal(p.expertReviewsCompleted,0);
 assert.equal(p.actualReaderSessions,0);
 assert.equal(p.originalObjectFolioCollationCount,0);
 assert.equal(p.webAppChanges,0);
 assert.ok(Object.values(p.releaseGate).every(v=>v===false));
 assert.match(editorial,/1719년 실제 인쇄/);
 assert.match(prose,/can_ship=false/);
 assert.equal(p.legacy.sourcePath,"research/data/V4_50_L1_24_CHAPTER_INTEGRATED_REVISED_MASTER.json");
});
