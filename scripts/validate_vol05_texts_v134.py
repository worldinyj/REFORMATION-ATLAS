#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/deep/atlas_v134_trent_spiritual_editions.json').read_text(encoding='utf8'))
assert d['publication_gate']=={'approved':False,'can_ship':False}
assert len(d['documents'])==4
assert {x['person_id'] for x in d['documents'] if 'person_id' in x}=={'OV-P-021','OV-P-022'}
assert d['documents'][0]['session']==6
assert d['documents'][1]['date']=='1548-07-31'
assert len(d['documents'][2]['edition_distinctions'])==5
assert d['documents'][3]['edition_collation_pending']
print('PASS V1.34: document structure and publication hold')
