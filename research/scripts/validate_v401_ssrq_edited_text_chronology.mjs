#!/usr/bin/env node
/** V4.01 conservative date-attribution / SSRQ scholarly TEI / research release validator. */
import {readFileSync} from "node:fs";
const validate=function validate(d,o){
 const errors=[],pub=d.release||{},source=d.official_source||{},ws=d.witnesses||[],facts=d.direct_transcription_results||[],notes=d.modern_editorial_notes||[],err=d.explicit_erratum||{},miss=d.missing_sources||{},r=o.hard_gates||{};
 if(d.version!=="V4.01"||d.status!=="RESEARCH_DRAFT"||d.parent_branch!=="research/atlas-v400-ott1855-alternate-edition-and-1533-marriage-text-witness")errors.push("stage");
 for(const p of ["can_ship","main_modified","essays_513_modified","ai_studio_modified","old_V400_overwritten","full_scholarly_tei_copied","images_copied","contact_sent"])if(pub[p]!==false)errors.push("release:"+p);
 if(source.repo!=="SSRQ-SDS-FDS/editio-data"||source.ref!=="v1.1.0"||source.commit!=="c6f409c719dfb46ded238e4c7f7b1d5b5391dbbe"||source.license!=="CC BY-NC-SA 4.0")errors.push("official_version");
 if(ws.length!==2||ws[0]?.blob_sha!=="4d9145fc3564bed1044b6fa75d14ee042c9c6b33"||ws[1]?.blob_sha!=="3b15cd7526f8d1eeba718162681c1c9b7a33ae61"||ws[0]?.date!=="1525-05-10"||ws[1]?.date!=="1533-05-20"||ws.some(x=>x.edited_tei_direct_read!==true))errors.push("witnesses");
 if(ws[0]?.original_print_image_seen!==false||ws[1]?.original_manuscript_photos_seen!==false||ws[1]?.notes_count!==4)errors.push("source_grade");
 if(facts.length!==6||facts[2]?.agenda?.length!==3||facts[2]?.agenda?.some(x=>x.draft44_article_number_known!==undefined)||facts[3]?.part!=="DORSAL_ADDENDUM_OTHER_HAND"||facts[3]?.date_when!=="1533-06-10"||facts[3]?.original_photo_seen!==false||facts[5]?.all_four_were_marriage_judges!==false)errors.push("historical_text");
 if(notes.length!==4||notes[1]?.revised!=="1539"||notes[1]?.consulted!=="1533"||notes[1]?.original_1539_print_read!==false||notes[2]?.direct_july_15_minutes_seen!==false||notes[2]?.all_five_cities_enactment_proven!==false)errors.push("notes");
 if(d.external_archival_corrob?.length!==2||d.external_archival_corrob.some(x=>x.date!=="1539-07-12"||x.physical_print_read!==false))errors.push("1539_archives");
 if(err.supersedes_version!=="V4.00"||err.corrected_year!==1539||err.old_files_kept_for_audit!==true||err.does_not_prove_1878_historian_wrong!==true)errors.push("correction");
 if(miss.Ott1855_printed_pages_108_122_seen!==false||miss.july_1533_A6_1_Nr7_minutes_read!==false||miss.article39_exact_text_read!==false||miss.forty_four_article_topics_read!==0||miss.prior_July1536_letter_identity!=="UNRESOLVED")errors.push("older_stops");
 if(o.version!=="V4.01-READER-ERRATUM"||o.status!=="REVIEW_ONLY_NOT_PUBLISHED"||o.target_id!=="MEDIUM-ZWINGLI"||o.corrected_reader_paragraphs?.length!==3||o.chapter_source_support?.length!==3||o.episode_patch?.status!=="REVIEW_ONLY")errors.push("reader-draft");
 if(o.chapter_source_support?.map(x=>x.asserted_date).join("|")!=="1525-05-10|1533-05-20 / annotation 1533-06-10|1539"||o.chapter_source_support?.[2]?.kind!=="MODERN_CRITICAL_EDITION_NOTE_RE_1539")errors.push("reader-attribution");
 if(r.two_witness_requirement_year!==1539||r.V400_incorrect_1533_claim_reused!==false||r.original_1539_print_directly_read!==false||r.corrected_1533_edited_tei_direct_read!==true||r.corrected_1525_edited_tei_direct_read!==true||r.three_issues_equated_to_draft44_articles!==false||r.art39_topic_identified!==false||r.all_five_cities_uniform_enactment_claimed!==false||r.womens_rights_interpretation_needs_historian_review!==true||r.SSRQ_license!=="CC BY-NC-SA 4.0")errors.push("reader-hard");
 for(const p of ["main_modified","existing_513_modified","ai_studio_modified","can_ship","historian_approved","rights_approved"])if(r[p]!==false)errors.push("reader-release:"+p);
 return errors;
};
const mutations=[["release",x=>x.d.release.can_ship=true],
["main",x=>x.d.release.main_modified=true],
["license",x=>x.d.official_source.license="CC0"],
["pin",x=>x.d.official_source.commit="main"],
["bad_1525",x=>x.d.witnesses[0].date="1533-05-20"],
["wrong_blob",x=>x.d.witnesses[1].blob_sha="f".repeat(40)],
["fake_photo",x=>x.d.witnesses[1].original_manuscript_photos_seen=true],
["zero_notes",x=>x.d.witnesses[1].notes_count=0],
["agenda_44",x=>x.d.direct_transcription_results[2].agenda.pop()],
["dorsal_date",x=>x.d.direct_transcription_results[3].date_when="1533-06-11"],
["dorsal_photo",x=>x.d.direct_transcription_results[3].original_photo_seen=true],
["false_judges",x=>x.d.direct_transcription_results[5].all_four_were_marriage_judges=true],
["editor_1533",x=>x.d.modern_editorial_notes[1].revised="1533"],
["year_1539_original",x=>x.d.modern_editorial_notes[1].original_1539_print_read=true],
["minutes_direct",x=>x.d.modern_editorial_notes[2].direct_july_15_minutes_seen=true],
["all_cities_enacted",x=>x.d.modern_editorial_notes[2].all_five_cities_enactment_proven=true],
["archival_date",x=>x.d.external_archival_corrob[0].date="1533-07-12"],
["1878_accused",x=>x.d.explicit_erratum.does_not_prove_1878_historian_wrong=false],
["wrong_correction",x=>x.d.explicit_erratum.corrected_year=1533],
["old_file_overwrite",x=>x.d.explicit_erratum.old_files_kept_for_audit=false],
["Ott_read",x=>x.d.missing_sources.Ott1855_printed_pages_108_122_seen=true],
["Art39_claim",x=>x.d.missing_sources.article39_exact_text_read=true],
["V400_reintroduced",x=>x.o.hard_gates.V400_incorrect_1533_claim_reused=true],
["reader_year",x=>x.o.hard_gates.two_witness_requirement_year=1533],
["reader_live",x=>x.o.hard_gates.can_ship=true],
["reader_uncleared",x=>x.o.hard_gates.womens_rights_interpretation_needs_historian_review=false],
["reader_art39",x=>x.o.hard_gates.art39_topic_identified=true],
["wrong_reader_source",x=>x.o.chapter_source_support[2].asserted_date="1533"],
["reader_paragraph_missing",x=>x.o.corrected_reader_paragraphs.pop()]];
const data=JSON.parse(readFileSync("research/data/V4_01_SSRQ_DIRECT_TEI_1525_1533_1539_ERRATUM_DRAFT.json","utf8"));
const reader=JSON.parse(readFileSync("research/data/V4_01_ZURICH_1525_1533_1539_READER_CORRECTION_DRAFT.json","utf8"));
const errors=validate(data,reader);if(errors.length){console.error("V401 ERROR",errors);process.exit(1);}
console.log("V401 PASS: SSRQ pinned edited texts, 1533 dorsal, modern 1539 two-witness correction, research rights");
if(process.argv.includes("--self-test")){let n=0;for(const [name,fn] of mutations){const x={d:JSON.parse(JSON.stringify(data)),o:JSON.parse(JSON.stringify(reader))};fn(x);if(!validate(x.d,x.o).length){console.error("FAULT NOT CAUGHT",name);process.exit(1)}n++;}console.log("V401 PASS "+n+" adversarial mutations caught");}
