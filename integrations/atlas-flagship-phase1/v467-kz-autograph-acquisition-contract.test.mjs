import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";

const load=async name=>JSON.parse(await readFile(fileURLToPath(new URL("../../research/data/"+name,import.meta.url)),"utf8"));
const acquisition=await load("ATLAS_V467_KZ_AUTOGRAPH_ARCHIVE_ACQUISITION_AND_SOURCE_GATES.json");
const oldTarget=await load("ATLAS_V462_FOUR_PRIMARY_FOLIO_IMAGE_ACQUISITION_REGISTER.json");
const graph=await load("ATLAS_V459_MANUSCRIPT_PRINT_WITNESS_VARIANT_GRAPH.json");
const by=id=>acquisition.targetWitnesses.find(t=>t.id===id);

test("V4.67 exact original K/Z and official contact paths cannot be confused with 1529 printed books",()=>{
 assert.equal(acquisition.targetWitnesses.length,2);
 assert.deepEqual(new Set(acquisition.targetWitnesses.map(t=>t.id)),new Set(["K","Z"]));
 assert.equal(by("K").witnessId,"M1529-K");
 assert.equal(by("Z").witnessId,"M1529-Z");
 assert.match(by("K").shelfmark,/3 Nr\. 245/);
 assert.equal(by("Z").shelfmark,"StAZH E I 3.1, Nr. 54");
 assert.equal(by("K").contact.address,"marburg@hla.hessen.de");
 assert.equal(by("Z").contact.address,"staatsarchivzh@ji.zh.ch");
 assert.equal(acquisition.primaryPrintsAreNotSignedAutographs,true);
 assert.ok(graph.witnesses.find(w=>w.id==="M1529-K"));
 assert.ok(graph.witnesses.find(w=>w.id==="M1529-Z"));
});

test("V4.67 both institutions have corroborated reproduction rules and cost consent remains false",()=>{
 for(const t of acquisition.targetWitnesses){
   assert.ok(t.archiveRequest.status==="DRAFT_NOT_SENT");
   assert.equal(t.archiveRequest.sentAt,null);
   assert.equal(t.archiveRequest.replyReceivedAt,null);
   assert.equal(t.archiveRequest.objectDelivered,false);
   assert.equal(t.archiveRequest.consentToCosts,false);
   assert.ok(acquisition.sourceRegistry[t.contact.verifiedBySource]?.url.startsWith("https://"));
   assert.ok(t.requestFields.usage.length>20);
 }
 assert.equal(by("Z").contact.orderProcedure,"FORMAL_SIGNED_REPRODUCTION_ORDER_REQUIRED");
 assert.match(by("Z").contact.officialFormUrl,/reproformular_2025_05_01\.pdf/);
});

test("V4.67 K/Z facsimile and editor copy text are discovery leads, not original autograph images",()=>{
 assert.equal(acquisition.scholarlySourceAccess.sources.length,6);
 for(const t of acquisition.targetWitnesses){
   assert.ok(t.facsimiles.length>=2);
   assert.ok(t.facsimiles.every(f=>f.article15SpecificFolioImageRead===false));
   assert.equal(t.targetEvidence.art15PixelRead,false);
   assert.equal(t.targetEvidence.originalImageSha256,null);
   assert.equal(t.targetEvidence.diplomaticGermanArt15,null);
   assert.equal(t.targetEvidence.independentHumanTranscriptionReview,false);
 }
 assert.ok(by("K").facsimiles.some(f=>f.reference.includes("Heppe")));
 assert.ok(by("Z").facsimiles.some(f=>f.reference.includes("Usteri")));
 assert.ok(acquisition.scholarlySourceAccess.sources.some(f=>f.editionId==="ED-MBW-K+Z"&&f.variantWitness==="Z"));
});

test("V4.67 all three historically documented additional loci stay uncollated in autograph K/Z",()=>{
 assert.deepEqual(acquisition.manuscriptVariantLoci.map(l=>l.article),[7,13,15]);
 for(const locus of acquisition.manuscriptVariantLoci){
   assert.equal(locus.catalogueStatesZAddition,true);
   assert.equal(locus.KoriginalText,null);
   assert.equal(locus.ZoriginalText,null);
   assert.equal(locus.fullOriginalGermanCollated,false);
 }
 assert.equal(acquisition.sourceOriginalManuscriptPagesActuallyRead,0);
 assert.equal(acquisition.requestsActuallySent,0);
});

test("V4.67 linked V4.62 original folio targets remain held, not automatically upgraded by letters",()=>{
 for(const [targetId,requestId] of [["T462-K-ART15","REQ467-K"],["T462-Z-ART15","REQ467-Z"]]){
   const t=oldTarget.targets.find(t=>t.id===targetId);
   assert.equal(t.directOriginalLeafViewed,false);
   assert.equal(t.originalImageSha256,null);
   assert.equal(t.archiveAcquisitionRequestV467.requestId,requestId);
   assert.equal(t.archiveAcquisitionRequestV467.requestStatus,"DRAFT_NOT_SENT");
   assert.equal(t.archiveAcquisitionRequestV467.financialApproval,false);
 }
 assert.equal(oldTarget.targets.filter(t=>t.directOriginalLeafViewed).length,0);
});

test("V4.67 source provenance and release gates prevent publication of unreviewed facsimiles",()=>{
 for(const s of Object.values(acquisition.sourceRegistry)){
   assert.match(s.url,/^https:\/\//);
   assert.ok(s.classification.length>8);
 }
 assert.equal(acquisition.release.canShip,false);
 assert.equal(acquisition.release.canMergeMain,false);
 assert.equal(acquisition.release.canImportAIStudio,false);
 assert.equal(acquisition.expertsApproved,0);
 assert.equal(acquisition.actualReaderParticipants,0);
 assert.ok(acquisition.filesPlannedForDigitalReceipts.includes("do not publish"));
});
