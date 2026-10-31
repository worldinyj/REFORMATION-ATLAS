#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/"data/deep/atlas_v151_wyclif_facs_access_result.json").read_text(encoding="utf8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert d["edition"]["direct_pdf_access"]=="BLOCKED_OFFHOST_REDIRECT"
assert d["edition"]["facsimile_verified"] is False
assert len(d["targets"])==2
assert all(x["verified_against_page_image"] is False for x in d["targets"])
assert d["introduction"]["manuscript_sigla_extracted"] is False
assert d["introduction"]["three_complete_witness_shelfmarks"]==[]
print("PASS: V1.51 no false facsimile or manuscript collation claims")
