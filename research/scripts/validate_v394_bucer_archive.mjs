#!/usr/bin/env node
/** REFORMATION-ATLAS V3.94 no-network validator; source grade & release hard gates. */
import {readFileSync} from "node:fs";
const validate=function validate(d){
 const e=[],rel=d.release||{},bk=d.primary_book||{},sc=d.sources||[],ch=d.cross_check||[],dig=d.digitization||{},g=d.hard_gates||{},ed=d.edition_disambiguation||{},r=d.reader_extension||{};
 if(d.version!=="V3.94"||d.status!=="RESEARCH_DRAFT"||d.parent_branch!=="research/atlas-v393-bucer-jud-may-june-critical-variants")e.push("metadata");
 for(const k of ["can_ship","main_changed","essays_513_changed","ai_studio_changed","correspondence_sent","external_order_placed"]){if(rel[k]!==false)e.push("release:"+k)}
 if(bk.target_letter!=="Nr.598"||bk.target_date!=="1532-06-23"||bk.printed_150_image_seen!==false||bk.printed_165_image_seen!==false||bk.book_p598_fulltext_read!==false||bk.book_pdf_hash!==null)e.push("printed_book");
 if(sc.length!==9||new Set(sc.map(s=>s.id)).size!==9||sc.some(s=>s.facsimile!==false))e.push("source_count_or_facsimile");
 if(sc.find(s=>s.id==="S394-HBBW-II")?.read!=="SEARCH_INDEX_EXCERPT_DIRECT_OPEN_TIMEOUT"||sc.find(s=>s.id==="S394-REVIEW-2011")?.read!=="HTML_DIRECT")e.push("access_grade");
 if(ch.length!==5||ch.find(c=>c.id==="C394-DATE")?.preferred_date!=="1532-06-23"||ch.find(c=>c.id==="C394-NUMBER")?.preferred_number!=="598"||ch.find(c=>c.id==="C394-NUMBER")?.cause!=="UNVERIFIED_EDITORIAL_VARIANT")e.push("identity");
 const a=ch.find(c=>c.id==="C394-ARCHIVE")||{};
 if(a.local_1532_folio_images_seen!==false||a.archive_2021_digitization!==true||a.current_catalog_collection_range!=="1539–1590"||a.explanation!=="UNRESOLVED_DIFFERENT_DESCRIPTION_LEVEL_OR_RENUMBERING")e.push("archive_discrepancy");
 if(ed.hbbw_vol2_110!=="Bullinger -> Martin Bucer, 12 July 1532"||ed.hbbw_vol2_111!=="Martin Bucer -> Bullinger, 12 July 1532"||!ed.rott_bullinger_und_strassburg.includes("not an alias"))e.push("different_items");
 for(const k of ["specific_eii345_126_141_url","specific_eii345_122_125_url","target_image_sha256"]){if(dig[k]!==null)e.push("invented_image:"+k);}
 if(dig.target_image_downloaded!==false||dig.target_image_visually_verified!==false||dig.hypothetical_mismatched_image_do_not_use!==true)e.push("facsimile_guard");
 if(!Array.isArray(r.target_ids)||r.target_ids.join("|")!=="MEDIUM-MARBURG|MEDIUM-ZWINGLI|MEDIUM-AUGSBURG"||r.published!==false||r.provenance_status!=="REVIEW_ONLY_NOT_IMPORTED")e.push("reader_guard");
 for(const k of ["bcor_viii598_150_165_images_seen","eii345_126_141_images_seen","eii345_122_125_images_seen","rott_1978_489_491_seen","parker_ms119_images_seen"]){if(g[k]!==false)e.push("inherited:"+k)}
 if(g.bucer_vadian_1536_07_23_equals_25!=="UNRESOLVED"||g.corrected_zurich_catalog_id!=="CH-002121-2-991170608445805501"||g.preferred_1532_06_23_not_primary_date_line!==true)e.push("date_and_id");
 return e;
};
const mutations=[["fake_book",x=>x.primary_book.book_p598_fulltext_read=true],
["fake_page",x=>x.primary_book.printed_150_image_seen=true],
["premature_ship",x=>x.release.can_ship=true],
["fake_archive",x=>x.cross_check[3].local_1532_folio_images_seen=true],
["range_erase",x=>x.cross_check[3].current_catalog_collection_range="1532–1532"],
["fabricated_url",x=>x.digitization.specific_eii345_126_141_url="https://example.com"],
["wrong_facsimile",x=>x.digitization.hypothetical_mismatched_image_do_not_use=false],
["false_independence",x=>x.sources[2].read="HTML_DIRECT"],
["mix_reply",x=>x.edition_disambiguation.hbbw_vol2_110=x.edition_disambiguation.hbbw_vol2_111],
["conflate_rott",x=>x.edition_disambiguation.rott_bullinger_und_strassburg="Alias for Rott 1978"],
["promote_webapp",x=>x.reader_extension.published=true],
["merge1536",x=>x.hard_gates.bucer_vadian_1536_07_23_equals_25="PROVEN"],
["claim_rott",x=>x.hard_gates.rott_1978_489_491_seen=true],
["claim_parker",x=>x.hard_gates.parker_ms119_images_seen=true]];
const path=process.argv.find(x=>x.endsWith(".json")) || "research/data/V3_94_BUCER598_ARCHIVE_DIGITIZATION_EVIDENCE_DRAFT.json";
const data=JSON.parse(readFileSync(path,"utf8"));
const errors=validate(data);if(errors.length){console.error("FAIL",errors);process.exit(1);}
console.log("PASS: V3.94 bibliographic date / archive digitization / manuscript access / release gates");
if(process.argv.includes("--self-test")) {
  let passed=0;
  for(const [name,mutate] of mutations){const x=JSON.parse(JSON.stringify(data));mutate(x);if(!validate(x).length){console.error("FAIL undetected:",name);process.exit(1);}passed++;}
  console.log("PASS: "+passed+" simulated false-positive scenarios rejected");
}
