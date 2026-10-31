import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((R/p).read_text(encoding="utf8"))
a=load("data/deep/atlas_v176_three_edition_readers_final_draft.json")["chapters"]
b=load("data/deep/atlas_v176_zurich_trent_reader_2000plus.json")["chapters"]
v=load("data/deep/atlas_v175_three_edition_readers.json")["chapters"]
assert len(a)==3 and len(b)==2
assert {x["key"] for x in a+b}=={"AUGSBURG","CALVIN1536","CALVIN1559","ZWINGLI","TRENT"}
for x in a+b:
 assert x["body_chars"]==sum(len(p["text"]) for p in x["sections"])
 assert x["body_chars"]>=2000 and x["can_publish"] is False
 assert x.get("original_facsimile_collated",x.get("primary_original_collated")) is False
 assert len(x["sections"])>=8
 assert all(p["heading"] and p["text"] for p in x["sections"])
assert all(x["body_chars"]>next(y["body_chars"] for y in v if y["key"]==x["key"]) for x in a)
assert all(x["urls"] and all(url.startswith("https://") for url in x["urls"]) for x in b)
print("PASS V176: five 2000+-char reader drafts, gate closed, predecessor preserved")
print([(x["key"],x["body_chars"]) for x in a+b])
