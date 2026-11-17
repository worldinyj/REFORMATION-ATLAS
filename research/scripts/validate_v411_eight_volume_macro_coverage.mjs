#!/usr/bin/env node
/** V4.11 read-only 8-volume L0 inventory, priority and release audit. */
import {readFileSync} from "node:fs";
const validate=function validate(d,md){
 const e=[],v=d.baseline||[],m=d.macro_layers||[],p=d.priority_queue||[],x=d.cross_volume_links||[],ids=new Set(v.map(z=>z.id));
 if(d.version!=="V4.11"||d.status!=="L0_EIGHT_VOLUME_COVERAGE_AUDIT_DRAFT"||d.parent_branch!=="research/atlas-v410-world-christianity-korea-local-agency-l0")e.push("metadata");
 if(v.length!==8||ids.size!==8||v.some((z,i)=>z.id!==`VOL-0${i+1}`||z.canonical_blob_sha?.length!==40||z.baseline_measured?.characters<2000))e.push("eight-volumes");
 if(m.length!==5||m.some((z,i)=>z.version!==(i===4?"V4.10":`V4.0${i+6}`)||z.sha?.length!==40||!z.path.endsWith(".md")))e.push("macro-layers");
 if(p.length!==5||p.some((z,i)=>z.priority!==i+1)||!p[0]?.task?.includes("VOL-06"))e.push("priority-order");
 if(x.length!==8||x.some(z=>!ids.has(z.from)||!ids.has(z.to)))e.push("cross-volume-links");
 if(v[7]?.macro_status!=="THEMATIC_BASELINE_ONLY"||v[7]?.baseline_measured?.representative_events!==0)e.push("vol08-thematic");
 if(d.derived_counts?.eight_baseline_volumes!==8||d.derived_counts?.macro_expanded_volumes!==3||d.derived_counts?.baseline_only_or_thematic_volumes!==5||d.derived_counts?.total_baseline_representative_events!==34||d.derived_counts?.highest_priority_gap_volume!=="VOL-06")e.push("computed-metrics");
 for(const k of ["can_ship","main_modified","existing_513_modified","ai_studio_modified","canonical_overviews_modified","new_deep_collation_started","user_approved","historian_review_complete","source_rights_review_complete"])if(d.release?.[k]!==false)e.push("release:"+k);
 if((md.match(/^### 우선순위 /gm)||[]).length!==5||!md.includes("VOL-06")||!md.includes("34건")||!md.includes("can_ship=false"))e.push("report");
 return e;
};
const mutations=[["fake-release",z=>z.d.release.can_ship=true],
["edit-main",z=>z.d.release.main_modified=true],
["edit-existing",z=>z.d.release.existing_513_modified=true],
["fake-approval",z=>z.d.release.user_approved=true],
["wrong-baseline-total",z=>z.d.derived_counts.total_baseline_representative_events=35],
["missing-volume",z=>z.d.baseline.pop()],
["duplicate-volume",z=>z.d.baseline[1].id="VOL-01"],
["false-SHA",z=>z.d.baseline[0].canonical_blob_sha="bad"],
["false-vol08-event",z=>z.d.baseline[7].baseline_measured.representative_events=2],
["false-three-expanded",z=>z.d.derived_counts.macro_expanded_volumes=5],
["missing-macro",z=>z.d.macro_layers.pop()],
["wrong-macro-SHA",z=>z.d.macro_layers[0].sha="bad"],
["wrong-first-priority",z=>z.d.priority_queue[0].task="VOL-08"],
["missing-priority",z=>z.d.priority_queue.pop()],
["invalid-cross-volume",z=>z.d.cross_volume_links[0].to="VOL-00"],
["report-missing-priority",z=>z.md=z.md.replace("### 우선순위 1","## 우선순위 1")],
["report-false-release",z=>z.md=z.md.replaceAll("can_ship=false","can_ship=true")]];
const d=JSON.parse(readFileSync("research/data/V4_11_EIGHT_VOLUME_L0_COVERAGE_GAP_PRIORITY_AUDIT_DRAFT.json","utf8"));
const md=readFileSync("research/notes/V4_11_EIGHT_VOLUME_L0_COVERAGE_GAPS_AND_RECOMMENDED_ORDER_KO.md","utf8");
const errors=validate(d,md);if(errors.length){console.error("V411 FAIL",errors);process.exit(1)}
console.log("V411 PASS: 8 volumes, 5 macro layers, 34 representative baseline events; next VOL-06");
if(process.argv.includes("--self-test")){let n=0;for(const [name,fn] of mutations){const z={d:JSON.parse(JSON.stringify(d)),md};fn(z);if(!validate(z.d,z.md).length){console.error("V411 mutation missed",name);process.exit(1)}n++;}console.log("V411 PASS "+n+" negative mutations");}
