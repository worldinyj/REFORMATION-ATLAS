import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
data=json.loads((r/'data/deep/atlas_v173_six_extended_chapters.json').read_text(encoding='utf8'))
v156=json.loads((r/'data/deep/atlas_v156_extended_narratives.json').read_text(encoding='utf8'))
assert data['gate']=={'approved':False,'can_ship':False}
ch=data['chapters'];assert len(ch)==6
assert len({x['key'] for x in ch})==6
assert all(x['source'] in {p['id'] for p in v156['pages']} for x in ch)
assert all(len(x['sections'])==4 and x['urls'] and not x['primary_original_collated'] for x in ch)
assert all(x['editorial_review']=='PENDING' for x in ch)
counts=[sum(len(s[1]) for s in x['sections']) for x in ch]
print('PASS V173: six linked four-section essays, gated review')
print('Character counts by essay:',dict(zip([x['key'] for x in ch],counts)))
print('Average',round(sum(counts)/len(counts),1),'min',min(counts),'max',max(counts))
