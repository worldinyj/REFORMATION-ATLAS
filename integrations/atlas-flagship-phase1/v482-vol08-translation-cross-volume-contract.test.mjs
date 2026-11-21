import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
const read=p=>readFile(fileURLToPath(new URL(p,import.meta.url)),"utf8");
const p=JSON.parse(await read("../../research/data/ATLAS_V482_TRANSLATION_LOCAL_RECEPTION_READER_CANDIDATE.json"));
const master=JSON.parse(await read("../../research/data/V4_50_L1_24_CHAPTER_INTEGRATED_REVISED_MASTER.json"));
const portfolio=JSON.parse(await read("../../research/data/ATLAS_V478_EIGHT_VOLUME_BASELINE_AND_PRIORITIES.json"));
const church=JSON.parse(await read("../../research/data/ATLAS_V480_VOL02_JINGJIAO_READER_CANDIDATE.json"));
const tamil=JSON.parse(await read("../../research/data/ATLAS_V479_VOL06_TAMIL_READER_CANDIDATE.json"));
const korean=JSON.parse(await read("../../research/data/ATLAS_V481_VOL07_KOREAN_CHURCH_READER_CANDIDATE.json"));
const gates=JSON.parse(await read("../../research/data/V4_44_GO_NO_GO_MASTER_GATE_REGISTER.json"));
const md=await read("./V482_VOL08_THEME06_TRANSLATION_LOCAL_RECEPTION_KO.md");
const review=await read("./V482_VOL08_T6_EDITION_WITNESS_AND_COMPARISON_DECISION_KO.md");
const old=master.volumes.find(v=>v.id==="VOL-08").chapters.find(c=>c.id==="L448-08-03");
const volumes={"VOL-02":church,"VOL-06":tamil,"VOL-07":korean};
const ids=new Set(p.sources.map(s=>s.id));
const citations=t=>[...new Set([...t.matchAll(/\[(S\d{3}-[A-Z0-9-]+)\]/g)].map(m=>m[1]))];

