#!/usr/bin/env node
/** REFORMATION-ATLAS V4.09 L0 source, coverage and release audit. */
import {readFileSync} from "node:fs";
const gate=function gate(d,story,notes,old){
const e=[],s=d.sources||[],ar=d.historical_arcs||[],m=d.turning_points||[],ps=d.people||[],r=d.regional_theaters||[],c=d.compare_scenes||[],links=d.crosswalk_to_V408||[];
const S=new Set(s.map(x=>x.id)),A=new Set(ar.map(x=>x.id)),M=new Set(m.map(x=>x.id)),O=new Set(old.events.map(x=>x.id));
if(d.version!=="V4.09"||d.status!=="L0_CATHOLIC_REFORM_CONFLICT_DRAFT"||d.level!=="L0"||d.parent_branch!=="research/atlas-v408-europe-synchronous-timeline-relationship-atlas")e.push("meta");
if(d.retained_source?.blob!=="755bda113a2dfdc9d2e959eea5450d317ed595c4"||d.retained_source?.unchanged!==true)e.push("ancestor");
if(s.length!==20||S.size!==20||s.some(x=>!x.url?.startsWith("https://")||x.full_paid_text_read!==false||x.original_document_image_copied!==false))e.push("sources");
if(ar.length!==6||A.size!==6||ar.some(x=>x.source_ids.some(z=>!S.has(z))||!x.core_ko||x.questions?.length!==2))e.push("six-arcs");
if(m.length!==18||M.size!==18||m.some(x=>!A.has(x.arc_id)||x.source_ids.some(z=>!S.has(z))||x.year_start<1524||x.year_start>1648||(x.year_end!==null&&x.year_end<x.year_start)))e.push("18-milestones");
for(const term of ["트리엔트 공의회 제1","트리엔트 공의회 제2","트리엔트 공의회 제3","아우크스부르크 화의","베스트팔렌"])if(!m.some(x=>x.title.includes(term)))e.push("missing-"+term);
if(ps.length!==13||new Set(ps.map(x=>x.id)).size!==13||ps.some(x=>!A.has(x.arc_id)||x.name_ko.includes("·")))e.push("people");
if(r.length!==6||r.some(x=>x.source_ids.some(z=>!S.has(z))))e.push("theaters");
if(c.length!==6||c.some(x=>x.arc_ids.some(z=>!A.has(z))))e.push("scenes");
if(links.length!==8||new Set(links.map(x=>x.v408_event_id)).size!==8||links.some(x=>!M.has(x.v409_milestone_id)||!O.has(x.v408_event_id)))e.push("crosswalk");
for(const k of ["can_ship","main_modified","existing_513_modified","AI_Studio_modified","previous_V408_modified","modern_human_rights_anachronism_allowed","Catholic_Reform_reduced_to_reaction","female_agency_erased"])if(d.scope_safety?.[k]!==false)e.push("release-"+k);
if(d.editorial_qualification?.raw_primary_trent_minutes_read!==false||d.editorial_qualification?.raw_original_Westphalia_folio_read!==false||d.editorial_qualification?.some_sources_only_abstract_or_publisher_blurb!==true)e.push("research-grade");
if(!S.has("S409-19")||!d.provenance_corrections?.some(x=>x.scope==="1568 Torda"))e.push("Torda");
if((story.match(/^## [1-6]\./gm)||[]).length!==6||(story.match(/^### 질문 /gm)||[]).length!==6||!story.includes("1545~1547년, 1551~1552년, 1562~1563년")||!story.includes("1685년 칙령 철회")||!story.includes("정교회")||!story.includes("여성")||!story.includes("can_ship=false"))e.push("longform");
if(!notes.includes("네 가지")||!notes.includes("V4.08")||!notes.includes("V4.10")||!notes.includes("can_ship=false"))e.push("editorial");
return e;
};
const mutations=[["publication",x=>x.d.scope_safety.can_ship=true],
["main-change",x=>x.d.scope_safety.main_modified=true],
["513-change",x=>x.d.scope_safety.existing_513_modified=true],
["AI-studio-change",x=>x.d.scope_safety.AI_Studio_modified=true],
["lost-ancestor",x=>x.d.retained_source.blob="BAD"],
["drop-arc",x=>x.d.historical_arcs.pop()],
["wrong-arc-source",x=>x.d.historical_arcs[0].source_ids=["S000"]],
["drop-milestone",x=>x.d.turning_points.pop()],
["bad-range",x=>x.d.turning_points.find(y=>y.year_end!==null).year_end=1500],
["fake-source",x=>x.d.turning_points[0].source_ids=["S000"]],
["drop-person",x=>x.d.people.pop()],
["group-two-people",x=>x.d.people[12].name_ko="불링거·유트"],
["drop-theater",x=>x.d.regional_theaters.pop()],
["drop-scene",x=>x.d.compare_scenes.pop()],
["fake-source-access",x=>x.d.sources[0].full_paid_text_read=true],
["image-reuse",x=>x.d.sources[0].original_document_image_copied=true],
["source-lost",x=>x.d.sources=x.d.sources.filter(y=>y.id!=="S409-19")],
["crosswalk-bad",x=>x.d.crosswalk_to_V408[0].v408_event_id="E000"],
["crosswalk-lost",x=>x.d.crosswalk_to_V408.pop()],
["modern-rights-overclaim",x=>x.d.scope_safety.modern_human_rights_anachronism_allowed=true],
["no-female-agency",x=>x.d.scope_safety.female_agency_erased=true],
["counter-only",x=>x.d.scope_safety.Catholic_Reform_reduced_to_reaction=true],
["Trent-primary-pretend",x=>x.d.editorial_qualification.raw_primary_trent_minutes_read=true],
["Westphalia-original-pretend",x=>x.d.editorial_qualification.raw_original_Westphalia_folio_read=true],
["remove-sixth-section",x=>x.story=x.story.replace("## 6.","## SIX.")],
["erase-chronology",x=>x.story=x.story.replace("1545~1547년, 1551~1552년, 1562~1563년","연속 회의")],
["erase-1685",x=>x.story=x.story.replace("1685년 칙령 철회","후일 사건")],
["erase-Orthodox",x=>x.story=x.story.replaceAll("정교회","다른 종교")],
["bad-editor-note",x=>x.notes=x.notes.replaceAll("V4.08","V4.07")],
["false-editor-release",x=>x.notes=x.notes.replaceAll("can_ship=false","can_ship=true")]];
const d=JSON.parse(readFileSync("research/data/V4_09_VOL05_CATHOLIC_REFORM_CONFLICT_COEXISTENCE_L0_DRAFT.json","utf8"));
const story=readFileSync("docs/01_CONTENT/OVERVIEW/V409_VOL05_CATHOLIC_REFORM_CONFLICT_COEXISTENCE_MASTER_KO.md","utf8");
const notes=readFileSync("research/notes/V4_09_VOL05_OVERVIEW_READER_APP_LINKAGE_AND_NEXT_PRIORITIES_KO.md","utf8");
const old=JSON.parse(readFileSync("research/data/V4_08_EUROPE_SYNCHRONOUS_EVENTS_PEOPLE_RELATIONSHIPS_L0_DRAFT.json","utf8"));
const errors=gate(d,story,notes,old);if(errors.length){console.error("V409 FAIL",errors);process.exit(1)}
console.log("V409 PASS: 6 arcs, 18 milestones, 20 sources, 8 crosslinks and no-release gates");
if(process.argv.includes("--self-test")){let n=0;for(const [name,mut] of mutations){const x={d:JSON.parse(JSON.stringify(d)),story,notes};mut(x);if(!gate(x.d,x.story,x.notes,old).length){console.error("V409 MISSED",name);process.exit(1)}n++;}console.log("V409 PASS "+n+" negative mutations");}
