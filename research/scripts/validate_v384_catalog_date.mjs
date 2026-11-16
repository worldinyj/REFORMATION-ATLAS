#!/usr/bin/env node
/**
 * REFORMATION-ATLAS V3.84 source-gate validator.
 * Run from repository root:
 *   node research/scripts/validate_v384_catalog_date.mjs [--self-test]
 * Node.js >=18; no external packages, no network or writes.
 */
import {readFileSync} from "node:fs";
import process from "node:process";

const DATA="research/data/V3_84_PARKER_MS119_CATALOG_DATE_COLLATION.json";
export function validate(d) {
  const errors=[];
  const assert=(condition,name)=>{if(!condition)errors.push(name);};
  const e=d.evidence??[];
  const byId=Object.fromEntries(e.map(x=>[x.id,x]));
  assert(d.version==="V3.84","VERSION");
  assert(d.release?.can_ship===false && d.release?.main_edited===false &&
         d.release?.essays_edited===false && d.release?.ai_studio_edited===false,"RELEASE_ISOLATION");
  assert(e.length>=5 && new Set(e.map(x=>x.id)).size===e.length,"EVIDENCE_UNIQUENESS");
  assert(e.every(x=>x.url && x.inspection),"SOURCE_PROVENANCE");
  assert(byId.E01?.dated_text==="pridie Non. Aug. 1566","JAMES_1912_VARIANT");
  assert(byId.E02?.dated_text==="pridie Nonas Augusti 1536","PARKER_MODERN_DATE");
  assert(byId.E03?.scholarly_reference==="Zwingliana XIV p.489","SECONDARY_CROSSREF");
  assert(d.discrepancy?.old_catalog_date==="1566-08-04" &&
         d.discrepancy?.modern_catalog_date==="1536-08-04" &&
         d.discrepancy?.preferred_provisional_date==="1536-08-04","DATE_COLLATION");
  assert(d.discrepancy?.verdict==="PROBABLE_1912_CATALOG_TYPO" &&
         d.discrepancy?.manuscript_date_directly_read===false,"NOT_PRIMARY_CORRECTION");
  assert(d.discrepancy?.latin_calendar?.nones_of_august===5 &&
         d.discrepancy?.latin_calendar?.day_prior===4,"ROMAN_DATE");
  assert(d.target?.manuscript?.includes("MS 119") &&
         d.target?.item_number===71 && d.target?.autograph_examined===false,"SOURCE_IDENTITY");
  assert(d.target?.manuscript_pages?.includes("199-200") &&
         d.target?.manuscript_pages?.some(x=>x.startsWith("205-206")),"CONTINUATION");
  assert(d.material_provenance?.conclusion_on_autograph_or_copy==="UNRESOLVED" &&
         d.material_provenance?.original_image_199_200_checked===false &&
         d.material_provenance?.continued_pages_205_206_checked===false,"NOT_AUTOGRAPH_PROVEN");
  assert(d.access_audit?.length>=3 &&
         d.access_audit.every(x=>x.visual_examined===false),"FACSIMILE_GATE");
  assert(d.identity_gates?.july23_equals_july25==="UNRESOLVED" &&
         d.identity_gates?.august4_to_july25_relation==="UNPROVEN_REPLY" &&
         d.identity_gates?.public_render_all_unverified_relations===false,"NO_FALSE_MERGE");
  assert(d.prior_corrected_catalog_id==="CH-002121-2-991170608445805501","V381_ID_PRESERVED");
  return errors;
}
let data;
try{data=JSON.parse(readFileSync(DATA,"utf8"));}
catch(e){console.error("FAIL load:",e.message);process.exit(2);}
const errors=validate(data);
const result={version:data.version,evidence:data.evidence.length,errors};
if(process.argv.includes("--self-test")){
  const mutants=[
    ["remove_1566_variant",x=>x.evidence.find(z=>z.id==="E01").dated_text="1536"],
    ["publish_data",x=>x.release.can_ship=true],
    ["claim_autograph",x=>x.target.autograph_examined=true],
    ["invent_full_Rott_text",x=>x.access_audit[2].visual_examined=true],
    ["merge_july_dates",x=>x.identity_gates.july23_equals_july25="SAME"],
    ["reverse_letter_date",x=>x.discrepancy.modern_catalog_date="1566-08-04"],
    ["replace_correct_zurich_ID",x=>x.prior_corrected_catalog_id="CH-002121-2-991170609317505501"],
  ];
  result.negative_tests=mutants.map(([name,mutate])=>{
    const x=structuredClone(data);mutate(x);
    return {name,rejected:validate(x).length>0};
  });
  if(result.negative_tests.some(x=>!x.rejected))errors.push("MUTATION_TEST_FAILURE");
}
console.log(JSON.stringify(result,null,2));
if(errors.length)process.exit(1);
console.log("PASS: V3.84 historical catalog variant recorded; release gates closed.");
