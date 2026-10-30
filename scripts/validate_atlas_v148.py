#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/deep/atlas_v148_ecclesia_critical_leads.json').read_text(encoding='utf-8'))
assert d['publication_gate']=={'approved':False,'can_ship':False}
assert len(d['work_ids'])==2
assert {x['page_line'] for x in d['wycliffe_textual_leads']}=={'257/1','467/29'}
assert all(x['primary_copy_checked'] is False for x in d['wycliffe_textual_leads'])
assert d['hus_metadata']['manuscript_collated'] is False
print('PASS V1.48 metadata, leads and gate')
