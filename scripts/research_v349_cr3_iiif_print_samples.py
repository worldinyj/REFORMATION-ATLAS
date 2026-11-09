#!/usr/bin/env python3
"""ATLAS V3.49 original 1836 CR III selected page images for printed-pagination visual search.
The scan sequence contains front matter; canvas number must not be misread as printed page number.
Only three 900px-thumbnails emitted to CI logs for live visual identification, no original scans committed.
"""
import urllib.request,urllib.parse,json,base64,io,hashlib
from PIL import Image
book='philippimelantho03mela'
for canvas_index in [85,92,99]:
 num=canvas_index+1
 resource=f'{book}/{book}_jp2.zip/{book}_jp2/{book}_{num:04d}.jp2'
 url='https://iiif.archive.org/image/iiif/3/'+urllib.parse.quote(resource,safe='')+'/full/1000,/0/default.jpg'
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'REFORMATION-ATLAS-V349-CR3-FACSIMILE/1.0','Accept':'image/jpeg'}),timeout=32) as r:
   raw=r.read(2500000);typ=r.headers.get('Content-Type','');status=r.status
  im=Image.open(io.BytesIO(raw)).convert('RGB')
  im.thumbnail((950,1500))
  out=io.BytesIO(); im.save(out,format='JPEG',quality=69,optimize=True)
  b=base64.b64encode(out.getvalue()).decode()
  print('V349_ORIGINAL_SAMPLE '+json.dumps({'scan_index_zero':canvas_index,'scan_number':num,'url':url,'http':status,'mime':typ,'bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest(),'image_dimensions':im.size,'chunks':(len(b)+2399)//2400}),flush=True)
  for i in range(0,len(b),2400):print(f'V349_IMAGE_CHUNK N{num:04d} {i//2400:04d} {b[i:i+2400]}',flush=True)
 except Exception as e:print('V349_SAMPLE_FAIL '+json.dumps({'scan_number':num,'error':str(e)[:240]}),flush=True)
print('V349_PHYSICAL_PAGINATION_PENDING until printed page number visually read',flush=True)
