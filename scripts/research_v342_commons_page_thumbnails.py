#!/usr/bin/env python3
"""ATLAS V3.42 second access route: Wikimedia page thumbnails, *not* full PDF.

Candidate IA corpusreformato09melagoog (420-page PDF, catalogued 1858).
Use image thumbnails for title & printed folio mapping. A successful request alone
does not certify volume or passage; requires actual visible page-header review.
No images committed; bounded requests; output transient visual contact sheet.
"""
import base64, io, json, urllib.request, urllib.error, time
from PIL import Image, ImageDraw
TEMPLATE="https://thumb.wikimedia.org/wikipedia/commons/thumb/3/37/Corpus_reformatorum_%28IA_corpusreformato09melagoog%29.pdf/page{n}-{w}px-Corpus_reformatorum_%28IA_corpusreformato09melagoog%29.pdf.jpg"
PAGES=[2,5,7,8,10,269,273,275,279,281,285,290,295,299,305,320]
out=[];images=[]
for n in PAGES:
    attempted=[]
    im=None
    for width in (500,250):
        url=TEMPLATE.format(n=n,w=width)
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS-V342-PageViewer/1.0","Accept":"image/jpeg"})
            with urllib.request.urlopen(req,timeout=20) as r:
                raw=r.read(3_000_000);typ=r.headers.get("Content-Type","")
                if not typ.startswith("image/"):raise RuntimeError("not image "+typ)
            im=Image.open(io.BytesIO(raw)).convert("RGB")
            attempted.append({"width":width,"http":200,"bytes":len(raw)})
            break
        except Exception as e:
            attempted.append({"width":width,"error":str(e)[:180]})
    out.append({"pdf_1based":n,"attempts":attempted,"image_retrieved":im is not None})
    if im is not None:
        im.thumbnail((600,700))
        w,h=im.size
        tile=Image.new("RGB",(630,730),"white")
        tile.paste(im,((630-w)//2,25));ImageDraw.Draw(tile).text((10,5),f"PDF page #{n}; print page? VERIFY visually",fill="black")
        images.append(tile)
    print("V342_THUMB "+json.dumps(out[-1]),flush=True)
print("V342_THUMB_SUMMARY "+json.dumps({"pages_requested":len(PAGES),"images_retrieved":len(images),"gallery_only_not_print_corroboration":True}),flush=True)
if images:
    montage=Image.new("RGB",(1260,730*((len(images)+1)//2)),(235,235,235))
    for idx,tile in enumerate(images):montage.paste(tile,((idx%2)*630,(idx//2)*730))
    buf=io.BytesIO();montage.save(buf,"JPEG",quality=65,optimize=True)
    z=base64.b64encode(buf.getvalue()).decode("ascii")
    print("V342_THUMB_MONTAGE "+json.dumps({"source":"Wikimedia Commons 1858 candidate","pages_sampled":PAGES,"montage_bytes":len(buf.getvalue()),"quality":"visual review only"}),flush=True)
    for i in range(0,len(z),2400):print(f"V342_THUMB_CHUNK {i//2400:05d} {z[i:i+2400]}",flush=True)
else:
    print("V342_THUMB_UNAVAILABLE: no image displayed; primary 1858 text not read",flush=True)
