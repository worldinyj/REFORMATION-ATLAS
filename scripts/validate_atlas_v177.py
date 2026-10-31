import json,re
from pathlib import Path
p=Path(__file__).resolve().parents[1]
d=json.loads((p/'data/deep/atlas_v177_unified_ten_reader_drafts.json').read_text())
assert len(d['chapters'])==10
assert not d['publication_gate']['can_ship']
assert len({x['key'] for x in d['chapters']})==10
for x in d['chapters']:
 assert x['body_chars_no_whitespace']==len(re.sub(r'\s','',x['body']))
 assert x['source_urls'] and all(u.startswith('https://') for u in x['source_urls'])
 assert not x['can_publish'] and not x['primary_original_collated']
print('PASS V177 10 linked research readers')
print('UNMET 2000-character no-whitespace targets:',[(x['key'],x['body_chars_no_whitespace']) for x in d['chapters'] if x['body_chars_no_whitespace']<2000])