test("V4.82 explicitly expands only T6 while leaving the original VOL08 dual-theme chapter untouched",()=>{
 assert.equal(p.volumeId,"VOL-08");assert.equal(p.chapterId,"L448-08-03");
 assert.equal(p.themeId,"T6");assert.equal(p.focus,"ONE_OF_SIX_THEMES_ONLY");
 assert.equal(p.legacy.originalBodyMarkdown,old.bodyMarkdown);
 assert.equal(p.legacy.originalBodyChars,old.bodyMarkdown.length);
 assert.deepEqual(p.legacy.originalCrossLinks,old.crossLinks);
 assert.deepEqual(p.legacy.originalSourceUrls,old.sourceUrls);
 assert.equal(p.reader.l0ParagraphCount,4);assert.equal(p.reader.l0Markdown.split(/\n\s*\n/).length,4);
 assert.equal(p.reader.l1SectionCount,10);assert.equal((p.reader.l1Markdown.match(/^### /gm)||[]).length,10);
 assert.ok(p.reader.l1Markdown.length>=5500);
 assert.ok(p.reader.l1Markdown.length>=7*old.bodyMarkdown.length);
 assert.ok(md.includes(p.reader.l0Markdown));
 assert.ok(md.includes(p.reader.l1Markdown));
});
test("Three original research candidates are still linked and retain their identities and unapproved state",()=>{
 assert.equal(p.sourceCandidateProvenance.length,3);
 assert.deepEqual(p.sourceCandidateProvenance.map(x=>x.volumeId),["VOL-02","VOL-06","VOL-07"]);
 assert.deepEqual(p.sourceCandidateProvenance.map(x=>x.chapterId),["L448-02-02","L448-06-02","L448-07-02"]);
 for(const link of p.sourceCandidateProvenance){
  assert.ok(link.gitBlobSha&&link.sourcePath);
  assert.ok(Object.values(link.releaseGate).every(x=>x===false));
  assert.equal(link.historianSignoff,false);
 }
});
test("Fifteen source cards only reuse verbatim URL and kind of the original relevant research candidate",()=>{
 assert.equal(p.sources.length,15);assert.equal(ids.size,15);
 for(const s of p.sources){
  const origin=volumes[s.originVolumeId];
  assert.ok(origin,"Unknown source volume "+s.originVolumeId);
  const prior=origin.sourceRegistry.find(x=>x.id===s.id);
  assert.ok(prior,"Source is not in its own prior volume: "+s.id);
  assert.equal(s.url,prior.url);assert.equal(s.kind,prior.kind);
  assert.equal(s.originSourceItemId,s.id);
  assert.equal(s.sourceAlreadyReviewedByHistorian,false);
  assert.ok(s.url.startsWith("https://")&&s.limitation);
 }
 assert.ok(citations(p.reader.l0Markdown+"\n"+p.reader.l1Markdown).length>=12);
 assert.ok(citations(p.reader.l0Markdown+"\n"+p.reader.l1Markdown).every(x=>ids.has(x)));
});
test("Actual VOL02 → VOL06 → VOL07 → VOL08 path matches existing chapter IDs, not a fabricated source stemma",()=>{
 const theme=portfolio.canonicalNavigation.themes.find(x=>x.id==="T6");
 assert.ok(theme);assert.deepEqual(p.chapterIdCoverage,theme.chapterIds);
 assert.deepEqual(p.readerStops.map(x=>x.volumeId),["VOL-02","VOL-06","VOL-07","VOL-08"]);
 assert.deepEqual(p.readerStops.map(x=>x.chapterId),theme.chapterIds);
 assert.ok(p.readerStops.every(s=>s.sourceIds.every(id=>ids.has(id))));
 for(const s of p.readerStops){
  assert.ok(master.volumes.find(v=>v.id===s.volumeId).chapters.some(c=>c.id===s.chapterId));
 }
 assert.equal(p.editorialBridges.length,3);
 assert.ok(p.editorialBridges.every(e=>e.type.endsWith("_NOT_CAUSATION")));
 assert.match(p.reader.l1Markdown,/직접.*계보/);
 assert.ok(p.holds.some(h=>h.id==="H482-CAUSE"));
});
test("China's retrospectively reported 635, stele built 781 and later rubbing are not collapsed into Bible editions",()=>{
 assert.deepEqual(p.chronology.slice(0,3).map(x=>x.time),["635","638","781"]);
 assert.equal(p.chronology[0].classification,"EVENT_REPORTED_LATER");
 assert.equal(p.chronology[2].classification,"MONUMENT_PRODUCTION");
 assert.equal(p.comparisonRows[0].region,"당나라 중국");
 assert.match(p.comparisonRows[0].textKind,/기념비/);
 assert.match(p.reader.l1Markdown,/성경 전권의 중국어 판본/);
 assert.ok(p.sources.some(x=>x.id==="S480-SMITH"&&x.kind==="RUBBING_OBJECT_CATALOGUE"));
});
test("1719 Tamil physical witness remains unresolved, and Korea's 1900/1906/1911 stages stay distinct",()=>{
 const tamilChron=p.chronology.filter(x=>x.volumeId==="VOL-06");
 const koreanChron=p.chronology.filter(x=>x.volumeId==="VOL-07");
 assert.deepEqual(tamilChron.map(x=>x.time),["1706","1714","1715","1719","1722"]);
 assert.equal(tamilChron.find(x=>x.time==="1719").classification,"UNRESOLVED_INSTITUTIONAL_CLAIM");
 assert.deepEqual(koreanChron.slice(-3).map(x=>x.time),["1900","1906","1911"]);
 assert.notEqual(koreanChron[4].classification,koreanChron[5].classification);
 assert.ok(p.holds.some(x=>x.id==="H482-TAMIL-1719"));
 assert.match(p.reader.l1Markdown,/인도성서공회/);
 assert.match(p.reader.l1Markdown,/공인역본/);
});
test("All 18 cited research claims are pending real specialist review and correspond to actual source cards",()=>{
 assert.equal(p.claimAudit.length,18);
 assert.equal(new Set(p.claimAudit.map(x=>x.id)).size,18);
 assert.equal(p.holds.length,9);
 for(const x of p.claimAudit){
  assert.equal(x.reviewDecision,"PENDING");
  assert.equal(x.historianReviewer,null);
  assert.equal(x.originalPhysicalTextCollated,false);
  assert.ok(x.sourceIds.length&&x.sourceIds.every(id=>ids.has(id)),x.id);
 }
 assert.ok(p.claimAudit.filter(x=>x.highRisk).length>=8);
 assert.equal(p.comparisonRows.length,3);
 assert.ok(p.comparisonRows.every(x=>x.citation));
});
test("All nine upstream specialist dockets remain unsubmitted; no fake reader, rights or host approval",()=>{
 const expected=gates.highRiskAndSecondaryReviews.filter(x=>x.targetVolumeIds.some(y=>["VOL-02","VOL-06","VOL-07","VOL-08"].includes(y)));
 assert.equal(p.reviewDockets.length,9);
 assert.equal(expected.length,9);
 for(const x of expected){
  const y=p.reviewDockets.find(z=>z.id===x.id);
  assert.ok(y,x.id);assert.equal(y.status,"NOT_SUBMITTED");
  assert.equal(y.actualReviewerCount,0);assert.deepEqual(y.claimIds,x.claimIds);
 }
 assert.equal(p.empiricalReview.historianApprovals,0);
 assert.equal(p.empiricalReview.actualReaderSessions,0);
 assert.equal(p.empiricalReview.physicalSourceCollations,0);
 assert.equal(p.empiricalReview.licenseApprovals,0);
 assert.equal(p.empiricalReview.appDeployments,0);
 assert.equal(p.empiricalReview.mainChanged,false);
 assert.ok(Object.values(p.releaseGate).every(x=>x===false));
 assert.match(review,/can_ship=false/);
 assert.match(md,/can_ship=false/);
});
