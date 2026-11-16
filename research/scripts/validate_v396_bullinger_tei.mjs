#!/usr/bin/env node
/** V3.96 source-pinned no-network research validator. Run from repository root. */
import {readFileSync} from "node:fs";
const verify=function verify(d){
 const errs=[],rs=d.release||{},so=d.source||{},ls=d.letter_analyses||[],u=d.uncertainties||{},rr=d.rights||{};
 if(d.version!=="V3.96"||d.status!=="RESEARCH_DRAFT")errs.push("version");
 for(const k of ["can_ship","main_modified","essays_513_modified","ai_studio_modified","original_tei_republished","facsimiles_republished","editor_contact_sent"])if(rs[k]!==false)errs.push("release_"+k);
 if(so.repo!=="stazh/bullinger-korpus-tei"||so.commit!=="dc9fb5290c210023a6a9182e8e3102c1f6dff734"||so.tei_license!=="CC BY-NC-ND 3.0 CH"||so.facsimile_license!=="CC BY-SA 4.0")errs.push("source");
 if(ls.length!==2||ls.map(x=>x.file_id).join(",")!=="file10140,file10250")errs.push("files");
 const a=ls[0]||{},b=ls[1]||{},x=a.structure||{},y=b.structure||{};
 if(x.sentence_count!==157||x.graphics?.length!==8||x.zone_count!==0||x.line_tags_with_ids!==0||x.matched_lines!==0||x.visual_verification!==false)errs.push("shape10140");
 if(y.sentence_count!==15||y.graphics?.length!==2||y.zone_count!==43||y.line_tags_with_ids!==43||y.matched_lines!==43||y.visual_verification!==false)errs.push("shape10250");
 if(y.graphics?.[0]?.zones!==38||y.graphics?.[1]?.zones!==5||x.graphics?.some(q=>q.zones!==0))errs.push("zones");
 if(a.blob_sha!=="3c51c77d8a588fd8fffa57d8df6365b65d6c3763"||b.blob_sha!=="2d9336d07262ac81e78624b9885155a486283b37")errs.push("blob");
 for(const item of ls){
  if(item.manuscript_image_verified!==false||item.structure.image_bytes_downloaded!==0)errs.push("physical_image");
  if(item.quoted_word_count>25||item.anchors?.some(z=>z.grade!=="DIRECT_TEI_CRITICAL_EDITION_TEXT"||z.original_manuscript_verified!==false))errs.push("citations");
 }
 if(a.anchors?.length!==9||b.anchors?.length!==8||a.anchors?.find(z=>z.sentence===20)?.edition_page!=="154"||b.anchors?.find(z=>z.sentence===8)?.edition_page!=="120")errs.push("passages");
 if(a.anchors?.find(z=>z.sentence===83)?.brief_source_excerpt!=="male sartam pacem"||b.anchors?.find(z=>z.sentence===4)?.brief_source_excerpt!=="priori anno in iulio")errs.push("quotes");
 if(u.image_extent?.catalog_folios!=="1362r-1364r"||u.image_extent?.registered_graphics!=="1362r-1365v"||u.image_extent?.all_8_belong_to_letter!=="UNVERIFIED")errs.push("image_extent");
 if(u.recollection_date?.forced_literal_rewrite!==false||u.june_letter?.original_bucer_jud_letter_read!==false||u.june_letter?.book_viii_nr598_page_seen!==false||u.june_letter?.archive_catalogue_1539_1590_discrepancy!=="UNRESOLVED")errs.push("editorial_date");
 if(u.inaccessible_image?.photo_read!==false||u.inaccessible_image?.photo_sha256!==null)errs.push("image_failure");
 if(u.older_research?.rott_1978_pages_489_491_seen!==false||u.older_research?.parker_ms119_images_seen!==false||u.older_research?.bucer_vadian_july1536_23_25_same!=="UNRESOLVED")errs.push("1536_unverified");
 if(d.research_to_reader?.status!=="REVIEW_ONLY_NOT_PUBLISHED"||d.research_to_reader?.targets?.length!==3||rr.edited_tei_copied_entirely!==false||rr.images_embedded!==false)errs.push("release_reader_rights");
 return errs;
};
const mutations=[["ship",z=>z.release.can_ship=true],
["remove_license",z=>z.source.tei_license="Public Domain"],
["wrong_pin",z=>z.source.commit="latest"],
["fake_scan",z=>z.letter_analyses[0].structure.visual_verification=true],
["wrong_zones",z=>z.letter_analyses[1].structure.matched_lines=42],
["wrong_38_5",z=>z.letter_analyses[1].structure.graphics[1].zones=6],
["invent_10140_zones",z=>z.letter_analyses[0].structure.zone_count=157],
["wrong_print_154",z=>z.letter_analyses[0].anchors[3].edition_page="155"],
["wrong_print_120",z=>z.letter_analyses[1].anchors[4].edition_page="119"],
["wrong_latin",z=>z.letter_analyses[1].anchors[1].brief_source_excerpt="priori anno in junio"],
["false_8_in_letter",z=>z.uncertainties.image_extent.all_8_belong_to_letter="YES"],
["wrong_folio",z=>z.uncertainties.image_extent.registered_graphics="1362r-1364r"],
["invent_book",z=>z.uncertainties.june_letter.book_viii_nr598_page_seen=true],
["invent_hash",z=>z.uncertainties.inaccessible_image.photo_sha256="fake"],
["merge_1536",z=>z.uncertainties.older_research.bucer_vadian_july1536_23_25_same="PROVEN"],
["promote_rott",z=>z.uncertainties.older_research.rott_1978_pages_489_491_seen=true],
["promote_reader",z=>z.research_to_reader.status="PUBLISHED"],
["quote_overlimit",z=>z.letter_analyses[1].quoted_word_count=50]];
const fn=process.argv.find(arg=>arg.endsWith(".json"))||"research/data/V3_96_BULLINGER_SENTENCE_ZONE_DOCTRINE_DRAFT.json";
const d=JSON.parse(readFileSync(fn,"utf8"));
const err=verify(d);if(err.length){console.error("FAIL",err);process.exit(1);}
console.log("PASS: V3.96 TEI passage / 43-43 zone / image and rights gates");
if(process.argv.includes("--self-test")) {
 let caught=0;for(const [name,mutate] of mutations){const bad=JSON.parse(JSON.stringify(d));mutate(bad);if(!verify(bad).length){console.error("FAULT NOT DETECTED",name);process.exit(1);}caught++;}
 console.log("PASS: "+caught+" of "+mutations.length+" adversarial cases caught");
}
