/**
 * REFORMATION ATLAS V4.30 — L0 private-stage, read-only content bridge.
 *
 * Input: V4.29 validated import JSON object, already loaded by the host app.
 * Output: immutable, participant-safe content entities and logical navigation.
 * No fetch, no network, no storage, no global state or app deployment.
 * Host access checks are declared by the caller, never implemented here.
 */
export const CONTRACT_VERSION = "V4.30";
const VOLUME_IDS = Object.freeze(Array.from({length:8},(_,i)=>"VOL-"+String(i+1).padStart(2,"0")));
const THEME_IDS = Object.freeze(Array.from({length:6},(_,i)=>"T415-"+String(i+1).padStart(2,"0")));
const CHAPTER_IDS = Object.freeze(Array.from({length:6},(_,i)=>"INTRO-"+(i+1)));
const LABELS = Object.freeze({
  CORE_CASE:"핵심 사례",
  CONTEXT_BRIDGE:"맥락 연결",
  LIMITED_CONTEXT_NOT_DOCTRINE:"제한된 배경"
});
const READER_LEAK = /\b(?:C417-\d+|Q419-\d+|SRC421-\d+)\b|정답표/;
const MEDIA_EMBED = /!\[[^\]]*\]\([^)]+\)/;
function fail(reason){throw new Error("ATLAS_V430_PRIVATE_STAGING_REJECTED: "+reason);}
function requireThat(value,reason){if(!value)fail(reason);}
function isText(x){return typeof x==="string" && x.trim().length>0;}
function isRecord(x){return x!==null&&typeof x==="object"&&!Array.isArray(x);}
function freezeDeep(x){
  if(x&&typeof x==="object"&&!Object.isFrozen(x)){
    for(const value of Object.values(x))freezeDeep(value);
    Object.freeze(x);
  }
  return x;
}
function safeBody(value,label){
  requireThat(isText(value),label+" is missing");
  requireThat(!READER_LEAK.test(value),label+" contains editor claim/scoring identifiers");
  requireThat(!MEDIA_EMBED.test(value),label+" contains embedded images not rights-cleared");
  requireThat(!/<(?:script|iframe|object|embed|svg|img)\b/i.test(value),label+" contains active HTML");
  return value;
}
function assertOrdered(list,expected,key,label){
  requireThat(Array.isArray(list)&&list.length===expected.length,label+" count mismatch");
  const seen=new Set();
  list.forEach((x,i)=>{
    requireThat(isRecord(x)&&x[key]===expected[i],label+" order/id mismatch at "+i);
    requireThat(!seen.has(x[key]),label+" duplicate id");seen.add(x[key]);
  });
}
function requirePrivateState(input,host){
  requireThat(isRecord(host)&&host.environment==="PRIVATE_STAGING"&&host.accessControlDeclared===true,
    "caller must declare a restricted PRIVATE_STAGING environment; this flag is not an authentication mechanism");
  requireThat(isRecord(input),"invalid import object");
  requireThat(input.schema==="REFORMATION_ATLAS_L0_STAGING_IMPORT_V1","unsupported import schema");
  requireThat(input.packageVersion==="V4.29"&&input.usageScope==="PRIVATE_AI_STUDIO_STAGING_ONLY","wrong release scope");
  requireThat(input.publicationState==="BLOCKED","publication must remain blocked");
  const p=input.privacyAndRights;
  requireThat(isRecord(p)&&p.canShip===false&&p.allowsPublicIndexing===false&&
    p.allowsPublicPublishing===false&&p.allowsMainMerge===false&&
    p.requiresLoginOrPrivateAccess===true&&p.collectsReaderResponses===false,
    "unsafe rights/privacy gate");
  const a=input.appContract;
  requireThat(isRecord(a)&&a.routeTargetsAreIdsNotURLs===true&&
    a.mustHideEditorScoringKeys===true&&a.accessControlEnforcedByHostAppNotByJson===true&&
    a.defaultShowEditorMetadata===false&&a.mustNotFetchExternalImages===true&&
    a.adminReleaseGate==="BLOCKED_FOR_PUBLICATION","unsafe consumer contract");
  requireThat(input.integrationChecks?.readyForPublicShip===false&&
    input.integrationChecks?.realAiStudioStagingTestCompleted===false&&
    input.integrationChecks?.realHistorianReviewCompleted===false&&
    input.integrationChecks?.realFiveReaderPilotCompleted===false&&
    input.integrationChecks?.realRightsClearanceCompleted===false,
    "unsupported claim of test/signoff completion");
  requireThat(isRecord(input.provenance)&&input.provenance.canonicalContent==="V4.23"&&
    /^[a-f0-9]{40}$/.test(input.provenance.sourceGitBlobSha),
    "missing frozen content provenance");
  requireThat(!Object.hasOwn(input,"editor_only"),"editor-only registry embedded in reader package");
}
export function createAtlasL0ReadOnlyBridge(packageObject, hostDeclaration){
  // JSON round-trip strips prototypes and shared references from untrusted host input.
  // Reject non-JSON inputs up front and never mutate the caller's original object.
  requirePrivateState(packageObject,hostDeclaration);
  let input;
  try{input=JSON.parse(JSON.stringify(packageObject));}
  catch(e){fail("input must be serializable JSON");}
  assertOrdered(input.volumes,VOLUME_IDS,"id","volumes");
  assertOrdered(input.themes,THEME_IDS,"id","themes");
  assertOrdered(input.reader?.chapters,CHAPTER_IDS,"id","reader chapters");
  requireThat(input.reader?.readingTimeMeasured===false && input.reader?.readingTimeTargetMinutes===10,
    "reading time must remain an unmeasured goal");
  requireThat(input.reader?.id==="INTRO-V421"&&isText(input.reader?.title),
    "reader identity missing");
  const volumes=new Map();
  for(const v of input.volumes){
    requireThat(v.kind===(v.id==="VOL-08"?"THEMATIC_INDEX":"CHRONOLOGICAL_VOLUME"),
      "VOL-08 must not appear as a chronological eighth period");
    requireThat(isText(v.title)&&isText(v.leadQuestion)&&isText(v.description),v.id+" metadata missing");
    safeBody(v.bodyMarkdown,v.id);
    requireThat(v.editorialState==="NOT_SIGNED_OFF",v.id+" is not signed off");
    requireThat(Array.isArray(v.relatedThemes)&&v.relatedThemes.length===(v.id==="VOL-08"?0:6),
      v.id+" invalid reverse navigation");
    if(v.id!=="VOL-08"){
      requireThat(v.relatedThemes.every((x,i)=>x.id===THEME_IDS[i]&&x.kind==="THEME"),
        v.id+" theme reverse-link mismatch");
    }
    volumes.set(v.id,freezeDeep({
      kind:"VOLUME",id:v.id,order:v.order,title:v.title,period:v.period,
      leadQuestion:v.leadQuestion,description:v.description,bodyMarkdown:v.bodyMarkdown,
      isThematicArchive:v.id==="VOL-08",
      relatedThemeIds:v.relatedThemes.map(x=>x.id)
    }));
  }
  const themes=new Map(), allLinks=new Set();
  for(const theme of input.themes){
    requireThat(isText(theme.title)&&isText(theme.leadQuestion),theme.id+" metadata missing");
    safeBody(theme.bodyMarkdown,theme.id);
    requireThat(Array.isArray(theme.compareLinks)&&theme.compareLinks.length===7,
      theme.id+" must link to seven historical volumes");
    const links=theme.compareLinks.map((link,i)=>{
      const target=link?.target;
      requireThat(isRecord(target)&&target.kind==="VOLUME"&&target.id===VOLUME_IDS[i]&&target.id!=="VOL-08",
        theme.id+" invalid target");
      requireThat(isText(link.title)&&LABELS[link.connectionKind]===link.connectionLabel,
        theme.id+" invalid anchor label");
      const key=theme.id+"/"+target.id;
      requireThat(!allLinks.has(key),key+" duplicated");
      allLinks.add(key);
      requireThat(volumes.has(target.id),key+" missing volume");
      return {targetKind:"VOLUME",targetId:target.id,title:link.title,
        relation:link.connectionKind,relationLabel:link.connectionLabel};
    });
    themes.set(theme.id,freezeDeep({
      kind:"THEME",id:theme.id,order:theme.order,title:theme.title,
      leadQuestion:theme.leadQuestion,bodyMarkdown:theme.bodyMarkdown,links
    }));
  }
  requireThat(allLinks.size===42,"expected 42 theme-to-volume links");
  const chapters=new Map();
  for(const [i,c] of input.reader.chapters.entries()){
    requireThat(isText(c.title)&&Number(c.order)===i+1,"chapter metadata malformed");
    safeBody(c.bodyMarkdown,c.id);
    chapters.set(c.id,freezeDeep({
      kind:"CHAPTER",id:c.id,order:i+1,title:c.title,bodyMarkdown:c.bodyMarkdown
    }));
  }
  safeBody(input.reader.prefaceMarkdown,"preface");
  const catalog=freezeDeep({
    volumes:VOLUME_IDS.map(id=>{
      const v=volumes.get(id);return {id,kind:v.kind,title:v.title,period:v.period,description:v.description,isThematicArchive:v.isThematicArchive};
    }),
    themes:THEME_IDS.map(id=>{const t=themes.get(id);return {id,title:t.title,leadQuestion:t.leadQuestion};}),
    chapters:CHAPTER_IDS.map(id=>{const c=chapters.get(id);return {id,title:c.title,order:c.order};})
  });
  const readerIntro=freezeDeep({
    id:"INTRO-V421",title:input.reader.title,readingTimeTargetMinutes:10,
    readingTimeMeasured:false,prefaceMarkdown:input.reader.prefaceMarkdown
  });
  const meta=freezeDeep({
    contractVersion:CONTRACT_VERSION,
    contentVersion:"V4.23",
    importVersion:"V4.29",
    sourceGitBlobSha:input.provenance.sourceGitBlobSha,
    runtimeMode:"PRIVATE_STAGING_ONLY",
    canPublish:false,
    canMergeMain:false,
    mayCollectResponses:false,
    hostAccessControlNotImplementedByAdapter:true,
    counts:{volumes:volumes.size,themes:themes.size,chapters:chapters.size,themeToVolumeLinks:allLinks.size}
  });
  function resolve(target){
    if(!isRecord(target)||!isText(target.kind)||!isText(target.id))return null;
    if(target.kind==="VOLUME")return volumes.get(target.id)??null;
    if(target.kind==="THEME")return themes.get(target.id)??null;
    if(target.kind==="CHAPTER")return chapters.get(target.id)??null;
    return null;
  }
  const searchEntries=[
    ...VOLUME_IDS.map(id=>volumes.get(id)),
    ...THEME_IDS.map(id=>themes.get(id)),
    ...CHAPTER_IDS.map(id=>chapters.get(id))
  ];
  function search(query,{limit=20}={}){
    if(typeof query!=="string"||!query.trim())return freezeDeep([]);
    requireThat(Number.isInteger(limit)&&limit>=1&&limit<=20,"invalid search limit");
    const q=query.trim().toLocaleLowerCase("ko");
    const results=[];
    for(const x of searchEntries){
      const full=[x.title,x.description??"",x.leadQuestion??"",x.bodyMarkdown].join("\n");
      const lower=full.toLocaleLowerCase("ko");
      const found=lower.indexOf(q);
      if(found<0)continue;
      const start=Math.max(0,found-44),end=Math.min(full.length,found+q.length+64);
      results.push(freezeDeep({
        kind:x.kind,id:x.id,title:x.title,excerpt:full.slice(start,end).replace(/[#*_\x60]/g," ").replace(/\s+/g," ").trim(),
        navigation:{kind:x.kind,id:x.id}
      }));
      if(results.length===limit)break;
    }
    return freezeDeep(results);
  }
  return freezeDeep({
    ...meta,
    catalog,
    readerIntro,
    getVolume(id){return volumes.get(id)??null;},
    getTheme(id){return themes.get(id)??null;},
    getChapter(id){return chapters.get(id)??null;},
    resolve,
    search
  });
}
