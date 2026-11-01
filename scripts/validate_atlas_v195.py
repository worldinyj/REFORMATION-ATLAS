import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'data/contracts/atlas_v195_calvin_iii_actual_apparatus_variants.json').read_text())
assert all(v is False for v in d['release'].values())
assert [x['locus'] for x in d['variants']]==['III.6','III.7','III.10']
assert all(x['verification']=='DIRECTLY_READ_ONLINE_APPARATUS' for x in d['variants'])
assert all(x['semantic_inference']=='UNASSESSED' for x in d['variants'])
assert all('1539-54' in x['reading'] and x['source'].startswith('https://') for x in d['variants'])
assert d['chapters_unchecked']==['III.8','III.9']
assert d['marburg_status']['exact_additions_transcribed'] is False
print('PASS V195: three real editorial apparatus notes, no false unique-1539 or original-print claims')
