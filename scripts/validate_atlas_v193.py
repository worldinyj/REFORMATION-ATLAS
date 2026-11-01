import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'data/contracts/atlas_v193_marburg_calvin_evidence_crosswalk.json').read_text())
assert all(v is False for v in d['publication'].values())
assert [r['article'] for r in d['marburg']['articles']]==[7,13,15]
assert all(r['exact_diplomatic_reading'] is None and r['translation_ko'] is None for r in d['marburg']['articles'])
assert len(d['marburg']['critical_edition_targets'])==3
assert '1883' in d['marburg']['facsimile_citation']
assert [r['to'] for r in d['calvin']['thematic_crosswalk']]==['III.6','III.7','III.8','III.9','III.10']
assert all(r['alignment']=='THEMATIC_EDITORIAL' for r in d['calvin']['thematic_crosswalk'])
assert d['calvin']['paragraph_level_1539_to_1559_verified'] is False
print('PASS V193: archival metadata vs uncollated readings, Calvin thematic crosswalk without false paragraph equivalence')
