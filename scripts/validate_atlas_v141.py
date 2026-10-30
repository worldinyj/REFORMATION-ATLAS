#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/"data/contracts/atlas_v141_identity_audit.json").read_text(encoding="utf8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert len(d["findings"])==3
assert d["audit_scope"].startswith("Targeted")
assert all(x["auto_apply"] is False for x in d["findings"])
assert d["findings"][0]["document_id"]=="OV-D-005"
print("PASS: V1.41 targeted identity audit findings and hold")
