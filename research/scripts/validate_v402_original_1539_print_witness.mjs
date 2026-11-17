#!/usr/bin/env node
/** REFORMATION-ATLAS V4.02 fixed-source & no-release auditor. */
import {readFileSync} from "node:fs";
const validate=function validate(d,r){
 const e=[],s=d.sources||[],p=d.release||{},f=s.find(x=>x.id==="S1539"),old=s.find(x=>x.id==="S1525"),mid=s.find(x=>x.id==="S1533"),lim=d.scope_limits||{},b=r.source_boundary||{};
 if(d.version!=="V4.02"||d.status!=="RESEARCH_DRAFT"||s.map(x=>x.year).join(",")!=="1525,1533,1539"||d.claims?.length!==10)e.push("metadata");
 for(const k of ["can_ship","main_modified","essays_513_modified","ai_studio_modified","old_research_rewritten","external_distribution"])if(p[k]!==false)e.push("source-release");
 if(old?.blob!=="4d9145fc3564bed1044b6fa75d14ee042c9c6b33"||old?.actual_photo_seen!==false||old?.edited_text_seen!==true)e.push("1525");
 if(mid?.blob!=="3b15cd7526f8d1eeba718162681c1c9b7a33ae61"||mid?.dorsal_other_hand_date!=="1533-06-10"||mid?.actual_photo_seen!==false)e.push("1533");
 if(f?.kind!=="ORIGINAL_PRINT_DIGITIZATION_VISUALLY_READ"||f?.date!=="1539-07-12"||f?.archive!=="Zentralbibliothek Zürich AW 1020"||f?.doi!=="10.3931/e-rara-151"||f?.pdf!=="https://www.e-rara.ch/zuz/download/pdf/40998")e.push("1539-bib");
 if(f?.verified_pages_zero_based?.join(",")!=="15,16"||f?.actual_photo_seen!==true||f?.full_text_read!==false||f?.full_ordinance_witness!==false||f?.pdf_byte_hash!==null||f?.pdf_pages!==23)e.push("1539-image");
 if(f?.original_short_quotations?.join("|")!=="zwen erbaren biderben mannen|die nit kuppler oder argwönig"||f?.original_phrase_quote_words!==9||f?.actual_pulpit_readings_verified!==false||f?.license!=="Public Domain Mark")e.push("printed-text");
 if(d.claims?.some(x=>!s.some(y=>y.id===x.ref)))e.push("claim-ref");
 if(d.licenses?.ssrq_2022!=="CC BY-NC-SA 4.0"||d.licenses?.images_copied_to_repo!==false)e.push("rights");
 if(lim.source_is_excerpt_not_full_ordinance!==true||lim.no_1533_article39_identification!==true||lim.forty_four_draft_article_text_read!==false||lim.any_five_city_identical_enactment!==false||lim.pulpit_practice_documented!==false||lim.downloaded_original_pdf_bytes!==false)e.push("boundaries");
 if(d.unresolved?.find(x=>x.id==="OTT1855")?.state!=="NOT_READ"||d.unresolved?.find(x=>x.id==="ARTICLE39")?.state!=="NOT_IDENTIFIED")e.push("unresolved");
 if(r.version!=="V4.02-READER-DRAFT"||r.status!=="REVIEW_ONLY_NOT_PUBLISHED"||r.target!=="MEDIUM-ZWINGLI"||r.paragraphs?.length!==3||r.evidence?.length!==4)e.push("reader");
 if(r.evidence?.map(x=>x.source).join(",")!=="S1525,S1533,S1539,S1539"||r.evidence?.[2]?.grade!=="DIRECT_1539_PRINT_SCAN_PDF_P15_P16"||r.original_1539_phrases?.length!==2||r.original_1539_phrases?.some(x=>x.pdf_page_zero_based!==16))e.push("reader-refs");
 if(r.standalone_story_patch?.review_only!==true||r.reader_questions?.length!==2)e.push("reader-story");
 for(const k of ["can_ship","existing_513_modified","main_modified","ai_studio_modified","historian_approved","rights_reviewed"])if(r.publication?.[k]!==false)e.push("reader-release");
 if(b.primary_1539_print_visual_read!==true||b.printed_pdf_pages?.join(",")!=="15,16"||b.original_1539_full_ordinance_read!==false||b.other_city_1539_enactment_proven!==false||b.art39_text_read!==false||b.modern_editor_view_separate!==true)e.push("reader-limits");
 return e;
};
const mutants=[["bad-year",x=>x.d.sources[2].date="1533-07-12"],
["bad-scan",x=>x.d.sources[2].verified_pages_zero_based=[15,17]],
["full-law",x=>x.d.sources[2].full_ordinance_witness=true],
["overread",x=>x.d.sources[2].full_text_read=true],
["not-actually-viewed",x=>x.d.sources[2].actual_photo_seen=false],
["fake-hash",x=>x.d.sources[2].pdf_byte_hash="fake"],
["wrong-quote",x=>x.d.sources[2].original_short_quotations[0]="fake"],
["pulpit-verified",x=>x.d.sources[2].actual_pulpit_readings_verified=true],
["misdated-dorsal",x=>x.d.sources[1].dorsal_other_hand_date="1533-07-10"],
["photograph-1525",x=>x.d.sources[0].actual_photo_seen=true],
["wrong-license",x=>x.d.licenses.ssrq_2022="CC0"],
["reproduce",x=>x.d.licenses.images_copied_to_repo=true],
["declare-44",x=>x.d.scope_limits.forty_four_draft_article_text_read=true],
["five-cities",x=>x.d.scope_limits.any_five_city_identical_enactment=true],
["pretend-article39",x=>x.d.scope_limits.no_1533_article39_identification=false],
["fake-Ott",x=>x.d.unresolved.find(y=>y.id==="OTT1855").state="READ"],
["fake-Art39",x=>x.d.unresolved.find(y=>y.id==="ARTICLE39").state="VERIFIED"],
["ship",x=>x.d.release.can_ship=true],
["main",x=>x.d.release.main_modified=true],
["wrong-reader-source",x=>x.r.evidence[2].source="S1533"],
["reader-published",x=>x.r.publication.can_ship=true],
["reader-513",x=>x.r.publication.existing_513_modified=true],
["reader-Art39",x=>x.r.source_boundary.art39_text_read=true],
["reader-full",x=>x.r.source_boundary.original_1539_full_ordinance_read=true],
["reader-wrong-page",x=>x.r.original_1539_phrases[0].pdf_page_zero_based=15],
["reader-story-release",x=>x.r.standalone_story_patch.review_only=false]];
const data=JSON.parse(readFileSync("research/data/V4_02_1539_DIRECT_PRINT_TWO_WITNESS_SCAN_EVIDENCE_DRAFT.json","utf8"));
const reader=JSON.parse(readFileSync("research/data/V4_02_ZURICH_MARRIAGE_RULE_ORIGINAL_PRINT_READER_DRAFT.json","utf8"));
const failures=validate(data,reader);if(failures.length){console.error("V402 FAIL",failures);process.exit(1)}
console.log("V402 PASS source evidence and reader gates");
if(process.argv.includes("--self-test")){let pass=0;for(const [name,fn] of mutants){const x={d:JSON.parse(JSON.stringify(data)),r:JSON.parse(JSON.stringify(reader))};fn(x);if(!validate(x.d,x.r).length){console.error("V402 BAD MUTATION",name);process.exit(1)}pass++;}console.log("V402 PASS "+pass+" mutation rejections");}
