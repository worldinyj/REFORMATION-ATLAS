#!/usr/bin/env node
/** V4.08 European L0 chronology and relationship graph validator (read-only). */
import {readFileSync} from "node:fs";
const verify=function verify(d,story,spec){
const errors=[],ev=d.events||[],people=d.people||[],regions=d.region_coverage||[],lanes=d.regional_lanes||[],src=d.bibliography||[],scenes=d.comparative_scenes||[],layers=d.layers||[],themes=d.themes||[],edges=d.region_relationships||[],rel=d.people_event_relationships||[];
const IDs={event:new Set(ev.map(x=>x.id)),region:new Set(regions.map(x=>x.region_id)),person:new Set(people.map(x=>x.id)),source:new Set(src.map(x=>x.id)),theme:new Set(themes.map(x=>x.id)),edge:new Set(edges.map(x=>x.id))};
if(d.version!=="V4.08"||d.status!=="L0_SYNCHRONOUS_EUROPE_OVERVIEW_DRAFT"||d.scope?.V407_source_blob!=="994194691771c63816fdcfc031314bc13487fabb")errors.push("parent");
if(ev.length!==45||IDs.event.size!==45||ev.some((x,i)=>(i>0&&ev[i-1].year_start>x.year_start)||x.year_start<1415||x.year_start>1648||(x.year_end!==null&&x.year_end<x.year_start)))errors.push("event-count-time");
if(people.length!==24||IDs.person.size!==24||themes.length!==6||IDs.theme.size!==6)errors.push("people-themes");
if(regions.length!==11||IDs.region.size!==11||regions.some(x=>x.event_count!==ev.filter(e=>e.region_ids.includes(x.region_id)).length||x.event_count<2))errors.push("coverage");
for(const x of ev){if(!x.region_ids?.length||!x.source_ids?.length||x.region_ids.some(z=>!IDs.region.has(z))||x.source_ids.some(z=>!IDs.source.has(z))||x.theme_ids.some(z=>!IDs.theme.has(z))||x.actor_ids.some(z=>!IDs.person.has(z))||x.date_precision!==(x.year_end===null?"year":"period"))errors.push("event-ref:"+x.id)}
if(layers.length!==6||layers.some(x=>x.event_ids.length<3||x.event_ids.some(z=>!IDs.event.has(z))))errors.push("6eras");
if(scenes.length!==8||scenes.some(x=>x.spotlight_event_ids.length<4||x.spotlight_event_ids.some(z=>!IDs.event.has(z)||!x.all_synchronized_event_ids.includes(z))||x.region_ids.some(z=>!IDs.region.has(z))))errors.push("8scenes");
if(lanes.length!==11||lanes.some(x=>!IDs.region.has(x.region_id)||x.event_ids.some(z=>!IDs.event.has(z))||x.event_ids.length!==ev.filter(y=>y.region_ids.includes(x.region_id)).length||x.person_ids.some(z=>!IDs.person.has(z))||x.relationship_ids.some(z=>!IDs.edge.has(z))))errors.push("11lanes");
if(edges.length!==17||IDs.edge.size!==17||edges.some(x=>!IDs.region.has(x.from_region)||!IDs.region.has(x.to_region)||x.geo_route_verified!==false))errors.push("17links");
if(rel.length!==ev.reduce((t,e)=>t+e.actor_ids.length,0)||rel.some(x=>!IDs.event.has(x.event_id)||!IDs.person.has(x.actor_id)))errors.push("personlinks");
if(src.length!==14||IDs.source.size!==14||src.some(x=>x.full_text_reviewed!==false||x.source_reproduced!==false||!x.url?.startsWith("https://")))errors.push("14sources");
if(d.map_source_staging?.map_image_copied!==false||d.map_source_staging?.actual_historic_gps_coordinates_in_data!==false||d.map_source_staging?.independent_rights_review_required!==true)errors.push("map");
if(d.coverage_guards?.source_full_text_review_claims_prohibited!==true||d.coverage_guards?.human_release_gate!==true||d.reader_display_rules?.connection_edges_not_automatic_diffusion_causation!==true)errors.push("guards");
for(const k of ["can_ship","main_modified","essays_513_modified","ai_studio_modified","old_research_files_modified","external_images_copied","full_paid_book_copied","historian_reviewed","rights_approved"])if(d.publication?.[k]!==false)errors.push("publication:"+k);
if(!story.includes("여섯 시대의 연속 이야기")||(story.match(/^### 장면 /gm)||[]).length!==8||!story.includes("11개 지역을 한 장의 연표로 연결")||!story.includes("can_ship=false"))errors.push("narrative");
if(!spec.includes("기간형 사건")||!spec.includes("관계망 그래프")||!spec.includes("can_ship=false"))errors.push("UX");
return errors;
};
const mutations=[["event missing",x=>x.d.events.pop()],
["duplicate event ID",x=>x.d.events[1].id=x.d.events[0].id],
["bad year sequence",x=>x.d.events[1].year_start=1400],
["bad period end",x=>x.d.events.find(z=>z.year_end!==null).year_end=1410],
["event region invalid",x=>x.d.events[0].region_ids=["ER-99"]],
["event source invalid",x=>x.d.events[0].source_ids=["missing"]],
["event actor invalid",x=>x.d.events[1].actor_ids=["P999"]],
["wrong date precision",x=>x.d.events.find(z=>z.year_end!==null).date_precision="year"],
["missing region",x=>x.d.region_coverage.pop()],
["regional count false",x=>x.d.region_coverage[0].event_count=999],
["fewer theme categories",x=>x.d.themes.pop()],
["fewer people",x=>x.d.people.pop()],
["fewer layer",x=>x.d.layers.pop()],
["layer refs invalid",x=>x.d.layers[0].event_ids=["bad"]],
["fewer comparison scene",x=>x.d.comparative_scenes.pop()],
["wrong scene spotlight",x=>x.d.comparative_scenes[0].spotlight_event_ids=["bad"]],
["fake synchronized scene",x=>x.d.comparative_scenes[0].all_synchronized_event_ids=[]],
["invalid scene region",x=>x.d.comparative_scenes[0].region_ids=["ER-99"]],
["region lane missing",x=>x.d.regional_lanes.pop()],
["region lane event invalid",x=>x.d.regional_lanes[0].event_ids=["bad"]],
["region lane link invalid",x=>x.d.regional_lanes[0].relationship_ids=["bad"]],
["fabricated route",x=>x.d.region_relationships[0].geo_route_verified=true],
["edge invalid",x=>x.d.region_relationships[0].to_region="ER-X"],
["actor event link invalid",x=>x.d.people_event_relationships[0].event_id="E999"],
["sources overclaim",x=>x.d.bibliography[0].full_text_reviewed=true],
["source copied",x=>x.d.bibliography[1].source_reproduced=true],
["wrong bibliography",x=>x.d.bibliography[2].url=""],
["fake GIS",x=>x.d.map_source_staging.actual_historic_gps_coordinates_in_data=true],
["release",x=>x.d.publication.can_ship=true],
["main changed",x=>x.d.publication.main_modified=true],
["513 changed",x=>x.d.publication.essays_513_modified=true],
["parent blob wrong",x=>x.d.scope.V407_source_blob="bad"],
["link types no distinction",x=>x.d.reader_display_rules.connection_edges_not_automatic_diffusion_causation=false],
["narrative missing scene",x=>x.story=x.story.replace("### 장면 1","## 장면 1")],
["UX missing event type",x=>x.spec=x.spec.replaceAll("기간형 사건","기간 표시")],
["UX falsely released",x=>x.spec=x.spec.replaceAll("can_ship=false","can_ship=true")]];
const d=JSON.parse(readFileSync("research/data/V4_08_EUROPE_SYNCHRONOUS_EVENTS_PEOPLE_RELATIONSHIPS_L0_DRAFT.json","utf8"));
const story=readFileSync("docs/01_CONTENT/OVERVIEW/V408_EUROPE_SYNCHRONOUS_HISTORY_COMPARATIVE_GUIDE_KO.md","utf8");
const spec=readFileSync("research/notes/V4_08_SYNCHRONOUS_EUROPE_EXPLORER_APP_INTEGRATION_SPEC_KO.md","utf8");
const errors=verify(d,story,spec);if(errors.length){console.error("V408 FAILED",errors);process.exit(1)}
console.log("V408 PASS: 45 events, 11 regions, 8 scenes, 6 eras, 24 persons, source and no-release gates");
if(process.argv.includes("--self-test")){let ok=0;for(const [name,mut] of mutations){const x={d:JSON.parse(JSON.stringify(d)),story,spec};mut(x);if(!verify(x.d,x.story,x.spec).length){console.error("V408 missed",name);process.exit(1)}ok++;}console.log("V408 PASS "+ok+" fault-injection test cases")}
