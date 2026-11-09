#!/usr/bin/env python3
"""V3.49 inspect IA IIIF v3 labels for 1836 CR III printed folios without guessing scan index.
"""
import urllib.request,json
url="https://iiif.archive.org/iiif/philippimelantho03mela/manifest.json"
try:
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS-V349-IIIF-LOCUS/1.0","Accept":"application/ld+json,application/json"}),timeout=30) as r:
  obj=json.load(r);status=r.status
 canvases=obj.get("items",[])
 print("V349_MANIFEST "+json.dumps({"status":status,"id":obj.get("id"),"type":obj.get("type"),"canvases":len(canvases),"label":obj.get("label"),"keys":list(obj)},ensure_ascii=False),flush=True)
 matches=[]
 for i,ca in enumerate(canvases):
  label=ca.get("label")
  labeltext=json.dumps(label,ensure_ascii=False)
  if any(f" {n}" in labeltext for n in ("75","76","77","78")):
   matches.append({"index_zero":i,"label":label})
 print("V349_PAGE_LABEL_MATCH "+json.dumps(matches[:30],ensure_ascii=False),flush=True)
 for i in list(range(0,min(14,len(canvases))))+list(range(65,min(132,len(canvases)),5)):
  ca=canvases[i]
  a=(ca.get("items") or [{}])[0]
  b=(a.get("items") or [{}])[0]
  body=b.get("body") or {}
  print("V349_CANVAS "+json.dumps({"index_zero":i,"id":ca.get("id"),"label":ca.get("label"),"height":ca.get("height"),"width":ca.get("width"),"body":str(body.get("id",""))[:250],"services":body.get("service")},ensure_ascii=False),flush=True)
except Exception as e:print("V349_MANIFEST_FAIL "+str(e)[:230],flush=True)
