#!/usr/bin/env node
/** V4.04 source-provenance / historical distinction audit, no network or writes. */
import {readFileSync} from "node:fs";
const gate=function gate(d,o){
const E=[],ss=d.sources||[],cc=d.claims||[],rel=d.release||{},src=new Map(ss.map(s=>[s.id,s])),cids=new Set(cc.map(c=>c.id));
if(d.version!=="V4.04"||d.status!=="RESEARCH_DRAFT"||d.parent_branch!=="research/atlas-v403-1550-composite-1539-marriage-edition-scope-audit")E.push("metadata");
for(const k of ["can_ship","main_modified","existing_513_modified","ai_studio_modified","V403_research_files_overwritten","original_quoted_text_bulk_republished","images_downloaded_to_repo","historian_approved"])if(rel[k]!==false)E.push("release:"+k);
if(ss.length!==5||new Set(ss.map(x=>x.id)).size!==5||cc.length!==14||new Set(cc.map(x=>x.id)).size!==14||d.stage_crosswalk?.length!==5)E.push("counts");
for(const c of cc){if(!src.has(c.source))E.push("unknown-claim-source:"+c.id);if(c.comparison_with&&!src.has(c.comparison_with))E.push("unknown-comp:"+c.id);}
const s1530=src.get("W404-1530")||{},s1539=src.get("W404-1539")||{},s1550=src.get("W404-1550")||{};
if(s1530.date!=="1530-03-26"||s1530.git_blob!=="e073dc750840d389f2d2909b651073a09c2deac0"||s1530.archive!=="StAZH III AAb 1.1 Nr17"||s1530.edition_source_locus!=="fol.3v–4r"||s1530.original_folio_photo_seen!==false||s1530.evidence_level!=="DIRECT_2022_SCHOLARLY_TEI_HISTORIC_TEXT")E.push("1530-primary");
if(s1530.specific_short_source_terms?.join("|")!=="zum minsten zwürend|deß nächsten Sunntags darvor|einest inn der wuchenn|offnem Kilchgang")E.push("source-quotations");
if(s1539.date!=="1539-07-12"||s1539.original_photo_seen!==true||s1539.checked_pdf_page_indexes_zero_based?.join(",")!=="15,16"||s1539.actual_full_ordinance_read!==false)E.push("1539-primary");
if(s1550.editorial_main_mandate_sections_read!==15||s1550.editorial_appended_1539_amended_rule_full_text_read!==false||s1550.original_marriage_appendix_pages_seen!==false||s1550.git_blob!=="34e398a32c3b2345c415e98882493e7adbd4e039")E.push("1550-scope");
if(d.stage_crosswalk?.map(x=>x.year).join("|")!=="1525|1530|1533|1539|circa 1550"||d.stage_crosswalk?.[1]?.issue!=="PUBLIC_MARRIAGE_SOLEMNIZATION"||d.stage_crosswalk?.[3]?.issue!=="PRIOR_PROMISE_EVIDENCE")E.push("different-two");
if(d.ssrq_provenance?.license!=="CC BY-NC-SA 4.0"||d.ssrq_provenance?.TEI_full_text_reproduced!==false||d.original_print_rights?.archive_1550_marriage_appendix_photo_seen!==false)E.push("rights");
if(d.exploration?.length!==5||d.exploration[0]?.actual_complete_pdf_download!==false||d.exploration[1]?.actual_marriage_appendix_image_read!==false||d.exploration[2]?.original_image_seen!==true||d.exploration[2]?.url!=="https://www.e-rara.ch/zuz/download/webcache/1000/41465")E.push("access-trials");
if(d.unchanged_blockers?.Ott_1855_pp108_122_read!==false||d.unchanged_blockers?.A6_1_7_1533_minutes_read!==false||d.unchanged_blockers?.article39_original_text_read!==false||d.unchanged_blockers?.year1550_marriage_appendix_read!==false||d.unchanged_blockers?.July1536_Bucer_Vadian_23_25!=="UNRESOLVED")E.push("unresolved");
if(o.version!=="V4.04-READER-REVIEW"||o.status!=="RESEARCH_DRAFT_NOT_PUBLISHED"||o.chapter_key!=="MEDIUM-ZWINGLI"||o.paragraphs?.length!==4||o.paragraph_evidence?.length!==4||o.concept_cards?.length!==2||o.research_questions?.length!==3)E.push("reader");
for(const x of o.paragraph_evidence||[]){if(x.claims?.some(k=>!cids.has(k)))E.push("reader-citation");if(x.source_areas?.some(k=>!src.has(k)))E.push("reader-src");}
if(o.paragraph_evidence?.[1]?.claims.join("|")!=="C404-03|C404-04|C404-05"||o.paragraph_evidence?.[2]?.claims.join("|")!=="C404-06|C404-07|C404-09|C404-13")E.push("reader-anchors");
if(o.concept_cards?.map(x=>x.legal_function).join("|")!=="PUBLIC_CHURCH_NOTICE|PRIOR_PROMISE_EVIDENCE")E.push("concept-mix");
const h=o.hard_gates||{};
if(h.year1530_public_announcement_count!==2||h.year1539_prior_promise_male_witness_count!==2||h.numeral_sameness_not_legal_identity!==true||h.source1530_folio!=="3v–4r"||h.source1530_historic_original_photo_seen!==false||h.source1539_historic_print_photo_seen!==true||h.source1550_marriage_appendix_read!==false||h.original_1533_article39_read!==false||h.complete_1539_law_read!==false||h.original_1530_handwritten_corrections_read!==false)E.push("reader-provenance");
if(o.independent_history_episode?.status!=="REVIEW_ONLY"||o.independent_history_episode?.evidence?.some(k=>!cids.has(k)))E.push("history");
for(const k of ["can_ship","existing_513_modified","main_modified","ai_studio_modified","historian_review_complete","source_licence_review_complete"])if(o.publication?.[k]!==false)E.push("reader-release");
return E;
};
const mutations=[["ship",x=>x.d.release.can_ship=true],
["main",x=>x.d.release.main_modified=true],
["source-date",x=>x.d.sources[1].date="1539-03-26"],
["wrong-1530-sha",x=>x.d.sources[1].git_blob="0".repeat(40)],
["fake-photo",x=>x.d.sources[1].original_folio_photo_seen=true],
["wrong-folio",x=>x.d.sources[1].edition_source_locus="fol.1r"],
["wrong-quoted-announcement",x=>x.d.sources[1].specific_short_source_terms[0]="zwen männer"],
["1539-not-seen",x=>x.d.sources[3].original_photo_seen=false],
["fake-1539-full",x=>x.d.sources[3].actual_full_ordinance_read=true],
["1550-appendix-in-tei",x=>x.d.sources[4].editorial_appended_1539_amended_rule_full_text_read=true],
["fake-1550-photos",x=>x.d.sources[4].original_marriage_appendix_pages_seen=true],
["conflate-two",x=>x.d.stage_crosswalk[1].issue="PRIOR_PROMISE_EVIDENCE"],
["source-link-dangling",x=>x.d.claims[0].source="NONE"],
["wrong-license",x=>x.d.ssrq_provenance.license="CC0"],
["IIIF-read-claimed",x=>x.d.exploration[1].actual_marriage_appendix_image_read=true],
["pdf-downloaded",x=>x.d.exploration[0].actual_complete_pdf_download=true],
["lost-image-id",x=>x.d.exploration[2].url="https://www.e-rara.ch/zuz/download/webcache/1000/41466"],
["fake-Ott",x=>x.d.unchanged_blockers.Ott_1855_pp108_122_read=true],
["Article39",x=>x.d.unchanged_blockers.article39_original_text_read=true],
["wrong-reader",x=>x.o.chapter_key="MEDIUM-CALVIN"],
["extra-story-paragraph",x=>x.o.paragraphs.pop()],
["reader-dangling-claim",x=>x.o.paragraph_evidence[2].claims=["C404-99"]],
["conflated-label",x=>x.o.concept_cards[1].legal_function="PUBLIC_CHURCH_NOTICE"],
["reader-claims-art39",x=>x.o.hard_gates.original_1533_article39_read=true],
["reader-claims-handwritten",x=>x.o.hard_gates.original_1530_handwritten_corrections_read=true],
["reader-claims-appendix",x=>x.o.hard_gates.source1550_marriage_appendix_read=true],
["reader-513",x=>x.o.publication.existing_513_modified=true],
["reader-published",x=>x.o.publication.can_ship=true]];
const data=JSON.parse(readFileSync("research/data/V4_04_1530_MARRIAGE_BANNS_VS_1539_PROMISE_WITNESSES_CROSSWALK_DRAFT.json","utf8"));
const reader=JSON.parse(readFileSync("research/data/V4_04_TWO_BANNS_VS_TWO_WITNESSES_ZWINGLI_READER_DRAFT.json","utf8"));
const err=gate(data,reader);if(err.length){console.error("V404 FAIL",err);process.exit(1)}
console.log("V404 PASS: 1530 church banns twice vs 1539 male witnesses twice, all source and release grades");
if(process.argv.includes("--self-test")){let n=0;for(const [name,fn] of mutations){const v={d:JSON.parse(JSON.stringify(data)),o:JSON.parse(JSON.stringify(reader))};fn(v);if(!gate(v.d,v.o).length){console.error("MISSED V404",name);process.exit(1)}n++;}console.log("V404 PASS "+n+" negative mutations detected");}
