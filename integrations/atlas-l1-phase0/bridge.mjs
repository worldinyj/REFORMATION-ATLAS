/**
 * Reformation ATLAS — Phase 0 research-only L0/L1 compatibility adapter.
 * Pure ESM, no fetch/storage/DOM/React dependency.
 *
 * This is NOT access control. Its output includes research text. Never import
 * input JSON into a public bundle or deliver it without host authentication.
 * It neither publishes content nor connects to the real AI Studio app.
 */
export const ATLAS_RESEARCH_BRIDGE_VERSION = "PHASE0-L0L1-1";
const VOL_IDS = Object.freeze(Array.from({length:8},(_,i)=>"VOL-"+String(i+1).padStart(2,"0")));
const THEME_IDS = Object.freeze(Array.from({length:6},(_,i)=>"T415-"+String(i+1).padStart(2,"0")));
const INTRO_IDS = Object.freeze(Array.from({length:6},(_,i)=>"INTRO-"+(i+1)));
function fail(msg){throw Error("ATLAS_PHASE0_RESEARCH_BLOCKED: "+msg);}
function assert(ok,msg){if(!ok)fail(msg);}
function record(x){return x!==null&&typeof x==="object"&&!Array.isArray(x);}
function string(x){return typeof x==="string"&&x.trim().length>0;}
function sortedIds(items){return items.map(v=>v.id).sort().join("|");}
function deepFreeze(x){if(x&&typeof x==="object"&&!Object.isFrozen(x)){Object.values(x).forEach(deepFreeze);Object.freeze(x);}return x;}
function unique(xs){return new Set(xs).size===xs.length;}
function makeReadOnlyIndex(xs){return new Map(xs.map(x=>[x.id,deepFreeze(x)]));}
/**
 * Compose L0 research (V4.47), L1 research (V4.50) and frozen staging contract (V4.29)
 * into a research-only reader projection. Caller must secure the actual input delivery.
 * The explicit LOCAL_RESEARCH_PREVIEW mode cannot make a public site private.
 */
