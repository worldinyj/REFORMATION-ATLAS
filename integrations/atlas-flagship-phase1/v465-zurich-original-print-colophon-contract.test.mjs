import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";

async function load(name){return JSON.parse(await readFile(fileURLToPath(new URL("../../research/data/"+name,import.meta.url)),"utf8"));}
const register=await load("ATLAS_V465_ZURICH_W2118_W2119_DIRECT_ARTICLES_AND_COLOPHON_COMPARISON.json");
const witness=await load("ATLAS_V459_MANUSCRIPT_PRINT_WITNESS_VARIANT_GRAPH.json");
const four=await load("ATLAS_V462_FOUR_PRIMARY_FOLIO_IMAGE_ACQUISITION_REGISTER.json");
const get=id=>register.editionWitnesses.find(x=>x.id===id);
const actual=id=>witness.witnesses.find(x=>x.id===id);

test("V4.65 W2118 source accession 291747 resolves authentic original 1529 scanned PDF",()=>{
 const w=get("P1529-W2118");
 assert.equal(w.catalogueRecordId,"291747");
 assert.equal(w.vd16,"W2118");
 assert.equal(w.shelfmark,"Zwingli MvK A 81,8");
 assert.equal(w.pdfPagesTotal,9);
 assert.deepEqual(w.visualPagesZeroIndexed,[3,4,5,6,7]);
 assert.equal(register.sources.W2118_SCAN.url,"https://www.e-rara.ch/zuz/download/pdf/291747");
 assert.equal(register.sources.W2118_IIIF.url,"https://www.e-rara.ch/i3f/v20/291747/manifest");
 assert.equal(actual("P1529-W2118").printedMainArticle15DirectlyRead,true);
});
test("V4.65 two Zürich 1529 prints share Article 15 propositions without pretending complete diplomatic identity",()=>{
 assert.equal(register.observedLoci.length,5);
 for(const id of ["P1529-W2118","P1529-W2119"]){
  assert.equal(get(id).article15Page6Read,true);
  assert.equal(get(id).imageChecksumSha256,null);
  assert.equal(get(id).fullDiplomaticTranscription,false);
  assert.equal(actual(id).fullWitnessCollated,false);
 }
 for(const locus of register.observedLoci.filter(x=>x.article===15)){
  assert.equal(locus.agreement,"SAME_THEOLOGICAL_PROPOSITION");
  assert.equal(locus.literalEquivalence,"NOT_ESTABLISHED_CHARACTER_BY_CHARACTER");
  assert.deepEqual(locus.w2118.pdfPageZeroIndexed,[6]);
  assert.deepEqual(locus.w2119.pdfPageZeroIndexed,[6]);
 }
});
test("V4.65 distinct signatory-page printer colophon is verified but printer priority is not inferred",()=>{
 const w8=get("P1529-W2118"),w9=get("P1529-W2119");
 assert.equal(w8.lastPage7PrintedNames,true);
 assert.equal(w9.lastPage7PrintedNames,true);
 assert.equal(w8.lastPage7PrintedPrinterColophon,false);
 assert.equal(w9.lastPage7PrintedPrinterColophon,true);
 assert.equal(actual("P1529-W2118").printedSignatoryColophonPresent,false);
 assert.equal(actual("P1529-W2119").printedSignatoryColophonPresent,true);
 const col=register.observedLoci.find(x=>x.id==="COLOPHON");
 assert.equal(col.agreement,"PRINTED_IMPRINT_DIFFERENCE");
 assert.equal(col.literalEquivalence,"COLATION_OF_FULL_SETTINGS_REQUIRED");
 assert.ok(register.conclusions.some(x=>x.includes("NOT in itself evidence")));
});
test("V4.65 signed manuscript pair remains uninspected; Basel third print is independent",()=>{
 assert.equal(get("P1529-W2108").city,"Basel");
 assert.equal(get("P1529-W2108").signaturesComparedHere,false);
 assert.equal(register.originalWitnessScope.signedZArticle15PageRead,false);
 assert.equal(register.originalWitnessScope.signedKArticle15PageRead,false);
 assert.equal(actual("M1529-Z").article15FullPageRead,false);
 assert.equal(actual("M1529-K").article15FullPageRead,false);
 assert.equal(four.targets.filter(t=>t.directOriginalLeafViewed).length,0);
});
test("V4.65 no 1531/1540 Latin print collation or release approval automatically granted",()=>{
 assert.equal(register.originalWitnessScope.original1531LatinC4734ArticleXPageRead,false);
 assert.equal(register.originalWitnessScope.original1540LatinC4713ArticleXPageRead,false);
 assert.equal(register.originalWitnessScope.sourceImageHashesCreated,false);
 assert.equal(register.expertApprovals,0);
 assert.equal(register.actualReaderPilotParticipants,0);
 assert.equal(register.release.canShip,false);
 assert.equal(register.release.canMergeMain,false);
 assert.equal(register.release.canImportAIStudio,false);
});
