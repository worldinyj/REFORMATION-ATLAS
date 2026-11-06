/** A single, explicit source-link corrigendum. No historical claims are promoted. */
import {assembleV308} from '../medium-atlas-v308/assemble.mjs';
const check=(x,m)=>{if(!x)throw Error('V309 evidence overlay: '+m);};
export function assembleV309(inputs,audit) {
 const {delivery,crosswalk}=assembleV308(...inputs);
 check(audit?.version==='3.09'&&audit?.status==='DRAFT'&&audit.link_corrections?.length===1,'audit contract');
 check(audit.publication_gate&&Object.values(audit.publication_gate).every(v=>v===false),'audit HOLD missing');
 check(delivery.publication_gate&&Object.values(delivery.publication_gate).every(v=>v===false),'bundle HOLD missing');
 const correction=audit.link_corrections[0],source=delivery.sources.find(s=>s.id===correction.source_id);
 check(correction.source_id==='V307-S08'&&source&&source.url===correction.original_url,'unexpected original source link');
 check(correction.action==='REPLACE_LINK_ONLY'&&correction.checked_on==='2026-11-06','unsupported correction type');
 check(correction.replacement_url==='https://www.bskorea.or.kr/bbs/content.php?co_id=subpage2_3_3_1_1','unreviewed corrected URL');
 check(correction.original_page_checked===false&&correction.material_reverified===false,'inaccurate source verification promotion');
 source.original_url=source.url;source.url=correction.replacement_url;
 source.link_correction={version:'3.09',status:'LINK_REPLACEMENT_VERIFIED',checked_on:correction.checked_on,
   evidence_level:correction.evidence_level,original_url:correction.original_url,
   reason:correction.reason,publication_effect:'NONE',historical_claim_validation:'NOT_CHANGED'};
 delivery.editorial_audit.v309_link_audit={scope:audit.scope,corrected_source_ids:[correction.source_id],
  findings:audit.findings.map(f=>({source_id:f.source_id,status:f.status,severity:f.severity})),
  bodies_changed:0,expert_approved:false};
 delivery.editorial_note += ' / V3.09 대한성서공회 링크 1건 정정. 본문·선택 주장·기관별 확인 범위 미변경.';
 check(crosswalk.entries.length===97&&delivery.readers.length===513&&delivery.sources.length===723,'counts changed');
 return {delivery,crosswalk};
}
