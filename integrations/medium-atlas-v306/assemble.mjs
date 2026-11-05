/** Reversible V3.06 integration of frozen V3.04 readers and V3.05 additions. */
const ok=(value,message)=>{if(!value)throw Error('V306: '+message);};
export const pathSpecs=[
 {id:'ISSUE-PIETISM-EDUCATION',axis:'ISSUE',title:'경건주의: 성경·교육·돌봄',indices:[0,8,14,1,9],reading_question:'실천적 갱신은 어떤 교육과 공동체 운영을 낳았는가?',interpretive_limit:'1675년 책·1695년 사업·1698년 건축을 구별한다.'},
 {id:'TIME-REVIVAL-1727-1746',axis:'CHRONOLOGY',title:'1727~1746: 공동체와 부흥, 분별',indices:[2,10,3,11,4,19,5,12,6,17,15,16],reading_question:'현장 경험과 기록된 부흥 해설은 어떻게 다른가?',interpretive_limit:'1722년 정착과 1727년 갱신, 공동체 규칙과 설교·찬송을 구별한다.'},
 {id:'REGION-ATLANTIC-INDIA-1792',axis:'REGION',title:'대서양과 인도: 근대 선교 기획',indices:[7,18,13],reading_question:'선교 조직·이동·현지 협력은 어떻게 연결되는가?',interpretive_limit:'1792년 결성과 1793년 도착을 구분하고 식민지 환경을 함께 살핀다.'}
];
export function assembleMediumDelivery(base,addition,cross){
 ok(base?.version==='3.04'&&base.readers?.length===475&&base.sources?.length===675,'475-reader base mismatch');
 ok(addition?.version==='3.05'&&addition.chapters?.length===20&&addition.sources?.length===22&&addition.catalogue?.length===495,'20-reader addition mismatch');
 ok(cross?.version==='3.04'&&cross.entries?.length===97,'overview mismatch');
 for(const gate of [base.publication_gate,addition.publication_gate,cross.publication_gate])ok(gate&&Object.values(gate).every(x=>x===false),'HOLD gate');
 const b=structuredClone(base),a=structuredClone(addition),x=structuredClone(cross);
 ok(base.readers.every((r,i)=>a.catalogue[i].id===r.id),'catalogue identity mismatch');
 b.version='3.06';b.kind='INTEGRATED_495_MEDIUM_READING_DELIVERY';
 b.parent_commit='b1e046dd6fae409d99ddbaa8d7ae08d696d1cced';
 b.editorial_note='V3.04 본문과 출처 검증 기록을 그대로 보존하고 V3.05 20편을 추가한 편집 검토본. 원전 재판독과 이번 버전의 외부 확인 없음.';
 const sourceIds=new Set(a.sources.map(s=>s.id)), readerIds=new Set(base.readers.map(r=>r.id));
 ok(sourceIds.size===22&&readerIds.size===475,'duplicate input IDs');
 for(const s of a.sources)b.sources.push({...s,id:'V305-'+s.id,original_id:s.id,provenance:{dataset:'data/deep/atlas_v305_medium_depth_pietism_revival_readers.json'}});
 for(const [i,c] of a.chapters.entries()){
  ok(!readerIds.has(c.id)&&c.sections?.length===3&&c.sources?.length&&c.sources.every(id=>sourceIds.has(id)),'new reader invalid '+c.id);
  readerIds.add(c.id);
  const type=c.id.split('-')[0];ok(['PERSON','EVENT','DOCUMENT'].includes(type),'invalid type');
  b.readers.push({...c,reader_type:type,sources:c.sources.map(id=>'V305-'+id),research_basis_ids:[],
   source_basis_status:'V305_SCOPED_INSPECTION_INHERITED_NOT_RECHECKED',
   provenance:{dataset:'data/deep/atlas_v305_medium_depth_pietism_revival_readers.json',chapter_index:i,reader_document:'docs/01_CONTENT/V305_PIETISM_REVIVAL_MEDIUM_READERS.md'}});
  const group=b.reader_groups.find(g=>g.id==='TYPE-'+type);ok(group,'group not found');group.reader_ids.push(c.id);
 }
 ok(a.chapters.every(c=>c.related_readers.every(id=>readerIds.has(id))),'unresolved related reader');
 const used=new Set();
 for(const p of pathSpecs){
  const ids=p.indices.map(i=>a.chapters[i].id);
  for(const id of ids){ok(!used.has(id),'repeated path reader');used.add(id);}
  b.reading_paths.push({id:p.id,axis:p.axis,title:p.title,reader_ids:ids,reading_question:p.reading_question,interpretive_limit:p.interpretive_limit,status:'EDITORIAL_NAVIGATION_DRAFT'});
 }
 ok(used.size===20&&b.reading_paths.length===27,'path coverage mismatch');
 b.source_dataset_notes.push({dataset:'data/deep/atlas_v305_medium_depth_pietism_revival_readers.json',note:'원판 이미지 판독0면; 기존 자료 확인 범위 상속·이번 통합 시 재검증 없음.'});
 b.metrics={...base.metrics,readers:495,sections:1485,questions:495,body_characters:base.metrics.body_characters+a.metrics.new_body_characters,
 source_records:697,new_historical_essays:0,integrated_v305_readers:20,added_reading_paths:3};
 b.editorial_audit.v306_review={reviewed_reader_ids:a.chapters.map(c=>c.id),body_revisions:0,
  scope:'기존 원고 보존 및 연대·기록 유형·해석 경계 점검. 외부 역사 전문 감수 아님.',
  distinctions:['1675 출판/1695 교육/1698 건물','1722 정착/1727 갱신','1792 선교회/1793 도착','감리교 규칙/설교 전체','부흥 체험/출판 기록','구빈 활동/노예제 지지','선교사 활동/현지 협력·식민지 조건','찬송집 서지/가사·악보 원본']};
 x.version='3.06';x.parent_commit=b.parent_commit;
 const rows=new Map(x.entries.map(r=>[r.overview_id,r]));
 for(const u of a.overview_link_updates){
  const row=rows.get(u.overview_id),target=b.readers.find(r=>r.id===u.reader_id);
  ok(row&&target&&row.title===u.overview_title&&row.mapping_status===u.previous_status,'mapping mismatch '+u.overview_id);
  row.mapping_status=u.new_status;row.scope=u.scope;
  row.reader_links=[{reader_id:u.reader_id,role:'PRIMARY',title:target.title},...row.reader_links.map(l=>({...l,role:l.role==='PRIMARY'?'FOLLOWUP':l.role}))];
 }
 const counts={DIRECT_TOPIC:0,PARTIAL_COVERAGE:0,BACKGROUND_ONLY:0,NO_MATCH:0};
 for(const r of x.entries){ok(Object.hasOwn(counts,r.mapping_status),'invalid status');counts[r.mapping_status]++;}
 ok(counts.DIRECT_TOPIC===64&&counts.PARTIAL_COVERAGE===14&&counts.BACKGROUND_ONLY===1&&counts.NO_MATCH===18,'coverage mismatch');
 x.metrics={...x.metrics,direct_topic:64,partial_coverage:14,background_only:1,no_match:18,default_readable:78,
 reading_links:x.entries.reduce((n,r)=>n+r.reader_links.length,0),unique_readers:new Set(x.entries.flatMap(r=>r.reader_links.map(l=>l.reader_id))).size};
 ok(b.readers.length===495&&b.sources.length===697,'result counts mismatch');
 ok(new Set(b.reader_groups.flatMap(g=>g.reader_ids)).size===495,'group partition');
 ok(JSON.stringify(b.readers.slice(0,475))===JSON.stringify(base.readers),'older readers changed');
 ok(JSON.stringify(b.sources.slice(0,675))===JSON.stringify(base.sources),'older sources changed');
 ok(JSON.stringify(b.source_verification)===JSON.stringify(base.source_verification),'source audit changed');
 return {delivery:b,crosswalk:x};
}
