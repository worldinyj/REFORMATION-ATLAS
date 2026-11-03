#!/usr/bin/env python3
"""Check selected B-sheet observations, not a full bibliographic classification."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'data/deep/atlas_v249_b_sheet_selected_state_matrix.json'
def require(ok, message):
    if not ok:
        raise ValueError(message)
def validate(d):
    require((d['version'],d['status'],d['parent_commit']) == ('2.49','DRAFT','dd4b3ea25c3880455e35b587a899c6c93c44d6ce'), 'version')
    require(len(d['preserved_files']) == 2, 'snapshot count')
    for p in d['preserved_files']:
        require(hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest() == p['sha256'], 'snapshot changed')
    require([s['id'] for s in d['sources']] == ['HAB','BSB','ONB'] and d['sources'][0]['original_faces_seen'] == 0, 'source tiers')
    expected=[('L1','B1r',2,'rad'),('L2','B3r',24,'hiemit'),('L3','B3r',27,'mich'),('L4','B3r',28,'ihr')]
    require([(x['id'],x['folio'],x['line'],x['reading']) for x in d['loci']] == expected, 'selected loci')
    require(len(d['observations']) == 8, 'observation count')
    for source,canvases in [('BSB',[13,17,17,17]),('ONB',[9,13,13,13])]:
        rows=[x for x in d['observations'] if x['source']==source]
        require(len(rows)==4 and [x['canvas'] for x in rows]==canvases, 'copy-specific offset')
        require([(x['locus'],x['folio'],x['reading']) for x in rows] == [(a,b,f) for a,b,c,f in expected], 'word observations')
        require(all(x['basis']=='DIRECT_PHOTO_REINSPECTION' for x in rows), 'evidence kind')
    require(d['catalogue_profiles'] == [
        {'holding':'147.5 Theol. (14)','A4':['kloisters','schrfftlich'],'B':['rad','hiemit','mich','ihr'],'basis':'CATALOGUE_NOT_PHOTO'},
        {'holding':'116.10 Theol. (11)','A4':['klosters','schrifftlich'],'B':['rad','hiemit','mich','ihr'],'basis':'CATALOGUE_NOT_PHOTO'}], 'catalogue profiles')
    require(all(v is False for k,v in d['guards'].items() if k!='new_1526_faces') and d['guards']['new_1526_faces']==0, 'scope inflation')
    require(all(v is False for v in d['publication_gate'].values()), 'publication gate')
    require(d['rights']['ONB']=='http://rightsstatements.org/vocab/NoC-NC/1.0/' and not d['rights']['commercial_clearance_granted'] and not d['rights']['image_binaries_in_repository'], 'rights')
    require(d['metrics']=={'reinspected_original_faces':4,'previously_unseen_original_faces':0,'new_selected_word_observations':8,'paired_word_loci':4,'catalogue_profiles':2,'core_essays':10,'core_sentences':543}, 'duplicate faces miscounted')
    a=d['artifacts'];require(len(a)==4 and len({x['filename'] for x in a})==4, 'artifact count')
    for x in a:
        require(x['bytes']>0 and len(x['sha256'])==64 and x['url'].startswith('https://'), 'artifact provenance')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--evidence-dir',type=Path);args=parser.parse_args()
    d=json.loads(DATA.read_text());validate(d)
    if args.evidence_dir:
        for a in d['artifacts']:
            b=(args.evidence_dir/a['filename']).read_bytes()
            require(len(b)==a['bytes'] and hashlib.sha256(b).hexdigest()==a['sha256'], 'download integrity')
    print('PASS V249:4 paired B-sheet loci/8 photo observations;4 reinspected faces/0 previously unseen; catalogue separated; HOLD')
