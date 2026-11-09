#!/usr/bin/env python3
"""ATLAS V3.47: two historically distinct 1540 exemplar folios (CA VII / VIII).
Two bounded original IIIF reads, no retry, no files committed. Institutional OCR
is not used to substantiate the text. Review encoded images directly before verdict.
"""
import urllib.request,io,json,base64,hashlib
from PIL import Image
targets=[
 ("REGENSBURG_VII_VIII","bsb11069754","00016"),
 ("BAMBERG_VII_VIII","bsb11399533","00020"),
]
for label,bid,folio in targets:
    url=f"https://api.digitale-sammlungen.de/iiif/image/v2/{bid}_{folio}/full/1800,/0/default.jpg"
    try:
        request=urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS-V347-PRESS-STATE/1.0","Accept":"image/jpeg"})
        with urllib.request.urlopen(request,timeout=27) as r:
            raw=r.read(3_600_000); code=r.status; media=r.headers.get("Content-Type","")
        picture=Image.open(io.BytesIO(raw)).convert("RGB")
        dims=picture.size
        print("V347_ORIGINAL "+json.dumps({"id":label,"source_url":url,"http":code,"mime":media,
          "original_dimensions":dims,"original_bytes":len(raw),"original_sha256":hashlib.sha256(raw).hexdigest(),
          "visual_review_pending":True}),flush=True)
        picture.thumbnail((1850,2600))
        out=io.BytesIO();picture.save(out,"JPEG",quality=81,optimize=True)
        encoded=base64.b64encode(out.getvalue()).decode("ascii")
        print("V347_QC_IMAGE "+json.dumps({"id":label,"view_dimensions":picture.size,
          "chunks":(len(encoded)+2399)//2400,"bytes":len(out.getvalue())}),flush=True)
        for n in range(0,len(encoded),2400):
            print(f"V347_QC_CHUNK {label} {n//2400:05d} {encoded[n:n+2400]}",flush=True)
    except Exception as e:
        print("V347_FAILURE "+json.dumps({"id":label,"url":url,"error":str(e)[:220]}),flush=True)
print("V347_END original print verdict must be made by direct visual inspection, not network success",flush=True)
