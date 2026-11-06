/** V3.11: attach scoped source-critical addenda to the 513-reader editorial preview.
 * Does NOT upgrade source verification, invent primary witness collation, or change publication status.
 */
import {assembleV310} from '../medium-atlas-v310/overlay.mjs';
const check=(condition,message)=>{if(!condition)throw Error('V311: '+message);};
const layers=new Set([
  'REPRINTED_ENGLISH_TRANSLATION',
  'CURATED_ENGLISH_TRANSLATED_EXCERPTS',
  'TRANSCRIPTION_OF_HISTORICAL_ENGLISH_SECOND_EDITION',
  'DENOMINATIONAL_MODERN_EXPLANATION',
  'HISTORICAL_PRINT_BIBLIOGRAPHIC_METADATA',
  'INSTITUTIONAL_MODERN_HISTORY',
  'INSTITUTIONAL_HISTORICAL_FORMULA_COMPARISON',
  'INSTITUTIONAL_REPRINT_OF_2002_RETROSPECTIVE',
  'PRIMARY_REPORT_CATALOGUE_METADATA_ONLY',
]);
const evidenceLevels=new Set([
  'TRANSLATED_PRIMARY_PASSAGE_SEEN',
  'CURATED_TRANSLATED_PRIMARY_EXCERPT_SEEN',
  'HISTORICAL_TRANSCRIPTION_SEEN',
  'MODERN_INSTITUTIONAL_HISTORY_SEEN',
  'MODERN_INSTITUTIONAL_FORMULA_COMPARISON_SEEN',
  'RETROSPECTIVE_SOURCE_SEEN_NOT_VOTE_ORIGINAL',
]);
export function assembleV311(inputs,priorLinkAudit,priorQuality,additions){
  const {delivery,crosswalk}=assembleV310(inputs,priorLinkAudit,priorQuality);
  check(additions?.version==='3.11'&&additions.status==='DRAFT'&&additions.depth==='MEDIUM','unsupported research addendum');
  check(additions.publishing_gate&&Object.values(additions.publishing_gate).every(v=>v===false),'research publication HOLD');
  check(delivery.publication_gate&&Object.values(delivery.publication_gate).every(v=>v===false),'delivery publication HOLD');
  const m=additions.metrics;
  check(m?.research_addenda===4&&m.sections===12&&m.claim_cards===12&&m.new_source_records===10&&m.prior_readers_preserved===513&&m.prior_sources_preserved===723&&m.prior_selected_claims_preserved===22&&m.new_original_language_collations===0&&m.webapp_updated===false,'scope metrics mismatch');
  const readerIds=new Set(delivery.readers.map(r=>r.id));
  const overviewIds=new Set(crosswalk.entries.map(r=>r.overview_id));
  const srcs=new Map(), annexes=new Map(), claimIds=new Set();
  check(delivery.readers.length===513&&delivery.sources.length===723&&delivery.source_verification.selected_claims.length===22&&crosswalk.entries.length===97,'frozen corpus mismatch');
  check(additions.source_records?.length===10&&additions.addenda?.length===4&&additions.claim_cards?.length===12,'incomplete addenda');
  for(const s of additions.source_records){
    check(s.id&&!srcs.has(s.id)&&s.title&&s.url?.startsWith('https://')&&layers.has(s.layer),'invalid or duplicated source '+s.id);
    check(s.inspected&&s.not_done&&s.locator,'unqualified source inspection '+s.id);
    srcs.set(s.id,s);
  }
  for(const a of additions.addenda){
    check(a.id&&!annexes.has(a.id)&&a.title&&a.lead&&a.research_question?.endsWith('?'),'invalid annex '+a.id);
    check(a.sections?.length===3&&a.sections.every(sec=>sec.heading&&sec.body?.length>=240),'missing middle-depth prose '+a.id);
    check(a.anchor_reader_ids?.length&&a.anchor_reader_ids.every(id=>readerIds.has(id)),'unresolved historical reader '+a.id);
    check(a.overview_ids?.length&&a.overview_ids.every(id=>overviewIds.has(id)),'unresolved overview id '+a.id);
    check(a.source_ids?.length&&a.source_ids.every(id=>srcs.has(id)),'unsupported source id '+a.id);
    annexes.set(a.id,a);
  }
  let characters=0;
  for(const a of additions.addenda)for(const sec of a.sections)characters+=sec.body.length;
  check(characters===m.new_body_characters,'character count mismatch');
  for(const c of additions.claim_cards){
    const annex=annexes.get(c.addendum_id);
    check(c.id&&!claimIds.has(c.id)&&annex&&Number.isInteger(c.section_index)&&c.section_index>=0&&c.section_index<3,'bad claim reference '+c.id);
    claimIds.add(c.id);
    check(annex.source_ids.includes(c.source_id)&&c.statement?.length>=20&&c.locator&&c.misinterpretation_guard&&evidenceLevels.has(c.evidence_level),'claim source or locator mismatch '+c.id);
    check(c.original_witness_collated===false&&c.historian_approved===false,'invalid claim approval '+c.id);
    if(c.evidence_level==='RETROSPECTIVE_SOURCE_SEEN_NOT_VOTE_ORIGINAL')check(c.source_id==='WCC-2002','unverified vote source');
  }
  check(claimIds.size===12&&annexes.size===4&&srcs.size===10,'duplicate provenance identity');
  check(additions.claim_cards.every(c=>c.statement&&!c.statement.includes('<script')),'claim unsafe');
  const oldSourceState=JSON.stringify(delivery.sources);
  const oldReaderState=JSON.stringify(delivery.readers);
  const oldClaimState=JSON.stringify(delivery.source_verification);
  delivery.version='3.11';
  delivery.kind='SOURCE_CRITICAL_513_MEDIUM_EDITORIAL_PREVIEW';
  delivery.primary_passage_addenda=structuredClone(additions.addenda);
  delivery.primary_passage_claims=structuredClone(additions.claim_cards);
  delivery.primary_passage_source_records=structuredClone(additions.source_records);
  delivery.editorial_audit.v311_source_critical={
    scope:'4 scoped mid-depth source readings; passages in translated transcripts and modern institutional history, not original-language manuscript collation',
    addendum_count:4,sections:12,new_body_characters:characters,claim_cards:12,source_records:10,
    prior_513_readers_unchanged:true,prior_723_sources_unchanged:true,expert_approved:false,original_language_collated:false,app_updated:false,
  };
  delivery.editorial_note+=' / V3.11 지정 문헌의 번역 전사·학술 발췌·현대 해설을 구별하는 연구 부록 4편을 별도 보관.';
  check(JSON.stringify(delivery.sources)===oldSourceState&&JSON.stringify(delivery.readers)===oldReaderState&&JSON.stringify(delivery.source_verification)===oldClaimState,'frozen manuscript/source/claim drift');
  check(Object.values(delivery.publication_gate).every(v=>v===false)&&Object.values(crosswalk.publication_gate).every(v=>v===false),'publication status changed');
  const getAddendaForReader=(readerId)=>{
    check(readerIds.has(readerId),'unknown reader '+readerId);
    return structuredClone(additions.addenda.filter(a=>a.anchor_reader_ids.includes(readerId)).map(a=>({
      ...a,source_records:a.source_ids.map(id=>srcs.get(id)),claims:additions.claim_cards.filter(c=>c.addendum_id===a.id)
    })));
  };
  return {delivery,crosswalk,getAddendaForReader};
}
