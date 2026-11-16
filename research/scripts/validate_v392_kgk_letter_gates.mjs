#!/usr/bin/env node
/** V3.92 reproducible read-only research gates; no external calls or writes. */
import { readFileSync } from "node:fs";
const validate=function validate(x){
 const errors=[];
 if(x.version!=="V3.92"||x.status!=="RESEARCH_DRAFT")errors.push("draft_meta");
 for(const k of ["can_ship","main_modified","essays_513_modified","ai_studio_modified","outreach_sent","reader_narrative_published"]){
  if(x.public_release?.[k]!==false)errors.push("release_"+k);
 }
 const rott=x.rott_1978||{};
 if(rott.current_article_link!==null||rott.current_pdf_link!==null||rott.pdf_sha256!==null||
   rott.pdf_original_verified!==false||rott.printed_489_checked!==false||rott.printed_491_checked!==false||
   JSON.stringify(rott.target_pages)!=="[489,491]")errors.push("rott_primary_witness");
 const sources=x.source_registry||[], ids=new Set(sources.map(s=>s.id));
 if(sources.length!==7||ids.size!==7)errors.push("sources");
 if(sources.some(s=>s.manuscript_image_seen!==false))errors.push("unearned_facsimile");
 if(sources.filter(s=>s.grade==="DIRECTLY_READ_CRITICAL_EDITION_TRANSCRIPTION_NOT_FACSIMILE").length!==1||
    sources.find(s=>s.id==="S392-KGK339-TEXT")?.read_method!=="WEB_HTML_TEXT")errors.push("edited_primary_grade");
 const events=x.event_crosswalk||[];
 if(events.length!==8||new Set(events.map(e=>e.id)).size!==8)errors.push("event_count");
 const direct=events.filter(e=>e.can_quote_event_primary);
 if(direct.length!==1||direct[0]?.id!=="T392-1533-05-08"||
    direct[0]?.source!=="S392-KGK339-TEXT"||direct[0]?.source_grade!=="DIRECT_EDITED_TRANSCRIPTION")errors.push("primary_event_scope");
 if(events.find(e=>e.id==="T392-LOST-1532-06-24")?.lost!==true||
    events.find(e=>e.id==="T392-LOST-1532-06-24")?.source_grade!=="LOST_LETTER_RECONSTRUCTED_FROM_OTHER_WITNESS")errors.push("lost_letter");
 if(events.find(e=>e.id==="T392-1536-08-04")?.can_quote_event_primary!==false||
    events.find(e=>e.id==="T392-1536-08-04")?.source_grade!=="SECONDARY_REFERENCE_ONLY_NOT_RECHECKED_HERE")errors.push("do_not_promote_1536");
 const dd=x.date_discrepancies||[];
 if(dd.length!==3||dd.find(q=>q.id==="D392-1532-JUNE-JULY")?.textual_retrospective!=="1533-05-08 KGK339 letter says prior year in July"||
    dd.find(q=>q.id==="D392-1532-JUNE-JULY")?.editorial_identification!=="1532-06-23 Bucer to Leo Jud"||
    dd.find(q=>q.id==="D392-1536-JULY")?.same_letter!=="UNRESOLVED"||
    dd.find(q=>q.id==="D392-1536-AUG")?.original_manuscript_date_line_seen!==false)errors.push("separate_date_discrepancies");
 const claim=x.page_claims||[];
 if(claim.length!==5||claim.filter(c=>c.public_status==="BLOCKED").length!==2||
    claim.find(c=>c.claim_id==="C392-04")?.public_status!=="BLOCKED"||
    claim.find(c=>c.claim_id==="C392-05")?.public_status!=="BLOCKED")errors.push("original_claim_block");
 if((x.archive_witnesses_for_kgk339||[]).length!==4||
   x.archive_witnesses_for_kgk339.some(q=>q.physical_image_seen!==false))errors.push("editor_versus_folio");
 if(x.technical_access?.original_rott_pdf_file_acquired!==false||
    x.technical_access?.publisher_contact_message_sent!==false||
    x.technical_access?.current_url_guesses_accepted!==false)errors.push("access");
 if(x.reviewer_ready_narrative?.status!=="REVIEW_ONLY_NOT_PUBLISHED"||
   x.corrected_zurich_catalog_id!=="CH-002121-2-991170608445805501")errors.push("review_guard");
 return errors;
};
const mutations=[["ship",x=>{x.public_release.can_ship=true;}],
["fake_pdf",x=>{x.rott_1978.pdf_original_verified=true;}],
["fake_489",x=>{x.rott_1978.printed_489_checked=true;}],
["promote_1536",x=>{x.event_crosswalk[7].can_quote_event_primary=true;}],
["claim_missing_folio",x=>{x.archive_witnesses_for_kgk339[0].physical_image_seen=true;}],
["lost_is_autograph",x=>{x.event_crosswalk[4].source_grade="DIRECT_EDITED_TRANSCRIPTION";}],
["retro_date_silence",x=>{x.date_discrepancies[0].textual_retrospective="1532-06-23";}],
["merge_1536_letters",x=>{x.date_discrepancies[1].same_letter="PROVEN";}],
["fake_parker",x=>{x.date_discrepancies[2].original_manuscript_date_line_seen=true;}],
["source_overlap",x=>{x.source_registry[1].id=x.source_registry[0].id;}],
["publication",x=>{x.reviewer_ready_narrative.status="PUBLISHED";}],
["outreach",x=>{x.technical_access.publisher_contact_message_sent=true;}]];
const file=process.argv.find(a=>a.endsWith(".json"))||"research/data/V3_92_KGK_1532_1533_CORRESPONDENCE_EVIDENCE_DRAFT.json";
const d=JSON.parse(readFileSync(file,"utf8"));
const errors=validate(d); if(errors.length){console.error("FAIL:",errors);process.exit(1)}
console.log("PASS: V3.92 release, edited-text, lost-letter, 1532-1536 date split and primary claim guards");
if(process.argv.includes("--self-test")){
 let rejected=0; for(const [name,change] of mutations){const z=JSON.parse(JSON.stringify(d));change(z);if(validate(z).length===0){console.error("MISSED:",name);process.exit(1);}rejected++;}
 console.log("PASS: "+rejected+" / "+mutations.length+" mutation tests rejected");
}
