#!/usr/bin/env python3
"""V3.46: verify 1540 Rhau Regensburg/Bamberg BSB IIIF IDs, seek Article X via *existing* institution OCR.
No image files committed; OCR is navigation only. Bounded 2 manifests + <= 14 OCR page reads per volume.
"""
import re,json,urllib.request,urllib.error,html
OBJECTS=[("REGENSBURG","bsb11069754","999/4Theol.syst.33"),("BAMBERG","bsb11399533",".10 D 14")]
def get(url,lim=3000000):
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS-V346-IIIF-ARTICLE-X-RESEARCH/1.0","Accept":"application/json,text/xml,text/html"})
  with urllib.request.urlopen(req,timeout=18) as r:
   return (r.status,r.headers.get("Content-Type",""),r.read(lim),r.geturl())
 except Exception as e:return (0,str(e)[:180],b"",url)
def plain(s):
 s=re.sub(r"<[^>]*>"," ",s)
 return re.sub(r"\s+"," ",html.unescape(s)).strip()
for label,obj,shelf in OBJECTS:
 url=f"https://api.digitale-sammlungen.de/iiif/presentation/v2/{obj}/manifest"
 status,typ,body,final=get(url,6000000)
 print("V346_BSB_MANIFEST "+json.dumps({"label":label,"obj":obj,"http":status,"mime":typ,"bytes":len(body),"url":url},ensure_ascii=False),flush=True)
 if status!=200: continue
 try:
  m=json.loads(body)
  canv=m.get("sequences",[{}])[0].get("canvases",[])
  meta=[{"label":str(x.get("label","")),"value":re.sub(r"<[^>]*>"," ",str(x.get("value","")))[:250]} for x in m.get("metadata",[])]
  print("V346_BSB_META "+json.dumps({"label":label,"obj":obj,"title":m.get("label"),"canvases":len(canv),"metadata":meta[:13],"description":str(m.get("description",""))[:350]},ensure_ascii=False),flush=True)
  alln=[44,52,60,68,76,84]
  for n in alln:
   if n>len(canv):continue
   u=f"https://api.digitale-sammlungen.de/ocr/{obj}/{n}"
   s,t,b,_=get(u,700000)
   text=plain(b.decode("utf-8","replace"))
   pos=re.search(r"(?:de\s+c[œo]ena\s+domini|c[œo]ena\s+domini|(?:corp[uv]s|co[rp]pus).{0,90}sanguis\s+christi)",text,re.I)
   nearby=text[max(0,pos.start()-100):pos.start()+450] if pos else ""
   print("V346_BSB_OCR "+json.dumps({"label":label,"obj":obj,"n":n,"http":s,"characters":len(text),"start":text[:130],"coena_hit":bool(pos),"around":nearby,"grade":"EXISTING_INSTITUTION_OCR_NAVIGATION_ONLY"},ensure_ascii=False),flush=True)
 except Exception as e:print("V346_BSB_PARSE_ERROR "+json.dumps({"obj":obj,"error":str(e)[:200]}),flush=True)
print("V346_BSB_END: image-based visual claim still OPEN pending printed page image",flush=True)
