#!/usr/bin/env python3
"""V3.46: single bounded metadata-and-access probe for independent 1540 Confessio print.
No retries, no source images stored, no repository data edits, no publication.
OCR/search snippets do NOT count as direct printed-page reading.
"""
import urllib.request, urllib.error, urllib.parse, json, re, html
TARGETS=[
("GOOGLE_CATALOG","https://books.google.com/books/about/Confessio_fidei_exhibita_invictiss_imp_C.html?id=HmpoAAAAcAAJ"),
("GOOGLE_TEXT","https://books.google.com/books?id=HmpoAAAAcAAJ&output=text&printsec=frontcover"),
("GOOGLE_SEARCH","https://books.google.com/books?jscmd=SearchWithinVolume2&q=exhibeantur&vid=HmpoAAAAcAAJ"),
("GOOGLE_PAGE","https://books.google.com/books?id=HmpoAAAAcAAJ&pg=PA10"),
("HALLE_URN","https://digitale.bibliothek.uni-halle.de/urn/urn:nbn:de:gbv:3:1-143262"),
("HALLE_RESOLVER","https://nbn-resolving.de/urn:nbn:de:gbv:3:1-143262"),
("MDZ_REGENSBURG","https://www.digitale-sammlungen.de/de/search?query=Theol.syst.33"),
("MDZ_BAMBERG","https://www.digitale-sammlungen.de/de/search?query=.10%20D%2014"),
]
class BoundedRedirect(urllib.request.HTTPRedirectHandler):
 def __init__(self):self.n=0
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  self.n+=1
  if self.n>3:raise urllib.error.HTTPError(newurl,code,"redirect depth limit",headers,fp)
  if not newurl.startswith("https://"):raise urllib.error.HTTPError(newurl,code,"HTTPS required",headers,fp)
  return super().redirect_request(req,fp,code,msg,headers,newurl)
for label,url in TARGETS:
 opener=urllib.request.build_opener(BoundedRedirect())
 try:
  with opener.open(urllib.request.Request(url,headers={"User-Agent":"REFORMATION-ATLAS-v346-metadata-audit/1.0","Accept":"text/html,application/json;q=0.9"}),timeout=15) as resp:
   raw=resp.read(400000); final=resp.geturl(); code=resp.status; typ=resp.headers.get("Content-Type","")
  t=raw.decode("utf-8","replace")
  title=re.search(r"<title[^>]*>(.*?)</title>",t,re.I|re.S)
  links=re.findall(r"""(?:href|src)\s*=\s*['"]([^'"]{5,300})['"]""",t,re.I)
  cand=[html.unescape(x) for x in links if re.search(r"(?:bsb\d{8}|iiif|manifest|reader\?|\.pdf|\.jpg|google|/page/|/content/)",x,re.I)]
  uniq=list(dict.fromkeys(cand))[:12]
  snippet=re.sub(r"\s+"," ",re.sub(r"<[^>]*>"," ",t))[:320]
  print("V346_ACCESS "+json.dumps({"id":label,"status":code,"url":url,"final_url":final,"content_type":typ,"bytes_sample":len(raw),"title":html.unescape(title.group(1))[:180] if title else None,"candidate_links":uniq,"snippet":html.unescape(snippet),"direct_print_letter_seen":False},ensure_ascii=False),flush=True)
 except Exception as e:
  print("V346_ACCESS "+json.dumps({"id":label,"status":0,"url":url,"error":str(e)[:230],"direct_print_letter_seen":False}),flush=True)
print("V346_GATE metadata/access probe only. Do not upgrade any exemplar to direct visual reading.",flush=True)
