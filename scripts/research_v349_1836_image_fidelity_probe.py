#!/usr/bin/env python3
"""V3.49: sparse 1836 CR III page 75–77 image fidelity test; Google higher zoom and IA BookReader.
No image reproduction or archive download. One request per target, output diagnostics only.
"""
import urllib.request,urllib.parse,json,hashlib,io
from PIL import Image
qs=[
 ("GOOGLE_A_ZOOM2","https://books.google.com/books/content?id=Ww-zXLF_5KAC&pg=PA75&img=1&zoom=2"),
 ("GOOGLE_A_ZOOM3","https://books.google.com/books/content?id=Ww-zXLF_5KAC&pg=PA75&img=1&zoom=3"),
 ("GOOGLE_B_ZOOM2","https://books.google.com/books/content?id=ZdrkTENsJaEC&pg=PA76&img=1&zoom=2"),
 ("GOOGLE_B_ZOOM3","https://books.google.com/books/content?id=ZdrkTENsJaEC&pg=PA76&img=1&zoom=3"),
 ("IA_BR_META","https://archive.org/services/metadata/philippimelantho03mela"),
 ("IA_BR_IMG","https://archive.org/BookReader/BookReaderImages.php?id=philippimelantho03mela&itemPath=%2F12%2Fitems%2Fphilippimelantho03mela&server=ia800902.us.archive.org&page=n100&scale=2&rotate=0")
]
for name,url in qs:
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS-RESEARCH-v349/1.0","Accept":"image/jpeg,image/png,application/json;q=.9"}),timeout=20) as r:
   raw=r.read(2000000); status=r.status;ctype=r.headers.get("Content-Type","");resolved=r.geturl()
  d={"id":name,"http":status,"content_type":ctype,"bytes":len(raw),"url":url,"final":resolved,
     "sha256":hashlib.sha256(raw).hexdigest()}
  try:
   im=Image.open(io.BytesIO(raw));d["image_size"]=list(im.size)
  except Exception:
   if "json" in ctype:
    meta=json.loads(raw);d["json_keys"]=list(meta)[:12];d["server"]=meta.get("server");d["dir"]=meta.get("dir")
   else:d["body_start"]=raw[:110].decode("utf8","replace")
  print("V349_RENDER "+json.dumps(d,ensure_ascii=False),flush=True)
 except Exception as e:print("V349_RENDER_FAIL "+json.dumps({"id":name,"error":str(e)[:230]}),flush=True)
print("V349_RENDER_GATE: direct image visual review still necessary",flush=True)
