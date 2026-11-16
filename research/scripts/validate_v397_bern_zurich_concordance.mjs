#!/usr/bin/env node
/** REFORMATION-ATLAS V3.97 source-chain & prose-overlay integrity check; no web or writes. */
import {readFileSync} from "node:fs";
const validate=function validate(data,overlay){
 const errs=[];
 if(data?.version!=="V3.97"||data?.status!=="RESEARCH_DRAFT"||data?.parent_branch!=="research/atlas-v396-bullinger-tei-line-zone-and-doctrine-audit")errs.push("data-version");
 const gates=["can_ship","main_modified","essay_513_modified","ai_studio_modified","existing_medium_readers_modified","outreach_sent","original_tei_reproduced","scan_reproduced"];
 for(const key of gates)if(data.publication?.[key]!==false)errs.push("publication-"+key);
 if(data.provenance?.source_repository!=="stazh/bullinger-korpus-tei"||data.provenance?.pinned_commit!=="dc9fb5290c210023a6a9182e8e3102c1f6dff734"||data.provenance?.tei_license!=="CC BY-NC-ND 3.0 CH"||data.provenance?.facsimile_license!=="CC BY-SA 4.0"||data.provenance?.physical_original_seen!==false)errs.push("source-license");
 const letters=data.overview_1533||[],num=letters.map(x=>x.edition_number),imageCounts=letters.map(x=>x.register_graphic_count),zones=letters.map(x=>x.zone_count);
 if(num.join(",")!=="219,220,221,228"||imageCounts.join(",")!=="2,4,2,2"||zones.join(",")!=="43,78,23,19"||letters.map(x=>x.text_sentence_count).join(",")!=="15,34,24,24")errs.push("source-shape");
 if(letters.some(x=>x.source_blob_sha.length!==40||x.source_url.includes("/main/")||x.original_folio_photo_read!==false||x.image_bytes_downloaded!==0||x.image_sha256!==null||x.short_quote_word_count>25||x.paired_zone_line_count!==x.zone_count||x.line_id_count!==x.zone_count))errs.push("source-provenance");
 if(letters.filter(x=>x.printed_year_bracketed).map(x=>x.edition_number).join(",")!=="220,228")errs.push("editorial-bracket-year");
 const t=data.totals||{};
 if(t.letters!==4||t.sentences!==97||t.graphics!==10||t.zones!==163||t.line_ids!==163||t.paired!==163||t.passages!==17)errs.push("counts");
 if(data.additional_critical_edition?.id!=="S397-CAPITO2015-EP507-N3"||data.additional_critical_edition?.print_page!==114||data.additional_critical_edition?.pdf_page_index_zero_based!==144||data.additional_critical_edition?.pdf_page_image_visually_checked!==true||data.additional_critical_edition?.editorial_synod_dates!=="1533-05-12 through 1533-05-14")errs.push("Capito2015-source");
 if(data.additional_critical_edition?.attendee_number_120_source!=="HBBW III Nr228 (Haller), cited by Kooistra; this is not a second independent count")errs.push("participant-dependence");
 const claims=data.claims||[],claimIds=claims.map(x=>x.id),claimIndex=new Set(claimIds);
 if(claims.length!==13||claimIndex.size!==13||!claimIndex.has("C397-13"))errs.push("claims");
 const letterLookup=new Map(letters.map(x=>[x.edition_number,x]));
 const isEvidenceRef=(ref)=>{
  if(ref==="S397-CAPITO2015-EP507-N3")return true;
  const m=ref.match(/^HBBW3-(\d+):s(\d+)$/);
  return !!m && (letterLookup.get(+m[1])?.selected_passages||[]).some(x=>x.sentence_n===+m[2]);
 };
 for(const c of claims)if(c.sources?.some(x=>!isEvidenceRef(x)))errs.push("bad-claim-ref:"+c.id);
 const countClaim=claims.find(x=>x.id==="C397-05");
 if(countClaim?.reported_participants!==120||countClaim?.independent_count_verified!==false)errs.push("count-not-independent");
 if(claims.find(x=>x.id==="C397-07")?.all_Lutheran_Zurich_eucharistic_divergence_resolved!==false)errs.push("unauthorized-consensus");
 const synod=claims.find(x=>x.id==="C397-13");
 if(synod?.event_start!=="1533-05-12"||synod?.event_end!=="1533-05-14"||synod?.report_date!=="1533-05-29"||synod?.number_120_independently_confirmed!==false||synod?.date_source_is_2015_editorial_note!==true)errs.push("synod-vs-report");
 if(data.historical_interpretation?.May29_is_report_not_synod_date!==true||data.image_access?.actual_image_bytes!==0||data.image_access?.handwritten_date_rows_checked!==false)errs.push("date-or-image-access");
 if(data.related_existing_context?.no_secondary_inference_as_folio!==true)errs.push("original-image-hard-gate");
 if(overlay.version!=="V3.97-READER-OVERLAY"||overlay.status!=="REVIEW_ONLY_NOT_PUBLISHED"||overlay.baseline_reader_file!=="data/deep/atlas_v254_medium_depth_ten_readers.json")errs.push("overlay-top");
 const ovs=overlay.overlays||[];
 if(ovs.map(x=>x.target_id).join(",")!=="MEDIUM-MARBURG,MEDIUM-ZWINGLI,MEDIUM-AUGSBURG"||ovs.some(x=>x.paragraphs?.length!==3||x.evidence_claim_ids.some(id=>!claimIndex.has(id))||x.evidence_claim_ids.indexOf("C397-13")<0))errs.push("overlay-targets-evidence");
 if(overlay.timeline?.length!==4||overlay.timeline.some(x=>x.evidence.some(ref=>!isEvidenceRef(ref)&&!claimIndex.has(ref))))errs.push("timeline");
 if(overlay.synod_context?.start_date!=="1533-05-12"||overlay.synod_context?.end_date!=="1533-05-14"||overlay.synod_context?.evidence_id!=="C397-13"||overlay.synod_context?.independent_participant_count!==false||overlay.synod_context?.state!=="REVIEW_ONLY")errs.push("overlay-synod-context");
 if(overlay.episode?.publication_gate!=="REVIEW_ONLY"||overlay.episode?.paragraphs?.length!==4||overlay.episode?.key_evidence.some(id=>!claimIndex.has(id))||overlay.episode?.misconceptions?.length!==4)errs.push("episode");
 if(overlay.proposed_review?.historian_approved!==false||overlay.proposed_review?.webapp_import_approved!==false||overlay.evidence_condition?.copy_or_edit_513!==false||overlay.evidence_condition?.publish!==false)errs.push("overlay-release");
 return errs;
};
const mutations=[["ship",({d})=>{d.publication.can_ship=true;}],
["change_main",({d})=>{d.publication.main_modified=true;}],
["published_513",({d})=>{d.publication.essay_513_modified=true;}],
["unpin",({d})=>{d.provenance.pinned_commit="main";}],
["alter_autograph",({d})=>{d.overview_1533[1].original_folio_photo_read=true;}],
["fake_scan_hash",({d})=>{d.overview_1533[1].image_sha256="fake";}],
["bad_zones",({d})=>{d.overview_1533[1].paired_zone_line_count=77;}],
["miscount_people",({d})=>{d.claims.find(x=>x.id==="C397-05").reported_participants=121;}],
["invent_double_count",({d})=>{d.claims.find(x=>x.id==="C397-05").independent_count_verified=true;}],
["revoke_uncertainty",({d})=>{d.claims.find(x=>x.id==="C397-07").all_Lutheran_Zurich_eucharistic_divergence_resolved=true;}],
["wrong_event_date",({d})=>{d.claims.find(x=>x.id==="C397-13").event_start="1533-05-29";}],
["wrong_report_date",({d})=>{d.claims.find(x=>x.id==="C397-13").report_date="1533-05-14";}],
["fake_new_participant_count",({d})=>{d.claims.find(x=>x.id==="C397-13").number_120_independently_confirmed=true;}],
["erase_editorial_bracket",({d})=>{d.overview_1533[1].printed_year_bracketed=false;}],
["capito_wrong_page",({d})=>{d.additional_critical_edition.print_page=115;}],
["capito_photo_claim",({d})=>{d.additional_critical_edition.pdf_page_image_visually_checked=false;}],
["unlicensed_copy",({d})=>{d.publication.original_tei_reproduced=true;}],
["delete_main_claim",({d})=>{d.claims.splice(0,1);}],
["dangling_evidence",({d})=>{d.claims[0].sources=["HBBW3-999:s1"];}],
["wrong_reader_key",({o})=>{o.overlays[0].target_id="MEDIUM-CALVIN";}],
["reader_published",({o})=>{o.status="PUBLISHED";}],
["approve",({o})=>{o.proposed_review.webapp_import_approved=true;}],
["episode_claim_missing",({o})=>{o.episode.key_evidence=["C397-99"];}],
["timeline_date_moved",({o})=>{o.synod_context.start_date="1533-05-29";}],
["overlay_synod_120_independent",({o})=>{o.synod_context.independent_participant_count=true;}],
["unverified_extra_media",({d})=>{d.image_access.actual_image_bytes=12345;}]];
const data=JSON.parse(readFileSync("research/data/V3_97_BERN_ZURICH_1533_OFFICIAL_TEI_EVIDENCE_DRAFT.json","utf8"));
const overlay=JSON.parse(readFileSync("research/data/V3_97_BERN_1533_FOUR_SCENE_READER_OVERLAY_DRAFT.json","utf8"));
const errors=validate(data,overlay);if(errors.length){console.error("V397 FAIL",errors);process.exit(1);}
console.log("V397 PASS: four TEI letters, Capito synod date, 120-person provenance and reader-only gates");
if(process.argv.includes("--self-test")){
  let rejected=0; for(const [name,mutate] of mutations){const x={d:JSON.parse(JSON.stringify(data)),o:JSON.parse(JSON.stringify(overlay))};mutate(x);if(!validate(x.d,x.o).length){console.error("UNDETECTED FAULT:",name);process.exit(1)}rejected++;}
  console.log("V397 PASS: "+rejected+" mutation failures detected");
}
