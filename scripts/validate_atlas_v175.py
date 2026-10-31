import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/deep/atlas_v175_three_edition_readers.json').read_text())
works=json.loads((r/'data/contracts/atlas_v161_edition_comparison_cards.json').read_text())['works']
ids={e['id'] for w in works for e in w['editions']}
assert d['status']=='EDITORIAL_HOLD' and len(d['chapters'])==3
assert len({x['key'] for x in d['chapters']})==3
for x in d['chapters']:
 assert len(x['sections'])==7 and all(s['heading'] and s['text'] for s in x['sections'])
 assert sum(len(s['text']) for s in x['sections'])==x['body_chars']
 assert x['body_chars']>=1600
 assert set(x['editions'])<=ids and len(x['sources'])>=3
 assert all(u.startswith('https://') for u in x['sources'])
 assert x['can_publish'] is False and x['original_facsimile_collated'] is False and x['peer_reviewed'] is False
print('PASS V175',[(x['key'],x['body_chars']) for x in d['chapters']])
