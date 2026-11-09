#!/usr/bin/env python3
"""V3.49 bounded IA original scan access diagnostics (metadata / page image only).
No login, no CAPTCHA bypass, no repeated retries.
"""
import urllib.request,urllib.error,json
id='philippimelantho03mela'
urls=[
 ('IA_META',f'https://archive.org/metadata/{id}'),
 ('IA_READ',f'https://archive.org/BookReader/BookReaderJSIA.php?id={id}'),
 ('IA_IIIF',f'https://iiif.archive.org/iiif/{id}/manifest.json'),
 ('ARCHIVELAB_IIIF',f'https://iiif.archivelab.org/iiif/{id}/manifest.json'),
 ('IA_OCR',f'https://archive.org/download/{id}/{id}_djvu.txt'),
 ('IA_BR_PAGE',f'https://archive.org/BookReader/BookReaderImages.php?id={id}&itemPath=%2F12%2Fitems%2F{id}&server=ia800902.us.archive.org&page=n100&scale=2&rotate=0')
]
for label,url in urls:
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'REFORMATION-ATLAS-V349-SOURCE-CHECK/1.0','Accept':'application/json,image/jpeg,text/plain'}),timeout=18) as r:
   raw=r.read(500000);status=r.status;typ=r.headers.get('Content-Type','');final=r.geturl()
  d={'id':label,'http':status,'mime':typ,'final':final,'bytes_sample':len(raw)}
  if label=='IA_META':
   m=json.loads(raw);d.update({'dir':m.get('dir'),'server':m.get('d1'),'d2':m.get('d2'),'files':[{k:f.get(k) for k in ('name','size')} for f in m.get('files',[]) if any(s in f.get('name','') for s in ['_jp2','_djvu','_scandata','_abbyy','_meta.xml'])][:10]})
  elif 'image' not in typ:d['body_start']=raw[:140].decode('utf8','replace')
  print('V349_IA_ACCESS '+json.dumps(d,ensure_ascii=False),flush=True)
 except Exception as e:print('V349_IA_ERROR '+json.dumps({'id':label,'error':str(e)[:240]}),flush=True)
print('V349_IA_END access diagnostic only, direct print visual gate OPEN',flush=True)
