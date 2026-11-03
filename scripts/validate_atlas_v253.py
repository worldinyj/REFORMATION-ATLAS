#!/usr/bin/env python3
"""Calendar consistency is conditional and does not certify a manuscript reading."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/deep/atlas_v253_petition_calendar_audit.json'
def require(ok,msg):
    if not ok:raise ValueError(msg)
def julian_jdn(year,month,day):
    a=(14-month)//12;y=year+4800-a;m=month+12*a-3
    return day+(153*m+2)//5+365*y+y//4-32083
def validate(d):
    require((d['version'],d['status'],d['parent_commit'])==('2.53','DRAFT','622ba5c87345ea28fde2cd943adc15a4b3a582ad'),'version')
    require(len(d['preserved_files'])==3,'snapshots')
    for p in d['preserved_files']:
        require(hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()==p['sha256'],'prior snapshot')
    require([x['id'] for x in d['sources']]==['USNO','JPL','FEAST','PRINT'],'sources')
    rows=d['calendar_rows'];require(len(rows)==3,'date count')
    for x,day in zip(rows,[11,12,13]):
        jd=julian_jdn(1526,11,day);greg=datetime.date.fromordinal(jd-1721425)
        require(x['julian_date']==f'1526-11-{day}' and x['jd_at_noon']==jd,'Julian arithmetic')
        require(x['weekday']==['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][jd%7] and x['proleptic_gregorian']==greg.isoformat(),'weekday/Gregorian arithmetic')
        require(greg.weekday()==jd%7 and greg.day-day==10,'calendar gap')
    require(d['print_check']=={'printed_page':338,'pdf_page':346,'date_phrase':'Montags nach Martini','editorial_footnote_day':12,'month':11,'year':1526,'reinspected_faces':1,'new_original_faces':0},'printed/reinspected distinction')
    a=d['assessment']
    require(len(a['assumptions'])==3 and a['conditional_date']=='1526-11-12' and a['conditional_date_calendar']=='JULIAN' and a['conditional_proleptic_gregorian']=='1526-11-22','conditional conclusion')
    require(a['catalogue_date']=='1526-11-13' and a['catalogue_date_weekday_under_julian']=='Tuesday' and a['calendar_arithmetic_resolved'] is True,'catalogue disagreement')
    require(a['manuscript_date_final'] is None and all(a[k] is False for k in ['same_day_calendar_switch_explains_one_day_gap','catalogue_error_proven','place_conflict_resolved','handwriting_collated','local_1526_liturgical_ordo_checked']),'calculation promoted to manuscript proof')
    require(len(d['artifacts'])==len({x['filename'] for x in d['artifacts']})==6,'API assets')
    require({(x['source'],int(x['filename'].split('_')[-1].split('.')[0])) for x in d['artifacts']}=={(s,n) for s in ['USNO','JPL'] for n in [11,12,13]},'API coverage')
    for x in d['artifacts']:
        day=int(x['filename'].split('_')[-1].split('.')[0]);row=rows[day-11];res=x['response']
        require(x['bytes']>0 and len(x['sha256'])==64 and x['url'].endswith(str(row['jd_at_noon'])),'query mapping')
        if x['source']=='USNO':
            v=res['data'][0];require((v['year'],v['month'],v['day'],v['dayofweek'])==(1526,11,day,row['weekday']),'USNO result')
        else:require(res['cd'].startswith(row['julian_date']) and res['dow_name']==row['weekday'],'JPL result')
    require(all(v is False for v in d['publication_gate'].values()),'publication gate')
    require(d['metrics']=={'calendar_dates_checked':3,'API_responses':6,'reinspected_print_faces':1,'new_original_faces':0,'core_essays':10,'core_sentences':543},'metrics')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--evidence-dir',type=Path);a=p.parse_args();d=json.loads(DATA.read_text());validate(d)
    if a.evidence_dir:
        for x in d['artifacts']:
            b=(a.evidence_dir/x['filename']).read_bytes();require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'] and json.loads(b)==x['response'],'API source bytes')
    print('PASS V253:Julian12 Monday/13 Tuesday;USNO+JPL6 responses;conditional date only;original0;HOLD')
