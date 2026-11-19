import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";

async function load(name){
 return JSON.parse(await readFile(fileURLToPath(new URL("../../research/data/"+name,import.meta.url)),"utf8"));
}
const current=await load("ATLAS_V468_KZ_GMAIL_DRAFTS_AND_ORIGINAL_FACSIMILE_ACCESS_AUDIT.json");
const previous=await load("ATLAS_V467_KZ_AUTOGRAPH_ARCHIVE_ACQUISITION_AND_SOURCE_GATES.json");
const folios=await load("ATLAS_V462_FOUR_PRIMARY_FOLIO_IMAGE_ACQUISITION_REGISTER.json");

test("V4.68 two official recipients have verified Gmail drafts but zero sends",()=>{
 assert.equal(current.verifiedDraftCount,2);
 assert.equal(current.institutionalEnquiries.length,2);
 assert.deepEqual(new Set(current.institutionalEnquiries.map(e=>e.requestId)),new Set(["REQ467-K","REQ467-Z"]));
 assert.deepEqual(new Set(current.institutionalEnquiries.map(e=>e.intendedInstitutionalRecipient)),new Set(["marburg@hla.hessen.de","staatsarchivzh@ji.zh.ch"]));
 for(const e of current.institutionalEnquiries){
  assert.equal(e.status,"DRAFT_PRESENT_IN_CONNECTED_GMAIL_VERIFIED");
  assert.equal(e.draftConfirmedByListing,true);
  assert.equal(e.sent,false);
  assert.equal(e.submittedAsOrder,false);
  assert.equal(e.reproductionFeeApproved,false);
  assert.equal(e.actualArchiveReplyReceived,false);
  assert.match(e.requiredBeforeSending,/User review/);
 }
 assert.equal(current.outgoingMessagesSent,0);
 assert.equal(current.paidArchiveOrders,0);
});

test("V4.68 public GitHub records no private Gmail identifiers or user email",()=>{
 assert.equal(current.safeguards.privateGmailDraftIdsStoredInPublicGithub,false);
 assert.equal(current.safeguards.privateSenderNameOrAccountSavedInPublicGithub,false);
 assert.equal(current.safeguards.originalsOrAttachmentsUploadedToPublicGithub,false);
 const raw=JSON.stringify(current);
 assert.doesNotMatch(raw,/r-6564066187778218122|r-4464073878752214223|nsc\.imp\.atom@gmail\.com/);
});

test("V4.68 1847 contemporary bibliographical citation is not silently equal to 1854 ebook",()=>{
 const early=current.externalSearch.K_Heppe1847Variant;
 const later=current.externalSearch.K_Heppe1854;
 assert.equal(early.identityResolved,false);
 assert.equal(early.manuscriptArticle15Read,false);
 assert.equal(later.fullSpecificManuscriptArticle15PageViewed,false);
 assert.equal(later.reportedDate,"1854");
 assert.ok(early.supportingURLs.length>=2);
 assert.match(early.issue,/1847 and 1854/);
});

test("V4.68 archive digitization and Usteri journal URLs are discovery not direct K/Z reading",()=>{
 assert.equal(current.originalManuscriptImagesReceived,0);
 assert.equal(current.directlyReadKZArticle15AutographImages,0);
 assert.equal(current.externalSearch.Z_Usteri1883.specificFolioImageViewed,false);
 assert.equal(current.externalSearch.archivalK.article15LeafImageViewed,false);
 assert.equal(current.externalSearch.archivalZ.article15LeafImageViewed,false);
 assert.deepEqual(current.externalSearch.archivalZ.additionsCertifiedAtArticles,[7,13,15]);
 assert.equal(previous.sourceOriginalManuscriptPagesActuallyRead,0);
 assert.equal(folios.targets.filter(t=>t.directOriginalLeafViewed).length,0);
});

test("V4.68 separate provenance, copyright, expert and reader gates remain blocked",()=>{
 for(const q of current.institutionalEnquiries)assert.ok(q.requiredFromArchive.length>=3);
 assert.ok(current.openIssues.some(x=>x.includes("1847")));
 assert.equal(current.realHistorianReviews,0);
 assert.equal(current.realReaderPilots,0);
 for(const n of ["canShip","canMergeMain","canImportAIStudio"])assert.equal(current.safeguards[n],false);
 assert.equal(current.safeguards.correspondenceActuallySent,false);
 assert.equal(current.safeguards.publicationRightsAssumed,false);
 assert.equal(current.safeguards.operatingAIStudioModified,false);
});
