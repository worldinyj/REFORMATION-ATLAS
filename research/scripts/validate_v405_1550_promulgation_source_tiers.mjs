#!/usr/bin/env node
import {readFileSync} from "node:fs";
/** V4.05 read-only original-vs-editorial distinction audit. */
const validate=function validate(d,o){
const e=[],ss=d.sources||[],cs=d.claims||[],s=Object.fromEntries(ss.map(x=>[x.id,x])),ids=new Set(ss.map(x=>x.id)),claims=new Set(cs.map(x=>x.id));
if(d.version!=="V4.05"||d.status!=="RESEARCH_DRAFT"||d.parent_branch!=="research/atlas-v404-1530-marriage-publication-vs-1539-witness-comparison")e.push("metadata");
if(ss.length!==7||ids.size!==7||cs.length!==12||claims.size!==12||d.timeline?.length!==4||d.different_twos?.length!==5)e.push("sizes");
for(const c of cs)if(c.refs.some(x=>!ids.has(x)))e.push("citation:"+c.id);
const a=s["S405-PRIMARY1550"]||{},n=s["S405-EDITOR1550"]||{},z=s["S405-ZURICH1550"]||{},g=s["S405-BSB1550"]||{},p=s["S405-PRINT1539"]||{},t=s["S405-TEI1530"]||{},pdf=s["S405-PDF2022"]||{};
if(a.sha!=="34e398a32c3b2345c415e98882493e7adbd4e039"||a.original_instruction!=="ONE_OR_TWO_ANNUAL_READINGS_AS_NEEDED"||a.short_terms?.[0]!=="ein oder zweymal im Jar"||a.edited_text_read!==true||a.first_clause_original_photo_seen!==false)e.push("1550-original");
if(n.editor!=="Sandra Reisinger"||n.original_synod_minutes_read!==false||n.editorial_note_read!==true||n.underlying_archive?.length!==4)e.push("editor-tier");
if(z.marriage_appendix_pages_read!==false||z.first_page_image_read!==true||z.original_full_pdf_downloaded!==false||z.pdf_sha256!==null)e.push("Zurich");
if(g.same_print_setting_as_ZB_AW1025!=="UNVERIFIED"||g.marriage_appendix_pages_read!==false||g.google_pdf_http!==403||g.google_plain_text_http!==403||g.catalog_page_count!==38||g.catalog_read!==true)e.push("BSB");
if(p.facsimile_pdf_pages_read?.join(",")!=="15,16"||p.annual_extract_reading_instruction!==4||p.actual_practice_verified!==false)e.push("1539");
if(t.public_marriage_banns!==2||t.sha!=="e073dc750840d389f2d2909b651073a09c2deac0")e.push("1530");
if(pdf.pdf_text_seen!==true||pdf.pdf_screenshot_succeeded!==false)e.push("PDF");
if(d.norm_vs_guidance?.historical_mandate!=="ONE_OR_TWO_AS_NEEDED"||d.norm_vs_guidance?.modern_editor_synod_account!=="TWICE_PER_YEAR_AND_SUPPLY_COPIES"||d.norm_vs_guidance?.original_1549_1550_synod_minutes_directly_read!==false||d.norm_vs_guidance?.sources_must_remain_separate!==true)e.push("norm-guide");
if(d.timeline?.map(x=>x.tier).join("|")!=="EDITORIAL_NOTE|EDITORIAL_NOTE|EDITORIAL_NOTE|DIRECT_CRITICAL_TRANSCRIPTION_OF_HISTORICAL_TEXT")e.push("timeline");
if(d.different_twos?.map(x=>x.kind).join("|")!=="PUBLIC_CHURCH_MARRIAGE_BANNS|CREDIBLE_MALE_PROMISE_WITNESSES|EXTRACT_ANNUAL_PROCLAMATIONS_INTENT|MAIN_MANDATE_READINGS_AS_NEEDED|SYNOD_RECOMMENDATION_EDITORIAL_NOTE")e.push("number-semantics");
if(d.SSRQ?.license!=="CC BY-NC-SA 4.0"||d.SSRQ?.pinned_commit!=="c6f409c719dfb46ded238e4c7f7b1d5b5391dbbe"||d.SSRQ?.whole_TEI_reprinted!==false)e.push("license");
for(const k of ["marriage_appendix_1550_read","full_1539_ordinance_read","BSB_1550_matter_directly_read","ZB_1550_marriage_pages_read","synod_1549_minutes_read","synod_1550_minutes_read","Ott1855_pp108_122_read","July1533_A6_1_Nr7_read","article39_1533_read"])if(d.unresolved?.[k]!==false)e.push("unresolved:"+k);
for(const k of ["can_ship","main_modified","essays_513_modified","ai_studio_modified","previous_files_overwritten","source_full_text_republished","source_images_republished","historian_approved"])if(d.release?.[k]!==false)e.push("release:"+k);
if(o.version!=="V4.05-READER-REVIEW"||o.status!=="DRAFT_ONLY_NOT_PUBLISHED"||o.chapter_target!=="MEDIUM-ZWINGLI"||o.paragraphs?.length!==4||o.evidence_links?.length!==4||o.editorial_questions?.length!==3)e.push("reader");
for(const ref of o.evidence_links||[])if(ref.claim_ids.some(x=>!claims.has(x)))e.push("reader-ref");
if(o.new_event_episode?.status!=="REVIEW_ONLY"||o.new_event_episode?.claim_ids.some(x=>!claims.has(x)))e.push("episode");
if(o.safety?.original_1550_reading_count!=="ONE_OR_TWO_AS_NEEDED"||o.safety?.May6_1550_editorial_synod_reading_count!=="TWO_PER_YEAR"||o.safety?.do_not_merge_numerals!==true||o.safety?.synod_minutes_directly_read!==false||o.safety?.ZB_1550_appendix_text_read!==false||o.safety?.BSB_1550_appendix_text_read!==false||o.safety?.year1533_art39_read!==false||o.safety?.pdf_screenshots_successful!==false)e.push("reader-gates");
for(const k of ["can_ship","existing_513_modified","main_modified","ai_studio_modified","rights_approved"])if(o.publication?.[k]!==false)e.push("reader-release");
return e;
};
const mutations=[["publish",x=>x.d.release.can_ship=true],
["modify-main",x=>x.d.release.main_modified=true],
["wrong-frequency",x=>x.d.sources[0].original_instruction="TWICE_ONLY"],
["wrong-term",x=>x.d.sources[0].short_terms[0]="twice a year"],
["invent-photo",x=>x.d.sources[0].first_clause_original_photo_seen=true],
["invent-synod",x=>x.d.sources[1].original_synod_minutes_read=true],
["delete-editor-sources",x=>x.d.sources[1].underlying_archive=[]],
["appendix-viewed",x=>x.d.sources[2].marriage_appendix_pages_read=true],
["Zurich-full-PDF",x=>x.d.sources[2].original_full_pdf_downloaded=true],
["invent-BSB-identity",x=>x.d.sources[3].same_print_setting_as_ZB_AW1025="VERIFIED"],
["invent-BSB-pages",x=>x.d.sources[3].marriage_appendix_pages_read=true],
["BSB-PDF-403->200",x=>x.d.sources[3].google_pdf_http=200],
["1539-annual-false",x=>x.d.sources[4].annual_extract_reading_instruction=2],
["1539-practice",x=>x.d.sources[4].actual_practice_verified=true],
["1530-banns",x=>x.d.sources[5].public_marriage_banns=1],
["PDF-screenshot",x=>x.d.sources[6].pdf_screenshot_succeeded=true],
["SSRQ-wrong-pin",x=>x.d.SSRQ.pinned_commit="main"],
["SSRQ-wrong-license",x=>x.d.SSRQ.license="CC0"],
["original-1549-read",x=>x.d.norm_vs_guidance.original_1549_1550_synod_minutes_directly_read=true],
["editor-as-original",x=>x.d.timeline[1].tier="DIRECT_1549_TEXT"],
["conflate-two",x=>x.d.different_twos[1].kind="PUBLIC_CHURCH_MARRIAGE_BANNS"],
["Ott-read",x=>x.d.unresolved.Ott1855_pp108_122_read=true],
["art39-read",x=>x.d.unresolved.article39_1533_read=true],
["reader-bad-claim",x=>x.o.evidence_links[0].claim_ids=["C405-99"]],
["reader-new-target",x=>x.o.chapter_target="MEDIUM-CALVIN"],
["reader-false-synod",x=>x.o.safety.synod_minutes_directly_read=true],
["reader-doubled",x=>x.o.safety.original_1550_reading_count="TWO"],
["reader-shipped",x=>x.o.publication.can_ship=true],
["reader-513",x=>x.o.publication.existing_513_modified=true],
["reader-appendix",x=>x.o.safety.BSB_1550_appendix_text_read=true]];
const data=JSON.parse(readFileSync("research/data/V4_05_1550_PROMULGATION_PRINT_COPIES_SOURCE_LEVEL_DRAFT.json","utf8"));
const reader=JSON.parse(readFileSync("research/data/V4_05_PROMULGATION_GAP_ZWINGLI_READER_DRAFT.json","utf8"));
const errors=validate(data,reader);if(errors.length){console.error("FAIL V4.05",errors);process.exit(1)}
console.log("PASS V4.05: 1550 original one-or-two annual readings not conflated with twice-yearly synod note");
if(process.argv.includes("--self-test")){let ok=0;for(const [name,fn] of mutations){const x={d:JSON.parse(JSON.stringify(data)),o:JSON.parse(JSON.stringify(reader))};fn(x);if(!validate(x.d,x.o).length){console.error("MISSED",name);process.exit(1)}ok++;}console.log("PASS V4.05 "+ok+" negative tests")}
