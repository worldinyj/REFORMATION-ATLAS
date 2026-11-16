#!/usr/bin/env node
/** V3.95 reproducibility validator. No network access or writes. */
import {readFileSync} from "node:fs";
const validate=function validate(x){
 const e=[],a=x.items||[],r=x.release||{},p=x.origin||{},z=x.anomalies||{},u=x.unresolved||{},t=x.reader_drafts||[];
 if(x.version!=="V3.95"||x.status!=="RESEARCH_DRAFT")e.push("meta");
 for(const k of ["can_ship","main_modified","essays_513_modified","ai_studio_modified","source_tei_republished","images_republished","email_sent"])if(r[k]!==false)e.push(k);
 if(p.repository!=="stazh/bullinger-korpus-tei"||p.commit!=="dc9fb5290c210023a6a9182e8e3102c1f6dff734"||p.text_license!=="CC BY-NC-ND 3.0 CH")e.push("upstream");
 if(a.length!==3||a.map(y=>y.id).join(",")!=="file10125,file10140,file10250"||a.map(y=>y.graphic_count).join(",")!=="0,8,2"||a.some(y=>y.photo_read!==false||y.edited_text_read!==true))e.push("tei_docs");
 if(a[1]?.archive!=="Zürich StA E II 338,1362r-1364r"||a[2]?.archive!=="Zürich StA E II 347,43-44")e.push("shelfmarks");
 if(z.folio_series?.catalog_range!=="1362r-1364r"||z.folio_series?.graphic_filename_range!=="1362r-1365v"||z.folio_series?.same_letter_all_pages!=="UNVERIFIED")e.push("folio_discrepancy");
 if(z.image_access?.actual_jpg_retrieved!==false||z.image_access?.visual_inspection!==false||z.image_access?.sha256!==null)e.push("images_not_seen");
 if(z.archive?.mapping!=="UNRESOLVED"||z.archive?.edited_letter_bcor_viii_598_page_seen!==false)e.push("archive_uncertainty");
 if(x.claims?.[2]?.exact_excerpt!=="priori anno in iulio"||x.claims?.length!==5)e.push("editorial_date");
 if(u.rott_1978_p489_491_seen!==false||u.parker_ms119_images_seen!==false||u.bucer_vadian_july_1536_23_25_identity!=="UNRESOLVED")e.push("inherited");
 if(t.length!==3||t.some(y=>y.published!==false)||t.map(y=>y.target).join(",")!=="MEDIUM-MARBURG,MEDIUM-ZWINGLI,MEDIUM-AUGSBURG")e.push("readers");
 return e;
};
const mutations=[["release",x=>x.release.can_ship=true],
["copied_edit",x=>x.release.source_tei_republished=true],
["claim_photo",x=>x.anomalies.image_access.visual_inspection=true],
["image_hash",x=>x.anomalies.image_access.sha256="invented"],
["photo_tei",x=>x.items[2].photo_read=true],
["missing_8",x=>x.items[1].graphic_count=5],
["folio_range_rewrite",x=>x.anomalies.folio_series.graphic_filename_range="1362r-1364r"],
["unearned_8",x=>x.anomalies.folio_series.same_letter_all_pages="YES"],
["wrong_original_date",x=>x.claims[2].exact_excerpt="priori anno in junio"],
["false_letter",x=>x.anomalies.archive.edited_letter_bcor_viii_598_page_seen=true],
["wrong_archive",x=>x.items[1].archive=x.items[2].archive],
["fake_rott",x=>x.unresolved.rott_1978_p489_491_seen=true],
["merge1536",x=>x.unresolved.bucer_vadian_july_1536_23_25_identity="PROVEN"],
["reader_published",x=>x.reader_drafts[0].published=true],
["upstream_unpinned",x=>x.origin.commit="main"]];
const file=process.argv.find(x=>x.endsWith(".json"))||"research/data/V3_95_BULLINGER_DIRECT_TEI_EVIDENCE_DRAFT.json";
const data=JSON.parse(readFileSync(file,"utf8"));
const violations=validate(data);if(violations.length){console.error("FAIL",violations);process.exit(1)}
console.log("PASS V3.95 pinned official source and image acquisition gates");
if(process.argv.includes("--self-test")) {
 let n=0;for(const [name,fn] of mutations){const x=JSON.parse(JSON.stringify(data));fn(x);if(!validate(x).length){console.error("FAIL missed",name);process.exit(1)}n++;}
 console.log("PASS "+n+" fault injections rejected");
}
