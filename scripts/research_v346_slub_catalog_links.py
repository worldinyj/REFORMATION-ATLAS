#!/usr/bin/env python3
"""V3.46 one-request SLUB catalog link audit for Regensburg/Bamberg/Halle 1540 exemplars.
Read catalog markup only; no downloads of library images; no retries.
"""
import re,json,urllib.request,html
url='https://katalog.slub-dresden.de/?tx_find_find%5Bq%5D%5Btopic%5D%5B0%5D=%22Confessio+Augustana%22+%22Theologie%22+'
try:
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'REFORMATION-ATLAS-v346-research-audit/1.0'}),timeout=22) as r:
  raw=r.read(1000000);final=r.geturl();status=r.status
 t=raw.decode('utf-8','replace')
 print('V346_SLUB_STATUS '+json.dumps({'status':status,'final':final,'bytes':len(raw),'has_1540':bool(re.search(r'1540',t))}),flush=True)
 for key in ['Theol.syst.33','.10 D 14','Pon Vg 3008','1540']:
  m=re.search(re.escape(key),t,re.I)
  raw_context=t[max(0,m.start()-2500):m.start()+2500] if m else ''
  urls=re.findall(r'''(?:href|data-href)\s*=\s*['"]([^'"]+)['"]''',raw_context,re.I)
  print('V346_SLUB_MATCH '+json.dumps({'key':key,'found':bool(m),'context_text':re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',html.unescape(raw_context)))[:550],'nearby_links':list(dict.fromkeys(html.unescape(u) for u in urls))[:18]}),flush=True)
 for token in list(dict.fromkeys(re.findall(r'bsb\d{8}',t,re.I)))[:16]:
  print('V346_SLUB_BSBID '+token,flush=True)
except Exception as e:print('V346_SLUB_FAILURE '+json.dumps({'url':url,'error':str(e)[:200]}),flush=True)
print('V346_SLUB_GATE catalog-only; full original image read status remains OPEN',flush=True)
