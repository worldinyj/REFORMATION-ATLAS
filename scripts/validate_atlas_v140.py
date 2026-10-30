#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
a=json.loads((R/'data/contracts/atlas_v140_expanded_reform_network.json').read_text(encoding='utf8'))
assert a['publication_gate']=={'approved':False,'can_ship':False}
ids={x['id'] for x in a['nodes']}
assert len(ids)==len(a['nodes'])==25
assert len(a['edges'])==24
assert all(x['from'] in ids and x['to'] in ids for x in a['edges'])
assert a['correction']['correct_person']=='OV-P-010'
assert not any(x['from']=='OV-P-009' and x['to']=='OV-D-005' for x in a['edges'])
print('PASS V1.40: 25 nodes / 24 relations / Hus attribution corrected')
