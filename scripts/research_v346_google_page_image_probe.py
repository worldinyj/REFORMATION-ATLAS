#!/usr/bin/env python3
"""V3.46: bounded Google Books 1540 Augsburg copy PAGE IMAGE probe, four distinct page anchors only.
No retries, no bulk scan, no source images committed.
"""
import urllib.request,urllib.error,json,base64
base="https://books.google.com/books/content?id=HmpoAAAAcAAJ&pg=PA{page}&img=1&zoom=3"
for p in [30,40,50,60]:
 url=base.format(page=p)
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS-v346-print-audit/1.0","Accept":"image/jpeg,image/png,image/webp"}),timeout=12) as r:
   payload=r.read(1200000);typ=r.headers.get("Content-Type","");status=r.status;fin=r.geturl()
  is_image=typ.startswith("image/") and payload[:3] in (b"\xff\xd8\xff",b"\x89PN")
  print("V346_PAGE_IMAGE "+json.dumps({"pg":"PA"+str(p),"url":url,"http":status,"final":fin,"mime":typ,"bytes":len(payload),"is_image":is_image,"visual_print_read":False}),flush=True)
  if is_image:
   b=base64.b64encode(payload).decode("ascii")
   print("V346_IMG_INFO "+json.dumps({"pg":"PA"+str(p),"mime":typ,"chunks":(len(b)+2199)//2200}),flush=True)
   for k in range(0,len(b),2200): print(f"V346_IMG_CHUNK PA{p} {k//2200:04d} {b[k:k+2200]}",flush=True)
 except Exception as e: print("V346_PAGE_IMAGE "+json.dumps({"pg":"PA"+str(p),"url":url,"http":0,"error":str(e)[:180],"visual_print_read":False}),flush=True)
print("V346_IMAGE_GATE result is only access metadata; never treat OCR or nonimage response as print reading",flush=True)
