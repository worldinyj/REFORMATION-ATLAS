#!/usr/bin/env python3
"""Generate research-only canonical long-reader view from existing approved-for-research drafts."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_text(encoding="utf8")
def data(p):return json.loads(read(p))
wh=read("docs/01_CONTENT/V171_DEEP_READER_WYCLIFFE_HUS.md")
lu=read("docs/01_CONTENT/V172_LUTHER_1517_1521_FULL_READER.md")
patterns=[
 ("WYCLIFFE","V156-Wycliffe",wh,r"## I\. .*?(?=\n## II\.)"),
 ("HUS","V156-Hus",wh,r"## II\. .*?(?=\n---|\Z)"),
 ("LUTHER1517","V156-Luther1517",lu,r"## 1장\. .*?(?=\n## 2장\.)"),
 ("LUTHER1521","V156-Luther1521",lu,r"## 2장\. .*?(?=\n## 출처와 연구 상태)")
]
chapters=[]
orig={x['id']:x for x in data("data/deep/atlas_v156_extended_narratives.json")['pages']}
for key,source,raw,pat in patterns:
 m=re.search(pat,raw,re.S)
 assert m, key
 block=m.group().strip()
 lines=block.splitlines()
 title=lines[0].replace("## ","",1)
 # Only text prose counts, excluding Markdown headings, formatting and bibliography.
 paragraphs=[p.strip() for p in re.split(r"\n\s*\n",block) if p.strip() and not p.startswith("#") and not p.startswith("**연구 출처:")]
 clean="\n\n".join(paragraphs)
 textcount=len(re.sub(r"\s","",clean))
 chapters.append({"key":key,"source_id":source,"title":title,"format":"MARKDOWN_PROSE","body":block,"body_chars_no_whitespace":textcount,"source_urls":orig[source]["source_urls"],"primary_original_collated":False,"peer_reviewed":False,"can_publish":False})
for name,path in [
 ("MARBURG","data/deep/atlas_v174_marburg_source_anchored_reader.json"),
]: 
 d=data(path)
 text="\n\n".join(x["text"] for x in d["sections"])
 chapters.append({"key":name,"source_id":d["source_id"],"title":d["title"],"format":"SECTION_TEXT","body":text,"body_chars_no_whitespace":len(re.sub(r"\s","",text)),"source_urls":[e["url"] for e in d["evidence"]],"primary_original_collated":False,"peer_reviewed":False,"can_publish":False})
for path in ["data/deep/atlas_v176_three_edition_readers_final_draft.json","data/deep/atlas_v176_zurich_trent_reader_2000plus.json"]:
 for d in data(path)["chapters"]:
  text="\n\n".join(s["text"] for s in d["sections"])
  key=d["key"];source={"AUGSBURG":"V156-Augsburg","CALVIN1536":"V156-Calvin1536","CALVIN1559":"V156-Calvin1559","ZWINGLI":"V156-Zwingli","TRENT":"V156-Trent"}[key]
  chapters.append({"key":key,"source_id":source,"title":d["title"],"format":"SECTION_TEXT","body":text,"body_chars_no_whitespace":len(re.sub(r"\s","",text)),"source_urls":d.get("sources",d.get("urls",orig[source]["source_urls"])),"primary_original_collated":False,"peer_reviewed":False,"can_publish":False})
assert len(chapters)==10 and {c["source_id"] for c in chapters}==set(orig)
output={"version":"1.77","publication_gate":{"can_ship":False,"scholarly_approval":False},"counting_policy":"whitespace-excluded Korean prose characters; paragraphs and references excluded where possible","chapters":chapters}
dest=R/"data/deep/atlas_v177_unified_ten_reader_drafts.json"
dest.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("Unified 10 readers, prose counts:",[(c["key"],c["body_chars_no_whitespace"]) for c in chapters])
