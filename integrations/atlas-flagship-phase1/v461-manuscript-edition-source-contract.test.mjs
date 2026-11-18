import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
const d=JSON.parse(await readFile(fileURLToPath(new URL("../../research/data/ATLAS_V461_KZ_ARTICLES_7_13_15_EDITORIAL_ALIGNMENT_AND_CR26_TEXT_DIFF.json",import.meta.url)),"utf8"));

test("V4.61 exact set of K-vs-Z addition loci retained with clear per-witness limits",()=>{
  assert.deepEqual(d.passages.map(p=>p.article),[7,13,15]);
  for(const passage of d.passages){
    assert.equal(passage.archiveDifference,"Z addition / K omission certified");
    assert.equal(passage.zManuscriptLeafRead,false);
    assert.equal(passage.kManuscriptLeafRead,false);
    assert.equal(passage.exactZOriginalGerman,null);
    assert.equal(passage.exactKOriginalGerman,null);
    assert.equal(passage.alignment,"MODERN_TRANSLATION_CONTAINS_Z_ADDITION_WHILE_LISTING_K_SHELFMARK");
  }
});
test("V4.61 mixed modern HAPuls text is not silently promoted into K diplomatic text",()=>{
  assert.equal(d.provenanceMisassignmentGuard.severity,"HIGH");
  assert.match(d.provenanceMisassignmentGuard.violation,/diplomatic K/);
  assert.ok(d.passages.every(p=>p.sourceIds.includes("HAPULS_TRANSLATION")&&p.sourceIds.includes("STAZH")));
  assert.match(d.sources.HAPULS_TRANSLATION.locator,/G May 1970/);
  assert.match(d.sources.GHDI_DE.witness,/not independently established/);
});
test("V4.61 1883 Z facsimile and K complete digitization links found, no invented images",()=>{
  const z=d.documentDiscovery.find(e=>e.sourceId==="TUEBINGEN_1883");
  const k=d.documentDiscovery.find(e=>e.sourceId==="HAPULS_DIGITIZED_K");
  assert.match(z.status,/TIMED_OUT/);
  assert.match(k.status,/IMAGE_NOT_READ/);
  assert.equal(d.verification.original1529ZArt15PixelViewed,false);
  assert.equal(d.verification.original1529KArt15PixelViewed,false);
});
test("V4.61 Article X variants are editorial CR26 readings, extraction mismatch flagged as OCR not witness",()=>{
  const x=d.materialTextualDiff;
  assert.equal(x.direct16cPageDiffCompleted,false);
  assert.equal(x.earlierEd1Ed2.direct1531OriginalImageRead,false);
  assert.equal(x.laterEd3Ed4.direct1540OriginalImageRead,false);
  assert.match(x.earlierEd1Ed2.reading,/vere adsint, et distribuantur/);
  assert.match(x.laterEd3Ed4.reading,/vere exhibeantur/);
  assert.match(x.laterEd3Ed4.pdfExtractVariant,/exhibeatur/);
  assert.match(x.laterEd3Ed4.visualReview,/OCR/);
});
test("V4.61 research stays blocked even when sources are discoverable",()=>{
  assert.equal(d.verification.historianApprovals,0);
  assert.equal(d.verification.realReaders,0);
  assert.equal(d.release.canShip,false);
  assert.equal(d.release.canMergeMain,false);
  assert.equal(d.release.canImportAIStudio,false);
  assert.equal(d.actualAIStudioModified,false);
  assert.equal(d.sourceHistoricalProseModified,false);
});
