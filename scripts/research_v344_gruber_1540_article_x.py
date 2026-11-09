#!/usr/bin/env python3
"""V3.44 bounded once-per-source sample of contemporary 1540 Variata image from the Gruber collection.
Image bytes appear only as ephemeral evidence in CI logs, never committed to repository.
"""
import urllib.request,io,base64,json
from PIL import Image
for name in ["gruber28var.jpg","gruber28a.jpg"]:
 url="https://gruber.lstc.edu/confessions/images/"+name
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS-v344/1.0"}),timeout=25) as r:
   data=r.read(3000000);status=r.status;mime=r.headers.get("Content-Type","")
  img=Image.open(io.BytesIO(data)).convert("RGB")
  print("V344_GRUBER_PRIMARY "+json.dumps({"url":url,"http":status,"mime":mime,"size":img.size,"bytes":len(data)}),flush=True)
  img.thumbnail((1800,2200))
  out=io.BytesIO();img.save(out,format="JPEG",quality=79,optimize=True)
  b=base64.b64encode(out.getvalue()).decode("ascii")
  print("V344_GRUBER_IMG_INFO "+json.dumps({"name":name,"size":img.size,"chunks":(len(b)+2199)//2200}),flush=True)
  for j in range(0,len(b),2200):print(f"V344_GRUBER_IMG_CHUNK {name} {j//2200:04d} {b[j:j+2200]}",flush=True)
 except Exception as e:print("V344_GRUBER_ERR "+json.dumps({"url":url,"error":str(e)[:200]}),flush=True)
print("V344_GRUBER_END direct reading only after human visual review",flush=True)
