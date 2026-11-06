import test from "node:test";
import assert from "node:assert/strict";
import {assertFrozenInputs, buildEffectiveOverviews, validateGraph, buildOutputs, loadAll} from "../../scripts/build_v323_chronology_navigation.mjs";
const clone=x=>structuredClone(x);
function fixture(){
  const x=loadAll();assertFrozenInputs(x.contract);
  const catalog=x.v307.catalogue;
  const effective=buildEffectiveOverviews(x.base,x.v305,x.v307,x.v310,catalog);
  return {x,catalog,effective};
}
test("frozen inputs, full 97 navigation, 513 catalogue and 156 validated links",()=>{
  const {x,catalog,effective}=fixture();
  assert.equal(catalog.length,513);
  assert.equal(effective.entries.length,97);
  assert.deepEqual(effective.stats,{DIRECT_TOPIC:78,PARTIAL_COVERAGE:19,BACKGROUND_ONLY:0,NO_MATCH:0});
  assert.equal(effective.entries.reduce((n,v)=>n+v.reader_links.length,0),156);
  assert.equal(new Set(effective.entries.flatMap(v=>v.reader_links.map(r=>r.reader_id))).size,107);
  assert.equal(effective.overviews.get("OV-D-017").mapping_status,"PARTIAL_COVERAGE");
  assert.ok(effective.overviews.get("OV-D-017").reader_links.some(v=>v.reader_id==="DOCUMENT-METHODIST_GENERAL_RULES1743"));
  assert.equal(x.contract.guardrails.full_corpus_factual_audit,false);
});
test("26 anchored timeline events, provenance, precision and witnesses",()=>{
  const {x,catalog,effective}=fixture();
  const valid=validateGraph(x.contract,effective,catalog,x.upstream);
  assert.equal(valid.events.size,26);assert.equal(valid.witness.size,10);
  const outputs=buildOutputs(x.contract,effective,catalog,valid);
  assert.deepEqual(Object.keys(outputs),x.contract.artifact_contract);
  assert.equal(outputs["v323_curated_event_timeline.json"].ordered_navigation_edges.length,22);
  assert.equal(outputs["v323_overview_97_reading_index.json"].count,97);
  assert.equal(outputs["v323_513_reader_catalogue_index.json"].count,513);
  for(const o of Object.values(outputs))assert.equal(o.publication_ready,false);
});
test("a fake reader link in the chronology is rejected",()=>{
  const {x,catalog,effective}=fixture(),altered=clone(x.contract);
  altered.events[0].reader_ids.push("PERSON-NONEXISTENT");
  assert.throws(()=>validateGraph(altered,effective,catalog,x.upstream),/Dangling reader/);
});
test("a mistaken date role is rejected against frozen V322 events",()=>{
  const {x,catalog,effective}=fixture(),altered=clone(x.contract);
  altered.events.find(e=>e.id==="V323-E13").date="1564-01-26";
  assert.throws(()=>validateGraph(altered,effective,catalog,x.upstream),/Expected values to be strictly equal/);
});
test("year-only printed 1649 witness must not be given a false exact rank",()=>{
  const {x,catalog,effective}=fixture(),altered=clone(x.contract);
  altered.paths.find(p=>p.id==="V323-P03").ordered_event_ids.push("V323-E21");
  assert.throws(()=>validateGraph(altered,effective,catalog,x.upstream),/Precision-sensitive|Duplicate event/);
});
test("Spanish-Dutch January Münster cannot become Imperial-French IPM",()=>{
  const {x,catalog,effective}=fixture(),altered=clone(x.contract);
  altered.events.find(e=>e.id==="V323-E15").work="IPM";
  assert.throws(()=>validateGraph(altered,effective,catalog,x.upstream),/Expected values to be strictly equal/);
});
test("different treaty witnesses cannot be promoted to same-work edition revisions",()=>{
  const {x,catalog,effective}=fixture(),altered=clone(x.contract);
  altered.witness_relations.find(r=>r.id==="V323-REL05").type="EDITION_REVISION";
  assert.throws(()=>validateGraph(altered,effective,catalog,x.upstream),/Expected values to be strictly equal/);
});
test("reference exclusions and upstream overlay mapping are fail-closed",()=>{
  const {x,catalog}=fixture(),base=clone(x.base);
  const person=base.entries.find(e=>e.overview_id==="OV-P-001");
  person.reader_links.push({reader_id:"PERSON-IGNATIUS",role:"PRIMARY"});
  assert.throws(()=>buildEffectiveOverviews(base,x.v305,x.v307,x.v310,catalog),/Forbidden conflation|Unknown reader/);
});
