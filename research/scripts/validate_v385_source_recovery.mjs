#!/usr/bin/env node
/* REFORMATION-ATLAS V3.85 research integrity checks.
   Run from repository root:
   node research/scripts/validate_v385_source_recovery.mjs --self-test
   No network access; no writes. Node 18+.
*/
import fs from "node:fs";
import process from "node:process";

const file = "research/data/V3_85_ROTT_REPRINT_PARKER_SOURCE_RECOVERY.json";
const raw = JSON.parse(fs.readFileSync(file, "utf8"));
export function check(d) {
  const fail=[];
  const ok=(value,label)=>{if(!value) fail.push(label);};
  ok(d.version==="V3.85", "version");
  ok(d.release?.can_ship===false && d.release?.main_edited===false
    && d.release?.ai_studio_edited===false && d.release?.emails_sent===false, "release");
  ok(d.author?.same_person===true && d.author?.preferred==="Jean Rott"
    && d.author?.aliases?.includes("Hans-Georg Rott"), "author_alias");
  ok(d.author?.bnf==="https://catalogue.bnf.fr/ark:/12148/cb11922721n", "authority");
  ok(d.rott1978?.volume===14 && d.rott1978?.issue===9 &&
    d.rott1978?.target_page===489 && d.rott1978?.fulltext_seen===false
    && d.rott1978?.page489_image_seen===false, "1978_reference");
  ok(d.rott1986?.volume===2 && d.rott1986?.pages==="203-234" &&
    d.rott1986?.scanned_reprint_seen===false &&
    d.rott1986?.page_231_is_unverified_offset_inference===true, "1986_reprint");
  ok(d.parker?.item_number===71 && d.parker?.images_obtained===0 &&
    d.parker?.manifest_opened===false && d.parker?.date_line_in_original_seen===false,
    "parker_facsimile");
  ok(d.parker?.working_date==="1536-08-04" &&
    d.parker?.earlier_catalog_variant==="1566-08-04", "parker_date");
  ok(d.parker?.pages_to_inspect?.join(",")==="199,200,205,206", "noncontinuous_pages");
  ok(d.parker?.original_or_copy==="UNRESOLVED", "material_state");
  ok(d.qa?.identity_gate===false && d.qa?.original_article_gate===false
    && d.qa?.reprint_primary_gate===false && d.qa?.manuscript_primary_gate===false, "gates");
  return fail;
}
const failures = check(raw);
const result={version:raw.version,failures};
if(process.argv.includes("--self-test")){
  const tests = [
    ["split_Jean_and_HansGeorg",x=>x.author.same_person=false],
    ["pretend_1978_p489_read",x=>x.rott1978.page489_image_seen=true],
    ["cite_inferred_1986_p231",x=>x.rott1986.page_231_is_unverified_offset_inference=false],
    ["pretend_manuscript_read",x=>x.parker.images_obtained=4],
    ["incorrect_date_variant",x=>x.parker.earlier_catalog_variant="1536-08-04"],
    ["publish_without_sources",x=>x.release.can_ship=true],
    ["claim_original_or_copy",x=>x.parker.original_or_copy="AUTOGRAPH"]
  ];
  result.negative_tests=tests.map(([name,fn])=>{
    const copy=structuredClone(raw);fn(copy);
    return {name,rejected:check(copy).length>0};
  });
  if(result.negative_tests.some(t=>!t.rejected))failures.push("mutation_tests_failed");
}
console.log(JSON.stringify(result,null,2));
if(failures.length)process.exit(1);
console.log("PASS: publication and provenance gates remain closed.");
