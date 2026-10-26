#!/usr/bin/env python3
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]
d=json.loads((p/"data/deep/vol04_manuscript_edition_reaudit_v02.json").read_text())
assert not d["publication_approved"]
assert all(v=="LOST_OR_UNLOCATED" for v in (d["manuscript_1530"]["original_german"],d["manuscript_1530"]["original_latin"]))
assert d["manuscript_1530"]["distinct_from_printed_copies"]
assert len(d["printed_1530"])==4 and all(x["kind"]!="submission_manuscript" for x in d["printed_1530"])
assert d["luther_1522"]["september_original_copy_shelfmark"] is None
assert not d["luther_1522"]["same_edition"]
assert d["calvin"]["work_id"]=="OV-D-012" and not d["calvin"]["text_collated"]
assert d["calvin"]["latin_editions"]==[1536,1539,1543,1550,1559]
assert d["calvin"]["french_editions"]==[1541,1545,1551,1560]
print("PASS: 1530 manuscript/print boundaries, Luther copy uncertainty, Calvin family; publication blocked")
