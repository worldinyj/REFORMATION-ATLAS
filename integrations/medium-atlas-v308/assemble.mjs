/** Integrate 18 V3.07 reader drafts atop V3.06 while preserving every frozen record.
 * An editorial navigation assembly, not a primary-source verification or publication.
 */
import {assembleMediumDelivery as assembleV306} from '../medium-atlas-v306/assemble.mjs';
const check=(x,m)=>{if(!x)throw new Error('V308 assembly: '+m);};
const DATASET='data/deep/atlas_v307_remaining_overview_medium_readers.json';
export const readingPathSpecs=[
  {id:'TIME-KOREAN-CATHOLIC-1784',axis:'CHRONOLOGY',title:'1784년 조선 천주교: 서학에서 공동체로',
   indices:[0,1,8],reading_question:'개인의 북경 세례, 조선의 학문 토론, 국내 신앙 모임은 어떻게 달랐는가?',
   interpretive_limit:'세례의 일부 연도 표기 차이·1784년 국내 공동체·1785년 적발을 각각 구분한다.'},
  {id:'TIME-KOREAN-PROTESTANT-1882-1907',axis:'CHRONOLOGY',title:'1882~1907년 한국 개신교: 번역·교육·부흥',
   indices:[2,9,14,3,10,4,5,11,12,17],reading_question:'한국인 신자·성서 번역·외국인 입국·제도 설립은 어떤 순서로 만났는가?',
   interpretive_limit:'1882년 복음서/1887년 신약, 1884년 입국/1885년 병원, 1885년 상륙/1886년 개교를 구별한다.'},
  {id:'ISSUE-EARLY-MEDIEVAL-STRUCTURES',axis:'ISSUE',title:'초기·중세 교회: 서신·수도원·동서 차이',
   indices:[6,7,16],reading_question:'대표 서신·수도 규칙·분열을 장기 제도사로 읽으면 무엇이 달라지는가?',
   interpretive_limit:'2세기 서신의 표본성, 6세기 규칙과 9세기 보급, 1054년 전후의 긴 분리 과정을 구분한다.'},
  {id:'ISSUE-WCC-1948',axis:'ISSUE',title:'1948년 WCC: 창립과 문서의 층위',
   indices:[13,15],reading_question:'총회 개최, 창립, 공식 보고서, 후대 신앙 기반 문구는 어떻게 다르게 읽는가?',
   interpretive_limit:'1948년 8월22일 개막/23일 창립, 1961년 문구 개정, 보고서 전문 미검증을 구분한다.'},
];
export function assembleV308(base,v305,cross304,v307){
  const old=assembleV306(base,v305,cross304);
  check(v307?.version==='3.07'&&v307.status==='DRAFT'&&v307.depth==='MEDIUM','missing V3.07 draft identity');
  check(v307.chapters?.length===18&&v307.sources?.length===26&&v307.catalogue?.length===513,'incomplete V3.07 draft');
  check(v307.publication_gate&&Object.values(v307.publication_gate).every(v=>v===false),'V3.07 publication gate');
  check(v307.coverage_projection?.actual_app_updated===false,'V3.07 app status');
  check(v307.catalogue.slice(0,495).every((c,i)=>JSON.stringify(c)===JSON.stringify(v305.catalogue[i])),'495 catalogue identity drift');
  const b=old.delivery,x=old.crosswalk;
  const ids=new Set(b.readers.map(r=>r.id)),sourceIds=new Set(v307.sources.map(s=>s.id));
  check(ids.size===495&&sourceIds.size===26,'duplicate input IDs');
  for(const s of v307.sources){
    check(s.checked_on==='2026-11-06'&&s.inspection_level==='PUBLIC_LANDING_PAGE_OR_SEARCH_EXCERPT'&&s.original_image_read===false,'source provenance state '+s.id);
    b.sources.push({...structuredClone(s),id:'V307-'+s.id,original_id:s.id,provenance:{dataset:DATASET}});
  }
  for(const [i,c] of v307.chapters.entries()){
    check(!ids.has(c.id),'duplicate reader '+c.id);
    check(c.sections?.length===3&&c.reading_question?.endsWith('?')&&c.sources?.length>0,'incomplete reader '+c.id);
    check(c.sources.every(id=>sourceIds.has(id)),'source ID resolution '+c.id);
    ids.add(c.id);
    const type=c.id.split('-')[0];check(['PERSON','EVENT','DOCUMENT','THEME'].includes(type),'invalid reader category '+c.id);
    const reader={...structuredClone(c),reader_type:type,sources:c.sources.map(id=>'V307-'+id),research_basis_ids:[],
      source_basis_status:'V307_SCOPED_INSPECTION_INHERITED_NOT_RECHECKED',
      provenance:{dataset:DATASET,chapter_index:i,reader_document:'docs/01_CONTENT/V307_REMAINING_OVERVIEW_MEDIUM_READERS.md'}};
    b.readers.push(reader);
    const group=b.reader_groups.find(g=>g.id==='TYPE-'+type);check(group,'missing reader group '+type);
    group.reader_ids.push(c.id);
  }
  check(v307.chapters.every(c=>c.related_readers.every(id=>ids.has(id))),'broken related-reading reference');
  check(b.readers.length===513&&new Set(b.readers.map(r=>r.id)).size===513,'final reader identities');
  const placed=new Set();
  for(const p of readingPathSpecs){
    const reader_ids=p.indices.map(i=>v307.chapters[i].id);
    for(const id of reader_ids){check(!placed.has(id),'duplicate new navigation '+id);placed.add(id);}
    b.reading_paths.push({id:p.id,axis:p.axis,title:p.title,reader_ids,reading_question:p.reading_question,
      interpretive_limit:p.interpretive_limit,status:'EDITORIAL_NAVIGATION_DRAFT'});
  }
  check(placed.size===18&&b.reading_paths.length===31,'four editorial paths coverage');
  b.version='3.08';b.kind='INTEGRATED_513_MEDIUM_READING_DELIVERY';
  b.parent_commit='b17a51c54733fc3fd358b6585602585fcede4bc0';
  b.editorial_note='V3.06의 495편 본문·근거·검토 기록 보존. V3.07 18편을 추가한 비공개 편집 검토본이며 원전 대조·전문 감수·실제 AI Studio 앱 연동이 아니다.';
  b.source_dataset_notes.push({dataset:DATASET,note:'26개 신규 출처는 V3.07의 공개 페이지·검색 발췌 범위에 한정. 이번 통합 단계에서 원판 재검토나 외부 재방문으로 승격하지 않음.'});
  b.metrics={...b.metrics,readers:513,sections:1539,questions:513,source_records:723,
    body_characters:old.delivery.metrics.body_characters+v307.metrics.new_body_characters,
    new_historical_essays:0,integrated_v307_readers:18,added_reading_paths:4};
  b.editorial_audit.v308_review={reviewed_reader_ids:v307.chapters.map(r=>r.id),body_revisions:0,
   scope:'독자 탐색과 명시적 개요 연결, 연대 구별에 대한 편집 검증. 전문 역사 감수·원판 교감은 해당 없음.',
   distinctions:['1784년 귀국/1785년 모임 적발','1882년 복음서/1887년 신약전서',
   '1884년 앨런 입국/1885년 의료기관','1885년 상륙/1886년 배재학당 개교',
   '1903년 원산/1907년 평양','1948년 WCC 창립/1961년 신앙 기반 개정',
   '6세기 수도규칙/9세기 보급','1054년 사건/장기적 동서 분리']};
  x.version='3.08';x.parent_commit=b.parent_commit;
  const rows=new Map(x.entries.map(r=>[r.overview_id,r]));
  check(rows.size===97&&v307.overview_link_updates.length===18,'overview basis');
  for(const u of v307.overview_link_updates){
    const row=rows.get(u.overview_id),reader=b.readers.find(r=>r.id===u.reader_id);
    check(row&&reader&&row.title===u.overview_title&&row.mapping_status===u.previous_status,'overview link mismatch '+u.overview_id);
    check(['DIRECT_TOPIC','PARTIAL_COVERAGE'].includes(u.new_status),'invalid promoted scope '+u.overview_id);
    row.mapping_status=u.new_status;row.scope=u.scope;
    row.reader_links=[{reader_id:u.reader_id,role:'PRIMARY',title:reader.title},
      ...row.reader_links.filter(l=>l.reader_id!==u.reader_id).map(l=>({...l,role:l.role==='PRIMARY'?'FOLLOWUP':l.role}))];
  }
  const count={DIRECT_TOPIC:0,PARTIAL_COVERAGE:0,BACKGROUND_ONLY:0,NO_MATCH:0};
  for(const r of x.entries){check(Object.hasOwn(count,r.mapping_status),'unknown crosswalk state');count[r.mapping_status]++;}
  check(count.DIRECT_TOPIC===78&&count.PARTIAL_COVERAGE===18&&count.BACKGROUND_ONLY===1&&count.NO_MATCH===0,'97-overview coverage mismatch');
  x.metrics={...x.metrics,direct_topic:78,partial_coverage:18,background_only:1,no_match:0,
    default_readable:96,reading_links:x.entries.reduce((n,r)=>n+r.reader_links.length,0),
    unique_readers:new Set(x.entries.flatMap(r=>r.reader_links.map(l=>l.reader_id))).size};
  const grouped=b.reader_groups.flatMap(g=>g.reader_ids);
  check(grouped.length===513&&new Set(grouped).size===513,'reader group partition');
  check(b.sources.length===723&&new Set(b.sources.map(s=>s.id)).size===723,'source count');
  check(b.readers.slice(0,495).every((r,i)=>JSON.stringify(r)===JSON.stringify(old.delivery.readers[i])),'previous bodies changed');
  check(b.sources.slice(0,697).every((s,i)=>JSON.stringify(s)===JSON.stringify(old.delivery.sources[i])),'previous source states changed');
  check(JSON.stringify(b.source_verification)===JSON.stringify(old.delivery.source_verification),'selected claim audit changed');
  return {delivery:b,crosswalk:x};
}
