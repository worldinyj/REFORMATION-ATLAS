import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'data/contracts/atlas_v185_editorial_text_comparison.json').read_text())
assert d['publication_gate']=={'can_ship':False,'original_16c_witness_collated':False,'scholarly_approved':False}
assert len(d['comparisons'])==4
a=next(x for x in d['comparisons'] if x['id']=='AC-X-1530-1540')
assert {x['kind'] for x in a['changes']}=={'VERB_CHANGE','QUALIFICATION_ADDED','CLAUSE_OMITTED'}
assert all(x['text_level']=='EXCERPT_FROM_LATER_EDITORIAL_SOURCE' for x in a['witnesses'])
b=next(x for x in d['comparisons'] if x['id']=='AC-IV-1530-1540')
assert all(x['full_latin_transcript'] is None for x in b['witnesses'])
m=next(x for x in d['comparisons'] if x['id']=='MAR-XV-1529')
assert all(x['article_15_addendum_text'] is None for x in m['witnesses'])
cal=next(x for x in d['comparisons'] if x['id']=='CAL-1536-1559')
assert cal['paragraph_alignments']==[]
assert all(all(u.startswith('https://') for u in x['source_urls']) for x in d['comparisons'])
print('PASS V185: edited textual fragments and omissions recorded, no invented original readings')
