#!/usr/bin/env node
/** V4.03 read-only source witness, edition-variant and publication-rights audit. */
import {readFileSync} from "node:fs";
const validate=function validate(d,o){
 const errs=[],s=d.witnesses||[],ids=new Set(s.map(x=>x.id)),c=d.claims||[],ci=new Set(c.map(x=>x.id)),pub=d.release||{};
 if(d.version!=="V4.03"||d.status!=="RESEARCH_DRAFT"||d.parent_branch!=="research/atlas-v402-1539-original-print-two-witness-visual-proof")errs.push("version");
 for(const k of ["can_ship","main_modified","essays_513_modified","ai_studio_modified","prior_research_overwritten","public_merged","full_scholarly_tei_reproduced","archival_images_reproduced"])if(pub[k]!==false)errs.push("release:"+k);
 if(s.length!==9||ids.size!==9||c.length!==12||ci.size!==12||d.crosswalk?.length!==5)errs.push("structure");
 for(const z of c)if(z.source?.some(id=>!ids.has(id)))errs.push("claim-source:"+z.id);
 const ss=Object.fromEntries(s.map(x=>[x.id,x]));
 if(ss["W403-1539-EXTRACT"]?.pdf_pages_visually_checked?.join(",")!=="15,16"||ss["W403-1539-EXTRACT"]?.complete_1539_ordinance!==false||ss["W403-1539-EXTRACT"]?.excerpt_annual_reading_target!==4||ss["W403-1539-EXTRACT"]?.actual_reading_attendance_confirmed!==false)errs.push("1539-proof");
 const raw=ss["W403-1550-PRINT"]||{};
 if(raw.doi!=="10.3931/e-rara-155"||raw.shelfmark!=="Zentralbibliothek Zürich AW 1025"||raw.first_main_page_visually_checked!==true||raw.marriage_appendix_specific_pages_seen!==false||raw.marriage_appendix_actual_text_read!==false||raw.pdf_sha256!==null||raw.pdf_bytes_read!==0||raw.source_has_public_domain_mark!==true)errs.push("1550-original-scope");
 const e=ss["W403-1550-SSRQ-CRITICAL-TEI"]||{};
 if(e.blob_sha!=="34e398a32c3b2345c415e98882493e7adbd4e039"||e.upstream_commit!=="c6f409c719dfb46ded238e4c7f7b1d5b5391dbbe"||e.main_mandate_items!==15||e.main_mandate_body_directly_read!==true||e.full_appended_1539_marriage_ordinance_in_Tei_body!==false||e.editorial_note_says_appended_1539_rule_modified!==true||e.editorial_note_says_appended_1532_synod_modified!==true||e.these_two_1550_variants_not_same_comparison_as_1539_vs_1550_marriage!==true||e.edition_license!=="CC BY-NC-SA 4.0")errs.push("edition");
 if(ss["W403-1550-INCOMPLETE"]?.missing_leaf_count!==4||ss["W403-1550-INCOMPLETE"]?.missing_leaves_printed!=="[15]–[18]"||ss["W403-1550-INCOMPLETE"]?.not_usable_as_complete_original_for_marriage_collation!==true)errs.push("missing-leaves");
 if(ss["W403-2011-CHURCH-ORDERS-TOC"]?.printed_vol1_no75_start_page!==176||ss["W403-2011-CHURCH-ORDERS-TOC"]?.printed_vol1_no119_start_page!==259||ss["W403-2011-CHURCH-ORDERS-TOC"]?.actual_edited_pages_176_181_seen!==false)errs.push("2011-index-only");
 if(ss["W403-1539-ARCHIVE-FULL"]?.full_law_text_read!==false||ss["W403-OTT1855-TEIL2"]?.source_target_text_read!==false||ss["W403-JULY1533-MINUTES"]?.article_39_topic_verified!==false)errs.push("unread-sources");
 const counts=d.summary||{};
 if(counts.total_witnesses!==9||counts.total_grounded_claims!==12||counts.crosswalk_topics!==5||counts.original_1550_marriage_appendix_pages_seen!==0||counts.modern_1550_main_sections_read!==15||counts.modern_1550_1539_appendix_full_text_available!==false||counts.article39_1533_identity_verified!==false||counts.ott1855_target_pages_read!==false||counts.full_1539_statute_pages_read!==false)errs.push("summary");
 if(d.copyright?.ssrq_2022_edited_tei!=="CC BY-NC-SA 4.0"||d.copyright?.zentrale_1539_1550_print!=="Public Domain Mark"||d.copyright?.modern_2011_full_edited_text_copied!==false)errs.push("rights");
 if(o.version!=="V4.03-READER-REVIEW"||o.status!=="RESEARCH_DRAFT_NOT_PUBLISHED"||o.target!=="MEDIUM-ZWINGLI"||o.paragraphs?.length!==4||o.evidence?.length!==4)errs.push("reader");
 if(o.evidence?.some(x=>x.ids.some(id=>!ci.has(id)))||o.evidence?.[2]?.ids.join(",")!=="C403-03,C403-04"||o.evidence?.[2]?.primary!=="W403-1550-SSRQ-CRITICAL-TEI")errs.push("reader-citations");
 const z=o.scope||{};
 for(const k of ["scan_1539_extract_p15_p16_seen","scan_1550_composite_first_main_page_seen","edited_1550_main_15_sections_read","distinct_1550_variant_issue_from_1539_to_1550_comparison","wedding_rules_1550_main_are_not_1539_appendix","two_annual_1550_readings_not_same_as_four_annual_1539_extract"])if(z[k]!==true)errs.push("reader-scope-true:"+k);
 for(const k of ["scan_1550_marriage_appendix_seen","edited_1550_full_marriage_appendix_read","article39_from_1533_read","full_1539_statute_read","Ott_1855_pp108_122_read","year_2011_edited_full_text_read"])if(z[k]!==false)errs.push("reader-scope-false:"+k);
 if(o.event_candidate?.content_status!=="DRAFT_ONLY"||o.event_candidate?.source_dates?.length!==3)errs.push("reader-event");
 for(const k of ["can_ship","main_modified","existing_513_modified","ai_studio_modified","historian_approved","rights_approved"])if(o.publication?.[k]!==false)errs.push("reader-release:"+k);
 return errs;
};
const mutants=[["ship",x=>x.d.release.can_ship=true],
["touch_main",x=>x.d.release.main_modified=true],
["source_count",x=>x.d.witnesses.pop()],
["fake_1539_full",x=>x.d.witnesses.find(z=>z.id==="W403-1539-EXTRACT").complete_1539_ordinance=true],
["read_1550_appendix",x=>x.d.witnesses.find(z=>z.id==="W403-1550-PRINT").marriage_appendix_actual_text_read=true],
["fake_image_hash",x=>x.d.witnesses.find(z=>z.id==="W403-1550-PRINT").pdf_sha256="fake"],
["fake_image_pages",x=>x.d.witnesses.find(z=>z.id==="W403-1550-PRINT").marriage_appendix_specific_pages_seen=true],
["fake_edited_appendix",x=>x.d.witnesses.find(z=>z.id==="W403-1550-SSRQ-CRITICAL-TEI").full_appended_1539_marriage_ordinance_in_Tei_body=true],
["wrong_tei_blob",x=>x.d.witnesses.find(z=>z.id==="W403-1550-SSRQ-CRITICAL-TEI").blob_sha="f".repeat(40)],
["shift_fifteen",x=>x.d.witnesses.find(z=>z.id==="W403-1550-SSRQ-CRITICAL-TEI").main_mandate_items=16],
["erase_modified_note",x=>x.d.witnesses.find(z=>z.id==="W403-1550-SSRQ-CRITICAL-TEI").editorial_note_says_appended_1539_rule_modified=false],
["merge_1550_variant",x=>x.d.witnesses.find(z=>z.id==="W403-1550-SSRQ-CRITICAL-TEI").these_two_1550_variants_not_same_comparison_as_1539_vs_1550_marriage=false],
["missing_leaf_dismissed",x=>x.d.witnesses.find(z=>z.id==="W403-1550-INCOMPLETE").not_usable_as_complete_original_for_marriage_collation=false],
["missing_leaf_count",x=>x.d.witnesses.find(z=>z.id==="W403-1550-INCOMPLETE").missing_leaf_count=0],
["2011_claim_read",x=>x.d.witnesses.find(z=>z.id==="W403-2011-CHURCH-ORDERS-TOC").actual_edited_pages_176_181_seen=true],
["Ott_claim_read",x=>x.d.witnesses.find(z=>z.id==="W403-OTT1855-TEIL2").source_target_text_read=true],
["Art39_claim",x=>x.d.witnesses.find(z=>z.id==="W403-JULY1533-MINUTES").article_39_topic_verified=true],
["witness_source_dangling",x=>x.d.claims[0].source=["MISSING"]],
["false_count",x=>x.d.summary.modern_1550_main_sections_read=16],
["wrong_license",x=>x.d.copyright.ssrq_2022_edited_tei="CC0"],
["reader_wrong_key",x=>x.o.target="MEDIUM-CALVIN"],
["reader_bad_ref",x=>x.o.evidence[2].ids=["C403-30"]],
["reader_attaches_to_1539",x=>x.o.evidence[2].primary="W403-1539-EXTRACT"],
["reader_full_copy",x=>x.o.scope.edited_1550_full_marriage_appendix_read=true],
["reader_equal_freq",x=>x.o.scope.two_annual_1550_readings_not_same_as_four_annual_1539_extract=false],
["reader_art39",x=>x.o.scope.article39_from_1533_read=true],
["reader_shipped",x=>x.o.publication.can_ship=true],
["reader_513",x=>x.o.publication.existing_513_modified=true],
["wrong_reader_sections",x=>x.o.paragraphs.pop()],
["reader_event_live",x=>x.o.event_candidate.content_status="PUBLISHED"]];
const d=JSON.parse(readFileSync("research/data/V4_03_1550_COMPOSITE_1539_MARRIAGE_WITNESS_CROSSWALK_DRAFT.json","utf8"));
const o=JSON.parse(readFileSync("research/data/V4_03_1550_PUBLIC_ORDER_VS_MARRIAGE_APPENDIX_READER_DRAFT.json","utf8"));
const baseline=validate(d,o);if(baseline.length){console.error("V403 FAIL",baseline);process.exit(1)}
console.log("V403 PASS: later 1550 composite and 1539 marriage appendix kept distinct");
if(process.argv.includes("--self-test")){let passed=0;for(const [name,fn] of mutants){const x={d:JSON.parse(JSON.stringify(d)),o:JSON.parse(JSON.stringify(o))};fn(x);if(!validate(x.d,x.o).length){console.error("MISSED V403",name);process.exit(1)}passed++;}console.log("V403 PASS "+passed+" negative mutations detected");}
