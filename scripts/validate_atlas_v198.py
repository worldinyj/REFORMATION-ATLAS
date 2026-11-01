import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]
d=json.loads((p/'data/contracts/atlas_v198_primary_scan_access_register.json').read_text())
assert d['publish'] is False and d['main_untouched'] and d['ai_studio_untouched']
assert {s['id'] for s in d['sources']}=={'CAL1539','CAL1559','CAL_CRITICAL','MAR1883'}
assert all(s['url'].startswith('https://') and s['images_verified'] is False for s in d['sources'])
assert len(d['comparative_workflow'])==4 and all(x['done'] is False for x in d['comparative_workflow'])
assert '545' in d['sources'][1]['access_observation']
print('PASS V198: source access and image read status accurately distinguished')
