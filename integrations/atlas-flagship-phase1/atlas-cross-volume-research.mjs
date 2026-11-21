import {validateAtlasReviewBundle} from "./atlas-review-bundle-contract.mjs";
const isText=x=>typeof x==="string"&&x.trim().length>0;
const unique=items=>new Set(items).size===items.length;
const allGates=["canShip","canMergeMain","canImportAIStudio","expertApproved","readerValidated","rightsApproved","hostAccessVerified"];
/**
 * Reuses V4.75 review schema across unrelated historical subjects and event counts.
 * Validates the actual data, including unapproved source limitations and links,
 * before exposing it to a RESEARCH-ONLY reader. It is NOT server authorization.
 */
export function buildAtlasCrossVolumeResearch(bundles,routeRegistry){
 const errors=[],bad=s=>errors.push(s);
 if(!Array.isArray(bundles)||bundles.length<2)return {ok:false,errors:["Need two independently sourced review bundles"],volumes:[],links:[]};
 const ids=bundles.map(b=>b?.identity?.volumeId);
 if(!unique(ids)||ids.some(x=>!isText(x)))bad("duplicate or missing volume IDs");
 for(const b of bundles){
  const verdict=validateAtlasReviewBundle(b);
  if(!verdict.valid)bad("Invalid "+(b?.identity?.volumeId||"?")+": "+verdict.errors.join("; "));
 }
 if(routeRegistry?.schema!=="ATLAS_V477_CROSS_VOLUME_READING_LINKS_V1"||routeRegistry?.state!=="RESEARCH_ONLY")bad("wrong route schema/stage");
 for(const field of allGates){if(routeRegistry?.releaseGate?.[field]!==false)bad("route release gate not closed: "+field)}
 if(routeRegistry?.actualReaderParticipants!==0||routeRegistry?.actualExpertApprovals!==0||routeRegistry?.operatingAppModified!==false||routeRegistry?.mainModified!==false)bad("invented approval or deployment");
 if(!Array.isArray(routeRegistry?.visualOrder)||!unique(routeRegistry.visualOrder)||routeRegistry.visualOrder.length!==bundles.length||
    routeRegistry.visualOrder.some(id=>!ids.includes(id)))bad("volume ordering invalid");
 const routes=Array.isArray(routeRegistry?.editorialComparisons)?routeRegistry.editorialComparisons:[];
 if(!routes.length||!unique(routes.map(x=>x.id)))bad("missing or duplicate cross-volume reading routes");
 for(const route of routes){
  if(!isText(route?.id)||!isText(route?.title)||!isText(route?.invitation)||!isText(route?.caution)||
   route?.interpretationStatus!=="UNREVIEWED_COMPARATIVE_EDITORIAL_LINK"||route?.expertApproved!==false)bad("unreviewed interpretation not marked: "+route?.id);
  const ends=[route?.from,route?.to];
  if(!isText(ends[0]?.volumeId)||!isText(ends[1]?.volumeId)||ends[0].volumeId===ends[1].volumeId)bad("cross-volume link must change volume: "+route?.id);
  for(const edge of ends){
   const volume=bundles.find(v=>v?.identity?.volumeId===edge?.volumeId);
   const event=volume?.timeline?.find(x=>x.id===edge?.eventId);
   if(!event){bad("unknown event: "+route?.id);continue}
   if(!Array.isArray(edge.sourceIds)||!edge.sourceIds.length||!unique(edge.sourceIds))bad("missing route citations: "+route?.id);
   else if(edge.sourceIds.some(id=>!event.sourceRefs.includes(id)||!volume.sources.some(s=>s.id===id&&s.eventIds.includes(event.id))))bad("route citation not present on event: "+route?.id);
  }
 }
 if(errors.length)return {ok:false,errors,volumes:[],links:[]};
 return {
  ok:true,errors:[],
  volumes:routeRegistry.visualOrder.map(id=>bundles.find(v=>v.identity.volumeId===id)),
  links:routes,
  rights:{publicResearchOnly:true,serverAuthenticationImplemented:false,canShip:false}
 };
}
export function getAtlasResearchEvent(library,volumeId,eventId){
 const volume=library?.volumes?.find(x=>x.identity.volumeId===volumeId);
 const event=volume?.timeline?.find(x=>x.id===eventId);
 return event?{volume,event}:null;
}
