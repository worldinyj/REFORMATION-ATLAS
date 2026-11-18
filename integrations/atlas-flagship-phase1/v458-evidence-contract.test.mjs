import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
async function json(path){return JSON.parse(await readFile(fileURLToPath(new URL(path,import.meta.url)),"utf8"));}
const matrix=await json("../../research/data/ATLAS_V458_HIGH_RISK_TEXTUAL_BIBLIOGRAPHIC_EVIDENCE_MATRIX.json");
const registry=await json("../../research/data/ATLAS_V457_CLAIM_SOURCE_CRITICAL_REGISTER.json");

test("V4.58 all ten historical HIGH claims receive traceable edition-level evidence",()=>{
 const high=registry.claims.filter(c=>c.risk==="HIGH");
 assert.equal(high.length,10);
 const highIds=new Set(high.map(c=>c.id));
 assert.equal(matrix.claimCoverage.totalHighRisk,10);
 const covered=new Set(matrix.evidence.flatMap(e=>e.claimIds));
 assert.equal(matrix.evidenceCount,14);
 for(const id of highIds)assert.ok(covered.has(id),"Missing: "+id);
 for(const id of covered)assert.ok(highIds.has(id),"Unrecognized HIGH claim: "+id);
 assert.equal(matrix.claimCoverage.uncoveredHighRisk.length,0);
});

test("V4.58 each evidence unit has a supported URL, archive locator, confidence limits and no approval",()=>{
 const ids=new Set();
 for(const e of matrix.evidence){
  assert.ok(!ids.has(e.id));ids.add(e.id);
  assert.ok(e.locator.length>12);
  assert.ok(e.verified.length>30);
  assert.ok(e.limit.length>20);
  assert.ok(e.sourceIds.length>0);
  assert.ok(e.anchorTokens.length>0);
  for(const id of e.sourceIds)assert.match(matrix.sourceRegistry[id]?.url||"",/^https:\/\//,"Broken source: "+id);
 }
 assert.equal(matrix.independentExpertReviews,0);
 assert.equal(matrix.release.canShip,false);
 assert.equal(matrix.release.canImportAIStudio,false);
});

test("V4.58 Marburg German art. 15 separates common belief from bodily-presence nonagreement",()=>{
 const part1=matrix.evidence.find(e=>e.id==="EV458-01");
 const part2=matrix.evidence.find(e=>e.id==="EV458-02");
 assert.ok(part1.sourceIds.includes("GHDI_DE"));
 assert.ok(part1.anchorTokens.includes("gaistliche niessung"));
 assert.ok(part2.anchorTokens.includes("leiblich im Brot und wein"));
 assert.ok(part2.limit.includes("Avoid back-projecting"));
 assert.match(matrix.sourceRegistry.GHDI_DE.locator,/WA 30\/III/);
});

test("V4.58 1531 catalogues and 1540 variants remain distinguishable",()=>{
 const wittenberg=matrix.evidence.find(e=>e.id==="EV458-04");
 const german=matrix.evidence.find(e=>e.id==="EV458-06");
 const unnumbered=matrix.evidence.find(e=>e.id==="EV458-10");
 const grammar=matrix.evidence.find(e=>e.id==="EV458-08");
 const originalArticle10=matrix.evidence.find(e=>e.id==="EV458-09");
 assert.ok(wittenberg.anchorTokens.includes("Witebergae"));
 assert.ok(german.anchorTokens.includes("November 1531"));
 assert.equal(unnumbered.disposition,"CATALOGUE_REPORT_CONFIRMED_OBJECT_ID_HOLD");
 assert.ok(unnumbered.limit.includes("absent"));
 assert.ok(grammar.anchorTokens[0].includes("Apologia Confessionis diligenter recognita"));
 assert.ok(originalArticle10.anchorTokens.includes("vere adsint et distribuantur"));
 assert.ok(originalArticle10.anchorTokens.includes("cum pane et vino vere exhibeantur"));
 assert.ok(matrix.evidence.find(e=>e.id==="EV458-11").sourceIds.includes("PITTS"));
});

test("V4.58 later confessional framing stays on hold, never auto-promotes",()=>{
 const reception=matrix.evidence.find(e=>e.id==="EV458-13");
 const retrospective=matrix.evidence.find(e=>e.id==="EV458-14");
 assert.equal(reception.disposition,"EXPERT_REVIEW_HOLD");
 assert.equal(retrospective.disposition,"INTERPRETATION_HOLD");
 assert.equal(matrix.release.canMergeMain,false);
});
