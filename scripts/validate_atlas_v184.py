import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'data/contracts/atlas_v184_witness_collation_workpack.json').read_text())
assert d['release']=={'can_ship':False,'scholarly_approved':False,'original_collation_complete':False}
assert len(d['comparisons'])==5
assert {x['id'] for x in d['comparisons']}=={'AC-IV','AC-X','AC-ORDER','MAR-ZK','CAL-TRANSITION'}
assert all(x['source'].startswith('https://') and x['witnesses'] for x in d['comparisons'])
assert all(d['quality_rules'].values())
assert all(w['text_transcribed'] is None for x in d['comparisons'] for w in x['witnesses'] if 'text_transcribed' in w)
mar=next(x for x in d['comparisons'] if x['id']=='MAR-ZK')
assert all(w['addition_transcribed'] is None for w in mar['witnesses'])
assert len(mar['critical_editions'])==3
cal=next(x for x in d['comparisons'] if x['id']=='CAL-TRANSITION')
assert [w['edition'] for w in cal['witnesses']]==['1536','1539','1543','1550','1559']
assert all(w['alignment_to_1559'] is None for w in cal['witnesses'][:-1])
print('PASS V184 five witness-oriented comparisons; unknown texts and scholarly gates held')
