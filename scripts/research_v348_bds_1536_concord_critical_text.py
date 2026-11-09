#!/usr/bin/env python3
"""V3.48 bounded critical edition HTML text audit (BDS 6/1 printed pp 120–126).
The 1988 editor's transcribed reading is *not* a 1536 autograph.
Single attempt per page, cite page URLs, print limited context only, no files/images saved.
"""
from urllib.request import Request,urlopen
from html import unescape
import json,re
from html.parser import HTMLParser
class Extract(HTMLParser):
 def __init__(self):super().__init__();self.lines=[];self.ignore=0
 def handle_starttag(self,tag,attrs):
  if tag in ['script','style']: self.ignore+=1
 def handle_endtag(self,tag):
  if tag in ['script','style']:self.ignore=max(0,self.ignore-1)
 def handle_data(self,s):
  if not self.ignore:self.lines.append(s)
targets=[124,125,126,127,128,129,130]
words=['Confitentur','Irenaei','cum pane','sacramentali','indign','Exhiberi','Eucharistiam','coelesti','substantialiter','merely']
for n in targets:
 u=f'https://digi.hadw-bw.de/view/bds6_1/{n:04d}?ui_lang=eng'
 try:
  with urlopen(Request(u,headers={'User-Agent':'REFORMATION-ATLAS-V348-Source-Audit/1.0','Accept':'text/html'}),timeout=20) as r:
   raw=r.read(750000);status=r.status;real=r.geturl()
  p=Extract();p.feed(raw.decode('utf8','replace'))
  text=re.sub(r'\s+',' ',unescape(' '.join(p.lines))).strip()
  hits=[]
  for w in words:
   for m in list(re.finditer(re.escape(w),text,re.I))[:3]:
    hits.append({'word':w,'context':text[max(0,m.start()-170):min(len(text),m.end()+300)]})
  print('V348_BDS_HTML '+json.dumps({'path_page':n,'url':u,'final_url':real,'http':status,
    'html_bytes':len(raw),'text_chars':len(text),'hits':hits[:15],
    'evidence_grade':'CRITICAL_EDITION_HTML_TRANSCRIPTION_NOT_CONTEMPORARY_FACSIMILE'},ensure_ascii=False),flush=True)
 except Exception as e: print('V348_BDS_FAIL '+json.dumps({'path_page':n,'url':u,'error':str(e)[:190]}),flush=True)
print('V348_END editorial reading only; 1536 autograph and CR III 1836 facsimile remain unverified')
