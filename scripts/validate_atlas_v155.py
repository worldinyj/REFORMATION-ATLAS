#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/"data/deep/atlas_v155_ten_reader_pages.json").read_text(encoding="utf-8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert len(d["pages"])==10
assert len({p["id"] for p in d["pages"]})==10
assert all(len(p["sections"])==3 and len(p["discussion_questions"])==2 for p in d["pages"])
assert all(len(p["source_urls"])>=2 and all(s.startswith("https://") for s in p["source_urls"]) for p in d["pages"])
assert all(p["primary_text_collated"] is False and p["editorial_status"]=="PENDING_EXPERT_REVIEW" for p in d["pages"])
assert (root/"docs/01_CONTENT/V155_TEN_IN_DEPTH_READER_PAGES.md").exists()
print("PASS V1.55: 10 reader pages, 30 sections, 20 questions, provenance and publication hold")
