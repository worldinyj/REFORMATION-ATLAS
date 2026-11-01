import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/contracts/atlas_v189_augustana_article_iv_two_editorial_texts.json').read_text())
assert d['ship'] is False and len(d['sources'])==2
assert {x['edition_id'] for x in d['editions']}=={'EDN-V161-AC-1530','EDN-V161-AC-1540'}
assert all(s['url'].startswith('https://') and s['tier'] and not s['first_print_collated'] for s in d['sources'])
assert all(len(x['units'])==3 and not x['original_print_checked'] for x in d['editions'])
assert all(u['latin_excerpt'] and u['meaning'] for x in d['editions'] for u in x['units'])
assert all(d['quality_gate'].values())
assert any(c['status']=='NOT_PROVEN' for c in d['conclusions'])
print('PASS V189: two source-classified editorial texts; six excerpt units; no first-imprint claims')
