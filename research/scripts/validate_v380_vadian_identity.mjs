#!/usr/bin/env node
/**
 * REFORMATION-ATLAS V3.80 historical identity gate.
 * Usage:
 *   node research/scripts/validate_v380_vadian_identity.mjs
 *   node research/scripts/validate_v380_vadian_identity.mjs --self-test
 *   node research/scripts/validate_v380_vadian_identity.mjs path/to/data.json
 * Node.js >= 18; no network access, no dependencies, no repository writes.
 * V3.81 correction: correct Kalliope Bucer/Vadian record id 991170608445805501; previous 991170609317505501 belongs to the next Bullinger/Blarer entry.
 */
import fs from "node:fs";
import path from "node:path";
import process from "node:process";

export function validate(d) {
  const errors=[];
  const fail=(tag,message)=>errors.push(tag+": "+message);
  const ids=arr=>new Set(arr).size===arr.length;
  if(d?.version!=="V3.80")fail("VERSION","expected V3.80");
  if(d?.release?.can_ship!==false || d?.release?.main_modified!==false ||
     d?.release?.ai_studio_modified!==false)fail("RELEASE","research data must remain isolated");
  const evidence=d?.evidences??[];
  const findings=d?.research_findings??[];
  const candidates=d?.candidates??[];
  const edges=d?.identity_edges??[];
  const evSet=new Set(evidence.map(x=>x.id));
  const canSet=new Set(candidates.map(x=>x.id));
  if(!ids(evidence.map(x=>x.id)) || !ids(candidates.map(x=>x.id)) ||
     !ids(findings.map(x=>x.id)))fail("DUPLICATE","reused source/claim/candidate ids");
  for(const f of findings){
    if(!f.evidence?.length || !f.evidence.every(x=>evSet.has(x)))fail(f.id,"uncited finding");
  }
  for(const ev of evidence)if(!ev.url || !ev.inspection || !ev.limits)fail(ev.id,"missing provenance");
  const july23=candidates.find(x=>x.id==="BVC-15360723");
  const july25=candidates.find(x=>x.id==="BVC-15360725");
  const aug06=candidates.find(x=>x.id==="BVC-15360806");
  if(!july23 || !july25 || !aug06)fail("CANDIDATES","missing one of three document candidates");
  if(july23 && (july23.publication_gate!=="BLOCKED"||july23.autograph_checked!==false||
      july23.date_checked!==false || july23.verified_catalog_identifier!==null))
    fail("JULY23","must stay blocked until original is established");
  if(july25 && (july25.publication_gate!=="RESEARCH_ONLY"||
      july25.catalog_identifier!=="CH-002121-2-991170608445805501"||
      july25.signature!=="Ms S 41, Nr. 33"||
      july25.autograph_checked!==false))fail("JULY25","catalog does not establish an inspected autograph");
  if(aug06 && (aug06.letter_number!=="HBBW 875"||
      aug06.publication_gate!=="EDITORIAL_ATTRIBUTION_ONLY"))
    fail("AUG06","Bullinger document misassigned");
  if(!edges.some(x=>x.from==="BVC-15360723" && x.to==="BVC-15360725" &&
      x.resolution==="UNRESOLVED" && x.public_render===false))
    fail("DATE_COLLISION","July 23/25 must never be auto-merged");
  if(edges.some(x=>x.relation.startsWith("POSSIBLE_") && x.public_render!==false))
    fail("UNVERIFIED_EDGE","potential links may not be published");
  if(d?.source_acquisition_log?.some(x=>x.image_verified!==false))
    fail("FACSIMILE","source image unverified; cannot claim inspection");
  if(d?.qa_targets?.safe_to_release!==false ||
     d?.qa_targets?.candidate_identity_resolved!==false)
    fail("PUBLISH","release/identity gate must remain closed");
  const signatureMismatch=d?.not_identical_identifiers?.some(pair=>
    pair.includes("Zürich ZB Ms S 41, Nr. 33") &&
    pair.includes("St Gallen VadSlg Ms 41:33")
  );
  if(!signatureMismatch)fail("SHELF_MARK","distinct institutional signatures must not be conflated");
  return errors;
}
const root=path.resolve("research/data/V3_80_VADIAN_BUCER_IDENTITY_HARD_GATES.json");
const args=process.argv.slice(2);
const file=path.resolve(args.find(x=>x!=="--self-test") ?? root);
let data;
try {data=JSON.parse(fs.readFileSync(file,"utf8"));} catch(e) {
  console.error("FAIL: cannot read research dataset:",e.message);
  process.exit(2);
}
const errors=validate(data);
const result={version:data.version,candidates:data.candidates?.length,evidences:data.evidences?.length,
  findings:data.research_findings?.length,errors};
if(args.includes("--self-test")){
  const mutants=[
    ["promote_July23",d=>d.candidates.find(c=>c.id==="BVC-15360723").publication_gate="PUBLIC"],
    ["merge_July23_July25",d=>d.identity_edges.find(e=>e.to==="BVC-15360725").resolution="SAME"],
    ["mark_facsimile_as_checked",d=>d.source_acquisition_log[0].image_verified=true],
    ["confuse_Zurich_StGallen_shelfmarks",d=>d.not_identical_identifiers=[]],
  ];
  result.negative_tests=mutants.map(([label,mutate])=>{
    const clone=structuredClone(data);mutate(clone);
    return {label,rejected:validate(clone).length>0};
  });
  if(result.negative_tests.some(x=>!x.rejected))errors.push("SELF_TEST: mutation not rejected");
}
console.log(JSON.stringify(result,null,2));
if(errors.length)process.exit(1);
console.log("PASS: V3.80 non-publication integrity gates hold.");
