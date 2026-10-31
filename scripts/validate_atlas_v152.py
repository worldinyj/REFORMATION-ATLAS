#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/deep/atlas_v152_alternative_access_review.json').read_text(encoding='utf8'))
assert d['publication_gate']=={'approved':False,'can_ship':False}
assert len(d['confirmed_access'])==5
assert all(not x['page_images_read'] for x in d['confirmed_access'])
assert {x['page'] for x in d['priority_pages']}=={257,467}
assert not d['loserth_introduction']['read']
assert not d['loserth_introduction']['shelfmarks_confirmed']
print('PASS V1.52 metadata access / no direct facsimile')