export function createAtlasResearchReadOnlyBridge(
 {frozenStagingPackage,researchOverview,researchIntermediate},
 {mode}={}
){
 assert(mode==="LOCAL_RESEARCH_PREVIEW","requires explicit local research preview mode");
 assert(record(frozenStagingPackage)&&record(researchOverview)&&record(researchIntermediate),"three source objects required");
 assert(frozenStagingPackage.publicationState==="BLOCKED"&&frozenStagingPackage.privacyAndRights?.canShip===false,
   "V429 staging package must remain blocked");
 assert(Array.isArray(frozenStagingPackage.volumes)&&Array.isArray(frozenStagingPackage.themes)&&Array.isArray(frozenStagingPackage.reader?.chapters),"invalid staging arrays");
 assert(Array.isArray(researchOverview.volumes)&&Array.isArray(researchIntermediate.volumes),"missing L0/L1 arrays");
 assert(sortedIds(frozenStagingPackage.volumes)===VOL_IDS.join("|"),"frozen eight volume IDs changed");
 assert(sortedIds(researchOverview.volumes)===VOL_IDS.join("|"),"research overview eight IDs changed");
 assert(sortedIds(researchIntermediate.volumes)===VOL_IDS.join("|"),"research L1 eight volume IDs changed");
 assert(sortedIds(frozenStagingPackage.themes)===THEME_IDS.join("|"),"six theme IDs changed");
 assert(sortedIds(frozenStagingPackage.reader.chapters)===INTRO_IDS.join("|"),"six intro IDs changed");
 const allLinks=frozenStagingPackage.themes.flatMap(x=>x.compareLinks||[]);
 assert(allLinks.length===42,"42 theme-volume links required");
 assert(allLinks.every(x=>x.target?.kind==="VOLUME"&&VOL_IDS.slice(0,7).includes(x.target?.id)),"theme targets invalid");
 const stagingIndex=new Map(frozenStagingPackage.volumes.map(v=>[v.id,v]));
 const overIndex=new Map(researchOverview.volumes.map(v=>[v.id,v]));
 const l1Index=new Map(researchIntermediate.volumes.map(v=>[v.id,v]));
 const volumes=[],chapters=[];
 for(const id of VOL_IDS){
  const prior=stagingIndex.get(id),ov=overIndex.get(id),item=l1Index.get(id);
  assert(item&&ov&&prior&&string(ov.bodyMarkdown)&&string(ov.title),"missing volume "+id);
  assert(item.chapters?.length===3,"exactly three L1 chapters per volume "+id);
  assert((id==="VOL-08") === (ov.kind==="THEMATIC_INDEX"),"VOL-08 must be the thematic archive");
  const chapterIds=[];
  for(const chapter of item.chapters){
   assert(string(chapter.id)&&string(chapter.title)&&string(chapter.bodyMarkdown)&&string(chapter.thesis),"invalid L1 chapter "+id);
   assert(Array.isArray(chapter.sourceUrls)&&chapter.sourceUrls.length>0&&chapter.sourceUrls.every(url=>typeof url==="string"&&url.startsWith("https://")),"unreviewed or missing citation field "+chapter.id);
   assert(chapter.canShip===false,"L1 chapter unexpectedly publishable "+chapter.id);
   assert(Array.isArray(chapter.crossLinks)&&chapter.crossLinks.every(x=>VOL_IDS.includes(x)),"invalid related volume "+chapter.id);
   chapterIds.push(chapter.id);
   chapters.push({kind:"L1_CHAPTER",id:chapter.id,volumeId:id,title:chapter.title,period:chapter.period,bodyMarkdown:chapter.bodyMarkdown,
      thesis:chapter.thesis,sourceUrls:[...chapter.sourceUrls],relatedVolumeIds:[...chapter.crossLinks],
      reviewCaution:chapter.reviewCaution??"",canShip:false});
  }
  assert(unique(chapterIds),"duplicate L1 chapter within "+id);
  volumes.push({kind:"VOLUME",id,title:ov.title,bodyMarkdown:ov.bodyMarkdown,stagingTitle:prior.title,
    introVersion:"V4.47_RESEARCH_L0",stagingVersion:"V4.29_FROZEN_L0",l1Version:"V4.50_RESEARCH_L1",
    stagingBodyIsSame:prior.bodyMarkdown===ov.bodyMarkdown,
    hasUnreviewedHistoricalClaims:true,
    chapterIds,canShip:false});
 }
 assert(unique(chapters.map(c=>c.id))&&chapters.length===24,"L1 chapters must be 24 globally unique");
 const themes=frozenStagingPackage.themes.map(t=>({kind:"THEME",id:t.id,title:t.title,bodyMarkdown:t.bodyMarkdown,
   links:t.compareLinks.map(x=>({volumeId:x.target.id,title:x.title,kind:x.connectionKind})),canShip:false}));
 const intros=frozenStagingPackage.reader.chapters.map(x=>({kind:"INTRO_CHAPTER",id:x.id,title:x.title,bodyMarkdown:x.bodyMarkdown,canShip:false}));
 const vIndex=makeReadOnlyIndex(volumes), cIndex=makeReadOnlyIndex(chapters),tIndex=makeReadOnlyIndex(themes),iIndex=makeReadOnlyIndex(intros);
 const frozenMismatch=volumes.filter(x=>!x.stagingBodyIsSame).map(x=>x.id);
 const meta=deepFreeze({bridgeVersion:ATLAS_RESEARCH_BRIDGE_VERSION,previewMode:"LOCAL_RESEARCH_PREVIEW",
   contentVersions:{staging:"V4.29",overview:"V4.47",intermediate:"V4.50"},
   volumeCount:8,intermediateChapterCount:24,themeCount:6,themeToHistoryLinks:42,introChapterCount:6,
   changedStagingOverviewIds:frozenMismatch,
   publicRepositoryMayExposePayload:true,
   hostAuthenticationImplemented:false,
   canShip:false,canMergeMain:false,canImportAIStudio:false});
 const searchable=[...volumes,...chapters,...themes];
 return Object.freeze({
  meta,
  catalog:deepFreeze(volumes.map(x=>({id:x.id,title:x.title,chapterIds:[...x.chapterIds],stagingBodyIsSame:x.stagingBodyIsSame}))),
  getVolume:id=>vIndex.get(id)??null,
  getChapter:id=>cIndex.get(id)??null,
  getTheme:id=>tIndex.get(id)??null,
  getIntroChapter:id=>iIndex.get(id)??null,
  resolve:route=>!record(route)||!string(route.id)?null:(
    route.kind==="VOLUME"?vIndex.get(route.id)??null:
    route.kind==="L1_CHAPTER"?cIndex.get(route.id)??null:
    route.kind==="THEME"?tIndex.get(route.id)??null:
    route.kind==="INTRO_CHAPTER"?iIndex.get(route.id)??null:null),
  search:(query,{limit=16}={})=>{
    if(!string(query))return Object.freeze([]);
    assert(Number.isInteger(limit)&&limit>=1&&limit<=24,"invalid search limit");
    const q=query.trim().toLocaleLowerCase("ko");
    const results=[];
    for(const x of searchable){
      const haystack=[x.title,x.bodyMarkdown,x.thesis??""].join("\n");
      const found=haystack.toLocaleLowerCase("ko").indexOf(q);
      if(found<0)continue;
      results.push(deepFreeze({kind:x.kind,id:x.id,title:x.title,volumeId:x.volumeId??(x.kind==="VOLUME"?x.id:null),
        excerpt:haystack.slice(Math.max(0,found-38),Math.min(haystack.length,found+q.length+55)).replace(/[\r\n]+/g," ")}));
      if(results.length===limit)break;
    }
    return Object.freeze(results);
  }
 });
}
