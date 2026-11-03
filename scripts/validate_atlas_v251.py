#!/usr/bin/env python3
"""Validate exact supplement text and navigation; never certifies historical truth."""
import hashlib
import json
from pathlib import Path
from query_atlas_v251 import search
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/deep/atlas_v251_searchable_women_supplement.json'
def require(ok,message):
    if not ok:raise ValueError(message)
def validate(d):
    require((d['version'],d['status'],d['parent_commit'])==('2.51','DRAFT','22884c080b3f2797155b1c0dd3667ab878262fa9'),'version')
    docs=[]
    for p in d['preserved_files']:
        b=(ROOT/p['path']).read_bytes();require(hashlib.sha256(b).hexdigest()==p['sha256'],'preserved content');docs.append(json.loads(b))
    require(len(docs)==2,'snapshots');base,source=docs
    require(d['evidence']==source['evidence'],'evidence copied exactly')
    sections={x['id']:x for x in d['sections']};paras={x['id']:x for x in d['paragraphs']}
    require(len(sections)==len(d['sections'])==8 and len(paras)==len(d['paragraphs'])==16,'unique structures')
    for x in d['sections']:
        old=next(s for s in source['reader_sections'] if s['id']==x['source_section'])
        require(x['title']==old['title'] and x['claim_kind']==old['claim_kind'] and x['evidence']==old['evidence'],'section provenance')
        pp=[p for p in d['paragraphs'] if p['section']==x['id']]
        require([p['text_exact'] for p in pp]==old['paragraphs'],'exact paragraphs')
    require(len(d['sentences'])==len({x['id'] for x in d['sentences']})==59,'sentence identities')
    for p in paras.values():
        rows=[s for s in d['sentences'] if s['paragraph']==p['id']];cursor=0
        for x in rows:
            start,end=x['start_char'],x['end_char'];text=p['text_exact']
            require(cursor<=start<end<=len(text) and not text[cursor:start].strip(),'gap/overlap')
            require(text[start:end]==x['text_exact'] and x['section']==p['section'],'sentence slice')
            require(x['evidence']==sections[x['section']]['evidence'] and x['evidence_scope']=='INHERITED_SECTION_NOT_SENTENCE_PROOF' and not x['publication_approved'],'evidence scope')
            cursor=end
        require(not p['text_exact'][cursor:].strip(),'paragraph tail lost')
    baseline={x['id']:x for x in base['sentences']}
    require(len(d['links'])==len({x['id'] for x in d['links']})==8,'links')
    require({x['section'] for x in d['links']}==sections.keys(),'section coverage')
    for x in d['links']:
        require(x['baseline_sentence'] in baseline,'dangling baseline link');old=baseline[x['baseline_sentence']]
        require(x['baseline_excerpt']==old['excerpt'] and x['baseline_reader']==old['reader_key'],'wrong baseline excerpt')
        require(x['relation']=='EDITORIAL_THEMATIC_COMPARISON' and len(x['rationale'])>20,'link inference scope')
    require(all(v is False for v in d['publication_gate'].values()),'HOLD')
    require(len(d['limitations'])==4 and d['metrics']=={'supplement_sections':8,'supplement_paragraphs':16,'supplement_sentences':59,'comparison_links':8,'baseline_essays':10,'baseline_sentences':543,'new_original_faces':0,'public_items':0},'metrics/limits')
    for query,section in [('숫자','SEC-V251-R05'),('접수','SEC-V251-R07')]:
        res=search(d,query,limit=100)
        require(any(x['sentence']['section']==section for x in res['results']),'expected search result')
        require(not res['publication_approved'] and res['limitations']==d['limitations'],'search evidence warnings')
    require(not search(d,'zz_no_match_251')['results'],'no-match')
    require(all(x['sentence']['section']=='SEC-V251-R07' for x in search(d,section='R07',limit=100)['results']),'section filter')
if __name__=='__main__':
    validate(json.loads(DATA.read_text()))
    print('PASS V251:8 sections/16 exact paragraphs/59 supplement sentences;8 baseline links;search limits/HOLD;core10/543')
