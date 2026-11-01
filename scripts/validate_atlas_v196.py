import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/contracts/atlas_v196_calvin_book3_five_chapter_apparatus.json').read_text())
assert d['can_publish'] is False and d['original_1539_print_collated'] is False
assert [c['chapter'] for c in d['chapters']]==['III.6','III.7','III.8','III.9','III.10']
assert all(c['url'].startswith('https://') for c in d['chapters'])
assert [c['chapter'] for c in d['chapters'] if c['verification']=='DIRECT_ONLINE_APPARATUS']==['III.8','III.9']
assert 'concutimur' in d['chapters'][2]['examples'][1]['note']
assert all('1539-54' in x['note'] for x in d['chapters'][3]['examples'])
assert d['marburg']['exact_german_text'] is None
print('PASS V196: five chapter coverage; directly checked III.8/9; publication and witness holds')
