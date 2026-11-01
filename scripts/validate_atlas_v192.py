import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/contracts/atlas_v192_marburg_calvin_substantive_links.json').read_text())
assert all(x is False for x in d['publish_gate'].values())
assert len(d['research'])==4
assert all(x['sources'] and all(u.startswith('https://') for u in x['sources']) for x in d['research'])
mar=next(x for x in d['research'] if x['id']=='MAR-Z-7')
assert mar['exact_german_added_text'] is None
assert len(mar['other_Z_additions'])==2 and all(v['text'] is None for v in mar['other_Z_additions'])
cal=next(x for x in d['research'] if x['id']=='CAL-LIFE')
assert [x['locator'] for x in cal['final_five_chapters']]==['III.6','III.7','III.8','III.9','III.10']
assert cal['direct_paragraph_collation'] is False
assert all(d['qa_policy'].values())
print('PASS V192: Marburg Z/K witness limits and Calvin 1539-to-1559 thematic alignment')
