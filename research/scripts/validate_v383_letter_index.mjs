#!/usr/bin/env node
/**
 * REFORMATION-ATLAS V3.83 – Bucer/Vadian source provenance and index-scope gates.
 *
 * Run from repository root:
 *   node research/scripts/validate_v383_letter_index.mjs [--self-test]
 *
 * Node >=18. No dependencies. No network calls. No writes.
 */
import { readFileSync } from "node:fs";
import process from "node:process";

const fn = "research/data/V3_83_BUCER_VADIAN_EARLY_AUGUST_SOURCE_BRIDGE.json";

export function validate(d) {
  const errors=[];
  const requireTrue=(b,msg)=>{if(!b)errors.push(msg);};
  const L=(id)=>d.letters?.find(x=>x.id===id);
  const sourceIds=new Set(d.sources?.map(x=>x.id)??[]);
  requireTrue(d.version==="V3.83","Expected V3.83");
  requireTrue(d.release?.can_ship===false && d.release?.main_edited===false &&
    d.release?.ai_studio_edited===false && d.release?.mail_sent===false,
    "Release or contact activity must not be inferred");
  requireTrue(new Set(d.sources?.map(x=>x.id)).size===d.sources?.length,
    "Duplicate source ID");
  requireTrue(new Set(d.letters?.map(x=>x.id)).size===d.letters?.length,
    "Duplicate letter ID");
  requireTrue(d.letters?.every(x=>Array.isArray(x.source_ids) &&
    x.source_ids.every(id=>sourceIds.has(id))), "Missing cited source");
  requireTrue(L("V383-L1")?.date==="1536-07-23" &&
    L("V383-L1")?.public_use==="BLOCKED" &&
    L("V383-L1")?.shelfmark===null,"July 23 must stay unresolved");
  requireTrue(L("V383-L2")?.catalog_id==="CH-002121-2-991170608445805501" &&
    L("V383-L2")?.public_use==="RESEARCH_ONLY", "Zurich July 25 catalog ID reverted");
  requireTrue(L("V383-L4")?.date==="1536-08-04" &&
    L("V383-L4")?.sender==="Joachim Vadian" &&
    L("V383-L4")?.recipient==="Martin Bucer" &&
    L("V383-L4")?.public_use==="RESEARCH_ONLY",
    "Cambridge reverse-direction 4 Aug letter unverified");
  requireTrue(d.date_normalization?.latin==="pridie Nonas Augusti 1536" &&
    d.date_normalization?.normalized==="1536-08-04",
    "Roman calendar conversion lost");
  requireTrue(L("V383-N1")?.date.startsWith("1530") &&
    L("V383-N1")?.identity==="DISTINCT_YEAR",
    "1530 negative control merged into 1536");
  requireTrue(d.index_audit?.reported_hits===49 &&
    d.index_audit?.individual_records_obtained===0 &&
    d.index_audit?.all_49_examined===false,
    "49-hit index must not count as 49 audited documents");
  requireTrue(d.letters?.every(x=>x.manuscript_checked===false) &&
    d.qa?.original_1905_p339_examined===false,
    "Undocumented direct manuscript/printed-page inspection");
  requireTrue(d.relations?.every(x=>x.public_render===false &&
    ["UNRESOLVED","NOT_PROVEN","DATES_IN_CATALOGS_ONLY","SCIENTIFIC_INTERPRETATION_NEEDS_TEXT_COMPARE"].includes(x.status)),
    "Unverified links cannot publish");
  requireTrue(d.qa?.july23_vs_july25_resolved===false, "Date identity cannot silently resolve");
  return errors;
}

let data;
try {data=JSON.parse(readFileSync(fn,"utf8"));}
catch(e){console.error("FAIL cannot load V3.83 source data:",e.message);process.exit(2);}
const errors=validate(data);
const result={version:data.version,source_count:data.sources?.length,letter_count:data.letters?.length,errors};
if(process.argv.includes("--self-test")){
  const mutants=[
    ["publish_july23",d=>d.letters.find(x=>x.id==="V383-L1").public_use="PUBLIC"],
    ["restore_bad_zurich_id",d=>d.letters.find(x=>x.id==="V383-L2").catalog_id="CH-002121-2-991170609317505501"],
    ["reverse_cambridge_sender",d=>d.letters.find(x=>x.id==="V383-L4").sender="Martin Bucer"],
    ["claim_49_audited",d=>d.index_audit.individual_records_obtained=49],
    ["merge_1530_into_1536",d=>d.letters.find(x=>x.id==="V383-N1").date="1536-07-17"],
    ["expose_unverified_relation",d=>d.relations[0].public_render=true],
  ];
  result.negative_tests=mutants.map(([name,mutate])=>{
    const x=structuredClone(data);mutate(x);
    return {name,rejected:validate(x).length>0};
  });
  if(result.negative_tests.some(t=>!t.rejected))errors.push("MUTATION_TEST_FAILED");
}
console.log(JSON.stringify(result,null,2));
if(errors.length)process.exit(1);
console.log("PASS V3.83: research-only provenance and identity gates intact.");
