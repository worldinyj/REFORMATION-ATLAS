import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/contracts/atlas_v191_augustana_iv_v_x_connected_analysis.json').read_text())
assert d['release']=={'can_ship':False,'original_print_collated':False,'scholarly_reviewed':False}
assert {x['id'] for x in d['questions']}=={'IV','V','X'}
assert len(d['connections'])==3
assert len(d['reception_positions'])==2
assert all(x['source_url'].startswith('https://') and not x['original_folio_checked'] for x in d['questions'])
assert all(x['source_class'] and x['interpretation_risk'] for x in d['questions'])
assert any(x['classification']=='INTERPRETIVE_BRIDGE_NOT_EXPLICIT_ASSERTION' for x in d['connections'])
assert all(x['source_url'].startswith('https://') for x in d['reception_positions'])
print('PASS V191: IV/V/X continuity and variations; interpretation and publication gates closed')
