import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const data = JSON.parse(await readFile(fileURLToPath(new URL("../../research/data/ATLAS_V469_HEPPE_BIBLIOGRAPHY_AND_MARBURG_VARIANT_HISTORIOGRAPHY.json", import.meta.url)), "utf8"));
const by = id => data.sources.find(s => s.id === id);

test("1847 contemporary advertisements and bibliographies are not confused with a directly seen Heppe title page", () => {
 for (const id of ["H47-R", "H47-A", "H47-S"]) {
  const s = by(id);
  assert.equal(s.dateOfPublication,"1847");
  assert.equal(s.searchableTextRead,true);
  assert.equal(s.pdfPixelsRead,false);
 }
 assert.equal(by("H47-R").directHeppeTitlePageRead,false);
 assert.equal(by("H47-A").directHeppeTitlePageRead,false);
 assert.equal(by("H47-S").reviewBodyRead,false);
 assert.match(by("H47-S").possibleContentsTypo,/1829/);
});
test("1854 catalogue and 1847 imprint are unresolved identities, not silently united", () => {
 assert.equal(by("H54-G").catalogueYear,"1854");
 assert.equal(by("H54-G").actualPrintedImprintViewed,false);
 assert.equal(by("H54-G").samePhysicalEditionAs1847,null);
 assert.equal(data.decision.resolveImprintEditionIdentity,false);
 assert.equal(data.decision.needPhysicalTitlePages,true);
});
test("Schubert interpretation and archive catalogue do not substitute for Z/K manuscript images", () => {
 assert.equal(by("HS09").statementIsAuthorInterpretation,true);
 assert.equal(by("HS09").originalKZManuscriptsRead,false);
 assert.deepEqual(by("ZCAT").additionArticles,[7,13,15]);
 assert.equal(by("ZCAT").actualAutographLeavesRead,false);
 assert.equal(data.sourceSeparation.currentWorkAutographArticle15ImagesRead,0);
 assert.equal(data.sourceSeparation.printedWitnesses1529AreNotSignedAutographs,true);
});
test("No Gmail sending, archive purchase, or publication permission implied", () => {
 assert.equal(data.correspondence.newMessagesSentThisVersion,0);
 assert.equal(data.correspondence.newOrdersPlacedThisVersion,0);
 assert.equal(data.correspondence.explicitSendApprovalFromUser,false);
 assert.equal(data.safeguard.privateGmailDataPublished,false);
});
test("Fail-closed product, AI Studio, historian and reader gates", () => {
 for(const k of ["canShip","canMergeMain","canImportAIStudio","mainModified","operatingAppModified","previousHistoricalProseModified"]) assert.equal(data.safeguard[k],false);
 assert.equal(data.sourceSeparation.historiansApproved,0);
 assert.equal(data.sourceSeparation.readerParticipants,0);
 assert.equal(data.sourceSeparation.originalLatinPrintArticle10ImagesRead,0);
});
