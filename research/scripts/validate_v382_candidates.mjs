#!/usr/bin/env node
/**
 * V3.82 research-only catalog candidate integrity checks.
 * Node.js >=18. No network calls and no repository writes.
 * Usage: node research/scripts/validate_v382_candidates.mjs [--self-test]
 */
import {readFileSync} from "node:fs";
import process from "node:process";

const path="research/data/V3_82_JULY_1536_ZURICH_STGALLEN_CANDIDATES.json";
const d=JSON.parse(readFileSync(path,"utf8"));
const BAD="CH-002121-2-991170609317505501";
const GOOD="CH-002121-2-991170608445805501";
function validate(a){
  const errors=[], fail=(tag)=>errors.push(tag);
  const ev=a.evidence??[], cl=a.candidate_letters??[];
  const ids=new Set(ev.map(x=>x.id));
  const get=(id)=>cl.find(x=>x.id===id);
  if(a.version!=="V3.82"||a.release?.can_ship!==false||a.release?.main_modified!==false)fail("release");
  if(new Set(cl.map(x=>x.id)).size!==4 || cl.length!==4)fail("candidate_ids");
  if(cl.some(c=>!Array.isArray(c.catalog_evidence_ids)||c.catalog_evidence_ids.some(id=>!ids.has(id))))fail("references");
  if(get("V382-L1")?.date!=="1536-07-23"||get("V382-L1")?.public_use!=="BLOCKED"||get("V382-L1")?.catalog_id!==null)fail("july23");
  if(get("V382-L2")?.date!=="1536-07-25"||get("V382-L2")?.catalog_id!==GOOD||get("V382-L2")?.shelfmark!=="Ms S 41, Nr. 33"||get("V382-L2")?.public_use!=="RESEARCH_ONLY")fail("bucer_july25");
  if(get("V382-L3")?.date_precision!=="CATALOG_YEAR_BRACKETED"||get("V382-L3")?.catalog_id!==null||
     get("V382-L3")?.shelfmark!=="Ms S 41, Nr. 31-32"||get("V382-L3")?.public_use!=="RESEARCH_ONLY")fail("bedrot_july25");
  if(JSON.stringify(cl).includes(BAD))fail("retired_id");
  if(cl.some(c=>c.document_examined!==false))fail("facsimile_check");
  if(a.inferences?.some(x=>!x.not_proven || !x.status))fail("inference_caveat");
  const subset=a.research_retrieval_log?.find(x=>x.target?.includes("49 matches"));
  if(!subset||subset.subset_fully_enumerated!==false||subset.matches_individually_audited!==0)fail("false_index_audit");
  if(!a.inferences?.some(x=>x.id==="V382-I4"&&x.status==="UNRESOLVED"))fail("date_merge");
  return errors;
}
const failures=validate(d);
const result={version:d.version,records:d.candidate_letters.length,evidence:d.evidence.length,errors:failures};
if(process.argv.includes("--self-test")){
  const mutants=[
    ["use_retired_ID",x=>x.candidate_letters.find(c=>c.id==="V382-L2").catalog_id=BAD],
    ["publish_july23",x=>x.candidate_letters.find(c=>c.id==="V382-L1").public_use="PUBLIC"],
    ["invent_Bedrot_ID",x=>x.candidate_letters.find(c=>c.id==="V382-L3").catalog_id="invented"],
    ["claim_49_verified",x=>x.research_retrieval_log[0].matches_individually_audited=49],
    ["claim_manuscript_examined",x=>x.candidate_letters.find(c=>c.id==="V382-L2").document_examined=true],
    ["merge_dates",x=>x.inferences.find(i=>i.id==="V382-I4").status="RESOLVED"]
  ];
  result.negative_tests=mutants.map(([name,fn])=>{
    const copy=structuredClone(d);fn(copy);
    return {name,blocked:validate(copy).length>0};
  });
  if(result.negative_tests.some(x=>!x.blocked))failures.push("self_test_failure");
}
console.log(JSON.stringify(result,null,2));
if(failures.length)process.exit(1);
console.log("PASS V3.82: independent dates, candidate provenance, non-publication gates.");
