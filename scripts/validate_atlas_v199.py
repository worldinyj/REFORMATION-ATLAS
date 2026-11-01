import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'data/contracts/atlas_v199_calvin_original_scan_evidence_gate.json').read_text())
assert d['can_ship'] is False and d['main_modified'] is False and d['ai_studio_modified'] is False
assert len(d['evidence'])==2
s=d['evidence'][0]
assert s['file_pages']==576 and s['file_size_bytes']>50_000_000
assert s['status']=='METADATA_CONFIRMED_IMAGE_NOT_READ'
assert s['folio_locator'] is None and s['verified_exact_reading'] is None
e=d['evidence'][1]
assert e['status']=='PASSAGE_AND_APPARATUS_ACCESSIBLE'
assert [r['word'] for r in e['critical_readings']]==['concutimur','continemur','contemnimur']
assert d['scientific_decisions'][0]['verdict']=='NOT_ESTABLISHED'
assert all(x['url'].startswith('https://') for x in d['evidence'])
print('PASS V199: original scan not falsely claimed, editorial apparatus provenance preserved')
