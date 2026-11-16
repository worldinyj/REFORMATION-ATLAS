#!/usr/bin/env node
/** V3.99: read-only source and 44 article fact gates. Run at repository root with node. */
import {readFileSync} from "node:fs";
const validate=function validate(d,o){
 const errs=[],rel=d.release||{},basis=d.article_number_basis||{},rows=basis.articles||[],src=d.source_witnesses||[],g=o.evidence_hard_gates||{};
 if(d.version!=="V3.99"||d.status!=="RESEARCH_DRAFT"||d.parent_branch!=="research/atlas-v398-bern-marriage-law-critical-reader-bridge")errs.push("metadata");
 for(const k of ["can_ship","main_modified","essays_513_modified","ai_studio_modified","prior_reader_merged","rights_approved_for_republication","external_outreach_sent","source_full_text_copied","facsimiles_copied"])if(rel[k]!==false)errs.push("release-"+k);
 if(basis.footnote!=="printed p106 note112"||basis.modern_historiographical_note_visually_read!==true||basis.direct_historical_1533_44_article_minutes_seen!==false||basis.page_number_scope!=="PDF zero-based page 107, printed 106")errs.push("scholar-note");
 const bern=[...Array.from({length:11},(_,i)=>i+1),19,21,23,25,26,27,36,38,39,42,43];
 if(rows.length!==44||new Set(rows.map(x=>x.article_no)).size!==44||rows.some((x,i)=>x.article_no!==i+1))errs.push("article-universe");
 for(const a of rows){
  if(a.bern_amendment_requested_in_Engeler2023_n112!==bern.includes(a.article_no)||a.zurich_amendment_requested_in_Engeler2023_n112!==(a.article_no===39)||a.article_original_1533_text_seen!==false||a.exact_topic_from_primary_article!=="NOT_READ"||a.substantive_agreement_state!=="UNDETERMINED"||a.textual_change_description!==null||a.manuscript_folio_mapping!==null)errs.push("article-state-"+a.article_no);
 }
 const c=d.stats||{};
 if(c.total!==44||c.bern_requests!==22||c.zurich_requests!==1||c.overlap!==1||c.bern_only!==21||c.without_documented_bern_request!==22||c.exact_text_directly_read!==0||c.agreed_articles_verified!==0)errs.push("counts");
 if(src.length!==8||new Set(src.map(x=>x.id)).size!==8)errs.push("sources");
 const byId=Object.fromEntries(src.map(x=>[x.id,x]));
 if(byId["V399-ZH-A6-1-7"]?.historical_folio_image_seen!==false||byId["V399-ZH-A6-1-7"]?.Ott1855_pp108_122_scans_seen!==false||byId["V399-ZH-A6-1-7"]?.shelfmark!=="A 6.1, Nr. 7")errs.push("A6.1.7");
 if(byId["V399-ZH-BIII6-217-222"]?.historical_folio_image_seen!==false||byId["V399-ZH-BIII6-217-222"]?.copy_title_visually_on_folio_seen!==false||byId["V399-ZH-BIII6-217-222"]?.scribal_layer!=="Abschrift (Nachtrag)"||byId["V399-ZH-BIII6-217-222"]?.shelfmark!=="B III 6, fol.217r–222v")errs.push("BIII6");
 if(byId["V399-ZH-BIII6-220V-1550"]?.date!=="1550-10-06"||byId["V399-ZH-BIII6-220V-1550"]?.text_seen!==false)errs.push("1550");
 if(byId["V399-OTT1855-PART2"]?.exact_page_scans_108_to_122_opened!==false||byId["V399-OTT1855-PART2"]?.printed_pages!=="108–122")errs.push("Ott-print");
 if(byId["V399-ENGELER2023-P103-106"]?.visual_screenshot_success!==true||byId["V399-ENGELER2023-P103-106"]?.publication_year!==2023)errs.push("Engeler-pdf");
 if(d.scope_separation?.length!==6||d.scope_separation.some(x=>!x.cannot_assert||!x.can_assert))errs.push("scope");
 if(d.inherited_gates?.bucer_vadian_july_1536_23_vs_25!=="UNRESOLVED"||d.inherited_gates?.rott_1978_pages_489_491_seen!==false||d.inherited_gates?.parker_ms119_photo_seen!==false)errs.push("old-proofs");
 if(o.version!=="V3.99-READER-OVERLAY"||o.status!=="REVIEW_ONLY_NOT_PUBLISHED"||o.target_keys?.join(",")!=="MEDIUM-MARBURG,MEDIUM-ZWINGLI,MEDIUM-AUGSBURG")errs.push("reader-meta");
 if(o.overlays?.length!==3||o.overlays.some(x=>x.paragraphs?.length!==2||x.status!=="REVIEW_ONLY"||x.evidence.some(z=>!byId[z])))errs.push("reader-overlay");
 const article=o.standalone_revised_episode||{};
 if(article.sections?.length!==7||article.misconceptions?.length!==4||article.published!==false||article.sections?.some(x=>x.evidence.some(z=>!byId[z])))errs.push("reader-story");
 const falseFlags=["printed_1855_108_122_directly_read","original_1533_A6_1_7_manuscript_seen","original_BIII6_217_222_manuscript_seen","article39_exact_text_seen","any_unchallenged_article_considered_agreed","any_city_identical_all44_enacted","main_modified","existing_513_modified","webapp_modified","published","can_ship"];
 for(const k of falseFlags)if(g[k]!==false)errs.push("reader-gate-"+k);
 if(g.original_44_article_texts_read!==0||o.editorial_reviews?.publication_approved!==false||o.editorial_reviews?.final_1536_claim_confession_article27!=="NOT_CAUSALLY_PROVEN")errs.push("causal-gate");
 return errs;
};
const mutations=[["publish",x=>{x.d.release.can_ship=true}],
["main_touched",x=>{x.d.release.main_modified=true}],
["fake_1533_manuscript",x=>{x.d.article_number_basis.direct_historical_1533_44_article_minutes_seen=true}],
["wrong_n112",x=>{x.d.article_number_basis.footnote="p105"}],
["drop_article",x=>{x.d.article_number_basis.articles.pop()}],
["dupe_number",x=>{x.d.article_number_basis.articles[1].article_no=1}],
["unrequested_to_requested",x=>{x.d.article_number_basis.articles[21].bern_amendment_requested_in_Engeler2023_n112=true}],
["article39_zurich_dropped",x=>{x.d.article_number_basis.articles[38].zurich_amendment_requested_in_Engeler2023_n112=false}],
["article39_text_invented",x=>{x.d.article_number_basis.articles[38].article_original_1533_text_seen=true}],
["invented_article_topic",x=>{x.d.article_number_basis.articles[38].exact_topic_from_primary_article="adultery"}],
["uncontested_called_agreed",x=>{x.d.article_number_basis.articles[0].substantive_agreement_state="AGREED"}],
["changed_22",x=>{x.d.stats.bern_requests=23}],
["sneak_print_scans",x=>{x.d.source_witnesses.find(z=>z.id==="V399-OTT1855-PART2").exact_page_scans_108_to_122_opened=true}],
["scan_A6",x=>{x.d.source_witnesses.find(z=>z.id==="V399-ZH-A6-1-7").historical_folio_image_seen=true}],
["claim_BIII_photo",x=>{x.d.source_witnesses.find(z=>z.id==="V399-ZH-BIII6-217-222").copy_title_visually_on_folio_seen=true}],
["erase_postscript_1550",x=>{x.d.source_witnesses.find(z=>z.id==="V399-ZH-BIII6-220V-1550").date="1533-07-15"}],
["conflate_copy",x=>{x.d.source_witnesses.find(z=>z.id==="V399-ZH-BIII6-217-222").scribal_layer="Original"}],
["fake_date_1536",x=>{x.d.inherited_gates.bucer_vadian_july_1536_23_vs_25="PROVEN"}],
["future_confession_cause",x=>{x.o.editorial_reviews.final_1536_claim_confession_article27="DIRECT_CAUSE"}],
["reader_published",x=>{x.o.evidence_hard_gates.published=true}],
["reader_wrong_key",x=>{x.o.target_keys[1]="MEDIUM-CALVIN"}],
["reader_wrong_source",x=>{x.o.overlays[1].evidence=["UNKNOWN"]}],
["story_wrong_source",x=>{x.o.standalone_revised_episode.sections[0].evidence=["NOT_FOUND"]}],
["trim_story",x=>{x.o.standalone_revised_episode.sections.pop()}],
["invent_adoption",x=>{x.o.evidence_hard_gates.any_city_identical_all44_enacted=true}],
["overclaim_unrequested",x=>{x.o.evidence_hard_gates.any_unchallenged_article_considered_agreed=true}],
["phoney_rights",x=>{x.d.release.rights_approved_for_republication=true}]];
const d=JSON.parse(readFileSync("research/data/V3_99_1533_44_ARTICLE_AMENDMENTS_ARCHIVE_WITNESS_DRAFT.json","utf8"));
const o=JSON.parse(readFileSync("research/data/V3_99_44_ARTICLES_READER_AND_CITY_LAW_STORY_DRAFT.json","utf8"));
const violations=validate(d,o);if(violations.length){console.error("V399 FAIL",violations);process.exit(1)}
console.log("V399 PASS: 44 article flags, 22 Bern + 1 Zurich overlapping 39, archival witness and release gates");
if(process.argv.includes("--self-test")){let caught=0;for(const [name,modify] of mutations){const x={d:JSON.parse(JSON.stringify(d)),o:JSON.parse(JSON.stringify(o))};modify(x);if(!validate(x.d,x.o).length){console.error("FAULT NOT CAUGHT",name);process.exit(1)}caught++;}console.log("V399 PASS "+caught+"/"+mutations.length+" fault injections detected");}
