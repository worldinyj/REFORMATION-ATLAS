#!/usr/bin/env node
/**** V4.10 world Christianity macro source/chronology/regional integrity validator. ****/
import {readFileSync} from "node:fs";
const validate=function validate(d,story,note){
const errs=[],arr=d.macro_arcs||[],reg=d.regional_routes||[],e=d.turning_points||[],people=d.actors||[],qs=d.comparative_questions||[],src=d.sources||[],edges=d.connections_to_V409||[];
const a=new Set(arr.map(x=>x.id)),r=new Set(reg.map(x=>x.id)),s=new Set(src.map(x=>x.id)),p=new Set(people.map(x=>x.id));
if(d.version!=="V4.10"||d.status!=="L0_WORLD_CHRISTIANITY_KOREA_DRAFT"||d.parent_branch!=="research/atlas-v409-catholic-reform-conflict-coexistence-l0"||d.level!=="L0")errs.push("meta");
if(arr.length!==9||a.size!==9||reg.length!==13||r.size!==13||e.length!==26||people.length!==17||p.size!==17||qs.length!==8||src.length!==32||s.size!==32||edges.length!==3)errs.push("counts");
for(const z of arr)if(z.source_ids.some(x=>!s.has(x))||z.region_ids.some(x=>!r.has(x)))errs.push("arc-reference");
for(const z of e)if(!a.has(z.arc_id)||!r.has(z.region_id)||z.source_ids.some(x=>!s.has(x))||!z.date_label||z.year_end!==null&&z.year_end<z.year_start)errs.push("milestone-reference");
for(const x of reg)if(x.arc_ids.some(y=>!a.has(y)))errs.push("region-arc");
for(const x of people)if(!a.has(x.arc_id)||!r.has(x.region_id)||!["COLLECTIVE","PERSON"].includes(x.type)||x.full_biography_verified!==false)errs.push("actor-grade");
for(const q of qs)if(q.arc_ids.some(x=>!a.has(x)))errs.push("comparison-ref");
if(src.some(x=>x.original_manuscript_read!==false||x.paid_chapter_full_text_read!==false||x.images_reproduced!==false))errs.push("license-source-grade");
const wcc=e.find(x=>x.title.includes("세계교회협의회 창립")),reg13=reg.find(x=>x.id==="RG410-13");
if(!wcc||wcc.region_id!=="RG410-13"||!reg13||reg13.continent!=="TRANSREGIONAL")errs.push("WCC-geography");
const inscription=e.find(x=>x.title.includes("635년")||x.date_label.includes("비문의 회고"));
if(!inscription||inscription.precision!=="retrospective_inscription_claim")errs.push("inscription-635");
if(!e.some(x=>x.year_start===781)||!e.some(x=>x.year_start===1784)||!e.some(x=>x.year_start===1882)||!e.some(x=>x.year_start===1887)||!e.some(x=>x.year_start===1919))errs.push("time-foundations");
if(people.find(x=>x.id==="A410-P17")?.type!=="COLLECTIVE")errs.push("group-not-person");
if(!edges.every(x=>a.has(x.v410_arc)&&/^A409-0[1-6]$/.test(x.v409_arc)))errs.push("V409-links");
const pub=d.publication||{};
for(const k of ["can_ship","main_modified","existing_513_modified","AI_Studio_modified","existing_VOL07_v01_modified","existing_L1_or_L2_modified","historic_facsimile_images_copied","paid_full_text_republished","regional_population_numbers_invented","historian_approved","rights_approved"])if(pub[k]!==false)errs.push("publication-"+k);
if((story.match(/^## [1-9]\./gm)||[]).length!==9||(story.match(/^### 질문 /gm)||[]).length!==8||!story.includes("635년")||!story.includes("1882년")||!story.includes("1907년")||!story.includes("1919년")||!story.includes("can_ship=false"))errs.push("reader");
if(!note.includes("RG410-13")||!note.includes("COLLECTIVE")||!note.includes("V4.11")||!note.includes("can_ship=false"))errs.push("editorial");
return errs;
};
const mutations=[["ship",x=>x.d.publication.can_ship=true],
["main",x=>x.d.publication.main_modified=true],
["513",x=>x.d.publication.existing_513_modified=true],
["drop-arc",x=>x.d.macro_arcs.pop()],
["drop-region",x=>x.d.regional_routes.pop()],
["drop-timeline",x=>x.d.turning_points.pop()],
["drop-person",x=>x.d.actors.pop()],
["source-dangling",x=>x.d.macro_arcs[0].source_ids=["BAD"]],
["region-dangling",x=>x.d.macro_arcs[0].region_ids=["BAD"]],
["actor-dangling",x=>x.d.actors[0].region_id="BAD"],
["question-dangling",x=>x.d.comparative_questions[0].arc_ids=["BAD"]],
["inscription-chronology",x=>x.d.turning_points.find(e=>e.precision==="retrospective_inscription_claim").precision="year"],
["inscription-lost",x=>x.d.turning_points.find(e=>e.year_start===781).year_start=780],
["Korean-1882-lost",x=>x.d.turning_points.find(e=>e.year_start===1882).year_start=1883],
["WCC-korean-false",x=>x.d.turning_points.find(e=>e.title.includes("세계교회협의회 창립")).region_id="RG410-12"],
["WCC-regional-false",x=>x.d.regional_routes.find(e=>e.id==="RG410-13").continent="KOREA"],
["collective-person",x=>x.d.actors.find(e=>e.id==="A410-P17").type="PERSON"],
["fake-biography",x=>x.d.actors[0].full_biography_verified=true],
["fake-fulltext",x=>x.d.sources[0].paid_chapter_full_text_read=true],
["fake-image",x=>x.d.sources[0].images_reproduced=true],
["false-mapping",x=>x.d.publication.regional_population_numbers_invented=true],
["v409-link-broken",x=>x.d.connections_to_V409[0].v410_arc="BAD"],
["erase-9",x=>x.story=x.story.replace("## 9.","## Ninth.")],
["erase-comparisons",x=>x.story=x.story.replace("### 질문 1.","#### 질문 1.")],
["erase-1882",x=>x.story=x.story.replaceAll("1882년","early translations")],
["note-wrong-WCC",x=>x.note=x.note.replaceAll("RG410-13","RG410-12")],
["note-released",x=>x.note=x.note.replaceAll("can_ship=false","can_ship=true")]];
const d=JSON.parse(readFileSync("research/data/V4_10_WORLD_CHRISTIANITY_KOREA_REGIONAL_AGENCY_L0_DRAFT.json","utf8"));
const story=readFileSync("docs/01_CONTENT/OVERVIEW/V410_VOL07_WORLD_CHRISTIANITY_KOREA_MASTER_KO.md","utf8");
const note=readFileSync("research/notes/V4_10_VOL07_WORLD_CHRISTIANITY_NAVIGATION_RELEASE_GATES_KO.md","utf8");
const errors=validate(d,story,note);if(errors.length){console.error("V410 FAIL",errors);process.exit(1)}
console.log("V410 PASS: 9 arcs, 13 routes, 26 milestones, Korean origins and 1948 WCC lane");
if(process.argv.includes("--self-test")){let n=0;for(const [name,fn] of mutations){const q={d:JSON.parse(JSON.stringify(d)),story,note};fn(q);if(!validate(q.d,q.story,q.note).length){console.error("V410 missed",name);process.exit(1)}n++;}console.log("V410 PASS "+n+" negative mutations");}
