import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";

const d=JSON.parse(await readFile(fileURLToPath(new URL("../../research/data/ATLAS_V460_CR26_ARTICLE_X_APPARATUS_AND_MARBURG_BASES.json",import.meta.url)),"utf8"));
test("V4.60 critical 1858 print page and apparatus note are located, and not falsely marked as 1540 original",()=>{
  const p=d.sources.CR26_1858;
  assert.equal(p.printedPage,"357");
  assert.equal(p.pdfZeroIndexPage,5);
  assert.equal(p.sourcePhotoDirectlyViewed,true);
  assert.match(p.sourcePhotoRole,/not a 1540 original/);
  assert.equal(d.article10CriticalApparatus.surface1540.original1540LeafRead,false);
  assert.equal(d.article10CriticalApparatus.earlier1531.original1531LeafRead,false);
});
test("V4.60 Article X earlier and later verbs linked to the same critical note, with limits",()=>{
  const a=d.article10CriticalApparatus;
  assert.match(a.editionContext,/note 34/);
  assert.equal(a.surface1540.verbPhrase,"cum pane et vino vere exhibeantur");
  assert.match(a.earlier1531.verbPhrase,/vere adsint, et distribuantur/);
  assert.equal(a.condemnationClause.later.includes("not present"),true);
  assert.ok(a.interpretationHold.length>=3);
});
test("V4.60 introductory edition sigla include 1531 princeps AND separate 1531 modified edition",()=>{
  assert.equal(d.crEditorialWitnesses.length,4);
  assert.deepEqual(d.crEditorialWitnesses.map(x=>x.editionKey),["Ed1","Ed2","Ed3","Ed4"]);
  assert.equal(d.crEditorialWitnesses[0].year,1531);
  assert.equal(d.crEditorialWitnesses[1].year,1531);
  assert.equal(d.crEditorialWitnesses[2].year,1540);
  assert.ok(d.crEditorialWitnesses.every(x=>x.literalTextDirect16cRead===false));
});
test("V4.60 K and Z textual editions have separate source bases; raw manuscript additions not yet transcribed",()=>{
  const k=d.marburgWitnessBase.K;
  const z=d.marburgWitnessBase.Z;
  assert.match(k.shelfmark,/HStAM/);
  assert.match(z.shelfmark,/StAZH/);
  assert.match(k.editionRecommended,/after K/);
  assert.match(z.editionRecommended,/after Z/);
  assert.deepEqual(d.marburgWitnessBase.officialSourceIdentifiesAdditionalArticles,[7,13,15]);
  assert.equal(d.marburgWitnessBase.additionalTextCollatedFromZAndK,false);
  assert.ok(d.marburgWitnessBase.parallelRecommended.some(s=>s.includes("K with Z deviations")));
});
test("V4.60 research release still blocked and bibliographical non-Variata remains distinct",()=>{
  assert.equal(d.humanHistoricalExpertApprovals,0);
  assert.equal(d.realReaderPilotParticipants,0);
  assert.equal(d.canShip,false);
  assert.equal(d.canMergeMain,false);
  assert.equal(d.canImportAIStudio,false);
  assert.ok(d.immediateReaderImplications.some(x=>x.rule.includes("unknown Gruber 1540 non-Variata")));
});
