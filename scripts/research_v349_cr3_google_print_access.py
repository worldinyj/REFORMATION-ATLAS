#!/usr/bin/env python3
"""ATLAS V3.49 bounded two-catalogue public-domain 1836 CR III page-image access check.
Read four printed-page labels around pp75-78 in each Google Books witness.
HTTP 200 for a substitute thumbnail is NOT direct print access. No images copied into repo.
"""
from urllib.request import Request,urlopen
from PIL import Image
import io,hashlib,json
ITEMS=[("GOOGLE1836_A","Ww-zXLF_5KAC"),("GOOGLE1836_B","ZdrkTENsJaEC")]
for name,vid in ITEMS:
 for page in (75,76,77,78):
  url=f"https://books.google.com/books/content?id={vid}&pg=PA{page}&img=1&zoom=1"
  try:
   with urlopen(Request(url,headers={"User-Agent":"REFORMATION-ATLAS-v349/1.0","Accept":"image/png,image/jpeg"}),timeout=15) as r:
    raw=r.read(1500000);ct=r.headers.get("Content-Type","");status=r.status
   image=Image.open(io.BytesIO(raw))
   dims=list(image.size)
   substitute=(len(raw)<11000 or (dims[0]==575 and dims[1]==750))
   print("V349_GOOGLE_PAGE "+json.dumps({"witness":name,"page":page,"url":url,"http":status,"mime":ct,"bytes":len(raw),"dimensions":dims,
   "sha256":hashlib.sha256(raw).hexdigest(),"suspected_placeholder":substitute,"direct_print_visually_read":False}),flush=True)
  except Exception as e:
   print("V349_GOOGLE_ERROR "+json.dumps({"witness":name,"page":page,"url":url,"error":str(e)[:190]}),flush=True)
print("V349_GATE provisional image access test only; must visually inspect and identify original print page.")
