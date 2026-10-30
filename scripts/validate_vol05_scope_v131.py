#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
a=json.loads((R/'data/deep/atlas_v131_vol05_scope_audit.json').read_text(encoding='utf-8'))
assert a['publication_gate']=={'approved':False,'can_ship':False}
assert a['vol05']['people_ids']==['OV-P-021','OV-P-022']
assert a['vol04_bridge']['person_ids']==['OV-P-015','OV-P-017']
for p in a['vol05']['research_files']+a['vol04_bridge']['research_files']:
 assert (R/p).is_file(),p
print('PASS: V1.31 actual files, volume boundary, nonpublic status')
