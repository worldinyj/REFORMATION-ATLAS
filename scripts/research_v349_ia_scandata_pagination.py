#!/usr/bin/env python3
"""ATLAS V3.49 physical scan leaf -> print page mapping using Internet Archive original scannedata XML.
No OCR and no image download, one request per URL, no retries.
"""
import urllib.request,xml.etree.ElementTree as ET,json
id="philippimelantho03mela"
urls=[
 f"https://archive.org/download/{id}/{id}_scandata.xml",
 f"https://ia800902.us.archive.org/12/items/{id}/{id}_scandata.xml"
]
for u in urls:
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"REFORMATION-ATLAS-V349-PAGINATION/1.0","Accept":"application/xml,text/xml"}),timeout=35) as r:
   raw=r.read(1200000)
  print("V349_SCAN_XML "+json.dumps({"url":u,"bytes":len(raw),"head":raw[:150].decode("utf8","replace")}),flush=True)
  root=ET.fromstring(raw)
  ps=[]
  for page in root.iter("page"):
   leaf=page.attrib.get("leafNum")
   pn=page.findtext("pageNumber")
   t=page.findtext("pageType")
   ps.append({"leaf":leaf,"number":pn,"type":t})
  keep=[p for p in ps if p["number"] in ("75","76","77","78")];
  print("V349_TARGETS "+json.dumps({"all_pages":len(ps),"hits":keep,"first":ps[:18],"samples":ps[76:110:5]},ensure_ascii=False),flush=True)
  break
 except Exception as e:print("V349_SCAN_FAIL "+json.dumps({"url":u,"error":str(e)[:200]}),flush=True)
print("V349_SCAN_END cannot claim facsimile until original source leaves seen",flush=True)
