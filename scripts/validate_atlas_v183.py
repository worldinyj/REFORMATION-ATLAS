import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/contracts/atlas_v183_critical_edition_findings.json').read_text())
assert d['release']=={'can_publish':False,'original_witness_collated':False,'peer_reviewed':False}
assert len(d['findings'])==4
ids={x['id'] for x in d['findings']}
assert ids=={'AC-ORDER','AC-IV-X','MAR-ZK','CALVIN-EDITIONS'}
assert all(x['source_class'] and x['source'].startswith('https://') and x['implication'] for x in d['findings'] if 'source' in x)
assert all(x['original_folio_checked'] is False for x in d['findings'])
order=next(x for x in d['findings'] if x['id']=='AC-ORDER')['locations']
assert [x['article'] for x in order]==['XI','XII','XII','XI']
mar=next(x for x in d['findings'] if x['id']=='MAR-ZK')
assert mar['locations'][0]['articles']==['7','13','15']
assert len(mar['edition_leads'])>=3
cal=next(x for x in d['findings'] if x['id']=='CALVIN-EDITIONS')
assert [x['year'] for x in cal['locations']]==[1536,1539,1543,1550,1559,1562]
print('PASS V183: topic-corrected Augsburg correspondence, Z/K archival locators, Calvin intermediate timeline')
