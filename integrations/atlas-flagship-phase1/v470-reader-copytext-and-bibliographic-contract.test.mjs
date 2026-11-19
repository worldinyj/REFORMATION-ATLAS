import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
const path=new URL("../../research/data/ATLAS_V470_W2119_ART15_TRANSLATION_GAP_AND_HEPPE_EDITION_CANDIDATE.json",import.meta.url);
const data=JSON.parse(await readFile(fileURLToPath(path),"utf8"));
const by=id=>data.sourceRegistry.find(s=>s.id===id);
test("W2119 original print p6 and p7 are actually seen and separately identified",()=>{
 assert.equal(by("P-W2119-ART15").pageIndexZeroBased,6);
 assert.equal(by("P-W2119-COLOPHON").pageIndexZeroBased,7);
 assert.equal(by("P-W2119-ART15").directlyViewedThisSession,true);
 assert.equal(by("P-W2119-COLOPHON").directlyViewedThisSession,true);
 assert.equal(data.sourceBoundaries.printedSignatureNamesAreNotAutographInk,true);
});
test("GHDI edited translation differs at mass clause; no fake manuscript genealogical conclusion",()=>{
 assert.equal(by("E-GHDI-ART15").massClauseVisibleInThisTranslation,false);
 assert.match(by("E-GHDI-ART15").editorialCopyText,/WA 30 III/);
 assert.equal(data.claims.find(c=>c.id==="C470-02").entailsKZAutographGenealogy,false);
 assert.equal(data.sourceBoundaries.modernEditedTranslationIsNotPrint,true);
});
test("Historical Schaff 1847 and 1854 second-edition attestation does not fake original Heppe title pages",()=>{
 const s=by("B-SCHAFF-1847-1854");
 assert.equal(s.claims[1],"2d ed. 1854");
 assert.equal(s.heppeTitlePagesDirectlyViewed,false);
 assert.equal(data.sourceBoundaries.heppe1847OriginalTitlePageRead,false);
 assert.equal(data.sourceBoundaries.heppe1854OriginalTitlePageRead,false);
 assert.equal(by("B-GPLAY-1854").editionStatementOnPhysicalTitlePageVerified,false);
});
test("All six research claims have explicit existing evidence references without pretending expert review",()=>{
 assert.equal(data.claims.length,6);
 const ids=new Set(data.sourceRegistry.map(s=>s.id));
 for(const claim of data.claims){
  assert.ok(claim.support.length>=1);
  assert.ok(claim.support.every(id=>ids.has(id)));
  assert.equal(claim.humanExpertApproved,false);
 }
 assert.deepEqual(by("A-Z-K").catalogueReportsZAdditionsArticles,[7,13,15]);
 assert.equal(by("A-Z-K").autographLeavesDirectlyRead,false);
});
test("L0/L1 candidate created but original/autograph and release gates strictly fail closed",()=>{
 assert.equal(data.readerDraft.l0Present,true);
 assert.equal(data.readerDraft.l1Present,true);
 assert.equal(data.sourceBoundaries.signedAutographKArticle15Read,false);
 assert.equal(data.sourceBoundaries.signedAutographZArticle15Read,false);
 assert.equal(data.sourceBoundaries.w2118W2108FreshlyReadThisSession,false);
 for(const key of ["canShip","canMergeMain","canImportAIStudio","mainModified","realAIStudioModified","productionHistoricalProseModified"]) assert.equal(data.reviewGates[key],false);
 assert.equal(data.reviewGates.historianApprovals,0);
 assert.equal(data.reviewGates.readerParticipants,0);
 assert.equal(data.privacy.emailsSentThisVersion,0);
 assert.equal(data.privacy.archiveOrdersPlacedThisVersion,0);
});
