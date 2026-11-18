import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";

async function load(name){return JSON.parse(await readFile(fileURLToPath(new URL("../../research/data/"+name,import.meta.url)),"utf8"));}
const matrix=await load("ATLAS_V464_W2119_W2108_EARLY_PRINT_PARALLEL_ARTICLES_7_13_15.json");
const graph=await load("ATLAS_V459_MANUSCRIPT_PRINT_WITNESS_VARIANT_GRAPH.json");
const oldTargets=await load("ATLAS_V462_FOUR_PRIMARY_FOLIO_IMAGE_ACQUISITION_REGISTER.json");
const get=id=>matrix.witnesses.find(x=>x.id===id);
const graphGet=id=>graph.witnesses.find(x=>x.id===id);

test("V4.64 two actually seen printed editions are distinct 1529 books from Zurich and Basel",()=>{
 assert.equal(matrix.pairedPrintedEditionsActuallyExamined,2);
 assert.equal(get("P1529-W2119").city,"Zürich");
 assert.equal(get("P1529-W2108").city,"Basel");
 assert.equal(get("P1529-W2119").vd16,"W2119");
 assert.equal(get("P1529-W2108").vd16,"W2108");
 assert.equal(get("P1529-W2119").sourcePixelsViewed,true);
 assert.equal(get("P1529-W2108").sourcePixelsViewed,true);
 assert.deepEqual(get("P1529-W2119").inspectedPdfZeroIndexed,[4,5,6]);
 assert.deepEqual(get("P1529-W2108").inspectedPdfZeroIndexed,[8,10,11]);
 assert.equal(matrix.sourceScreenshotsInspected.length,2);
});

test("V4.64 articles 7, 13, 15 printed propositions found in each viewed edition at explicit pages",()=>{
 assert.equal(matrix.lociCount,4);
 assert.equal(matrix.comparisonLoci.filter(x=>x.article===15).length,2);
 for(const locus of matrix.comparisonLoci){
  assert.equal(locus.readingJudgment,"SAME_PROPOSITION_IN_TWO_1529_PRINTS");
  assert.equal(locus.exactReadingIdentical,"NOT_ESTABLISHED");
  assert.equal(locus.evidence.length,3);
  for(const id of ["P1529-W2108","P1529-W2119"]){
   const x=locus.evidence.find(e=>e.witnessId===id);
   assert.equal(x.status,"DIRECT_PIXEL_EXAMINED");
   assert.ok(Number.isInteger(x.pageIndex0));
   assert.ok(get(id).inspectedPdfZeroIndexed.includes(x.pageIndex0));
   assert.ok(x.anchor.length>15);
   assert.equal(x.completeDiplomaticText,false);
  }
 }
});
test("V4.64 W2118 is the third catalogued, not-inspected Zurich print and no reading invented",()=>{
 const w=get("P1529-W2118");
 assert.equal(w.vd16,"W2118");
 assert.equal(w.shelfmark,"Zwingli MvK A 81,8");
 assert.equal(w.directPrintContentInspected,false);
 assert.equal(w.digitalPDF,null);
 assert.equal(w.inspectedPdfZeroIndexed.length,0);
 for(const locus of matrix.comparisonLoci){
  const missing=locus.evidence.find(e=>e.witnessId===w.id);
  assert.equal(missing.status,"UNVIEWED_NO_TEXT_CLAIM");
  assert.equal(missing.anchor,null);
 }
 assert.equal(graphGet(w.id).article15FullPageRead,false);
});
test("V4.64 revised graph must preserve earlier evidence and never promote signed K/Z",()=>{
 for(const id of ["P1529-W2119","P1529-W2108"]){
  const w=graphGet(id);
  assert.equal(w.printedMainArticle7DirectlyRead,true);
  assert.equal(w.printedMainArticle13DirectlyRead,true);
  assert.equal(w.printedMainArticle15DirectlyRead,true);
  assert.equal(w.fullWitnessCollated,false);
  assert.equal(w.article15FullPageRead,false);
 }
 assert.equal(graphGet("M1529-Z").article15FullPageRead,false);
 assert.equal(graphGet("M1529-K").article15FullPageRead,false);
 assert.equal(oldTargets.targets.filter(t=>t.directOriginalLeafViewed).length,0);
});
test("V4.64 no false direct image hash or scholar/release approval",()=>{
 assert.ok(matrix.witnesses.every(x=>x.imageSha256===null));
 assert.equal(matrix.expertApprovals,0);
 assert.equal(matrix.actualReaderPilotParticipants,0);
 assert.equal(matrix.release.canShip,false);
 assert.equal(matrix.release.canMergeMain,false);
 assert.equal(matrix.release.canImportAIStudio,false);
 assert.ok(matrix.negativeClaims.includes("NO_FULL_DIPLOMATIC_TEXTUAL_COLLATION"));
});
