import React, {useId, useMemo, useRef, useState} from "react";
import "./atlas-flagship.css";
import {parseResearchMarkdown} from "./research-markdown.mjs";

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
function InlineTokens({tokens}) {
  return tokens.map((token,index)=>token.kind==="strong"
    ? <strong key={index}>{token.text}</strong>
    : token.kind==="em" ? <em key={index}>{token.text}</em>
    : <React.Fragment key={index}>{token.text}</React.Fragment>);
}
function SafeResearchMarkdown({source}) {
  return <div className="atlas-fp-prose">
    {parseResearchMarkdown(source).map((block,index)=>block.kind==="rule"
      ? <hr key={index}/>
      : React.createElement(block.tag,{key:index},<InlineTokens tokens={block.segments}/>))}
  </div>;
}
const safeExternal=url=>typeof url==="string"&&/^https:\/\/[^\s]+$/.test(url);
export default function AtlasFlagship1529Panel({
  scene, atlas, readerPack=null, privatePreviewGranted=false, onReturnToAtlas
}) {
  const [eventId,setEventId]=useState("EVENT-MARBURG-1529");
  const [layer,setLayer]=useState("L0");
  const [showEvidence,setShowEvidence]=useState(true);
  const [showEditionCompare,setShowEditionCompare]=useState(false);
  const [showWitnessCompare,setShowWitnessCompare]=useState(false);
  const readerPanelId=useId();
  const comparePanelId=useId();
  const witnessPanelId=useId();
  const evidencePanelId=useId();
  const timelineRef=useRef(null);
  const timelineYearsRef=useRef(null);
  const headingRef=useRef(null);
  const integrity=useMemo(()=>{
    if(!scene||!atlas||!atlas.meta)return null;
    const chapter=atlas.getChapter?.(scene.entry?.l1ChapterId);
    const volume=atlas.getVolume?.(scene.entry?.volumeId);
    const events=scene.timeline;
    if(!chapter||!volume||!Array.isArray(events)||events.length!==4 ||
      atlas.meta.canShip!==false || scene.contentGate?.canShip!==false ||
      !Array.isArray(scene.documentCards)||scene.documentCards.length!==2)return null;
    if(readerPack!==null&&(
      readerPack?.schema!=="ATLAS_V474_RESEARCH_READER_PACK" ||
      readerPack.canShip!==false ||
      readerPack.releaseGate?.canShip!==false ||
      readerPack.releaseGate?.canMergeMain!==false ||
      readerPack.releaseGate?.canImportAIStudio!==false ||
      readerPack.releaseGate?.hostAccessControlsVerified!==false ||
      readerPack.historianApproved!==false ||
      readerPack.readerPilotConfirmed!==false ||
      readerPack.archiveKZOriginalLeavesVerified!==false ||
      !readerPack.l0?.text?.includes("핵심 쟁점 가운데 하나") ||
      !readerPack.l1?.text?.includes("저본의 전승 관계를 확정할 수는 없다") ||
      !Array.isArray(readerPack.sources)||readerPack.sources.length!==6||
      !Array.isArray(readerPack.witnessComparison)||readerPack.witnessComparison.length!==3 ||
      !readerPack.sources.every(s=>safeExternal(s.sourceUrl)&&Array.isArray(s.linkedEventIds))
    ))return null;
    return {chapter,volume,events,pack:readerPack};
  },[scene,atlas,readerPack]);
  if(!privatePreviewGranted||!integrity) {
    return <section className="atlas-fp" data-atlas-state="BLOCKED" role="status">
      <h2>연구 원고 접근 제한</h2>
      <p>이 화면은 비공개 검토 전용입니다. 화면의 접근 허용 값은 서버 인증을 대신하지 않습니다.</p>
    </section>;
  }
  const selected=integrity.events.find(e=>e.id===eventId)||integrity.events[0];
  const docs=(integrity.pack?.sources??scene.documentCards).filter(d=>d.linkedEventIds.includes(selected.id));
  const {chapter,volume}=integrity;
  const activeText=layer==="L0"?(integrity.pack?.l0.text??volume.bodyMarkdown):(integrity.pack?.l1.text??chapter.bodyMarkdown);
  const sourceIds=[...new Set((activeText.match(/\\[(?:GA|GE|WP|ZA|SC|GR)\\]/g)||[]).map(x=>x.slice(1,-1)))];
  const allSources=integrity.pack?.sources??[];

  function handleRestart() {
    setEventId("EVENT-MARBURG-1529");
    setLayer("L0");
    setShowEvidence(true);
    setShowEditionCompare(false);
    setShowWitnessCompare(false);
    timelineYearsRef.current?.scrollTo?.({left:0,behavior:"instant"});
    headingRef.current?.scrollIntoView?.({block:"start",behavior:"instant"});
  }
  function handleReadingKeyDown(event) {
    if(!["ArrowLeft","ArrowRight","Home","End"].includes(event.key))return;
    event.preventDefault();
    const index=event.key==="Home"?0:event.key==="End"?1:layer==="L0"?1:0;
    const targetLayer=index===0?"L0":"L1";
    setLayer(targetLayer);
    event.currentTarget.parentElement?.querySelectorAll('[role="tab"]')[index]?.focus();
  }
  return <section className="atlas-fp" data-atlas-state="RESEARCH_PREVIEW" aria-label="마르부르크 아우크스부르크 역사 탐색">
    <header ref={headingRef} className="atlas-fp-heading">
      <div className="atlas-fp-kicker">REFORMATION ATLAS / 16TH CENTURY</div>
      <div className="atlas-fp-topline"><h1>{scene.title}</h1>
        <span className="atlas-fp-caveat">연구 초안 · 출판 보류</span></div>
      <p>{scene.educationalQuestion}</p>
      <div className="atlas-fp-meta">제4권 · L0 개요 / L1 중급 · 1529–1540 · 사료 {integrity.pack?"6종":"2종"} · {integrity.pack?"V4.72 연구 원고":"구형 연구 원고"}</div>
    </header>

    <div className="atlas-fp-layout">
      <nav ref={timelineRef} className="atlas-fp-timeline" aria-label="역사 사건 연표">
        <h2>시간의 흐름</h2>
        <p className="atlas-fp-help">연도를 선택하면 해당 사건과 문헌 근거가 바뀝니다.</p>
        <p className="atlas-fp-mobile-hint">연표를 좌우로 밀어 다른 사건을 보세요.</p>
        <div className="atlas-fp-timeline-years" ref={timelineYearsRef}>
          {integrity.events.map(e=><button type="button" key={e.id} className={"atlas-fp-year"+(selected.id===e.id?" selected":"")}
            aria-current={selected.id===e.id?"step":undefined} onClick={()=>setEventId(e.id)}>
            <span>{e.dateLabel}</span><strong>{e.title}</strong>
          </button>)}
        </div>
        <div className="atlas-fp-timeline-footnote">연표는 사건의 연도 비교이며 실제 이동 경로를 표현하지 않습니다.</div>
      </nav>
      <main className="atlas-fp-main">
        <div className="atlas-fp-section-kicker">SELECTED EVENT / {selected.dateLabel}</div>
        <h2 aria-live="polite">{selected.title}</h2>
        <div className="atlas-fp-place"><strong>관련 장소·주제</strong> {selected.placeLabel}</div>
        <p className="atlas-fp-lead">{selected.readersFinding}</p>
        <div className="atlas-fp-concern"><strong>왜 조심해야 할까?</strong><p>{selected.claimLimit}</p></div>
        <div className="atlas-fp-compare-control">
          <button type="button" onClick={()=>setShowEditionCompare(x=>!x)}
            aria-expanded={showEditionCompare} aria-controls={comparePanelId}>
            1530·1531·1540년 판본 비교 {showEditionCompare?"접기":"열기"}
          </button>
        </div>
        <section id={comparePanelId} className="atlas-fp-compare" hidden={!showEditionCompare} aria-label="판본 비교">
          <h3>제출된 문서와 뒤이은 인쇄본 구별</h3>
          <table><thead><tr><th scope="col">연도</th><th scope="col">역사적 구분</th></tr></thead>
            <tbody>{integrity.events.filter(e=>e.year>1529).map(e=>
              <tr key={e.id}><th scope="row">{e.dateLabel}</th><td>{e.readersFinding}</td></tr>
            )}</tbody></table>
          <p>제출 문서와 판본의 실제 동일성은 연도만으로 확정하지 않습니다.</p>
        </section>

        {integrity.pack&&<div className="atlas-fp-witness-control">
          <button type="button" aria-expanded={showWitnessCompare} aria-controls={witnessPanelId}
            onClick={()=>setShowWitnessCompare(x=>!x)}>
            1529년 인쇄본·번역문·서명본 비교 {showWitnessCompare?"접기":"열기"}
          </button>
        </div>}
        {integrity.pack&&<section id={witnessPanelId} className="atlas-fp-compare atlas-fp-witness" hidden={!showWitnessCompare}
            aria-label="1529년 문헌 증거 비교">
          <h3>서로 다른 문헌 증인과 확인되지 않은 사실</h3>
          <table><thead><tr><th scope="col">사료</th><th scope="col">자료에서 확인한 내용</th><th scope="col">현재의 한계</th></tr></thead>
            <tbody>{integrity.pack.witnessComparison.map(w=><tr key={w.id}>
              <th scope="row">{w.label} [{w.sourceId}]</th><td>{w.finding}</td><td>{w.limit}</td>
            </tr>)}</tbody></table>
          <p>인쇄본·편집 번역·보관소 목록의 차이만으로 필사본 계보를 확정하지 않습니다.</p>
        </section>}
        <div className="atlas-fp-tabs" role="tablist" aria-label="역사 원고의 깊이">
          <button role="tab" id={readerPanelId+"-l0"} aria-controls={readerPanelId}
            aria-selected={layer==="L0"} tabIndex={layer==="L0"?0:-1}
            onClick={()=>setLayer("L0")} onKeyDown={handleReadingKeyDown} type="button">L0 · 전체 개요</button>
          <button role="tab" id={readerPanelId+"-l1"} aria-controls={readerPanelId}
            aria-selected={layer==="L1"} tabIndex={layer==="L1"?0:-1}
            onClick={()=>setLayer("L1")} onKeyDown={handleReadingKeyDown} type="button">L1 · 역사적 해설</button>
        </div>
        <div className="atlas-fp-reading" id={readerPanelId} role="tabpanel"
          aria-labelledby={readerPanelId+(layer==="L0"?"-l0":"-l1")} tabIndex={0}>
          <div className="atlas-fp-reading-meta">{integrity.pack?"V4.72 연구용 개정본":layer==="L0"?"V4.47 연구용 개요":"V4.50 연구용 중급 해설"} · {integrity.pack?(layer==="L0"?integrity.pack.l0.title:integrity.pack.l1.title):(layer==="L0"?volume.title:chapter.title)}</div>
          <SafeResearchMarkdown source={activeText}/>
          {integrity.pack&&<div className="atlas-fp-provenance" aria-label="본문에 표시된 출처">
            <strong>이 원고의 출처</strong>{" "}
            {sourceIds.map(id=>{
              const src=allSources.find(s=>s.id===id);
              return src&&safeExternal(src.sourceUrl)?<a href={src.sourceUrl} key={id} target="_blank" rel="noopener noreferrer">[{id}]</a>:null;
            })}
            <p>링크는 선택할 때만 외부 기관으로 이동합니다. 원전 확인 수준은 사료 카드에서 확인하세요.</p>
          </div>}
        </div>
        <div className="atlas-fp-toolbar">
          <button type="button" onClick={handleRestart}>1529년으로 돌아가기</button>
          <button type="button" onClick={()=>setShowEvidence(x=>!x)} aria-expanded={showEvidence} aria-controls={evidencePanelId}>
            {showEvidence?"사료 카드 접기":"사료 카드 펼치기"}
          </button>
          {typeof onReturnToAtlas==="function"&&<button type="button" onClick={()=>onReturnToAtlas({kind:"VOLUME",id:scene.entry.volumeId})}>제4권 목록으로 돌아가기</button>}
        </div>
      </main>
      <aside id={evidencePanelId} className="atlas-fp-sources" hidden={!showEvidence} aria-label="사료와 판본 근거">
        <div className="atlas-fp-section-kicker">EVIDENCE / SOURCES</div>
        <h2>그 자료는 무엇을 증명하나?</h2>
        <p className="atlas-fp-help">당대 문헌의 편집 번역과 희귀본 소장목록은 근거 성격이 서로 다릅니다.</p>
        {docs.map(d=><article className="atlas-fp-source" key={d.id}>
          <h3>{d.title}</h3>
          {integrity.pack&&<span className="atlas-fp-source-id">[{d.id}] · {d.sourceKind}</span>}
          <p>{integrity.pack?d.note:d.documentClass==="HISTORICAL_AGREEMENT_TEXT"?"회담 문서의 후대 편집·번역 자료":"원본 판본을 구별하는 도서관 소장목록"}</p>
          {safeExternal(d.sourceUrl)?<a href={d.sourceUrl} target="_blank" rel="noopener noreferrer">기관 자료 열기 (외부 사이트)</a>:<span>출처 주소 확인 필요</span>}
        </article>)}
        <div className="atlas-fp-source"><strong>근거 유형</strong><p>{KIND[selected.evidenceType]||selected.evidenceType}</p></div>
        <div className="atlas-fp-source-warning">당대 인쇄본 전체 교감·K/Z 필사 원본 제15조 판독·역사학자 검토가 완료되지 않았습니다. 공개 GitHub 자료는 인증된 비공개 열람을 의미하지 않습니다.</div>
      </aside>
    </div>
    <footer className="atlas-fp-footer">연구 검토용 · 역사 전문가 승인 없음 · 실제 Google AI Studio 앱 미설치 · can_ship=false</footer>
  </section>;
}
