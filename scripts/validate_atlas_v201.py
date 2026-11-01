import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
old=json.loads((root/'data/deep/atlas_v178_ten_readers_standardized.json').read_text())
new=json.loads((root/'data/deep/atlas_v201_three_p0_revised_readers.json').read_text())
assert new['publication_gate']=={'can_ship':False,'scholarly_approval':False}
assert {x['key'] for x in new['chapters']}=={'MARBURG','AUGSBURG','CALVIN1559'}
originals={x['key']:x for x in old['chapters']}
for n in new['chapters']:
 p=originals[n['key']]
 assert n['body'].startswith(p['body']+'\n\n')
 assert n['previous_body_chars_no_whitespace']==len(re.sub(r'\s','',p['body']))
 assert len(re.sub(r'\s','',n['body']))>n['previous_body_chars_no_whitespace']+350
 assert 'https://' in n['body']
 assert '미완료' in n['body']
 assert n['added_review']=='PENDING'
print('PASS V201: 3 historical reader bodies expanded, V178 text preserved, URLs and non-publication gates retained')
