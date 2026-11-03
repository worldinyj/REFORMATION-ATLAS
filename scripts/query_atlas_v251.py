#!/usr/bin/env python3
"""Local research search; all output remains draft and carries evidence limits."""
import argparse
import json
import unicodedata
from pathlib import Path
DATA=Path(__file__).resolve().parents[1]/'data/deep/atlas_v251_searchable_women_supplement.json'
def norm(text):
    return unicodedata.normalize('NFKC',text).casefold()
def search(d,query='',section=None,limit=10):
    sections={x['id']:x for x in d['sections']};evidence={x['id']:x for x in d['evidence']}
    terms=norm(query).split();result=[]
    for sentence in d['sentences']:
        sec=sections[sentence['section']]
        if section and section not in [sec['id'],sec['source_section']]:continue
        haystack=norm(' '.join([sec['title'],*sec['topics'],sentence['text_exact']]))
        if not all(term in haystack for term in terms):continue
        result.append(dict(sentence=sentence,section_title=sec['title'],claim_kind=sec['claim_kind'],
            evidence=[evidence[k] for k in sentence['evidence']],
            related_core=[x for x in d['links'] if x['section']==sec['id']]))
        if len(result)>=limit:break
    return {'status':d['status'],'publication_approved':False,'limitations':d['limitations'],'results':result}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--query',default='');parser.add_argument('--section');parser.add_argument('--limit',type=int,default=10);args=parser.parse_args()
    if not 1<=args.limit<=100:parser.error('--limit must be between 1 and 100')
    d=json.loads(DATA.read_text())
    if args.section and args.section not in {v for x in d['sections'] for v in [x['id'],x['source_section']]}:parser.error('unknown section')
    print(json.dumps(search(d,args.query,args.section,args.limit),ensure_ascii=False,indent=2))
