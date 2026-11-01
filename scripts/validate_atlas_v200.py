import json,re
from pathlib import Path
r=Path(__file__).resolve().parents[1]
a=json.loads((r/'data/contracts/atlas_v200_ten_reader_quality_audit.json').read_text())
b=json.loads((r/'data/deep/atlas_v178_ten_readers_standardized.json').read_text())
e=json.loads((r/'data/contracts/atlas_v179_ten_reader_claim_evidence.json').read_text())
assert a['publication_gate']=={'can_ship':False,'expert_reviewed':False,'originals_collated':False}
assert len(a['reader_audits'])==len(b['chapters'])==len(e['claims'])==10
assert a['totals']['characters_no_whitespace']==sum(len(re.sub(r'\s','',x['body'])) for x in b['chapters'])
assert a['totals']['min_chars']==min(len(re.sub(r'\s','',x['body'])) for x in b['chapters'])
m={x['key']:x for x in a['reader_audits']}
for x in b['chapters']:
 y=m[x['key']]
 assert y['metrics']['heading_count']==len(re.findall(r'^### ',x['body'],re.M))
 assert y['metrics']['body_length_threshold']==(len(re.sub(r'\s','',x['body']))>=2000)
assert sum(x['priority']=='P0' for x in a['reader_audits'])==3
assert set(k for k,v in m.items() if v['priority']=='P0')=={'MARBURG','AUGSBURG','CALVIN1559'}
assert a['totals']['human_review_pending']==10 and a['totals']['original_folio_checked']==0
print('PASS V200: 10 real reader bodies audited, priority and all metrics reproducible')
