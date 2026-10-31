import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'data/deep/atlas_v174_marburg_source_anchored_reader.json').read_text())
p=json.loads((root/'data/deep/atlas_v156_extended_narratives.json').read_text())
assert d['source_id'] in {x['id'] for x in p['pages']}
assert d['status']=='RESEARCH_DRAFT_NOT_PUBLISHABLE'
assert d['can_publish'] is False and d['primary_folio_collation'] is False
assert d['scholarly_approved'] is False and d['rights_approved'] is False
assert len(d['sections'])==7
chars=sum(len(x['text']) for x in d['sections'])
assert chars>=2000, f'Expected >=2000 substantial characters, got {chars}'
assert len(d['evidence'])>=4 and all(x['url'].startswith('https://') for x in d['evidence'])
assert any(x.get('shelfmark')=='E I 3.1, Nr. 54' for x in d['evidence'])
print('PASS V174 substantive reader:',chars,'characters; 7 sections; 4 source records')
