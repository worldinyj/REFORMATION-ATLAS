#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
read=lambda name:json.loads((r/name).read_text(encoding='utf8'))
m=read('data/contracts/atlas_v157_historical_city_map.json')
t=read('data/contracts/atlas_v157_spatiotemporal_links.json')
p=read('data/deep/atlas_v156_extended_narratives.json')
assert len(m['places'])==11 and len(t['links'])==11
assert m['publication_gate']['can_ship'] is False and t['publication_gate']['can_ship'] is False
assert len({x['id'] for x in m['places']})==11
ids={x['id'] for x in m['places']}
pages={x['id'] for x in p['pages']}
assert all(x['place_id'] in ids and x['reader_page_id'] in pages for x in t['links'])
assert all(x['coordinate_scope']=='CITY_CENTROID_APPROXIMATE' for x in m['places'])
assert all(-90<=x['lat']<=90 and -180<=x['lon']<=180 for x in m['places'])
assert m['media_policy']['images_embedded']==0
print('PASS V1.57: 11 city-level anchors, 11 page relations, permissions hold')
