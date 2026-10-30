#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'data/deep/atlas_v146_two_de_ecclesia_works.json').read_text(encoding='utf8'))
assert d['publication_gate']=={'approved':False,'can_ship':False}
assert len(d['works'])==2
assert {w['author_id'] for w in d['works']}=={'OV-P-009','OV-P-010'}
assert d['works'][0]['id']!=d['works'][1]['id']
assert d['relationship']['type']=='INTELLECTUAL_INFLUENCE_NOT_SAME_TEXT'
assert all(not w.get('original_manuscript_collated',False) for w in d['works'])
print('PASS V1.46 independent works and manuscript publication hold')
