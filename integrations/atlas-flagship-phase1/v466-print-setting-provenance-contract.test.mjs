import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
async function getJSON(name){return JSON.parse(await readFile(fileURLToPath(new URL("../../research/data/"+name,import.meta.url)),"utf8"));}
const current=await getJSON("ATLAS_V466_ZURICH_1529_PRINT_SETTING_AND_EDITION_COPYTEXT_GATES.json");
const graph=await getJSON("ATLAS_V459_MANUSCRIPT_PRINT_WITNESS_VARIANT_GRAPH.json");

test("V4.66 edition identity distinct from textual identity; accurate old/new viewing state",()=>{
  assert.deepEqual(current.editionObjects.map(x=>x.vd16),["W2118","W2119"]);
  assert.equal(current.editionObjects[0].holding,"ZB Zürich, Zwingli MvK A 81,8");
  assert.equal(current.editionObjects[1].holding,"ZB Zürich, 5.174,5");
  assert.equal(current.editionObjects[0].reopenedInV466,false);
  assert.equal(current.editionObjects[1].reopenedInV466,true);
  assert.equal(current.sourceRegistry.W2118_ORIGINAL.observedCurrentTurn,false);
  assert.equal(current.sourceRegistry.W2119_ORIGINAL.observedCurrentTurn,true);
  assert.ok(current.editionObjects.every(x=>x.physicalCopyPDFSha256===null));
});
test("V4.66 authoritative critical-edition copy-text traces W2119, K and Z separately",()=>{
  const idx=Object.fromEntries(current.editorialSources.map(x=>[x.id,x]));
  assert.equal(idx["ED-ZW6-2-146"].copyTextId,"P1529-W2119");
  assert.equal(idx["ED-LUTHERAN-K-2014"].copyTextId,"M1529-K");
  assert.equal(idx["ED-REFORMED-Z"].copyTextId,"M1529-Z");
  assert.equal(idx["ED-MBW-T3-825"].copyTextId,"M1529-K");
  assert.deepEqual(idx["ED-MBW-T3-825"].additionalVariantIds,["M1529-Z"]);
  assert.equal(idx["ED-1529-WA"].copyTextStatus,"UNRESOLVED_FROM_AVAILABLE_EDITION_INFO");
  assert.ok(current.editorialSources.every(x=>x.mayBeCalledSignedZAutograph===false));
  const graphMap=graph.editorialCopyTextMap_V466;
  assert.equal(graphMap.ZWINGLI_WERKE_6_2_NO_146.baseWitnessId,"P1529-W2119");
  assert.equal(graphMap.REFORMED_CONFESSIONS_1_1_NO11.baseWitnessId,"M1529-Z");
  assert.equal(graphMap.MBW_TEXTE_3_NO_825.variantWitnessId,"M1529-Z");
});
test("V4.66 observed colophon distinction is not elevated into type-setting or chronological proof",()=>{
  const p=current.printingDecisionTree;
  assert.equal(p.colophonDifferenceDocumented,true);
  assert.equal(p.colophonDifferenceAloneDeterminesSetting,false);
  assert.equal(p.sameSettingProved,false);
  assert.equal(p.differentSettingProved,false);
  assert.equal(p.chronologicalPriorityEstablished,false);
  assert.equal(p.copyDirectionEstablished,false);
  assert.equal(p.hypothesesAreNotFindings,true);
  assert.ok(p.sameSettingCriteria.length>=5);
});
test("V4.66 five source-specific textual loci preserve missing line-level measurements",()=>{
  assert.equal(current.comparisonLoci.length,5);
  assert.deepEqual(current.comparisonLoci.map(x=>x.id),[
    "TYPO-A15-TITLE","TYPO-A15-MASS","TYPO-A15-PRESENCE","TYPO-A15-CLOSING","TYPO-SIGNATORY-COLOPHON"
  ]);
  for(const l of current.comparisonLoci){
    assert.equal(l.W2119.observedThisTurn,true);
    assert.equal(l.W2118.observedThisTurn,false);
    assert.ok(l.requires.length>=3 || l.id==="TYPO-SIGNATORY-COLOPHON");
  }
  assert.equal(current.comparisonLoci[4].W2119.printerColophonVisible,true);
  assert.equal(current.comparisonLoci[4].W2118.printerColophonVisible,false);
  assert.equal(current.comparisonLoci[4].W2118.priorV465Reported,true);
});
test("V4.66 official source and editorial source ids trace to verifiable specific URLs",()=>{
  assert.equal(current.sourceRegistry.ZURICH_ARCHIVE.kind,"OFFICIAL_ARCHIVE_CATALOGUE");
  const named=new Set(Object.keys(current.sourceRegistry));
  for(const item of current.editorialSources){
    assert.ok(item.sourceRefs.length>=1);
    for(const id of item.sourceRefs){
      assert.ok(named.has(id),"missing source "+id);
      assert.match(current.sourceRegistry[id].url,/^https:\/\//);
    }
  }
  assert.match(current.editorialSources.find(x=>x.id==="ED-ZW6-2-146").basisSentence,/VD16 W 2119/);
});
test("V4.66 no manuscript or Latin page autopsy, no app integration or shipping",()=>{
  const state=current.currentStudyStatus;
  assert.equal(state.actualLineByLineTextualAlignmentComplete,false);
  assert.equal(state.manuscriptKandZPagesRead,false);
  assert.equal(state.fullPhysicalBookHashesAvailable,false);
  assert.equal(state.expertApprovals,0);
  assert.equal(state.readerPilotParticipants,0);
  assert.equal(state.canShip,false);
  assert.equal(state.canMergeMain,false);
  assert.equal(state.canImportAIStudio,false);
  assert.equal(graph.researchUpdate_V466.typeSettingConclusion,"NOT_ESTABLISHED_FROM_COLOPHON_ALONE");
});
