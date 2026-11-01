import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/contracts/atlas_v187_article_iv_1531_1540_comparison.json').read_text())
assert d['can_ship'] is False and d['scholarly_approved'] is False
assert d['original_16c_folio_checked'] is False
assert len(d['witnesses'])==2 and len(d['collation_points'])>=3
assert all(x['source'].startswith('https://') for x in d['witnesses'])
assert all(x['full_text_collated_against_CR26_p275'] is False for x in d['witnesses'])
assert d['cr26_editorial_apparatus']['printed_page']==352
assert d['cr26_editorial_apparatus']['footnote']==5
print('PASS V187: tiered Article IV side-by-side and editorial footnote; first prints unverified')
