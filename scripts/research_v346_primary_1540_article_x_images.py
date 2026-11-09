#!/usr/bin/env python3
"""V3.46 one-shot direct 1540 Article X facsimile: Regensburg canvas 17 and Bamberg canvas 21.
Images are transient QC artifacts in GitHub Actions logs ONLY, not committed to repository.
No retries, no other-page downloads, no OCR required for proof; visual inspection needed after retrieval.
"""
import urllib.request,io,hashlib,base64,json
from PIL import Image
TARGETS=[("REGENSBURG","bsb11069754","00017"),("BAMBERG","bsb11399533","00021")]
for label,obj,page in TARGETS:
 url=f"https://api.digitale-sammlungen.de/iiif/image/v2/{obj}_{page}/full/1800,/0/default.jpg"
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS-V346-PRINT-VERIFICATION/1.0","Accept":"image/jpeg"})
  with urllib.request.urlopen(req,timeout=30) as r:
   raw=r.read(3500000);s=r.status;typ=r.headers.get("Content-Type","")
  im=Image.open(io.BytesIO(raw)).convert("RGB")
  print("V346_PRINT_SOURCE "+json.dumps({"id":label,"obj":obj,"canvas":int(page),"url":url,"http":s,"mime":typ,"original_bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"source_dimensions":im.size,"text_verified_by_human":False}),flush=True)
  im.thumbnail((1800,2500))
  buf=io.BytesIO();im.save(buf,format="JPEG",quality=80,optimize=True)
  b=base64.b64encode(buf.getvalue()).decode("ascii")
  print("V346_PRINT_IMG_INFO "+json.dumps({"id":label,"size":im.size,"bytes":len(buf.getvalue()),"chunks":(len(b)+2199)//2200}),flush=True)
  for k in range(0,len(b),2200):print(f"V346_PRINT_IMG_CHUNK {label} {k//2200:05d} {b[k:k+2200]}",flush=True)
 except Exception as e:print("V346_PRINT_FAILURE "+json.dumps({"id":label,"url":url,"error":str(e)[:220]}),flush=True)
print("V346_VISUAL_GATE incomplete until images explicitly visually reviewed",flush=True)
