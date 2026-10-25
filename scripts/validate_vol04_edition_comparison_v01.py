#!/usr/bin/env python3
"""Read-only edition comparison assertions. Never authorizes publication."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
data=json.loads((root/"data/deep/vol04_edition_comparison_v01.json").read_text(encoding="utf-8"))
cases={c["case_id"]:c for c in data["comparison_cases"]}
assert data["publication_approved"] is False and data["source_text_collated"] is False
assert len(cases)==3
assert [(e["year"],e["chapters"]) for e in cases["VOL04-CMP-001"]["editions"]]==[(1536,6),(1539,17),(1559,80)]
assert cases["VOL04-CMP-001"]["work_family"]=="OV-D-012"
assert [e["month"] for e in cases["VOL04-CMP-002"]["editions"]]==[9,12]
assert cases["VOL04-CMP-002"]["type"]=="ICONOGRAPHIC_VARIANT"
assert cases["VOL04-CMP-003"]["work_family"]=="OV-D-011"
assert cases["VOL04-CMP-003"]["evidence_level"]=="SECONDARY_COMPARISON_UNCOLLATED"
for c in cases.values():
    assert c["sources"] and c["observation_ko"] and c["interpretation_ko"]
    assert all(x.startswith("https://") for x in c["sources"])
print("PASS: 3 research-only edition comparisons; no source collation or public release")
