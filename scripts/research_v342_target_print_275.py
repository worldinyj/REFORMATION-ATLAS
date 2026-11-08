#!/usr/bin/env python3
"""V3.42 targeted per-PDF-page original 1858 print spread review.

Public-domain Wikimedia Commons image-scans of IA corpusreformato09melagoog,
accessed as individual page thumbnails, without full PDF download.
This verifier does NOT use OCR; human image inspection is required before
recording Latin readings. Avoid promoting guessed printed page offsets.
"""
import base64,io,json,urllib.request,urllib.error
from PIL import Image
PAGES=[157,158,159,160,161,162,163,164,165,166,167,168]
TEMPLATE="https://thumb.wikimedia.org/wikipedia/commons/thumb/3/37/Corpus_reformatorum_%28IA_corpusreformato09melagoog%29.pdf/page{n}-1280px-Corpus_reformatorum_%28IA_corpusreformato09melagoog%29.pdf.jpg"
for n in PAGES:
 url=TEMPLATE.format(n=n)
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS/1.0","Accept":"image/jpeg"})
  with urllib.request.urlopen(req,timeout=18) as f:
   b=f.read(5_000_000);ct=f.headers.get("Content-Type","");status=f.status
  if not ct.startswith("image/"):raise RuntimeError("not-image "+ct)
  im=Image.open(io.BytesIO(b)).convert("RGB")
  print("V342_TARGET_PRINT "+json.dumps({"pdf_page_1based":n,"http":status,"image_pixels":[im.width,im.height],"bytes":len(b),"page_num_formula":"printed_left=2*(pdf_page_1based)-49, to visually verify","facsimile_source":url}),flush=True)
  # For efficiency emit full visual data only around the expected 275 and 276 printed pages.
  if n in [160,161,162,163,164,165]:
   s=base64.b64encode(b).decode()
   for i in range(0,len(s),2400):
    print(f"V342_TARGET_CHUNK {n} {i//2400:05d} {s[i:i+2400]}",flush=True)
 except Exception as e:
  print("V342_TARGET_ERROR "+json.dumps({"pdf_page_1based":n,"error":str(e)}),flush=True)
print("V342_TARGET_REVIEW_REQUIRED",flush=True)
