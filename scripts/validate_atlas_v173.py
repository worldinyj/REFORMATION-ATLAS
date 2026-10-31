#!/usr/bin/env python3
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
names=['AUGSBURG','ZWINGLI','MARBURG','CALVIN1536','CALVIN1559','TRENT']
stats=[]
for name in names:
 p=root/f'docs/01_CONTENT/V173_{name}_DEEP_READER.md'
 s=p.read_text(encoding='utf8')
 body=s.split('**출처')[0]
 blocks=re.findall(r'^## ',body,re.M)
 assert len(blocks)>=5,(name,'sections',len(blocks))
 assert 'https://' in s and '미완료' in s
 assert len(body)>=1300,(name,len(body))
 stats.append({'topic':name,'characters':len(body),'sections':len(blocks),'editorial_review':'PENDING','primary_collated':False,'approved_to_publish':False})
report={'version':'1.73','scope':'six formerly missing standalone depth-reader drafts','chapters':stats,'total_characters':sum(x['characters'] for x in stats),'historical_primary_source_collation':'NOT_DONE','publication_gate':'HOLD','note':'Length and structural integrity only, not scholar peer-review'}
out=root/'v173-audit.json';out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
