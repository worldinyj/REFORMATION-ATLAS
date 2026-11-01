import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/contracts/atlas_v188_article_iv_source_corroboration.json').read_text())
assert all(x is False for x in d['publication'].values())
assert len(d['claims'])==3 and len(d['sources'])==3
assert len({s['id'] for s in d['sources']})==3
assert all(s['url'].startswith('https://') for s in d['sources'])
assert 'not a witness-certified' in d['correction']['issue']
assert all(x['certainty'] and x['explanation'] for x in d['claims'])
assert len(d['next_readings'])==3 and len(d['cannot_claim'])==3
assert any('1531' in x for x in d['cannot_claim'])
print('PASS V188: three source tiers, corrected 1531 attribution, three substantive comparisons, no original imprint claims')
