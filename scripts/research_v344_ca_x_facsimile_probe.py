#!/usr/bin/env python3
"""V3.44 single-run, bounded acquisition: 1531 BSB Article X locus and Gruber 1540 article-X image.
Remote OCR is navigation only. Print excerpts, never publish image in repository.
No modification to corpus or web app. No retries.
"""
import re,json,base64,io,html
from urllib.request import Request,urlopen
from urllib.parse import urljoin
from PIL import Image
ID="bsb00103368"
def get(url,max_bytes=1800000):
 try:
  with urlopen(Request(url,headers={"User-Agent":"ATLAS-REFORMATION-RESEARCH-v344/1.0"}),timeout=25) as r:
   raw=r.read(max_bytes+1)
   return r.status,r.headers.get("Content-Type",""),raw[:max_bytes]
 except Exception as ex: return 0,str(ex)[:200],b""
def emit_image(code,raw):
 try:
  im=Image.open(io.BytesIO(raw)).convert("RGB"); original=im.size
  im.thumbnail((1500,2000))
  out=io.BytesIO();im.save(out,format="JPEG",quality=72,optimize=True)
  b=base64.b64encode(out.getvalue()).decode("ascii")
  print("V344_IMG_INFO "+json.dumps({"code":code,"original":original,"scaled":im.size,"jpeg_bytes":len(out.getvalue()),"chunks":(len(b)+2199)//2200}),flush=True)
  for j in range(0,len(b),2200):print(f"V344_IMG_CHUNK {code} {j//2200:04d} {b[j:j+2200]}",flush=True)
 except Exception as e:print("V344_IMG_ERROR "+code+" "+str(e)[:150],flush=True)
print("V344_START BOUNDED_READ_ONLY",flush=True)
manifest=f"https://api.digitale-sammlungen.de/iiif/presentation/v2/{ID}/manifest"
status,typ,raw=get(manifest,6000000)
print("V344_MANIFEST "+json.dumps({"http":status,"bytes":len(raw),"content_type":typ}),flush=True)
if status==200:
 try:
  o=json.loads(raw);canv=o.get("sequences",[{}])[0].get("canvases",[])
  print("V344_CANVAS_COUNT "+str(len(canv)),flush=True)
  for n in [17,18,19]:
   if n>len(canv):continue
   ca=canv[n-1]
   service=ca.get("images",[{}])[0].get("resource",{}).get("service",{}).get("@id","")
   print("V344_CANVAS "+json.dumps({"n":n,"label":ca.get("label"),"service":service}),flush=True)
   s,t,xml=get(f"https://api.digitale-sammlungen.de/ocr/{ID}/{n}",500000)
   txt=re.sub(r"\\s+"," ",html.unescape(re.sub("<[^>]+>"," ",xml.decode("utf-8","replace"))))
   z=re.search(r"(?i)coen[ae]|c[œo]ena|cena|corp[uv]s|[ad]d[sſ]int|di[sſ]trib",txt)
   print("V344_1531_OCR "+json.dumps({"canvas":n,"http":s,"len":len(txt),"first":txt[:300],"locus":txt[max(0,z.start()-240):z.start()+750] if z else "NONE","evidence_grade":"OCR_NAVIGATION_ONLY"},ensure_ascii=False),flush=True)
   if n in [17,18] and service:
    url=service.rstrip("/")+"/full/1800,/0/default.jpg"
    st,mt,raw_img=get(url,3500000)
    print("V344_1531_IMAGE_HTTP "+json.dumps({"canvas":n,"http":st,"mime":mt,"url":url,"bytes":len(raw_img)}),flush=True)
    if st==200 and mt.startswith("image/"):emit_image("BSB1531P"+str(n),raw_img)
 except Exception as e: print("V344_BSB_PARSE "+str(e)[:220],flush=True)
u="https://gruber.lstc.edu/confessions/augs_apol.php"
st,mt,raw=get(u,500000)
print("V344_GRUBER_HTML "+json.dumps({"http":st,"len":len(raw)}),flush=True)
if st==200:
 s=raw.decode("utf-8","replace"); pos=s.lower().find("gruber 28")
 print("V344_GRUBER_POS "+str(pos),flush=True)
 if pos>=0:
  around=s[max(0,pos-3000):pos+6500]
  assets=[]
  for m in re.finditer(r"(?:src|href)\\s*=\\s*['\"]([^'\"]+)['\"]",around,re.I):
   url=urljoin(u,html.unescape(m.group(1)))
   if re.search(r"\\.(?:jpe?g|png|gif)(?:\\?|$)",url,re.I):assets.append(url)
  assets=list(dict.fromkeys(assets))
  print("V344_GRUBER_NEAR_IMG "+json.dumps(assets[:20]),flush=True)
  for j,url in enumerate(assets[:4]):
   ss,ct,rr=get(url,2000000)
   print("V344_GRUBER_IMAGE_HTTP "+json.dumps({"n":j,"url":url,"http":ss,"mime":ct,"bytes":len(rr)}),flush=True)
   if ss==200 and ct.startswith("image/"):emit_image("GRUBER"+str(j),rr)
print("V344_END observational; proof only after visual review",flush=True)
