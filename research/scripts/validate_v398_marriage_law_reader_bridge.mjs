#!/usr/bin/env node
import {readFileSync} from "node:fs";
const validate=function validate(d,p,b,prior){
const errs=[],a=d.teiletters||[],sc=d.sources||[],cla=d.claims||[],t=d.timeline||[],r=d.release||{};
if(d.version!=="V3.98"||d.status!=="RESEARCH_DRAFT")errs.push("metadata");
for(const k of ["can_ship","main_modified","readers_513_modified","ai_studio_modified","contact_sent","full_edition_copied","facsimiles_copied"])if(r[k]!==false)errs.push("release:"+k);
if(d.upstream?.commit!=="dc9fb5290c210023a6a9182e8e3102c1f6dff734"||d.upstream?.tei_license!=="CC BY-NC-ND 3.0 CH")errs.push("upstream");
if(a.map(x=>x.id).join("|")!=="HBBW3-222|HBBW3-233|HBBW3-239|HBBW3-241|HBBW3-275"||a.map(x=>x.anchors.length).join("|")!=="1|5|2|4|2")errs.push("witness-list");
if(a.some(x=>x.git_blob_sha?.length!==40||x.archival_folio_seen!==false||x.image_bytes_downloaded!==0||x.images_sha256!==null||x.zone_line_pairs!==x.line_count||x.unpaired_zone_count!==x.zone_count-x.line_count))errs.push("witness-grade");
if(a.map(x=>x.unpaired_zone_count).join("|")!=="0|0|2|0|0"||a[2]?.unpaired_zone_ids?.join("|")!=="p1z26-0|p1z27-0"||d.additional_unresolved_visual_issue?.state!=="RESEARCH_UNRESOLVED")errs.push("zone-anomaly");
if(sc.length!==5||sc.find(x=>x.id==="ZH-ARCH-A6-1-NR6")?.original_folio_read!==false||sc.find(x=>x.id==="ZH-ARCH-A6-1-NR7")?.original_folio_read!==false||sc.find(x=>x.id==="ENGELER2023-P103-107")?.web_pdf_screenshot_succeeded!==false)errs.push("source-grades");
if(cla.length!==12||t.length!==9||t.map(x=>x.date).join("|")!=="1532|1533-05-12/14|1533-05-13|1533-05-20|1533-06-08|1533-06-10|1533-07-14|1533-07-15|1533-10-18")errs.push("dated-claims");
const ids=new Set([...a.map(x=>x.id),...sc.map(x=>x.id)]);
for(const claim of cla)for(const ref of claim.source||[]){const [id,s]=ref.split(":s");if(!ids.has(id)||s&&!a.find(x=>x.id===id)?.anchors.some(x=>x.sentence===+s))errs.push("unresolved-citation:"+ref);}
const law=d.legal_outcome||{};
if(law.june10_draft_articles!==44||law.did_all_cities_enact_identical_rules!==false||law.original_minutes_seen!==false||law.details_still_disputed!==true||law.hoped_but_not_present?.join("|")!=="Oswald Myconius|Joachim Vadian")errs.push("overclaim-44");
if(d.inherited_unresolved?.Jul1536_Bucer_Vadian_23_25_equivalence!=="UNRESOLVED"||d.inherited_unresolved?.Rott_1978_p489_491!==false)errs.push("prior-claims");
const preserved=new Set([...(prior.claims||[]).map(x=>x.id),...cla.map(x=>x.id)]);
if(p.status!=="DRAFT_ONLY"||p.source_baseline?.git_blob_sha!=="ac219f34d4caceb2ceae1d64b61e71c53350244c"||p.chapters?.map(x=>x.key).join("|")!=="MARBURG|ZWINGLI|AUGSBURG")errs.push("reader-status");
for(const x of p.chapters||[]){const y=b.chapters.find(z=>z.key===x.key);if(!y||y.id!==x.id||y.title!==x.title||y.lead!==x.lead||y.reading_question!==x.reading_question||JSON.stringify(y.basis)!==JSON.stringify(x.basis)||x.sections?.length!==4||JSON.stringify(y.sections)!==JSON.stringify(x.sections.slice(0,3)))errs.push("baseline-corrupt");if(x.evidence_links?.some(id=>!preserved.has(id)))errs.push("reader-no-source");}
if(p.standalone_episode?.sections?.length!==6||p.standalone_episode?.misconceptions?.length!==3||p.standalone_episode.sections.some(x=>x.sources.some(id=>!preserved.has(id))))errs.push("episode");
if(p.standalone_episode?.publication?.can_ship!==false||p.publication_gate?.can_ship!==false||p.publication_gate?.existing_513_modified!==false)errs.push("publication");
return errs;
};
const mods=[["ship",x=>x.d.release.can_ship=true],
["fake_image",x=>x.d.teiletters[2].archival_folio_seen=true],
["extra_zones",x=>x.d.teiletters[2].unpaired_zone_ids=[]],
["wrong_law",x=>x.d.legal_outcome.june10_draft_articles=45],
["full_uniformity",x=>x.d.legal_outcome.did_all_cities_enact_identical_rules=true],
["Vadian_present",x=>x.d.legal_outcome.hoped_but_not_present=[]],
["phantom_folio",x=>x.d.sources[1].original_folio_read=true],
["pdf_screenshot",x=>x.d.sources[2].web_pdf_screenshot_succeeded=true],
["misdated_Basel",x=>x.d.timeline[2].date="1533-05-12"],
["misdated_July",x=>x.d.timeline[7].date="1533-07-14"],
["dangling_ref",x=>x.d.claims[2].source=["HBBW3-999:s1"]],
["wrong_s",x=>x.d.claims[3].source=["HBBW3-233:s99"]],
["date_merge_1536",x=>x.d.inherited_unresolved.Jul1536_Bucer_Vadian_23_25_equivalence="PROVEN"],
["reader_replace",x=>x.p.chapters[0].sections[0].body="new"],
["reader_invalid",x=>x.p.chapters[1].evidence_links=["CL398-999"]],
["story_unpublished_violation",x=>x.p.standalone_episode.publication.can_ship=true],
["story_remove",x=>x.p.standalone_episode.sections.pop()],
["prior_overwritten",x=>x.b.chapters.find(z=>z.key==="AUGSBURG").lead="different"]];
const d=JSON.parse(readFileSync("research/data/V3_98_1533_MARRIAGE_LAW_CRITICAL_CROSSWALK_DRAFT.json","utf8"));
const p=JSON.parse(readFileSync("research/data/V3_98_THREE_MEDIUM_READERS_AND_MARRIAGE_COURTS_STANDALONE_DRAFT.json","utf8"));
const b=JSON.parse(readFileSync("data/deep/atlas_v254_medium_depth_ten_readers.json","utf8"));
const prior=JSON.parse(readFileSync("research/data/V3_97_BERN_ZURICH_1533_OFFICIAL_TEI_EVIDENCE_DRAFT.json","utf8"));
const e=validate(d,p,b,prior);if(e.length){console.error("FAIL V3.98",e);process.exit(1)}
console.log("PASS: V3.98 source, dates, 44 article non-uniformity and 3 unchanged original chapters");
if(process.argv.includes("--self-test")){let n=0;for(const [name,change] of mods){const x={d:JSON.parse(JSON.stringify(d)),p:JSON.parse(JSON.stringify(p)),b:JSON.parse(JSON.stringify(b)),prior:JSON.parse(JSON.stringify(prior))};change(x);if(!validate(x.d,x.p,x.b,x.prior).length){console.error("MISSED",name);process.exit(1)}n++}console.log("PASS: "+n+" fault injections rejected")}
