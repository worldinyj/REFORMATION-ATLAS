from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]
a=json.loads((r/'data/deep/atlas_v171_ten_research_chapters.json').read_text())
b=json.loads((r/'data/deep/atlas_v171_reader_seven_section_drafts.json').read_text())
old=json.loads((r/'data/deep/atlas_v156_extended_narratives.json').read_text())
assert len(a['chapters'])==len(b['chapters'])==len(old['pages'])==10
assert all(c['publication_gate']=='RESEARCH_HOLD' and not c['verified_firsthand'] for c in a['chapters'])
assert all(len(c['sections'])==7 and not c['primary_collated'] and c['review']=='PENDING' for c in b['chapters'])
assert {c['source_id'] for c in a['chapters']}=={c['id'] for c in old['pages']}
assert {c['predecessor'] for c in b['chapters']}=={c['id'] for c in old['pages']}
lengths=[sum(len(s['text']) for s in c['sections']) for c in b['chapters']]
print('PASS V171: 10 research essay outlines, 10 seven-section reading drafts, 70 sections, all editorially gated')
print('Seven-section body characters: min',min(lengths),'max',max(lengths),'avg',round(sum(lengths)/10,1))
