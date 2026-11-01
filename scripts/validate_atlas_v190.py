import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'data/contracts/atlas_v190_augustana_iv_v_theological_continuity.json').read_text())
assert d['can_ship'] is False and d['original_print_collated'] is False
assert len(d['analysis'])==4
assert {x['id'] for x in d['analysis']}=={'IV-1531','V-1531','IV-1540','V-1540'}
assert all(x['evidence'] and x['logic'] for x in d['analysis'])
assert len(d['sources'])>=3 and all(x['url'].startswith('https://') for x in d['sources'])
assert all(d['quality_rules'].values())
assert 'p.275' in d['unverified'][0]
print('PASS V190: IV/V argument continuity with explicit historical evidence levels and publication gates')
