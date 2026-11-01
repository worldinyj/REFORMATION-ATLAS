import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/contracts/atlas_v194_calvin_primary_witness_and_apparatus.json').read_text())
assert all(v is False for v in d['release'].values())
n=d['calvin']['first_print_1539']
assert n['year']==1539 and n['shelfmark']=='VAULT folio Case 6A 224'
assert n['page_images_directly_read'] is False
c=d['calvin']['critical_apparatus']
assert len(c['evidence_examples'])==2
assert all(v['url'].startswith('https://') for v in c['evidence_examples'])
assert d['calvin']['direct_paragraph_alignment_completed'] is False
assert not d['marburg']['facsimile_pages_directly_read']
assert not d['marburg']['additions_7_13_15_transcribed']
print('PASS V194: real 1539 holding, digital critical apparatus, no original/Marburg false attestations')
