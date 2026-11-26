export function createResearchAdapter({preview,crosswalk,enabled=false,hostNamespace=""}={}){
 const closed=()=>null;
 const disabled=(reason)=>Object.freeze({status:"DISABLED",reason,getSupplement:closed,listNewPeople:()=>[]});
 if(enabled!==true||hostNamespace!=="ATLAS_OVERVIEW_V01")return disabled("Explicit review mode and matching host namespace required");
 if(preview?.mode!=="research_preview_only"||crosswalk?.host_namespace!==hostNamespace||[preview?.can_ship,preview?.can_merge_main,preview?.can_import_ai_studio,crosswalk?.can_ship,crosswalk?.can_import_ai_studio].some(v=>v!==false))return disabled("Research release guard failed");
 const idx=(items,key="id")=>new Map(items.map(x=>[x[key],x]));
 const maps={chapter_ids:idx(preview.chapters),case_ids:idx(preview.cases,"case_id"),person_ids:idx(preview.people),theology_ids:idx(preview.theology.units),global_ids:idx(preview.global_units),asset_ids:idx(preview.assets)};
 const records=idx(crosswalk.records,"legacy_id");
 if(records.size!==crosswalk.records.length||Object.entries(maps).some(([k,m])=>crosswalk.records.some(r=>!Array.isArray(r[k])||r[k].some(id=>!m.has(id)))))return disabled("Crosswalk integrity failed");
 const clone=x=>JSON.parse(JSON.stringify(x));
 function getSupplement(kind,hostRecord){
   if(!hostRecord||typeof hostRecord.id!=="string")return null;
   const r=records.get(hostRecord.id),label=["person","place"].includes(kind)?hostRecord.name_ko:hostRecord.title;
   if(!r||r.kind!==kind||label!==r.legacy_label||r.relation==="no_curated_match")return null;
   const resolved=Object.fromEntries(Object.entries(maps).map(([k,m])=>[k.replace(/_ids$/,"s"),r[k].map(id=>m.get(id))]));
   return clone({host_id:r.legacy_id,relation:r.relation,notice:"연구 검토용 추가 읽기 · 기존 개요를 대체하지 않음 · 전문가 검토 미완료",...resolved,can_ship:false,can_import_ai_studio:false});
 }
 function listNewPeople(){return clone(crosswalk.unmerged_people);}
 return Object.freeze({status:"REVIEW_ADAPTER_READY",getSupplement,listNewPeople});
}
