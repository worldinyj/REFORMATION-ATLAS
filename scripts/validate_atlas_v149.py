#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'data/deep/atlas_v149_wyclif_1886_access_audit.json').read_text(encoding='utf-8'))
assert d['publication_gate']=={'approved':False,'can_ship':False}
assert len(d['textual_probes'])==2
assert {(x['edition_page'],x['line']) for x in d['textual_probes']}=={(257,1),(467,29)}
assert all(x['direct_images_checked'] is False for x in d['textual_probes'])
assert d['manuscript_shelfmarks']['three_complete_wyclif_manuscripts']==[]
print('PASS V1.49 catalogued access, 2 unresolved collation targets, publication hold')
