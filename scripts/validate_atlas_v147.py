#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'data/deep/atlas_v147_ecclesia_witness_catalog.json').read_text(encoding='utf8'))
assert d['publication_gate']=={'approved':False,'can_ship':False}
assert len(d['works'])==2
hus,wyclif=d['works']
assert hus['id']=='OV-D-005' and len(hus['witnesses'])==5
assert wyclif['id']=='WRK-V03-WYCLIFFE-DE-ECCLESIA' and len(wyclif['witnesses'])==1
assert all(x['level']=='CATALOG_METADATA_ONLY' for x in hus['witnesses'])
assert wyclif['witnesses'][0]['level']=='PRINTED_EDITION_CATALOG_ONLY'
print('PASS V1.47: distinct authors, five Hus manuscript references, one Wyclif printed witness')
