#!/usr/bin/env node
/** REFORMATION-ATLAS V4.12 L0 history and source integrity, read only. */
import {readFileSync} from "node:fs";
const gate=function gate(d,story,note,v409,v410){
const e=[],ss=d.sources||[],aa=d.arcs||[],rr=d.regional_routes||[],tt=d.turning_points||[],pp=d.actors||[],qq=d.comparative_questions||[],x9=d.links_to_V409||[],x10=d.links_to_V410||[];
const S=new Set(ss.map(z=>z.id)),A=new Set(aa.map(z=>z.id)),R=new Set(rr.map(z=>z.id)),P=new Set(pp.map(z=>z.id)),T=new Set(tt.map(z=>z.id));
const older9=new Set(v409.historical_arcs.map(z=>z.id)),older10=new Set(v410.macro_arcs.map(z=>z.id));
if(d.version!=="V4.12"||d.chapter!=="VOL-06"||d.level!=="L0"||d.status!=="L0_PIETISM_REVIVAL_WORLD_MISSIONS_DRAFT"||d.parent_branch!=="research/atlas-v411-eight-volume-l0-coverage-gaps-and-priorities")e.push("metadata");
if(d.baseline_source?.sha!=="0bc11f8771783de94afebc8338e10042836eba50"||d.baseline_source?.unchanged!==true)e.push("baseline");
if(ss.length!==26||S.size!==26||ss.some(z=>!z.url?.startsWith("https://")||z.source_url_verified!==true||z.full_paid_book_read!==false||z.image_reproduced!==false))e.push("sources");
if(aa.length!==8||A.size!==8||aa.some(z=>!z.story||!z.source_ids?.length||z.source_ids.some(y=>!S.has(y))||z.region_ids.some(y=>!R.has(y))))e.push("arcs");
if(rr.length!==12||R.size!==12||rr.some(z=>z.arc_ids.some(y=>!A.has(y))||z.historic_coordinates_verified!==false))e.push("regions");
if(tt.length!==28||T.size!==28||tt.some((z,i)=>(i>0&&tt[i-1].year_start>z.year_start)||!A.has(z.arc_id)||!R.has(z.region_id)||z.source_ids.some(y=>!S.has(y))||(z.year_end!==null&&z.year_end<z.year_start)||z.full_original_read!==false))e.push("milestones");
if(tt.some(z=>!aa.find(a=>a.id===z.arc_id)?.region_ids?.includes(z.region_id)))e.push("arc-region-membership");
if(pp.length!==17||P.size!==17||pp.some(z=>!A.has(z.arc_id)||!R.has(z.region_id)||z.complete_biography_verified!==false))e.push("actors");
if(pp.filter(z=>z.node_type==="COLLECTIVE").length!==2||pp.find(z=>z.id==="P412-16")?.region_id!=="R412-03"||pp.find(z=>z.id==="P412-17")?.region_id!=="R412-07")e.push("Tamil-Bengali");
if(qq.length!==8||qq.some(z=>z.arc_ids.some(y=>!A.has(y))))e.push("questions");
if(x9.length!==4||x9.some(z=>!A.has(z.from_arc)||!older9.has(z.to_arc))||x10.length!==6||x10.some(z=>!A.has(z.from_arc)||!older10.has(z.to_arc)))e.push("crosslinks");
if(tt.find(z=>z.id==="MS412-27")?.source_ids?.join(",")!=="S412-24"||tt.find(z=>z.id==="MS412-28")?.source_ids?.join(",")!=="S412-25,S412-27"||tt.find(z=>z.id==="MS412-10")?.source_ids?.join(",")!=="S412-26")e.push("specific-source-attribution");
if(d.quality_addendum?.Korean_1882_1887_source_corrected!==true||d.quality_addendum?.group_nodes_separated_by_language!==true||d.quality_addendum?.no_original_image_included!==true)e.push("source-fixes");
if(d.reader_timeline?.period_events_render_as_bands!==true||d.reader_timeline?.multi_region_acts_do_not_imply_one_way_diffusion!==true)e.push("date-displays");
for(const k of ["can_ship","main_modified","existing_513_modified","AI_Studio_modified","canonical_VOL06_modified","previous_macro_layers_modified","original_source_full_text_republished","source_images_reproduced","verified_historic_coordinates_invented","manual_approval","history_editor_review_complete"])if(d.publication?.[k]!==false)e.push("release:"+k);
if((story.match(/^### [1-8]\./gm)||[]).length!==8||(story.match(/^### 질문 /gm)||[]).length!==8||!story.includes("자레나 리")||!story.includes("웨일스")||!story.includes("1882년")||!story.includes("can_ship=false"))e.push("story");
if(!note.includes("V4.13")||!note.includes("COLLECTIVE")||!note.includes("can_ship=false")||!note.includes("R412-")||!note.includes("VOL-06"))e.push("note");
return e;
};
const mutations=[["publish",z=>z.d.publication.can_ship=true],
["main",z=>z.d.publication.main_modified=true],
["513",z=>z.d.publication.existing_513_modified=true],
["AI studio",z=>z.d.publication.AI_Studio_modified=true],
["modify base",z=>z.d.publication.canonical_VOL06_modified=true],
["bad base SHA",z=>z.d.baseline_source.sha="BAD"],
["remove arc",z=>z.d.arcs.pop()],
["bad arc source",z=>z.d.arcs[0].source_ids=["S_BAD"]],
["remove region",z=>z.d.regional_routes.pop()],
["bad region arc",z=>z.d.regional_routes[0].arc_ids=["A_BAD"]],
["remove event",z=>z.d.turning_points.pop()],
["unsorted timeline",z=>z.d.turning_points[1].year_start=1600],
["inverted date",z=>z.d.turning_points.find(x=>x.year_end!==null).year_end=1600],
["bad event source",z=>z.d.turning_points[0].source_ids=["S_BAD"]],
["event wrong region",z=>z.d.turning_points.find(x=>x.id==="MS412-13").region_id="R412-10"],
["drop actor",z=>z.d.actors.pop()],
["merge collaborator roles",z=>z.d.actors.find(x=>x.id==="P412-16").region_id="R412-07"],
["fake full bio",z=>z.d.actors[0].complete_biography_verified=true],
["drop question",z=>z.d.comparative_questions.pop()],
["bad V409 arc",z=>z.d.links_to_V409[0].to_arc="A409-99"],
["bad V410 arc",z=>z.d.links_to_V410[0].to_arc="A410-99"],
["1882 bad source",z=>z.d.turning_points.find(x=>x.id==="MS412-27").source_ids=["S412-12"]],
["1887 bad source",z=>z.d.turning_points.find(x=>x.id==="MS412-28").source_ids=["S412-24"]],
["Wesley wrong source",z=>z.d.turning_points.find(x=>x.id==="MS412-10").source_ids=["S412-01"]],
["paid book falsely read",z=>z.d.sources[0].full_paid_book_read=true],
["image illegally reproduced",z=>z.d.sources[0].image_reproduced=true],
["false geographic precision",z=>z.d.regional_routes[0].historic_coordinates_verified=true],
["fake GPS",z=>z.d.publication.verified_historic_coordinates_invented=true],
["reader chapter lost",z=>z.story=z.story.replace("### 1.","## 1.")],
["reader question lost",z=>z.story=z.story.replace("### 질문 1.","## 질문 1.")],
["erase Wales",z=>z.story=z.story.replaceAll("웨일스","영국")],
["note false ship",z=>z.note=z.note.replaceAll("can_ship=false","can_ship=true")],
["note groups erased",z=>z.note=z.note.replaceAll("COLLECTIVE","GROUP")]];
const d=JSON.parse(readFileSync("research/data/V4_12_VOL06_PIETISM_REVIVAL_WORLD_MISSIONS_L0_DRAFT.json","utf8"));
const story=readFileSync("docs/01_CONTENT/OVERVIEW/V412_VOL06_PIETISM_REVIVALS_GLOBAL_MISSIONS_MASTER_KO.md","utf8");
const note=readFileSync("research/notes/V4_12_VOL06_L0_NAVIGATION_SOURCE_TIERS_RELEASE_GATES_KO.md","utf8");
const v409=JSON.parse(readFileSync("research/data/V4_09_VOL05_CATHOLIC_REFORM_CONFLICT_COEXISTENCE_L0_DRAFT.json","utf8"));
const v410=JSON.parse(readFileSync("research/data/V4_10_WORLD_CHRISTIANITY_KOREA_REGIONAL_AGENCY_L0_DRAFT.json","utf8"));
const errors=gate(d,story,note,v409,v410);if(errors.length){console.error("V412 FAIL",errors);process.exit(1)}
console.log("V412 PASS 8 arcs, 12 regions, 28 events, 17 actors, 26 sources, 10 crosslinks");
if(process.argv.includes("--self-test")){let count=0;for(const [n,fn] of mutations){const z={d:JSON.parse(JSON.stringify(d)),story,note};fn(z);if(!gate(z.d,z.story,z.note,v409,v410).length){console.error("V412 MISSED",n);process.exit(1)}count++;}console.log("V412 PASS "+count+" negative mutations")}
