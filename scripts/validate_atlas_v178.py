import json,re
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/deep/atlas_v178_ten_readers_standardized.json').read_text())
base=json.loads((r/'data/deep/atlas_v177_unified_ten_reader_drafts.json').read_text())
assert len(d['chapters'])==len(base['chapters'])==10
assert {x['key'] for x in d['chapters']}=={x['key'] for x in base['chapters']}
assert d['publication_gate']['can_ship'] is False
for x in d['chapters']:
 assert x['body_chars_no_whitespace']==len(re.sub(r'\s','',x['body']))
 assert x['body_chars_no_whitespace']>=2000,x['key']
 assert x['source_urls'] and all(u.startswith('https://') for u in x['source_urls'])
 assert x['primary_original_collated'] is False and x['peer_reviewed'] is False and x['can_publish'] is False
print('PASS V178: ten >2000 nonwhitespace-character research drafts with publication gate closed')
print([(x['key'],x['body_chars_no_whitespace']) for x in d['chapters']])
