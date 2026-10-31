#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/"data/contracts/atlas_v158_visual_rights_registry.json").read_text(encoding="utf-8"))
pages=json.loads((root/"data/deep/atlas_v156_extended_narratives.json").read_text(encoding="utf-8"))
ids={p["id"] for p in pages["pages"]}
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert len(d["assets"])==14
assert len({x["id"] for x in d["assets"]})==14
assert all(x["reader_page_id"] in ids for x in d["assets"])
assert all(not x["approved_to_publish"] and not x["image_downloaded"] for x in d["assets"])
assert all(x["rights_statement_uri"] is None and x["license_review"]=="NOT_EVALUATED" for x in d["assets"])
print("PASS V1.58: 14 candidates, all reader links valid, no unreviewed image licensed for use")
