#!/usr/bin/env python3
"""V3.41 research-only facsimile excerpt visualization.
Fetches 1531 public-domain printed leaves via BSB official IIIF and existing hOCR
for navigation, crops four short strips in CI memory; never commits page images.
Explicitly not a substitute for cross-exemplar collation.
"""
import base64, io, json, re, sys, urllib.request, urllib.error, time
from html.parser import HTMLParser
from PIL import Image, ImageDraw, ImageFont, ImageOps

OBJECT="bsb00103368"
BASE="https://api.digitale-sammlungen.de"
PAGES=[16]
TARGETS=[
 ("W04","CA VIII",16,r"^(?:fenties|fentiebant|sentiebant|ſentiebant|sentibant|fentibant)$"),
]
def get_bytes(url):
    req=urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS-v341-research/1.0","Accept":"*/*"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=35) as f:
                return f.status,f.read(),f.headers.get("Content-Type","")
        except urllib.error.HTTPError as e:
            print("V341_FETCH_HTTP_ERROR "+json.dumps({"url":url,"status":e.code,"attempt":attempt+1}),flush=True)
            if e.code not in (429,500,502,503,504) or attempt==2: raise
            time.sleep(attempt+1)
class Words(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth=0
        self.target=None
        self.text=[]
        self.words=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if self.target is not None: self.depth+=1
        elif tag in ("span","div") and any(v in d.get("class","") for v in ["ocrx_word","ocr_word"]):
            m=re.search(r"\bbbox\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",d.get("title",""))
            if m: self.target=tuple(map(int,m.groups()));self.depth=1;self.text=[]
    def handle_data(self,data):
        if self.target: self.text.append(data)
    def handle_endtag(self,tag):
        if self.target:
            self.depth-=1
            if self.depth==0:
                s="".join(self.text).strip()
                if s: self.words.append((s,self.target))
                self.target=None;self.text=[]

by_page={}
for page in PAGES:
    u=f"{BASE}/ocr/{OBJECT}/{page}"
    st,raw,typ=get_bytes(u)
    parser=Words();parser.feed(raw.decode("utf8",errors="replace"))
    imgurl=f"{BASE}/iiif/image/v2/{OBJECT}_{page:05d}/full/full/0/default.jpg"
    status,data,itype=get_bytes(imgurl)
    im=Image.open(io.BytesIO(data)).convert("RGB")
    print("V341_SOURCE "+json.dumps({"canvas":page,"ocr_http":st,"ocr_words_with_bbox":len(parser.words),"image_http":status,"image_content_type":itype,"image_pixels":[im.width,im.height],"image_url":imgurl}),flush=True)
    by_page[page]={"words":parser.words,"image":im}
crops=[]
for key,article,page,rx in TARGETS:
    p=by_page[page];words=p["words"];im=p["image"]
    matches=[(s,box) for s,box in words if re.search(rx,s,re.I)]
    if not matches:
        print("V341_CROP_NOT_LOCATED "+json.dumps({"id":key,"page":page,"sample_words":[x[0] for x in words[:24]]}),flush=True)
        continue
    s,(x1,y1,x2,y2)=matches[0]
    cx=(x1+x2)//2;cy=(y1+y2)//2
    width=min(1950,im.width);height=min(410,im.height)
    left=max(0,min(cx-width//2,im.width-width))
    top=max(0,min(cy-height//2,im.height-height))
    crop=im.crop((left,top,left+width,top+height))
    # Labels occupy their own separate strip; original crop pixels not manipulated.
    lab=Image.new("RGB",(width,45),"white")
    draw=ImageDraw.Draw(lab)
    draw.text((14,13),f"{key} / {article} / 1531 BSB Canvas {page} / institutional hOCR search '{s}'",fill="black")
    panel=Image.new("RGB",(width,height+45),"white");panel.paste(lab,(0,0));panel.paste(crop,(0,45))
    crops.append(panel)
    print("V341_CROP "+json.dumps({"id":key,"canvas":page,"hocr_token":s,"bbox":[x1,y1,x2,y2],"crop":[left,top,left+width,top+height],"image_crop_is_facsimile":True}),flush=True)
if not crops:
    sys.exit("No crops could be located")
w=max(x.width for x in crops)
montage=Image.new("RGB",(w,sum(x.height for x in crops)+18*(len(crops)-1)),(236,236,236))
y=0
for im in crops:montage.paste(im,(0,y));y+=im.height+18
buf=io.BytesIO();montage.save(buf,format="JPEG",quality=78,optimize=True)
encoded=base64.b64encode(buf.getvalue()).decode("ascii")
print("V341_CONTACT_SHEET_INFO "+json.dumps({"witness":OBJECT,"panels":len(crops),"image_size":[montage.width,montage.height],"jpeg_bytes":len(buf.getvalue()),"status":"FACSIMILE_EXCERPTS_FOR_VISUAL_SCHOLARLY_REVIEW_NOT_PUBLISHED","comparison_with_CR26_1858":False}),flush=True)
for i in range(0,len(encoded),1500):
    print(f"V341_CONTACT_SHEET_CHUNK {i//1500:05d} {encoded[i:i+1500]}",flush=True)
print("V341_FACSIMILE_CAPTURED_REVIEW_PENDING",flush=True)
