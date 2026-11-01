import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def get(n): return json.loads((R/'data/deep'/n).read_text())
old=get('atlas_v178_ten_readers_standardized.json')
p0=get('atlas_v201_three_p0_revised_readers.json')
p1=get('atlas_v202_seven_p1_revised_readers.json')
all_=get('atlas_v202_unified_ten_revised_readers.json')
assert len(p0['chapters'])==3 and len(p1['chapters'])==7 and len(all_['chapters'])==10
assert all(v is False for v in all_['publication_gate'].values())
baseline={x['key']:x for x in old['chapters']}
bykey={x['key']:x for x in p0['chapters']+p1['chapters']}
assert len(bykey)==10
for x in all_['chapters']:
 assert x['body']==bykey[x['key']]['body']
 assert x['body'].startswith(baseline[x['key']]['body']+'\n\n')
 assert x['review_status']=='PENDING'
 assert 'https://' in x['body'] and '미완료' in x['body']
 assert len(re.sub(r'\s','',x['body']))>len(re.sub(r'\s','',baseline[x['key']]['body']))
assert sum(len(re.sub(r'\s','',x['body'])) for x in all_['chapters'])==25404
print('PASS V202: seven newly revised readers, ten unified, original prose preserved, research publication blocked')
