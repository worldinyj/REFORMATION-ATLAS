import React,{useEffect,useMemo,useRef,useState} from "react";
import {createAtlasL0ReadOnlyBridge} from "../atlas-l0-v430/bridge.mjs";
import "./atlas-l0.css";

/* V4.31 isolated React candidate, NOT the real AI Studio app.
 * Host must authenticate access to component AND V4.29 payload server-side.
 * stagingGranted is not an authentication mechanism. No network or storage.
 */
const TABS=[
 {kind:"VOLUME_INDEX",label:"역사 8권",key:"volumes",itemKind:"VOLUME"},
 {kind:"THEME_INDEX",label:"비교 6주제",key:"themes",itemKind:"THEME"},
 {kind:"CHAPTER_INDEX",label:"입문 6장면",key:"chapters",itemKind:"CHAPTER"}
];
const LABELS={VOLUME:"역사권",THEME:"주제",CHAPTER:"입문 장면"};
const LISTS={VOLUME:"VOLUME_INDEX",THEME:"THEME_INDEX",CHAPTER:"CHAPTER_INDEX"};

/** No raw HTML, images or injected links; supports only the corpus Markdown subset. */
function inlineParts(input,key){
 const pieces=String(input).split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g).filter(Boolean);
 return pieces.map((part,i)=>{
   if(part.startsWith("**")&&part.endsWith("**"))return <strong key={key+"s"+i}>{part.slice(2,-2)}</strong>;
   if(part.startsWith("*")&&part.endsWith("*"))return <em key={key+"e"+i}>{part.slice(1,-1)}</em>;
   return <React.Fragment key={key+"t"+i}>{part}</React.Fragment>;
 });
}
export function AtlasL0SafeMarkdown({source}){
 const blocks=String(source??"").trim().split(/\n{2,}/).filter(Boolean);
 return <div className="atlas-l0-text">{blocks.map((raw,i)=>{
   const para=raw.trim();
   const heading=para.match(/^(#{1,4})[ \t]+([\s\S]+)$/);
   if(heading)return React.createElement("h"+Math.min(4,heading[1].length+1),{key:"h"+i},
     ...inlineParts(heading[2].replace(/\n/g," "),"h"+i));
   if(para.startsWith("> "))return <blockquote key={"q"+i}>{inlineParts(para.replace(/^> ?/gm,"").replace(/\n/g," "),"q"+i)}</blockquote>;
   return <p key={"p"+i}>{inlineParts(para.replace(/\n/g," "),"p"+i)}</p>;
 })}</div>;
}
export default function AtlasL0Panel({payload,stagingGranted=false,onNavigate}){
 const [stack,setStack]=useState([]);
 const [view,setView]=useState({kind:"VOLUME_INDEX"});
 const [search,setSearch]=useState("");
 const titleRef=useRef(null),firstRender=useRef(true);
 const bridge=useMemo(()=>{
   if(!stagingGranted)return {status:"BLOCKED",reason:"비공개 접근 확인 필요"};
   try{return {status:"READY",atlas:createAtlasL0ReadOnlyBridge(payload,{
     environment:"PRIVATE_STAGING",accessControlDeclared:true
   })};}catch(e){return {status:"BLOCKED",reason:String(e?.message??e)};}
 },[payload,stagingGranted]);
 useEffect(()=>{
   if(firstRender.current){firstRender.current=false;return;}
   if(view.kind!=="SEARCH")titleRef.current?.focus({preventScroll:true});
 },[view.kind,view.id]);
 function navigate(next){
   setStack(previous=>[...previous,view]);setView(next);setSearch("");
   if(typeof onNavigate==="function")onNavigate({kind:next.kind,id:next.id??null});
 }
 function tab(next){setStack([]);setView({kind:next});setSearch("");}
 function back(){
   if(stack.length){const last=stack[stack.length-1];setStack(s=>s.slice(0,-1));setView(last);}
   else setView({kind:LISTS[view.kind]??"VOLUME_INDEX"});
   setSearch("");
 }
 function searchChange(value){
   setSearch(value);
   setView(value.trim()?{kind:"SEARCH"}:{kind:"VOLUME_INDEX"});
   if(!value.trim())setStack([]);
 }
 if(bridge.status!=="READY")return <section className="atlas-l0-root" data-atlas-state="BLOCKED" aria-label="내부 검토 자료 접근 제한">
   <h2>콘텐츠 접근 제한</h2><p role="alert">{bridge.reason}</p>
   <p>클라이언트의 상태는 실제 서버 인증·접근제어를 대신하지 않습니다.</p>
 </section>;
 const atlas=bridge.atlas,activeTab=TABS.find(t=>t.kind===view.kind);
 const hits=view.kind==="SEARCH"?atlas.search(search,{limit:20}):[];
 const entity=!activeTab&&view.kind!=="SEARCH"?atlas.resolve(view):null;
 return <section className="atlas-l0-root" data-atlas-state="READY" aria-label="종교개혁 ATLAS L0 독해">
  <div className="atlas-l0-eyebrow">REFORMATION ATLAS · 세계 교회사 · 비공개 스테이징</div>
  <nav className="atlas-l0-tabs" aria-label="상위 역사 원고 탐색">
   {TABS.map(t=><button type="button" key={t.kind} data-testid={"tab-"+t.kind}
     aria-current={view.kind===t.kind?"page":undefined}
     onClick={()=>tab(t.kind)}>{t.label}</button>)}
  </nav>
  <label htmlFor="atlas-l0-search">전체 원고 검색</label>
  <input id="atlas-l0-search" type="search" autoComplete="off" value={search}
    placeholder="후스, 성찬, 한국, 번역…" onChange={e=>searchChange(e.target.value)}/>
  <div className="atlas-l0-status" role="status">
   {view.kind==="SEARCH"?"검색 "+hits.length+"건":activeTab?"원고 탐색":LABELS[view.kind]+" 열람"} · 게시 보류
  </div>
  <div className="atlas-l0-content">
   {activeTab&&<>
    <h2 ref={titleRef} tabIndex={-1}>{activeTab.label}</h2>
    <div className="atlas-l0-list">{atlas.catalog[activeTab.key].map(row=>
      <button className="atlas-l0-card" type="button" key={row.id}
       data-testid={"entry-"+row.id} onClick={()=>navigate({kind:activeTab.itemKind,id:row.id})}>
       <span className="atlas-l0-id">{row.id}{row.isThematicArchive?" · 주제 아카이브":""}</span>
       <strong>{row.title}</strong>{row.description&&<span className="atlas-l0-detail">{row.description}</span>}
      </button>)}</div>
   </>}
   {view.kind==="SEARCH"&&<>
    <h2 ref={titleRef} tabIndex={-1}>검색 결과 {hits.length}건</h2>
    <div className="atlas-l0-list">{hits.map(hit=>
     <button className="atlas-l0-card" type="button" key={hit.kind+hit.id}
      data-testid={"hit-"+hit.id} onClick={()=>navigate(hit.navigation)}>
      <span className="atlas-l0-id">{LABELS[hit.kind]} · {hit.id}</span>
      <strong>{hit.title}</strong><span className="atlas-l0-detail">{hit.excerpt}</span>
     </button>)}</div>
   </>}
   {!activeTab&&view.kind!=="SEARCH"&&(entity?<>
     <button className="atlas-l0-back" type="button" onClick={back}>← 이전 탐색으로</button>
     <article className="atlas-l0-article">
       <h2 ref={titleRef} tabIndex={-1}>{entity.title}</h2>
       <AtlasL0SafeMarkdown source={entity.bodyMarkdown}/>
     </article>
     {view.kind==="THEME"&&<>
       <h3>일곱 시대권 비교</h3>
       <div className="atlas-l0-list">{entity.links.map(link=>
        <button className="atlas-l0-card" type="button" key={link.targetId}
         data-testid={"link-"+link.targetId} onClick={()=>navigate({kind:"VOLUME",id:link.targetId})}>
         <span className="atlas-l0-id">{link.targetId} · {link.relationLabel}</span>
         <strong>{link.title}</strong>
        </button>)}</div>
     </>}
     {view.kind==="VOLUME"&&entity.relatedThemeIds.length>0&&<>
       <h3>여섯 비교 주제로 이동</h3>
       <div className="atlas-l0-links">{entity.relatedThemeIds.map(id=>
        <button type="button" key={id} onClick={()=>navigate({kind:"THEME",id})}>
          {atlas.getTheme(id).title}
        </button>)}</div>
     </>}
     {view.kind==="CHAPTER"&&<div className="atlas-l0-links">
      {atlas.catalog.chapters.filter(c=>Math.abs(c.order-entity.order)===1).map(ch=>
       <button type="button" key={ch.id} onClick={()=>navigate({kind:"CHAPTER",id:ch.id})}>
         {ch.order<entity.order?"← 이전":"다음 →"} · {ch.title}
       </button>)}</div>}
   </>:<p role="alert">존재하지 않는 자료입니다.</p>)}
  </div>
  <footer className="atlas-l0-footer">V4.23 원고 원문 · 교회사·교파 전문 교열 전 · 외부 공개 불가 · 수집되는 독해 응답 없음</footer>
 </section>;
}
