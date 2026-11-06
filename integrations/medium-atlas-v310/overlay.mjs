/**
 * V3.10 editorial overlay. Keeps V3.09's 513 bodies and source link corrigendum,
 * upgrades stale overview navigation, appends clearly limited research dossiers.
 * No publication or original-text collation.
 */
import {assembleV309} from '../medium-atlas-v309/overlay.mjs';
const check=(v,m)=>{if(!v)throw Error('V310 quality overlay: '+m);};
export function assembleV310(inputs,v309Audit,v310Audit){
  const prior=assembleV309(inputs,v309Audit);
  const {delivery:b,crosswalk:x}=prior;
  check(b.readers.length===513&&b.sources.length===723&&x.entries.length===97,'base input counts');
  check(v310Audit?.version==='3.10'&&v310Audit.status==='DRAFT'&&v310Audit.depth==='MEDIUM','audit version');
  check(v310Audit.publication_gate&&Object.values(v310Audit.publication_gate).every(v=>v===false),'audit publication HOLD');
  check(v310Audit.coverage_audit?.length===19&&v310Audit.navigation_patches?.length===10
    &&v310Audit.source_reading_dossiers?.length===6,'incomplete quality audit');
  const audits=new Map(v310Audit.coverage_audit.map(a=>[a.overview_id,a]));
  check(audits.size===19,'duplicate audit ID');
  const rows=new Map(x.entries.map(r=>[r.overview_id,r]));
  const priorScope=[...rows.values()].filter(r=>['PARTIAL_COVERAGE','BACKGROUND_ONLY'].includes(r.mapping_status));
  check(priorScope.length===19&&priorScope.every(r=>audits.has(r.overview_id)),'not all 19 limited overview entries audited');
  for(const r of priorScope){
    const a=audits.get(r.overview_id);
    check(a.title===r.title&&a.previous_status===r.mapping_status,'audit identity/status '+r.overview_id);
    check(JSON.stringify(a.current_primary_reader_ids)===JSON.stringify(r.reader_links.filter(l=>l.role==='PRIMARY').map(l=>l.reader_id)),
      'audit primary target drift '+r.overview_id);
    check(a.expert_reviewed===false&&a.original_witness_collated===false&&a.remaining_limit&&a.followup,
      'false source-verification promotion '+r.overview_id);
  }
  const idx=new Map(b.readers.map(r=>[r.id,r]));
  const changed=new Set();
  for(const p of v310Audit.navigation_patches){
    check(!changed.has(p.id),'duplicate patch target');changed.add(p.id);
    const r=rows.get(p.id);
    check(r&&r.title===p.overview_title&&r.mapping_status===p.previous_status,'overview patch identity '+p.id);
    check(p.targets?.length>0,'empty patch '+p.id);
    if(p.new_status){
      check(p.id==='TOP-08'&&r.mapping_status==='BACKGROUND_ONLY'&&p.new_status==='PARTIAL_COVERAGE',
        'unreviewed status promotion '+p.id);
      r.mapping_status=p.new_status;
    }
    check(p.scope?.trim(),'missing scoped interpretation '+p.id);
    r.scope=p.scope;
    const oldIds=new Set(r.reader_links.map(l=>l.reader_id));
    const newEntries=[];
    for(const t of p.targets){
      const reader=idx.get(t.reader_id);
      check(reader&&reader.title===t.title,'unknown or changed reader '+t.reader_id);
      check(!oldIds.has(t.reader_id),'duplicate historical link '+p.id+'/'+t.reader_id);
      check(['PRIMARY','FOLLOWUP'].includes(t.role),'unsupported role '+t.role);
      oldIds.add(t.reader_id);
      newEntries.push({reader_id:t.reader_id,title:reader.title,role:t.role});
    }
    r.reader_links=[...newEntries,...r.reader_links];
  }
  check(changed.size===10,'wrong patch count');
  const totals={DIRECT_TOPIC:0,PARTIAL_COVERAGE:0,BACKGROUND_ONLY:0,NO_MATCH:0};
  for(const r of x.entries){
    check(Object.hasOwn(totals,r.mapping_status),'unknown status');
    totals[r.mapping_status]++;
    check(r.reader_links.every(l=>idx.has(l.reader_id)&&idx.get(l.reader_id).title===l.title),
      'broken target: '+r.overview_id);
  }
  check(totals.DIRECT_TOPIC===78&&totals.PARTIAL_COVERAGE===19&&totals.BACKGROUND_ONLY===0&&totals.NO_MATCH===0,
    'quality coverage mismatch');
  check(rows.get('TOP-08').reader_links.filter(l=>l.role==='PRIMARY').length===3,'TOP-08 still lacks primary guidance');
  check(v310Audit.source_reading_dossiers.every(d=>
    d.source_url.startsWith('https://')&&d.verification_boundary&&d.inspected_representation&&
    d.facts?.length>=2&&d.overview_ids.every(id=>rows.has(id))&&
    d.reader_ids.every(id=>idx.has(id))),'source reading dossier missing information');
  const ids=new Set(v310Audit.source_reading_dossiers.map(d=>d.id));
  check(ids.size===6,'duplicate dossier ID');
  b.version='3.10';b.kind='EDITORIAL_SCOPED_513_MEDIUM_DELIVERY';
  b.editorial_note+=' / V3.10 제한적 해설 19건의 품질심사와 개요 읽기 연결10건. 본문·원전 확인·선택 주장 검증 상태는 변경하지 않는다.';
  b.source_reading_dossiers_v310=structuredClone(v310Audit.source_reading_dossiers);
  b.editorial_audit.v310_quality_review={
    scope:v310Audit.scope,reviewed_overview_ids:[...audits.keys()],
    revised_overview_ids:[...changed],
    notes_added:6,readers_rewritten:0,sources_rewritten:0,
    expert_approved:false,original_witness_collated:false,published:false
  };
  x.version='3.10';
  x.metrics={...x.metrics,direct_topic:78,partial_coverage:19,background_only:0,no_match:0,default_readable:97,
    reading_links:x.entries.reduce((n,r)=>n+r.reader_links.length,0),
    unique_readers:new Set(x.entries.flatMap(r=>r.reader_links.map(l=>l.reader_id))).size};
  x.quality_audit={version:'3.10',audited_limited_overviews:19,patched_overviews:10,source_reading_dossiers:6,
    expert_approved:false,scope:'Navigation and source reading notes, not full historical review or live-app integration'};
  check(b.readers.length===513&&b.sources.length===723,'mutable content counts');
  check(JSON.stringify(b.readers)===JSON.stringify(prior.delivery.readers),'reader body drift');
  check(JSON.stringify(b.sources)===JSON.stringify(prior.delivery.sources),'source URL or status drift');
  check(JSON.stringify(b.source_verification)===JSON.stringify(prior.delivery.source_verification),'claim drift');
  check(JSON.stringify(x.entries.map(r=>r.overview_record))===
    JSON.stringify(prior.crosswalk.entries.map(r=>r.overview_record)),'overview source record drift');
  check(Object.values(b.publication_gate).every(v=>v===false)&&Object.values(x.publication_gate).every(v=>v===false),
    'publication gate revoked');
  return {delivery:b,crosswalk:x};
}
