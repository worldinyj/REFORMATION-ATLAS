#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/contracts/atlas_v160_document_facsimile_review.json').read_text(encoding='utf8'))
assert d['publication_gate']=={'approved':False,'can_ship':False}
assert len(d['facsimiles'])==4
assert len(d['portrait_card_spec']['records'])==5
assert all(not x['image_approved'] and not x['original_page_collated'] for x in d['facsimiles'])
assert all(x['catalog_url'].startswith('https://') and x['scope'] for x in d['facsimiles'])
assert d['facsimiles'][0]['shelfmark']=='BRA2651/A-B'
print('PASS V1.60: 5 portrait card labels, 4 facsimile records, rights gates retained')
