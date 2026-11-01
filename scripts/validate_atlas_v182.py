from pathlib import Path
import json
p=Path(__file__).resolve().parents[1]
d=json.loads((p/'data/contracts/atlas_v182_variant_transmission_research.json').read_text())
assert d['can_ship'] is False and d['original_witness_collated'] is False
assert len(d['findings'])==5
assert len(d['calvin_timeline'])==6
assert [x['edition'] for x in d['calvin_timeline']]==['1536 Latin','1539 Latin','1543 Latin','1550 Latin','1559 Latin','1560 French']
assert [x['chapters'] for x in d['calvin_timeline']][:3]==[6,17,21]
assert d['calvin_timeline'][4]['chapters']==80
assert all(x['original_witness_verified'] is False and x['editorial_review']=='PENDING' for x in d['findings'])
assert all(x['source'].startswith('https://') and x['finding'] for x in d['findings'])
assert all(x['direct_text_alignment_verified'] is False for x in d['calvin_timeline'])
print('PASS V182: 5 findings + 6 edition stages; original collation and publication gated')
