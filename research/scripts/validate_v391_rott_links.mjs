#!/usr/bin/env node
// Read-only consistency checks for frozen V3.91 research data.
import { readFileSync } from "node:fs";
const validate = function validate(v){
 const errs=[],a=v.target||{},r=v.release||{},pr=v.provenance||{},st=v.source_status||{};
 if(v.version!=="V3.91"||v.status!=="RESEARCH_DRAFT")errs.push("version");
 for(const k of ["can_ship","main_modified","essays_513_modified","ai_studio_modified","external_messages_sent"])if(r[k]!==false)errs.push("release:"+k);
 if(a.historic_url!=="https://www.zwingliana.ch/index.php/zwa/article/view/910/820")errs.push("historic_url");
 if(a.modern_pdf_url!==null||a.original_pdf_sha256!==null||a.original_pdf_acquired!==false||a.printed_489_seen!==false||a.printed_491_seen!==false)errs.push("unearned_pdf");
 if(JSON.stringify(a.target_pages)!=="[489,491]"||a.page_range!=="461-492")errs.push("pages");
 if(pr.earliest_identified_external_reference!=="2025-08-27"||pr.first_ever_external_reference_proven!==false||pr.author_and_blog_same_in_both_years!==true||pr.independent_source_families_for_blog_link!==1||pr.historical_link_worked_in_2025!=="UNVERIFIED"||pr.second_route_token_role!=="UNKNOWN_FROM_LINK_ALONE")errs.push("provenance");
 if(!Array.isArray(pr.references)||pr.references.length!==2||JSON.stringify(pr.references.map(z=>z.date))!=='["2025-08-27","2026-08-27"]'||pr.references.some(z=>z.author!=="Jim"||z.title_link_typo!=="Brucer"||z.target!==a.historic_url||z.live_click_result_on_2026_11_16!=="HTTP_404"))errs.push("blog_records");
 const orth=v.orthography||[];if(orth.length!==4||JSON.stringify(orth.map(z=>z.literal))!=='["Bucer","Brucer","Fucer","Drie"]'||orth[0].accept_as_original_title!==true||orth.slice(1).some(z=>z.accept_as_original_title!==false))errs.push("orthography");
 const src=v.corroboration||[];if(src.length!==7||new Set(src.map(z=>z.id)).size!==7||src.some(z=>!z.grade||!z.url))errs.push("sources");
 const at=v.attempts||[];if(at.length!==4||at.some(z=>z.got_pdf!==false)||at.filter(z=>z.result==="HTTP_404").length!==2||at.filter(z=>z.result==="LOCAL_DNS_FAILURE").length!==1)errs.push("acquisition");
 if(st.rott_original_1978_seen!==false||st.parker_ms119_199_200_205_206_images_seen!==false||st.july23_and_july25_letters_same!=="UNRESOLVED"||st.ms119_date_original_seen!==false||st.corrected_zurich_kalliope_id!=="CH-002121-2-991170608445805501")errs.push("manuscript_and_letter");
 return errs;
};
const mutations = [["fabricated_pdf",x=>{x.target.original_pdf_acquired=true;}],
["fabricated_page",x=>{x.target.printed_489_seen=true;}],
["release",x=>{x.release.can_ship=true;}],
["2025_broken_chronology",x=>{x.provenance.earliest_identified_external_reference="2026-08-27";}],
["false_blog_independence",x=>{x.provenance.independent_source_families_for_blog_link=2;}],
["invent_2025_access",x=>{x.provenance.historical_link_worked_in_2025=true;}],
["ocr_as_original",x=>{x.orthography[2].accept_as_original_title=true;}],
["false_date_merge",x=>{x.source_status.july23_and_july25_letters_same="PROVEN";}],
["misclassify_dns",x=>{x.attempts[3].result="HTTP_404";}]];
const path = process.argv.find(x => x.endsWith(".json")) || "research/data/V3_91_ROTT_LINK_CHRONOLOGY_AND_SPELLING_DRAFT.json";
const data = JSON.parse(readFileSync(path, "utf8"));
const violations = validate(data);
if(violations.length){ console.error("FAIL", violations); process.exit(1); }
console.log("PASS: V3.91 provenance, spelling, acquisition and release gates");
if(process.argv.includes("--self-test")) {
  const missed=[];
  for(const [name, mutate] of mutations) {
    const bad=JSON.parse(JSON.stringify(data)); mutate(bad);
    if(validate(bad).length===0) missed.push(name);
  }
  if(missed.length){ console.error("FAIL: undetected mutations",missed); process.exit(1); }
  console.log("PASS: 9 mutation tests rejected");
}
