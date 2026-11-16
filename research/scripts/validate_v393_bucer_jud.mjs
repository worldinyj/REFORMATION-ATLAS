#!/usr/bin/env node
/** V3.93 reproducible no-network research proof gates. Usage: node research/scripts/validate_v393_bucer_jud.mjs --self-test */
import {readFileSync} from "node:fs";
const validate=function validate(d){
 const e=[],r=d.release||{},src=d.sources||[],ev=d.evidence||[],rr=d.resolved_identification||{},claims=d.claim_gates||[],ct=d.existing_content_targets||[],ins=d.proposed_reviewer_inserts||[],ms=d.manuscript_targets||[],guard=d.inherited_guards||{};
 if(d.version!=="V3.93"||d.status!=="RESEARCH_DRAFT"||d.based_on!=="V3.92")e.push("metadata");
 for(const k of ["can_ship","main_modified","essays_513_modified","ai_studio_modified","external_inquiries_sent","reader_drafts_published"])
  if(r[k]!==false)e.push("release_"+k);
 if(src.length!==6||new Set(src.map(v=>v.id)).size!==6||src.some(v=>v.historical_folio_seen!==false))e.push("source_register");
 if(ev.length!==6||new Set(ev.map(v=>v.id)).size!==6)e.push("evidence_length");
 const byid=Object.fromEntries(ev.map(v=>[v.id,v]));
 if(byid["E393-01"]?.date_literal!=="1532-07 [retrospective month]"||
   byid["E393-01"]?.can_assert_identical_to_june23!==false||
   byid["E393-02"]?.stated_date!=="1532-05-23"||
   byid["E393-03"]?.stated_date!=="1532-06-23"||
   byid["E393-03"]?.stated_number!=="150"||
   byid["E393-04"]?.stated_date!=="1532-06-23"||
   byid["E393-04"]?.stated_number!=="598")e.push("variants");
 if(byid["E393-05"]?.reply_to_date!=="1532-06-23"||
  byid["E393-05"]?.archive_for_bucer_letter!=="Staatsarchiv Zürich E II 345, 126–141"||
  byid["E393-05"]?.archive_image_seen!==false)e.push("hbbw_locator");
 if(byid["E393-06"]?.edition_ref!=="Bucer Briefwechsel VIII Nr.581, pp.23-28"||
    byid["E393-06"]?.original_edition_page_seen!==false)e.push("earlier_letter");
 if(rr.preferred_date!=="1532-06-23"||
    rr.preferred_critical_edition!=="Bucer, Briefwechsel VIII Nr.598 pp.150-165"||
    rr.prior_year_july_same_letter!=="PROBABLE_EDITORIAL_IDENTIFICATION_NOT_ORIGINAL_LITERAL_DATE"||
    rr.actual_june23_manuscript_seen!==false||
    rr.original_bucer_briefwechsel_vol8_598_page_image_seen!==false||
    rr.early_may_letter_nr581_is_not_nr598!==true)e.push("identification");
 if(claims.length!==6||claims.filter(v=>v.allowed==="BLOCKED").length!==3||claims.find(c=>c.id==="C393-04")?.status!=="UNRESOLVED")e.push("claim_gates");
 if(ct.length!==5||JSON.stringify(ct.map(x=>x.id))!==JSON.stringify(["MEDIUM-MARBURG","MEDIUM-ZWINGLI","MEDIUM-AUGSBURG","OV-E-018","OV-E-019"])||
    ct.some(z=>z.existing_file_modified!==false))e.push("target_map");
 if(ins.length!==3||ins.some(v=>v.status!=="REVIEW_ONLY"||v.published!==false||!v.body||!ct.some(c=>c.id===v.target)))e.push("drafts");
 if(ms.length!==3||ms.some(z=>z.direct_folio_seen!==false))e.push("manuscript_guard");
 if(guard.rott_1978_pdf_verified!==false||guard.rott_489_491_images_seen!==false||guard.parker_ms119_original_images_seen!==false||
   guard.bucer_vadian_1536_07_23_equals_07_25!=="UNRESOLVED"||
   guard.zurich_kalliope_corrected_id!=="CH-002121-2-991170608445805501")e.push("inherited_hard_gates");
 return e;
};
const mutations=[["promote_pdf",d=>d.inherited_guards.rott_1978_pdf_verified=true],
["merge_1536",d=>d.inherited_guards.bucer_vadian_1536_07_23_equals_07_25="PROVEN"],
["replace_may",d=>d.evidence[1].stated_date="1532-06-23"],
["number_rewrite",d=>d.evidence[2].stated_number="598"],
["lose_latin_july",d=>d.evidence[0].date_literal="1532-06-23"],
["invent_same_letter",d=>d.evidence[0].can_assert_identical_to_june23=true],
["fake_hbbw_folio",d=>d.evidence[4].archive_image_seen=true],
["fake_primary_vol8",d=>d.resolved_identification.original_bucer_briefwechsel_vol8_598_page_image_seen=true],
["pretend_article_published",d=>d.proposed_reviewer_inserts[0].published=true],
["rewrite_existing",d=>d.existing_content_targets[0].existing_file_modified=true],
["new_independent_source",d=>d.sources[1].id=d.sources[0].id],
["wrong_archive",d=>d.manuscript_targets[0].direct_folio_seen=true],
["promote_claim",d=>d.claim_gates[3].status="PROVEN"],
["unblock_release",d=>d.release.can_ship=true],
["outreach_sent",d=>d.release.external_inquiries_sent=true]];
const filename=process.argv.find(x=>x.endsWith(".json"))||"research/data/V3_93_BUCER_JUD_EDITION_VARIANT_READER_TARGETS_DRAFT.json";
const data=JSON.parse(readFileSync(filename,"utf8"));
const errs=validate(data);
if(errs.length){console.error("FAIL",errs);process.exit(1);}
console.log("PASS: V3.93 source, edition date, reference number, witness, reader and release gates");
if(process.argv.includes("--self-test")) {
  let rejected=0;for(const [name,change] of mutations){const bad=JSON.parse(JSON.stringify(data));change(bad);if(!validate(bad).length){console.error("MUTATION MISSED",name);process.exit(1)}rejected++;}
  console.log(`PASS: ${rejected}/${mutations.length} fault injections rejected`);
}
