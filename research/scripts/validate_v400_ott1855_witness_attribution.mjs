#!/usr/bin/env node
/** V4.00 research-only read-access and source-provenance guard. */
import {readFileSync} from "node:fs";
const guard=function guard(d,p){
 const e=[],r=d.release||{},x=d.access_trials||[],w=d.critical_witnesses||[],law=d.legal_1525_1533_comparison||{},a=d.article39_evidence||{},ed=p.evidence_disclosure||{};
 if(d.version!=="V4.00"||d.status!=="RESEARCH_DRAFT")e.push("version");
 for(const name of ["can_ship","main_changed","essays_513_changed","ai_studio_changed","prior_research_rewritten","source_full_text_copied","images_republished","outreach_sent","rights_cleared"])if(r[name]!==false)e.push("release");
 if(x.map(z=>z.id).join("|")!=="AC400-EP-VOLUME|AC400-EP-OCR|AC400-GOOGLE-PLAY|AC400-GOOGLE-BOOKS")e.push("access");
 if(x[0]?.target_pages_visual_read!==false||x[0]?.target_text_read!==false||x[0]?.source_code_or_pdf_sha256!==null||x[1]?.body_downloaded!==false||x[1]?.target_pages_text_found!==false||x[1]?.sha256!==null||x[2]?.reader_book_pdf_or_epub_obtained!==false||x[2]?.preview_page_108_122_read!==false||x[2]?.download_sha256!==null||x[3]?.printed_page_image_seen!==false)e.push("unread-access");
 if(x[2]?.advertised_pages!==204||x[2]?.catalog_directly_read!==true||x[2]?.price_label!=="Get for free")e.push("catalog");
 if(w.map(z=>z.id).join("|")!=="W400-OTT1855|W400-1878|W400-SSRQ156|W400-ZH-A61-7|W400-ZH-BIII6")e.push("witnesses");
 if(w[0]?.actual_printed_text_read!==false||w[1]?.OCR_excerpt_in_search_index!==true||w[1]?.printed_page_image_seen!==false||w[1]?.is_direct_16c_original!==false||w[2]?.individual_text_directly_read!==false||w[2]?.record_number!==156||w[2]?.printed_edition_page!==376||w[3]?.primary_facsimile_seen!==false||w[4]?.physical_copy_page_seen!==false)e.push("witness-grades");
 if(law.earlier_1525_as_described?.primary_1525_rule_seen!==false||law.later_1533_as_described?.original_1533_article_seen!==false||law.later_1533_as_described?.original_article_number!=="UNVERIFIED"||law.later_1533_as_described?.is_article_39!=="NOT_ESTABLISHED"||law.is_this_same_as_44_article_draft_final_text!=="UNVERIFIED"||law.may_20_1533_archival_query?.relation_to_later_rule!=="THEME_OVERLAP_NOT_TEXTUAL_IDENTITY")e.push("text-level");
 if(a.article_number!==39||a.bern_amendment_requested!==true||a.zurich_amendment_requested!==true||a.exact_text_seen!==false||a.subject_matter_verified!==false||a.no_inference_from_1878_marriage_witness!==true)e.push("article39");
 if(d.publication_cautions?.length!==6||d.publication_cautions.map(z=>z.allowed).join("|")!=="false|true|false|true|false|true")e.push("caution");
 if(d.inherited_unresolved?.ott1855_pp108_122_read!==false||d.inherited_unresolved?.july1536_Bucer_Vadian_23_25!=="UNRESOLVED")e.push("inherited");
 if(p.version!=="V4.00-READER-REVIEW"||p.status!=="REVIEW_ONLY"||p.target_id!=="MEDIUM-ZWINGLI"||p.paragraphs?.length!==3||p.checks?.length!==4||p.source_blocks?.length!==3)e.push("reader");
 if(ed.ott1855_book_204_pages_listed_not_read!==true||ed.year1878_ocr_text_in_search_index!==true||ed.year1878_print_page_image_seen!==false||ed.SSRQ156_individual_original_text_read!==false||ed.article39_text_read!==false||ed.any_text_falsely_ascribed_to_Art39!==false||ed.any_1878_generalization_as_five_city_enactment!==false||ed.gender_history_requires_editor_review!==true||ed.original_text_reproduction!==false)e.push("reader-evidence");
 if(p.standalone_episode_insert?.review_only!==true||p.standalone_episode_insert?.evidence?.join("|")!=="W400-1878|W400-SSRQ156")e.push("episode");
 for(const key of ["publication_approved","main_changed","source_medium_reader_changed","existing_513_essays_changed","ai_studio_changed","can_ship"])if(p.release?.[key]!==false)e.push("reader-release");
 return e;
};
const mutations=[["ship",x=>x.d.release.can_ship=true],
["main",x=>x.d.release.main_changed=true],
["Ott_read",x=>x.d.access_trials[0].target_pages_visual_read=true],
["fake_hash",x=>x.d.access_trials[0].source_code_or_pdf_sha256="abc"],
["ocr_read",x=>x.d.access_trials[1].target_pages_text_found=true],
["google_read",x=>x.d.access_trials[2].preview_page_108_122_read=true],
["google_204",x=>x.d.access_trials[2].advertised_pages=198],
["1878_original",x=>x.d.critical_witnesses[1].is_direct_16c_original=true],
["1878_scan",x=>x.d.critical_witnesses[1].printed_page_image_seen=true],
["SSRQ_text",x=>x.d.critical_witnesses[2].individual_text_directly_read=true],
["SSRQ_number",x=>x.d.critical_witnesses[2].record_number=157],
["1525_primary",x=>x.d.legal_1525_1533_comparison.earlier_1525_as_described.primary_1525_rule_seen=true],
["1533_same_44",x=>x.d.legal_1525_1533_comparison.is_this_same_as_44_article_draft_final_text="PROVEN"],
["conflate_art39",x=>x.d.legal_1525_1533_comparison.later_1533_as_described.is_article_39="YES"],
["invent_art39",x=>x.d.article39_evidence.subject_matter_verified=true],
["drop_zurich39",x=>x.d.article39_evidence.zurich_amendment_requested=false],
["may20_same_text",x=>x.d.legal_1525_1533_comparison.may_20_1533_archival_query.relation_to_later_rule="SAME_TEXT"],
["uniform_44",x=>x.d.publication_cautions[4].allowed=true],
["1536_same",x=>x.d.inherited_unresolved.july1536_Bucer_Vadian_23_25="PROVEN"],
["reader_live",x=>x.p.release.can_ship=true],
["wrong_reader",x=>x.p.target_id="MEDIUM-CALVIN"],
["gender_unreviewed",x=>x.p.evidence_disclosure.gender_history_requires_editor_review=false],
["reader_article39",x=>x.p.evidence_disclosure.any_text_falsely_ascribed_to_Art39=true],
["reader_four",x=>x.p.paragraphs.push("extra")],
["episode_publish",x=>x.p.standalone_episode_insert.review_only=false]];
const data=JSON.parse(readFileSync("research/data/V4_00_OTT_1855_ACCESS_AND_1533_MARRIAGE_RULE_WITNESS_DRAFT.json","utf8"));
const reader=JSON.parse(readFileSync("research/data/V4_00_ZURICH_MARRIAGE_RULE_TEXT_READER_INSERT_DRAFT.json","utf8"));
const errors=guard(data,reader);if(errors.length){console.error("V4.00 FAILED",errors);process.exit(1)}
console.log("PASS V4.00: no false Ott page, 1878 witness, SSRQ156, Art39, or premature reader claims");
if(process.argv.includes("--self-test")){let passed=0;for(const [name,fn] of mutations){const x={d:JSON.parse(JSON.stringify(data)),p:JSON.parse(JSON.stringify(reader))};fn(x);if(!guard(x.d,x.p).length){console.error("UNDETECTED",name);process.exit(1)}passed++;}console.log("PASS "+passed+" mutation tests");}
