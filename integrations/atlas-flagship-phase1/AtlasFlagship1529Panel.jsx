import React, {useMemo, useState} from "react";
import "./atlas-flagship.css";

/**
 * First research-only vertical slice for the existing REFORMATION ATLAS app.
 * Host must enforce real authentication/authorisation and limit delivery of
 * research payload at the server. privatePreviewGranted is only a UI guard.
 * This candidate is NOT part of the actual AI Studio Build app.
 */
const KIND = {
  EDITED_PRIMARY_TEXT_IN_ENGLISH_TRANSLATION:"편집·번역된 역사 문서",
  INSTITUTIONAL_RARE_BOOKS_BIBLIOGRAPHY:"희귀본 소장목록",
  TWO_RARE_BOOKS_CATALOGUE_DESCRIPTIONS:"희귀본 판본 구분"
};
function StrongSegments({value}) {
  return String(value).split(/(\*\*[^*]+\*\*)/g).filter(Boolean).map((segment,index)=>
    segment.startsWith("**")&&segment.endsWith("**")
    ? <strong key={index}>{segment.slice(2,-2)}</strong>
    : <React.Fragment key={index}>{segment}</React.Fragment>);
}
function SafeResearchMarkdown({source}) {
  return <div className="atlas-fp-prose">
    {String(source??"").trim().split(/\n\s*\n/g).filter(Boolean).map((part,i)=>{
      const txt=part.trim();
      const heading=txt.match(/^#{1,4} +(.+)$/);
      if(heading)return <h3 key={i}><StrongSegments value={heading[1]}/></h3>;
      return <p key={i}><StrongSegments value={txt.replace(/\n/g," ")}/></p>;
    })}
  </div>;
}
const safeExternal=url=>typeof url==="string"&&/^https:\/\/[^\s]+$/.test(url);
export default function AtlasFlagship1529Panel({
  scene, atlas, privatePreviewGranted=false, onReturnToAtlas
}) {
  const [eventId,setEventId]=useState("EVENT-MARBURG-1529");
  const [layer,setLayer]=useState("L0");
  const [showEvidence,setShowEvidence]=useState(true);
  const integrity=useMemo(()=>{
    if(!scene||!atlas||!atlas.meta)return null;
    const chapter=atlas.getChapter?.(scene.entry?.l1ChapterId);
    const volume=atlas.getVolume?.(scene.entry?.volumeId);
    const events=scene.timeline;
    if(!chapter||!volume||!Array.isArray(events)||events.length!==4 ||
      atlas.meta.canShip!==false || scene.contentGate?.canShip!==false ||
      !Array.isArray(scene.documentCards)||scene.documentCards.length!==2)return null;
    return {chapter,volume,events};
  },[scene,atlas]);
  if(!privatePreviewGranted||!integrity) {
    return <section className="atlas-fp" data-atlas-state="BLOCKED" role="status">
      <h2>연구 원고 접근 제한</h2>
      <p>이 화면은 비공개 검토 전용입니다. 화면의 접근 허용 값은 서버 인증을 대신하지 않습니다.</p>
    </section>;
  }
  const selected=integrity.events.find(e=>e.id===eventId)||integrity.events[0];
  const docs=scene.documentCards.filter(d=>d.linkedEventIds.includes(selected.id));
  const {chapter,volume}=integrity;
  return <section className="atlas-fp" data-atlas-state="RESEARCH_PREVIEW" aria-label="마르부르크 아우크스부르크 역사 탐색">
    <header className="atlas-fp-heading">
      <div className="atlas-fp-kicker">REFORMATION ATLAS / 16TH CENTURY</div>
      <div className="atlas-fp-topline"><h1>{scene.title}</h1>
        <span className="atlas-fp-caveat">연구 초안 · 출판 보류</span></div>
      <p>{scene.educationalQuestion}</p>
      <div className="atlas-fp-meta">제4권 · L0 개요 / L1 중급 · 1529–1540 · 사료 2종</div>
    </header>

    <div className="atlas-fp-layout">
      <nav className="atlas-fp-timeline" aria-label="역사 사건 연표">
        <h2>시간의 흐름</h2>
        <p className="atlas-fp-help">연도를 선택하면 해당 사건과 문헌 근거가 바뀝니다.</p>
        {integrity.events.map(e=><button type="button" key={e.id} className={"atlas-fp-year"+(selected.id===e.id?" selected":"")}
          aria-current={selected.id===e.id?"step":undefined} onClick={()=>setEventId(e.id)}>
          <span>{e.dateLabel}</span><strong>{e.title}</strong>
        </button>)}
        <div className="atlas-fp-timeline-footnote">연표는 사건의 연도 비교이며 실제 이동 경로를 표현하지 않습니다.</div>
      </nav>
      <main className="atlas-fp-main">
        <div className="atlas-fp-section-kicker">SELECTED EVENT / {selected.dateLabel}</div>
        <h2>{selected.title}</h2>
        <div className="atlas-fp-place"><strong>관련 장소·주제</strong> {selected.placeLabel}</div>
        <p className="atlas-fp-lead">{selected.readersFinding}</p>
        <div className="atlas-fp-concern"><strong>왜 조심해야 할까?</strong><p>{selected.claimLimit}</p></div>

        <div className="atlas-fp-tabs" role="tablist" aria-label="역사 원고의 깊이">
          <button role="tab" aria-selected={layer==="L0"} onClick={()=>setLayer("L0")} type="button">L0 · 전체 개요</button>
          <button role="tab" aria-selected={layer==="L1"} onClick={()=>setLayer("L1")} type="button">L1 · 역사적 해설</button>
        </div>
        <div className="atlas-fp-reading">
          <div className="atlas-fp-reading-meta">{layer==="L0"?"V4.47 연구용 개요":"V4.50 연구용 중급 해설"} · {layer==="L0"?volume.title:chapter.title}</div>
          <SafeResearchMarkdown source={layer==="L0"?volume.bodyMarkdown:chapter.bodyMarkdown}/>
        </div>
        <div className="atlas-fp-toolbar">
          <button type="button" onClick={()=>setShowEvidence(x=>!x)} aria-expanded={showEvidence} aria-controls="atlas-fp-evidence">
            {showEvidence?"사료 카드 접기":"사료 카드 펼치기"}
          </button>
          {typeof onReturnToAtlas==="function"&&<button type="button" onClick={()=>onReturnToAtlas({kind:"VOLUME",id:scene.entry.volumeId})}>제4권 목록으로 돌아가기</button>}
        </div>
      </main>
      <aside id="atlas-fp-evidence" className="atlas-fp-sources" hidden={!showEvidence} aria-label="사료와 판본 근거">
        <div className="atlas-fp-section-kicker">EVIDENCE / SOURCES</div>
        <h2>그 자료는 무엇을 증명하나?</h2>
        <p className="atlas-fp-help">당대 문헌의 편집 번역과 희귀본 소장목록은 근거 성격이 서로 다릅니다.</p>
        {docs.map(d=><article className="atlas-fp-source" key={d.id}>
          <h3>{d.title}</h3>
          <p>{d.documentClass==="HISTORICAL_AGREEMENT_TEXT"?"회담 문서의 후대 편집·번역 자료":"원본 판본을 구별하는 도서관 소장목록"}</p>
          {safeExternal(d.sourceUrl)?<a href={d.sourceUrl} target="_blank" rel="noopener noreferrer">기관 자료 열기 (외부 사이트)</a>:<span>출처 주소 확인 필요</span>}
        </article>)}
        <div className="atlas-fp-source"><strong>근거 유형</strong><p>{KIND[selected.evidenceType]||selected.evidenceType}</p></div>
        <div className="atlas-fp-source-warning">당대 인쇄본 전문 교감·역사학자 검토가 완료된 자료가 아닙니다. 이미지·지도의 고증 및 권리 확인도 아직 없습니다.</div>
      </aside>
    </div>
    <footer className="atlas-fp-footer">연구 검토용 · 역사 전문가 승인 없음 · 실제 Google AI Studio 앱 미설치 · can_ship=false</footer>
  </section>;
}
