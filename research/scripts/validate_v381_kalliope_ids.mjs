#!/usr/bin/env node
/**
 * V3.81 Kalliope catalog ID and research-publication guard.
 * Node 18+, no network, no writes. Run from repository root:
 *   node research/scripts/validate_v381_kalliope_ids.mjs
 *   node research/scripts/validate_v381_kalliope_ids.mjs --self-test
 */
import {readFileSync} from "node:fs";
import process from "node:process";

const WRONG = "CH-002121-2-991170609317505501";
const CORRECT = "CH-002121-2-991170608445805501";
const paths = {
  v77:"research/data/V3_77_BUCER_VADIAN_DATE_COLLISION_AUDIT.json",
  v78:"research/data/V3_78_BUCER_VADIAN_ARCHIVAL_GATE.json",
  v79:"research/data/V3_79_BUCER_VADIAN_CLAIM_EVIDENCE.json",
  v80:"research/data/V3_80_VADIAN_BUCER_IDENTITY_HARD_GATES.json",
  v81:"research/data/V3_81_CATALOG_ID_CORRECTION_AND_ARCHIVE_LEAD.json",
};
const load=(p)=>JSON.parse(readFileSync(p,"utf8"));
let files;
try{files=Object.fromEntries(Object.entries(paths).map(([k,p])=>[k,load(p)]));}
catch(e){console.error("FAIL: Cannot load research data:",e.message);process.exit(2);}

export function validate(F){
  const failures=[];
  const check=(cond,msg)=>{if(!cond)failures.push(msg);};
  const exact=CORRECT;
  check(F.v77?.pivotal_finding?.catalog_entry_id===exact,"V3.77 Bucer ID mismatch");
  check(F.v78?.confirmed?.catalog_1536_07_25?.identifier===exact,"V3.78 Bucer ID mismatch");
  check(F.v79?.evidence?.find(e=>e.id==="E04")?.catalog_id===exact,"V3.79 Bucer source E04 mismatch");
  check(F.v80?.evidences?.find(e=>e.id==="S380-01")?.lookup_id===exact,"V3.80 Bucer source S380-01 mismatch");
  check(F.v80?.candidates?.find(c=>c.id==="BVC-15360725")?.catalog_identifier===exact,"V3.80 Bucer candidate mismatch");
  check(F.v80?.candidates?.find(c=>c.id==="BVC-15360723")?.publication_gate==="BLOCKED","Unverified July 23 claim promoted");
  check(F.v80?.identity_edges?.filter(e=>e.from==="BVC-15360723" && e.to==="BVC-15360725")
   ?.every(e=>e.resolution==="UNRESOLVED" && e.public_render===false),"July 23/25 collision illegally resolved");
  const items=F.v81?.critical_correction?.verified_assignment;
  check(Array.isArray(items) && items.length===2,"V3.81 two catalog records missing");
  check(items?.[0]?.id===CORRECT && items?.[0]?.heading?.includes("Joachim Vadianus") &&
        items?.[0]?.heading?.includes("Martin Bucer") && items?.[0]?.printed_date==="1536.07.25",
        "Corrected ID not linked to Bucer/Vadian July 25");
  check(items?.[1]?.id===WRONG && items?.[1]?.heading?.includes("Ambrosius Blarer") &&
        items?.[1]?.heading?.includes("Bullinger") && items?.[1]?.printed_date==="1547.08.24",
        "Old ID not mapped to Bullinger/Blarer 1547");
  check(F.v81?.unchanged_historical_constraints?.july23_july25_same_item==="UNRESOLVED",
        "Date collision must stay unresolved");
  check(F.v81?.publication?.promotable_now===false && F.v81?.publication?.main_edited===false &&
        F.v81?.publication?.ai_studio_edited===false,"Research data incorrectly publishable");
  for(const [k,v] of Object.entries(F)){
    if(k==="v81")continue;
    const correction=v.catalog_id_amendment;
    check(correction?.corrected_bucer_vadian_identifier===CORRECT &&
          correction?.formerly_misattributed_identifier===WRONG,k+" missing correction audit");
    // Retired ID is allowed only in the audit field; never in active references.
    const shallow={...v};delete shallow.catalog_id_amendment;
    check(!JSON.stringify(shallow).includes(WRONG),k+" still contains retired ID in active research fields");
  }
  return failures;
}
const issues=validate(files);
const output={version:"V3.81",errors:issues};
if(process.argv.includes("--self-test")){
  const mutations=[
    ["restore_wrong_v77_id",f=>f.v77.pivotal_finding.catalog_entry_id=WRONG],
    ["restore_wrong_v80_candidate",f=>f.v80.candidates.find(c=>c.id==="BVC-15360725").catalog_identifier=WRONG],
    ["publish_July23",f=>f.v80.candidates.find(c=>c.id==="BVC-15360723").publication_gate="PUBLISHED"],
    ["incorrectly_merge_dates",f=>f.v80.identity_edges.find(e=>e.to==="BVC-15360725").resolution="SAME"],
    ["swap_canonical_record",f=>f.v81.critical_correction.verified_assignment[0].id=WRONG]
  ];
  output.negative_tests=mutations.map(([name,mutate])=>{
    const copy=structuredClone(files);mutate(copy);
    return {name,rejected:validate(copy).length>0};
  });
  if(output.negative_tests.some(t=>!t.rejected))issues.push("Mutation guard failed");
}
console.log(JSON.stringify(output,null,2));
if(issues.length)process.exit(1);
console.log("PASS — catalog IDs corrected, July identity unresolved, release held.");
