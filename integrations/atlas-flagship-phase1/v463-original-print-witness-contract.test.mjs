import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
async function load(name) {return JSON.parse(await readFile(fileURLToPath(new URL("../../research/data/"+name,import.meta.url)),"utf8"));}
const evidence=await load("ATLAS_V463_W2119_1529_PRINT_ART13_ART15_DIRECT_SCAN_EVIDENCE.json");
const witness=await load("ATLAS_V459_MANUSCRIPT_PRINT_WITNESS_VARIANT_GRAPH.json");
const targets=await load("ATLAS_V462_FOUR_PRIMARY_FOLIO_IMAGE_ACQUISITION_REGISTER.json");
const w=witness.witnesses.find(x=>x.id==="P1529-W2119");

test("V4.63 actual photographed 1529 printed page has exact institutional edition identity and page loci",()=>{
 assert.equal(evidence.bibliography.editionId,"VD16 W2119");
 assert.equal(evidence.bibliography.holdingInstitution,"Zentralbibliothek Zürich");
 assert.equal(evidence.bibliography.shelfmark,"5.174,5");
 assert.equal(evidence.bibliography.primaryScanPdf,"https://www.e-rara.ch/zuz/download/pdf/170052");
 assert.deepEqual(evidence.inspection.pagesActuallyRead,[5,6]);
 assert.equal(evidence.observations[0].pdfPageIndex0,5);
 assert.equal(evidence.observations[1].pdfPageIndex0,6);
 assert.equal(evidence.observations.every(x=>x.directPhotoViewed),true);
});
test("V4.63 new primary-page reading updates graph beyond catalogue but not autograph witness K or Z",()=>{
 assert.equal(w.printedMainArticle13DirectlyRead,true);
 assert.equal(w.printedMainArticle15DirectlyRead,true);
 assert.ok(w.originalPDFPageIndicesInspected.includes(5) && w.originalPDFPageIndicesInspected.includes(6)); // Later research may add further verified pages.
 assert.equal(w.fullWitnessCollated,false);
 assert.equal(w.article15FullPageRead,false);
 assert.equal(witness.witnesses.find(x=>x.id==="M1529-K").article15FullPageRead,false);
 assert.equal(witness.witnesses.find(x=>x.id==="M1529-Z").article15FullPageRead,false);
 assert.equal(evidence.sourceRelationship.directionOfDependenceBetweenZAndW2119,"UNRESOLVED");
});
test("V4.63 document reports mass clause and disputed bodily presence within printed Article 15",()=>{
 const a=evidence.observations.find(x=>x.article==="15");
 assert.ok(a.observedPrintedSegments.some(x=>x.role==="MASS_CLAUSE"));
 assert.ok(a.observedPrintedSegments.some(x=>x.role==="BODILY_PRESENCE_NONAGREEMENT"));
 assert.ok(a.observedPrintedSegments.some(x=>x.role==="SHARED_COMMUNION_AND_CHARITY"));
 assert.equal(a.handwrittenAnnotationsFullyTranscribed,false);
 assert.equal(a.printedTextDiplomaticTranscriptionCompleted,false);
});
test("V4.63 1529 print does not falsely complete four different 16th century direct-leaf targets",()=>{
 assert.equal(targets.targets.length,4);
 assert.equal(targets.targets.filter(x=>x.directOriginalLeafViewed).length,0);
 assert.equal(targets.additionalIndependentOriginalEraPrintInspections.length,1);
 const addition=targets.additionalIndependentOriginalEraPrintInspections[0];
 assert.equal(addition.id,"P1529-W2119");
 assert.equal(addition.countsTowardFourSignedAndLatinTargetFolios,false);
 assert.equal(addition.imageBinarySha256,null);
 assert.equal(evidence.bibliography.pdfBinarySha256,null);
});
test("V4.63 research not promoted to finished original collation or production",()=>{
 assert.equal(evidence.counts.independentHistorianReviewers,0);
 assert.equal(evidence.counts.requiredFourOriginalFolioTargetsOfV462Read,0);
 assert.equal(evidence.sourceRelationship.article7AddedTextVisibleInW2119,"NOT_YET_VERIFIED");
 assert.equal(evidence.release.canShip,false);
 assert.equal(evidence.release.canMergeMain,false);
 assert.equal(evidence.release.canImportAIStudio,false);
});
