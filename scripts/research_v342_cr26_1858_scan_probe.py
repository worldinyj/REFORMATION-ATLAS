#!/usr/bin/env python3
"""V3.42 — identify actual CR26 1858 first-edition print folios.
Read-only and temporary: downloads a PUBLIC-DOMAIN 1858 scanned PDF
to CI runner storage and reports page headers. No OCR or output corpus edits.
An IA identifier is NOT considered proof of volume until scan title and
specific folio headers have been independently inspected.
"""
import base64, hashlib, io, json, os, pathlib, sys, tempfile, urllib.request
import fitz
from PIL import Image,ImageDraw

URLS=[
 "https://upload.wikimedia.org/wikipedia/commons/3/37/Corpus_reformatorum_%28IA_corpusreformato09melagoog%29.pdf",
 "https://archive.org/download/corpusreformato09melagoog/corpusreformato09melagoog.pdf",
]
MAX=44*1024*1024
data=None;origin=None;errors=[]
for url in URLS:
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS-historical-scholarship/1.0 (public-domain-text)","Accept":"application/pdf"})
  with urllib.request.urlopen(req,timeout=110) as r:
   raw=r.read(MAX+1)
   if len(raw)>MAX: raise RuntimeError("PDF too large")
   if not raw.startswith(b"%PDF"): raise RuntimeError("not PDF response")
   data=raw;origin=url
  break
 except Exception as e:errors.append({"url":url,"error":str(e)})
print("V342_DOWNLOAD "+json.dumps({"source":origin,"bytes":len(data) if data else 0,"errors":errors}),flush=True)
if data is None:sys.exit(2)
sha=hashlib.sha1(data).hexdigest()
doc=fitz.open(stream=data,filetype="pdf")
pages=len(doc)
print("V342_PDF "+json.dumps({"sha1":sha,"pages":pages,"metadata":doc.metadata,"title_confirmation":"NOT_YET_VERIFIED"}),flush=True)
if pages<360 or pages>800:sys.exit("unexpected page count")
indices=[0,1,2,3,4,5,6,7,8,250,255,260,265,270,272,274,275,276,278,280,284,286,288,290,294,298,300,340,350,355,410]
for p in indices:
 if p>=pages: continue
 pg=doc[p]
 text=pg.get_text("text")
 print("V342_PAGE "+json.dumps({"pdf_zero_based":p,"text_layer_chars":len(text),"text_sample":text[:320].replace("\n"," "),"size":[pg.rect.width,pg.rect.height]}),flush=True)
thumb_pages=[0,2,4,260,265,270,275,280,285,290,294,298,350,410]
tiles=[]
for i in thumb_pages:
 if i>=pages:continue
 pg=doc[i]
 # crop top 35% of page to read print header and title, not content-level variants yet
 clip=fitz.Rect(0,0,pg.rect.width,pg.rect.height*.37)
 pix=pg.get_pixmap(matrix=fitz.Matrix(.85,.85),clip=clip,alpha=False)
 im=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
 im.thumbnail((600,390))
 tile=Image.new("RGB",(620,420),"white")
 tile.paste(im,((620-im.width)//2,24))
 d=ImageDraw.Draw(tile);d.text((9,5),f"PDF zero-based {i} / page number TO VERIFY",fill="black")
 tiles.append(tile)
mont=Image.new("RGB",(1240,420*((len(tiles)+1)//2)),(230,230,230))
for i,im in enumerate(tiles):mont.paste(im,((i%2)*620,(i//2)*420))
buff=io.BytesIO();mont.save(buff,"JPEG",quality=61,optimize=True)
b64=base64.b64encode(buff.getvalue()).decode()
print("V342_HEADER_MONTAGE_META "+json.dumps({"pages":thumb_pages,"size":[mont.width,mont.height],"bytes":len(buff.getvalue())}),flush=True)
for i in range(0,len(b64),2000):
 print(f"V342_HEADER_MONTAGE_CHUNK {i//2000:05d} {b64[i:i+2000]}",flush=True)
print("V342_SCAN_PROBE_DONE_HEADER_REVIEW_REQUIRED",flush=True)
