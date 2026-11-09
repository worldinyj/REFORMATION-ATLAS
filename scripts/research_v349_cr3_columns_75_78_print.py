#!/usr/bin/env python3
"""V3.49 CR III 1836 direct original-print columns 75-78: IA IIIF canvas sequence near scan 62–63.
Only source image pixels and hashes logged; NEVER equate scan index with printed column number.
"""
import urllib.request,urllib.parse,json,base64,io,hashlib
from PIL import Image
id='philippimelantho03mela'
for page_scan in [62,63]:
 resource=f'{id}/{id}_jp2.zip/{id}_jp2/{id}_{page_scan:04d}.jp2'
 url='https://iiif.archive.org/image/iiif/3/'+urllib.parse.quote(resource,safe='')+'/full/1400,/0/default.jpg'
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'REFORMATION-ATLAS-V349-CR3-1836-COLLATION/1.0','Accept':'image/jpeg'}),timeout=55) as r:
   raw=r.read(3500000);typ=r.headers.get('Content-Type','');status=r.status
  im=Image.open(io.BytesIO(raw)).convert('RGB')
  orig=im.size
  im.thumbnail((1400,1900));out=io.BytesIO();im.save(out,'JPEG',quality=75,optimize=True)
  b=base64.b64encode(out.getvalue()).decode()
  print('V349_CR3_PRINT '+json.dumps({'scan_number':page_scan,'image_url':url,'http':status,'mime':typ,'raw_bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest(),'original_dimensions':orig,'review_dimensions':im.size,'chunks':(len(b)+2399)//2400,'direct_visual_read':False}),flush=True)
  for k in range(0,len(b),2400):print(f'V349_CR3_CHUNK S{page_scan:04d} {k//2400:04d} {b[k:k+2400]}',flush=True)
 except Exception as e:print('V349_CR3_PRINT_FAIL '+json.dumps({'scan_number':page_scan,'url':url,'error':str(e)[:240]}),flush=True)
print('V349_CR3_GATE: inspect printed column header, date, and Concordia wording visually',flush=True)
