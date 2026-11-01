import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]
d=json.loads((p/'data/contracts/atlas_v186_article_iv_apparatus_comparison.json').read_text())
assert d['release']=={'can_ship':False,'original_16c_print_collated':False,'academic_approved':False}
assert len(d['comparisons'])==3
iv=d['comparisons'][0]
assert iv['id']=='AC-IV' and iv['location']['volume']==26
assert iv['verified']=='1858_EDITED_LATIN_PAGE_AND_APPARATUS'
assert iv['full_1531_text_collated'] is False
assert all(x['sixteenth_century_original_checked'] is False for x in d['comparisons'])
assert d['source'].startswith('https://')
print('PASS V186: source-located 1858 edited Latin quotation, 16th-c original review blocked')
