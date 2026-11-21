import React, {useId,useMemo,useRef,useState} from "react";
import {buildAtlasCrossVolumeResearch} from "./atlas-cross-volume-research.mjs";
import {parseResearchMarkdown} from "./research-markdown.mjs";
import "./atlas-cross-volume.css";

/**
 * Research-only two-volume reading surface.
 * privatePreviewGranted is UI protection, not authentication/authorization.
 * Real access restrictions, rights and historical approval remain with the host.
 */
function ResearchText({markdown}) {
 return <div className="atlas-cv-prose">
  {parseResearchMarkdown(markdown).map((block,i)=>block.kind==="rule"
   ? <hr key={i}/>
   : React.createElement(block.tag,{key:i},block.segments.map((token,j)=>
     token.kind==="strong"?<strong key={j}>{token.text}</strong>:
     token.kind==="em"?<em key={j}>{token.text}</em>:
     <React.Fragment key={j}>{token.text}</React.Fragment>)))}
 </div>;
}
const safeLink=url=>typeof url==="string"&&/^https:\/\/[^\s]+$/.test(url);
const names={"VOL-04":"제4권 · 개혁자들의 신앙고백","VOL-05":"제5권 · 가톨릭 쇄신과 공의회"};
export default function AtlasCrossVolumeResearchPanel({
 bundles,readingPaths,privatePreviewGranted=false,initialVolumeId="VOL-04",onReturnToAtlas
}){
 const library=useMemo(()=>buildAtlasCrossVolumeResearch(bundles,readingPaths),[bundles,readingPaths]);
 const [location,setLocation]=useState({volumeId:initialVolumeId,eventId:null,layer:"L0",compare:false,evidence:true});
 const tabId=useId(),compareId=useId(),sourceId=useId();
 const headingRef=useRef(null);
 if(!privatePreviewGranted||!library.ok||!library.volumes.some(v=>v.identity.volumeId===initialVolumeId)){
  return <section className="atlas-cv" data-atlas-state="BLOCKED" role="status">
   <h2>두 권 통합 연구 화면 접근 제한</h2>
   <p>검토 자료가 승인되지 않았거나 화면 접근 조건이 충족되지 않았습니다. UI 접근 값은 서버 인증을 대신하지 않습니다.</p>
  </section>;
 }
 const volume=library.volumes.find(v=>v.identity.volumeId===location.volumeId)||library.volumes[0];
 const event=volume.timeline.find(e=>e.id===location.eventId)||volume.timeline[0];
 const layer=volume.layers.find(l=>l.level===location.layer);
 const cited=[...new Set(Array.from(layer.markdown.matchAll(/\[([A-Z]{2,10})\]/g),m=>m[1]))];
 const currentSources=volume.sources.filter(s=>s.eventIds.includes(event.id));
 const volName=id=>names[id]||id;
 const jump=(targetVolumeId,targetEventId=null,targetLayer="L0")=>{
  const next=library.volumes.find(v=>v.identity.volumeId===targetVolumeId);
  if(!next)return;
  setLocation({volumeId:targetVolumeId,eventId:targetEventId||next.timeline[0].id,
    layer:targetLayer,compare:false,evidence:true});
 };
 const reset=()=>{jump(initialVolumeId,null,"L0");headingRef.current?.scrollIntoView?.({block:"start",behavior:"instant"})};
 const keyDown=e=>{
  if(!["ArrowLeft","ArrowRight","Home","End"].includes(e.key))return;
  e.preventDefault();
  const next=e.key==="Home"?"L0":e.key==="End"?"L1":e.key==="ArrowRight"?"L1":"L0";
  setLocation(s=>({...s,layer:next}));
  e.currentTarget.parentElement?.querySelectorAll('[role="tab"]')[next==="L0"?0:1]?.focus();
 };
 return <section className="atlas-cv" data-atlas-state="CROSS_VOLUME_RESEARCH"
  aria-label="종교개혁 ATLAS 제4권과 제5권 통합 연구 탐색">
  <header className="atlas-cv-heading" ref={headingRef}>
   <div className="atlas-cv-kicker">REFORMATION ATLAS / TWO-VOLUME RESEARCH READER / V4.77</div>
   <h1>신앙고백과 가톨릭 쇄신, 서로 다른 문헌을 읽다</h1>
   <p>1529~1564년 주요 문헌을 두 권에서 연결해 읽습니다. 비교는 학습 경로이며 사료 계보나 직접 인과관계의 확정이 아닙니다.</p>
   <div className="atlas-cv-status">연구 초안 · 역사학자 승인 0명 · 독자 실증 0명 · 실제 AI Studio 운영 앱 미반영 · can_ship=false</div>
   <nav className="atlas-cv-volumes" aria-label="연구 권 선택">
    {library.volumes.map((v,i)=><button type="button" className="atlas-cv-volume" key={v.identity.volumeId}
       aria-current={v.identity.volumeId===volume.identity.volumeId?"page":undefined}
       onClick={()=>jump(v.identity.volumeId)}>{volName(v.identity.volumeId)} <span>사건 {v.timeline.length}개 · 사료 {v.sources.length}종</span></button>)}
   </nav>
  </header>
  <section className="atlas-cv-paths" aria-label="두 권을 잇는 독자 경로">
   <h2>독자 탐색 경로 <small>서로 다른 역사 문헌을 비교하기 위한 질문</small></h2>
   <div className="atlas-cv-route-grid">{library.links.map(path=><article className="atlas-cv-route" key={path.id}>
    <h3>{path.title}</h3><p>{path.invitation}</p>
    <div className="atlas-cv-route-actions">
     <button type="button" className="atlas-cv-jump" onClick={()=>jump(path.from.volumeId,path.from.eventId,"L1")}>
      {path.from.volumeId==="VOL-04"?"제4권":"제5권"}에서 읽기
     </button>
     <button type="button" className="atlas-cv-jump" onClick={()=>jump(path.to.volumeId,path.to.eventId,"L1")}>
      {path.to.volumeId==="VOL-04"?"제4권":"제5권"}에서 읽기
     </button>
    </div>
    <p className="atlas-cv-route-sources">연결 사료: {path.from.sourceIds.map(id=>"["+id+"]").join(" ")} ↔ {path.to.sourceIds.map(id=>"["+id+"]").join(" ")}</p>
    <p className="atlas-cv-caveat"><strong>해석상 주의:</strong> {path.caution}</p>
   </article>)}</div>
  </section>
  <div className="atlas-cv-layout">
   <nav className="atlas-cv-timeline" aria-label="선택한 권의 역사 사건 연표">
    <h2>{volume.identity.volumeId==="VOL-04"?"제4권":"제5권"} 사건 연표</h2>
    <div className="atlas-cv-years">{volume.timeline.map(e=><button type="button" key={e.id} className="atlas-cv-event"
      aria-current={e.id===event.id?"step":undefined}
      onClick={()=>setLocation(s=>({...s,eventId:e.id}))}>
      <span>{e.dateLabel}</span><strong>{e.title}</strong></button>)}</div>
    <p className="atlas-cv-footnote">동시대 사건의 시간 비교이지 인물의 이동 경로나 사료의 필사 계보가 아닙니다.</p>
   </nav>
   <main className="atlas-cv-main">
    <div className="atlas-cv-kicker">{volume.identity.volumeId} / {event.dateLabel}</div>
    <h2>{event.title}</h2><p className="atlas-cv-event-summary">{event.summary}</p>
    <p className="atlas-cv-warning"><strong>원전 검토의 한계:</strong> {event.claimLimit}</p>
    <div className="atlas-cv-controls">
     <button type="button" aria-expanded={location.compare} aria-controls={compareId}
      onClick={()=>setLocation(s=>({...s,compare:!s.compare}))}>
      {location.compare?"문헌 비교 접기":"이 권의 문헌 증거 비교"}
     </button>
    </div>
    <section id={compareId} className="atlas-cv-comparison" hidden={!location.compare} aria-label="선택한 권의 근거 비교">
     <h3>문헌이 확인해 주는 것과 아직 확인하지 못한 것</h3>
     <table><thead><tr><th scope="col">사료</th><th scope="col">관찰 내용</th><th scope="col">미확정 사항</th></tr></thead>
      <tbody>{volume.comparisons.map(c=><tr key={c.id}><th scope="row">{c.label} [{c.sourceId}]</th>
       <td>{c.observation}</td><td>{c.limitation}</td></tr>)}</tbody></table>
    </section>
    <div className="atlas-cv-tabs" role="tablist" aria-label="역사 원고의 깊이">
     {["L0","L1"].map(level=><button key={level} type="button" role="tab" id={tabId+"-"+level}
       tabIndex={location.layer===level?0:-1} aria-selected={location.layer===level}
       aria-controls={tabId+"-content"} onKeyDown={keyDown}
       onClick={()=>setLocation(s=>({...s,layer:level}))}>
       {level==="L0"?"L0 · 전체 개요":"L1 · 역사적 해설"}</button>)}
    </div>
    <article id={tabId+"-content"} role="tabpanel" tabIndex={0}
     aria-labelledby={tabId+"-"+location.layer} className="atlas-cv-reading">
     <div className="atlas-cv-reading-title">{layer.title}</div>
     <ResearchText markdown={layer.markdown}/>
     <div className="atlas-cv-trace" aria-label="해당 원고의 사료 근거">
      <strong>본문 근거</strong>{" "}
      {cited.map(id=>{const s=volume.sources.find(x=>x.id===id);
       return s&&safeLink(s.url)?<a href={s.url} key={id} target="_blank" rel="noopener noreferrer">[{id}]</a>:null})}
      <p>목록·번역·인쇄본은 서로 다른 자료 유형입니다. 링크는 선택할 때만 외부 기관으로 이동합니다.</p>
     </div>
    </article>
    <div className="atlas-cv-actions">
     <button type="button" onClick={reset}>제4·5권 읽기 시작점으로</button>
     <button type="button" aria-expanded={location.evidence} aria-controls={sourceId}
      onClick={()=>setLocation(s=>({...s,evidence:!s.evidence}))}>
      {location.evidence?"사료 카드 접기":"사료 카드 펼치기"}</button>
     {typeof onReturnToAtlas==="function"&&<button type="button"
      onClick={()=>onReturnToAtlas({kind:"VOLUME",id:volume.identity.volumeId})}>
      선택한 권의 목록으로 돌아가기</button>}
    </div>
   </main>
   <aside id={sourceId} className="atlas-cv-sources" hidden={!location.evidence} aria-label="선택한 사건의 사료 카드">
    <div className="atlas-cv-kicker">EVIDENCE AND LIMITS</div><h2>어떤 증거인가?</h2>
    <p>사료의 종류와 확인 한계를 구별해야 같은 사건의 문헌을 혼동하지 않습니다.</p>
    {currentSources.map(s=><article className="atlas-cv-source-card" key={s.id}>
     <h3>[{s.id}] {s.title}</h3>
     <div className="atlas-cv-source-kind">{s.sourceKind}</div>
     <p>{s.sourceLimit}</p>
     {safeLink(s.url)?<a href={s.url} target="_blank" rel="noopener noreferrer">공식·원문 자료 열기</a>:<span>출처 주소 확인 필요</span>}
    </article>)}
    <p className="atlas-cv-source-warning">이 화면의 역사학자 검토와 독자 평가는 완료되지 않았습니다. GitHub의 공개 연구 파일은 실제 접근 인증을 제공하지 않습니다.</p>
   </aside>
  </div>
  <footer className="atlas-cv-footer">V4.77 · 공통 React 연구 컴포넌트 · 외부 네트워크 호출/평가 응답 수집 없음 · 운영 앱 변경 없음 · can_ship=false</footer>
 </section>;
}
