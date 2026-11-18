import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
import {REQUIRED_PRIMARY_TARGETS, checkOriginalFolio, evaluateFourFolios} from "./primary-source-evidence-gate.mjs";

const data=JSON.parse(await readFile(fileURLToPath(new URL("../../research/data/ATLAS_V462_FOUR_PRIMARY_FOLIO_IMAGE_ACQUISITION_REGISTER.json",import.meta.url)),"utf8"));
const clone=()=>JSON.parse(JSON.stringify(data));
test("V4.62 has exactly four independently traced signed-manuscript and Latin print loci",()=>{
 assert.equal(data.targets.length,4);
 assert.deepEqual(new Set(data.targets.map(t=>t.id)),new Set(REQUIRED_PRIMARY_TARGETS));
 assert.equal(data.targets.filter(t=>t.witnessKind==="SIGNED_MANUSCRIPT").length,2);
 assert.equal(data.targets.filter(t=>t.witnessKind==="EARLY_PRINTED_LATIN_BOOK").length,2);
 for(const t of data.targets){
   assert.ok(t.sourceLinks.length>=2);
   for(const source of t.sourceLinks)assert.match(source.url,/^https:\/\//);
   assert.ok(t.requiredEvidence.length>=3);
 }
});
test("V4.62 no current 16th-century article leaf can be quoted as directly checked",()=>{
 const r=evaluateFourFolios(data);
 assert.equal(r.directFolioCount,0);
 assert.equal(r.article15PairedReady,false);
 assert.equal(r.articleXPairedReady,false);
 assert.equal(r.originalPageTextComparisonReady,false);
 assert.ok(r.checks.every(t=>t.blockers.includes("DIRECT_ORIGINAL_PAGE_NOT_INSPECTED")));
 assert.equal(r.canShip,false);
 assert.equal(r.canImportAIStudio,false);
});
test("V4.62 catalogue metadata, spinner and PDF timeout do not qualify as original page evidence",()=>{
 const known=data.targets.find(t=>t.id==="T462-K-ART15");
 assert.match(known.viewerReachability,/UNAVAILABLE/);
 assert.equal(known.articleSpecificLeaf,null);
 assert.equal(known.originalImageSha256,null);
 assert.ok(data.targets.find(t=>t.id==="T462-Z-ART15").lastBlockingCondition.includes("timed out"));
 const alt=data.targets.find(t=>t.id==="T462-L1540-ARTX");
 assert.match(alt.copyIdentityGoogleVsPitts,/UNVERIFIED/);
 assert.equal(alt.diplomaticLatinText,null);
});
test("V4.62 even invented hash and text cannot pass without exact folio and human QC",()=>{
 const t={...data.targets[0],directOriginalLeafViewed:true,originalImageSha256:"a".repeat(64),diplomaticGermanText:"SYNTHETIC TEST TEXT"};
 const r=checkOriginalFolio(t);
 assert.equal(r.directlyCitable,false);
 assert.ok(r.blockers.includes("EXACT_PAGE_OR_CANVAS_MISSING"));
 assert.ok(r.blockers.includes("TRANSCRIPTION_HUMAN_QC_MISSING"));
});
test("V4.62 synthetic complete fixture tests readiness logic but never clears historical release gate",()=>{
 const synthetic=clone();
 for(const t of synthetic.targets){
   t.directOriginalLeafViewed=true;
   t.originalImageSha256="a".repeat(64);
   t.leafOrCanvas="SYNTHETIC_PAGE_1";
   if(t.witnessKind==="SIGNED_MANUSCRIPT")t.diplomaticGermanText="SYNTHETIC GERMAN TEXT";
   else t.diplomaticLatinText="SYNTHETIC LATIN TEXT";
   t.transcriptionReview="HUMAN_QC_PASS";
 }
 const ready=evaluateFourFolios(synthetic);
 assert.equal(ready.directFolioCount,4);
 assert.equal(ready.article15PairedReady,true);
 assert.equal(ready.articleXPairedReady,true);
 assert.equal(ready.canShip,false);
 assert.equal(ready.canMergeMain,false);
 assert.equal(ready.canImportAIStudio,false);
 synthetic.targets[3].selectedSourceKind="GOOGLE_ALTERNATE";
 const unverified=evaluateFourFolios(synthetic);
 assert.equal(unverified.directFolioCount,3);
 assert.equal(unverified.articleXPairedReady,false);
 assert.ok(unverified.checks[3].blockers.includes("PRINT_EDITION_IDENTITY_UNVERIFIED"));
 assert.throws(()=>evaluateFourFolios({...synthetic,targets:synthetic.targets.slice(1)}),/four distinct/);
});
