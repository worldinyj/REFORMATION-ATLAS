#!/usr/bin/env python3
"""Validate synthesis traceability without approving historical interpretation."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/deep/atlas_v250_women_three_perspectives_synthesis.json'
def require(ok,message):
    if not ok:raise ValueError(message)
def validate(d):
    require((d['version'],d['status'],d['parent_commit'])==('2.50','DRAFT','06e02d95b9805539b0be0f03d812acab8248ca5a'),'version/parent')
    require(d['kind']=='READER_SYNTHESIS_WITH_EVIDENCE_LEDGER','deliverable kind')
    require(len(d['preserved_files'])==6,'snapshot count')
    snapshots={}
    for p in d['preserved_files']:
        b=(ROOT/p['path']).read_bytes()
        require(hashlib.sha256(b).hexdigest()==p['sha256'],'inherited snapshot changed')
        snapshots[p['path']]=json.loads(b)
    e={x['id']:x for x in d['evidence']}
    require(len(e)==len(d['evidence'])==6,'evidence IDs')
    for x in e.values():
        require(x['dataset'] in snapshots and x['field'] in snapshots[x['dataset']] and x['locus'] and x['scope'],'evidence path')
    require([e[f'E{i:02}']['level'] for i in range(1,7)]==['PRINT_PHOTO_AND_EDITION','LATER_PRINT','LATER_PRINT_OF_COPY','SELECTED_ORIGINAL_PRINT_PAIR','NUMERIC_PENDING','DEPENDENT_REGEST'],'evidence levels')
    numeric=snapshots[e['E05']['dataset']]['numeric_review']
    require(not numeric['palaeography_approved'] and all(t['autograph_final_value'] is None for t in numeric['targets']),'numeric pending inherited')
    rows=d['reader_sections']
    require([x['id'] for x in rows]==[f'R{i:02}' for i in range(1,9)],'section IDs')
    for row in rows:
        require(len(row['paragraphs'])==2 and all(len(x)>90 for x in row['paragraphs']),'reader paragraphs')
        require(row['evidence'] and set(row['evidence'])<=e.keys(),'unresolved evidence ID')
    require(rows[0]['claim_kind']==rows[7]['claim_kind']=='COMPARATIVE_INTERPRETATION','interpretation attribution')
    require(rows[4]['claim_kind']=='LATER_PRINT_NUMBERS_AUTOGRAPH_PENDING' and 'E05' in rows[4]['evidence'],'numbers promoted')
    require(rows[5]['claim_kind']=='PETITION_VIA_LATER_PRINT_OF_SCRIBAL_COPY','petition autograph claim')
    require(d['guards']=={'new_original_faces':0,'new_numeric_approval':False,'petition_autograph_seen':False,'emperor_receipt_proven':False,'Gess_independent_witness':False,'pamphlet_caused_1525_attack':False,'full_edition_collation_complete':False,'same_convent_for_all_women':False,'public_historical_review_approved':False},'historical overclaim')
    require(all(v is False for v in d['publication_gate'].values()),'publication gate')
    require(d['metrics']=={'reader_sections':8,'reader_paragraphs':16,'evidence_records':6,'new_original_faces':0,'core_essays':10,'core_sentences':543},'metrics')
if __name__=='__main__':
    validate(json.loads(DATA.read_text()))
    print('PASS V250:8 reader sections/16 paragraphs;6 linked evidence records;numeric/receipt/causality guards;core10/543;HOLD')
