#!/usr/bin/env python3
"""Verify catalogue identity and preserve unresolved metadata disagreements."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/deep/atlas_v252_petition_catalogue_identity_conflicts.json'
def require(ok,msg):
    if not ok:raise ValueError(msg)
def validate(d):
    require((d['version'],d['status'],d['parent_commit'])==('2.52','DRAFT','8353aadcd51d6a12313f6e956ad5e3ee3e266b7c'),'version')
    require(len(d['preserved_files'])==3,'snapshots')
    for p in d['preserved_files']:
        require(hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()==p['sha256'],'snapshot changed')
    c=d['catalogue']
    require((c['id'],c['shelfmark'],c['extent_leaves'],c['document_type'])==('DE-611-HS-3408588','Chart. A 123, Bl. 19r-20v',2,'Abschrift'),'petition identity')
    require(c['reported_blank_folios']==['19r'] and c['catalogue_date']=='1526-11-13' and c['catalogue_place']=='Bamberg','catalogue fields')
    require(c['authors']==['Katherina Wachdorff','Felicitas (von Helfta)'] and c['recipient']=='Karl V.' and c['parent_volume']=='DE-611-BF-72245','roles')
    require(c['date_formula']=='montags nach Martinj','date formula')
    bad=d['rejected_record']
    require(bad['id']=='DE-611-HS-3408675' and bad['actual_author']=='Johannes Mathesius' and bad['actual_date']=='1556-11-18' and not bad['accepted_as_petition'],'wrong neighbour accepted')
    require([(x['id'],x['field'],x['prior_print_value'],x['catalogue_value'],x['final_value'],x['status']) for x in d['conflicts']]==[
        ('C01','date','1526-11-12','1526-11-13',None,'UNRESOLVED'),
        ('C02','place','[Leipzig]','Bamberg',None,'UNRESOLVED'),
        ('C03','second_author_name','Felicitas Tabelles zu der Zelle','Felicitas (von Helfta)',None,'IDENTITY_NORMALIZATION_PENDING')],'conflict silently resolved')
    require(all(v is False for k,v in d['guards'].items() if k!='original_faces_seen') and d['guards']['original_faces_seen']==0,'metadata promoted to original')
    require(all(v is False for v in d['publication_gate'].values()),'publication gate')
    require(d['metrics']=={'accepted_item_records':1,'rejected_neighbour_records':1,'conflict_records':3,'new_original_faces':0,'core_essays':10,'core_sentences':543},'metrics')
    require(len(d['artifacts'])==2 and len({x['filename'] for x in d['artifacts']})==2,'artifacts')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--evidence-dir',type=Path);a=p.parse_args();d=json.loads(DATA.read_text());validate(d)
    if a.evidence_dir:
        for row in d['artifacts']:
            b=(a.evidence_dir/row['filename']).read_bytes()
            require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'HTML bytes')
        correct=(a.evidence_dir/'petition252_correct.html').read_text()
        require(all(x in correct for x in ['3408588','19r-20v','Bamberg','13.11.1526','Abschrift']),'detail-page identity')
        rejected=(a.evidence_dir/'petition252_kalliope.html').read_text()
        require('Mathesius' in rejected and '18.11.1556' in rejected,'neighbour identity')
    print('PASS V252:correct catalogue3408588;reject3408675;3 unresolved fields;new faces0;HOLD')
