#!/usr/bin/env node
/**
 * V3.86 - verify cross-reference provenance and historical claim gates.
 * Run: node research/scripts/validate_v386_rott_crossrefs.mjs [--self-test]
 * Node >=18. No network access; no repository writes.
 */
import fs from "node:fs";
import process from "node:process";

const F="research/data/V3_86_ROTT_P489_P491_SECONDARY_CROSSREFS.json";
const root=JSON.parse(fs.readFileSync(F,"utf8"));

function validate(d) {
  const errors=[], add=(key,ok)=>{if(!ok)errors.push(key);};
  const E=new Map((d.sources??[]).map(x=>[x.id,x]));
  const C=new Map((d.historical_observations??[]).map(x=>[x.id,x]));
  const X=new Map((d.crossreferences??[]).map(x=>[x.id,x]));
  add("VERSION",d.version==="V3.86");
  add("RESEARCH_ISOLATION",d.release?.can_ship===false &&
    d.release?.main_modified===false && d.release?.ai_studio_modified===false &&
    d.release?.essays_513_modified===false && d.release?.emails_sent===false);
  add("SOURCE_IDS", E.size===d.sources?.length && E.size>=5);
  add("CROSSREF_IDS", X.size===d.crossreferences?.length && X.size>=6);
  add("CLAIM_IDS", C.size===d.historical_observations?.length && C.size>=7);
  for(const x of d.crossreferences??[]){
    add(x.id+"_BOTH_SOURCES",E.has(x.secondary_source) && E.has(x.target_source));
    add(x.id+"_RUESCH_PROVENANCE",x.secondary_source==="S386-RUESCH");
    add(x.id+"_SECONDARY_LABEL",x.certainty?.includes("SECONDARY") ||
      x.certainty==="REFERENCE_IN_SECONDARY_STUDY_CONFIRMED");
    add(x.id+"_NO_PRIMARY_IMAGE",x.original_1978_page_seen!==true &&
      x.original_ed_page_seen!==true && x.manuscript_seen!==true);
  }
  for(const c of d.historical_observations??[]){
    add(c.id+"_SOURCE", E.has(c.source_id));
    if(["NOT_VERIFIED","UNRESOLVED"].includes(c.claim_type))
      add(c.id+"_BLOCK",c.public_use==="BLOCKED");
    if(c.public_use==="SOURCE_ATTRIBUTED_REVIEW")
      add(c.id+"_NOT_AUTO_PUBLISHED",d.release.can_ship===false);
  }
  add("ROTT_489",X.get("R386-489")?.target_location==="Zwingliana XIV, p.489" &&
      X.get("R386-489")?.secondary_location?.includes("p.285"));
  add("ROTT_491",X.get("R386-491")?.target_location==="Zwingliana XIV, p.491" &&
      X.get("R386-491")?.secondary_location?.includes("p.286"));
  add("WA_3078",X.get("R386-WA3078")?.target_location?.includes("Nr.3078"));
  add("HARD_BLOCKS",["C386-04","C386-05","C386-06","C386-07"].every(
      id=>C.get(id)?.public_use==="BLOCKED"));
  add("NO_FALSE_ORIGINAL_TRANSCRIPT",d.publication_gate?.prohibit_verbatim_1978_transcription===true &&
      d.publication_gate?.prohibit_parker_original_image_claim===true &&
      d.publication_gate?.prohibit_july_date_merge===true);
  add("SEARCH_LOG_LIMIT",d.source_access_attempts?.length>=3 &&
      d.source_access_attempts.every(x=>x.verified_pdf_page===false));
  add("DO_NOT_SHIP",d.publication_gate?.ship_disabled===true);
  return errors;
}

const errors=validate(root);
const output={version:root.version,source_count:root.sources.length,crossrefs:root.crossreferences.length,
  claim_count:root.historical_observations.length,errors};
if(process.argv.includes("--self-test")){
  const mutants=[
    ["claim_Rott_p489_directly_read",d=>d.crossreferences.find(x=>x.id==="R386-489").original_1978_page_seen=true],
    ["promote_unread_1978",d=>d.historical_observations.find(x=>x.id==="C386-04").public_use="PUBLIC"],
    ["misplace_page491",d=>d.crossreferences.find(x=>x.id==="R386-491").target_location="Zwingliana XIV, p.489"],
    ["assert_original_ms119_read",d=>d.publication_gate.prohibit_parker_original_image_claim=false],
    ["claim_july_identical",d=>d.publication_gate.prohibit_july_date_merge=false],
    ["ship",d=>d.release.can_ship=true],
    ["claim_1983_pdf_image",d=>d.source_access_attempts[2].verified_pdf_page=true]
  ];
  output.negative_tests=mutants.map(([name,mut])=>{
    const d=structuredClone(root);mut(d);
    return {name,rejected:validate(d).length>0};
  });
  if(output.negative_tests.some(x=>!x.rejected))errors.push("UNDETECTED_MUTATION");
}
console.log(JSON.stringify(output,null,2));
if(errors.length)process.exit(1);
console.log("PASS — V3.86 cross-reference matrix preserves source provenance.");
