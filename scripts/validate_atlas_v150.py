#!/usr/bin/env python3
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"data/deep/atlas_v150_wyclif_print_access_locator.json"
d=json.loads(p.read_text(encoding="utf-8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert d["edition_1886"]["internet_archive_item"]=="tractatusdeeccl00wycl"
assert len(d["pagination_probes"])==2
assert not d["edition_1886"]["print_page_images_directly_read"]
assert all(not r["verified_by_direct_scan"] for r in d["pagination_probes"])
assert d["critical_witness_status"]["three_complete_manuscript_shelfmarks"]==[]
print("PASS: edition identifier and original-image gate")
