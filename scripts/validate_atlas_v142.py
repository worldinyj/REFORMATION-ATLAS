#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'data/contracts/atlas_v142_crossfile_identity_audit.json').read_text(encoding='utf-8'))
assert d['publication_gate']=={'approved':False,'can_ship':False}
assert d['repository_inventory']['tracked_json_under_data']==94
assert d['repository_inventory']['files_content_inspected']==len(d['files_examined'])==6
assert len(d['findings'])==4
assert all((R/p).exists() for p in d['files_examined'])
print('PASS V1.42: scoped repository inventory and identity findings')
