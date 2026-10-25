#!/usr/bin/env python3
"""Read-only source-level checks for VOL-04 copy evidence (not text collation)."""
import json
from pathlib import Path
from urllib.parse import urlparse
R=Path(__file__).resolve().parents[1]
def load(x): return json.loads((R/x).read_text(encoding="utf-8"))
def validate(evidence,splits):
    errors=[]
    children={c["split_key"] for g in splits["groups"] for c in g["children"]}
    targets=evidence["review_targets"]
    keys=[x["split_key"] for x in targets]
    if len(set(keys))!=len(keys) or not set(keys)<=children: errors.append("unknown or duplicated split key")
    if evidence["publication_approved"] or evidence["full_text_collation_completed"]: errors.append("invalid release status")
    for target in targets:
        if not target["evidence"]: errors.append("missing evidence")
        for entry in target["evidence"]:
            u=urlparse(entry["url"])
            if u.scheme!="https" or not u.netloc: errors.append("invalid HTTPS source")
            if not all(entry.get(k) for k in ("institution","holding","finding","limit")): errors.append("missing provenance detail")
    if "1918" not in str(targets) or "MUST NOT" not in str(targets): errors.append("reprint distinction missing")
    if "BRA0930" not in str(targets) or "BRA2651/A-B" not in str(targets): errors.append("copy records missing")
    return sorted(set(errors))
if __name__=="__main__":
    errs=validate(load("data/deep/vol04_copy_evidence_v01.json"),load("data/deep/vol04_split_proposals_v01.json"))
    for x in errs: print("FAIL",x)
    if not errs: print("PASS catalog provenance; no full-text collation or publication permission")
    raise SystemExit(bool(errs))
