#!/usr/bin/env python3
"""V1.70 structural/editorial triage. No network or claim of peer review."""
import json, re, sys
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def get(path):return json.loads((R/path).read_text(encoding="utf-8"))
issues=[]; checks=[]
def check(name,good,detail=""):
 checks.append({"name":name,"pass":bool(good),"detail":detail})
 if not good:issues.append(name)
mods=[m for x in 'abcdef' for m in get(f'data/deep/atlas_v154_group_{x}.json')['modules']]
pages=get('data/deep/atlas_v156_extended_narratives.json')['pages']
evid=get('data/contracts/atlas_v163_source_evidence_cards.json')['cards']
matrix=get('data/contracts/atlas_v162_edition_article_matrix.json')['rows']
editions=get('data/contracts/atlas_v161_edition_comparison_cards.json')['works']
nav=get('data/contracts/atlas_v164_evidence_navigation.json')['claims']
geo=get('data/contracts/atlas_v157_historical_city_map.json')['places']
visual=get('data/contracts/atlas_v158_visual_rights_registry.json')['assets']
portraits=get('data/contracts/atlas_v159_portrait_item_provenance.json')['portrait_candidates']
fac=get('data/contracts/atlas_v160_document_facsimile_review.json')['facsimiles']
check('60 micro lessons',len(mods)==60)
check('10 reader pages',len(pages)==10)
check('8 evidence cards',len(evid)==8)
check('5 editions',sum(len(w['editions']) for w in editions)==5)
check('6 edition comparisons',len(matrix)==6)
check('11 mapped cities',len(geo)==11)
check('14 visual candidates',len(visual)==14)
for kind,items,key in [('micro',mods,'id'),('readers',pages,'id'),('evidence',evid,'id')]:
 check(kind+' unique ids',len({x[key] for x in items})==len(items))
 check(kind+' has source URLs',all(x.get('source_urls') for x in items))
 check(kind+' sources HTTPS',all(str(u).startswith('https://') for x in items for u in x['source_urls']))
check('micro required fields',all(m.get('reader_text') and m.get('question') for m in mods))
check('micro primary truth gated',all(m.get('verified_primary') is False for m in mods))
check('reader has five segments',all(len(p.get('segments',[]))>=5 for p in pages))
check('reader segments titled',all(s.get('heading') and s.get('text') for p in pages for s in p['segments']))
check('reader original collation gated',all(p.get('primary_collated') is False for p in pages))
check('reader review pending',all(p.get('review')=='PENDING' for p in pages))
check('evidence original gated',all(e.get('primary_original_folio_checked') is False for e in evid))
check('evidence release held',all(e.get('release')=='EDITORIAL_HOLD' for e in evid))
check('evidence uncertainty',all(e.get('unverified') for e in evid))
check('evidence source tier',all(e.get('proof_level') for e in evid))
check('navigation IDs',set(x['claim_id'] for x in nav)==set(x['id'] for x in evid))
check('navigation original gated',all(not x['verified_primary'] for x in nav))
check('matrix references',all(m['references'] for m in matrix))
check('matrix collation gated',all(m['collated'] is False for m in matrix))
check('portrait publish held',all(not x['approved_to_publish'] for x in portraits))
check('visual publish held',all(not x['approved_to_publish'] for x in visual))
check('facsimile image held',all(not x['image_approved'] for x in fac))
check('facsimile direct collation held',all(not x['original_page_collated'] for x in fac))
check('5 editorial blockers',len(get('data/contracts/atlas_v165_integration_readiness_manifest.json')['blocking_issues'])==5)
lens=[len(m['reader_text']) for m in mods];plens=[sum(len(s['text']) for s in p['segments']) for p in pages]
check('micro texts not empty',min(lens)>30)
check('reader text not empty',min(plens)>100)
dups=[v for v,n in Counter(m['reader_text'] for m in mods).items() if n>1]
check('no exact duplicated micro texts',not dups)
findings=[]
for p,n in zip(pages,plens):
 if n<1200:findings.append({'type':'DEPTH_SHORTFALL','id':p['id'],'character_count':n,'action':'서술·원문·사료 관점 확장 권장'})
for m,n in zip(mods,lens):
 if n<240:findings.append({'type':'MICRO_BRIEF','id':m['id'],'character_count':n,'action':'현재 미니 강의 분량; 심층 콘텐츠로 간주하지 않음'})
result={'version':'1.70','pass':not issues,'checks_total':len(checks),'checks_passed':sum(x['pass'] for x in checks),'checks':checks,'inventory':{'lessons':len(mods),'reader_pages':len(pages),'evidence':len(evid),'editions':5,'cities':len(geo)},'content_length':{'micro_min':min(lens),'micro_max':max(lens),'micro_mean':round(sum(lens)/len(lens),1),'reader_min':min(plens),'reader_max':max(plens),'reader_mean':round(sum(plens)/len(plens),1)},'editorial_findings':findings,'notes':['구조검사이며 사료·외부 URL의 실제 응답이나 역사적 진실성 판정 아님','240자 및 1200자는 연구용 작성 우선순위 기준이며 합격/불합격 기준 아님'],'publication_gate':'BLOCKED'}
out=R/'audit-v170.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:result[k] for k in ['pass','checks_total','checks_passed','inventory','content_length']},ensure_ascii=False))
print('Editorial improvement items:',len(findings))
sys.exit(0 if not issues else 1)
