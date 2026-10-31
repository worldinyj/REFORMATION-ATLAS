#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/contracts/atlas_v163_source_evidence_cards.json').read_text(encoding='utf8'))
m=json.loads((r/'data/contracts/atlas_v162_edition_article_matrix.json').read_text(encoding='utf8'))
assert d['publication_gate']=={'approved':False,'can_ship':False}
assert len(d['cards'])==8
ids={x['id'] for x in m['rows']}
assert all(x['matrix_id'] in ids for x in d['cards'])
assert len({x['id'] for x in d['cards']})==8
assert all(x['source_urls'] and x['proof_level'] and x['unverified'] for x in d['cards'])
assert all(not x['primary_original_folio_checked'] and x['release']=='EDITORIAL_HOLD' for x in d['cards'])
print('PASS V1.63: 8 evidence cards, matrix IDs, sources and editorial holds')
