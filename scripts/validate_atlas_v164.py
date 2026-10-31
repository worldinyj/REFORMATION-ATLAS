#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((r/p).read_text(encoding='utf8'))
nav=load('data/contracts/atlas_v164_evidence_navigation.json')
ev=load('data/contracts/atlas_v163_source_evidence_cards.json')
matrix=load('data/contracts/atlas_v162_edition_article_matrix.json')
ed=load('data/contracts/atlas_v161_edition_comparison_cards.json')
readers=load('data/deep/atlas_v156_extended_narratives.json')
ids={x['id'] for x in ev['cards']}
mid={x['id'] for x in matrix['rows']}
eids={e['id'] for w in ed['works'] for e in w['editions']}
rids={p['id'] for p in readers['pages']}
assert nav['publication_gate']=={'approved':False,'can_ship':False}
assert len(nav['claims'])==8
assert {v['claim_id'] for v in nav['claims']}==ids
assert all(v['matrix_id'] in mid and set(v['edition_ids'])<=eids and v['reader_page_id'] in rids for v in nav['claims'])
assert all(not v['verified_primary'] and v['original_folio_status']=='NOT_VERIFIED' for v in nav['claims'])
assert len(nav['editions'])==5
print('PASS V1.64: eight evidence navigation paths, five editions, valid historical page references')
