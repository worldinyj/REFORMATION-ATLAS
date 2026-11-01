import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((R/p).read_text())
d=load('data/contracts/atlas_v180_edition_claim_location_register.json')
readers=load('data/deep/atlas_v178_ten_readers_standardized.json')['chapters']
editions={e['id'] for w in load('data/contracts/atlas_v161_edition_comparison_cards.json')['works'] for e in w['editions']}
assert not d['publication_gate']['can_ship']
assert len(d['claims'])>=15
assert len({c['id'] for c in d['claims']})==len(d['claims'])
for c in d['claims']:
 assert c['reader_key'] in {x['key'] for x in readers}
 assert c['edition_id'] is None or c['edition_id'] in editions
 assert c['location_label'] and c['claim_ko'] and c['source_url'].startswith('https://')
 assert c['original_folio_collated'] is False and c['exact_wording_verified'] is False
 assert c['editorial_status']=='VERIFY_BEFORE_PUBLICATION'
print('PASS V180: 15 edition-location claims, source URLs, editorial and original-collation gates')
