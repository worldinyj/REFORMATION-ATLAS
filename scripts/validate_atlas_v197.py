import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]
d=json.loads((p/'data/contracts/atlas_v197_calvin_iii8_contextual_variant.json').read_text())
assert all(v is False for v in d['release'].values())
c=d['focused_case']
assert c['text_locus'].startswith('III.8.7')
assert [v['reading'] for v in c['editorial_readings']]==['concutimur','continemur','contemnimur']
assert c['editorial_readings'][1]['editorial_mark']=='male'
assert c['editorial_readings'][2]['editorial_mark']=='ex coniectura'
assert c['original_1539_text_checked'] is False
assert d['source_discovery']['text_inspected'] is False
assert d['marburg']['articles_7_13_15_original_text'] is None
print('PASS V197 contextual variant + editorial judgment; 1539 original and Marburg uncollated')
